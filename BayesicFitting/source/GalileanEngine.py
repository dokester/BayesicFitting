import numpy as numpy
import math
import sys
from .Formatter import formatter as fmt
from .Formatter import fma

from .Engine import Engine
from .Engine import DummyPlotter

### Uncomment all plot sections
#> sed '/##PlotSection/, /^$/ s/^#PLT/    /g'
### Comment back all plot sections
#> sed '/##PlotSection/, /^$/ s/^    /#PLT/g'


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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2017 - 2025 Do Kester

class GalileanEngine( Engine ):
    """
    Move all parameters in forward steps, with optional mirroring on the edge.

    Move the parameters in a random direction for N iterations; mirror the direction
    on the gradient of the logLikelihood when the parameters enter the zone of logLlow.

    Attributes
    ----------
    size : float (0.5)
        adaptable fraction for the (unit) direction of the stepping
    wiggle : float (0.3)
        factor to perturb the direction at each step. 
        between 0 (no perturbation) and 1 (new direction)

    Attributes from Engine
    ----------------------
    walkers, errdis, maxtrials, nstep, slow, rng, report, phancol, verbose

    Author       Do Kester.

    """

    SIZE = 0.5
    WIGGLE = 0.2


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
            "phancol", "slow", "seed", "verbose"

        """
        super( ).__init__( walkers, errdis, copy=copy, **kwargs )

        self.wiggle = self.WIGGLE
        self.size = self.SIZE
        
        ## increase step size at success; decrease at failure 
        ## balance 3 successes to 1 failure
        self._dsize = 0.01              ## fractional change in size
        self._balance = 3               ## balance between increments and decrements
        self._increment = 1 + self._dsize
        self._decrement = 1 / ( 1 + self._balance * self._dsize )

        self.plotter = DummyPlotter( )

##PlotSection
#PLT    self.plot = False               ## for checking the findEdge method

    def copy( self ):
        """ Return copy of this.  """
        engine = GalileanEngine( self.walkers, self.errdis, copy=self )
        return engine

    def __str__( self ):
        """ Return the name of this engine.  """
        return str( "GalileanEngine" )

    #  *********EXECUTE***************************************************
    def execute( self, kw, lowLhood, iteration=0 ):
        """
        Execute the engine by diffusing the parameters.

        Parameters
        ----------
        kw : int
            index in walkerlist, of the walker
        lowLhood : float
            lower limit in logLikelihood

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

        isOutside = 0                                           ## start inside lowLhood area
        Ltry = 0

        ff = ( 1.0 if lowLhood <= -sys.float_info.max 
                else 1 / math.sqrt( max( 1, problem.npars ) ) )
        size = self.size * ff                    ## adaptable size for velocity

        self.plotter.start( param=allpars )
        um = UnitMovements( walker, self, size, lowLhood )

        nstep = self.nstep()
        maxtrial = self.maxtrials

        ptry = allpars.copy()
        if self.verbose > 4 :
            print( "Galilean   LogL  ", fmt( Lhood ), " LowL  ", fmt( lowLhood), 
                    nstep, maxtrial, size )
            print( "alpar ", fma( ptry, linelength=200 ) )
            fip = allpars[fitIndex]
            print( "uap   ", fma( self.domain2Unit( problem, fip, fitIndex ), linelength=200) )
            print( "unitr ", fma( um.upran, linelength=200 ) )
            print( '--------------------' )
        step = 0
        trial = 0
#        self.tripSq = 0

#        um.setParameters( problem, allpars )
#        self.startJourney( um.upar )

        while True:
            trial += 1

            um.setParameters( problem, allpars )           # restart at safe location

            if isOutside == 0 :                            # safely inside lowLhood area
                um.uvel = ( 1 - self.wiggle ) * um.uvel + self.wiggle * um.getVelocity( size )

                ptry[fitIndex] = um.trialStep( 1.0, size )

            elif isOutside == 1 :                          # first time outside -> mirror

                pedge, restep = self.findEdge( problem, ptry, fitIndex, Lhood, Ltry, lowLhood, 
                                              um, size, plot=False )

                dLdp = self.errdis.partialLogL( problem, pedge, fitIndex )
                um.acceptTrial()
                um.mirrorOnLowL( dLdp )
                ptry[fitIndex] = um.trialStep( restep, size )    ## part of te step still to be done

