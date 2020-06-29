import numpy as numpy
from astropy import units
import math
import re
from . import Tools
from .Tools import setAttribute as setatt

from .BracketModel import BracketModel
from .Formatter import formatter as fmt

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
__version__ = "2.5.3"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Perpetual Beta"

#  *
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
#  *    2011 - 2014 Do Kester, SRON (Java code)
#  *    2017 - 2020 Do Kester

class CombiModel( BracketModel ):
    """
    CombiModel combines a number of copies of the same model.

    Fixed relations can be set between similar parameters.
    The relations can be either multiplicative or additive.
    When these relations are set, they must be set for all models.

        f( x:p ) = &sum; g( x:p )

    where g( x:p ) is a model ( e.g. GaussModel )

    For consistency reasons it is not possible to change the attributes of a
    CombiModel. It is better to make a new one with the required settings.

    Attributes
    ----------
    nrepeat : int
        number of Models in this CombiModel
    nmp : int
        number of parameters in each Model
    expandpar : array of float
        expanded parameters. to be used in the repeated models
    npcmax : int
        number of parameters in expandpar (= nmp * nrepeat)
    expandindex : array of int
        converts parameter index into expandpar index
    addindex : array of int
        indices of additively connected parameters
    addvalue : array of float
        list of values to be added to the parameters in addindex
    mulindex : array of int
        indices of multiplicatively connected parameters
    mulvalue : array of float
        list of values to be multiplied to the parameters in mulindex
    select : array of int
        indices of expandpar to get parameters

    Attributes from BracketModel
    --------------------------
        model, deep

    Attributes from Model
    --------------------------
        npchain, parameters, stdevs, xUnit, yUnit

    Attributes from FixedModel
    --------------------------
        npmax, fixed, parlist, mlist

    Attributes from BaseModel
    --------------------------
        npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames


    Examples
    --------
    >>> gauss = GaussModel( )
    >>> combi = CombiModel( gauss, 3, addCombi={1:[0,0.1,0.3]}, mulCombi={2,[0]*3} )
    >>> print combi
    Combi of 3 times GaussModel
    >>> print( combi.npchain, combi.nrepeat, combi.nmp, combi.nexpand )
    5 3 3 9
    >>> print( combi.select )
    [0 1 2 3 6]
    >>> print( combi.expandindex )
    [0 1 2 3 1 2 4 1 2]
    >>> print( combi.modelindex )
    [0 0 0 1 2]
    >>> print( combi.addindex )
    [1 4 7]
    >>> print( combi.mulindex )
    [2 5 8]

    Category     mathematics/Fitting

    Notes
    -----
    1. When all parameters are left free, precise initial parameters are
    needed to converge to the global optimum.
    2. The model seems to be especially unstable when the basic models
    are overlapping. Fixing the widths relative to each other, helps.
    3. Using a PolynomialModel ( or similar ones ) as basic model, is not going
    to work.

    """
    def __init__( self, model, nrepeat=1, copy=None, oper='add',
                  addCombi=None, mulCombi=None, **kwargs ):
        """
        CombiModel combines several copies of the same model int one.

        Parameters
        ----------
        model : Model
            model to be repeated
        nrepeat : int
            number of repetitions
        oper : "add" or "mul"
            the repeated models are combined using this operation
        addCombi : None or dict
            make additive connections between parameters
            None : no additive connection
            dict : { int : array }
                key : int
                    index pointing to the key-th parameter in the model
                value : array of nrepeat floats
                    values added to each of the key-th parameters
        mulCombi : None or dict
            make multiplicative connections between parameters
            None : no multiplicative connection
            dict : { int : array }
                key : int
                    index pointing to the key-th parameter in the model
                value : array of nrepeat floats
                    values  multiplied to each of the key-th parameters

        """
        mdl = model.copy()
        for k in range( 1, nrepeat ) :
            if oper == 'add' :
                mdl.addModel( model.copy() )
            elif oper == 'mul' :
                mdl.multiplyModel( model.copy() )
            else :
                raise ValueError( "Unknown operation : " + oper )

        super( CombiModel, self ).__init__( mdl, **kwargs )

        setatt( self, "nmp", model.npchain )
        setatt( self, "nrepeat", nrepeat )
        setatt( self, "npcmax", model.npchain * nrepeat )

        self.combine( addCombi=addCombi, mulCombi=mulCombi )

        if copy is not None :
            setatt( self, "addindex", copy.addindex.copy() )
            setatt( self, "addvalue", copy.addvalue.copy() )
            setatt( self, "mulindex", copy.mulindex.copy() )
            setatt( self, "mulvalue", copy.mulvalue.copy() )
            setatt( self, "select", copy.select.copy() )
            setatt( self, "expandindex", copy.expandindex.copy() )

        setatt( self, "_npchain", len( self.select ) )
        setatt( self, "npbase", self._npchain )
        setatt( self, "npmax", self.npbase )
        setatt( self, "parameters", self.parameters[self.select] )

    def copy( self ):
        """ Copy method.  """
        oper = "add"
        if self.model._next and self.model._next._operation == 3 :
            oper = "mul"

        return CombiModel( self.model.isolateModel( 0 ), nrepeat=self.nrepeat,
                    oper=oper, copy=self )

    def combine( self, addCombi=None, mulCombi=None ) :
        """
        (re)sets the value of attributes "addindex", "addvalue", "mulindex", "mulvalue",
        "select" and "expandindex".

        Parameters
        ----------
        addCombi : None or dict
            make additive connections between parameters
            None : no additive connection
            dict : { int : array }
                key : int
                    index pointing to the key-th parameter in the model
                value : array of nrepeat floats
                    values added to each of the key-th parameters
        mulCombi : None or dict
            make multiplicative connections between parameters
            None : no multiplicative connection
            dict : { int : array }
                key : int
                    index pointing to the key-th parameter in the model
                value : array of nrepeat floats
                    values  multiplied to each of the key-th parameters

        """
