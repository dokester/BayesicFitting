import numpy
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


class CauchyPrior( Prior ):
    """
    Cauchy prior distribution.
    .. math::
        Pr( x ) =  scale / ( \pi * ( scale^2 + x^2 )

    By default: scale = 1.
    It can also have a limited domain. By default the domain is [-Inf,+Inf].
    In computational practice it is limited to [-1e16, 1e16]

    Equivalent to a double-sided exponential prior

    domain2unit: u = arctan( d / s ) / pi + 0.5
    unit2domain: d = tan( ( u - 0.5 ) * pi ) * s

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
    def __init__( self, scale=1, prior=None ):
        """
        Constructor.

        Parameters
        ----------
        scale : float
            of the exponential
        prior : CauchyPrior
            prior to copy (with new scale if applicable)

        """
        super( CauchyPrior, self ).__init__( prior=prior )
        self.scale = scale

    def copy( self ):
        return CauchyPrior( prior=self, scale=self.scale )

    def domain2Unit( self, dval ):
        """
        Return a value in [0,1] given a value within the valid domain of
        a parameter for a Cauchy distribution.

        domain2unit: u = arctan( d / s ) / pi + 0.5

        Parameters
        ----------
        dval : float
            value within the domain of a parameter

        """
        return numpy.arctan( dval / self.scale ) / math.pi + 0.5

    def unit2Domain( self, uval ):
        """
        Return a value within the valid domain of the parameter given a value
        between [0,1] for a Cauchy distribution.

        unit2domain: d = tan( ( u - 0.5 ) * pi ) * self.scale

        Parameters
        ----------
        uval : float
            value within [0,1]

        """
        return numpy.tan( ( uval - 0.5 ) * math.pi ) * self.scale

    def result( self, x ):
        """
        Return a the result of the distribution function at x.

        Parameters
        ----------
        x : float
            value within the domain of a parameter

        """
        return self.scale / ( ( self.scale * self.scale + x * x ) * math.pi )

# logResult has no better definition than the default: just take the math.log of result.
# No specialized method here.

    def partialLog( self, p ):
        """
        Return partial derivative of log( Prior ) wrt parameter.

        Parameters
        ----------
        p : float
            the value

        """
        return - 2 * p / ( self.scale * self.scale + p * p )

    def isBound( self ):
        """ Return true if the integral over the prior is bound.  """
        return True

    def __str__( self ):
        """ Return a string representation of the prior.  """
        return str( "Cauchy prior with scale = %.2f"%( self.scale ) )



