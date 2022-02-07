import numpy as numpy
from . import Tools

from .Walker import Walker

__author__ = "Do Kester"
__year__ = 2021
__license__ = "GPL3"
__version__ = "2.7.2"
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
#  *    2017 - 2021 Do Kester

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
    SUCCESS = 0             #  succesfull move
    REJECT = 1              #  rejected move
    FAILED = 2              #  failed to move
    BEST   = 3              #  better than all
    NCALLS = 4              #  number of calls

    #  *********CONSTRUCTORS***************************************************

    def __init__( self, walkers, errdis, slow=None, copy=None, seed=4213, verbose=0 ):
        """
        Constructor.

        Parameters
        ----------
        walkers : list of Walker
            walkers to be diffused
        errdis : ErrorDistribution
            error distribution to be used
        slow : None or int > 0
            Run this engine every slow-th iteration. None for all.
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

        if copy is None :
            self.maxtrials = 5
            self.rng = numpy.random.RandomState( seed )
            self.unitRange = None
            self.unitMin = None
            self.verbose = verbose
            if slow is not None : self.slow = slow
            # self.setWalker = self.setWalkerAdd2List if usePhantoms else self.setWalkerInPlace
            # self.lastWalkerId = 0
        else :
            self.maxtrials = copy.maxtrials
            self.rng = copy.rng
            self.unitRange = copy.unitRange
            self.unitMin   = copy.unitMin
            self.verbose   = copy.verbose
            if hasattr( copy, "slow" ) : self.slow = copy.slow
            # self.setWalker = copy.setWalker
            # self.lastWalkerId = copy.lastWalkerId

    def copy( self ):
        """ Return a copy of this engine.  """
        return Engine( self.walkers, self.errdis, copy=self )

    #  *********SET & GET***************************************************
    def setWalker( self, kw, problem, allpars, logL, fitIndex=None ) :
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
        fitIndex : array_like
            (new) fitIndex
        """
        id = 0 if kw >= len( self.walkers ) else self.walkers[kw].id
        walker = Walker( id, problem, allpars, fitIndex )
        walker.logL = logL
        self.walkers.setWalker( walker, kw )

#       DONT DO THIS ANY MORE        
#        self.checkBest( problem, allpars, logL, fitIndex=fitIndex )


    def checkBest( self, problem, allpars, logL, fitIndex=None ) :
        """
        Check if Ltry better than the best at self.walkers[-1].
        If so replace.

        Parameters
        ----------
        problem : Problem
            the problem in the walker
        logL : float
            likelihood
        allpars : array_like
            parameters of problem
        fitIndex : array_like
            (new) fitIndex
        """
        if logL > self.walkers[-1].logL :
            self.setWalker( -1, problem, allpars.copy(), logL, fitIndex )
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

    def printReport( self ) :
        print( " %10d %10d %10d %10d %10d" % (self.report[0], self.report[1],
                              self.report[2], self.report[3], self.report[4] ) )

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

    def calculateUnitRange( self ):
        """
        Calculate the range of the present parameter values in unit values.

        For Dynamic models the range is calculated for those parameters present in all models;
        it is 1.0 for other parameters.

        """
        kmx = 0
        if not self.walkers[0].problem.model.isDynamic() :
            npmax = len( self.walkers[0].allpars )
        else :
            npmax = 0
            for k, walker in enumerate( self.walkers ) :
                if len( walker.allpars ) > npmax :
                    npmax = len( walker.allpars )
                    kmx = k

        minv = self.walkers[kmx].allpars.copy()
        maxv = self.walkers[kmx].allpars.copy()
        nval = numpy.zeros( npmax, dtype=int )

        for walker in self.walkers :
            fi = walker.fitIndex
#            print( "Eng   ", fi, minv, walker.allpars )
            minv[fi] = numpy.fmin( minv[fi], walker.allpars[fi] )
            maxv[fi] = numpy.fmax( maxv[fi], walker.allpars[fi] )
            nval[fi] += 1

        problem = self.walkers[kmx].problem
        fi = self.walkers[kmx].fitIndex

        maxv[fi] = self.domain2Unit( problem, maxv[fi], kpar=fi )
        minv[fi] = self.domain2Unit( problem, minv[fi], kpar=fi )

        self.unitRange = numpy.abs( maxv - minv )
        self.unitMin = numpy.fmin( minv, maxv )

#        print( "Eng1  ", self.unitRange )
        return

    def __str__( self ) :
        return str( "Engine" )

    def execute( self, kw, lowLhood ):
        """
        Execute the engine for diffusing the parameters

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

    def __init__( self, iter=0 ) :
        self.iter = iter

    def start( self, param=None ):
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

