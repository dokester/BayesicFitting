import numpy as numpy
from . import Tools
from .Formatter import formatter as fmt
from .Tools import setAttribute as setatt
from .Prior import Prior
from .ExponentialPrior import ExponentialPrior
from .UniformPrior import UniformPrior

__author__ = "Do Kester"
__year__ = 2021
__license__ = "GPL3"
__version__ = "2.7.0"
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
#  *    2016 - 2021 Do Kester


class Dynamic( object ):
    """
    Class adjoint to Model which implements some dynamic behaviour.


    Attributes
    ----------
    ncomp : int
        the number of components in the dynamic model
    deltaNpar : int
        the number of parameters in each component
    minComp : int
        minimum number of repetitions
    maxComp : None or int
        maximum number of repetitions
    growPrior : None or Prior
        governing the birth and death.
        ExponentialPrior (scale=2) if  maxOrder is None else UniformPrior

    """
    def __init__( self, dynamic=True ) :
        """
        Constructor for Dynamic

        Parameters
        ----------
        dynamic: bool
            True if the Model is to be considered dynamic.
        """

        setatt( self, "dynamic", dynamic )


    def isDynamic( self ) :
        return self.dynamic

    def setGrowPrior( self, growPrior=None, min=1, max=None, name="Comp" ) :
        """
        Set the growth prior.

        Parameters
        ----------
        growPrior : None or Prior
            governing the birth and death.
            ExponentialPrior (scale=2) if  maxOrder is None else UniformPrior
        min : int
            lower limit on growthprior
        max : None or int
            upper limit on growthprior
        name : str
            name of the component
        """
        setatt( self, "min%s"%name, min, type=int )
        setatt( self, "max%s"%name, max, type=int, isnone=True )
        if growPrior is None :
            if max is None :
                setatt( self, "growPrior", ExponentialPrior( scale=2 ) )
            else :
                lim = [min, max+1]              # limits on components
                setatt( self, "growPrior", UniformPrior( limits=lim ) )
        else :
            setatt( self, "growPrior", growPrior, type=Prior )


    def setDynamicAttribute( self, name, value ) :
        """
        Set attribute, if it belongs to a Dynamic Models.

        Parameters
        ----------
        name : str
            name of the attribute
        value : anything
            value of the attribute

        Return
        ------
        bool : True if name was a Dynamic name
               False if not

        """
        if name == "ncomp" :
            setatt( self, name, value, type=int )
            return True
        if name == "deltaNpar" :
            setatt( self, name, value, type=int )
            return True
        if name == "maxComp" :
            setatt( self, name, value, type=int, isnone=True )
            return True
        if name == "minComp" :
            setatt( self, name, value, type=int )
            return True
        if name == "growPrior" :
            setatt( self, name, value, type=Prior )
            return True

        return False


    def grow( self, offset=0, rng=None, **kwargs ):
        """
        Increase the degree by one upto maxComp ( if present ).

        Parameters
        ----------
        offset : int
            index where the params of the Dynamic model start
        rng : random number generator
            to generate a new parameter.

        Return
        ------
        bool :  succes

        """
        if self.maxComp is not None and self.ncomp >= self.maxComp:
            return False

        location = self.npbase

        dnp = self.deltaNpar
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

        self.changeNComp( 1 )

        return True

    def shrink( self, offset=0, rng=None, **kwargs ):
        """
        Decrease the degree by one downto minComp ( default 1 ).

        Parameters
        ----------
        offset : int
            index where the params of the Dynamic model start
        rng : random number generator
            Not used in this implementation

        Return
        ------
        bool : succes

        """
        if self.ncomp <= self.minComp :
            return False

        location = self.npbase
        dnp = - self.deltaNpar
        self.alterParameterSize( dnp, offset, location=location )

        head = self._head
        mdlpar = head.parameters
        mdlpar = self.alterParameters( mdlpar, location, dnp, offset )
        setatt( self._head, "parameters", mdlpar )

        self.alterParameterNames( dnp )

        self.changeNComp( -1 )

        return True

    def alterParameterNames( self, dnp ) :
        """
        Renumber the parameter names.

        Parameters
        ----------
        dnp : int
            change in the number of parameters
        """
        if dnp > 0 :
            parNames = ["parameter_%d"%k for k in range( self.npbase )]
        else :
            parNames = self.parNames[:self.npbase]

        setatt( self, "parNames", parNames )


    def alterParameterSize( self, dnp, offset, location=None, value=0 ) :
        """
        Change the number of parameters and self.parameters.

        Parameters
        ----------
        dnp : int
            change in the number of parameters in the DynamicModel
        offset : int
            starting index of the DynamicModel
        location : int
            index in param[offset:] at which to insert/delete the new parameters
        """
        if dnp == 0 :
            return

        if location is None :
            location = self.npbase

