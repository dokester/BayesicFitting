# run with : python3 -m unittest TestSampleList

import unittest
import numpy as numpy
import math

from BayesicFitting import *
from BayesicFitting import formatter as fmt

__author__ = "Do Kester"
__year__ = 2021
__license__ = "GPL3"
__version__ = "0.9"
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
#  *  2002 Do Kester

class Test( unittest.TestCase ):
    """
    Test harness.

    Author       Do Kester

    """

    # Define x independent variable
    x = numpy.asarray( [ -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0], dtype=float )

    # Define noise: random Gaussian noise sig=0.3
    noise = numpy.asarray( [ -0.000996, -0.046035,  0.013656,  0.418449,  0.0295155,  0.273705,
    -0.204794,  0.275843, -0.415945, -0.373516, -0.158084], dtype=float )
    wgt = numpy.asarray( [1,2,3,4,5,6,7,4,3,2,1], dtype=float )                 #  total 38
    par = numpy.asarray( [3,2,1,0.3], dtype=float )
    fi  = [0,1,2,3]
    len = 11

    #  **************************************************************
    def test1( self ) :
        print( "========= test1 ===========================" )

        wlist = WalkerList()
        self.assertTrue( wlist.firstIndex( 0 ) is None )

        w0 = Walker( 0, ClassicProblem(), self.par, self.fi )
        w0.logL = 0.0

        wlist = wlist.insertWalker( w0 )
        print( wlist, wlist._count )
        for w in wlist :
            print( w.id, w.logL )

        self.assertTrue( wlist.firstIndex( -1 ) == 0 )
        self.assertTrue( wlist.firstIndex( 1 ) == 1 )

        w1 = Walker( 1, ClassicProblem(), self.par, self.fi )
        w1.logL = 1.0

        wlist = wlist.insertWalker( w1 )
        print( wlist, wlist._count )
        for w in wlist :
            print( w.id, w.logL )

        numpy.random.seed( 123456 )
        lgl = numpy.random.rand( 10 ) * 1.4 - 0.2
        for k, l in enumerate( lgl ) :
            w2 = Walker( k+2, ClassicProblem(), self.par, self.fi )
            w2.logL = l

            wlist = wlist.insertWalker( w2 )
            print( wlist, wlist._count )

        logl = -math.inf
        for w in wlist :
            print( w.id, w.logL )
            self.assertTrue( logl <= w.logL )
            logl = w.logL

        wl1 = wlist.cropOnLow( -0.1 )
        self.assertTrue( len( wl1 ) == len( wlist ) )
        self.assertTrue( wl1._count == 12 )

        wl2 = wl1.cropOnLow( -0.01 )
        self.assertTrue( len( wl2 ) == 10 )
        self.assertTrue( wl2._count == 12 )

        wl3 = wl2.cropOnLow( 0 )
        self.assertTrue( len( wl3 ) == 9 )
        self.assertTrue( wl3._count == 12 )

        lgl = numpy.random.rand( 5 ) * 1.4
        for k, l in enumerate( lgl ) :
            w2 = Walker( wl3._count, ClassicProblem(), self.par, self.fi )
            w2.logL = l

            wl3 = wl3.insertWalker( w2 )
            print( wl3, wl3._count )

        logl = -math.inf
        for w in wl3 :
            print( w.id, w.logL )
            self.assertTrue( logl <= w.logL )
            logl = w.logL



    #  **************************************************************
    def testWalkerList( self ):
        print( "=========  WalkerListTest  =======================" )
        gm = GaussModel( )
        gm += PolynomialModel( 0 )

        problem = ClassicProblem( gm, xdata=self.x, ydata=self.noise )

        walker = Walker( 0, problem, self.par, self.fi )
        wl0 = WalkerList( walker=walker, ensemble=self.len )
        self.assertTrue( wl0._count == self.len )

        k = 0
        for s in wl0 :
            self.assertTrue( s.id == k )
            self.assertTrue( s.parent == -1 )
            self.assertTrue( isinstance( s.problem, ClassicProblem ) )
            self.assertTrue( s.logL == 0 )
            self.assertTrue( s.start == 0 )
            self.assertTrue( s.allpars[0] == 3 )
            self.assertTrue( s.allpars[1] == 2 )
            self.assertTrue( s.allpars[2] == 1 )
            self.assertTrue( s.allpars[3] == 0.3 )

            self.assertTrue( len( s.fitIndex ) == 4 )
            k += 1

        ap = numpy.append( gm.parameters, [0.5] )
        fi = numpy.asarray( [0,1,2,3,-1] )

        walker = Walker( 0, problem, self.par, self.fi )
        wl = WalkerList( walker=walker, ensemble=self.len )
        k = 0
        for s in wl:
            s.id = k + 1
            s.parent = ( k + 2 ) % self.len + 1
            s.allpars = ap + 0.01 * self.noise[k]
            s.logL = -1213.0 + self.x[k]
            print( s )
            print( "    allpars ", fmt( s.allpars ) )
            print( "    fitindx ", fmt( s.fitIndex ) )
            k += 1


    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestWalkerList.__class__ )



if __name__ == '__main__':
    unittest.main()


