import numpy as numpy
from astropy import units
import math
import warnings
from . import Tools
from .Formatter import formatter as fmt
from .Formatter import fma

from .Engine import Engine
from .Engine import DummyPlotter

import matplotlib.pyplot as plt

__author__ = "Do Kester"
__year__ = 2023
__license__ = "GPL3"
__version__ = "3.2.0"
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
#  *    2017 - 2023 Do Kester

class GalileanEngine( Engine ):
    """
    Move all parameters in forward steps, with optional mirroring on the edge.

    Move the parameters in a random direction for N iterations; mirror the direction
    on the gradient of the logLikelihood when the parameters enter the zone of logLlow.

    Attributes
    ----------
    size : 0.5
        of the step

    Attributes from Engine
    ----------------------
    walkers, errdis, maxtrials, nstep, slow, rng, report, phantoms, verbose

    Author       Do Kester.

    """

    SIZE = 0.5

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, **kwargs ):
        """
        Default Constructor.

        Parameters
        ----------
        walkers : WalkerList
            walkers to be diffused
        errdis : ErrorDistribution
            error distribution to be used
        copy : GalileanEngine
            to be copied
        kwargs : for Engine
            "phantoms", "slow", "seed", "verbose"

        """
        super( ).__init__( walkers, errdis, copy=copy, **kwargs )

        self.size = self.SIZE

        self.plotter = DummyPlotter( )

    def copy( self ):
        """ Return copy of this.  """
        engine = GalileanEngine( self.walkers, self.errdis, copy=self )
        engine.nstep = self.nstep

        return engine

    def __str__( self ):
        """ Return the name of this engine.  """
        return str( "GalileanEngine" )

    #  *********EXECUTE***************************************************
    def execute( self, kw, lowLhood, append=False, iteration=0 ):
        """
        Execute the engine by diffusing the parameters.

        Parameters
        ----------
        kw : int
            index in walkerlist, of the walker
        lowLhood : float
            lower limit in logLikelihood
        append : bool
            set walker in place of append

        Returns
        -------
        int : the number of successfull moves

        """
        self.reportCall()

        walker = self.walkers[kw].copy()
        problem = walker.problem
        Lhood = walker.logL
        allpars = walker.allpars
        fitIndex = walker.fitIndex

        inside = 0
        Ltry = 0
        size = self.size

        self.plotter.start( param=allpars )
        um = UnitMovements( walker, self, size, lowLhood )

#        nstep = int( self.nstep * ( 1 + self.rng.rand() ) )
        nstep = 2 + int( self.nstep * ( 1 + self.rng.rand() ) )

        maxtrial = self.maxtrials

        ptry = allpars.copy()
        if self.verbose > 4 :
            print( "Galilean   LogL  ", fmt( Lhood ), " LowL  ", fmt( lowLhood), nstep, maxtrial, size )
            print( "alpar ", fma( ptry, linelength=200 ) )
            fip = allpars[fitIndex]
            print( "uap   ", fma( self.domain2Unit( problem, fip, fitIndex ), linelength=200) )
            print( "unitr ", fma( um.upran, linelength=200 ) )
            print( '--------------------' )
        step = 0
        trial = 0

        while True:
            trial += 1
            f = -1

            um.setParameters( problem, allpars )        # restart at safe location

            if inside == 0 :                            # safely inside lowLhood area
                ptry[fitIndex] = um.trialStep( 1.0, size )

            elif inside == 1 :                          # first time outside -> mirror

                ptry[fitIndex] = um.trialStep( 0.5, size )    # params at mid point
                Lmid = self.errdis.logLikelihood( problem, ptry )

                f = self.quadinterpol( Lhood, Lmid, Ltry, lowLhood )

                pedge = allpars.copy()
                pedge[fitIndex] = um.trialStep( f, size )      # params at edge  

                if self.verbose > 4 :
                    Ledge = self.errdis.logLikelihood( problem, pedge )
                    print( "Lmid  ", fmt( iteration ), fmt( Lmid ), fmt( f ), fmt( Ltry ),
                            fmt( lowLhood ), fmt( Ledge ), fmt( Lhood ) )

                dLdp = self.errdis.partialLogL( problem, pedge, fitIndex )
                self.plotter.move( allpars, pedge, col=1, sym=4 )
                um.acceptTrial()

                um.mirrorOnLowL( dLdp )

                ptry[fitIndex] = um.trialStep( 1 - f, size )

                self.plotter.move( pedge, ptry, col=2 )
            else:                                       # mirroring failed; do reverse
                size *= 0.7
                um.reverseVelocity( size )
                ptry[fitIndex] = um.trialStep( 1.0, size )

                self.plotter.move( allpars, ptry, col=3, sym=0 )

            Ltry = self.errdis.logLikelihood( problem, ptry )


            if Ltry >= lowLhood:
                self.plotter.move( allpars, ptry, col=0, sym=0 )

                um.acceptTrial()

                allpars = ptry.copy( )
                Lhood = Ltry
                self.reportSuccess( )
                inside = 0
                step += 1
                trial = 0
                size = self.size

                ## update the walker
                update = len( self.walkers ) if append else kw
                self.setWalker( update, problem, allpars, Lhood, fitIndex=fitIndex )

            else:
                inside += 1
                if inside == 1:
                    self.plotter.move( allpars, ptry, col=5, sym=4 )
                    self.reportReject( )
                else:
                    self.plotter.move( allpars, ptry, col=4 )
                    self.reportFailed( )

            if self.verbose > 4 :
                print( "upar  ", fma( um.upar, linelength=200 ) )
                print( "uvel  ", fma( um.uvel, linelength=200 ) )
                print( "ptry  ", fma( ptry, linelength=200 ) )
                print( "Ltry  ", fmt( Ltry ), inside, step, trial, self.plotter.iter-1, 
                        fmt( size ) )
                print( '--------------------' )


            if not ( step < nstep and trial < maxtrial ):
                break


        # dynamically adjust step size
        if step == 0 :
            self.size = max( 0.9 * self.size, 1e-6 )
            if self.verbose > 4 :
                warnings.warn( "GalileanEngine: no steps found" )
        else :
            self.size = min( self.SIZE, self.size * 1.1 )

        self.plotter.stop( param=allpars, name="GalileanEngine" )

        return step * len( fitIndex )           # nr of successfull steps

    def quadinterpol( self, L0, Lm, L1, lowL ) :
        """
        Quadratic interpolation of points (x,y)
        x = [0.0, 0.5, 1.0]
        y = [L0, Lm, L1]  where L0 > Lm > L1    
        interpolation at y = lowL.

        Returns
        -------
        xvalue : float
            largest of the two inside [0,1]
        """ 
        c = L0
        b = 4 * Lm - L1 - 3 * L0
        a = 2 * L0 - 4 * Lm  + 2 * L1

        if a == 0 :
            return 1 if b == 0 else ( lowL - c ) / b

        det = b * b - 4 * a * ( c - lowL )
        det = 0 if det < 0 else math.sqrt( det )

        x1 = ( - b - det ) / ( 2 * a )
        x2 = ( - b + det ) / ( 2 * a )

        if a < 0 :      # top parabola: return largest
            return x1 if x1 > x2 else x2
        else :          # valley parabala : return smallest
            return x1 if x1 < x2 else x2



