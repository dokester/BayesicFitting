import numpy as numpy

from .Tools import setAttribute as setatt

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
#  *    2019 - 2020 Do Kester


class Modifiable( object ):
    """
    Class adjoint to Model which implements the modifiable behaviour of some Models.

    In the inhertance list is should be *before* Model as it changes the behaviour of Model.

    """
    def __init__( self, modifiable=True ) :
        """
        Constructor for Modifiable

        Parameters
        ----------
        modifiable: bool
            True if the Model is to be considered modifiable.
        """

        setatt( self, "modifiable", modifiable )


    def isModifiable( self ) :
        return self.modifiable


    def vary( self, location=None, rng=None, **kwargs ) :
        """
        Vary the structure of a Modifiable Model
        Default implementation: does nothing.

        Parameters
        ----------
        location : int
            index of the item to be modified; otherwise random
        rng : RNG
            random number generator
        kwargs : keyword arguments
            for specific implementations
        """
        return True




