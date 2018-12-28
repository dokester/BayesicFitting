import numpy as numpy

from .Dynamic import Dynamic
from .Engine import Engine

__author__ = "Do Kester"
__year__ = 2018
__license__ = "GPL"
__version__ = "1.0"
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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2017 - 2018 Do Kester

class BirthEngine( Engine ):
    """
    The BirthEngine adds a new component to the model.

    Only for Models that are Dynamic.
    The birth rate is governed by the growth-prior in the dynamic model.

    The member is kept when the logLikelihood > lowLhood.

    Author       Do Kester.

    """

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, seed=23455, verbose=0 ) :
        """
        Constructor.

        Parameters
        ----------
        walkers : list of Walker
            walkers to be diffused
        errdis : ErrorDistribution
            error distribution to be used
        copy : BirthEngine
            to be copied
        seed : int
            for random number generator

        """
        super( BirthEngine, self ).__init__( walkers, errdis, copy=copy,
                    seed=seed, verbose=verbose )

    def copy( self ):
        """ Return copy of this.  """
        return BirthEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "BirthEngine" )

    #  *********EXECUTE***************************************************
    def execute( self, walker, lowLhood ):
        """
        Execute the engine by adding a component and diffusing the parameters.

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

        cwalker = walker.copy()                  ## work on local copy.

        problem = cwalker.problem
        ptry = cwalker.allpars
        ftry = cwalker.fitIndex

        if self.verbose > 4 :
            print( "BEN0  ", walker.id, walker.parent, len( ptry ), len( fitIndex ) )

        pat = 0
        model = problem.model
        while model is not None and not isinstance( model, Dynamic ) :
            pat += model.npbase
            model = model._next

        nc = model.ncomp
        np = model.npbase

        if self.verbose > 4 :
            print( "BEN1  ", cwalker.id, nc, np, len( ptry ), len( ftry ) )

        if not ( nc < model.growPrior.unit2Domain( self.rng.rand() ) and
                 model.grow( pat ) ):
#            print( "BEN2  ", "failed" )
            self.reportFailed()
            return 0

        dnp = model.npbase - np         # parameter change
        ptry = model.alterParameters( ptry, np, dnp, pat )
        ftry = model.alterFitindex( ftry, np, dnp, pat )
        problem.npars += dnp

        t = 0
        while t < self.maxtrials :
            for kp in range( pat+np, pat+np+dnp ) :
                ptry[kp] = problem.unit2Domain( self.rng.rand(), kpar=kp )
            Ltry = self.errdis.logLikelihood( problem, ptry )

            if Ltry >= lowLhood:
                self.reportSuccess()
                self.setWalker( cwalker, problem, ptry, Ltry, fitIndex=ftry )
                wlkr = self.walkers[walker.id]
                wlkr.check( nhyp=self.errdis.nphypar )
                return dnp
            else :
                self.reportFailed()
                t += 1

        self.reportReject( )

        return 0