#                self.plotter.move( allpars, pedge, col=1, sym=4 )
                self.plotter.move( allpars, pedge, col=1 )
                self.plotter.move( pedge, ptry, col=2 )

            else:                                          # mirroring failed; do reverse
                size *= 0.7
                um.reverseVelocity( size )
                ptry[fitIndex] = um.trialStep( 1.0, size )

#                self.plotter.move( allpars, ptry, col=3, sym=0 )
                self.plotter.move( allpars, ptry, col=3 )

            Ltry = self.errdis.logLikelihood( problem, ptry )


            if Ltry >= lowLhood:
#                self.plotter.move( allpars, ptry, col=0, sym=0 )
                self.plotter.move( allpars, ptry, col=0 )
#                self.tripSq += self.unitTripSquare( um.upar - um.uptry )
#                self.calcJourney( um.upar - um.uptry )

                um.acceptTrial()

                allpars = ptry.copy( )
                Lhood = Ltry
                self.reportSuccess( )
                isOutside = 0
                step += 1
                trial = 0
                ## adaptable size for velocity
                size = self.incsize() * ff

                ## update the walker
                self.setWalker( kw, problem, allpars, Lhood, walker=walker,
                                fitIndex=fitIndex )

            else:
                isOutside += 1
                if isOutside == 1:
#                    self.plotter.move( allpars, ptry, col=5, sym=4 )
                    self.plotter.move( allpars, ptry, col=5 )
                    self.reportReject( )
                else:
                    self.plotter.move( allpars, ptry, col=4 )
                    self.reportFailed( )
                ## adaptable size for velocity
                size = self.decsize() * ff

            if self.verbose > 4 :
                print( "upar  ", fma( um.upar, linelength=200 ) )
                print( "uvel  ", fma( um.uvel, linelength=200 ) )
                print( "ptry  ", fma( ptry, linelength=200 ) )
                print( "Ltry  ", fmt( Ltry ), isOutside, step, trial, self.plotter.iter-1, 
                        fmt( size ) )
                print( '--------------------' )


            if not ( step < nstep and trial < maxtrial ):
                break


        self.plotter.stop( param=allpars, name="GalileanEngine" )

        return step * len( fitIndex )           # nr of successfull steps

    def incsize( self ):
        """ Return increased self.size """
        self.size = min( self.size * self._increment, self.SIZE * 4 )
        return self.size

    def decsize( self ) :
        """ Return decreased self.size. """       
        self.size = max( self.size * self._decrement, self.SIZE / 4 )
        return self.size

    def findEdge( self, problem, ptry, fitIndex, Lhood, Ltry, lowLhood, um, size, 
                    plot=False ) :
        """
        Find the edge of the likelihood where logL equals LowLhood. 

        Parameters
        ----------
        problem : Problem
            the problem
        ptry : array-like
            parameters with likelihood outside lowLhood region
        fitIndex : array-like
            indices of parameters that need fitting
        Lhood : float
            last likelihood before going outside
        Ltry : float
            likelihood outside (at ptry)
        lowLhood : float
            lower limit in logLikelihood
        um : UnitMovements (see below)
            of this run
        size : float
            present size value

        Returns
        -------
        pedge : array-like
            parameter values at the edge of lowLhood
        restep : float
            part of the step outside lowLhood area. 
        """
##PlotSection
#PLT    if self.plot :
#PLT        import matplotlib.pyplot as plt
#PLT        Led = [0] * 101
#PLT        xed = [0.01*ked for ked in range( 101 )]
#PLT        for ked in range( 101 ) :
#PLT            ped = ptry.copy()
#PLT            ped[fitIndex] = um.trialStep( 0.01*ked, size )
#PLT            Led[ked] = self.errdis.logLikelihood( problem, ped )
#PLT        plt.plot( xed, Led, 'b-' )
#PLT        plt.plot( [0,1], [lowLhood,lowLhood], 'g-' )

        ptry[fitIndex] = um.trialStep( 0.5, size )    # params at mid point
        Lmid = self.errdis.logLikelihood( problem, ptry )

        pedge = ptry.copy()

        xint = [0.0, 0.5, 1.0]
        yint = [Lhood, Lmid, Ltry]

        eps = 0.001 * ( Lhood - Ltry )
        for ktr in range( 10 ) :

            f = self.quadInterpol( xint, yint, lowLhood, plot=plot )

            pedge[fitIndex] = um.trialStep( f, size )
            Ledge = self.errdis.logLikelihood( problem, pedge )

