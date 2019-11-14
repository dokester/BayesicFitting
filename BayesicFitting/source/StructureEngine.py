import numpy as numpy

from .Modifiable import Modifiable
from .Engine import Engine
from . import Tools

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
#  *    2019        Do Kester

class StructureEngine( Engine ):
    """
    The StructureEngine varies the structure of the model.

    Only for Models that are Modifiable.
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
        copy : StructureEngine
            to be copied
        seed : int
            for random number generator

        """
        super( StructureEngine, self ).__init__( walkers, errdis, copy=copy,
                    seed=seed, verbose=verbose )

    def copy( self ):
        """ Return copy of this.  """
        return StructureEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "StructureEngine" )

    #  *********EXECUTE***************************************************
    def execute( self, walker, lowLhood ):
        """
        Execute the engine by changing a component.

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
        t = 0
        k = 0
        while t <= walker.problem.model.ncomp and k < self.maxtrials :
            dt = self.executeOnce( walker, lowLhood )
            if dt > 0 :
                t += dt
                k = 0
            else :
                k += 1

        return t

    def executeOnce( self, walker, lowLhood ) :
        """
        One execution call.
        """
        self.reportCall()

        cwalker = walker.copy()                  ## work on local copy.
        problem = cwalker.problem
        ptry = cwalker.allpars
        ftry = cwalker.fitIndex

        if self.verbose > 4 :
            print( "SEN0  ", walker.id, walker.parent, len( ptry ), len( ftry ) )

        off = 0
        model = problem.model
        while model is not None and not isinstance( model, Modifiable ) :
            off += model.npbase
            model = model._next

        if self.verbose > 4 :
            nc = model.ncomp
            np = model.npbase
            print( "SEN1  ", cwalker.id, nc, np, len( ptry ), len( ftry ) )

        if not model.vary( rng=self.rng ):
#            print( "SEN2  ", "failed" )
            self.reportReject()
            return 0

        Ltry = self.errdis.logLikelihood( problem, ptry )

        if Ltry >= lowLhood:
            self.reportSuccess()
            self.setWalker( cwalker, problem, ptry, Ltry, fitIndex=ftry )
            wlkr = self.walkers[walker.id]

#            Tools.printclass( walker )
            wlkr.check( nhyp=self.errdis.nphypar )

            ## check if better than Lbest in walkers[-1]
            self.checkBest( problem, ptry, Ltry, ftry )

#            return model.npbase
            return 1

        self.reportFailed()
        return 0


