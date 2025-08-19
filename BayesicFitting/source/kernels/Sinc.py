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



class Sinc( Kernel ):
    """
    Sinc is an unbound Kernel function.

     K( x ) = sin( &pi; x ) / ( &pi; x )

    Sinc is not strictly positive.

    """
    def __init__( self ) :
        """
        Constructor.

         Using
         integral = 1.0
         fwhm = 2 * 1.8954942670 / &pi;
         range = inf
        """
        super( Sinc, self ).__init__( integral=1.0, fwhm=2 * 1.8954942670 / math.pi,
                                      range=math.inf )

    def result( self, x ):
        """
        Return the result for input values.

        Parameters
        ----------
        x : array-like
            input values
        """
        xp = x * math.pi
        return numpy.where( x == 0, 1.0, numpy.sin( xp ) / xp )

    def partial( self, x ):
        """
        Return the partial derivative wrt the input values.

        Parameters
        ----------
        x : array-like
            the input values
        """
        xp = x * math.pi
        return numpy.where( x == 0, 0.0,
                    math.pi * ( xp * numpy.cos( xp ) - numpy.sin( xp ) ) / ( xp * xp ) )

    def isBound( self ):
        """ Return False """
        return False

    def name( self ):
        """ Return the name of the kernel """
        return str( "Sinc: sin( pi * x ) / ( pi * x )" )


