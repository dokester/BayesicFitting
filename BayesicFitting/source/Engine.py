import numpy as numpy
from . import Tools

from .LevenbergMarquardtFitter import LevenbergMarquardtFitter
from .Walker import Walker
from .PhantomCollection import PhantomCollection
from .Formatter import formatter as fmt

__author__ = "Do Kester"
__year__ = 2024
__license__ = "GPL3"
__version__ = "3.2.1"
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
#  *    2010 - 2014 Do Kester, SRON (Java code)
#  *    2017 - 2024 Do Kester

class Engine( object ):
    """
    Engine defines common properties of all Engines.

    An Engine moves around a walker in a random way such that its likelood
    remain above the low-likelihood-limit.

    Attributes
    ----------
    walkers : WalkerList
        list of walkers to be diffused
    errdis : ErrorDistribution
        error distribution to be used
    slow : int
        If slow > 0, run this engine every slow-th iteration.
    phantoms : PhantomCollection
        Collection of valid walker positions collected during engine execution
    maxtrials : int
        maximum number of trials for various operations
    rng : numpy.random.RandomState
        random number generator
    verbose : int
        if verbose > 4 report about the engines. (mostly for debugging)

    report : list of int (read only)
        reports number of succes, accepted, rejected, failed calls. Plus the total.
    unitRange : array_like (read only)
        present max size of the parameter cloud (in unitspace: [0,1])
    unitMin : array_like (read only)
        present minimum values of the parameter cloud (in unitspace: [0,1])

    Author       Do Kester.

    """
    NSTEP  = 5              #  number of steps
    MAXTRIALS = 5           # maximum number of trials

    SUCCESS = 0             #  succesfull move
    REJECT = 1              #  rejected move
    FAILED = 2              #  failed to move
    BEST   = 3              #  better than all
    NCALLS = 4              #  number of calls

    #  *********CONSTRUCTORS***************************************************

    def __init__( self, walkers, errdis, slow=None, phantoms=None, copy=None, 
                    seed=4213, verbose=0 ):
        """
        Constructor.

        Only one PhantomCollection should be present for all Engines.

        Parameters
        ----------
        walkers : list of Walker
            walkers to be diffused
        errdis : ErrorDistribution
            error distribution to be used
        slow : None or int > 0
            Run this engine every slow-th iteration. None for all.
        phantoms : None or PhantomCollection
            Container for all valid walkers, that have been tried. But were not kept.
            To calculate the spread of the parameters vs likelihood.
        seed : int
            for random number generator
        verbose : int
            report about the engines when verbose > 4
        copy : Engine
            engine to be copied 
        """
        self.walkers = walkers
        self.errdis = errdis
        self.report = [0]*5

        self.checkBest = self.noBoost
 
        if copy is None :
            self.maxtrials = self.MAXTRIALS
            self.nstep = self.NSTEP
            self.rng = numpy.random.RandomState( seed )
            self.verbose = verbose
            if slow is not None : self.slow = slow
            if not phantoms is None :
                self.phantoms = phantoms
        else :
            self.maxtrials = copy.maxtrials
            self.nstep = copy.nstep
            self.rng = copy.rng
            self.verbose   = copy.verbose
            if hasattr( copy, "slow" ) : self.slow = copy.slow
            self.phantoms = copy.phantoms

    def copy( self ):
        """ Return a copy of this engine.  """
        return Engine( self.walkers, self.errdis, copy=self )

    def bestBoost( self, problem, myFitter=None ) :
        """
        When a logL is found better that all the rest, try to update
        it using a fitter.

        Parameters
        problem : Problem
            the problem at hand
        myFitter : None or Fitter
            None fetches LevenbergMarquardtFitter
            a (non-linear) fitter
        """
        self.checkBest = self.doBoost
        if myFitter is None :
            myFitter = LevenbergMarquardtFitter
        self.fitter = myFitter( problem.xdata, problem.model )



    #  *********SET & GET***************************************************
    def setWalker( self, kw, problem, allpars, logL, walker=None, fitIndex=None ) :
        """
        Update the walker with problem, allpars, LogL and logW.

        Parameters
        ----------
        walker : Sample
            sample to be updated

        kw : int
            index in walkerlist, of the walker to be replaced
        problem : Problem
            the problem in the walker
        allpars : array_like
            list of all parameters
        logL : float
            log Likelihood
        walker : Walker or None
            Copy this walker or create new one
        fitIndex : array_like
            (new) fitIndex
        """
        if walker is None :
            id = 0 if kw >= len( self.walkers ) else self.walkers[kw].id
            wlkr = Walker( id, problem, allpars, fitIndex )
        else :
            wlkr = walker.copy()
            wlkr.allpars = allpars    # Tools.toArray( allpars, ndim=1, dtype=float )

        wlkr.logL = logL
        self.checkBest( wlkr )

        self.walkers.setWalker( wlkr, kw )

        self.phantoms.storeItems( wlkr )

    def noBoost( self, walker ) :
        pass

    def doBoost( self, walker ) :
        """
        Check if walker is best in phantoms and try to optimize.

        Parameters
        ----------
        walker : Walker
            new walker to be checked
        """
        wlist = self.phantoms.getList( walker )

        if wlist is None or wlist[-1].logL >= walker.logL :
            return

