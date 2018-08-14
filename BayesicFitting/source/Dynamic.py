import numpy as numpy
from . import Tools
from .Formatter import formatter as fmt
from .Tools import setAttribute as setatt

from .Prior import Prior

__author__ = "Do Kester"
__year__ = 2018
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

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
#  *    2016 - 2018 Do Kester


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

#    def getNumberOfComponents( self ):
#        return self.npbase // self.deltaNpar


    def grow( self, pat=0 ):
        """
        Increase the degree by one upto maxComp ( if present ).

        Parameters
        ----------
        pat : int
            location where the new params should be inserted

        Return
        ------
        bool :  succes

        """
#        ncomp = self.getNumberOfComponents()
        if self.maxComp is not None and self.ncomp >= self.maxComp:
            return False

        self.alterParameterSize( self.deltaNpar, pat )

        self.changeNComp( 1 )

        return True

    def shrink( self, pat=0 ):
        """
        Decrease the degree by one downto minComp ( default 1 ).

        Parameters
        ----------
        pat : int
            location where the new params should be inserted

        Return
        ------
        bool : succes

        """
#        ncomp = self.getNumberOfComponents()
        if self.ncomp <= self.minComp :
            return False

        self.alterParameterSize( -self.deltaNpar, pat )

        self.changeNComp( -1 )

        return True

    def alterParameterSize( self, dnp, pat ) :
        """
        Change the number of parameters and self.parameters.

        Parameters
        ----------
        npnew : int
            number of parameters in the DynamicModel
        pat : int
            starting index of the DynamicModel
        """
        if dnp == 0 :
            return

        mdlpar = self._head.parameters

#        print( "DYN1  ", dnp, pat, self.npmax, self.npbase, self.npchain,
#            mdlpar )

        mdlpar = self.alterParameters( mdlpar, self.npbase, dnp, pat )

        setatt( self, "npmax", self.npmax + dnp )
        setatt( self, "npbase", self.npbase + dnp )
        setatt( self._head, "_npchain", self._head._npchain + dnp )

#        print( "DYN2  ", dnp, pat, self.npmax, self.npbase, self.npchain,
#            mdlpar )

        setatt( self._head, "parameters", mdlpar )

    def shuffle( self, param, pat, np, rng ) :
        """
        Shuffle the parameters of the components (if they are equivalent)
        Default implementation: does nothing.

        Parameters
        ----------
        param : array-like
            list of all parameters
        pat : int
            index where the dynamic model starts
        np : int
            length of the parameters of the dynamic model
        rng : RNG
            random number generator
        """
        return param

    def alterParameters( self, param, npbase, dnp, pat ) :

        newpar = numpy.zeros( len( param ) + dnp, dtype=float )
        kh = pat + npbase + dnp
        kb = pat + npbase

#        print( "DPA1  ", npbase, dnp, pat, kh, kb )
#        print( "DPA2  ", param )

        if dnp < 0 :
            newpar[:kh] = param[:kh]
        else :
            newpar[:kb] = param[:kb]

        newpar[kh:] = param[kb:]

#        print( "DPA3  ", newpar )

        return newpar

    def alterFitindex( self, findex, npbase, dnp, pat ) :

        newfi = numpy.zeros( len( findex ) + dnp, dtype=int )
        kh = pat + npbase + dnp
        kb = pat + npbase

#        print( "DFI1  ", npbase, dnp, pat, kh, kb )
#        print( "DFI2  ", findex )


        if dnp < 0 :
            newfi[:kh] = findex[:kh]
        else :
            newfi[:kb] = findex[:kb]
            fill = numpy.arange( dnp )
            if kb > 0 :
                fill += findex[kb-1] + 1
            newfi[kb:kh] = fill

        # the last part needs a shift of dnp, except when < 0
        newfi[kh:] = [fi if fi < 0 else fi + dnp for fi in findex[kb:]]

        if newfi[0] > 0 :
            print( npbase, dnp, pat )
            print( findex )
            print( newfi )
            raise AssertionError()

#        print( "DFI3  ", newfi )
        return newfi




