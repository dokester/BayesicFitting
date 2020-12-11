
from .UniformPrior import UniformPrior

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
#  *    2016 - 2020 Do Kester

class CircularUniformPrior( UniformPrior ):
    """
    Circular Uniform prior distribution, for location parameters.
    The lowLimit is wrapped onto the highLimit.

    A wrapper around:
        UniformPrior( circular=... limits=... )

    Examples
    --------
    >>> pr = CircularUniformPrior( circular=math.pi )       # circular between [0,pi]
    >>> pr = CircularUniformPrior( limits=[3,10] )          # circular between [3,10]

    Attributes from Prior
    --------------------=
    lowLimit, highLimit, deltaP, circular, _lowDomain, _highDomain, _umin, _urng

    """

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, circular=None, limits=None, prior=None ):
        """
        Constructor.

        Parameters
        ----------
        limits : array of 2 floats
            [low,high]  range of the prior. Low is wrapped onto high.
        circular : float
            period of circularity
        prior : CircularUniformPrior
            to be copied.

        """
        if circular is None :
            circular = True             ## use limits as period

        super( ).__init__( circular=circular, limits=limits, prior=prior )

    def copy( self ):
        """ Return a (deep) copy of itself. """
        return CircularUniformPrior( prior=self, limits=self.limits, circular=self.circular )

    def __str__( self ):
        """ Return a string representation of the prior.  """
        return str( "CircularUniformPrior " + ( "unbound." if not self.isBound( )
                else ( "period [%.2f..%.2f]"%( self.lowLimit, self.highLimit ) ) ) )



