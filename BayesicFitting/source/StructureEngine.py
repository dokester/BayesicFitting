import numpy as numpy

from .Modifiable import Modifiable
from .Engine import Engine
from . import Tools
from .Formatter import formatter as fmt

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL"
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
#  *    2019 - 2020 Do Kester

class StructureEngine( Engine ):
    """
    The StructureEngine varies the internal structure of the model.

    Only for Models that are Modifiable.

    The member is kept when the logLikelihood > lowLhood.

    Attributes
    ----------
    None of its own

    Attributes from Engine
    ----------------------
    walkers, errdis, slow, maxtrials, rng, report, unitRange, unitMin, verbose

    Author       Do Kester.

    """

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, slow=None, copy=None, seed=23455, verbose=0 ) :
        """
        Constructor.

        Parameters
        ----------
        walkers : list of Walker
            walkers to be diffused
        errdis : ErrorDistribution
            error distribution to be used
        slow : None or int > 0
            Run this engine every slow-th iteration. None for all.
        copy : StructureEngine
            to be copied
        seed : int
            for random number generator

        """
        super( ).__init__( walkers, errdis, slow=slow, copy=copy,
                    seed=seed, verbose=verbose )

    def copy( self ):
        """ Return copy of this.  """
        return StructureEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "StructureEngine" )

    #  *********EXECUTE***************************************************
    def execute( self, kw, lowLhood, append=False, iteration=0 ):
        """
        Execute the engine by changing a component.

        Parameters
        ----------
        kw : int
            index of walker to diffuse
        lowLhood : float
            lower limit in logLikelihood
        append : bool
            set walker in place or append in walkerlist
        iteration : int
            iteration number

        Returns
        -------
        int : the number of successfull moves

        """
        self.reportCall()

        t = 0
        k = 0
        perm = self.rng.permutation( self.walkers[kw].problem.model.ncomp - 2 )     ## TBC
        for p in perm :
            update = len( self.walkers ) if append else kw
            dt = self.executeOnce( kw, lowLhood, update, location=p+1 )
            if dt > 0 :
                kw = update
            t += dt

        return t

    def executeOnce( self, wlkrid, lowLhood, update, location=None ) :
        """
        One execution call.
        """

        walker = self.walkers[wlkrid]
        cwalker = walker.copy()                  ## work on local copy.
        problem = cwalker.problem.copy()
        ptry = cwalker.allpars.copy()
        ftry = cwalker.fitIndex.copy()

        if self.verbose > 4 :
            print( "SEN0  ", walker.id, walker.parent, len( ptry ), len( ftry ), walker.logL )
            print( "      ", fmt( problem.model.knots, max=None ) )

        off = 0
        model = problem.model
        while model is not None and not isinstance( model, Modifiable ) :
            off += model.npbase
            model = model._next

        if self.verbose > 4 :
            nc = model.ncomp
            np = model.npbase
            print( "SEN1  ", cwalker.id, nc, np, len( ptry ), len( ftry ) )

        if not model.vary( location=location, rng=self.rng ):
            self.reportReject()
            return 0

        problem.model = model._head
        Ltry = self.errdis.logLikelihood( problem, ptry )

        if self.verbose > 4 :
            print( "SEN3  ", fmt( ptry, max=None ), Ltry, lowLhood )
            print( "      ", fmt( problem.model.knots, max=None ) )

        if Ltry >= lowLhood:
            self.reportSuccess()
            self.setWalker( update, problem, ptry, Ltry, fitIndex=ftry )
            wlkr = self.walkers[update]

            wlkr.check( nhyp=self.errdis.nphypar )

            return 1

        self.reportFailed()
        return 0


