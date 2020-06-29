import numpy as numpy
from astropy import units
import math
from . import Tools
from .Tools import setAttribute as setatt
from .Formatter import formatter as fmt

from .Model import Model
from .Dynamic import Dynamic
from .ExponentialPrior import ExponentialPrior
from .UniformPrior import UniformPrior
from .Prior import Prior

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL"
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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2018 - 2020 Do Kester

class RepeatingModel( Model, Dynamic ):
    """
    RepeatingModel is a dynamic model, that calls the same model zero or more times,
    each time with the next set of parameters.

    RepeatingModel is a Dynamic model that grows and shrinks according to a growPrior.
    The growPrior defaults to ExponentialPrior, unless a maxComp (max nr of components)
    then it defaults to a UniformPrior with limits minComp .. maxComp.

    When isDynamic is set to False or minComp == maxComp, the RepeatingModel is a normal
    model with a static number of parameters/components.

    Priors and/or limits for the RepeatingModel are stored in the (encapsulated) model.

    It can be arranged that all similar parameters are the same, represented by the
    same parameters. Use keywords same=.

    Attributes
    ----------
    ncomp : int
        number of repetitions
    model : Model
        (encapsulated) model to be repeated
    same : None or int or list of int
        indices of parameters of model that get identical values
    index : list of int
        list of parameter indices not in same.
    isDyna : bool
        Whether this is a Dynamic Model.

    Attributes from Dynamic
    -----------------------
        ncomp, deltaNpar, minComp, maxComp, growPrior

    Attributes from Model
    ---------------------
        parameters, stdevs, npchain
        _next, _head, _operation
        xUnit, yUnit (relegated to model)

    Attributes from FixedModel
    --------------------------
        npmax, fixed, parlist, mlist

    Attributes from BaseModel
    --------------------------
        npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames

    Example
    -------
    >>> # Define a model containing between 1 and 6 VoigtModels, starting with 3
    >>> # and all with the same widths (for Gauss and Cauchy)
    >>> vgt = VoigtModel()
    >>> mdl = RepeatingModel( 3, vgt, minComp=1. maxComp=6, same=[2,3] )
    >>> print( mdl.npbase )             # 4 + 2 + 2
    >>> 8
    >>> # Define a static RepeatingModel of 5 GaussModels
    >>> gm = GaussModel()
    >>> mdl = RepeatingModel( 5, gm, isDynamic=False )
    >>> print( mdl.npbase )             # 5 * 3
    >>> 15
    >>> # Define a RepeatingModel with and exponential grow prior with scale 10
    >>> mdl = RepeatingModel( 1, gm, growPrior=ExponentialPrior( scale=10 ) )
    >>> print( mdl.npbase )             # 3
    >>> 3

    Author       Do Kester

    """
    #  *****CONSTRUCTOR*********************************************************
    def __init__( self, ncomp, model, minComp=0, maxComp=None, fixed=None,
                  same=None, growPrior=None, dynamic=True, copy=None, **kwargs ):
        """
        Repeating the same model several times.

        Parameters
        ----------
        ncomp : int
            number of repetitions
        model : Model
            model to be repeated
        minComp : int (0)
            minimum number of repetitions
        maxComp : None or int
            maximum number of repetitions
        same : None or int or list of int
            indices of parameters of model that get identical values

        growPrior : None or Prior
            governing the birth and death.
            ExponentialPrior (scale=2) if  maxOrder is None else UniformPrior
        dynamic : bool (True)
            Whether this is a Dynamic Model.
        copy : RepeatingModel
            model to copy

        Raises
        ------
        AttributeError when fixed parameters are requested
        ValueError when order is outside [min..max] range

        """
        if fixed is not None :
            raise AttributeError( "DynamicModel cannot have fixed parameters; " +
                                  " put fixed parameter(s0 in model." )
        if ncomp < minComp or ( maxComp is not None and ncomp > maxComp ) :
            raise ValueError( "ncomp outside range of [min..max] range" )

        np = ncomp * model.npchain - ( ncomp - 1 ) * Tools.length( same )
        self.isDyna = dynamic and ( maxComp is None or minComp < maxComp )

        super( RepeatingModel, self ).__init__( np, copy=copy, **kwargs )

        self.ncomp = ncomp
        self.model = model

        if copy is None :
            self.minComp = minComp
            self.maxComp = maxComp
            self.priors = model.priors          ## point to the same
        else :
            self.minComp = copy.minComp
            self.maxComp = copy.maxComp
            growPrior = copy.growPrior.copy()
            same = copy.same

        self.setSame( same )
        self.deltaNpar = len( self.index )

        if self.isDynamic() :
            if growPrior is None :
                if maxComp is None :
                    self.growPrior = ExponentialPrior( scale=2 )
                else :
                    lim = [minComp, maxComp+1]        # limits on components
                    self.growPrior = UniformPrior( limits=lim )
            else :
                self.growPrior = growPrior

    def copy( self ):
        """ Copy method.  """
        return RepeatingModel( self.ncomp, self.model, isDynamic=self.isDyna, copy=self )

    def changeNComp( self, dn ) :
        setatt( self, "ncomp", self.ncomp + dn )

    def setSame( self, same ) :
        """
        Assign similar parameters the same value.

        Parameters
        ----------
        same : None or int or [int]
            similar parameters indicated as an index in encapsulated model.
        """
        self.same = same
        if same is None :
            self.index = numpy.arange( self.model.npbase, dtype=int )
            return

        index = []
        for k in range( self.model.npbase ) :
            if not k in self.same :
                index += [k]
        self.index = numpy.array( index, dtype=int )

    def grow( self, offset=0, rng=None, **kwargs ):
        """
        Increase the the number of components by 1 (if allowed by maxComp)

        Parameters
        ----------
        offset : int
            index where the dynamic model starts
        rng : RandomState
            random numbr generator

        Return
        ------
        bool :  succes

        """
        if not self.isDynamic() :
            return False

        if self.maxComp is not None and self.ncomp >= self.maxComp:
            return False

        location = self.npbase

        dnp = self.deltaNpar if self.ncomp > 0 else self.model.npbase
        self.alterParameterSize( dnp, offset, location=location )

        head = self._head
        mdlpar = head.parameters
        k1 = location + offset
        value = numpy.zeros( dnp, dtype=float )
        if rng is not None :
            for k in range( dnp ) :
                value[k] = head.unit2Domain( rng.rand(), k + k1 )

        mdlpar = self.alterParameters( mdlpar, location, dnp, offset, value=value )

        setatt( self._head, "parameters", mdlpar )

        self.alterParameterNames( dnp )

        self.ncomp += 1

        return True

    def shrink( self, offset=0, **kwargs ):
        """
        Decrease the the number of componenets by 1 (if allowed by minComp)
        Remove an arbitrary item.

        Parameters
        ----------
        offset : int
            index where the dynamic model starts

        Return
        ------
        bool : succes

        """
        if ( not self.isDynamic() ) or self.ncomp <= self.minComp :
            return False

        location = self.npbase
        dnp = -( self.deltaNpar if self.ncomp > 1 else self.model.npbase )
        self.alterParameterSize( dnp, offset, location=location )

        head = self._head
        mdlpar = head.parameters
        mdlpar = self.alterParameters( mdlpar, location, dnp, offset )
        setatt( self._head, "parameters", mdlpar )

        self.alterParameterNames( dnp )

        self.ncomp -= 1

        return True

    def shuffle( self, param, offset, np, rng ) :
        """
        Shuffle the parameters of the components (if they are equivalent)

        Parameters
        ----------
        param : array-like
            list of all parameters
        offset : int
            index where the dynamic model starts
        np : int
            length of the parameters of the dynamic model
        rng : RNG
            random number generator
        """
        if self.ncomp <= 1 :
            return param

        off = self.model.npbase + offset
        src = numpy.arange( self.ncomp ) * self.deltaNpar + off
        per = rng.permutation( self.ncomp )
        for i in self.index :
            src[-1] = offset + i             # replace last src by index
            param[src[per]] = param[src]
            src += 1

        return param


    #  *************************************************************************
    def __setattr__( self, name, value ) :

        if self.setDynamicAttribute( name, value ) :
            return

        if name == "isDyna" :
            setatt( self, name, value, type=bool )
        elif name == "model" :
            setatt( self, name, value, type=Model )
        elif name == "same" :
            setatt( self, name, value, type=int, islist=True, isnone=True )
        elif name == "index" :
            setatt( self, name, value, type=int, islist=True, isnone=True )
        else :
            super( RepeatingModel, self ).__setattr__( name, value )

    def isDynamic( self ) :
        return self.isDyna

    #  *************************************************************************
    def baseResult( self, xdata, params ):
        """
        Returns the result of the model function.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result
        params : array_like
             values for the parameters

        """
        result = numpy.zeros( Tools.length( xdata ), dtype=float )
        if self.ncomp == 0 :
            return result

        ke = self.model.npbase
        pars = params[:ke].copy()
        k = 1

