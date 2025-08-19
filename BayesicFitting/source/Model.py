from __future__ import print_function

import numpy as numpy
import random
from astropy import units
import warnings

from .FixedModel import FixedModel
#from .Prior import Prior
#from .UniformPrior import UniformPrior
from . import Tools
from .Formatter import formatter as fmt
from .Formatter import fma
from .Tools import setAttribute as setatt

__author__ = "Do Kester"
__year__ = 2025
__license__ = "GPL3"
__version__ = "3.2.4"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Perpetual Beta"

#  * This file is part of the BayesicFitting package.
#  *
#  * BayesicFitting is free software: you can redistribute it and/or modify
#  * it under the terms of the GNU Lesser General Public License as
#  * published by the Free Software Foundation, either version 3 of
#  * the License, or ( at your option ) any later version.
#  *
#  * BayesicFitting is distributed in the hope that it will be useful,
#  * but WITHOUT ANY WARRANTY; without even the implied warranty of
#  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  * GNU Lesser General Public License for more details.
#  *
#  * The GPL3 license can be found at <http://www.gnu.org/licenses/>.
#  *
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2003 - 2011 Do Kester, SRON (JAVA code)
#  *    2016 - 2025 Do Kester


class Model( FixedModel ):
    """
    Model implements the common parts of (compound) models.
    It is the last common anchestor of all Models.

    Models can be handled by the Fitter classes.

    A model consists of one or more instantiations of (base) models which
    are concatenated in a chain of models using various operations
    (+-*/). A special operation is the pipe (|). It works like a unix pipe,
    i.e. the output of the left-hand process in used as input of the
    right-hand process.

    Methods defined in BaseModel as eg. baseResult() are recursively called
    here as result(). They are the ones used in the fitters.

    The Model is the place where model-related items are kept, like parameters,
    stdevs.

    Model also implements a numerical derivation of partial to be
    used when partial is not given in the model definition itself. This same
    numerical derivation of partial is used in testPartial to indeed test
    whether the partial has been implemented properly.

    Example:
    --------
    >>> x = numpy.arange( 10 )
    >>> poly = PolynomialModel( 2 )             # quadratic model
    >>> poly.parameters = [3,2,1]               # set the parameters for the model
    >>> y = poly( x )                           # evaluate the model at x
    >>> p0 = poly[0]                            # 3: the first parameter
    >>>
    >>> # To make a compound model consisting of a gaussian and a constant background
    >>>
    >>> gauss = GaussModel( )                   # gaussian model
    >>> gauss += PolynomialModel( 0 )           # gaussian on a constant background
    >>> print( gauss.getNumberOfParameters( ) )
    >>> 4
    >>>
    >>> # Set limits to this model
    >>>
    >>> lolim = [0,-10,0,-5]                    # lower limits for the parameters
    >>> hilim = [10,10,2, 5]                    # high limits for parameters
    >>> gauss.setLimits( lolim, hilim )         # set limits. Does not work with all Fitters
    >>>
    >>> # Pipe a model; The order of operation matters.
    >>> # m5 = ( m1 | m2 ) + m3
    >>>
    >>> m1 = PolynomialModel( 1 )               # m1( x, p )
    >>> m2 = SineModel()                        # m2( x, q )
    >>> m3 = PolynomialModel( 0 )               # m3( x, r )
    >>> m4 = m1 | m2                            # m2( m1( x, p ), q )
    >>> m5 = m4 + m3                            # m2( m1( x, p ), q ) + m3( x, r )
    >>> print( m5.parameters )                  # [p, q, r]
    >>>
    >>> # Implicit brackets
    >>> # m5 = m1 | ( m2 + m3 )
    >>>
    >>> m1 = PolynomialModel( 1 )               # m1( x, p )
    >>> m2 = SineModel()                        # m2( x, q )
    >>> m3 = PolynomialModel( 0 )               # m3( x, r )
    >>> m4 = m2 + m3                            # m2( x, q ) + m3( x, r )
    >>> m5 = m1 | m4                            # m2( m1( x, p ), q ) + m3( m1( x, p ), r )
    >>> print( m5.parameters )                  # [p, q, r]

    Attributes
    ----------
    parameters : array_like
        parameters of the model
    stdevs : None or array_like
        standard deviations after a fit to the data
    xUnit : astropy.units or list of
        unit of the x-values (list of in case of more dimensions)
    yUnit : astropy.units
        unit of the y-values
    npars : int (read only)
        number of parameters in this model
    npchain : int (read only)
        identical to npars

    Attributes from FixedModel
    --------------------------
        npmax, fixed, parlist, mlist

    Attributes from BaseModel
    --------------------------
        npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames

    Author       Do Kester

    """

    NOP = 0
    ADD = 1
    SUB = 2
    MUL = 3
    DIV = 4
    PIP = 5

    #  *****CONSTRUCTOR*********************************************************
    def __init__( self, nparams=0, ndim=1, copy=None, params=None, **kwargs ):
        """
        Initializes the Model with all attributes set to None, except for
        the parammeters which are all initialized to 0.

        Parameters
        ----------
        nparams : int
            the number of parameters in this model
        ndim : int
            the dimensionality of the xdatas (default: 1)
        copy : Model
            model to be copied (default: None)
        params : array_like
            initial parameters of the model
        fixed : None or dictionary of {int:float|Model}
            int         index of parameter to fix permanently.
            float|Model values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
            See: @FixedModel

        """
        super( Model, self ).__init__( nparams=nparams, ndim=ndim, copy=copy,
                            **kwargs )

        setatt( self, "_next", None )
        setatt( self, "_head", self )

        if params is None :
            params = numpy.zeros( nparams, dtype=float )
        else :
            params = Tools.toArray( params, dtype=float )
        setatt( self, "parameters", self.select( params ), type=float, islist=True )

        nparams = self.npbase                       # accounting len( fixed )
        setatt( self, "_npchain", nparams )
        setatt( self, "stdevs", None )

        # xUnit is by default a (list[ndim] of) scalars, unitless
        xUnit = units.Unit( 1.0 ) if ndim == 1 else [units.Unit( 1.0 )]*ndim
        setatt( self, "xUnit", xUnit )
        setatt( self, "yUnit", units.Unit( 1.0 ) )                  # scalar
        setatt( self, "_operation", self.NOP )

        if copy is None : return

        ## the head has been copied; append now the rest of the chain
        last = copy._next
        while last is not None:
            self.appendModel( last.isolateModel( 0 ), last._operation )
            last = last._next

        setatt( self, "_npchain", copy._npchain )
        if copy.parameters is not None :
            setatt( self, "parameters", copy.parameters.copy() )
        if copy.stdevs is not None :
            setatt( self, "stdevs", copy.stdevs.copy() )

        setatt( self, "xUnit", copy.xUnit )
        setatt( self, "yUnit", copy.yUnit )

    def copy( self ):
        """ Return a copy.  """
        return Model( copy=self )

    def __setattr__( self, name, value ):
        """
        Set attributes.

        Parameters
        ----------
        name :  string
            name of the attribute
        value :
            value of the attribute

        """

        if name in ['parameters', 'stdevs'] :
            if value is not None and Tools.length( value ) != self.npchain :
                raise ValueError( "%s: Nr of %s does not comply. expect %d; got %d" %
                                ( self.shortName(), name, self.npchain, Tools.length( value ) ) )
            setatt( self, name, value, type=float, islist=True, isnone=True )

        elif name in ['xUnit', 'yUnit'] :
            isl = ( name == 'xUnit' and self.ndim > 1 )
            setatt( self, name, value, type=units.core.UnitBase, islist=isl, isnone=True )

        elif name in ['pipePartial', 'pipeDeriv'] :
            setatt( self, name, value )

        else :
            super( Model, self ).__setattr__( name, value )

    def __getattr__( self, name ) :
        """
        Return value belonging to attribute with name.

        Parameters
        ----------
        name : string
            name of the attribute
        """
        if name == 'npars' or name == 'npchain' :
            return self._head._npchain
        elif name == 'ndout' :
            return 1
        elif name == 'lastndout' :
            last = self
            while last._next is not None : last = last._next
            return last.ndout

        return super( Model, self ).__getattr__( name )


    def chainLength( self ):
        """ Return length of the chain.  """
        last = self
        i = 0
        while last is not None:
            last = last._next
            i += 1
        return i

    def isNullModel( self ) :
        """
        Return True if the model has no parameters (a NullModel).
        """
        return len( self.parameters ) == 0

    def isolateModel( self, k ):
        """
        Return a ( isolated ) copy of the k-th model in the chain.
        Fixed parameters and priors which might be present in the compound model
        will be lost in the isolated model.

        Parameters
        ----------
        k : int
            the model number ( head = 0 )

        Raises
        ------
        IndexError when the chain is shorter than k.

        """
        last = self
        i = 0
        np = 0
        while last is not None:
            if i == k :
                next = last._next               #  save

                setatt( last, "_next", None )   #  isolate
                head = last._head               #  save
                setatt( last, "_head", last )   #  isolate
                mdl = last.copy()               #  copy
                setatt( last, "_next", next )   #  restore
                setatt( last, "_head", head )
                setatt( mdl, "_operation", self.NOP )

                n2 = np + last.npbase
                # hard overwrite of the base parameters (over the chain parameters)
                setatt( mdl, "parameters", self._head.parameters[np:n2] )

                if self.stdevs is not None :
                    setatt( mdl, "stdevs", self._head.stdevs[np:n2] )
                else :
                    setatt( mdl, "stdevs", None )
                setatt( mdl, "_npchain", mdl.npbase )      # only extract one model
                return mdl

            np += last.npbase
            last = last._next
            i += 1
        raise IndexError( "There are only %d models in this compound model" % i )

    #  *************************************************************************
    def addModel( self, model ):
        """
        Make a compound model by concatinating/adding model to this.

        The final result is the sum of the individual results.

        The compound model is implemented as a chain of Models.
        Each of these base models contain the attributes ( parameters, limits etc. )
        and when needed these attributes are taken from there, or stored there.

        The operation (addition in this case) is always with the total result of the
        existing chain. For the use of "brackets" in a chain use BracketModel.

        Parameters
        ----------
        model : Model
            model to be added to

        """
        self.appendModel( model, self.ADD )

    def subtractModel( self, model ):
        """
        Make a compound model by concatinating/subtracting a model from this.

        The final result is the difference of the models.

        Parameters
        ----------
        model : Model
            model to be subtracted from

        """
        self.appendModel( model, self.SUB )

    def multiplyModel( self, model ):
        """
        Make a compound model by concatinating/multiplying a model with this.

        The final result is the product of the models.

        Parameters
        ----------
        model : Model
            model to be multiplied by

        """
        self.appendModel( model, self.MUL )

    def divideModel( self, model ):
        """
        Make a compound model by concatinating/dividing by a model.

        The final result is the division of the models.

        Parameters
        ----------
        model : Model
            model to be divided by

        """
        self.appendModel( model, self.DIV )

    def pipeModel( self, model ):
        """
        Make a compound model by piping the result into the next.

        Parameters
        ----------
        model : Model
            model to pipe into

        """
        self.appendModel( model, self.PIP )

    def appendModel( self, model, operation ):
        """
        Append a model to the present chain using a operation.

        Parameters
        ----------
        model : Model
            the model to be appended
        operation : int
            operation index

        Raises
        ------
        ValueError when a model of a different dimensionality is offered.
        """
        if self.isDynamic() and model.isDynamic():
            raise ValueError( "Only one Dynamic model in a chain" )
        if operation != self.PIP :
            opname = ["", "+", "-", "*", "/", "|" ]
            if self.ndim != model.ndim:
                raise ValueError( "Trying to combine incompatible model dimensions: %d %s %d"%
                                (self.ndim, opname[operation], model.ndim) )
        else :
            if self.lastndout != model.ndim :
                raise ValueError( "Trying to pipe incompatible models:  %d | %d"%
                                (self.lastndout, model.ndim) )
            model.selectPipe( self.ndim, model.ndim, model.ndout )

        if model._next is not None :
            model = Brackets( model )     # provide brackets if model is a chain

        last = self
        while last._next is not None:
            last = last._next
        setatt( last, "_next",  model )
        setatt( model, "_operation", operation )
        while last._next is not None:
            last = last._next
            setatt( last, "_head", self._head )

        setatt( self, "_npchain", len( self.parameters ) + len( model.parameters ) )

        setatt( self, "parameters", self._optAppend( self.parameters, model.parameters ) )

        # Erase the model's attributes; not needed anymore
        setatt( model, "parameters", None )

        return

    def _optAppend( self, x, y ) :
        if y is not None :
            if x is None : return y
            else : return numpy.append( x, y )
        else : return x

    #  *****CHECK**************************************************************
    def correctParameters( self, params ):
        """
        Check parameters for non-zero and positivity

        Parameters
        ----------
        params : array_like
            parameters for the model.

        """
        newpar = numpy.asarray( [], dtype=float )

        pp = self._recursiveCorrect( params, newpar )
        return pp

    def _recursiveCorrect( self, params, newpar ) :

        np = self.npbase
        newpar = numpy.append( newpar,  super( Model, self ).checkParameter( params[:np] ) )
        model = self._next
        if model is None :
            return newpar

        newpar = model._recursiveCorrect( params[np:], newpar )
        return newpar

    #  *****RESULT**************************************************************
    def result( self, xdata, param=None ):
        """
        Return the result of the model as applied to an array of input data.

        Parameters
        ----------
        xdata : array_like
            input data
        param : array_like
            parameters for the model. Default parameters from the Model

        """
        if param is None :
            param = self.parameters

        res = None
        xdata = Tools.toArray( xdata )
        return self._recursiveResult( xdata, param, res )

    def _recursiveResult( self, xdata, param, res ) :

        np = self.npbase

        if not self._operation == self.PIP :
            nextres = super( Model, self ).result( xdata, param[:np] )
        else :
            nextres = None
        res = self.operate( res, param[:np], nextres )
        model = self._next
        if model is None :
            return res

        res = model._recursiveResult( xdata, param[np:], res )
        return res

    def operate( self, res, pars, next ):
        if res is None or self._operation == self.NOP: # first one
            res = next
        elif self._operation == self.ADD:                 # NOP & ADD
            res = numpy.add( res, next )
        elif self._operation == self.SUB:
            res = numpy.subtract( res, next )
        elif self._operation == self.MUL:
            res = numpy.multiply( res, next )
        elif self._operation == self.DIV:
            res = numpy.divide( res, next )
        elif self._operation == self.PIP:
            res = super( Model, self ).result( res, pars )

        return res

    #  *****DERIVATIVE*********************************************************
    def derivative( self, xdata, param, useNum=False ):
        """
        Return the derivatives (df/dx) of the model at the inputs

        Parameters
        ----------
        xdata : array_like
            an input vector or array
        param : array_like
            parameters for the model
        useNum : bool
            if true, numeric derivatives are used.

        """
        result = None
        xdata = Tools.toArray( xdata )

        df = self._recursiveDerivative( xdata, param, result, 0,
                    useNum=useNum )
        return df

    def _recursiveDerivative( self, xdata, param, result, df, useNum=False ):
        """
        Workhorse for derivative.

        Implements the optional concatenation of models via recursion

        """
        np = self.npbase
        par = param[:np]
        nextres = None

