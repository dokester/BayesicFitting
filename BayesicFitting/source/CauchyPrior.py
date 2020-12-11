import numpy
import math

from .Prior import Prior

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
__version__ = "2.6.2"
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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2010 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2020 Do Kester


class CauchyPrior( Prior ):
    """
    Cauchy prior distribution.

        Pr( x ) =  scale / ( &pi; * ( scale^2 + ( x - center )^2 )

    By default: center = 0 and scale = 1.

    It can also have a limited domain. (To be done)
    By default the domain is [-Inf,+Inf].
    In computational practice it is limited to [-1e16, 1e16]

    domain2unit: u = arctan( ( d - c ) / s ) / pi + 0.5
    unit2domain: d = tan( ( u - 0.5 ) * pi ) * s + c

    Examples
    --------
    >>> pr = CauchyPrior()                         # center=0, scale=1
    >>> pr = CauchyPrior( center=1.0, scale=0.5 )
    >>> pr = CauchyPrior( limits=[0,None] )        # lowlimit=0, highlimit=inf
    >>> pr = CauchyPrior( center=1, circular=3 )   # circular between 0.5 and 2.5

    Attributes
    ----------
    center : float
        center of the Cauchy prior
    scale : float
        scale of the Cauchy prior

    Attributes from Prior
    --------------------=
    lowLimit, highLimit, deltaP, _lowDomain, _highDomain

    lowLimit and highLimit cannot be used in this implementation.

    """

    #  *********CONSTRUCTOR***************************************************
    def __init__( self, center=0.0, scale=1, limits=None, circular=False, prior=None ):
        """
        Constructor.

        Parameters
        ----------
        center : float
            of the prior
        scale : float
            of the prior
        limits : None or [float,float]
            None    no limits are set
            2 floats    lowlimit and highlimit
        circular : bool or float
            bool : y|n circular with period from limits[0] to limits[1]
            float : period of circularity
        prior : CauchyPrior
            prior to copy (with new scale if applicable)

        """
        self.center = center
        self.scale = scale

        super( CauchyPrior, self ).__init__( limits=limits, circular=circular, prior=prior )

    def copy( self ):
        return CauchyPrior( prior=self, center=self.center, scale=self.scale,
                            limits=self.limits, circular=self.circular )

    def domain2Unit( self, dval ):
        """
        Return a value in [0,1] given a value within the valid domain of
        a parameter for a Cauchy distribution.

        domain2unit: u = arctan( ( d - c ) / s ) / pi + 0.5

        Parameters
        ----------
        dval : float
            value within the domain of a parameter

        """
        return numpy.arctan( ( dval - self.center ) / self.scale ) / math.pi + 0.5

    def unit2Domain( self, uval ):
        """
        Return a value within the valid domain of the parameter given a value
        between [0,1] for a Cauchy distribution.

        unit2domain: d = tan( ( u - 0.5 ) * pi ) * s + c

        Parameters
        ----------
        uval : float
            value within [0,1]

        """
        return numpy.tan( ( uval - 0.5 ) * math.pi ) * self.scale + self.center

    def result( self, x ):
        """
        Return a the result of the distribution function at x.

        Parameters
        ----------
        x : float
            value within the domain of a parameter

        """
        xc = x - self.center
        return self.scale / ( ( self.scale * self.scale + xc * xc ) * math.pi )

# logResult has no better definition than the default: just take the math.log of result.
# No specialized method here.

    def partialLog( self, x ):
        """
        Return partial derivative of log( Prior ) wrt parameter.

        Parameters
        ----------
        x : float
            the value

        """
        xc = x - self.center
        return - 2 * xc / ( self.scale * self.scale + xc * xc )

    def isBound( self ):
        """ Return true if the integral over the prior is bound.  """
        return True

    def shortName( self ):
        """ Return a string representation of the prior.  """
        return str( "CauchyPrior" )



