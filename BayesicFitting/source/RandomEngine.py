import numpy as numpy

from .Engine import Engine

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
__version__ = "2.6.2"
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

class RandomEngine( Engine ):
    """
    RandomEngine generates a random trial sample.

    It is used to initialize the set of trial samples.

    Author       Do Kester.

    """
    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, seed=4213, verbose=0 ):
        """
        Constructor.
        Parameters
        ----------
        walkers : WalkerList
            walkers to be diffused
        errdis : ErrorDistribution
            error distribution to be used
        copy : RandomEngine
            engine to be copied
        seed : int
            for random number generator
        """
        super( ).__init__( walkers, errdis, copy=copy, seed=seed, verbose=verbose )

    def copy( self ):
        """ Return copy of this.  """
        return RandomEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "RandomEngine" )

    #  *********EXECUTE***************************************************
    def execute( self, kw, lowLhood, append=False, iteration=0 ):
        """
        Execute the engine by a random selection of the parameters.

        Parameters
        ----------
        kw : int
            index of Walker to diffuse
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

        walker = self.walkers[kw].copy()
        problem = walker.problem
        fitIndex = walker.fitIndex

        perm = self.rng.permutation( fitIndex )

        ### Needs more study to make the engine effective.
        mlen = len( self.walkers )
        ur = self.unitRange * mlen / ( mlen - 1 )
        um = self.unitMin - ur / mlen
        q = numpy.where( um < 0 )
        um[q] = 0
        ux = um + ur
        q = numpy.where( ux > 1 )
        ux[q] = 1 - um[q]

        t = 0
        for c in perm :
            param = walker.allpars.copy( )
            save = param[c]
            kk = 0
            while True :
                kk += 1
                uval = self.rng.uniform( um[c], ux[c], 1 )
                param[c] = self.unit2Domain( problem, uval, c )

                Ltry = self.errdis.updateLogL( problem, param, parval={c : save} )
                if Ltry >= lowLhood:
                    self.reportSuccess( )
                    update = len( self.walkers ) if append else kw
                    self.setWalker( update, problem, param, Ltry, fitIndex=fitIndex )
                    t += 1
                    break
                elif kk < self.maxtrials :
                    self.reportReject( )
                else :
                    self.reportFailed()
                    param[c] = save
                    break

        return t                        # nr of succesfull steps


