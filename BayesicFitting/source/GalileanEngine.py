import numpy as numpy
from astropy import units
import math
import warnings
from . import Tools
from .Formatter import formatter as fmt
from .Formatter import fma

from .Engine import Engine
from .Engine import DummyPlotter

__author__ = "Do Kester"
__year__ = 2021
__license__ = "GPL3"
__version__ = "2.8.0"
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
#  *    2017 - 2021 Do Kester

class GalileanEngine( Engine ):
    """
    Move all parameters in forward steps, with optional mirroring on the edge.

    Move the parameters in a random direction for N iterations; mirror the direction
    on the gradient of the logLikelihood when the parameters enter the zone of logLlow.

    Attributes
    ----------
    nstep : int (5)
        average number of steps to be taken

    Attributes from Engine
    ----------------------
    walkers, errdis, maxtrials, slow, rng, report, unitRange, unitMin, verbose

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
            "slow", "seed", "verbose"

        """
        super( ).__init__( walkers, errdis, copy=copy, **kwargs )

        self.nstep = 5
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

        npout = 0
        inside = 0
        Ltry = 0
        size = self.size

        self.plotter.start( param=allpars )
        um = UnitMovements( walker, self, size )

        nstep = int( self.nstep * ( 1 + self.rng.rand() ) )
#        maxtrial = self.maxtrials * nstep
        maxtrial = self.maxtrials

        ptry = allpars.copy()
        if self.verbose > 4 :
            print( "LogL  ", fmt( Lhood ), " LowL  ", fmt( lowLhood), nstep, maxtrial, size )
            print( "alpar ", fma( ptry, linelength=200 ) )
            fip = allpars[fitIndex]
            print( "uap   ", fma( self.domain2Unit( problem, fip, fitIndex ), linelength=200) )
            print( "unitr ", fma( self.unitRange, linelength=200 ), self.unitRange[-2] )

        step = 0
        trial = 0

        while True:
            trial += 1
            f = -1

            um.setParameters( problem, allpars )
            if inside == 0 :                            # safely inside lowLhood area
                ptry[fitIndex] = um.stepPars( 1.0 )

            elif inside == 1 :                          # first time outside -> mirror
                f = ( 1.0 if Lhood == Ltry else
                      ( Lhood - lowLhood ) / ( Lhood - Ltry ) )     # lin interpolation to edge

                pedge = ptry.copy()
                pedge[fitIndex] = um.stepPars( f )                # ptry on edge

                dLdp = self.errdis.partialLogL( problem, pedge, fitIndex )
                self.plotter.move( allpars, pedge, col=1, sym=4 )

                um.mirrorOnLowL( dLdp )
                ptry[fitIndex] = um.stepPars( 1 - f )

                self.plotter.move( pedge, ptry, col=2 )
            else:                                       # mirroring failed; do reverse
                size *= 0.7
                um.reverseVelocity( size )
                ptry[fitIndex] = um.stepPars( 1.0 )

                self.plotter.move( allpars, ptry, col=3, sym=0 )

            ## future extension #########################
            # if self.constrain :
            #     xdata = self.errdis.xdata
            #     ptry = self.constrain( model, ptry, xdata )
            #############################################

            Ltry = self.errdis.logLikelihood( problem, ptry )

            if self.verbose > 4 :
                print( "uval  ", fma( um.upar, linelength=200 ) )
#                print( "Ltry  ", Ltry, "  Lowl  ", lowLhood, self.walkers[-1].logL )

            if Ltry >= lowLhood:
                self.plotter.move( allpars, ptry, col=0, sym=0 )

                allpars = ptry.copy( )
                Lhood = Ltry
                self.reportSuccess( )
                npout = len( allpars )
                inside = 0
                step += 1
                trial = 0

                ## update the walker
                update = len( self.walkers ) if append else kw
                self.setWalker( update, problem, allpars, Lhood, fitIndex=fitIndex )

            else:
                inside += 1
                if inside == 1:
                    self.plotter.move( allpars, ptry, col=5, sym=4 )
                    self.reportReject( )
                else:
                    self.plotter.move( allpars, ptry, col=4, sym=4 )
                    self.reportFailed( )

            if self.verbose > 4 :
                print( "GEng  ", fma(ptry, linelength=200) )
                print( "Ltry  ", fmt(Ltry), inside, step, trial, fmt( size ) )


            if not ( step < nstep and trial < maxtrial ):
                break



        if npout == 0 :
            self.size = max( 0.9 * self.size, 1e-6 )
            if self.verbose > 4 :
                warnings.warn( "GalileanEngine: no steps found" )
        else :
            self.size = min( self.SIZE, self.size * 1.1 )

        self.plotter.stop( param=allpars, name="GalileanEngine" )
        return npout

class UnitMovements( object ):
    """
    Define all parameter movements in unitspace.



    """
    def __init__( self, walker, engine, size ):
        self.problem = walker.problem
        self.fitIndex = walker.fitIndex

        self.np = len( self.fitIndex )
        self.engine = engine
        self.setParameters( self.problem, walker.allpars )

        if self.np > len( self.engine.unitRange ) :
            self.engine.unitRange = numpy.ones( self.np, dtype=float )

        self.upran = self.engine.unitRange[self.fitIndex]
        self.setVelocity( size )

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

    def stepPars( self, f ):
        """
        Return a new stepped parameter set.
        """
        uv = self.uvel
        # add small random contribution to velocity
        uv *= 1 + ( self.uniform() * 0.1 )
        pv = self.upar + uv * f

        # check if outside [0,1]
        pv, uv = numpy.where( pv <= 0, ( -pv, -uv ), ( pv, uv ) )
        self.upar, self.uvel = numpy.where( pv >= 1, ( 2 - pv, -uv ), ( pv, uv ) )

        return self.engine.unit2Domain( self.problem, self.upar, kpar=self.fitIndex )

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
        self.uvel = self.uniform() * self.upran * size

    def reverseVelocity( self, size ):
        """
        Reverse the unit velocity when mirroring fails.
        Add small perturbation.
        """
        upv = self.uvel                 # keep original velocity
        self.setVelocity( size )        # get a new one to perturb
        nm = len( self.engine.walkers )
        self.uvel = size * ( self.np * self.uvel - nm * upv ) / ( nm + self.np )



