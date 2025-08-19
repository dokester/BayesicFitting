import numpy as numpy

from .Kernel import Kernel
from .Cosine import Cosine

__author__ = "Do Kester"
__year__ = 2025
__license__ = "GPL3"
__version__ = "3.2.4"
__url__ = "https://dokester.github.io/BayesicFitting/"
__status__ = "Perpetual Beta"

#  *
#  *    This file is part of the BayesicFitting package.
#  *
#  *    BayesicFitting is free software: you can redistribute it and/or modify
#  *    it under the terms of the GNU Lesser General Public License as
#  *    published by the Free Software Foundation, either version 3 of
#  *    the License, or ( at your option ) any later version.
#  *
#  *    BayesicFitting is distributed in the hope that it will be useful,
#  *    but WITHOUT ANY WARRANTY; without even the implied warranty of
#  *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  *    GNU Lesser General Public License for more details.
#  *
#  *    The GPL3 license can be found at <http://www.gnu.org/licenses/>.
#  *
#  *    2016 - 2025 Do Kester

class CosSquare( Kernel ):
    """
    CosSquare (Cosine Squared) is a Kernel function between [-1,1]; it is 0 elsewhere.

        K( x ) = cos^2( 0.5 &pi; x )  if |x| < 1 else 0


    """
    def __init__( self ) :
        """
        Constructor.

        Using
            integral = 1.0
            fwhm = 1.0

        """
        super( CosSquare, self ).__init__( integral=1.0, fwhm=1.0 )

    def result( self, x ):
        """
        Return the result for input values.

        Parameters
        ----------
        x : array-like
            input values
        """
        res = Cosine.result( Cosine, x )
        return res * res

    def partial( self, x ):
        """
        Return the partial derivative wrt the input values.

        Parameters
        ----------
        x : array-like
            the input values
        """
        return 2 * Cosine.result( Cosine, x ) * Cosine.partial( Cosine, x )

    def isBound( self ):
        """ Return True """
        return True

    def name( self ):
        """ Return the name of the kernel """
        return str( "CosSquare: cos^2( 0.5*PI*x ) if |x| < 1 else 0" )


