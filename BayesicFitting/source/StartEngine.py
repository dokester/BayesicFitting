import numpy as numpy
import math
from .Formatter import formatter as fmt
from .Dynamic import Dynamic
from .Engine import Engine

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

class StartEngine( Engine ):
    """
    StartEngine generates a random trial sample.

    It is used to initialize the set of trial samples.

    Attributes from Engine
    ----------------------
    walkers, errdis, maxtrials, nstep, slow, rng, report, phantoms, verbose

    Author       Do Kester.

    """
    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, **kwargs ):
        """
        Constructor.

        Parameters
        ----------
        walkers : WalkerList
            list of walkers to be initiated
        errdis : ErrorDistribution
            error distribution to be used
        copy : StartEngine
            engine to be copied

        """
        super( ).__init__( walkers, errdis, copy=copy, **kwargs )

    def copy( self ):
        """ Return copy of this.  """
        return StartEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "StartEngine" )

    #  *********EXECUTE***************************************************
    def execute( self, kw, lowLhood ):
        """
        Execute the engine by a random selection of the parameters.

        Parameters
        ----------
        kw : int
            index in the WalkerList
        lowLhood : float
            lower limit in logLikelihood

        Returns
        -------
        int : the number of successfull moves

        """
        walker = self.walkers[kw]
        problem = walker.problem
        model = problem.model
        fitIndex = walker.fitIndex
        ptry = walker.allpars.copy()

        nhyp = self.errdis.nphypar
        npar = len( ptry ) - nhyp
        onp = problem.npars

        maxtrials = self.maxtrials
        if hasattr( self.errdis, "constrain" ) and callable( self.errdis.constrain ) :
            maxtrials *= 100

        if self.verbose > 4 :
            print( "Start   ", model.shortName(), fmt( model.npars ) )

        ktry = 0
        while True :

            if model.isDynamic() :
                np0 = model.npars
                off = 0

                ## find the model in the chain that is actually dynamic
                while model is not None and not isinstance( model, Dynamic ) :
                    off += model.npbase
                    model = model._next

                npbase = model.npbase
                ## Grow the dynamic model a number of times according to growPrior
                while ( model.ncomp < model.growPrior.unit2Domain( self.rng.rand() ) and
                        model.grow( offset=off, rng=self.rng ) ) :
                    np1 = model.npars
                    dnp = np1 - np0
                    fitIndex = model.alterFitindex( fitIndex, npbase, dnp, off )
                    npbase = model.npbase
                    np0 = np1

                if self.verbose > 4 :
                    print( "Dyn  ", model.ncomp, model.npars )
                    print( fmt( fitIndex, max=None ) )


                ptry = numpy.zeros( npar + np0 - onp, dtype=float )
                if nhyp > 0 :
                    ptry = numpy.append( ptry, walker.allpars[-nhyp:] )

            uval = self.rng.rand( len( fitIndex ) )

            ptry[fitIndex] = self.unit2Domain( problem, uval, kpar=fitIndex )

            logL = self.errdis.logLikelihood( problem, ptry )

            if self.verbose > 4 :
                print( fmt( ptry, max=None ) )
                print( "logL   ", fmt( logL ) )

            if math.isfinite( logL ) :
                break
            elif ktry > ( maxtrials + walker.id ) :
                raise RuntimeError( "Cannot find valid starting solutions at walker %d" % walker.id )
            else :
                ktry += 1

        self.setWalker( walker.id, problem, ptry, logL, fitIndex=fitIndex )

        return len( fitIndex )



