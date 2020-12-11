import math as math
import random as random

from .Tools import setAttribute as setatt
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
#  *    2017 - 2020 Do Kester

class ExponentialPrior( Prior ):
    """
    Exponential prior distribution.

        Pr( x ) = exp( -x / scale )

    By default scale = 1.

    The domain is [0,+Inf].
    In computational practice the domain is limited to about [0,36] scale units

    domain2unit: u = 1 - exp( - d / scale )
    unit2domain: d = -log( 1 - u ) * scale

    Optionally one can set a zero fraction as the fraction of u where the unit2Domain
    method returns a 0.

    Examples
    --------
    >>> pr = ExponentialPrior()                     # scale=1.0
    >>> pr = ExponentialPrior( scale=5.0 )          # scale=5

    Attributes
    ----------
    scale : float
        scale of the exponential
    zeroFraction : float
        fraction of unit that map to zero in domain and vice versa.

    Hidden Attributes
    -----------------
    _shift : float
        shift of the exponential part to make room for zeros.
    _uval : float
        random number within [0,zeroFraction].

    Attributes from Prior
    --------------------=
    lowLimit, highLimit, deltaP, _lowDomain, _highDomain

    lowLimit and highLimit cannot be used in this implementation.

    Author: Do Kester.
    """

    MAXVAL = 40

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, scale=1.0, prior=None ):
        """
        Constructor.

        Parameters:
        scale : float
            of the exponential
        prior : ExponentialPrior
            prior to copy (with new scale if applicable)

        """
        self.scale = scale
        self.zeroFraction = 0.0
        self._uval = 0.0

        super( ).__init__( domain=[0,math.inf], prior=prior )

        if prior is not None :
            self.zeroFraction = prior.zeroFraction
            self.lowLimit = prior.lowLimit
            self._uval = prior._uval

    def copy( self ):
        """ Copy the prior """
        return ExponentialPrior( scale=self.scale, prior=self )

    def __setattr__( self, name, value ):
        """
        Set attributes: zeroFraction

        Raises
        ------
        ValueError when zeroFraction is not in [0,1]

        """
        if name == "zeroFraction" :
            if not ( 0 <= value < 1 ) :
                raise ValueError( "Fraction of zeroes must be between [0,1]" )
            setatt( self, name, float( value ) )
            setatt( self, "_shift", 1.0 - value )
            random.seed( 34567 )
            setatt( self, "_rng", random )
        elif name == "_uval" :
            setatt( self, name, float( value ) )
        else :
            super( ExponentialPrior, self ).__setattr__( name, value )

    def unit2Domain( self, uval ):
        """
        Return a value within the valid domain of the parameter given a value
        between [0,1] for a Exponential distribution.

        Parameters
        ----------
        uval : float
            value within [0,1]

        """
        uv = 1 - uval
        if uv == 0 : return self.MAXVAL * self.scale
        if ( uv > self._shift ) :
            self._uval = self._rng.random() * self.zeroFraction     # arbitrary
            return 0
        else :
            return -math.log( uv / self._shift ) * self.scale

    def domain2Unit( self, dval ):
        """
        Return a value in [0,1] given a value within the valid domain of
        a parameter for a Exponential distribution.

        Parameters
        ----------
        dval : float
            value within the domain of a parameter

        """
        return ( self._uval if ( dval == 0 )
                 else 1 - math.exp( -dval / self.scale ) * self._shift )


    def result( self, x ):
        """
        Return a the result of the distribution function at x.

        Parameters
        ----------
        x : float
            value within the domain of a parameter

        """
        if self.isOutOfLimits( x ) : return 0

        return math.exp( -x / self.scale ) * self._shift / self.scale

    def logResult( self, x ):
        """
        Return a the log of the result of the distribution function to p.

        Parameters
        ----------
        x : float
            value within the domain of a parameter

        """
        if self.isOutOfLimits( x ) : return -math.inf

        return math.log( self._shift / self.scale ) - x / self.scale

    def partialLog( self, p ):
        """
        Return partial derivative of log( Prior ) wrt parameter.

        Parameters
        ----------
        p : float
            the value

        """
        return math.nan if self.isOutOfLimits( p ) else -1.0 / self.scale

    def isBound( self ):
        """ Return true if the integral over the prior is bound.  """
        return True

    def __str__( self ):
        """ Return a string representation of the prior.  """
        return str( "Exponential prior with scale = %.2f"%self.scale +
            ( (" and zero fraction = %2f"%( self.zeroFraction ) ) if self._shift < 1 else "") )

#      * End of ExponentialPrior


