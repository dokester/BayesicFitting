import numpy as numpy

from .Engine import Engine
from .Engine import DummyPlotter

__author__ = "Do Kester"
__year__ = 2024
__license__ = "GPL3"
__version__ = "3.2.1"
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
#  *    2017 - 2024 Do Kester

class RandomEngine( Engine ):
    """
    RandomEngine.

    It generates a random trial point from the available unit box.
    If it is OK (> lowLhood) it is kept. 
    The execute method returns immediately as the new point is random and 
    completely independent of the fiducial point.

    If is is not OK, the trial point is shrunk by a random amount toward 
    the fiducial point, until it is accepted.
    Now the new point is not independent of the fiducial point. We start 
    the execution again starting from the new point. 

    The restart is repeated a few times after which he new point is deemed
    sufficiently independent. 

    Attributes from Engine
    ----------------------
    walkers, errdis, maxtrials, slow, rng, report, phantoms, verbose

    Author       Do Kester.

    """
    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, **kwargs ):
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
        kwargs : for Engine
            "phantoms", "slow", "seed", "verbose"
        """
        super( ).__init__( walkers, errdis, copy=copy, **kwargs )
        self.plotter = DummyPlotter()

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
        fi = walker.fitIndex
        nf = len( fi )
        param = walker.allpars
        
        ## Make a unit box to find a new walker in
        nap = len( param )
        um, ux = self.getUnitMinmax( problem, lowLhood )

        mlen = len( self.walkers )
        dr = 10 * ( ux - um ) / mlen
        um -= dr
        um = numpy.where( um < 0, 0.0, um )
        ux += dr
        ux = numpy.where( ux > 1, 1.0, ux )

        self.plotter.start( param=walker.allpars )

        t = 0
        for tt in range( self.nstep ) :
            ptry = param.copy()
            uval = self.rng.uniform( um, ux, nap )
            ptry[fi] = self.unit2Domain( problem, uval, kpar=fi )

            Ltry = self.errdis.logLikelihood( problem, ptry )

            if Ltry >= lowLhood :       ## Lucky, in 1 step a truely random point
                self.plotter.move( param, ptry, col=0, sym=2 )
                self.reportSuccess()
                update = len( self.walkers ) if append else kw
                self.setWalker( update, problem, ptry, Ltry, fitIndex=fi )

                self.plotter.stop( param=ptry, name="RandomEngine" )
                return nf                  # nr of successfull params moves

            self.plotter.move( param, ptry, col=5, sym=4 )
            """
            ## not lucky; shrink onto the fiducial point
            utry = self.domain2Unit( problem, param )
            kk = 0
            while True :
                kk += 1
                dr = self.rng.uniform( 0.0, 1.0, 1 )
                uval = ( 1 - dr ) * utry + dr * uval
                ptry[fi] = self.unit2Domain( problem, uval, kpar=fi )

                Ltry = self.errdis.logLikelihood( problem, ptry )
                if Ltry >= lowLhood:
                    self.reportSuccess( )
                    self.plotter.move( param, ptry, col=0, sym=4 )
                    update = len( self.walkers ) if append else kw
                    self.setWalker( update, problem, ptry, Ltry, fitIndex=fi )
                    param = ptry
                    t += 1
                    break
                elif kk < self.maxtrials :
                    self.reportReject( )
                    self.plotter.move( param, ptry, col=5, sym=4 )
                else :
                    self.reportFailed()
                    break
            """
        if t == 0 :
            self.reportFailed()
            return 0

        self.plotter.stop( param=ptry, name="RandomEngine" )

        return nf                        # nr of successfull params moves


