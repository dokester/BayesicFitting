# run with : python3 -m unittest TestFootbalModel.Test.test1

import unittest
import os
import numpy as numpy
#from astropy.modeling.models import Gaussian1D
#from astropy.modeling.models import Polynomial1D
import matplotlib.pyplot as plt

from numpy.testing import assert_array_almost_equal as assertAAE
from numpy.testing import assert_array_equal as assertAE

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


class Test( unittest.TestCase ):
    """
    Test harness for Models

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )


    def test1( self ):
        print( "******Football MODEL 1***********************" )

        m1 = FootballModel( 3, complexity=1  )

        p1 = numpy.asarray( [10, 6.0, 3.0], dtype=float )
        xdata = numpy.asarray( [[0,1], [1,2], [2,0]], dtype=int )

        print( fmt( p1 ) )

        r1 = m1.result( xdata, p1 )
        self.rprint( xdata, r1 )
        print( m1.lastndout, m1.ndout )

        m5 = FootballModel( 3 )

        p5 = numpy.asarray( [10, 0, 1, 1, 1, 6, 0, 1, 1, 1, 3.0, 0, 1, 1, 1], dtype=float )

        print( fmt( p5, max=None )  )

        r5 = m5.result( xdata, p5 )
        self.rprint( xdata, r5 )

        assertAE( r1, r5 )

        k = [1,6,11]
        p5[k] = [0.5, 0.7, 0.9]

        r5 = m5.result( xdata, p5 )
        print( fmt( p5, max=None )  )
        self.rprint( xdata, r5 )

        k = [2,7,12]
        p5[k] = [1.5, 0.7, 1.0]

        r5 = m5.result( xdata, p5 )
        print( fmt( p5, max=None )  )
        self.rprint( xdata, r5 )

    def rprint( self, x, r ) :
        for k in range( x.shape[0] ) :
            print( "%d - %d result %8.3f - %8.3f" % ( x[k,0], x[k,1], r[k,0], r[k,1] ) ) 
        


    def test2( self ):
        print( "******FOOTBALL MODEL 2***********************" )

        N = 10                                          # nr of teams
        M = N // 2                                      # nr of matches
        xdata = numpy.arange( N, dtype=int ).reshape( (5,2) )
        print( xdata )
        mf = numpy.linspace( 0.4, 1.6, M )

        print( "== midfield ====" )

        m3 = FootballModel( N, complexity=3 )
        p3 = numpy.asarray( [10, 0.5, 1] * N, dtype=float )

        p3[2::6] = mf
        print( "p3   ", p3.reshape( (-1,3) ) )
        r3 = m3.result( xdata, p3 )
        rh = r3[:,0]
        ra = r3[:,1]

        print( "home ", fmt( rh ) )
        print( "away ", fmt( ra ) )

        if self.doplot :
            plt.plot( mf, rh, 'k.' )
            plt.plot( mf, ra, 'r.' )

        print( "== home advantage ====" )

        m4 = FootballModel( N, complexity=4 )
        p4 = numpy.asarray( [10, 0.5, 1, 1] * N, dtype=float )

        p4[7::8] = mf
        print( "p4   ", p4.reshape( (-1,4) ) )
        r4 = m4.result( xdata, p4 )
        rh = r4[:,0]
        ra = r4[:,1]

        if self.doplot :
            plt.plot( mf, rh, 'k-' )
            plt.plot( mf, ra, 'r-' )


    def test5( self ):
        print( "******FOOTBALL MODEL 5***********************" )

        N = 10                                          # nr of teams
        M = N // 2                                      # nr of matches
        xdata = numpy.arange( N, dtype=int ).reshape( (5,2) )
        print( xdata )
        mf = numpy.linspace( 0.4, 1.6, M )

        print( "== strategy ====" )

        m5 = FootballModel( N, complexity=5 )
        p5 = numpy.asarray( [10, 0.5, 1, 1, 1] * N, dtype=float )

        p5[4::10] = mf
        print( "p5   \n", p5.reshape( (-1, 5) ) )
        r5 = m5.result( xdata, p5 )
        rh = r5[:,0]
        ra = r5[:,1]

        print( "home ", fmt( rh ) )
        print( "away ", fmt( ra ) )
        if self.doplot :
            plt.plot( mf, rh, 'k-.' )
            plt.plot( mf, ra, 'r-.' )

        p5 = numpy.asarray( [10, 0.5, 1, 1, 1] * N, dtype=float )

        c5 = m5.copy()

        p5[2::10] = 1.2
        p5[9::10] = mf
        print( "p5   \n", p5.reshape( (-1, 5) ) )
        r5 = c5.result( xdata, p5 )
        rh = r5[:,0]
        ra = r5[:,1]

        if self.doplot :
            plt.plot( mf, rh, 'b-.' )
            plt.plot( mf, ra, 'g-.' )
            plt.show()

        for k in range( 0, 5*N, 6 ) :
            print( k, c5.getParameterName( k ), m5.getParameterUnit( k ) )



    def test3( self ):
        print( "******FOOTBALL MODEL test 3***********************" )

        xdata = numpy.asarray( [[0,1], [1,2]], dtype=int )


        numpy.random.seed( 123456 )
        for k in range( 1, 6 ) :
            print( "------- Complexity %d --------------" % k )
            print( "k0   ", xdata[:,0] * k )
            print( "k1   ", xdata[:,1] * k )
            mdl = FootballModel( 3, complexity=k )

            par = numpy.random.rand( 3 * k )
            kk = numpy.asarray( range( 0, 3*k, k ) )
            par[kk]*= 10
            for i in range( 2, k ) :
                par[kk+i] *= 2
            print( k, fmt( par, max=None ) )
            
            res = mdl.result( xdata, par )
            self.rprint( xdata, res )
            print( res )   

            
            part = mdl.partial( xdata, par )
            print( "partial" )
            print( fmt( part, max=None ) )
            nump = mdl.strictNumericPartial( xdata, par )
            print( "numeric" )
            print( fmt( nump, max=None ) )
            assertAAE( part, nump )

    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestUserModel.__class__ )

if __name__ == '__main__':
    unittest.main( )


