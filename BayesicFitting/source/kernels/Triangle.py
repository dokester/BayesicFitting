import numpy as numpy

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

class Triangle( Kernel ):
    """
    Triangle is a Kernel function between [-1,1]; it is 0 elsewhere.

        K( x ) = ( 1 - |x| )        if |x| < 1
                 0                  elsewhere

    """
    def __init__( self ) :
        """
        Constructor.

        Using
            integral = 1.0
            fwhm = 1.0
        """
        super( Triangle, self ).__init__( integral=1.0, fwhm=1.0 )

    def result( self, x ):
        """
        Return the result for input values.

        Parameters
        ----------
        x : array-like
            input values
        """
        ax = numpy.abs( x )
        return numpy.where( ax <= 1, 1 - ax, 0.0 )

    def partial( self, x ):
        """
        Return the partial derivative wrt the input values.

        Parameters
        ----------
        x : array-like
            the input values
        """
        return numpy.where( numpy.abs( x ) <= 1, - numpy.sign( x ), 0.0 )

    def isBound( self ):
        """ Return True """
        return True

    def name( self ):
        """ Return the name of the kernel """
        return str( "Triangle: ( 1 - |x| ) if |x| < 1 else 0" )


