# run with : python3 -m unittest TestSalesmanProblem

import unittest
import os
import numpy as numpy
from astropy import units
from numpy.testing import assert_array_equal as assertAE
from numpy.testing import assert_array_almost_equal as assertAAE
import math
import matplotlib.pyplot as plt

from BayesicFitting import *
from BayesicFitting import formatter as fmt
from BayesicFitting import fma


__author__ = "Do Kester"
__year__ = 2018
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
#  *  2006 Do Kester

class Test( unittest.TestCase ):
    """
    Test harness for solving the SalesmanProblem with NestedSampler.

    Author       Do Kester

    """
    def __init__( self, name ):
        super( ).__init__( name )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

    def square( self, xdata, pars, roll=1 ) :
        rpar = numpy.roll( pars, -roll )
        return numpy.sum( numpy.square( xdata[pars] - xdata[rpar] ), 1 ) 


    def initProblem( self, np=10, random=False, weights=False, distance="euclid", scale=1 ):

        n2 = np * np
        if random :
            numpy.random.seed( 12345 )
            x0 = numpy.random.rand( n2 ) * np
            x1 = numpy.random.rand( n2 ) * np
        else :
            x0 = numpy.arange( n2, dtype=int ) % np
            x1 = numpy.arange( n2, dtype=int ) // np
        xdata = numpy.append( x0, x1 ).reshape( 2, n2 ).transpose()
        xdata = numpy.array( xdata, dtype=float )

        wgt = numpy.array( [2.0] * n2 ) if weights else None


        problem = SalesmanProblem( xdata, wgt, distance=distance, scale=scale )

#        numpy.set_printoptions( precision=3, suppress=True )
        return problem

    def test1( self ):
        print( "\n   SalesmanProblem Test Manhattan\n" )
        np = 10
        pars = numpy.arange( np*np, dtype=int )

        problem = self.initProblem( np=np, distance="manhattan" )
        print( problem )

        mdis = problem.minimumDistance( )
        print( "mindis  ", mdis )

        dis = problem.result( pars )
        sdis = numpy.sum( dis )
        print( fmt( dis, max=None ), fmt( sdis ) )
        self.assertAlmostEqual( sdis,  198, 6 )

        problem = self.initProblem( np=np, distance="manhattan", scale=3 )
        dis = problem.result( pars )
        sdis = numpy.sum( dis )
        print( fmt( dis, max=None ), fmt( sdis ) )
        self.assertAlmostEqual( sdis,  198/3, 6 )



    def test2( self ):
        print( "\n   SalesmanProblem Test Euclidic\n" )
        np = 10
        pars = numpy.arange( np*np, dtype=int )

        problem = self.initProblem( np=np )
        print( problem )

        mdis = problem.minimumDistance( )
        print( "mindis  ", mdis )

        dis = problem.result( pars )
        sdis = numpy.sum( dis )
        print( fmt( dis, max=None ), fmt( sdis ) )
        print( sdis, ( 90 + 9 * 9.05538514 + 12.72792206 ) )
        self.assertAlmostEqual( sdis, ( 90 + 9 * 9.05538514 + 12.72792206 ), 6 )

        problem = self.initProblem( np=np, weights=True )
        dis = problem.result( pars )
        sdis = numpy.sum( dis )
        print( fmt( dis, max=None ), fmt( sdis ) )
        print( sdis, 2*( 90 + 9 * 9.05538514 + 12.72792206 ) )
        self.assertAlmostEqual( sdis, 2 * ( 90 + 9 * 9.05538514 + 12.72792206 ), 6 )

    def test3( self ):
        print( "\n   SalesmanProblem Test Spherical\n" )
        np = 10
        pars = numpy.arange( np*np, dtype=int )

        problem = self.initProblem( np=np, distance="spheric" )
        problem.xdata[:,0] *= 36
        problem.xdata[:,1] -= 5
        problem.xdata[:,1] *= 18

        print( problem )

        print( problem.xdata.T )

        mdis = problem.minimumDistance( )
        print( "mindis  ", mdis )


        dis = problem.result( pars )
        sdis = numpy.sum( dis )
        print( fmt( dis, max=None ), fmt( sdis ) )
#        print( sdis, ( 90 + 9 * 9.05538514 + 12.72792206 ) )
#        self.assertAlmostEqual( sdis, ( 90 + 9 * 9.05538514 + 12.72792206 ), 6 )

        xd = [[0,0], [90,0], [100,0], [200,0], [270,0], [0,0],  
              [0,10], [0,30], [0,65], [111,90], [111,-10], [111,-90]]

        problem = SalesmanProblem( xd, distance="sheric" )

        print( "scale   ", problem.scale )

        dis = problem.result( pars[:12] ) *180 / math.pi
        
        print( fmt( dis, max=None ) )

        dd = [90, 10, 100, 70, 90, 10, 20, 35, 25, 100, 80, 90]
        assertAAE( dis, dd )

        xx = [[20,33], [43,30], [55,23], [120,33], [143,30], [155,23],
              [220,-33], [243,-30], [255,-23], [120,-33], [143,-30], [155,-23]]

        problem = SalesmanProblem( xx, distance="sheric" )

        dis = problem.result( pars[:12] ) *180 / math.pi
        
        print( fmt( dis, max=None ) )

        assertAAE( dis[0], dis[3] )
        assertAAE( dis[1], dis[4] )
        assertAAE( dis[3], dis[6] )
        assertAAE( dis[4], dis[7] )
        assertAAE( dis[6], dis[9] )
        assertAAE( dis[7], dis[10] )


    def test4( self ):
        print( "\n   SalesmanProblem Test User distance\n" )
        np = 10
        pars = numpy.arange( np*np, dtype=int )

        problem = self.initProblem( np=np, distance=self.square )
        print( problem )

        mdis = problem.minimumDistance( )
        print( "mindis  ", mdis )

        dis = problem.result( pars )
        sdis = numpy.sum( dis )
        print( fmt( dis, max=None ), fmt( sdis ) )
        self.assertAlmostEqual( sdis,  990, 6 )

        problem = self.initProblem( np=np, distance=self.square, scale=3 )
        dis = problem.result( pars )
        sdis = numpy.sum( dis )
        print( fmt( dis, max=None ), fmt( sdis ) )
        self.assertAlmostEqual( sdis,  990/3, 6 )


    def suite( cls ):
        return unittest.TestCase.suite( TestSalesmanProblem.__class__ )


if __name__ == '__main__':
    unittest.main( )


