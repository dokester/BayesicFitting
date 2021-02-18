# run with : python3 -m unittest TestSampleList

import unittest
import numpy as numpy
import sys
from numpy.testing import assert_array_almost_equal as assertAAE
from astropy import units
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

class TestWalkerList( unittest.TestCase ):
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
    def testWalkerList( self ):
        print( "=========  WalkerListTest  =======================" )
        gm = GaussModel( )
        gm += PolynomialModel( 0 )

        problem = ClassicProblem( gm, xdata=self.x, ydata=self.noise )
#        errdis = GaussErrorDistribution( )

        lnZ = 1.234
        wl0 = WalkerList( problem, self.len, self.par, self.fi )
        self.assertTrue( wl0.logZ == 0 )
        self.assertTrue( wl0.info == 0 )
        self.assertTrue( wl0._count == self.len )
        self.assertTrue( wl0.iteration == 0 )

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

        wl = WalkerList( problem, self.len, ap, fi )
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
        wl.logZ = lnZ
        wl.info = 30
        self.assertTrue( wl.logZ == lnZ )
        self.assertTrue( wl.info == 30 )


    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestWalkerList.__class__ )



if __name__ == '__main__':
    unittest.main()


