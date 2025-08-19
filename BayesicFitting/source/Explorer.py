import numpy as numpy
from threading import Thread

from .Engine import Engine
from .ModelDistribution import ModelDistribution
from .Formatter import formatter as fmt
from . import Tools

__author__ = "Do Kester"
__year__ = 2025
__license__ = "GPL3"
__version__ = "3.2.4"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Perpetual Beta"

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
#  *    2017 - 2025 Do Kester


threadErrors = []

class Explorer( object ):
    """
    Explorer is a helper class of NestedSampler, which contains and runs the
    diffusion engines.

    It uses Threads to parallelise the diffusion engines.

    Attributes
    ----------
    walkers : WalkerList
        walkers to be explored
    engines : [engine]
        list of engines to be used
    errdis : ErrorDistribution
        to be used
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
    iteration : int
        counting explorer calls

    Author       Do Kester.

    """
    TWOP32 = 2 ** 32

    def __init__( self, ns, threads=False ):
        """
        Construct Explorer from a NestedSampler object.

        Parameters
        ----------
        ns : NestedSampler
            the calling NestedSampler. It provides the attributes.

        """
        self.walkers = ns.walkers
        self.engines = ns.engines
        self.errdis = ns.distribution
        self.rng = ns.rng
        self.rate = ns.rate
        self.maxtrials = ns.maxtrials
        self.verbose = ns.verbose
        self.threads = threads
        self.usePhantoms = ns.usePhantoms

        self.unitSize = ns.unitDomain

        self.selectEngines = self.allEngines    ## default: always use all engines
        for eng in self.engines :
            if hasattr( eng, "slow" ) :
                self.selectEngines = self.selEngines    ## use selection
                break

    def explore( self, worst, lowLhood, iteration ):
        """
        Explore the likelihood function, using threads.

        Parameters
        ----------
        worst : [int]
            list of walkers to be explored/updated
        lowLhood : float
            level of the low likelihood

        """
        self.iteration = iteration
        engines = self.selectEngines( iteration )

        if not self.threads :
            for kw in worst :
                self.exploreWalker( kw, lowLhood, engines, self.rng )

            return

        ## We have Threads
        explorerThreads = []
        self.lowLhood = lowLhood

        nrep = Engine.NCALLS
        for kw in worst :
            seed = self.rng.randint( self.TWOP32 )
            exThread = ExplorerThread( "explorer_%d"%kw, kw, self, engines, seed )
            exThread.start( )
            explorerThreads += [exThread]

        for thread in explorerThreads :
            thread.join( )

            for k,engine in enumerate( engines ) :
                nc = 0
                for i in range( nrep ) :
                    nc += thread.engines[k].report[i]
                    engine.report[i] += thread.engines[k].report[i]
                engine.report[nrep] += nc

        if len( threadErrors ) > 0: #check if there are any errors
            for e in threadErrors:
                print( e )
            raise Exception( "Thread Error" )

    def exploreWalker( self, kw, lowLhood, engines, rng ):
        """
        Move the walker around until it is randomly distributed over the prior and
        higher in logL then lowLhood

        Parameters
        ----------
        kw : int
            index in walkerlist, of the walker to be explored
        lowLhood : float
            minimum value for the log likelihood
        engine : list of Engine
            to be used
        rng : RandomState
            random number generator
        """
        if self.verbose >= 4 :
            print( "-------- Start exploreWalker ---------------------------------" )
#            self.checkWalkers()

        walker = self.walkers[kw]
        oldlogL = walker.logL

        self.errdis.lowLhood = lowLhood

        npars = len( walker.allpars ) 
        maxmoves = npars / self.rate
        maxtrials = self.maxtrials / self.rate
#        minTripSq = self.unitSize()
#        minTripSq *= len( walker.fitIndex ) ##  * minTripSq

        moves = 0
        trials = 0
#        tripSq = 0

        while moves < maxmoves and trials < maxtrials :

            for engine in rng.permutation( engines ) :
                mv = engine.execute( kw, lowLhood, iteration=self.iteration )
                moves += mv
#                tripSq += engine.tripSq

#                if isinstance( self.errdis, ModelDistribution ) :
#                    print( "%3d  %-15.15s %3d %3d %3d %3d %3d" % 
#                           ( kw, engine, mv, moves, maxmoves, trials, maxtrials ) )

                if self.verbose >= 4 and mv > 0 :
                    wlkr = self.walkers[kw]
                    print( "%4d %-15.15s %4d %10.3f %10.3f ==> %3d  %10.3f"%
                            ( trials, engine, kw, lowLhood, oldlogL, moves,
                                wlkr.logL ) )
                    print( "IN       ", fmt( walker.allpars, max=None, linelength=200 ), len( walker.allpars ) )
                    print( "OUT      ", fmt( wlkr.allpars, max=None, linelength=200 ), len( wlkr.allpars ) )

                    if len( wlkr.allpars ) < len( wlkr.fitIndex ) :
                        raise ValueError( "Walker parameter %d fitIndex %d" %
                            ( len( wlkr.allpars ), len( wlkr.fitIndex ) ) )
                    oldlogL = wlkr.logL

                    ## check walker for consistency
                    walker.check( self.errdis )

            trials += 1

#        if self.iteration % 100 == -1 :
#            ur2 = engine.unitTripSquare( engine.urange[walker.fitIndex] )
#            print( "Remaining  %#10.3g  %#10.3g %#10.3g   trip  %#10.3g  ratio   %#10.3g %#10.3g" % 
#                ( minTripSq, numpy.power( 0.99, self.iteration ) * 5, ur2, tripSq, tripSq/minTripSq, tripSq/ur2 ) )


        if moves == 0 :
            self.walkers[kw].check( self.errdis )

        if self.walkers[kw].logL < lowLhood :
            raise Exception( "%10.3f < %10.3f" % ( self.walkers[kw].logL, lowLhood )  )


        return

    def selEngines( self, iteration ) :
        """
        Select engines with slowly changing parameters once per so many iterations.

        Parameter
        ---------
        iteration : int
            iteration number
        """
        engines = []
        for eng in self.engines :
            if not hasattr( eng, "slow" ) or ( iteration % eng.slow ) == 0 :
                engines += [eng]

        return engines

    def allEngines( self, iteration ) :
        """
        Always use all engines.

        Parameters
        ----------
        iteration : int
            iteration number
        """
        return self.engines

    def checkWalkers( self ) :
        """ Perform sanity check on all walkers. """
        for w in self.walkers :
            w.check( self.errdis )



class ExplorerThread( Thread ):
    """
    One thread for the Explorer. It updates one walker.

    Attributes
    ----------
    id : int
        identity for thread
    walkers : WalkerList
        list of walkers
    rng : numpy.random.RandomState
        random number generator
    engines : [Engine]
        copy of the list of Engines of Explorer
    """

    global threadErrors

    def __init__( self, name, id, explorer, engines, seed ):
        super( ExplorerThread, self ).__init__( name=name )
        self.id = id
        self.explorer = explorer
        self.engines = [eng.copy() for eng in engines]
        self.rng = numpy.random.RandomState( seed )


    def run( self ):
        try :
            self.explorer.exploreWalker( self.id, self.explorer.lowLhood,
                                         self.engines, self.rng )
        except Exception as e :
            threadErrors.append( [repr(e) + " occurred in walker %d" % self.id] )
            raise