##PlotSection
#PLT        if self.plot :
#PLT            plt.plot( [f], [Ledge], 'r*' )
#PLT            plt.text( f, Ledge, "%d"%ktr )
#PLT            plt.plot( [f,f], [lowLhood,Ledge], 'k-' )

            if abs( Ledge - lowLhood ) < eps :
                break

            k = 2 if f < xint[1] else 0
            yint[k] = yint[1]
            xint[k] = xint[1]
            yint[1] = Ledge
            xint[1] = f

#        print( ktr, Ledge, lowLhood )

##PlotSection
#PLT    if self.plot :
#PLT        plt.show()


        return pedge, 1 - f


    def quadInterpol( self, x, y, lowL, plot=False ) :
        """
        Quadratic interpolation of a function defined by 3 point (x,y) at level
        ylow.

        Parameters
        ----------
        x : array of 3 floats
            x-values
        y : array of 3 floats
            y-values   
        ylow : float 
            find xlow at ylow
        """
        mat = [[x[0]*x[0], x[0], 1.0], [x[1]*x[1], x[1], 1.0], [x[2]*x[2], x[2], 1.0]]
        mat = numpy.array( mat )
        beta = numpy.array( y )
        try :
            a, b, c = numpy.linalg.solve( mat, beta )
        except :
            return ( x[2] - x[0] ) / 2

        if a == 0 :
            return 1 if b == 0 else ( lowL - c ) / b

##PlotSection
#PLT    if self.plot :
#PLT        tt = numpy.linspace( x[0], x[2], 101 )
#PLT        aa = a * tt * tt + b * tt + c
#PLT        plt.plot( tt, aa, 'r-' )

        det = b * b - 4 * a * ( c - lowL )
        det = 0 if det < 0 else math.sqrt( det )

        xint = ( - b - det ) / ( 2 * a )
        if x[0] < xint < x[2] :
            return xint
        else :
            return ( - b + det ) / ( 2 * a )




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

        uran, umin = engine.getUnitRange( self.problem, lowLhood, walker.nap )
        self.upran = uran[self.fitIndex]

        self.upran = numpy.amax( self.upran )
        self.uvel = self.getVelocity( size )

    def getVelocity( self, size ):
        """
        Return a new (random) unit velocity.

        Parameters
        ----------
        size : float
            of the (unit) bounding box
        """
        lohi = 0.5 * size * self.upran
        return self.engine.rng.uniform( -lohi, lohi, self.np )

    def setParameters( self, problem, allpars ):
        """
        Set unit values for the applicable parameters

        Parameters
        ----------
        problem : Problem
            the problem at hand
        allpars : array-like
            all parameters of the problem

        """
        fip = allpars[self.fitIndex]
        self.upar = self.engine.domain2Unit( problem, fip, kpar=self.fitIndex )

    def trialStep( self, f, size ):
        """
        Return a new trial parameter set.

        Parameters
        ----------
        f : float between [-1,1]
            fraction of velocity to apply
        size : float
            of the (unit) bounding box
        """
        uv = self.uvel
        up = self.upar + uv * f

        # check if outside [0,1]
        up, uv = numpy.where( up <= 0, ( -up, -uv ), ( up, uv ) )
        self.uptry, self.uvtry = numpy.where( up >= 1, ( 2 - up, -uv ), ( up, uv ) )

        # When on edge, start a new direction with the same signs
        if not all( self.uvtry == self.uvel ) :
            uv = self.getVelocity( size ) 
            self.uvtry = numpy.copysign( uv, self.uvtry )

        return self.engine.unit2Domain( self.problem, self.uptry, kpar=self.fitIndex )

    def acceptTrial( self ) :
        """ Accept this trial """
        self.upar = self.uptry
        self.uvel = self.uvtry

    def mirrorOnLowL( self, dLdp ):
        """
        Mirror the velocity on the low likelihood border.

        Parameters
        ----------
        dLdp : array-like
            derivative of logL to the parameters at the edge
        """
        inprod = numpy.sum( dLdp * self.uvel )
        sumsq  = numpy.sum( dLdp * dLdp )
        if sumsq == 0 : return

        self.uvel -= 2 * dLdp * inprod / sumsq


    def reverseVelocity( self, size ):
        """
        Reverse the unit velocity when mirroring fails.
        Add small perturbation.

        Parameters
        ----------
        size : float
            of the (unit) bounding box
        """
        ff = 0.1                                # 10 percent
        uvpert = self.getVelocity( ff * size )  # unit velocity perturbance
        self.uvel *= ( ff - 1 )                 # reverse uvel and take 90 %
        self.uvel += uvpert                     # add perturbance


