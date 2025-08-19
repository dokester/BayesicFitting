import math
import numpy
import warnings

from .Prior import Prior

__author__ = "Do Kester"
__year__ = 2025
__license__ = "GPL3"
__version__ = "3.2.4"
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
#  *    2016 - 202025 Do Kester


class LaplacePrior( Prior ):
    """
    Laplace prior distribution.

        Pr( x ) = 1 / ( 2 s ) exp( - |x - c| / s )

    By default: c = center = 0.0 and s = scale = 1.

    It can also have a limited domain.
    By default the domain is [-Inf,+Inf].
    In computational practice the domain is limited to about [-36,36] scale units

    Equivalent to a double-sided exponential prior

    domain2unit: 
     u = 0.5 * exp( ( d - c ) / scale )             if d < c
         1.0 - 0.5 * exp( ( c - d ) / scale )       otherwise
    unit2domain: 
     d = c + log( 2 * u ) * scale                   if u < 0.5
         c - log( 2 * ( 1 - u ) ) * scale           otherwise

    Examples
    --------
    >>> pr = LaplacePrior()                         # center=0, scale=1
    >>> pr = LaplacePrior( center=1.0, scale=0.5 )
    >>> pr = LaplacePrior( limits=[0,None] )        # limites to values >= 0
    >>> pr = LaplacePrior( center=1, circular=3 )   # circular between 0.5 and 2.5

    Attributes
    ----------
    center : float
        center of the Laplace prior
    scale : float
        scale of the Laplace prior

    Attributes from Prior
    --------------------=
    lowLimit, highLimit, deltaP, _lowDomain, _highDomain

    lowLimit and highLimit cannot be used in this implementation.

    """
    MAXVAL = 40                 ## scale units

    #  *********CONSTRUCTOR***************************************************
    def __init__( self, center=0.0, scale=1.0, limits=None, circular=False, prior=None ):
        """
        Constructor.

        Parameters
        ----------
        center : float
            of the prior
        scale : float
            of the prior
        limits : None or list of 2 float/None
            None : no limits.
            2 limits, resp low and high
        circular : bool or float
            bool : y|n circular with period from limits[0] to limits[1]
            float :period of circularity
        prior : LaplacePrior
            prior to copy (with new scale if applicable)

        """
        self.center = center
        self.scale = scale

        if circular is True and center == 0 and limits is not None :
            self.center = 0.5 * ( limits[0] + limits[1] )    

        self.limint = self.limitedIntegral( center=center, circular=circular, 
                                            limits=limits )

        super().__init__( limits=limits, circular=circular, prior=prior )


    def copy( self ):
        return LaplacePrior( prior=self, center=self.center, scale=self.scale,
                             limits=self.limits, circular=self.circular )

    def domain2Unit( self, dval ):
        """
        Return a value in [0,1] given a value within the valid domain of
        a parameter for a Laplace distribution.

         u = 0.5 * exp( ( d - c ) / s )       if d < c else
             1.0 - 0.5 * exp( ( c - d ) / s )

        Parameters
        ----------
        dval : float
            value within the domain of a parameter

        """
        dv = ( dval - self.center ) / self.scale
        try :
            uval = ( 0.5 * math.exp( dv ) if dv < 0 else 
                    1.0 - 0.5 * math.exp( -dv ) )
        except ValueError :
            uval = numpy.where( dv < 0, 0.5 * numpy.exp(  dv ),
                                  1.0 - 0.5 * numpy.exp( -dv ) )
        return uval

    def unit2Domain( self, uval ):
        """
        Return a value within the valid domain of the parameter given a value
        between [0,1] for a Laplace distribution.

         d = c + log( 2 * u ) * scale           if u < 0.5 else
             c - log( 2 * ( 1 - u ) ) * scale

        Parameters
        ----------
        uval : float
            value within [0,1]

        """
        uv = 2 * uval
        try :
            if uv == 0 :
                dv = -self.MAXVAL
            elif uv == 2 :
                dv = self.MAXVAL
            elif uv <= 1 :
                dv = math.log( uv )
            else :
                dv = -math.log( 2 - uv )
        except ValueError :
            with warnings.catch_warnings():
                warnings.simplefilter( "ignore", category=RuntimeWarning )
                dv = numpy.where( ( uv == 0 ) | ( uv == 2 ),
                    numpy.copysign( self.MAXVAL, uv - 1 ),
                    numpy.where( uv <= 1, numpy.log( uv ),
                                 -numpy.log( 2 - uv ) ) )
        return self.center + dv * self.scale

    def result( self, x ):
        """
        Return a the result of the distribution function at x.

        Parameters
        ----------
        x : float
            value within the domain of a parameter

        """
        xs = ( x - self.center ) / self.scale
        return numpy.where( self.isOutOfLimits( x ), 0, 
                0.5 * numpy.exp( -abs( xs ) ) / ( self.scale * self.limint ) )

    def logResult( self, x ):
        """
        Return a the log of the result of the distribution function to p.

        Parameters
        ----------
        x : float
            value within the domain of a parameter

        """
        xs = ( x - self.center ) / self.scale
        sl = -math.log( 2 * self.scale * self.limint )
        return numpy.where( self.isOutOfLimits( x ), -math.inf, sl - abs( xs ) )

    def partialLog( self, x ):
        """
        Return partial derivative of log( Prior ) wrt parameter.

        Parameters
        ----------
        x : float
            the value

        """
        if x == self.center : return 0                  ## actually a cusp
        elif self.isOutOfLimits( x ) : return math.nan

        return -1 / self.scale if x > self.center else 1 / self.scale

    def isBound( self ):
        """ Return true if the integral over the prior is bound.  """
        return True

    def shortName( self ) :
        return "LaplacePrior"


