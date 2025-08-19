import numpy as numpy
import math
from . import Tools
from .Formatter import formatter as fmt

from .OrderEngine import OrderEngine

__author__ = "Do Kester"
__year__ = 2025
__license__ = "GPL3"
__version__ = "3.2.4"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Alpha"

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
#  *    2018 - 2025 Do Kester

class NearEngine( OrderEngine ):
    """
    The NearEngine searches the nearest neighbour (NN) for a point and
    goes there first.

    This is NOT a random engine as it mostly(??) steps uphill.

    It belongs to the class of generalized travelling salesman problems
    where the parameters of the problem is an ordered list.

    The walker is kept when the logLikelihood > lowLhood

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
        walkers : SampleList
            walkers to be diffused
        errdis : ErrorDistribution
            error distribution to be used
        copy : NearEngine
            to be copied
        kwargs : dict for Engine
            "phantoms", "slow", "seed", "verbose"

        """
        super( ).__init__( walkers, errdis, copy=copy, **kwargs )

#        if copy is None :
#            ## initialize nearest at -1
#            self.nearest = numpy.zeros_like( walkers[0].problem.parameters ) - 1
#        else :
#            self.nearest = copy.nearest



    def copy( self ):
        """ Return copy of this.  """
        return NearEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "NearEngine" )

    #  *********EXECUTE***************************************************
    def executeOnce( self, kw, lowLhood, dims=[0,1] ) :
        """
        Execute the NearEngine one time.

        TBC: This engine seems to take a lot of CPU.

        Parameters
        ----------
        kw : int
            id of walker to diffuse
        lowLhood : float
            lower limit in logLikelihood
        dims : list of 2 ints
            dimensions to process over
        """
        walker = self.walkers[kw]

        problem = walker.problem
        np = problem.npars
        param = walker.allpars

        if not hasattr( self, "nearest" ) :
            self.nearest = numpy.zeros_like( param ) - 1


        ks = self.rng.randint( np )
        ptry = numpy.roll( param, ks )

        xd = problem.xdata
        # k* are indices in the ptry list
        # n* are indices in the xdata list (eg. nearest)

        n0 = ptry[0]
        nsel = [n0,ptry[1]]
        if self.nearest[n0] < 0 :                                   # not yet calculated
            dmin = problem.distance( xd[nsel,:], [0,1] )[0]         # need only one distance
#            print( 0, fmt( nsel ), fmt( dmin ), fmt( dmin ) )
        
            kmin = 1
            for k in range( 2, np ) :                               # find nearest
                nsel[1] = ptry[k]
                d = problem.distance( xd[nsel,:], [0,1] )[0]
#                print( k, fmt( nsel ), fmt( d ), fmt( dmin ) )
                if d < dmin :
                    dmin = d
                    kmin = k
            self.nearest[n0] = ptry[kmin]                           # store for later use

        else :                                                      # it is stored
            np = self.nearest[n0]                                   # get the nearest
            kmin = numpy.where( ptry == np )[0][0]                  # find where NN is in ptry

        if kmin == 1 :                                              # it is already the NN 
            self.reportFailed()
            return 0

        ## make the NN the last one
        pkm = ptry[kmin]
        ptry[kmin:-1] = ptry[kmin+1:]
        ptry[-1] = pkm

        ptry = numpy.roll( ptry, -ks )

        Ltry = self.errdis.logLikelihood( problem, ptry )

        if self.verbose > 4 :
            print( "Near     ", ks, n0, kmin, fmt( lowLhood ), fmt( Ltry ) )
            print( fmt( param, max=None, format='%3d' ) )
            print( fmt( ptry, max=None, format='%3d' ) )
            print( fmt( self.nearest, max=None, format='%3d' ) )

        if Ltry >= lowLhood:
            self.reportSuccess( )
            self.setWalker( walker.id, problem, ptry, Ltry )
            t = 1

        else :
            self.reportReject()
            t = 0

        return t                        # nr of succesfull steps


