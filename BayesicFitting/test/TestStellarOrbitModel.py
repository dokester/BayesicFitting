# run with : python3 -m unittest TestModels.TestModels.testGaussModel

import unittest
import numpy as numpy
from astropy import units
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

    def plot1( self ) :
        self.test1( plot=True )

    def test1( self, plot=False ):
        x  = numpy.linspace( 0, 1400, 1401, dtype=float )
        print( "****** STELLAR ORBIT test 1 ***************" )
        m = StellarOrbitModel( )
        self.assertTrue( m.getNumberOfParameters( ) == 7 )
        self.assertTrue( m.npbase == 7 )

        # eccen, semimajor, inclin, ascnodepos, ascnodelong, period, periastron
        p = [0.67, 13, 1500.0, 0.0, 0.0, 0.0, 0.0]
        if plot :
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

#        stdModeltest( m, p, plot=plot )

    def test2( self ) :
        x  = numpy.linspace( 0, 1400, 7, dtype=float )
        print( "****** STELLAR ORBIT test 1 ***************" )
        m = StellarOrbitModel( )

        # eccen, semimajor, period, periastron, inclin, ascnodepos, ascnodelong
        p = [0.67, 13, 1200.0, 0.1, 0.2, 0.3, 0.4]

        self.dtest( x, m, p )

        print( "Make copy of model: ", m )
        mc = m.copy()

        self.dtest( x, mc, p )



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


