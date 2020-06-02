# run with : python3 -m unittest TestModels.TestModels.testGaussModel

import unittest
import os
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt
import warnings

from numpy.testing import assert_array_almost_equal as assertAAE
from StdTests import stdModeltest

from BayesicFitting import *
from BayesicFitting import formatter as fmt

__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

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

class TestStellarOrbitModel( unittest.TestCase ):
    """
    Test harness for Stellar Orbit Model

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )


    def test1( self ):
        x  = numpy.linspace( 0, 1400, 1401, dtype=float )
        print( "****** STELLAR ORBIT test 1 ***************" )
        m = StellarOrbitModel( spherical=False )
        self.assertTrue( m.getNumberOfParameters( ) == 7 )
        self.assertTrue( m.npbase == 7 )

        # eccen, semimajor, inclin, ascnodepos, ascnodelong, period, periastron
        p = [0.67, 13, 1500.0, 0.0, 0.0, 0.0, 0.0]
        if self.doplot :
            plt.plot( [0], [0], 'k.' )

            hpi = 1.5
            p = [0.67, 13, 1500.0, 0.0, 0.0, 4.0, 0.0]
            for k in range( 5 ) :
                y = m.result( x, p )
                plt.plot( y[:,0], y[:,1], 'k-' )
                plt.plot( y[0,0], y[0,1], 'k.' )
                p[3] += 0.4


            p = [0.67, 13, 1500.0, 0.0, 0.0, 0.0, 0.0]
            for k in range( 5 ) :
                y = m.result( x, p )
                plt.plot( y[:,0], y[:,1], 'r-' )
                plt.plot( y[0,0], y[0,1], 'r.' )
                p[4] += 0.7


            p = [0.67, 13, 1500.0, 0.0, 1.0, 0.0, 0.0]
            for k in range( 5 ) :
                y = m.result( x, p )
                plt.plot( y[:,0], y[:,1], 'g-' )
                plt.plot( y[0,0], y[0,1], 'g.' )
                p[6] += 0.4

            p = [0.67, 13, 1500.0, 0.0, hpi, 0.0, 0.0]
            for k in range( 5 ) :
                y = m.result( x, p )
                plt.plot( y[:,0], y[:,1], 'b-' )
                plt.plot( y[0,0], y[0,1], 'b.' )
                p[5] += 0.4

            plt.show()


    def test2( self ) :
        x  = numpy.linspace( 0, 1400, 7, dtype=float )
        print( "****** STELLAR ORBIT test 2 ***************" )
        m = StellarOrbitModel( )

        # eccen, semimajor, period, periastron, inclin, ascnodepos, ascnodelong
        p = [0.67, 13, 1200.0, 0.1, 0.2, 0.3, 0.4]

        self.dtest( x, m, p )

        print( "Make copy of model: ", m )
        mc = m.copy()

        self.dtest( x, mc, p )

    def test3( self ) :
        x  = numpy.linspace( 0, 1400, 7, dtype=float )
        print( "****** STELLAR ORBIT test 3 ***************" )
        m = StellarOrbitModel( spherical=False )

        # eccen, semimajor, period, periastron, inclin, ascnodepos, ascnodelong
        p = [0.67, 13, 1200.0, 0.1, 0.2, 0.3, 0.4]

        self.dtest( x, m, p )

        print( "Make copy of model: ", m )
        mc = m.copy()

        self.dtest( x, mc, p )

    def test4( self ) :

        print( "****** STELLAR ORBIT test 4 ***************" )
        m = StellarOrbitModel( spherical=False )

        p = math.pi
        rho = numpy.array( [0, 1, 1, 1, 1, 3, 2.4] )
        phi = numpy.array( [0, 0, p, p/2, p/4, p/6, 4.3] )
        rp0 = numpy.append( rho, phi ).reshape(2,-1).transpose()

        xy0 = m.toRect( rp0 )

        print( "x0   ", fma( xy0[:,0] ) )
        print( "y0   ", fma( xy0[:,1] ) )

        rp1 = m.toSpher( xy0 )

        print( "r1   ", fma( rp1[:,0] ) )
        print( "t1   ", fma( rp1[:,1] ) )

        xy1 = m.toRect( rp1 )

        print( "x1   ", fma( xy1[:,0] ) )
        print( "y1   ", fma( xy1[:,1] ) )

        rp2 = m.toSpher( xy1 )

        print( "r2   ", fma( rp2[:,0] ) )
        print( "t2   ", fma( rp2[:,1] ) )

        xy2 = m.toRect( rp2 )

        print( "x2   ", fma( xy2[:,0] ) )
        print( "y2   ", fma( xy2[:,1] ) )

        rp3 = m.toSpher( xy2 )

        print( "r3   ", fma( rp3[:,0] ) )
        print( "t3   ", fma( rp3[:,1] ) )


#        assertAAE( xy0, xy1 )
        assertAAE( xy1, xy2 )
        assertAAE( rp1, rp2 )
        assertAAE( rp2, rp3 )


    def dtest( self, x, m, p ) :

        dfdx = m.baseDerivative( x, p )

        xp = x + 0.0001
        xm = x - 0.0001

        yp = m.result( xp, p )
        ym = m.result( xm, p )

        numx = ( yp - ym ) / 0.0002

        print( "dx0   ", fma( dfdx[:,0] ) )
        print( "nm0   ", fma( numx[:,0] ) )
        print( "dx1   ", fma( dfdx[:,1] ) )
        print( "nm1   ", fma( numx[:,1] ) )
        assertAAE( dfdx, numx )

        part0, part1 = m.basePartial( x, p )
        for k in range( 7 ) :
            pp = p[:]
            pp[k] += 0.0001
            pm = p[:]
            pm[k] -= 0.0001
            yp = m.result( x, pp )
            ym = m.result( x, pm )
            print( "parameter ", k, "  ", m.parNames[k] )

            num0 = ( yp[:,0] - ym[:,0] ) / 0.0002
            num1 = ( yp[:,1] - ym[:,1] ) / 0.0002
            print( "dp0   ", fma( part0[:,k] ) )
            print( "nm0   ", fma( num0 ) )
            print( "dp1   ", fma( part1[:,k] ) )
            print( "nm1   ", fma( num1 ) )
            assertAAE( part0[:,k], num0 )
            assertAAE( part1[:,k], num1 )


    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestStellarOrbitModel.__class__ )

if __name__ == '__main__':
    unittest.main( )


