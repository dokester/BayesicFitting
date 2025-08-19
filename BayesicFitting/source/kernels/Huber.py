import numpy as numpy
import math

from .Kernel import Kernel

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

class Huber( Kernel ):
    """
    Huber is an improper Kernel function

     K( x ) = 1.0 if |x| < 1 else 1.0 / |x|

    It is improper because the integral equals +inf.

    It plays a role in robust fitting, see RobustShell, for medianizing the fit.

    """
    def __init__( self ) :
        """
        Constructor.

        Improper Kernel.

         Using
         integral = inf
         fwhm = 4
         range = inf
        """
        super( Huber, self ).__init__( integral=math.inf, fwhm=4.0, range=math.inf )

    def result( self, x ):
        """
        Return the result for input values.

        Parameters
        ----------
        x : array-like
            input values
        """
        ax = numpy.abs( x )
        return numpy.where( ax < 1, 1.0, 1.0 / ax )

    def partial( self, x ):
        """
        Return the partial derivative wrt the input values.

        Parameters
        ----------
        x : array-like
            the input values
        """
        ax = numpy.abs( x )
        return numpy.where( ax < 1, 0.0, -1.0 / ( x * ax ) )

    def isBound( self ):
        """ Return False """
        return False

    def name( self ):
        """ Return the name of the kernel """
        return str( "Huber: 1 if |x| < 1 else 1/|x|" )


