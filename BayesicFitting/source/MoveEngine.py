import numpy as numpy
import math
from . import Tools
from .Formatter import formatter as fmt

from .OrderEngine import OrderEngine

__author__ = "Do Kester"
__year__ = 2025
__license__ = "GPL3"
__version__ = "3.2.4"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Alpha"

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

class MoveEngine( OrderEngine ):
    """
    The MoveEngine tries to move a selection of the parameters to another spot.

    Input order : [0,1,2,3,4,5,6,7,8,9]

    output order: [4,5,6,7,1,2,3,8,9,0]


    It belongs to the class of generalized travelling salesman problems
    where the parameters of the problem is an ordered list.

    The walker is kept when the logLikelihood > lowLhood

    Attributes from Engine
    ----------------------
    walkers, errdis, maxtrials, nstep, slow, rng, report, phantoms, verbose

    Author       Do Kester.

    """
    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, **kwargs ) :
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
        return MoveEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "MoveEngine" )

    #  *********EXECUTE***************************************************
    def executeOnce( self, kw, lowLhood ) :

        walker = self.walkers[kw]
        problem = walker.problem
        param = walker.allpars

        src = self.rng.randint( problem.npars )
        des = src
        while des == src :
            des = self.rng.randint( problem.npars )

        mx = ( des - src ) if src < des else ( problem.npars - src )
        t = min( self.rng.geometric( 0.2 ), mx )
        while t > 0 :
            if src < des :
                kln = src + t
                ptry = param[kln:des]
                ptry = numpy.append( ptry, param[src:kln] )
                ptry = numpy.append( ptry, param[des:] )
                ptry = numpy.append( ptry, param[:src] )
            else :
                kln = src + t
                ptry = param[kln:]
                ptry = numpy.append( ptry, param[:des] )
                ptry = numpy.append( ptry, param[src:kln] )
                ptry = numpy.append( ptry, param[des:src] )

            Ltry = self.errdis.logLikelihood( problem, ptry )

            if self.verbose > 4 :
                print( "Order    ", src, kln, t, des, fmt( lowLhood ), fmt( Ltry ) )
                print( fmt( param, max=None, format='%3d' ) )
                print( fmt( ptry, max=None, format='%3d' ) )

            if Ltry >= lowLhood:
                self.reportSuccess( )
                self.setWalker( walker.id, problem, ptry, Ltry )

                ## check if better than Lbest in walkers[-1]
                ## self.checkBest( problem, ptry, Ltry )

                return t

            t = self.rng.randint( t )
            self.reportFailed( )


        self.reportReject()

        return t                        # nr of reordered parameters


