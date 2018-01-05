import numpy as numpy
from threading import Thread

__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2017        Do Kester

class Explorer( object ):
    """
    Explorer is a helper class of NestedSampler, which contains and runs the
    diffusion engines.

    It uses Threads to parallelise the diffusion engines.

    Attributes
    ----------
    walkers : SampleList
        samples to be explored
    engines : [engine]
        list of engines to be used
    rng : numpy.random.RandomState
        random number generator
    rate : float (1.0)
        governs processing speed (vs precision)
    maxtrials : int (5)
        number of trials
    verbose : int (0)
        level of blabbering
    lowLhood : float
        present low likelihood level
    generation : int
        counting explorer calls

    Author       Do Kester.

    """

    def __init__( self, ns ):
        """
        Construct Explorer from a NestedSampler object.
        Parameters
        ----------
        ns : NestedSampler
            the calling NestedSampler

        """
        self.walkers = ns.walkers
        self.engines = ns.engines
        self.rng = self.engines[0].rng
        self.rate = ns.rate
        self.maxtrials = ns.maxtrials
        self.verbose = ns.verbose
        self.engines[0].calculateUnitRange( )

    def explore( self, worst, lowLhood, fitindex ):
        """
        Explore the likelihood function, using threads.

        Parameters
        ----------
        worst : [int]
            list of samples to be explored/updated
        lowLhood : float
            level of the low likelihood
        fitindex : list of int
            list of parameter indices to fit

        """
        self.lowLhood = lowLhood
        explorerThreads = []
        for kw in worst :
            exThread = ExplorerThread( "explorer_%d"%kw, kw, self, fitindex )
            exThread.start( )
            explorerThreads += [exThread]

        for thread in explorerThreads :
            thread.join( )
            for k,e in enumerate( self.engines ) :
                nc = 0
                for i in range( 3 ) :
                    nc += thread.engines[k].report[i]
                    e.report[i] += thread.engines[k].report[i]
                e.report[3] += nc

        # recalculate  TBC
        self.engines[0].calculateUnitRange( )

class ExplorerThread( Thread ):
    """
    One thread for the Explorer. It updates one walker.

    Attributes
    ----------
    id : int
        identity for thread
    walkers : SampleList
        list of walkers
    rng : numpy.random.RandomState
        random number generator
    engines : [Engine]
        copy of the list of Engines of Explorer
    errdis : ErrorDistribution
        to be used (=self.engines[0].errdis)
    """

    def __init__( self, name, id, explorer, fitindex ):
        super( ExplorerThread, self ).__init__( name=name )
        self.id = id
        self.explorer = explorer
        self.fitindex = fitindex
        self.engines = [eng.copy() for eng in explorer.engines]
        seed = explorer.rng.randint( 100000 )
        self.rng = numpy.random.RandomState( seed )
        self.errdis = self.engines[0].errdis
        self.verbose = explorer.verbose

    def run( self ):
        self.explore( self.id, self.fitindex )

    def explore( self, walkerId, fitindex ):
        walker = self.explorer.walkers[walkerId]
        oldlogL = walker.logL

        maxmoves = len( fitindex ) / self.explorer.rate
        maxtrials = self.explorer.maxtrials / self.explorer.rate

        lowLhood = self.explorer.lowLhood
        moves = 0
        trials = 0
        while moves < maxmoves and trials < maxtrials :
            i = 0
            for engine in self.rng.permutation( self.engines ) :

                moves += engine.execute( walker, lowLhood, fitindex )

                if self.verbose >= 4:
                    print( "%4d -%12.12s %4d %8.1f %8.1f ==> %3d  %8.1f"%
                            ( i, engine, walkerId, lowLhood, oldlogL, moves, walker.logL ) )
                    i += 1
                    oldlogL = walker.logL

            trials += 1

        if moves == 0 :
            self.logLcheck( walker )

        return

    def logLcheck( self, walker ) :
        wlogL = self.errdis.logLikelihood( walker.model, walker.parlist )
        if wlogL != walker.logL :
            raise ValueError( "Inconsistency between stored logL %f and calculated logL %f" %
                                ( walker.logL, wlogL ) )