#        if self.npmax > 0:            #  the base model has no parameters at all: skip
        xd = xdata if self._operation != self.PIP else result
        nextdf = ( super( ).numDerivative( xd, par ) if useNum else 
                       super( ).derivative( xd, par ) )

#        else :
#            nextdf = numpy.zeros_like( xdata, dtype=float )

#        print( "Model2  ", self.shortName(), df.shape, nextdf.shape, self._operation )

        isnotlist = self.ndim == 1 or self.ndout == 1
        if self._operation == self.NOP :
            df = nextdf

        elif self._operation == self.ADD :
            df = ( df + nextdf if isnotlist else 
                 [ d + n for d,n in zip( df, nextdf )] )

        elif self._operation == self.SUB :
            df = df - nextdf

        elif self._operation == self.MUL :
            nextres = super( Model, self ).result( xdata, par )
            df = df * nextres + nextdf * result

        elif self._operation == self.DIV :
            nextres = super( Model, self ).result( xdata, par )
            df = ( df * nextres - nextdf * result ) / ( nextres * nextres )

        elif self._operation == self.PIP :
#            nextres = 'dummy'           ## not needed, but needs something
            df = self.pipeDeriv( df, nextdf )
        else :
            raise ValueError( "Unknown operation: %d" & self.PIP )

        if self._next is None :
            return df
        if nextres is None:
            nextres = super( Model, self ).result( xdata, par )
        result = self.operate( result, par, nextres )

        #  append the dfs of the _next model
        model = self._next
        return model._recursiveDerivative( xdata, param[np:], result, df,
                    useNum=useNum )

    #  *****PARTIAL*************************************************************
    def partial( self, xdata, param, useNum=False ):
        """
        Return the partial derivatives of the model at the inputs

        Parameters
        ----------
        xdata : array_like
            an input vector or array
        param : array_like
            parameters for the model
        useNum : bool
            if true, numeric partials are used.

        """
