import math as math

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
#  *    2016 - 2017 Do Kester.

class JeffreysPrior( Prior ):
    """
    Jeffreys prior distribution, for scale-like parameters.
    Jeffreys prior is a improper prior ( i.e. its integral is unbound ).
    Because of that it always needs limits, low and high, such that
    0 < low < high < +Inf.
    .. math::
        Pr( x ) = 1.0 / ( x * norm )   if low < x < high else 0

    where norm = log( high ) - log( low )

    No limits are set by default.

    domain2unit: u = ( log( d ) - log( lo ) ) / ( log( hi ) - log( lo ) );
    unit2domain: d = exp( u * ( log( hi ) - log( lo ) ) + log( lo ) );

    Hidden Attributes
    -----------------
    _logLo : float
        log of lowLimit
    _norm : float
        log of highLimit / lowLimit

    The default of lowLimit and _lowDomain is zero.

    """

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, limits=None, prior=None ):
        """
        Default constructor.

        Parameters
        ----------
        limits : list of 2 floats
            2 limits resp. low and high
        prior : JeffreysPrior
            prior to copy (with new limits if applicable)
        """
        super( JeffreysPrior, self ).__init__( limits=limits, prior=prior )

        #   private attributes at default values
        object.__setattr__( self, "_logLo", -math.inf )
        object.__setattr__( self, "_norm", math.inf )
        object.__setattr__( self, "_lowDomain", 0 )

        if limits is None and prior is not None :
            limits = ( prior.lowLimit, prior.highLimit )
        if limits is not None :
            self.setLimits( limits )
        else :
            self.lowLimit = 0.0

    def copy( self ):
        return JeffreysPrior( prior=self )

    def __setattr__( self, name, value ) :
        if name in ["_logLo", "_norm"] :
            object.__setattr__( self, name, float( value ) )
        else :
            super( JeffreysPrior, self ).__setattr__( name, value )

        if name == "lowLimit" or name == "highLimit" :
            self._logLo = -math.inf if ( self.lowLimit <= 0 ) else math.log( self.lowLimit )
            self._norm = math.log( self.highLimit ) - self._logLo

    def getIntegral( self ) :
        """
        Return the integral of JeffreysPrior from lowLimit to highLimit.
        """
        return self._norm

    def domain2Unit( self, dval ):
        """
        Return a value in [0,1] given a value within the valid domain of
        a parameter for a Jeffreys distribution.

        Parameters
        ----------
        dval : float
            value within the domain of a parameter

        """
        u = ( math.log( dval ) - self._logLo ) / self._norm
        if math.isnan( u ) :
            raise AttributeError( "Limits are needed for JeffreysPrior" )
        return u


    def unit2Domain( self, uval ):
        """
        Return a value within the valid domain of the parameter given a value
        between [0,1] for a Jeffreys distribution.

        Parameters
        ----------
        uval : float
            value within [0,1]

        """
        d = math.exp( uval * self._norm + self._logLo )
        if math.isnan( d ) :
            raise AttributeError( "Limits are needed for JeffreysPrior" )
        return d

    def result( self, x ):
        """
        Return a the result of the distribution function at x.

        Parameters
        ----------
        x : float
            value within the domain of a parameter

        """
        r = 0 if self.isOutOfLimits( x ) else 1.0 / ( x * self._norm )
        if math.isnan( r ) :
            raise AttributeError( "Limits are needed for JeffreysPrior" )
        return r

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
        return math.nan if self.isOutOfLimits( p ) else -1 / p

    def isBound( self ):
        """ Return true if the integral over the prior is bound.  """
        return self.hasLowLimit( ) and self.hasHighLimit( )

    def __str__( self ):
        """ Return a string representation of the prior.  """
        return str( "Jeffreys prior " + ( "unbound." if not self.isBound( )
            else ( "between %.2f and %.2f"%( self.lowLimit, self.highLimit ) ) ) )

#      * End of JeffreysPrior


