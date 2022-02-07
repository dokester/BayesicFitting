import numpy as numpy
import math
from . import Tools
from .Formatter import formatter as fmt

from .Engine import Engine

__author__ = "Do Kester"
__year__ = 2022
__license__ = "GPL3"
__version__ = "3.0.0"
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
#  *    2018 - 2022 Do Kester

class OrderEngine( Engine ):
    """
    The OrderEngine is the base engine for all order problems

    Author       Do Kester.

    """
    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, seed=4213, verbose=0 ):
        """
        Constructor.

        Parameters
        ----------
        walkers : SampleList
            walkers to be diffused
        errdis : ErrorDistribution
            error distribution to be used
        copy : OrderEngine
            to be copied
        seed : int
            for random number generator

        """
        super( ).__init__( walkers, errdis, copy=copy, seed=seed, verbose=verbose )

    def copy( self ):
        """ Return copy of this.  """
        return OrderEngine( self.walkers, self.errdis, copy=self )

    #  *********EXECUTE***************************************************
    def execute( self, kw, lowLhood, append=False, iteration=0 ):
        """ 
        Execute the engine by diffusing the parameters.
        
        Parameters
        ----------   
        kw : walker-id
            walker to diffuse
        lowLhood : float
            lower limit in logLikelihood
        append : bool
            not used here
        iteration : int
            iteration number        

        Returns
        -------
        int : the number of successfull moves
           
        """
        self.reportCall()
        t = 0
        k = 0
        while t == 0 and k < self.maxtrials :
            t = self.executeOnce( kw, lowLhood )
            k = k + 1
        
        return t

    def __str__( self ):
        return str( "OrderEngine" )

    def calculateUnitRange( self ) :
        """
        Irrelevant for OrderProblems
        """
        pass
