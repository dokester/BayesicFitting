import math
import numpy
from scipy import special

from .Formatter import formatter as fmt
from .Prior import Prior

__author__ = "Do Kester"
__year__ = 2024
__license__ = "GPL3"
__version__ = "3.2.1"
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
#  *    2017 - 2024 Do Kester


class GaussPrior( Prior ):
    """
    Gauss prior distribution. Use  normalized version:

        Pr( x ) = 1 / &sqrt;( 2 &pi; s^2 ) exp( - 0.5 * ( ( x - c ) / s )^2 )

    By default: c = center = 0 and s = scale = 1.

    It can also have a limited domain. (To be done)
    By default the domain is [-Inf,+Inf].
    In computational practice the domain is limited to about [-8.5, 8.5] scale units.

    According to integral-calculator.com we have:

    domain2unit: u = 0.5 * ( erf( ( d - c ) / ( s * &sqrt; 2 ) ) + 1 )
    unit2domain: d = erfinv( 2 * u - 1 ) * s * &sqrt; 2 + c

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

    S2PI = 1.0 / math.sqrt( 2 * math.pi )
    LS2PI = math.log( S2PI )
    SQRT2 = math.sqrt( 2.0 )

    MAXVAL = 8.5

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

        if circular is True and center == 0 and limits is not None :
            self.center = 0.5 * ( limits[0] + limits[1] )

        self.limint = self.limitedIntegral( center=center, circular=circular, 
                                            limits=limits )

        super( ).__init__( limits=limits, circular=circular, prior=prior )


    def copy( self ):
        """ Copy the prior """
        return GaussPrior( prior=self, center=self.center, scale=self.scale,
                           limits=self.limits, circular=self.circular )

    def domain2Unit( self, dval ):
        """
        Return a value in [0,1] given a value within the valid domain of
        a parameter for a Gauss distribution.

        domain2unit: u = 0.5 * ( erf( ( d - center ) / ( &sqrt; 2 * scale ( ) + 1 )

        Parameters
        ----------
        dval : float or array_like
            value(s) within the domain of a parameter

        """
        return 0.5 * ( special.erf( ( dval - self.center ) / ( self.SQRT2 * self.scale ) ) + 1 )

    def unit2Domain( self, uval ):
        """
        Return a value within the valid domain of the parameter given a value
        between [0,1] for a Gauss distribution.

        unit2domain: d = erfinv( 2 * u - 1 ) * scale * &sqrt; 2 + center

        Parameters
        ----------
        uval : float or array_like
            value(s) within [0,1]

        """
#       MAXVAL already contains the SQRT2 factor
        dom = special.erfinv( 2 * uval - 1 )
        return numpy.where( numpy.isfinite( dom ), 
                dom * self.scale * self.SQRT2 + self.center,
                numpy.copysign( self.MAXVAL, uval - 0.5 ) * self.scale + self.center )


    def result( self, x ):
        """
        Return a the result of the distribution function at x.

        Parameters
        ----------
        x : float or array_like
            value within the domain of a parameter

        """
        xs = ( x - self.center ) / self.scale
        return numpy.where( self.isOutOfLimits( x ), 0,
               self.S2PI / ( self.scale * self.limint ) * 
               numpy.exp( - 0.5 * xs * xs ) )

    def logResult( self, x ):
        """
        Return a the log of the result of the prior.

        Parameters
        ----------
        x : float
            value within the domain of a parameter

        """
        xs = ( x - self.center ) / self.scale
        sl = math.log( self.scale * self.limint )

        return numpy.where( self.isOutOfLimits( x ), -math.inf,  
                            self.LS2PI - sl - 0.5 * xs * xs ) 
#        return self.LS2PI - math.log( self.scale ) - 0.5 * ( xs * xs )

    def partialLog( self, x ):
        """
        Return partial derivative of log( Prior ) wrt x.

        Parameters
        ----------
        x : float
            the value

        """
        return - ( x - self.center ) / ( self.scale * self.scale )

    def isBound( self ):
        """ Return true if the integral over the prior is bound.  """
        return True

    def shortName( self ):
        """ Return a string representation of the prior.  """
        return str( "GaussPrior" )