#        print( "RM   ", self.ncomp, fmt( params, max=None ) )
        while True :
            result += self.model.result( xdata, pars )
            if k == self.ncomp :
                return result
            k += 1
            ks = ke
            ke += self.deltaNpar
#            print( "RM1  ", k, ks, ke, self.index )
            pars[self.index] = params[ks:ke]

        return result

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result
        params : array_like
            values for the parameters
        parlist : array_like
            list of indices of active parameter

        """
        nxdata = Tools.length( xdata )
        partial = numpy.zeros( ( nxdata, self.npbase ), dtype=float )
        if self.ncomp == 0 :
            return partial

        ke = self.model.npbase
        pars = params[:ke].copy()
        full = numpy.arange( self.model.npbase, dtype=int )
        k = 1
        while True :
            partial[:,full] += self.model.partial( xdata, pars )
            if k == self.ncomp :
                break
            k += 1
            ks = ke
            ke += self.deltaNpar

            full[self.index] = [k for k in range( ks, ke )]
            pars[self.index] = params[ks:ke]

        if parlist is None :
            return partial

        return partial[:,parlist]

    def baseDerivative( self, xdata, params ):
        """
        Returns the derivative df/dx at the input value.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result
        params : array_like
             values for the parameters

        """
        dfdx = numpy.zeros( Tools.length( xdata ), dtype=float )
        if self.ncomp == 0 :
            return dfdx

        ke = self.model.npbase
        pars = params[:ke].copy()
        k = 1
        while True :
            dfdx += self.model.derivative( xdata, pars )
            if k == self.ncomp :
                return dfdx
            k += 1
            ks = ke
            ke += self.deltaNpar
            pars[self.index] = params[ks:ke]

        return dfdx

    def setLimits( self, lowLimits=None, highLimits=None ) :
        self.model.setLimits( lowLimits=lowLimits, highLimits=highLimits )

    def hasPriors( self ) :
        return self.model.hasPriors()

    def basePrior( self, k ):
        """
        Return the prior for parameter k.

        Parameters
        ----------
        k : int
            the parameter to be selected.
        """
        i,k = self.par2model( k )
        return self.model.getPrior( i )

    def baseName( self ):
        """ Return a string representation of the model.  """
        return ( "Repeat %d times:\n  " % self.ncomp + self.model.baseName( ) )

    def baseParameterName( self, k ):
        """
        Return the name of the indicated parameter.

        Parameters
        ----------
        k : int
            parameter number.

        """
        i,k = self.par2model( k )
        return self.model.getParameterName( i ) + "_%d" % k

    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.

        Parameters
        ----------
        k : int
            parameter number.

        """
        self.model.xUnit = self.xUnit
        self.model.yUnit = self.yUnit

        i,k = self.par2model( k )
        return self.model.getParameterUnit( i )

    def par2model( self, k ) :
        """
        Return index in model and repetition nr for param k
        """
        if k >= self.model.npchain :
            k -= self.model.npchain
            i = self.index[ k % self.deltaNpar ]
            k = 1 + k // self.deltaNpar
        else :
            i = k
            k = 0
        return i, k
