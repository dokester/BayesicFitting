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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2017 Do Kester

class UniformPrior( Prior ):
    """
    Uniform prior distribution, for location parameters.

    A uniform prior is a improper prior ( i.e. its integral is unbound ).
    Because of that it always needs limits, low and high, such that
    -Inf < low < high < +Inf.
    .. math::
        Pr( x ) = 1 / ( high - low )   if low < x < high else 0

    domain2Unit: u = ( d - lo ) / range
    unit2Domain: d = u * range + lo

    Hidden Attributes
    -----------------
    _range : float
        valid range ( highLimit - lowLimit )

    """

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, limits=None, prior=None ):
        """ Constructor.  """
        super( UniformPrior, self ).__init__( limits=limits, prior=prior )

    def copy( self ):
        """ Return a (deep) copy of itself. """
        return UniformPrior( prior=self, limits=[self.lowLimit,self.highLimit] )

    def __setattr__( self, name, value ) :
        if name == "_range" :
            object.__setattr__( self, name, value )
        else :
            super( UniformPrior, self ).__setattr__( name, value )

        if name == "lowLimit" or name == "highLimit" :
            self._range = self.highLimit - self.lowLimit

    def getIntegral( self ) :
        """
        Return integral of UniformPrior from lowLimit to highLimit.
        """
        return self._range

    def domain2Unit( self, dval ):
        """
        Return a value in [0,1] given a value within the valid domain of
        a parameter for a Uniform distribution.

        Parameters
        ----------
        dval : float
            value within the domain of a parameter

        """
        if math.isinf( self._range ) :
            raise AttributeError( "Limits are needed for UniformPrior" )
        return 0 if self.isOutOfLimits( dval ) else ( dval - self.lowLimit ) / self._range

    def unit2Domain( self, uval ):
        """
        Return a value within the valid domain of the parameter given a value
        between [0,1] for a Uniform distribution.

        Parameters
        ----------
        uval : float
            value within [0,1]

        """
        if math.isinf( self._range ) :
            raise AttributeError( "Limits are needed for UniformPrior" )
        return uval * self._range + self.lowLimit

    def result( self, x ):
        """
        Return a the result of the distribution function at x.

        Parameters
        ----------
        x : float
            value within the domain of a parameter

        """
        if math.isinf( self._range ) :
            raise AttributeError( "Limits are needed for UniformPrior" )

        return 0.0 if self.isOutOfLimits( x ) else 1.0 / self._range


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
        return math.nan if self.isOutOfLimits( p ) else 0

    def isBound( self ):
        """ Return true if the integral over the prior is bound.  """
        return self.hasLowLimit( ) and self.hasHighLimit( )

    def __str__( self ):
        """ Return a string representation of the prior.  """
        return str( "UniformPrior " + ( "unbound." if not self.isBound( )
                else ( "between %.2f and %.2f"%( self.lowLimit, self.highLimit ) ) ) )

#      * End of UniformPrior