class UnitMovements( object ):
    """
    Define all parameter movements in unitspace.



    """
    def __init__( self, walker, engine, size, lowLhood ):
#        print( "GEUM  ", engine.unitRange )
        self.problem = walker.problem
        self.fitIndex = walker.fitIndex

        self.np = len( self.fitIndex )
        self.engine = engine
        self.setParameters( self.problem, walker.allpars )


        nap = len( walker.allpars )
        uran, umin = engine.getUnitRange( self.problem, lowLhood, npars=nap )
        self.upran = uran[self.fitIndex]
        self.uvel = self.setVelocity( size )

    def uniform( self ) :
        """
        Return random step between [0.5,0.5]
        """
        return self.engine.rng.rand( self.np ) - 0.5

    def setParameters( self, problem, allpars ):
        """
        Set unit values for the applicable parameters
        """
        fip = allpars[self.fitIndex]
        self.upar = self.engine.domain2Unit( problem, fip, kpar=self.fitIndex )

    def trialStep( self, f, size ):
        """
        Return a new trial parameter set.
        """

        uv = self.uvel
        pv = self.upar + uv * f

        # check if outside [0,1]
        pv, uv = numpy.where( pv <= 0, ( -pv, -uv ), ( pv, uv ) )
        self.ptry, self.vtry = numpy.where( pv >= 1, ( 2 - pv, -uv ), ( pv, uv ) )

        # When on edge, start a new direction with the same signs
        if not all( self.vtry == self.uvel ) :
            uv = self.setVelocity( size ) 
#            vt = self.vtry.copy()
            self.vtry = numpy.copysign( uv, self.vtry )

#            print( "newV  ", fmt( self.uvel ), fmt( vt ), fmt( uv ), fmt( self.vtry ) )

        return self.engine.unit2Domain( self.problem, self.ptry, kpar=self.fitIndex )

    def acceptTrial( self ) :
        self.upar = self.ptry
        self.uvel = self.vtry

    def mirrorOnLowL( self, dLdp ):
        """
        Mirror the velocity on the low likelihood border.
        """
        inprod = numpy.sum( dLdp * self.uvel )
        sumsq  = numpy.sum( dLdp * dLdp )
        if sumsq == 0 : return

        self.uvel -= 2 * dLdp * inprod / sumsq


    def setVelocity( self, size ):
        """
        Set a (random) unit velocity.
        """
        return self.uniform() * self.upran * size

    def reverseVelocity( self, size ):
        """
        Reverse the unit velocity when mirroring fails.
        Add small perturbation.
        """

        upv = self.uvel                 # keep original velocity
        self.setVelocity( size )        # get a new one to perturb
        nm = len( self.engine.walkers )
        self.uvel = size * ( self.np * self.uvel - nm * upv ) / ( nm + self.np )

        """
        ff = 0.3
        self.uvel = self.setVelocity( ff )      # pertubance of 10 percent
        self.uvel -= self.vold * ( 1 - ff )     # reverse previous (before mirror) direction
        self.uvel *= size
        """