#        print( "Partial ", self.shortName( ), self._operation )

        result = None
        partial = None
        xdata = Tools.toArray( xdata )
        partial = self._recursivePartial( xdata, param, 0, result,
                            partial, useNum=useNum )
        return partial

    def _recursivePartial( self, xdata, param, at, result, partial, useNum=False ):
        """
        Workhorse for partial.

        Implements the optional concatenation of models via recursion

        """
        np = self.npbase
        par = param[at:at+np]
        nextres = None

        xd = xdata if self._operation != self.PIP else result

        nextpartial = ( super( ).numPartial( xd, par ) if useNum else
                        super( ).partial( xd, par ) )

        if self._operation == self.SUB :
            nextpartial = numpy.negative( nextpartial )

        elif self._operation == self.MUL :
            nextres = super( Model, self ).result( xdata, par )
            partial = numpy.multiply( partial.transpose(), nextres ).transpose()
            nextpartial = numpy.multiply( nextpartial.transpose(), result ).transpose()

        elif self._operation == self.DIV :
            nextres = super( Model, self ).result( xdata, par )
            partial = numpy.divide( partial.transpose(), nextres ).transpose()
            invres = - result / ( nextres * nextres )
            nextpartial = numpy.multiply( nextpartial.transpose(), invres ).transpose()

        elif self._operation == self.PIP :

            # Need derivative: dHdG
            dHdG = ( super( ).numDerivative( result, par ) if useNum else 
                     super( ).derivative( result, par ) )

            partial = self.pipePartial( partial, dHdG )

        if not isinstance( partial, list ) :
            partial = ( nextpartial if partial is None
                    else numpy.append( partial, nextpartial, axis=1 ) )
        else :
            for k in range( len( partial ) ) :
                partial[k] = numpy.append( partial[k], nextpartial[k], axis=1 )

        model = self._next
        if model is None:
            return partial
        if nextres is None:
            nextres = super( Model, self ).result( xdata, par )

        result = self.operate( result, param[at:], nextres )
        #  append the partials of the _next model
        at += np
        return model._recursivePartial( xdata, param, at, result, partial,
                    useNum=useNum )


    def selectPipe( self,  ndim, ninter, ndout ) :
        """
        Select one of 9 pipe operations, depending on the dimensionality
        of the inputs and outputs of the model G and H

        Model G has pars p and model H has pars q.

         F(x:pq) ==>  H(G(x:p):q)            G(x:p) | H(*:q)   
         dF/dp   ==>  dH/dG * dG/dp          H.derivative(G,p) * G.partial(x,q)
         dF/dq   ==>  dH(G(x:p):q) / dq      G.partial(H,q)

         G.ndout mustbe H.ndim
         partial <== G
         dfdx    <== H

        Parameters
        ----------
        ndim : int
            input dimensions to G and thus to F
        ninter : int
            output dim of G and input dim to H (must be same)
        ndout : int
            output dimensions of H and thus of F
        """

        if ( ndim == 1 and ninter == 1 and ndout == 1 ) :
            self.pipePartial = self.pipe_0
            self.pipeDeriv   = self.pipe_4
        elif ( ndim > 1 and ninter == 1 and ndout == 1 ) :
            self.pipePartial =  self.pipe_0
            self.pipeDeriv   = self.pipe_0
       
        elif ( ndim == 1 and ninter > 1 and ndout > 1 ) :
            self.pipePartial = self.pipe_1
            self.pipeDeriv   = self.pipe_5

        elif ( ndim > 1 and ninter > 1 and ndout > 1 ) :
            self.pipePartial = self.pipe_1
            self.pipeDeriv   = self.pipe_1

        elif ( ndim == 1 and ninter > 1 and ndout == 1 ) :
            self.pipePartial = self.pipe_2
            self.pipeDeriv   = self.pipe_6

        elif ( ndim == 1 and ninter == 1 and ndout > 1 ) :
            self.pipePartial = self.pipe_3
            self.pipeDeriv   = self.pipe_7

        elif ( ndim > 1 and ninter > 1 and ndout == 1 ) :
            self.pipePartial = self.pipe_2
            self.pipeDeriv   = self.pipe_8

        elif ( ndim > 1 and ninter == 1 and ndout > 1 ) :
            self.pipePartial = self.pipe_3
            self.pipeDeriv   = self.pipe_9

        return


    ########################################################################
    # Next follow a number of pipe operations for partials.
    #    F( x:p,q ) = H( G( x:p ), q ) or
    #                 G( x:p ) | H( x:q )
    #    dF/dp = dH/dG * dG/dp
    #          = H.derive * G.partial
    #    dF/dx = dH/dG * dG/dx
    #          = H.derive * G.derivative
    # Different cases defined by the dimensions of of input partial
    # where N : number of datapoints x
    #       I : dimension of x (inputs)
    #       K : dimension of G (intermediate: out for G; in for H)
    #       O : dimension of F (outputs)
    #       P : number of parameters
    ########################################################################

    def pipe_0( self, dGd, dHdG ) :
        """
        ninter == 1 and ndout == 1

        Return partial in the form of [N,P]
        
        Parameters
        ----------
        dGd:  array of form [N,P]
            Either partial dGdp or derivative dGdx  
        dHdG: array of form [N]
            Derivative of H to G  
        """
        return numpy.multiply( dGd.transpose(), dHdG ).transpose()

    def pipe_1( self, dGd, dHdG ) :
        """
        ninter > 1 and ndout > 1

        Return partial in the form [O][N,P]
        
        Parameters
        ----------
        dGd:  array of form [K][N,P]
            Either partial dGdp or derivative dGdx  
        dHdG: array of form [O][N,K]
            Derivative of H to G  
        """
        part = []
        for dd in dHdG :
            pp = 0
            for k in range( len( dGd ) ) :
                pp += numpy.multiply( dGd[k].T, dd[:,k] )
            part += [pp.T]

        return part

    def pipe_2( self, dGd, dHdG ) :
        """
        ndim == 1 and ninter > 1 and ndout == 1

        Return partial in the form of [N,P]
        
        Parameters
        ----------
        dGd:  array of form [K][N,P]
            Either partial dGdp or derivative dGdx  
        dHdG: array of form [N,K]
            Derivative of H to G  
        """
        parr = numpy.asarray( dGd )
        part = numpy.zeros_like( dGd[0] )

        for k in range( dGd[0].shape[1] ) :
            part[:,k] = numpy.sum( dHdG.T * parr[:,:,k], axis=0 )
            
        return part

    def pipe_3( self, dGd, dHdG ) :
        """
        ndim == 1 and ninter = 1 and ndout > 1

        Return partial in the form of [O][NP]
        
        Parameters
        ----------
        dGd:  array of form [N,P]
            Either partial dGdp or derivative dGdx  
        dHdG: array of form [N,0]
            Derivative of H to G  
        """
        part = []
        for k in range( dHdG.shape[1] ) :
            part += [ numpy.multiply( dGd.transpose(), dHdG[:,k] ).transpose() ]

        return part

    def pipe_4( self, dGdx, dHdG ) :
        """
        ndim == 0 and ninter == 1 and ndout == 1

        Return partial in the form of [N]
        
        Parameters
        ----------
        dGdx: array of form [N]
            Derivative dGdx  
        dHdG: array of form [N]
            Derivative of H to G  
        """
        return dGdx * dHdG

    def pipe_5( self, dGdx, dHdG ) :
        """
        ndim == 1 and ninter > 1 and ndout > 1

        Return derivative in the form of [N,O]
        
        Parameters
        ----------
        dGdx:  array of form [N,K]
            Either partial dGdp or derivative dGdx  
        dHdG: array of form [O][N,K]
            Derivative of H to G  
        """
        darr = numpy.asarray( dHdG )
        part = numpy.zeros_like( darr[:,:,0] ).T

        for k in range( part.shape[1] ) :
            part[:,k] = numpy.sum( numpy.multiply( darr[k,:,:], dGdx ), axis=1 )

        return part

    def pipe_6( self, dGdx, dHdG ) :
        """
        ndim == 1 and ninter > 1 and ndout == 1

        Return derivative in the form of [N]
        
        Parameters
        ----------
        dGdx:  array of form [N,K]
            Either partial dGdp or derivative dGdx  
        dHdG: array of form [N,K]
            Derivative of H to G  
        """
        part = numpy.sum( numpy.multiply( dHdG, dGdx ), axis=1 )
        return part

    def pipe_7( self, dGdx, dHdG ) :
        """
        ndim == 1 and ninter = 1 and ndout > 1

        Return derivative in the form of [N,O]
        
        Parameters
        ----------
        dGdx:  array of form [N,O]
            Either partial dGdp or derivative dGdx  
        dHdG: array of form [N]
            Derivative of H to G  
        """
        part = numpy.multiply( dHdG.T, dGdx.T ).T

        return part

    def pipe_8( self, dGdx, dHdG ) :
        """
        ndim > 1 and ninter > 1 and ndout == 1

        Return derivative in the form of [N,I]
        
        Parameters
        ----------
        dGdx:  array of form [K][N,I]
            Either partial dGdp or derivative dGdx  
        dHdG: array of form [N,K]
            Derivative of H to G  
        """
        darr = numpy.asarray( dGdx )

        part = numpy.zeros_like( dGdx[0] )
        for k in range( part.shape[1] ) :
            part[:,k] = numpy.sum( numpy.multiply( dHdG.T, darr[:,:,k] ), axis=0 )

        return part

    def pipe_9( self, dGdx, dHdG ) :
        """
        ndim > 1 and ninter == 1 and ndout > 1

        Return derivative in the form of [O][N,I]
        
        Parameters
        ----------
        dGdx:  array of form [N,I]
            Either partial dGdp or derivative dGdx  
        dHdG: array of form [N,O]
            Derivative of H to G  
        """
        part = []
        for k in range( dHdG.shape[1] ) :
            part += [numpy.multiply( dGdx.T, dHdG[:,k] ).T]

        return part


    #  *****TOSTRING***********************************************************
    def __str__( self ):
        """ Returns a string representation of the model.  """
        return self._toString( )

    def _toString( self, indent="", npars=0 ) :
        opname = [" null\n", " +\n", " -\n", " *\n", " /\n", " |\n" ]
        np = self.npbase

        if self._next is None :
            return super( )._toString( npars=npars )

        return ( super( )._toString( npars=npars ) +
                 opname[self._next._operation] +
                 indent + self._next._toString( indent=indent, npars=npars+np ) )

    def shortName( self ) :
        """
        Return a short version the string representation: upto first non-letter.
        """
        opname = [" null\n", " + ", " - ", " * ", " / ", " | " ]
        if self._next is None :
            return super( ).shortName()

        return ( super( ).shortName( ) + opname[self._next._operation] +
                 self._next.shortName( ) )


    #  *****GET/SET*************************************************************
    def getNumberOfParameters( self ):
        """ Returns the number of parameters of the ( compound ) model.  """
        return len( self._head.parameters )

    #  *****NUMERIC DERIVATIVE*************************************************
    def numDerivative( self, xdata, param ):
        """
        Returns numerical derivatives (df/dx) of the model function.

        Parameters
        ----------
        xdata : array_like
            input data
        param : array_like
            a parameters vector

        """
        return self.derivative( xdata, param, useNum=True )

    #  *****NUMERIC PARTIAL****************************************************
    def numPartial( self, xdata, param ):
        """
        Returns numerical partial derivatives of the model function.

        Parameters
        ----------
        xdata : array_like
            input data
        param : array_like
            a parameters vector

        """
        return self.partial( xdata, param, useNum=True )

    def isDynamic( self ) :
        """
        Return whether the model can change the number of parameters dynamically.
        """
        if super( Model, self ).isDynamic() :
            return True
        elif self._next is not None :
            return self._next.isDynamic()

        return False

    #  *****PRIOR***************************************************************
    def hasPriors( self, isBound=True ) :
        """
        Return True when the model has priors for all its parameters.

        Parameters
        ----------
        isBound : bool
            Also check if the prior is bound.
        """
        hasp = True
        mdl = self
        while mdl is not None and hasp :
            hasp = hasp and super( Model, self ).hasPriors( isBound=isBound )
            mdl = mdl._next
        return hasp

    def getPrior( self, kpar ):
        """
        Return the prior of the indicated parameter.

        Parameters
        ----------
        kpar : int
            parameter number.

        Raises
        ------
        IndexError when kpar is larger than the number of parameters.

        """
        np = self.npbase
        if kpar < np:
            return super( Model, self  ).getPrior( kpar )
        elif self._next is not None:
            return self._next.getPrior( kpar - np )
        else:
            raise IndexError( "The (compound) model does not have %d parameters"%
                              ( kpar + 1 ) )

    def setPrior( self, kpar, prior=None, **kwargs ):
        """
        Set the prior for the indicated parameter.

        Parameters
        ----------
        kpar : int
            parameter number.
        prior : Prior
            prior for parameter kpar
        kwargs : keyword arguments
            attributes to be passed to the prior

        Raises
        ------
        IndexError when kpar is larger than the number of parameters.

        """
        np = self.npbase
        if kpar < np:
            super( Model, self  ).setPrior( kpar, prior=prior, **kwargs )
        elif self._next is not None:
            self._next.setPrior( kpar - np, prior=prior, **kwargs )
        else:
            raise IndexError( "The (compound) model does not have %d parameters"%
                              ( kpar + 1 ) )


    #  ***PARAMETER NAME *******************************************************
    def getParameterName( self, kpar ):
        """
        Return the name of the indicated parameter.

        Parameters
        ----------
        kpsr : int
            parameter number.

        Raises
        ------
        IndexError when kpar is larger than the number of parameters.

        """
        np = self.npbase
        if kpar < np:
            return super( Model, self ).getParameterName( kpar )
        elif self._next is not None:
            return self._next.getParameterName( kpar - np )
        else:
            raise IndexError( "The (compound) model does not have %d parameters."%
                               ( kpar + 1 ) )

    def getParameterUnit( self, kpar ):
        """
        Return the unit of the indicated parameter.

        Parameters
        ----------
        kpar : int
            parameter number.

        Raise
        -----
        IndexError when kpar is > number of parameters

        """
        np = self.npbase
        if kpar < np:
            return super( Model, self).getParameterUnit( kpar )
        elif self._next is not None:
            return self._next.getParameterUnit( kpar - np )
        else:
            raise IndexError( "The (compound) model does not have %d parameters."%
                               ( kpar + 1 ) )


    def getIntegralUnit( self ):
        """ Return the unit of the integral of the model over x. """

        unit = self.yUnit
        if isinstance( self.xUnit, list ) :
            for u in self.xUnit : unit *= u
        else : unit *= self.xUnit
        return unit


    #  *****LIMITS**************************************************************
    def setLimits( self, lowLimits=None, highLimits=None ):
        """
        Sets the limits for the parameters of the compound model.

        1. It is valid to insert for either parameter a None value
        indicating no lower/upper limits.
        2. When a lowerlimit >= upperlimit no limits are enforced.
        It only works in *Fitter classes which support it.

        Parameters
        ----------
        lowLimits : array_like
            lower limits on the parameters
        highLimits : array_like
            upper limits on the parameters

        """
        ml = 0
        if lowLimits is not None :
            lowLimits = Tools.toArray( lowLimits )
            nl = len( lowLimits )
            ml = max( ml, nl )
        if highLimits is not None :
            highLimits = Tools.toArray( highLimits )
            nh = len( highLimits )
            ml = max( ml, nh )
        if ml == 0 : return

        if ml > self.npchain :
            warnings.warn( "More limits given than parameters present: %d < %d" %
                            ( ml, self.npchain ) )

        for k in range( ml ) :
            lo = None if k >= nl else lowLimits[k]
            hi = None if k >= nh else highLimits[k]
            self.setPrior( k, limits=[lo,hi] )

    def getLimits( self ) :
        """
        Return the limits stored in the priors

        Returns
        -------
        limits : tuple of 2 array-like or of 2 None (if `self.priors` is None)
            (lowlimits, highlimits)

        lolim = []
        hilim = []
        mdl = self
        while mdl is not None :
            if not super( Model, mdl ).hasLimits( ) :
                return [None,None]
            lolim += [p.lowLimit for p in mdl.priors]
            hilim += [p.highLimit for p in mdl.priors]

            mdl = mdl._next
        return (lolim, hilim)
        """

        lolim = [self.getPrior(k).lowLimit for k in range( self.npchain )]
        hilim = [self.getPrior(k).highLimit for k in range( self.npchain )]
        return (lolim, hilim)




    #  *************************************************************************
    def hasLimits( self, fitindex=None ):
        """
        Return true if limits has been set for this model.

        Parameters
        ----------
        fitindex    list of indices to be fitted.

        """
        haslim = True
        mdl = self
        while mdl is not None :
            haslim = haslim and super( Model, mdl ).hasLimits( fitindex=fitindex )
            if not haslim :
                return haslim
            if fitindex is not None :
                q = numpy.where( fitindex >= mdl.npbase )
                fitindex = fitindex[q] - mdl.npbase
            mdl = mdl._next
        return haslim


    #  ****** UNIT <--> DOMAIN ********************************************
    def unit2Domain( self, uvalue, kpar=None ):
        """
        Convert a value in [0,1] to one inside the limits of the parameter.

        Parameters
        ----------
        uvalue : (list of) float
            value in [0,1]
        kpar : int
            index of the parameter

        """
        if kpar is not None :
            return self.getPrior( kpar ).unit2Domain( uvalue )


        pgen = self.nextPrior(  )
        dval = numpy.fromiter( ( next( pgen ).unit2Domain( uv ) for uv in uvalue ), float )
        try :
            pgen.close()
        except Exception :
            pass
        return dval


    def domain2Unit( self, dvalue, kpar=None ):
        """
        Convert a value within the domain of the parameter to one in [0,1].

        Parameters
        ----------
        dvalue : (list of) float
            value of parameter
        kpar : int
            index of the parameter

        """
        if kpar is not None :
            return self.getPrior( kpar ).domain2Unit( dvalue )

        pgen = self.nextPrior()
        uval = numpy.fromiter( ( next( pgen ).domain2Unit( dv ) for dv in dvalue ), float )
        try :
            pgen.close()
        except Exception :
            pass
        return uval

    def partialDomain2Unit( self, dvalue ):
        """
        Return a the derivate of the domain2Unit function to dval.

        Parameters
        ----------
        dvalue : (list of) float
           parameter array

        """
        pgen = self.nextPrior(  )
        part = numpy.fromiter( ( next( pgen ).partialDomain2Unit( dv ) for dv in dvalue ), float )
        try :
            pgen.close()
        except Exception :
            pass
        return part

    def nextPrior( self ) :
        mdl = self
        k = 0
        while True :
            try :
                yield mdl.priors[k]
            except Exception :
                yield mdl.priors[-1]
            k += 1
            if k >= mdl.npbase :
                mdl = mdl._next
                k = 0


    #  *****SOME DUMMY METHODS TO ALLOW LINEAR MODELS IN NONLIN FITTERS********
    def isMixed( self ):
        """ Return false.  """
        return False

    def getLinearIndex( self ):
        """ Return null.  """
        return None

    #  ***** PYTHON INTERFACES ****************************************************
    def __getitem__( self, i ):
        """
        Return the i-th parameter.

        >>> p_i = model[i]

        Parameters
        ----------
        i : int
            index for the parameter.

        """
        return self.parameters[i]

    def __call__( self, x ):
        """
        Return the result of the model.

        >>> y = model( x )
        is equivalent to
        >>> y = model.result( x, model.parameters )

        Parameters
        ----------
        x : (list of) float
            apply the model to x (as input)

        """
        return self.result( x, self.parameters )

    def __iadd__( self, model ):
        """
        Method for making compound models using += operator.

        >>> model1 += model2

        Parameters
        ----------
        model : Model
            a model to add to self (the existing chain)

        """
        self.addModel( model )
        return self

    def __add__( self, model ):
        """
        Method for making compound models using + operator.

        >>> model1 = model2 + model3

        Parameters
        ----------
        model : Model
            a copy of model to add to a copy of self (the existing chain)

        """
        return self.copy().__iadd__( model.copy() )

    def __isub__( self, model ):
        """
        Method for making compound models using -= operator.

        >>> model1 -= model2

        Parameters
        ----------
        model : Model
            a model to subtract from self (the existing chain)

        """
        self.subtractModel( model )
        return self

    def __sub__( self, model ):
        """
        Method for making compound models using - operator.

        >>> model1 = model2 - model3

        Parameters
        ----------
        model : Model
            a copy of model to subtract from a copy of self (the existing chain)

        """
        return self.copy().__isub__( model.copy() )

    def __imul__( self, model ):
        """
        Method for making compound models using *= operator.

        >>> model1 *= model2

        Parameters
        ----------
        model : Model
            a model to multiply with self (the existing chain)

        """
        self.multiplyModel( model )
        return self

    def __mul__( self, model ):
        """
        Method for making compound models using * operator.

        >>> model1 = model2 * model3

        Parameters
        ----------
        model : Model
            a copy of model to multiply with a copy of self (the existing chain)

        """
        return self.copy().__imul__( model.copy() )

    def __itruediv__( self, model ):
        """
        Method for making compound models using /= operator.

        >>> model1 /= model2

        Parameters
        ----------
        model : Model
            a model to divide self with (the existing chain)

        """
        self.divideModel( model )
        return self

    def __truediv__( self, model ):
        """
        Method for making compound models using / operator.

        >>> model1 = model2 / model3

        Parameters
        ----------
        model : Model
            a copy of model to divide a copy of self with (the existing chain)

        """
        return self.copy().__itruediv__( model.copy() )

    def __ior__( self, model ):
        """
        Method for making compound models using |= operator.

        >>> model1 |= model2

        Use the results of model1 as input for model2.

        Parameters
        ----------
        model : Model
            a model to pipe the previous results through

        """
        self.pipeModel( model )
        return self

    def __or__( self, model ):
        """
        Method for making compound models using | (pipe) operator.

        >>> model1 = model2 | model3

        Parameters
        ----------
        model : Model
            a copy of model to pipe the results of a copy of self (the existing chain)

        """
        return self.copy().__ior__( model.copy() )

    #  *************************************************************************
    def testPartial( self, xdata, params, silent=True ):
        """
        A test routine to check the calculation of the partial derivatives.

        It is compared to a numerical calculation.

        Parameters
        ----------
        xdata : (list of) float
            values of the independent variable
        params : list of floats
            parameters for the model
        silent : bool
            if false print outputs

        Return
        ------
        The number of large deviations.

        """
        xdata  = Tools.toArray( xdata, ndim=self.ndim )
        params = Tools.toArray( params )
        sz = xdata.shape
        res = self.result( xdata, params )

        random.seed( 13010804 )

        try :
            snum = self.strictNumericDerivative( xdata, params )
        except Exception :
            snum = 0

        try :
            df = self.derivative( xdata, params )
            if df is None :
                raise ValueError
        except Exception :
            df = snum
            if not silent :
                print( "The model has no derivatives df/dx" )

