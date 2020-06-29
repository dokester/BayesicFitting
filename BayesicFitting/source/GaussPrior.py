import math
from scipy import special
from .Prior import Prior

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
__version__ = "2.5.3"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Perpetual Beta"

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
#  *    2017 - 2020  Do Kester


class GaussPrior( Prior ):
    """
    Gauss prior distribution.

        Pr( x ) = exp( - ( ( x - c ) / scale )^2 )

    By default: center = 0 and scale = 1.

    It can also have a limited domain. (To be done)
    By default the domain is [-Inf,+Inf].
    In computational practice the domain is limited to about [-6, 6] scale units.

    domain2unit: u = 0.5 * ( erf( ( d - center ) / scale ) + 1 )
    unit2domain: d = erfinv( 2 * u - 1 ) * scale + center

    Attributes
    ----------
    center : float
        center of the Gaussian prior
    scale : float
        scale of the Gaussian prior

    Attributes from Prior
    --------------------=
    lowLimit, highLimit, deltaP, _lowDomain, _highDomain

    lowLimit and highLimit cannot be used in this implementation.

    """

    SPI = 1.0 / math.sqrt( math.pi )
    LSPI = math.log( SPI )

    #  *********CONSTRUCTOR***************************************************
    def __init__( self, center=0.0, scale=1.0, prior=None ):
        """
        Constructor.

        Parameters
        ----------
        center : float
            of the location of the prior
        scale : float
            of the exponential
        prior : GaussPrior
            prior to copy (with new scale if applicable)

        """
        super( GaussPrior, self ).__init__( prior=prior )
        self.center = center
        self.scale = scale

    def copy( self ):
        """ Copy the prior """
        return GaussPrior( prior=self, center=self.center, scale=self.scale )

    def domain2Unit( self, dval ):
        """
        Return a value in [0,1] given a value within the valid domain of
        a parameter for a Gauss distribution.

        domain2unit: u = 0.5 * ( erf( ( d - center ) / scale ) + 1 )

        Parameters
        ----------
        dval : float
            value within the domain of a parameter

        """
        return 0.5 * ( special.erf( ( dval - self.center ) / self.scale ) + 1 )

    def unit2Domain( self, uval ):
        """
        Return a value within the valid domain of the parameter given a value
        between [0,1] for a Gauss distribution.

        unit2domain: d = erfinv( 2 * u - 1 ) * scale + center

        Parameters
        ----------
        uval : float
            value within [0,1]

        """
        return special.erfinv( 2 * uval - 1 ) * self.scale + self.center

#    def partialDomain2Unit( self, dval ):
    def result( self, x ):
        """
        Return a the result of the distribution function at x.

        Parameters
        ----------
        x : float
            value within the domain of a parameter

        """
        xs = ( x - self.center ) / self.scale
        return self.SPI * math.exp( - xs * xs )

    def logResult( self, x ):
        """
        Return a the log of the result of the prior.

        Parameters
        ----------
        x : float
            value within the domain of a parameter

        """
        xs = ( x - self.center ) / self.scale
        return self.LSPI - ( xs * xs )

    def partialLog( self, x ):
        """
        Return partial derivative of log( Prior ) wrt x.

        Parameters
        ----------
        x : float
            the value

        """
        return -2 * ( x - self.center ) / ( self.scale * self.scale )

    def isBound( self ):
        """ Return true if the integral over the prior is bound.  """
        return True

    def __str__( self ):
        """ Return a string representation of the prior.  """
        return str( "Gauss prior with scale = %.2f"%( self.scale ) )



