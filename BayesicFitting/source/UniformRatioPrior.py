import math
import numpy as numpy
import warnings

from .Prior import Prior
from .Tools import setAttribute as setatt

__author__ = "Do Kester"
__year__ = 2026
__license__ = "GPL3"
__version__ = "3.3.0"
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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 202026 Do Kester



class UniformRatioPrior( Prior ):
    """
    Distribution of the ratio of two uniform distributed, positive variables.

    A uniform ratio prior is a proper prior.
        Pr( x ) = 0         if x < 0
                  0.5       if 0 < x < 1
                  0.5/x**2  if x > 1

    domain2Unit.
        u = 0.5 d       if 0 < d < 1
            1 - 0.5/d   if d > 1

    unit2Domain.
        d = 2 u         if 0   < u < 0.5
            1/2(1-u)    if 0.5 < u < 1

    The keyword "circular" does not apply to this prior.

    Examples
    --------
    >>> pr = UniformRatioPrior()

    Attributes from Prior
    --------------------=
    lowLimit, highLimit, deltaP, _lowDomain, _highDomain


    """
    MAXVAL = 1e14               ## maximum value for u2d and d2u
    LOG05 = math.log( 0.5 )


    #  *********CONSTRUCTORS***************************************************
    def __init__( self, range=None, median=1.0, limits=None, prior=None ):
        """
        Constructor.

        Parameters
        ----------
        range : None or float
            set limits tp [1/range, range]
        median : float
            median point of the ratio
        limits : None or [float,float]
            None    no limits are set
            2 floats    lowlimit and highlimit
        prior : UniformRatioPrior
            to be copied
        """
        setatt( self, "median", median )

        if range is not None :
            limits = [1/range, range]

        self.limint = self.limitedIntegral( limits=limits )

        super( ).__init__( limits=limits, domain=[0,math.inf], prior=prior )

    def copy( self ):
        """ 
        Return a (deep) copy of itself. 
        """
        return UniformRatioPrior( prior=self, limits=self.limits )

    def getIntegral( self ) :
        """
        Return integral of UniformRatioPrior from lowLimit to highLimit.
        """
        return 1.0

    def domain2Unit( self, dval ):
        """
        Return a value in [0,1] given a positive ratio value

        Parameters
        ----------
        dval : float
            value within the domain of a parameter

        """
        dv = dval / self.median
        try :
            return 1 - 0.5 / dv if dv > 1 else 0.5 * dv
        except ValueError :
            with warnings.catch_warnings():
                warnings.simplefilter( "ignore", category=RuntimeWarning )
                return numpy.where( dv > self.MAXVAL, 1.0, 
                       numpy.where( dv < 1, 0.5 * dv, 1 - 0.5 / dv ) )

    def unit2Domain( self, uval ):
        """
        Return a ratio value given a value in [0,1].

        Parameters
        ----------
        uval : float
            value within [0,1]

        """
        uv = 2 * uval
        try :
            dv = uv if uv < 1 else ( 1 / ( 2 - uv ) if uv < 2 else self.MAXVAL )
            return dv * self.median
        except ValueError :
            with warnings.catch_warnings():
                warnings.simplefilter( "ignore", category=RuntimeWarning )
                dv =  numpy.where( uv < 1, uv, 
                       numpy.where( uv == 2, self.MAXVAL, 1 / ( 2 - uv ) ) )
                return dv * self.median

    def result( self, x ):
        """
        Return a the result of the distribution function at x.

        Parameters
        ----------
        x : float or array_like
            value within the domain of a parameter

        """
        with warnings.catch_warnings():
            warnings.simplefilter( "ignore", category=RuntimeWarning )
            hm = 0.5 / self.median
            return numpy.where( self.isOutOfLimits( x ), 0.0, 
                   numpy.where( x > self.median, hm * ( self.median / x )**2, hm ) / self.limint )

    def logResult( self, x ):
        """
        Return a the log of the result of the distribution function at x.

        Parameters
        ----------
        x : float or array_like
            value within the domain of a parameter

        """
        with warnings.catch_warnings():
            warnings.simplefilter( "ignore", category=RuntimeWarning )
            return numpy.where( x > 1, self.LOG05 - 2 * numpy.log( x ), 
                   numpy.where( x < 0, -math.inf, self.LOG05 ) )

        ## logResult has no better definition than the default: the log of result.
        ## No specialized method here.

    def partialLog( self, p ):
        """
        Return partial derivative of log( Prior ) wrt parameter.

        Parameters
        ----------
        p : float or array_like
            the value

        """
        with warnings.catch_warnings():
            warnings.simplefilter( "ignore", category=RuntimeWarning )
            return numpy.where( p > self.median, -2 / ( p * self.median ), 0 )

    def isBound( self ):
        """ 
        Return true if the integral over the prior is bound.  
        """
        return True

    def shortName( self ):
        """ 
        Return a string representation of the prior.  
        """
        return "UniformRatioPrior"




