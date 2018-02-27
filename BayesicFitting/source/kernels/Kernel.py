
__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

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
#  * 2013 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2017 Do Kester


class Kernel( object ):
    """
    A kernel is a non-negative real-valued integrable function.

    It is satisfying the following two requirements:

    1. The integral over [-Inf,+Inf] exists ( < Inf ).
    2. It is an even function: K( x ) = K( -x ).

    A kernel is called bound when it is 0 everywhere except when |x| < 1.0.

    Several kernel functions, K( x ) are defined in this package:

    Name        Definition          Integral    FWHM    bound   alias
    Biweight    ( 1-x^2 )^2            16/15    1.08     True   Tukey
    CosSquare   cos^2( 0.5*PI*x )        1.0    1.00     True
    Cosine      cos( 0.5*PI*x )         4/PI    1.33     True
    Gauss       exp( -0.5*x*x )   sqrt(2*PI)    1.22    False
    Huber       min( 1, 1/|x| )          inf    4.00    False   Median
    Lorentz     1 / ( 1 * x*x )           PI    2.00    False
    Parabola    1 - x*x                  4/3    1.41     True
    Sinc        sin(x) / x               1.0    1.21    False
    Triangle    1 - |x|                  1.0    1.00     True
    Tricube     ( 1 - |x|^3 )^3        81/70    1.18     True
    Triweight   ( 1 - x^2 )^3          32/35    0.91     True
    Uniform     1.0                      2.0    1.00     True   Clip

    For all bound Kernels the definition in the table is true for |x| < 1;
    elsewhere it is 0.

    Huber is not a proper Kernel as the integral is inf. However it is important
    in robust fitting (RobustShell) to get a madian-like solution for the outliers.

    Author:      Do Kester

    Category:    mathematics/Fitting

    """
    def __init__( self, numpar=3, integral=1.0, fwhm=1.0  ) :
        self.numpar = numpar
        self.integral = integral
        self.fwhm = fwhm

    def result( self, x ):
        """
        Return the result for one input value.

        Parameters
        ----------
        x : array-like
            the input value

        """
        pass

    def resultsq( self, xsq ):
        """
        Return the result for one input value.

        Parameters
        ----------
        x : array-like
            the input value
        Parameters: x the square of the input value

        """
        pass

    def partial( self, x ):
        """
        Return the partial derivative wrt input value.

        Parameters
        ----------
        x : array-like
            the input value

        """
        pass

    def isBound( self ):
        """
        Return true when the kernel is bound.
        All non-zero values are between -1 and +1

        """
        pass

    def __str__( self ):
        """ Return a name.  """
        return self.name()



