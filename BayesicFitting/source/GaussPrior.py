import math
from scipy import special
from .Prior import Prior

__author__ = "Do Kester"
__year__ = 2021
__license__ = "GPL3"
__version__ = "2.7.0"
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
#  *    2017 - 2021 Do Kester


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

    Examples
    --------
    >>> pr = GaussPrior()                         # center=0, scale=1
    >>> pr = GaussPrior( center=1.0, scale=0.5 )
    >>> pr = GaussPrior( limits=[0,None] )        # limited to values >= 0
    >>> pr = GaussPrior( center=1, circular=3 )   # circular between 0.5 and 2.5

    Attributes
    ----------
    center : float
        center of the Gaussian prior
    scale : float
        scale of the Gaussian prior

    Attributes from Prior
    --------------------=
    lowLimit, highLimit, circular, deltaP, _lowDomain, _highDomain


    """

    SPI = 1.0 / math.sqrt( math.pi )
    LSPI = math.log( SPI )

    MAXVAL = 6

    #  *********CONSTRUCTOR***************************************************
    def __init__( self, center=0.0, scale=1.0, limits=None, circular=False, prior=None ):
        """
        Constructor.

        Parameters
        ----------
        center : float
            of the location of the prior
        scale : float
            of the exponential
        limits : None or [float,float]
            None    no limits are set
            2 floats    lowlimit and highlimit
        circular : bool or float
            bool : y|n circular with period from limits[0] to limits[1]
            float : period of circularity
        prior : GaussPrior
            prior to copy (with new scale if applicable)

        """
        self.center = center
        self.scale = scale

        super( ).__init__( limits=limits, circular=circular, prior=prior )

    def copy( self ):
        """ Copy the prior """
        return GaussPrior( prior=self, center=self.center, scale=self.scale,
                           limits=self.limits, circular=self.circular )

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
        dom = special.erfinv( 2 * uval - 1 )
        if math.isfinite( dom ) :
            return dom * self.scale + self.center
        else :
            fs = - self.MAXVAL if uval < 0.5 else self.MAXVAL
            return self.center + fs * self.scale

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

    def shortName( self ):
        """ Return a string representation of the prior.  """
        return str( "GaussPrior" )



