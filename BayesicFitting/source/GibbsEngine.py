import numpy as numpy
from . import Tools
from .Formatter import formatter as fmt
from .Formatter import fma

from .Engine import Engine
from .Engine import DummyPlotter

__author__ = "Do Kester"
__year__ = 2021
__license__ = "GPL3"
__version__ = "2.7.0"
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

class GibbsEngine( Engine ):
    """
    Move a one parameter at a time by a random amount.

    The walker is kept when the logLikelihood > lowLhood

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
        copy : GibbsEngine
            to be copied
        kwargs : for Engine
            "slow", "seed", "verbose"

        """
        super( ).__init__( walkers, errdis, copy=copy, **kwargs )

        self.plotter = DummyPlotter()

    def copy( self ):
        """ Return copy of this.  """
        return GibbsEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "GibbsEngine" )

    #  *********EXECUTE***************************************************
    def execute( self, kw, lowLhood, append=False, iteration=0 ):
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
        int : the number of successfull moves

        """
        self.reportCall()

        walker = self.walkers[kw].copy()              ## work on local copy

        problem = walker.problem
        fitIndex = walker.fitIndex

        perm = self.rng.permutation( fitIndex )
        if hasattr( self, "nstep" ) :
            pm = perm
            for k in range( 1, self.nstep ) :
                perm = numpy.append( perm, pm )

        ur = self.unitRange * ( 1 + 2.0 / len( self.walkers ) )

        param = walker.allpars
        self.plotter.start( param=param )

        if self.verbose > 4 :
            print( "alpar ", fma( param ), fmt( walker.logL ), fmt( lowLhood) )
            fip = param[fitIndex]
            print( "uap   ", fma( self.domain2Unit( problem, fip, fitIndex )))
            print( "fitin ", fma( fitIndex ), self.maxtrials )
            print( "unitr ", fma( self.unitRange ) )

        steps = 0
        for c in perm :

            save = param[c]
            ptry = param.copy()
            usav = self.domain2Unit( problem, save, kpar=c )
            while True :
                step = 2 * self.rng.rand() - 1.0
                if c < len( ur ) :
                    step *= ur[c]
                utry = usav + step
                if 0 < utry < 1 : break

            kk = 0
            while True :
                kk += 1
                ptry[c] = self.unit2Domain( problem, utry, kpar=c )

                Ltry = self.errdis.updateLogL( problem, ptry, parval={c : save} )

                if self.verbose > 4 :
                    print( "Gibbs ", fma(ptry), fmt(Ltry), kk, fmt( step ) )

                if Ltry >= lowLhood:
                    self.plotter.move( param, ptry, col=0, sym=0 )
                    self.reportSuccess( )
                    param = ptry

                    update = len( self.walkers ) if append else kw
                    self.setWalker( update, problem, param, Ltry, fitIndex=fitIndex )
                    steps += 1
                    break
                elif kk < self.maxtrials :
                    self.plotter.move( param, ptry, col=5, sym=4 )
                    while True :
                        utry = usav + step * ( 2 * self.rng.rand() - 1.0 )
                        if 0 < utry < 1 : break
                    self.reportReject( )
                else :
                    self.reportFailed()
                    param[c] = save
                    break

        self.plotter.stop( param=param, name="GibbsEngine" )

        return steps                        # nr of succesfull steps


