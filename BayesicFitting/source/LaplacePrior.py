import math

from .Prior import Prior

__author__ = "Do Kester"
__year__ = 2017
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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2010 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2017 Do Kester


class LaplacePrior( Prior ):
    """
    Laplace prior distribution.
    .. math::
        Pr( x ) = exp( - |x| / scale )

    By default: scale = 1.
    It can also have a limited domain. By default the domain is [-Inf,+Inf].
    In computational practice the domain is limited to about [-36,36] scale units

    Equivalent to a double-sided exponential prior

    domain2unit: u = 0.5 * exp( d / scale )             if d < 0
                     1.0 - 0.5 * exp( -d / scale )      otherwise
    unit2domain: d = log( 2 * u ) * scale               if u < 0.5
                    -log( 2 * ( 1 - u ) ) * scale       otherwise

    Attributes
    ----------
    scale : float
        scale of the exponential
    lowLimit : float
        low limit (inactive for now)
    highLimit : float
        high limit ( inactive for now)

    """

    #  *********CONSTRUCTOR***************************************************
    def __init__( self, scale=1.0, prior=None ):
        """
        Constructor.

        Parameters
        ----------
        scale : float
            of the exponential
        prior : LaplacePrior
            prior to copy (with new scale if applicable)

        """
        super( LaplacePrior, self ).__init__( prior=prior )
        self.scale = scale

    def copy( self ):
        return LaplacePrior( prior=self, scale=self.scale )

    def domain2Unit( self, dval ):
        """
        Return a value in [0,1] given a value within the valid domain of
        a parameter for a Laplace distribution.

        domain2unit: u = 0.5 * exp( d / scale ) if d < 0 else
                         1.0 - 0.5 * exp( -d / scale )

        Parameters
        ----------
        dval : float
            value within the domain of a parameter

        """
        return ( 0.5 * math.exp(  dval / self.scale ) if ( dval < 0 ) else
           1.0 - 0.5 * math.exp( -dval / self.scale ) )

    def unit2Domain( self, uval ):
        """
        Return a value within the valid domain of the parameter given a value
        between [0,1] for a Laplace distribution.

        unit2domain: d = log( 2 * u ) * scale if u < 0.5 else
                        -log( 2 * ( 1 - u ) ) * scale;

        Parameters
        ----------
        uval : float
            value within [0,1]

        """
        if uval == 0 : return -math.inf
        elif uval == 1 : return math.inf
        scl = self.scale
        if uval > 0.5:
            uval = 1 - uval
            scl *= -1
        return math.log( 2 * uval ) * scl

    def result( self, x ):
        """
        Return a the result of the distribution function at x.

        Parameters
        ----------
        x : float
            value within the domain of a parameter

        """
        return 0.5 * math.exp( -abs( x ) / self.scale ) / self.scale

    def logResult( self, x ):
        """
        Return a the log of the result of the distribution function to p.

        Parameters
        ----------
        x : float
            value within the domain of a parameter

        """
        if self.isOutOfLimits( x ) : return -math.inf

        return math.log( 0.5 / self.scale ) - abs( x ) / self.scale

    def partialLog( self, p ):
        """
        Return partial derivative of log( Prior ) wrt parameter.

        Parameters
        ----------
        p : float
            the value

        """
        if p == 0 : return 0
        return -1 / self.scale if p > 0 else 1 / self.scale

    def isBound( self ):
        """ Return true if the integral over the prior is bound.  """
        return True

    def __str__( self ):
        """ Return a string representation of the prior.  """
        return str( "Laplace prior with scale = %.2f"%( self.scale ) )



