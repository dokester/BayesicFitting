import numpy as numpy
import math as math

__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"


#  *
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

class Prior( object ):
    """
    Base class defining prior distributions.
    Most of the lower and upper limit handling is done in this class.

    Two methods need to be defined which map the values between [0,1]
    on to the domain, and vice versa: unit2Domain and domain2Unit.

    The copy method is also necessary.

    Attributes
    ----------
    lowLimit : float
        low limit on the Prior
    highLimit : float
        high limit on the Prior
    deltaP : float
        width of numerical partial derivative calculation

    Hidden Attributes
    -----------------
    _lowDomain : float
        lower limit of the Priors possible values
    _highDomain : float
        upper limit of the Priors possible values

    """

    #*********CONSTRUCTORS***************************************************
    def __init__( self, limits=None, prior=None ):
        """
        Default constructor.

        Parameters
        ----------
        limits : list of 2 floats
            2 limits resp. low and high
        prior : Prior
            prior to copy (with new limits if applicable)
        """
        super( object, self ).__init__()

        self.deltaP = 0.0001
        self._lowDomain = -math.inf
        self._highDomain = math.inf

        object.__setattr__( self, "deltaP", 0.001 )             # for numerical partials
        object.__setattr__( self, "lowLimit", -math.inf )       # Lower limit.
        object.__setattr__( self, "highLimit", math.inf )       # Upper limit.
#       private properties of the Prior
        object.__setattr__( self, "_lowDomain", -math.inf )     # Lower limit of the Priors possible domain.
        object.__setattr__( self, "_highDomain", math.inf )     # Upper limit of the Priors possible domain

        self.setLimits( limits )
        if prior is not None :
            self.deltaP = prior.deltaP

    def copy( self ) :
        """ Return a copy """
        return Prior( prior=self, limits=self.limits )

    def setLimits( self, limits ):
        """
        Set limits.
        It is asserted that limits[0] is smaller than limits[1].

        Parameters
        ----------
        limits : None or list of 2 float
            None : limits are set to [-inf,+inf]
            the [low,high] limits.
        Raises
        ------
        ValueError when low limit is larger than high limit

        """
        if limits is None :
            limits = [-math.inf,+math.inf]

        if limits[0] > limits[1] :
            raise ValueError( "The lowlimit %f must be smaller than the high limit %f"%
                                ( limits[0], limits[1] ) )
        if not ( self._lowDomain <= limits[0] < limits[1] <= self._highDomain ) :
            raise ValueError( "Limits out of order or out of domain" )

        self.lowLimit = limits[0]
        self.highLimit = limits[1]

    def __setattr__( self, name, value ) :
        """
        Set attributes: lowLimit, highLimit, deltaP, _lowDomain, _highDomain.

        Also set scale for Priors that need a scale.

        """
        keys = ["lowLimit", "highLimit", "deltaP", "scale", "_lowDomain", "_highDomain"]
        if name == "scale" and value <= 0 :
            raise ValueError( "Scale must be positive" )

        if name in keys :
            object.__setattr__( self, name, float( value ) )
        else :
            raise AttributeError( repr( self ) + " object has no attribute " + name )

    def unsetLimits( self ):
        """ Remove all limits.  """
        self.lowLimit = self._lowDomain
        self.highLimit = self._highDomain

    def isOutOfLimits( self, par ):
        """
        True if the parameter is out of limits

        Parameters
        ----------
        par : float
            the parameter to check

        """
        return ( par < self.lowLimit ) or ( par > self.highLimit )

    def checkLimit( self, par ):
        """
        Check whether the parameter is within limits.

        Parameters
        ----------
        par : float
            the parameter to check

        Raises
        ------
            ValueError when outside limits.

        """
        if self.isOutOfLimits( par ):
            raise ValueError( "Parameter outside supplied limits" )

    def stayInLimits( self, par ):
        """
        Return lower limit or upper limit when parameter is outside.

        Parameters
        ----------
        par : float
            the parameter to check

        """
        if par < self.lowLimit:
            return self.lowLimit
        if par > self.highLimit:
            return self.highLimit
        return par

    def hasLowLimit( self ):
        """ Return true if the prior has its low limits set.  """
        return self.lowLimit > self._lowDomain

    def hasHighLimit( self ):
        """ Return true if the prior has its high limits set.  """
        return self.highLimit < self._highDomain

    def hasLimits( self ):
        """ Return true if it has any limits.  """
        return self.hasLowLimit() and self.hasHighLimit()

    def getLimits( self ):
        """ Return the limits.  """
        return numpy.array( [ self.lowLimit, self.highLimit ] )

    def getIntegral( self ) :
        """
        Return the integral of the prior over the valid range.

        Default: 1.0 (for bound priors)
        """
        return 1.0

    def getRange( self ):
        """ Return the range.  """
        return self.highLimit - self.lowLimit

    def domain2Unit( self, dval ):
        """
        Return a value in [0,1] given a value within the valid domain of
        a parameter for a distribution.

        Parameters
        ----------
        dval : float
            value within the domain of a parameter

        """
        pass

    def unit2Domain( self, uval ):
        """
        Return a value within the valid domain of the parameter given a value
        between [0,1] for a distribution.

        Parameters
        ----------
        uval : float
            value within [0,1]

        """
        pass

    def result( self, p ):
        """
        Return value of the Prior at a given value.

        If result is not defined, fall back to numerical derivative od Domain2Unit.

        Parameters
        ----------
        p : float
            the value

        """
        return self.numPartialDomain2Unit( p )
#        return 0.0 if self.isOutOfLimits( p ) else self.partialDomain2Unit( p )

    def partialDomain2Unit( self, p ):
        """
        Return the derivative of Domain2Unit, aka the result of the distribution at p

        Parameters
        ----------
        p : float
            the value

        """
        return self.result( p )

    def logResult( self, p ) :
        """
        Return the log of the result; -inf when p == 0.

        Parameters
        ----------
        p : float
            the value

        """
        try :
            return math.log( self.result( p ) )
        except :
            return -math.inf

#    def partialDomain2Unit( self, dval ):
        """
        Return a the derivate of the domain2Unit function to dval.
        By default: numeric derivative.

        Parameters
        ----------
        dval : float
            value within the domain of a parameter

        """
#        return self.numPartialDomain2Unit( dval )

    def numPartialDomain2Unit( self, dval ):
        """
        Return a the numeric derivate of the domain2Unit function to dval.

        Parameters
        ----------
        dval : float
            value within the domain of a parameter

        """
        return ( ( self.domain2Unit( dval + self.deltaP ) -
                   self.domain2Unit( dval - self.deltaP) ) /
                        ( 2 * self.deltaP ) )

    def partialLog( self, p ):
        """
        Return partial derivative of log( Prior ) wrt parameter.
        default numPartialLog

        Parameters
        ----------
        p : float
            the value

        """
        return self.numPartialLog( p )

    def numPartialLog( self, p ):
        """
        Return the numeric partial derivative of log( Prior ) wrt parameter.
        Parameters
        ----------
        p : float
            the value

        """
        if self.isOutOfLimits( p ) : return math.nan
#        if math.isinf( p ) : return -p
        rm = self.logResult( p - self.deltaP )
        rp = self.logResult( p + self.deltaP )
        return ( rp - rm ) / ( 2 * self.deltaP )

    def isBound( self ):
        """ Return true if the integral over the prior is bound.  """
        return False

    def __str__( self ):
        """ Return a string representation of the prior.  """
        pass

#      * End of Prior


