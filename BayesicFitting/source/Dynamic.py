import numpy as numpy
from . import Tools
from .Formatter import formatter as fmt

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

    """

    def getNumberOfComponents( self ):
        return self.npbase / self.deltaNpar


    def grow( self, pat=0 ):
        """
        Increase the degree by one upto maxDegree ( if present ).

        Parameters
        ----------
        pat : int
            location where the new params should be inserted

        Return
        ------
        bool :  succes

        """
        ncomp = self.getNumberOfComponents()
        if self.maxComp is not None and ncomp >= self.maxComp:
            return False

        self.alterParameterSize( self.deltaNpar, pat )

        self.changeNComp( 1 )

        return True

    def shrink( self, pat=0 ):
        """
        Decrease the degree by one downto minDegree ( default 1 ).

        Parameters
        ----------
        pat : int
            location where the new params should be inserted

        Return
        ------
        bool : succes

        """
        ncomp = self.getNumberOfComponents()
        if ncomp <= self.minComp :
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
        mdlpar = self.alterParameters( mdlpar, self.npbase, dnp, pat )

        self.npmax += dnp
        self.npbase += dnp
        self._head._npchain += dnp

        self._head.parameters = mdlpar

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

        if dnp < 0 :
            newpar[:kh] = param[:kh]
        else :
            newpar[:kb] = param[:kb]

        newpar[kh:] = param[kb:]

        return newpar

    def alterFitindex( self, findex, npbase, dnp, pat ) :

        newfi = numpy.zeros( len( findex ) + dnp, dtype=int )
        kh = pat + npbase + dnp
        kb = pat + npbase

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

        return newfi




