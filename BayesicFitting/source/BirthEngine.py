import numpy as numpy

from .Dynamic import Dynamic
from .Engine import Engine
from .Formatter import formatter as fmt

__author__ = "Do Kester"
__year__ = 2021
__license__ = "GPL"
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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2017 - 2021 Do Kester

class BirthEngine( Engine ):
    """
    The BirthEngine adds a new component to the model.

    Only for Models that are Dynamic.
    The birth rate is governed by the growth-prior in the Dynamic.

    The member is kept when the logLikelihood > lowLhood.

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
        copy : BirthEngine
            to be copied
        seed : int
            for random number generator

        """
        super( ).__init__( walkers, errdis, slow=slow, copy=copy,
                    seed=seed, verbose=verbose )

    def copy( self ):
        """ Return copy of this.  """
        return BirthEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "BirthEngine" )

    #  *********EXECUTE***************************************************
    def execute( self, kw, lowLhood, append=False, iteration=0 ):
        """
        Execute the engine by adding a component and diffusing the parameters.

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

        walker = self.walkers[kw].copy()            ## work on local copy.

        nhyp = self.errdis.nphypar
        walker.problem.model.parameters = walker.allpars[:-nhyp] if nhyp > 0 else walker.allpars

        problem = walker.problem
        allp = walker.allpars
        ftry = walker.fitIndex

        if self.verbose > 4 :
            print( "BEN0  ", walker.id, walker.parent, fmt( allp, max=None ), len( ftry ) )

        off = 0
        model = problem.model
        model.parameters = allp[:model.npars]

        while model is not None and not isinstance( model, Dynamic ) :
            off += model.npbase
            model = model._next

        nc = model.ncomp
        np = model.npbase

        if self.verbose > 4 :
            print( "BEN1  ", walker.id, nc, np, len( allp ), len( ftry ) )

        if not ( nc < model.growPrior.unit2Domain( self.rng.rand() ) and
                 model.grow( offset=off, rng=self.rng ) ):
            self.reportReject()
            return 0

        dnp = model.npbase - np         # parameter change
        ftry = model.alterFitindex( ftry, np, dnp, off )
        ptry = problem.model.parameters          ## list of grown parameters
        if nhyp > 0 :
            ptry = numpy.append( ptry, allp[-nhyp:] )

        loc = model.location            # where the extra parameters are inserted
        del( model.location )           # not needed anymore

        t = 0
        k0 = off + loc
        k1 = k0 + dnp
        klst = [k for k in range( k0, k1 )]

        while t < self.maxtrials :

            Ltry = self.errdis.logLikelihood( problem, ptry )

            if Ltry >= lowLhood:
                self.reportSuccess()
                update = len( self.walkers ) if append else kw
                self.setWalker( update, problem, ptry, Ltry, fitIndex=ftry )
                wlkr = self.walkers[update]
                wlkr.check( nhyp=nhyp )
                return dnp
            else :
                uval = self.rng.rand( dnp )
                ptry[klst] = self.unit2Domain( problem, uval, kpar=klst )

                self.reportReject()
                t += 1

#        print( "Birth   ", walker.id, fmt( ptry, max=None ) )

        self.reportFailed()

        return 0


