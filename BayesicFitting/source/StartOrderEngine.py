import numpy as numpy
from astropy import units
import math
from . import Tools

from .OrderEngine import OrderEngine

__author__ = "Do Kester"
__year__ = 2022
__license__ = "GPL3"
__version__ = "3.0.0"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Alpha"

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
#  *    2017 - 2022 Do Kester

class StartOrderEngine( OrderEngine ):
    """
    StartEngine generates a parameter list in random order.

    It is used to initialize the set of trial samples.

    Author       Do Kester.

    """
    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, seed=4213, verbose=0 ):
        """
        Constructor.
        Parameters
        ----------
        copy : StartEngine
            engine to be copied

        """
        super( ).__init__( walkers, errdis, copy=copy, seed=seed, verbose=verbose )

    def copy( self ):
        """ Return copy of this.  """
        return StartOrderEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "StartOrderEngine" )

    #  *********EXECUTE***************************************************
    def execute( self, kw, lowLhood, fitIndex=None ):
        """
        Execute the engine by a random selection of the parameters.

        Parameters
        ----------
        kw : id
            id of waker to diffuse
        lowLhood : float
            lower limit in logLikelihood
        fitIndex : array_like
            list of parameter indices (not active)
        Returns
        -------
        int : the number of successfull moves

        """
        walker = self.walkers[kw]

        problem = walker.problem
#        print( walker.allpars )
        par = numpy.random.permutation( walker.allpars )
#        print( par )

        logL = self.errdis.logLikelihood( problem, par )
        self.setWalker( walker.id, problem, par, logL )

        return len( par )


