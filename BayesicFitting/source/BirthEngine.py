import numpy as numpy

from .Dynamic import Dynamic
from .Engine import Engine
from .Formatter import formatter as fmt

__author__ = "Do Kester"
__year__ = 2025
__license__ = "GPL"
__version__ = "3.2.4"
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

class BirthEngine( Engine ):
    """
    The BirthEngine adds a new component to the model.

    Only for Models that are Dynamic.
    The birth rate is governed by the growth-prior in the Dynamic.

    The member is kept when the logLikelihood > lowLhood.

    Attributes from Engine
    ----------------------
    walkers, errdis, maxtrials, slow, rng, report, phantoms, verbose

    Author       Do Kester.

    """

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, **kwargs ) :
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
        kwargs : for Engine
            "phantoms", "slow", "seed", "verbose"

        """
        super( ).__init__( walkers, errdis, copy=copy, **kwargs ) 

    def copy( self ):
        """ Return copy of this.  """
        return BirthEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "BirthEngine" )

    #  *********EXECUTE***************************************************
    def execute( self, kw, lowLhood, iteration=0 ):
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
            print( "Birth  ", walker.id, walker.parent, fmt( allp, max=None ), len( ftry ) )

        off = 0
        model = problem.model
        model.parameters = allp[:model.npars]

        while model is not None and not isinstance( model, Dynamic ) :
            off += model.npbase
            model = model._next

        nc = model.ncomp
        np = model.npbase

        if self.verbose > 4 :
            print( "       ", walker.id, nc, np, len( allp ), len( ftry ) )

        if not ( nc < model.growPrior.unit2Domain( self.rng.rand() ) and
                 model.grow( offset=off, rng=self.rng ) ):
            self.reportFailed()
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
                self.setWalker( kw, problem, ptry, Ltry, fitIndex=ftry )

                return dnp
            else :
                uval = self.rng.rand( dnp )
                ptry[klst] = self.unit2Domain( problem, uval, kpar=klst )

                self.reportReject()
                t += 1

#        print( "Birth   ", walker.id, fmt( ptry, max=None ) )

        self.reportFailed()

        return 0


