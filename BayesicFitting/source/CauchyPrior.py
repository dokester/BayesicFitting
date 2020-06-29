import numpy
import math

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
    def __init__( self, center=0.0, scale=1, prior=None ):
        """
        Constructor.

        Parameters
        ----------
        center : float
            of the prior
        scale : float
            of the prior
        prior : CauchyPrior
            prior to copy (with new scale if applicable)

        """
        super( CauchyPrior, self ).__init__( prior=prior )
        self.center = center
        self.scale = scale

    def copy( self ):
        return CauchyPrior( prior=self, center=self.center, scale=self.scale )

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

    def __str__( self ):
        """ Return a string representation of the prior.  """
        return str( "Cauchy prior with scale = %.2f"%( self.scale ) )