#        print( "DYN1  ", dnp, offset, self.npmax, self.npbase, self.npchain, mdlpar )

        setatt( self, "location", location )
        setatt( self, "npmax", self.npmax + dnp )
        setatt( self, "npbase", self.npbase + dnp )
        setatt( self._head, "_npchain", self._head._npchain + dnp )

#        print( "DYN2  ", dnp, offset, self.npmax, self.npbase, self.npchain, mdlpar )


    def alterParameters( self, param, location, dnp, offset, value=None ) :
        """
        change the parameters to comply with the changed model.

        param:      [p0 p1 p2 p3 p4 p5 p6 p7 p8 p9]   # previous set
        offset:     2           # parameters of models in preceeding chain
        location:   1           # location where to add/delete parameter
        value:      [v0 ...]    # values to be given to added parameters

        dnp:        +1
        ==> newpar: [p0 p1 p2 v0 p3 p4 p5 p6 p7 p8 p9]

        dnp:        +2
        ==> newpar: [p0 p1 p2 v0 v1 p3 p4 p5 p6 p7 p8 p9]

        dnp:        -1
        ==> newpar: [p0 p1 p3 p4 p5 p6 p7 p8 p9]

        dnp:        -2
        ==> ERROR: not enough space in param before location

        Parameters
        ----------
        param : array_like
            parameters of the parent model (chain)
        location : int
            index in param[offset:] at which to insert/delete the new parameters
        dnp : int
            number of parameters to insert (dnp>0) or delete (dnp<0)
        offset : int
            start index of the parameters of the dynamic model in param
        value : float or array_like
            to be given to the inserted parameters (only when dnp>0)

        """

#        print( "DY IN  ", fmt( param, max=None ), location, dnp, offset )

        np = len( param )
        newpar = numpy.zeros( np + dnp, dtype=float )

        if dnp > 0 :
            k1 = offset + location
            k2 = k1 + dnp
            newpar[:k1] = param[:k1]
            newpar[k1:k2] = value
            newpar[k2:] = param[k1:]
        else :
            if location + dnp < 0 :
                raise IndexError( "Cannot delete %d from parameters at %d"%(-dnp,location) )
            k2 = offset + location
            k1 = k2 + dnp
            newpar[:k1] = param[:k1]
            newpar[k1:] = param[k2:]

#        print( "DY OUT ", fmt( newpar, max=None ), k1, k2 )

        return newpar


    def alterFitindex( self, findex, location, dnp, offset ) :
        """
        change the fit index to comply with the changed model.

        Parameters
        ----------
        findex : array_like
            fit index of the parent model (chain)
        location : int
            index in param[offset:] at which to insert/delete the new parameters
        dnp : int
            number of parameters to insert (dnp>0) or delete (dnp<0)
        offset : int
            start index of the parameters of the dynamic model in param
        """
        lfin = len( findex )
        newfi = numpy.zeros( lfin + dnp, dtype=int )

        k = 0
        kol = offset + location

        kh = kol if dnp > 0 else kol + dnp
#        while findex[k] >=0 and findex[k] < kh :    ## copy first parts
        while k < lfin and findex[k] >=0 and findex[k] < kh :    ## copy first parts
            newfi[k] = findex[k]
            k += 1
        kl = k if dnp > 0 else k - dnp              ## where we are if findex

        for i in range( dnp ) :                     ## insert extra indices if dnp>0
            newfi[k] = kol + i
            k += 1

        for j in range( kl, lfin ) :                 ## copy the tail
            if findex[j] >= 0 :
                newfi[k] = findex[j] + dnp           ## in/de-crease indices
            else :
                newfi[k] = findex[j]                 ## negitive indices for hyperpars
            k += 1

        return newfi


    def shuffle( self, param, offset, np, rng ) :
        """
        Shuffle the parameters of the components (if they are equivalent)
        Default implementation: does nothing.

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
        return param




