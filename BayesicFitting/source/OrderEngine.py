import numpy as numpy
import math
from . import Tools
from .Formatter import formatter as fmt

from .Engine import Engine

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
#  *    2018 - 2025 Do Kester

class OrderEngine( Engine ):
    """
    The OrderEngine is the base engine for all order problems

    Attributes from Engine
    ----------------------
    walkers, errdis, maxtrials, nstep, slow, rng, report, phantoms, verbose

    Author       Do Kester.

    """
    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, **kwargs ):
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
        kwargs : dict for Engine
            "phantoms", "slow", "seed", "verbose"

        """
        super( ).__init__( walkers, errdis, copy=copy, **kwargs )   

    def copy( self ):
        """ Return copy of this.  """
        return OrderEngine( self.walkers, self.errdis, copy=self )

    #  *********EXECUTE***************************************************
    def execute( self, kw, lowLhood, iteration=0 ):
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
