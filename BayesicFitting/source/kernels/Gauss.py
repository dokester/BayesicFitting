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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2010 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2025 Do Kester

class Gauss( Kernel ):
    """
    Gauss is an unbound Kernel function:

     f( x ) = exp( -0.5 * x * x ).

    """
    def __init__( self ) :
        """
        Constructor.

         Using
         integral = sqrt( 2 &pi; )
         fwhm = sqrt( 2 log( 2 ) )
         range = inf
        """
        integral = numpy.sqrt( 2 * math.pi )
        fwhm = 2 * math.sqrt( 2 * math.log( 2 ) )
        super( Gauss, self ).__init__( integral=integral, fwhm=fwhm, range=math.inf )

    def result( self, x ):
        """
        Return the result for input values.

        Parameters
        ----------
        x : array-like
            input values
        """
        return self.resultsq( x * x )

    def resultsq( self, xsq ):
        """
        Return the result for squared input values.   

        Parameters
        ----------
        x : array-like
            the squares of the input values                                     
        """
        return numpy.exp( -0.5 * xsq )

    def partial( self, x ):
        """
        Return the partial derivative wrt the input values.

        Parameters
        ----------
        x : array-like
            the input values
        """
        return -x * self.result( x )

    def isBound( self ):
        """ Return False """
        return False

    def name( self ):
        """ Return the name of the kernel """
        return str( "Gauss: exp( -0.5 * x^2 )" )


