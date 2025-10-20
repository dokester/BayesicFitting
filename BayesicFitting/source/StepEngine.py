import numpy as numpy
from .Formatter import formatter as fmt
from .Formatter import fma

from .Engine import Engine
from .Engine import DummyPlotter

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

class StepEngine( Engine ):
    """
    Move a walker in a random direction.

    The StepEngine tries to move the parameters at most 4 times in
    a random direction.

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
        walkers : WalkerList
            walkers to be diffused
        errdis : ErrorDistribution
            error distribution to be used
        copy : StepEngine
            to be copied
        kwargs : for Engine
            "phantoms", "slow", "seed", "verbose"
        """
        super( ).__init__( walkers, errdis, copy=copy, **kwargs )
        self.plotter = DummyPlotter()


    def copy( self ):
        """ Return copy of this.  """
        return StepEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "StepEngine" )


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
        append : bool
            set walker in place or append
        iteration : int
            iteration number

        Returns
        -------
        int : the number of successfull steps

        """
        self.reportCall()

        walker = self.walkers[kw].copy()
        problem = walker.problem
        fitIndex = walker.fitIndex
        np = len( fitIndex )

        param = walker.allpars
        urange, umin = self.getUnitRange( problem, lowLhood, walker.nap )
        urange = urange[fitIndex]

        dur = urange / len( self.walkers )      ## some fraction
        urange += 2 * dur                       ## extension

        self.plotter.start( param=param )
        usav = self.domain2Unit( problem, param[fitIndex], kpar=fitIndex )
#        self.startJourney( usav )

        if self.verbose > 4 :
            print( "alpar ", fma( param ), fmt( walker.logL ), fmt( lowLhood) )
            print( "uap   ", fma( usav ) )
            print( "fitin ", fma( fitIndex ), self.maxtrials )
            print( "unitr ", fma( urange ) )


        sz = 1.0
        step = ( self.rng.rand( np ) - 0.5 ) * urange
        ks = kt = 0

        while ks < self.nstep() :
            ptry = param.copy()

            # iterate until all utry is in [0,1]
            while True :
                utry = usav + step
                q0 = numpy.where( utry < 0 )[0]
                nq0 = len( q0 )
                q1 = numpy.where( utry > 1 )[0]
                nq1 = len( q1 )

                if nq0 > 0 :
                    step[q0] = ( self.rng.rand( nq0 ) - 0.5 ) * urange[q0]
                elif nq1 > 0 :
                    step[q1] = ( self.rng.rand( nq1 ) - 0.5 ) * urange[q1]
                else :
                    break

            # calculate ptry from utry and hence the trial of Likelihood.
            ptry[fitIndex] = self.unit2Domain( problem, utry, kpar=fitIndex  )
            Ltry = self.errdis.logLikelihood( problem, ptry )

            if self.verbose > 4 :
                print( "Step  ", fma(ptry), fmt(Ltry), ks, kt, fmt( sz ) )

            # success. Update walker. reset size and step
            if Ltry >= lowLhood:
                self.plotter.move( param, ptry, col=0, sym=0 )
#                self.calcJourney( utry - usav )
                self.reportSuccess( )

                self.setWalker( kw, problem, ptry, Ltry, fitIndex=fitIndex )
                param = ptry
                usav = utry
                sz = 1.0
                step = ( self.rng.rand( np ) - 0.5 ) * urange
                ks += 1
                kt = 0
            # failed. reverse and shrink step
            elif kt <= self.maxtrials :
                self.plotter.move( param, ptry, col=5, sym=4 )

                sz *= ( -1 if kt % 2 == 0 else self.rng.rand( 1 ) )
                step *= sz
                kt += 1
                self.reportReject( )
            # failed too many times
            else :
                self.reportFailed()
                break

        self.plotter.stop( param=param, name="StepEngine" )

        return np * ks                       # nr of successfull parameter moves


