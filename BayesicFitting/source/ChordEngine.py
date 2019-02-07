import numpy as numpy
import math
import warnings
from . import Tools

from .Engine import Engine
from .Engine import DummyPlotter
from .OrthonormalBasis import OrthonormalBasis
from .Formatter import formatter as fmt

__author__ = "Do Kester"
__year__ = 2018
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
#  *    2010 - 2014 Do Kester, SRON (Java code)
#  *    2017 - 2018 Do Kester

class ChordEngine( Engine ):
    """
    Move a a walker in a random direction.

    The ChordEngine draws a random line through the walker parameters in
    unit space, from unitMin (lowpoint) with lengths unitRange (highpoint).
    A random point on the line is selected. If the corresponding parameter
    set has a likelihood < LowLhood, it is accepted. Otherwise either the
    highpoint is reset to the random point (if randompoint > walkerpoint)
    or the lowpoint is increased to randompoint (if walker < random)
    then continue.
    when the point is accepted select another random line orthogonal to
    the previous ones.

    This is an independent implementation inspired by the polychord engine
    described in:
    "POLYCHORD: next-generation nested sampling",
    WJ Handley, MP Hobson and AN Lasenby.
    MNRAS (2015) Volume 453, Issue 4, p 4384–4398

    Attributes
    ----------
    nstep : int
        average number of orthogonal steps
    debug : bool
        perform the step-out action too

    Attributes from Engine
    ----------------------
    walkers, errdis, maxtrials, rng, verbose, report, unitRange, unitMin

    Author       Do Kester.

    """
    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, seed=4213, debug=False, verbose=0 ):
        """
        Constructor.

        Parameters
        ----------
        walkers : WalkerList
            walkers to be diffused
        errdis : ErrorDistribution
            error distribution to be used
        copy : ChordEngine
            to be copied
        seed : int
            for rng
        verbose : int
            <= 4 : silent
            > 4  : info about engine execution

        """
        super( ).__init__( walkers, errdis, copy=copy, seed=seed, verbose=verbose )

        self.nstep = 5
        self.maxtrials = 25
        self.plotter = DummyPlotter()
        self.debug = False

    def copy( self ):
        """ Return copy of this.  """
        return ChordEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "ChordEngine" )


    #  *********EXECUTE***************************************************
    def execute( self, walker, lowLhood ):
        """
        Execute the engine by diffusing the parameters.

        Parameters
        ----------
        walker : Walker
            walker to diffuse
        lowLhood : float
            lower limit in logLikelihood

        Returns
        -------
        int : the number of successfull moves

        """
        self.reportCall()

        walker = walker.copy()
        problem = walker.problem
        fitIndex = walker.fitIndex
        np = len( fitIndex )

        self.plotter.start()

#        self.calculateUnitRange()

        uran = self.unitRange[fitIndex]
        umin = self.unitMin[fitIndex]

        dur = 2 * numpy.max( uran ) / len( self.walkers )      # extend range a bit
        uran += 2 * dur
        umin = self.unitMin[fitIndex] - dur

        umin = numpy.maximum( umin, 0 )
        umax = numpy.minimum( umin + uran, 1 )


        param = walker.allpars
        usav = self.domain2Unit( problem, param[fitIndex], kpar=fitIndex )

        nstep = int( self.nstep * ( 1 + self.rng.rand() ) )

        onb = OrthonormalBasis( )
        vel = self.rng.rand( np ) - 0.5

        if self.verbose > 4 :
            print( "++++++++++++++++++++++++++++++++++++++++++" )
            print( walker.id, nstep, fmt(lowLhood), fmt( param ) )
            print( "umin  ", fmt( umin ) )
            print( "umax  ", fmt( umax ) )
#            print( "umean ", fmt( umn ) )
            print( "usav  ", fmt( usav ) )

        self.plotter.point( param, col=0, sym=2 )


        reset = True
        ptry = param.copy()
        step = 0
        for ks in range( nstep ) :

            ## orthonormalise the random vector
            vel = onb.normalise( vel, reset=reset )

            if self.verbose > 4 :
                print( ks, step, "vel   ", fmt( vel ) )

            ## append travel times wrt usav (==0) to all edges umin and umax
            ## tt contains entrance times as negative values
            ## and exit times as positive values.
            tt = numpy.append( ( umin - usav ) / vel, ( umax - usav ) / vel )

            ## find smallest entrance and exit times
            t1 = numpy.min( numpy.where( tt > 0, tt, +math.inf ) )
            t0 = numpy.max( numpy.where( tt < 0, tt, -math.inf ) )

            ## same now for the values at the edges of the unit box (0,1)
            if self.debug :
                tt = numpy.append( - usav / vel, ( 1.0 - usav ) / vel )
                t1max = numpy.min( numpy.where( tt > 0, tt, +math.inf ) )
                t0max = numpy.max( numpy.where( tt < 0, tt, -math.inf ) )

                t0 = self.stepOut( problem, ptry, usav, vel, t0, t0max, lowLhood, fitIndex )
                t1 = self.stepOut( problem, ptry, usav, vel, t1, t1max, lowLhood, fitIndex )

            kk = 0
            while True :
                kk += 1

                assert t0 < 0 < t1, "%f < %f < %f"%(t0,0,t1)
                ## dt is timestep wrt. usav (at 0)
                dt = t0 + self.rng.rand( 1 ) * ( t1 - t0 )
                utry = usav + vel * dt

                ptry[fitIndex] = self.unit2Domain( problem, utry, kpar=fitIndex  )

                Ltry = self.errdis.logLikelihood( problem, ptry )

                if self.verbose > 4 :
                    print( kk, fmt(t0), fmt(t1), fmt(dt), fmt(t1-t0), fmt(Ltry) )


                if Ltry >= lowLhood:
                    self.reportSuccess( )
                    step += 1

                    self.plotter.move( param, ptry, col=0, sym=0 )

                    ## check if better than Lbest in walkers[-1]
                    self.checkBest( problem, ptry, Ltry, fitIndex )

                    ## keep the trial parameters
                    param = ptry.copy()
                    usav = self.domain2Unit( problem, param[fitIndex], kpar=fitIndex )

                    ## find a new random direction, orthonormal to the previous ones
                    vel = self.rng.rand( np ) - 0.5
                    reset = False

                    break

                elif kk > self.maxtrials :
                    self.reportFailed()

                    ## find new random direction; discard the previous ie. reset the basis
                    vel = self.rng.rand( np ) - 0.5
                    reset = True

                    break

                self.plotter.move( param, ptry, col=5, sym=4 )
                self.reportReject( )

                if dt < 0 :
                    t0 = dt
                else :
                    t1 = dt

        if step > 0 :
            ## update the walker
            self.setWalker( walker, problem, ptry, Ltry, fitIndex=fitIndex )
            step = np
        elif self.verbose > 4 :
            warnings.warn( "ChordEngine: no steps found" )

        self.plotter.stop()

        return step


    def stepOut( self, problem, ptry, usav, vel, t, tmax, lowLhood, fitIndex ) :
        ## Step out
        if t == 0 :
            t = 0.01 * tmax
        while True :
            if abs( t ) >= abs( tmax ) :
                return tmax
            self.reportFailed()

            utry = usav + vel * t
            ptry[fitIndex] = self.unit2Domain( problem, utry, kpar=fitIndex  )
#            print( t, tmax, utry, ptry )
            Ltry = self.errdis.logLikelihood( problem, ptry )
            if Ltry <= lowLhood :
                return t
            else :
                t *= 2
        return t