#        print( df )
#        print( snum )


        snmp = self.strictNumericPartial( xdata, params )
        try :
            partial = self.partial( xdata, params )
        except Exception :
            partial = snmp
            if not silent :
                print( "The model has no partials df/dp" )


        ndout = self.lastndout

        kerr = 0
        lrang = range( sz[0] )
        if sz[0] > 10 :
            lrang = numpy.sort( random.sample( lrang, 10 ) )


        spaces = "          "
        for k in lrang :
            if not silent :
                print( "xdata[%2d]" % k, end='' )
                if self.ndim == 1 :
                    print( "   %8.3f"%(xdata[k]), end='' )
                else :
                    for i in range( sz[1] ) :
                        print( "   %8.3f"%(xdata[k,i]), end='' )

                print( "       result  ",  fmt( res[k] ) )
                print( "    par         value      partial      numeric" )

            if isinstance( df, list ) :
                df   = numpy.asarray( df )
                snum = numpy.asarray( snum )

            ms = numpy.maximum( numpy.abs( df + snum ), 1.0 )
            q = numpy.where( numpy.abs( df - snum ) > 0.001 * ms )
            lq = len( q[0] )
            kerr += lq

            if self.ndim == ndout == 1:
                if not silent :
                    print( "   dfdx               %12.5f %12.5f" % ( df[k], snum[k] ) )
            elif ( self.ndim > 1 ) and ( ndout > 1 ) : 
                for i in range( self.ndim ) :
                    ksi = 10 if i < 10 else 9
                    for j in range( ndout ) :
                        ks = ksi if j < 10 else ksi - 1
                        if not silent :
                            print( "  df%idx%i   %s %12.5f %12.5f" %
                                ( i, j, spaces[:ks], df[j,k,i], snum[j,k,i] ) )
            else :
                for i in range( max( self.ndim, ndout ) ) :
                    ks = 10 if i < 10 else 9
                    if not silent :
                        print( "  dfdx%i   %s  %12.5f %12.5f" %
                           ( i, spaces[:ks], df[k,i], snum[k,i] ) )


            if isinstance( partial, list ) :
                partial = numpy.asarray( partial )
                snmp    = numpy.asarray( snmp )

            ms = numpy.maximum( numpy.abs( partial + snmp ), 1.0 )
            q = numpy.where( numpy.abs( partial - snmp ) > 0.001 * ms )
            lq = len( q[0] )
            kerr += lq

            for i in range( self.npars ) :
                if ( lq >= 1 and i in q[-1] ) or random.random() < 5.0 / self.npars :
                    ks = 4 if i < 10 else 3 if i < 100 else 2
                        
                    if ndout == 1 : 
                        if not silent :
                            print( "  dfdp%d %s %8.3f %12.5f %12.5f"%
                            (i, spaces[:ks], params[i], partial[k,i], snmp[k,i]) )
                    else : 
                        for j in range( ndout ) :
                            if not silent :
                                print( " df%ddp%d %s %8.3f %12.5f %12.5f"%
                                (j, i, spaces[:ks], params[i], partial[j,k,i], snmp[j,k,i]) )
                    
        return kerr

    def strictNumericPartial( self, xdata, params, parlist=None ) :
        """
        Strictly numeric calculation of partials to params.

        For compound models it is different from numPartial and numDerivative.

        Parameters
        ----------
        xdata : float
            single xdata point (possibly multidimensional)
        params : array-like
            parameters
        kpar : None or int or list of int
            int  : return derivative to parameter kpar.
        """
        nxdata = Tools.length( xdata )
        if self.lastndout <= 1 :
            partial = numpy.zeros( ( nxdata, self.npars ), dtype=float  )
            assignPart = self.assignDF1
        else :
            partial = [ numpy.zeros( ( nxdata, self.npars ), dtype=float  ) 
                        for k in range( self.lastndout ) ]
            assignPart = self.assignDF2 

        dpg = Tools.makeNext( self.deltaP, 0 )
        
        par = params.copy()
        if parlist is None :
            parlist = numpy.arange( self.npars )
        
        for i, k in enumerate( parlist ) :
            dp = next( dpg )   
            par[k] += 0.5 * dp
            r1 = self.result( xdata, par )
            par[k] -= dp   
            r2 = self.result( xdata, par )

            assignPart( partial, i, ( r1 - r2 ) / dp )
            par[k] = params[k]
        try :
            dpg.close()
        except Exception :
            pass
        return partial

    def assignDF1( self, partial, i, dpi ) :
        partial[:,i] = dpi

    def assignDF2( self, partial, i, dpi ) :

