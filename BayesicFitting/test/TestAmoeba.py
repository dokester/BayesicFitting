# run with : python3 -m unittest TestAmoeba

import numpy as numpy
import unittest
from astropy import units
import math
import matplotlib.pyplot as plt
from numpy.testing import assert_array_almost_equal as assertAAE

from BayesicFitting import *

__author__ = "Do Kester"
__year__ = 2017
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

class TestAmoeba( unittest.TestCase ):
    """
    Test harness for AnnealingAmoeba class.

    Author       Do Kester

    """
    def __init__( self, name ):
        """     #  noise Normal distr.  """
        super( TestAmoeba, self ).__init__( name )

    def func1( self, xx ) :
        yy = 3.14
        p = 1.2
        for x in xx :
            x += p
            yy += x * x
            p *= p
        return yy

    def func2( self, xx ) :
        yy = 3.14
        p = 1.2
        a = 1.0 * math.pi
        for x in xx :
            x += p
            yy += x * ( x + 1 ) * ( 2 - numpy.cos( a * x ) )
            p *= p
        return yy

    #  **************************************************************
    def test1( self ):
        """     # 	test iterative slope fit  """
        print( "Testing AnnealingAmoeba" )

        xx = numpy.asarray( [3, -2], dtype=float )
        amb = AnnealingAmoeba( self.func1, xx, verbose=5 )

        Tools.printclass( amb )
        amb.minimize()
        Tools.printclass( amb )
        assertAAE( amb.xopt, [-1.2,-1.44], 2 )
        assertAAE( amb.fopt, self.func1( [-1.2,-1.44] ), 3 )

    #  **************************************************************
    def test2( self ):
        """     # 	test iterative slope fit  """
        print( "Testing AnnealingAmoeba with limits" )

        xx = numpy.asarray( [3, -2], dtype=float )
        amb = AnnealingAmoeba( self.func1, xx, limits=[[-1,0],[3,3]], reltol=1e-10,
            maxiter=100, verbose=5 )
        Tools.printclass( amb )
        self.assertRaises( ConvergenceError, amb.minimize )

        xx = numpy.asarray( [3, -2], dtype=float )
        amb = AnnealingAmoeba( self.func1, xx, limits=[[-1,0],[3,3]], reltol=1e-10, verbose=5 )

        amb.minimize()
        Tools.printclass( amb )
        assertAAE( amb.xopt, [-1.0,0.0] )
        assertAAE( amb.fopt, self.func1( [-1.0,0.0] ) )

    #  **************************************************************
    def plot3( self ) :
        self.test3( plot=True )

    def xxxtest3( self, plot=False ):
        """     # 	test iterative slope fit  """
        print( "Testing AnnealingAmoeba with limits" )

        if plot :
            x = numpy.linspace( -10, 10, 201, dtype=float )
            y = numpy.linspace( -10, 10, 201, dtype=float )
            self.plot( self.func2, x=x, y=y, contour=[5,10,15,20,30,40,60,80,100, 200] )

        xx = numpy.asarray( [3, -2], dtype=float )
        amb = AnnealingAmoeba( self.func2, xx, reltol=1e-10, verbose=5 )
        xopt = amb.minimize()

        print( amb.fopt, xopt )
        if plot :
            plt.plot( [xopt[1]], [xopt[0]], 'r+' )


        amb = AnnealingAmoeba( self.func2, xx, temp=10, seed=123456, verbose=100 )
        amb.minimize()

        xopt = amb.xopt
        print( amb.fopt, xopt )
        if plot :
            plt.plot( [xopt[1]], [xopt[0]], 'g+' )
            plt.show()

        assertAAE( amb.xopt, [-1.836, -2.0767], 3 )
        assertAAE( amb.fopt, 2.0221211, 5 )
# 2.02212110215 [-1.83671038 -2.07670877]



    def plot( self, func, x=None, y=None, contour=None ) :
        if x is None :
            x = numpy.linspace( -10, 10, 21 )
        if y is None :
            y = numpy.linspace( -10, 10, 41 )
        nx = len( x )
        ny = len( y )

        map = numpy.ndarray( (nx,ny), dtype=float )
        k0 = 0
        for yy in y :
            k1 = 0
            for xx in x :
                map[k1,k0] = func( [xx,yy] )
                k1 += 1
            k0 += 1

        if contour is None :
            contour = 10
        plt.contour( x, y, map, contour )








    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestAmoeba.__class__ )


if __name__ == '__main__':
    unittest.main( )

