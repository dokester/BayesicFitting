import numpy as numpy
import math
import warnings

from .Engine import Engine
from .Engine import DummyPlotter
from .OrthonormalBasis import OrthonormalBasis
from .Formatter import formatter as fmt
from .Formatter import fma
from .Tools import setAttribute as setatt

__author__ = "Do Kester"
__year__ = 2025
__license__ = "GPL3"
__version__ = "3.2.5"
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
#  *    2017 - 2025 Do Kester

class ChordEngine( Engine ):
    """
    Move a a walker in a random direction.

    The ChordEngine draws a random line through the walker parameters in
    unit space, from unitMin (lowpoint) with lengths unitRange (highpoint).

    A random point on the line is selected. If the corresponding parameter
    set has a likelihood < LowLhood, it is accepted. Otherwise either the
    highpoint is reset to the random point (if randompoint > walkerpoint)
    or the lowpoint is replaced by the randompoint (if walker < random).
    Then a new random point on the line is selected, until the point is accepted.

    When the point is accepted, another random line is constructed
    through the new point and orthogonal to (all) previous ones.
    (The orthogonality is not implemented now. TBC).

    This is an independent implementation inspired by the polychord engine
    described in:
    "POLYCHORD: next-generation nested sampling",
    WJ Handley, MP Hobson and AN Lasenby.
    MNRAS (2015) Volume 453, Issue 4, p 4384–4398

    Attributes
    ----------
    reset : bool (False)
        always reset othonormal basis 
    extend : bool (False)
        perform the step-out action until logL < lowL
    plotter : 

    Attributes from Engine
    ----------------------
    walkers, errdis, slow, maxtrials, nstep, rng, verbose, report, unitRange, unitMin

    Author       Do Kester.

    """
    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, **kwargs ) :
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
        kwargs : for Engine
            "slow", "seed", "verbose"
        """
        super( ).__init__( walkers, errdis, copy=copy, **kwargs )

        self.maxtrials = 25
        self.plotter = DummyPlotter()

        ## 2 attributes to govern the behaviour
        ## extend the line on both sides until logL < lowL
        self.extend = False
        ## always reset the orthonormal basis 
        self.reset = False

    def copy( self ):
        """ Return copy of this.  """
        return ChordEngine( self.walkers, self.errdis, copy=self )

    def __setattr__( self, name, value ):
        """
        Set attributes.

        """
        setatt( self, name, value )
        if name == "plotter" :
            if isinstance( value, DummyPlotter ) :
                self.plotout = self.plotOutDummy
            else :
                self.plotout = self.plotOut

    def __str__( self ):
        return str( "ChordEngine" )


    #  *********EXECUTE***************************************************
    def execute( self, kw, lowLhood, iteration=0 ):
        """
        Execute the engine by diffusing the parameters.

        Parameters
        ----------
        kw : int
            index of walker to diffuse
        lowLhood : float
            lower limit in logLikelihood
        iteration : int
            iteration number

        Returns
        -------
        int : the number of successfull moves

        """
        self.reportCall()

        walker = self.walkers[kw].copy()
        problem = walker.problem
        fitIndex = walker.fitIndex
        np = len( fitIndex )

        param = walker.allpars
        usav = self.domain2Unit( problem, param[fitIndex], kpar=fitIndex )
        self.plotter.start( param=param )
        self.tripSq = 0.0

#        self.startJourney( usav )

        # Determine n-dim box boundaries in which the parameters are located 
        uran, umin = self.getUnitRange( problem, lowLhood, walker.nap )

#        print( "CE   ", uran )

        uran = uran[fitIndex]
        umin = umin[fitIndex]

        dur = 5 * numpy.amax( uran ) / len( self.walkers )       # extend range a bit
        uran += 2 * dur
        umin -= dur
        umax = umin + uran

        # make sure that 0 <= umin < usav < umax <= 1
        umin = numpy.where( usav < umin, 2 * usav - umin, umin )
        umax = numpy.where( usav > umax, 2 * usav - umax, umax )
        umin = numpy.maximum( umin, 0 )
        umax = numpy.minimum( umax, 1 )

        # number of cycles in ChordEngine
        nstep = self.nstep()

        onb = OrthonormalBasis( )
        # random direction in n-dim unit-parameter space
        vel = self.rng.rand( np ) - 0.5

        if self.verbose > 4 :
            print( "Chord     LogL  ", fmt( walker.logL ), " LowL  ", fmt( lowLhood), 
                    nstep, self.maxtrials )
            print( "alpar ", fma( param, linelength=200 ) )
            print( "usav  ", fma( usav ) )
            print( "umin  ", fma( umin ) )
            print( "umax  ", fma( umax ) )

        reset = True
        ptry = param.copy()
        step = 0
        st2 = 0
        for ks in range( nstep ) :

            ## orthonormalise the random vector
            vel = onb.normalise( vel, reset=reset )

            ## append travel times wrt usav (==0) to all edges umin and umax
            ## tt contains entrance times as negative values
            ## and exit times as positive values.
            tt = numpy.append( ( umin - usav ) / vel, ( umax - usav ) / vel )
            if self.verbose > 4 :
                print( "uvel  ", fma( vel ) )
                print( "ttb   ", fma( tt[:10] ) )
                print( "tte   ", fma( tt[10:] ) )

            ## find smallest entrance and exit times
            t1 = numpy.min( numpy.where( tt > 0, tt, +math.inf ) )
            t0 = numpy.max( numpy.where( tt < 0, tt, -math.inf ) )

            ## same now for the values at the edges of the unit box (0,1)
            if self.extend :
                tt = numpy.append( - usav / vel, ( 1.0 - usav ) / vel )
                if self.verbose > 4 :
                    print( "tt0   ", fma( tt[:10] ) )
                    print( "tt1   ", fma( tt[10:] ) )
                t1max = numpy.min( numpy.where( tt > 0, tt, +math.inf ) )
                t0max = numpy.max( numpy.where( tt < 0, tt, -math.inf ) )

                tt0 = self.stepOut( problem, ptry, usav, vel, t0, t0max, lowLhood, fitIndex )
                tt1 = self.stepOut( problem, ptry, usav, vel, t1, t1max, lowLhood, fitIndex )

#                print( fmt( ( t0max, tt0, t0, t1, tt1, t1max ), max=None ) )
                t0 = tt0
                t1 = tt1

            if self.verbose > 4 :
                print( step, "vel   ", fmt( vel ), fmt( tt ), fmt( t0 ), fmt( t1 ) )

            kk = 0
            while True :
                kk += 1

                # assert t0 < 0 < t1, "%f < %f < %f"%(t0,0,t1)

                if not ( t0 < 0 < t1 and math.isfinite( t0 ) and math.isfinite( t1 ) ) : 
                    break

                self.plotout( problem, usav, vel, t0, t1 )


                ## dt is timestep wrt. usav (at 0)
                dt = t0 + self.rng.rand( ) * ( t1 - t0 )

                utry = usav + vel * dt

                ptry[fitIndex] = self.unit2Domain( problem, utry, kpar=fitIndex  )

                Ltry = self.errdis.logLikelihood( problem, ptry )

                if self.verbose > 4 :
                    print( kk, fmt(t0), fmt(t1), fmt(dt), fmt(t1-t0), fmt(Ltry) )

                if Ltry >= lowLhood:
                    self.reportSuccess( )

                    step += 1

#                    self.plotter.move( param, ptry, col=0, sym=0 )
                    self.plotter.move( param, ptry, col=0 )
#                    self.tripSq += self.unitTripSquare( usav - utry )
#                    self.calcJourney( usav - utry )

                    if self.verbose == 3 :
                        cr = numpy.sqrt( numpy.sum( numpy.square( t1 - t0 ) ) )
                        st = numpy.sum( numpy.square( usav - utry ) )
                        st2 += st
                        st = numpy.sqrt( st ) 
                        print( fmt( ks ), fmt( kk ), fmt( step ), fmt( cr ),
                            fmt( st ), fmt( numpy.sqrt( st2 ) ) )

                    ## check if better than Lbest in walkers[-1]
                    # self.checkBest( problem, ptry, Ltry, fitIndex )

                    ## keep the trial parameters
                    param = ptry.copy()
                    usav = utry

                    # make sure that 0 <= umin < usav < umax <= 1
                    umin = numpy.where( usav < umin, 2 * usav - umin, umin )
                    umax = numpy.where( usav > umax, 2 * usav - umax, umax )
                    umin = numpy.maximum( umin, 0 )
                    umax = numpy.minimum( umax, 1 )

                    ## find a new random direction, orthonormal to the previous ones
                    vel = self.rng.rand( np ) - 0.5

                    ## by default dont reset.
                    reset = self.reset

                    ## update the walker
                    self.setWalker( kw, problem, ptry, Ltry, fitIndex=fitIndex )

                    break

                elif kk > self.maxtrials :
                    self.reportFailed()

                    ## find new random direction; discard the previous ie. reset the basis
                    vel = self.rng.rand( np ) - 0.5
                    reset = True

                    break

#                self.plotter.move( param, ptry, col=5, sym=4 )

                self.reportReject( )

                if dt < 0 :
                    t0 = dt
                else :
                    t1 = dt

        if step == 0 and self.verbose > 4 :
            warnings.warn( "ChordEngine: no steps found" )

        self.plotter.stop( param=param, name="ChordEngine" )

        return step * np            # nr of successfull parameter moves

    def stepOut( self, problem, ptry, usav, vel, t, tmax, lowLhood, fitIndex ) :
        """
        Check if endpoints are indeed outside the lowLhood domain.
        """

        param = self.unit2Domain( problem, usav, kpar=fitIndex )

        ## Step out
        if t == 0 :
            t = 0.01 * tmax
        while True :
#            self.reportFailed()

            utry = usav + vel * t
            ptry[fitIndex] = self.unit2Domain( problem, utry, kpar=fitIndex  )
            Ltry = self.errdis.logLikelihood( problem, ptry )
            if Ltry <= lowLhood :
                self.plotter.move( param, ptry, col=4 )
                return t
            else :
                t *= 2
                if abs( t ) >= abs( tmax ) :
                    utry = usav + vel * tmax
                    ptry[fitIndex] = self.unit2Domain( problem, utry, kpar=fitIndex  )
                    self.plotter.move( param, ptry, col=4 )
                    return tmax

        return t

    def plotOut( self, problem, usave, vel, t0, t1 ) :
        pedg0 = self.unit2Domain( problem, usave + t0 * vel )
        pedg1 = self.unit2Domain( problem, usave + t1 * vel )

        self.plotter.move( pedg0, pedg1, col=4 )
                
        return

    def plotOutDummy( self, problem, usave, vel, t0, t1 ) :
        pass
