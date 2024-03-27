import math as math
import random as random

from .Tools import setAttribute as setatt
from .LaplacePrior import LaplacePrior

__author__ = "Do Kester"
__year__ = 2024
__license__ = "GPL3"
__version__ = "3.2.1"
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
#  *    2017 - 202024 Do Kester

class ExponentialPrior( LaplacePrior ):
    """
    Exponential prior distribution.

        Pr( x ) = exp( -x / scale )

    By default scale = 1.

    The domain is [0,+Inf].
    In computational practice the domain is limited to about [0,36] scale units

    Wrapper for:
    LaplacePrior( center=0, scale=scale, limits=[0, hilim] )

    Examples
    --------
    >>> pr = ExponentialPrior()                     # scale=1.0
    >>> pr = ExponentialPrior( scale=5.0 )          # scale=5

    Attributes
    ----------
    scale : float
        scale of the exponential

    Attributes from Prior
    --------------------=
    lowLimit, highLimit, deltaP, _lowDomain, _highDomain

    Author: Do Kester.
    """

    MAXVAL = 40

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, scale=1.0, hilimit=math.inf, prior=None ):
        """
        Constructor.

        Parameters:
        scale : float
            of the exponential
        hilimit : float
            high limit
        prior : ExponentialPrior
            prior to copy (with new scale if applicable)

        """
        super( ).__init__( scale=scale, limits=[0,hilimit], prior=prior )

        self._lowDomain = 0 

    def copy( self ):
        """ Copy the prior """
        return ExponentialPrior( scale=self.scale, hilimit=self.limits[1], 
            prior=self )

    def shortName( self ) :
        return "ExponentialPrior"