#        print( addCombi, mulCombi )

        addindex, addvalue = self.setCombi( addCombi )
        setatt( self, "addindex", addindex )
        setatt( self, "addvalue", addvalue )
        mulindex, mulvalue = self.setCombi( mulCombi )
        setatt( self, "mulindex", mulindex )
        setatt( self, "mulvalue", mulvalue )

        expandindex = numpy.arange( self.npcmax, dtype=int )
        expandindex = self.makeExpandIndex( expandindex, self.addindex )
        expandindex = self.makeExpandIndex( expandindex, self.mulindex )

        setatt( self, "select", numpy.asarray( list( sorted( set( expandindex ) ) ) ) )

        i = 0
        for k in range( self.npcmax ) :
            if expandindex[k] >= i :
                expandindex[k] = i
                i += 1

        setatt( self, "expandindex", expandindex )


    def makeExpandIndex( self, expandindex, amindex ) :
        """
        Make an expanded index enumerating the parameters for the full model
        """

        for i,k in enumerate( amindex ) :
            if i % self.nrepeat == 0 :
                kk = amindex[i]
            else :
                expandindex[k] = kk
#            print( i, k, kk, amindex, expandindex )
        return expandindex


    def setCombi( self, combi ) :
        index = numpy.ndarray( 0, dtype=int )
        value = numpy.ndarray( 0, dtype=float )
        if combi is None :
            return (index,value)
        if not isinstance( combi, dict ) :
            raise ValueError( "The parameters addCombi, mulCombi need to be a dictionary" )

        for key in combi.keys() :
            if key >= self.nmp :
                raise ValueError( "The keys of a combi-dict need to be " +
                                    "< %d"%self.nmp )
            if len( combi[key] ) != self.nrepeat :
                raise ValueError( "The values of a combi-dict need to be " +
                                    "a list of length %d"%self.nrepeat )
            index = numpy.append( index, [k for k in range( key, self.npcmax, self.nmp )] )
            value = numpy.append( value, list( combi[key] ) )
        return ( index, value )

    def expandParameters( self, param ) :
        exppar = param[self.expandindex]
        exppar[self.addindex] += self.addvalue
        exppar[self.mulindex] *= self.mulvalue
        return exppar

    def baseResult( self, xdata, params ) :
        """
        Returns the result calculated at the xdatas.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        exppar = self.expandParameters( params )
        return super( CombiModel, self ).baseResult( xdata, exppar )

    def basePartial( self, xdata, params, parlist=None ) :
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
        exppar = self.expandParameters( params )
        fulldp = super( CombiModel, self ).basePartial( xdata, exppar )
        partial = fulldp[:,self.select]
        kk = 0
        for i,k in enumerate( self.addindex ) :
            if i % self.nrepeat == 0 :
                kk = k
            else :
                partial[:,kk] += fulldp[:,k]
        for i,k in enumerate( self.mulindex ) :
            if i % self.nrepeat == 0 :
                kk = k
                partial[:,kk] *= self.mulvalue[i]
            else :
                partial[:,kk] += fulldp[:,k] * self.mulvalue[i]
        return partial

    def baseDerivative( self, xdata, params ) :
        """
        Returns the derivative (df/dx) calculated at the xdatas.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            values for the parameters.

        """
        exppar = self.expandParameters( params )
        return super( CombiModel, self ).baseDerivative( xdata, exppar )

    def baseName( self ):
        """ Returns a string representation of the model.  """
        shortname = self.model.shortName( )
        m = re.match( "^[a-zA-Z_]*", shortname )
        return str( "Combi of %d times "%self.nrepeat + m.group(0) )

    def baseParameterName( self, k ):
        """
        Return the name of the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.

        """
        return ( self.model.getParameterName( self.expandindex[k] % self.nmp ) +
                "_%d" % ( self.expandindex[k] / self.nmp ) )

    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.

        """
        return self.model.getParameterUnit( self.expandindex[k] )



