import numpy as numpy
import math
from . import Tools
from .Formatter import formatter as fmt

from .OrderEngine import OrderEngine

__author__ = "Do Kester"
__year__ = 2022
__license__ = "GPL3"
__version__ = "3.0.0"
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
#  *    2018 - 2022 Do Kester

class LoopEngine( OrderEngine ):
    """
    The LoopEngine tries to unloop a crossing loop.

    Only for 2 dimensional TS problems.

    Input order :
         0  1  2  3
        15 14  5  4
         7  6 13 12
         8  9 10 11

    The loop crosses between (5,6) and (13,14). By switching the positions
    of 6 and 13, and reversing the loop in between, a better solution is
    reached (triangle inequality)

    output order:
         0  1  2  3
        15 14  5  4
        12 13  6  7
        11 10  9  8

    This is NOT a random engine as it only steps in the uphill direction.

    It belongs to the class of generalized travelling salesman problems
    where the parameters of the problem is an ordered list.

    The walker is kept when the logLikelihood > lowLhood

    Author       Do Kester.

    """
    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, seed=4213, verbose=0 ):
        """
        Constructor.

        Parameters
        ----------
        walkers : SampleList
            walkers to be diffused
        errdis : ErrorDistribution
            error distribution to be used
        copy : LoopEngine
            to be copied
        seed : int
            for random number generator

        """
        super( ).__init__( walkers, errdis, copy=copy, seed=seed, verbose=verbose )

    def copy( self ):
        """ Return copy of this.  """
        return LoopEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "LoopEngine" )

    #  *********EXECUTE***************************************************
    def executeOnce( self, kw, lowLhood, dims=[0,1] ) :
        """
        Execute the LoopEngine one time.

        Parameters
        ----------
        kw : int
            walker to diffuse
        lowLhood : float
            lower limit in logLikelihood
        dims : list of 2 ints
            dimensions to process over
        """
        walker = self.walkers[kw]

        problem = walker.problem
        np = problem.npars
        param = walker.allpars

        ## roll the parameter list to an arbitrary point
        ks = self.rng.randint( np )
        ptry = numpy.roll( param, ks )

        ## select last point and first point
        k1 = ptry[-1]
        k2 = ptry[0]
        x1, y1 = tuple( problem.xdata[k1,dims] )
        x2, y2 = tuple( problem.xdata[k2,dims] )
        if x1 == x2 :
            dims = [dims[1], dims[0]]           ## reverse dimensional order
            m1 = 0                              ## slope of point k1 to k2
        else :
            m1 = ( y2 - y1 ) / ( x2 - x1 )

        k4 = ptry[1]
        for t in range( 2, np - 1 ) :       ## skip adjacent points
            k3 = k4
            k4 = ptry[t]
            x3, y3 = tuple( problem.xdata[k3,dims] )
            x4, y4 = tuple( problem.xdata[k4,dims] )

            if x3 == x4 :
                xc = x3
                yc = y1 + m1 * ( xc - x1 )
                if Tools.isBetween( x1, xc, x2 ) and Tools.isBetween( y3, yc, y4 ) :
                    break

            else :
                m3 = ( y4 - y3 ) / ( x4 - x3 )
                xc = ( y3 - y1 + m3 * x3 - m1 * x1 ) / ( m3 - m1 )
                if Tools.isBetween( x1, xc, x2 ) and Tools.isBetween( x3, xc, x4 ) :
                    break

        else :
            self.reportReject()
            return 0


        ## reverse first t items
        ptry[:t] = ptry[t-1::-1]

        ptry = numpy.roll( ptry, -ks )

        Ltry = self.errdis.logLikelihood( problem, ptry )

        if self.verbose > 4 :
            print( "Loop     ", ks, t, fmt( lowLhood ), fmt( Ltry ) )
            print( fmt( param, max=None, format='%3d' ) )
            print( fmt( ptry, max=None, format='%3d' ) )

        if Ltry >= lowLhood:
            self.reportSuccess( )
            self.setWalker( walker.id, problem, ptry, Ltry )

        else :
            self.reportFailed()
            t = 0

        return t                        # nr of succesfull steps


