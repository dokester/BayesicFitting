
from .UniformPrior import UniformPrior

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
#  *    2016 - 2020 Do Kester

class CircularUniformPrior( UniformPrior ):
    """
    Cricular Uniform prior distribution, for location parameters.
    The lowLimit is wrapped onto the highLimit.

    A circular uniform prior is a proper prior ( i.e. its integral is bound ).
    Because of its wrapping around needs limits, low and high, such that
    -Inf < low < high < +Inf.

        Pr( x ) = 1 / ( high - low )   if low < x < high else 0

    For computational purposes the unit range is from [1/3..2/3]; the u value
    always returns in that range. The wings are needed for the wrapping.

    The d value aways returns inside the range [low..high]

    domain2Unit: u = ( d - lo ) / range
                 u = ( u + 1 ) / 3              ## shrink to [1/3..2/3]
    The u value can reach any value in [0..1].
    unit2Domain: u = ( 3 * u ) % 1.0            ## wrap around
                 d = u  * range + lo

    Attributes from UniformPrior
    ----------------------------
    _range : float
        valid range ( highLimit - lowLimit )

    Attributes from Prior
    --------------------=
    lowLimit, highLimit, deltaP, _lowDomain, _highDomain

    """

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, limits=None, prior=None ):
        """
        Constructor.

        Parameters
        ----------
        limits : array of 2 floats
            [low,high]  range of the prior. Low is wrapped onto high.
        prior : CircularUniformPrior
            to be copied.

        """
        super( CircularUniformPrior, self ).__init__( limits=limits, prior=prior )

    def copy( self ):
        """ Return a (deep) copy of itself. """
        return CircularUniformPrior( prior=self, limits=[self.lowLimit,self.highLimit] )

    def isCircular( self ) :
        """
        Always True
        """
        return True

    def domain2Unit( self, dval ):
        """
        Return a value in [0,1] given a value within the valid domain of
        a parameter for a Uniform distribution.

        Parameters
        ----------
        dval : float
            value within the domain of a parameter

        """
        uval = super( CircularUniformPrior, self ).domain2Unit( dval )
        return ( uval + 1 ) / 3.0

    def unit2Domain( self, uval ):
        """
        Return a value within the valid domain of the parameter given a value
        between [0,1] for a Uniform distribution.

        Parameters
        ----------
        uval : float
            value within [0,1]

        """
        uval = ( uval * 3 ) % 1.0
        return super( CircularUniformPrior, self ).unit2Domain( uval )


    def __str__( self ):
        """ Return a string representation of the prior.  """
        return str( "CircularUniformPrior " + ( "unbound." if not self.isBound( )
                else ( "period [%.2f..%.2f]"%( self.lowLimit, self.highLimit ) ) ) )



