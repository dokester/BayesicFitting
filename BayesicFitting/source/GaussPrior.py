import math
from scipy import special
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
#  *    2017        Do Kester


class GaussPrior( Prior ):
    """
    Gauss prior distribution.
    .. math::
        Pr( x ) = exp( - ( x / scale )^2 )

    By default: scale = 1.
    It can also have a limited domain. By default the domain is [-Inf,+Inf].
    In computational practice the domain is limited to about [-6, 6] scale units.

    Equivalent to a double-sided exponential prior

    domain2unit: u = 0.5 * ( erf( d / scale ) + 1 )
    unit2domain: d = erfinv( 2 * u - 1 ) * scale

    Attributes
    ----------
    scale : float
        scale of the Gaussian distribution
    lowLimit : float
        low limit (inactive for now)
    highLimit : float
        high limit ( inactive for now)

    """

    SPI = 1.0 / math.sqrt( math.pi )
    LSPI = math.log( SPI )

    #  *********CONSTRUCTOR***************************************************
    def __init__( self, scale=1.0, prior=None ):
        """
        Constructor.

        Parameters
        ----------
        scale : float
            of the exponential
        prior : GaussPrior
            prior to copy (with new scale if applicable)

        """
        super( GaussPrior, self ).__init__( prior=prior )
        self.scale = scale

    def copy( self ):
        return GaussPrior( prior=self, scale=self.scale )

    def domain2Unit( self, dval ):
        """
        Return a value in [0,1] given a value within the valid domain of
        a parameter for a Gauss distribution.

        domain2unit: u = 0.5 * ( erf( d / scale ) + 1 )

        Parameters
        ----------
        dval : float
            value within the domain of a parameter

        """
        return 0.5 * ( special.erf(  dval / self.scale ) + 1 )

    def unit2Domain( self, uval ):
        """
        Return a value within the valid domain of the parameter given a value
        between [0,1] for a Gauss distribution.

        unit2domain: d = erfinv( 2 * u - 1 ) * scale

        Parameters
        ----------
        uval : float
            value within [0,1]

        """
        return special.erfinv( 2 * uval - 1 ) * self.scale

#    def partialDomain2Unit( self, dval ):
    def result( self, x ):
        """
        Return a the result of the distribution function at x.

        Parameters
        ----------
        x : float
            value within the domain of a parameter

        """
        xs = x / self.scale
        return self.SPI * math.exp( - xs * xs )

    def logResult( self, x ):
        """
        Return a the log of the result of the distribution function to p.

        Parameters
        ----------
        x : float
            value within the domain of a parameter

        """
        xs = x / self.scale
        return self.LSPI - ( xs * xs )

    def partialLog( self, x ):
        """
        Return partial derivative of log( Prior ) wrt x.

        Parameters
        ----------
        x : float
            the value

        """
        return -2 * x / ( self.scale * self.scale )

    def isBound( self ):
        """ Return true if the integral over the prior is bound.  """
        return True

    def __str__( self ):
        """ Return a string representation of the prior.  """
        return str( "Gauss prior with scale = %.2f"%( self.scale ) )