#        print( "Best   ", fmt( walker.logL ) )
#        print( fmt( walker.allpars, max=None ) )

        problem = walker.problem
        nh = self.errdis.nphypar
        par0 = walker.allpars[:-nh]
        try :
            self.fitter.model = problem.model
            pars = self.fitter.fit( problem.ydata, par0=par0 )
        except :
            return

        if nh == 0 :
            ptry = pars
        elif walker.fitIndex[-1] == -1 :
            ptry = numpy.append( pars, self.fitter.getScale() )
        else :
            ptry = numpy.append( pars, walker.allpars[-1] )

        Ltry = self.errdis.logLikelihood( problem, ptry )

        if Ltry > walker.logL :
            walker.allpars = ptry
            walker.logL = Ltry

#        print( "Better ", fmt( walker.logL ) )
#        print( fmt( walker.allpars, max=None ) )

        self.reportBest()

######## domain <> unit ###########################################

    def domain2Unit( self, problem, dval, kpar=None ) :
        """
        Return value in [0,1] for the selected parameter.

        Parameters
        ----------
        problem : Problem
            the problem involved
        dval : float
            domain value for the selected parameter
        kpar : None or array_like
            selected parameter index, where kp is index in [parameters, hyperparams]
            None means all
        """
        np = problem.npars
        if kpar is None :
            kpar = self.makeIndex( np, dval )

        elif Tools.isInstance( kpar, int ) :
            return ( problem.domain2Unit( dval, kpar ) if kpar >= 0 else
                     self.errdis.domain2Unit( dval, kpar ) )

        uval = numpy.ndarray( len( kpar ), dtype=float )

        for i,kp in enumerate( kpar ) :
            if kp >= 0 :
                uval[i] = problem.domain2Unit( dval[i], kp )
            else :
                uval[i] = self.errdis.domain2Unit( dval[i], kp )
        return uval

    def unit2Domain( self, problem, uval, kpar=None ) :
        """
        Return domain value for the selected parameter.

        Parameters
        ----------
        problem : Problem
            the problem involved
        uval : array_like
            unit value for the selected parameter
        kpar : None or array_like
            selected parameter indices, where kp is index in [parameters, hyperparams]
            None means all.
        """
        np = problem.npars

        if kpar is None :
            kpar = self.makeIndex( np, uval )
        elif Tools.isInstance( kpar, int ) :
            return ( problem.unit2Domain( uval, kpar ) if kpar >= 0 else
                     self.errdis.unit2Domain( uval, kpar ) )

        dval = numpy.ndarray( len( kpar ), dtype=float )
        for i,kp in enumerate( kpar ) :
            if kp >= 0 :
                dval[i] = problem.unit2Domain( uval[i], kp )
            else :
                dval[i] = self.errdis.unit2Domain( uval[i], kp )
        return dval

    def startJourney( self, unitStart ) :
        """
        Calculate the starting position and reset

        Parameters
        ----------
        unitStart : array_like
            start position in npars-dimensions in unit space
        """
        self.journey = 0
        self.jstart = numpy.sqrt( numpy.sum( unitStart * unitStart ) )

    def calcJourney( self, unitDistance ) :
        """
        Calculate the distance travelled since reset

        Parameters
        ----------
        unitDistance : array_like
            step size in npars-dimensions in unit space
        """
        self.journey += numpy.sqrt( numpy.sum( unitDistance * unitDistance ) )

    def reportJourney( self ) :
        try :
            return ( self.jstart, self.journey )
        except :
            return ( 0,0 )

    def makeIndex( self, np, val ) :
        kpar = [k for k in range( np )]
        nh = len( val ) - np
        kpar += [-k for k in range( nh, 0, -1 )]
        return kpar

    def reportCall( self ):
        """ Store a call to engine  """
        self.report[self.NCALLS] += 1

    def reportSuccess( self ):
        """
        Add 1 to the number of succesfull steps: logL < lowLhood.
        """
        self.report[self.SUCCESS] += 1

    def reportReject( self ):
        """
        Add 1 to the number of rejected steps: logL > lowLhood.
        """
        self.report[self.REJECT] += 1

    def reportFailed( self ):
        """
        Add 1 to the number of failed steps: could not construct a step.
        """
        self.report[self.FAILED] += 1

    def reportBest( self ):
        """
        Add 1 to the number of best likelihoods found upto now.
        """
        self.report[self.BEST] += 1

    def printReport( self, best=False ) :
        if best :
            print( " %10d %10d %10d %10d %10d" % (self.report[0], self.report[1],
                              self.report[2], self.report[3], self.report[4] ) )
        else :
            print( " %10d %10d %10d %10d" % (self.report[0], self.report[1],
                              self.report[2], self.report[4] ) )

    def successRate( self ) :
        """
        Return percentage of success.
        """
        if not hasattr( self, "save" ) :
            self.save = [0, 0]

        srate = ( 100 * ( self.report[0] - self.save[0] ) / 
                  ( self.report[0] + self.report[1] + self.report[2] - self.save[1] ) )
        self.save = [self.report[0], ( self.report[0] + self.report[1] + self.report[2] )]
        return srate


    def getUnitMinmax( self, problem, lowLhood ) :
        """
        Calculate unit minimum and maximum from the Phantoms

        Parameters
        ----------
        problem : Problem
            To extract the unit range for
        lowLhood : float
            low likelihood boundary
        """
        npars = problem.npars
        pamin, pamax = self.phantoms.getParamMinmax( lowLhood, np=problem.npars )

        npars += self.errdis.nphypar
        umax = ( numpy.ones( npars, dtype=float )  if pamax is None
                else self.domain2Unit( problem, pamax ) )
        umin = ( numpy.zeros( npars, dtype=float )  if pamin is None
                else self.domain2Unit( problem, pamin ) )
        umin = numpy.fmin( umin, umax )

        return ( umin, umax )

    def getUnitRange( self, problem, lowLhood ) :
        """
        Calculate unit range and minimum from PhantomCollection

        Parameters
        ----------
        problem : Problem
            To extract the unit range for
        lowLhood : float
            low likelihood boundary
        """
        umin, umax = self.getUnitMinmax( problem, lowLhood )
 
        uran = numpy.abs( umax - umin )
                
        return ( uran, umin )

    def __str__( self ) :
        return str( "Engine" )

    def execute( self, kw, lowLhood ):
        """
        Execute the engine for difusing the parameters

        Parameters
        ----------
        kw : walker-id
            walker to diffuse
        lowLhood : float
            low limit on the loglikelihood

        Returns
        -------
        int : number of succesfull moves

        """
        pass


class DummyPlotter( object ) :

    def __init__( self, iter=1 ) :
        self.iter = iter

    def start( self, param=None, ulim=None ):
        """ start the plot. """
        pass

    def point( self, param, col=None, sym=0 ):
        """
        Place a point at position param using color col and symbol sym.
        """
        pass

    def move( self, param, ptry, col=None, sym=None ):
        """
        Move parameters at position param to ptry using color col.
        """
        pass

    def stop( self, param=None, name=None ):
        """ Stop (show) the plot. """
        pass