#        print( "assignDF2  ", len( partial ), partial[0].shape, dpi.shape )
        for k in range( self.lastndout ) :
            partial[k][:,i] = dpi[:,k]


    def strictNumericDerivative( self, xdata, param ) :
        """
        Strictly numeric calculation of derivative.

        For compound models it is different from numPartial and numDerivative.

            ## More dimensions in x

        Parameters
        ----------
        xdata : float
            single xdata point (possibly multidimensional)
        param : array-like
            parameters
        """

        dx = self.deltaP[0]

        if self.ndim == 1:
            r1 = self.result( xdata+dx, param )
            r2 = self.result( xdata-dx, param )
            return ( r1 - r2 ) / ( 2 * dx )

        ## More dimensions in xdata
        if self.lastndout == 1 :
            df = numpy.zeros_like( xdata )
            assignDF = self.assignDF1
        else :
            df = [ numpy.zeros_like( xdata ) for k in range( self.lastndout ) ]
            assignDF = self.assignDF2

        for i in range( self.ndim ) :
            x = xdata.copy()
            
            x[:,i] += dx
            r1 = self.result( x, param )
            x[:,i] -= 2 * dx
            r2 = self.result( x, param )
            dpi = ( r1 - r2 ) / ( 2 * dx )
            assignDF( df, i, dpi )

        return df


