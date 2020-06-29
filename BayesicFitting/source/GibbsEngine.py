import numpy as numpy
from . import Tools
from .Formatter import formatter as fmt
from .Formatter import fma

from .Engine import Engine

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
__version__ = "2.5.3"
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
#  *    2017 - 2020 Do Kester

class GibbsEngine( Engine ):
    """
    Move a one parameter at a time by a random amount.

    The walker is kept when the logLikelihood > lowLhood

    Author       Do Kester.

    """
    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, slow=None, copy=None, seed=4213, verbose=0 ):
        """
        Constructor.

        Parameters
        ----------
        walkers : WalkerList
            walkers to be diffused
        errdis : ErrorDistribution
            error distribution to be used
        slow : None or int > 0
            Run this engine every slow-th iteration. None for all.
        copy : GibbsEngine
            to be copied
        seed : int
            for random number generator

        """
        super( ).__init__( walkers, errdis, slow=slow, copy=copy, seed=seed, verbose=verbose )

    def copy( self ):
        """ Return copy of this.  """
        return GibbsEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "GibbsEngine" )

    #  *********EXECUTE***************************************************
    def execute( self, walker, lowLhood ):
        """
        Execute the engine by diffusing the parameters.

        Parameters
        ----------
        walker : Sample
            walker to diffuse
        lowLhood : float
            lower limit in logLikelihood

        Returns
        -------
        int : the number of successfull moves

        """
        self.reportCall()

        walker = walker.copy()              ## work on local copy

        problem = walker.problem
        fitIndex = walker.fitIndex

        perm = self.rng.permutation( fitIndex )
        ur = self.unitRange * ( 1 + 2.0 / len( self.walkers ) )

        param = walker.allpars
        if self.verbose > 4 :
            print( "alpar ", fma( param ), fmt( walker.logL ), fmt( lowLhood) )
            fip = param[fitIndex]
            print( "uap   ", fma( self.domain2Unit( problem, fip, fitIndex )))
            print( "fitin ", fma( fitIndex ), self.maxtrials )
            print( "unitr ", fma( self.unitRange ) )

        Lbest = self.walkers[-1].logL
        t = 0
        for c in perm :
            param = walker.allpars.copy()
            save = param[c]
            usav = self.domain2Unit( problem, save, kpar=c )
            while True :
                step = 2 * self.rng.rand() - 1.0
                if c < len( ur ) :
                    step *= ur[c]
                ptry = usav + step
                if 0 < ptry < 1 : break

            kk = 0
            while True :
                kk += 1
                param[c] = self.unit2Domain( problem, ptry, kpar=c )

                Ltry = self.errdis.updateLogL( problem, param, parval={c : save} )

                if self.verbose > 4 :
                    print( "Gibbs ", fma(param), fmt(Ltry), kk, fmt( step ) )

                if Ltry >= lowLhood:
                    self.reportSuccess( )
                    self.setWalker( walker, problem, param, Ltry, fitIndex=fitIndex )
                    t += 1
                    break
                elif kk < self.maxtrials :
                    while True :
                        ptry = usav + step * ( 2 * self.rng.rand() - 1.0 )
                        if 0 < ptry < 1 : break
                    self.reportReject( )
                else :
                    self.reportFailed()
                    param[c] = save
                    break

            if Ltry > Lbest :
                Lbest = Ltry
                self.setWalker( self.walkers[-1], problem, param.copy(), Lbest, fitIndex=fitIndex )
                self.reportBest()

        return t                        # nr of succesfull steps