##### End Model #########################################################


class Brackets( Model ):
    """
    Brackets is only for use in Model. Use BracketModel for independent uses.

    """

    #  *************************************************************************
    def __init__( self, model, copy=None, **kwargs ):

        super( Brackets, self ).__init__( model.npchain, ndim=model.ndim,
                                copy=copy, **kwargs )
        setatt( self, "model", model, type=Model )
        setatt( self, "parameters", model.parameters )

        next = model
        deep = 1
        while next is not None :
            if isinstance( next, Brackets ) :
                deep += 1
            next = next._next
        setatt( self, "deep", deep )
        setatt( self, "parNames", [] )

    def copy( self ):

        return Brackets( self.model.copy(), copy=self )


    #  *****Brackets RESULT**************************************************************
    def baseResult( self, xdata, param ):
        """
        Returns the result calculated at the xdatas.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        return self.model.result( xdata, param )

    #  *****Brackets PARTIAL*************************************************************
    def basePartial( self, xdata, param, parlist=None ):
        """
        Returns the partial derivatives calculated at the xdatas.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            values for the parameters.
        parlist : array_like
            Not in use

        """
        return self.model.partial( xdata, param )

    #  *****Brackets DERIVATIVE***********************************************************
    def baseDerivative( self, xdata, param ):
        """
        Returns the derivative (df/dx) calculated at the xdatas.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            values for the parameters.

        """
        return self.model.derivative( xdata, param )


    def _XXXsetLimits( self, lowLimits=None, highLimits=None ) :
        self.model.setLimits( lowLimits=lowLimits, highLimits=highLimits )

    def _XXXgetLimits( self ) :
        return self.model.getLimits()

    def setPrior( self, kpar, prior=None, **kwargs ):
        np = self.npbase
        if kpar < np :
            return self.model.setPrior( kpar, prior=prior, **kwargs )
        else :
            return super().setPrior( kpar, prior=prior, **kwargs )

    def getPrior( self, kpar ) :
        np = self.npbase
        if kpar < np :
            return self.model.getPrior( kpar )
        else :
            return super().getPrior( kpar )

    def nextPrior( self ) :
        yield self.model.nextPrior()

    def _toString( self, indent="", npars=0 ) :
        opname = [" null\n", " +\n", " -\n", " *\n", " /\n", " |\n" ]
        np = self.npbase
        indbrk = indent + "  " * self.deep

        brktstr = "{ " + self.model._toString( indent=indbrk, npars=npars ) + " }"
        if self._next is None :
            return brktstr

        return ( brktstr + opname[self._next._operation] +
                 indent + self._next._toString( indent=indent, npars=npars+np ) )

    #  ******Brackets BASENAME*******************************************************************
#    def baseName( self ):
#        """ Returns a string representation of the model.  """
#        indent = "  "
#        return "{ " + self.model._toString( indent * self.deep ) + " }"

    def basePrior( self, k ) :
        """
        Return the prior of the indicated parameter.

        Parameters
        ----------
        k : int
            parameter number.
        """
        return self.model.getPrior( k )

    def hasPriors( self, isBound=True ) :
        """
        Return True when the model has priors for all its parameters.

        Parameters
        ----------
        isBound : bool
            Also check if the prior is bound.
        """
        return self.model.hasPriors( isBound=isBound )


    #  ******Brackets Parameter NAME*******************************************************************

    def baseParameterName( self, k ):
        """
        Return the name of the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.

        """
        return self.model.getParameterName( k )

    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.

        """
        return self.model.getParameterUnit( k )


##### End Brackets #########################################################

