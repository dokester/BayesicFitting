# run with : python3 -m unittest TestBasicSplinesModel

import unittest
import os
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt
from numpy.testing import assert_array_almost_equal as assertAAE
from numpy.testing import assert_array_equal as assertAE

from BayesicFitting import formatter as fmt
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
#  *  2006 Do Kester

class Test( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author       Do Kester

    """
    def __init__( self, name ):
        super( ).__init__( name )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

    def test1( self ) :
        print( "==== test 1 ====================" )

        x = numpy.linspace( 0, 10, 101, dtype=float )
        kn1 = numpy.asarray( [0,2,4,6,8,10], dtype=float )

        cc = ['k-', 'b-', 'r-', 'g-', 'c-', 'm-']
        for k in [0,1] :
            sm = BasicSplinesModel( knots=kn1, border=k )

            par = numpy.ones( sm.npars, dtype=float )

            y = sm.result( x, par )
            dy = sm.derivative( x, par )
            pt = sm.partial( x, par )

#            for i in range( 101 ) :
#                print( fmt( x[i] ), fmt( pt[i,:], max=None ) )

            if self.doplot :
                plt.plot( x, y, cc[k] )
                plt.plot( x, dy, cc[k+3] )
                for i in range( sm.npars ) :
                    plt.plot( x, pt[:,i] )

                plt.show()

    def test2( self ) :
        print( "==== test 2 ====================" )

        x = numpy.linspace( 0, 10, 101, dtype=float )
        kn1 = numpy.asarray( [0,1,4,5,6,7,8,10], dtype=float )

        cc = ['k-', 'b-', 'r-', 'g-', 'c-', 'm-']
        for k in [0,1] :
            sm = BasicSplinesModel( knots=kn1, border=k )

            par = numpy.ones( sm.npars, dtype=float )

            y = sm.result( x, par )
            dy = sm.derivative( x, par )
            pt = sm.partial( x, par )

#            for i in range( 101 ) :
#                print( fmt( x[i] ), fmt( pt[i,:], max=None ) )

            if self.doplot :
                plt.plot( x, y, cc[k] )
                plt.plot( x, dy, cc[k+3] )
                for i in range( sm.npars ) :
                    plt.plot( x, pt[:,i] )
                plt.plot( kn1, [-0.02]*8, 'r|' )
                plt.show()

    def test3( self ) :
        print( "==== test 3 BasicSplinesModel ====================" )

        x = numpy.linspace( 0, 100, 1001, dtype=float )

        kn = [0.000, 1.470, 16.049, 28.465, 36.358, 36.374, 36.829,
              59.589, 59.699, 70.193, 75.844, 88.918, 88.919,  100.000]

        sm = BasicSplinesModel( knots=kn )
        par = numpy.ones( sm.npars, dtype=float )

        y = sm.result( x, par )
        dy = sm.derivative( x, par )
        pt = sm.partial( x, par )

        fm = BasicSplinesModel( knots=kn, fixed={0:0.0, -1:0.0} )
        far = numpy.ones( fm.npars, dtype=float )

        print( fm.npbase, fm.npars, fm.npmax, len( far ) )
        print( fm.parlist )
        assertAE( fm.parlist, numpy.arange( 14, dtype=int ) + 1 )
        print( fm.fixed )
        assertAE( list( fm.fixed.keys() ), [0, 15] )


        fy = fm.result( x, far )
        fdy = fm.derivative( x, far )
        fpt = fm.partial( x, far )


        cc = ['k-', 'b-', 'r-', 'g-', 'c-', 'm-']
        if self.doplot :
            for k in kn :
                plt.plot( [k,k], [0,1], 'k:' )

            plt.plot( x, y, cc[0] )
            plt.plot( x, dy, cc[3] )
            for i in range( sm.npars ) :
                plt.plot( x, pt[:,i] )

            plt.plot( x, fy+2, cc[0] )
            plt.plot( x, fdy+2, cc[3] )
            for i in range( fm.npars ) :
                plt.plot( x, fpt[:,i]+2 )

            plt.ylim( -0.3, 3.3 )
            plt.show()

    def test4a( self ) :
        print( "==== test 4a SplinesModel ====================" )

        x = numpy.linspace( 0, 10, 1001, dtype=float )
        kn1 = numpy.linspace( 0, 10, 11 , dtype=float )

        sm1 = SplinesModel( knots=kn1 )
        par1 = numpy.ones( sm1.npars, dtype=float )

        for k in range( 100 ) :
            y1  = sm1.result( x, par1 + k )

    def test4b( self ) :
        print( "==== test 4b BasicSplinesModel ====================" )

        x = numpy.linspace( 0, 10, 1001, dtype=float )
        kn1 = numpy.linspace( 0, 10, 11 , dtype=float )

        sm1 = BasicSplinesModel( knots=kn1 )
        par1 = numpy.ones( sm1.npars, dtype=float )

        for k in range( 100 ) :
            y1  = sm1.result( x, par1 + k )


    def test4c( self ) :
        print( "==== test 4c BSplinesModel ====================" )

        x = numpy.linspace( 0, 10, 1001, dtype=float )
        kn1 = numpy.linspace( 0, 10, 11 , dtype=float )

        sm2 = BSplinesModel( knots=kn1 )
        par2 = numpy.ones( sm2.npars, dtype=float )

        for k in range( 100 ) :
            y1  = sm2.result( x, par2 + k )



    def test4( self ) :
        print( "==== test 4 ====================" )

        x = numpy.linspace( 0, 10, 101, dtype=float )
#        kn1 = numpy.asarray( [0,1,4,5,6,7,8,10], dtype=float )
        kn1 = numpy.linspace( 0, 10, 11 , dtype=float )

        cc = ['k-', 'b-', 'r-', 'g-', 'c-', 'm-']

        sm1 = BasicSplinesModel( knots=kn1 )
        sm2 = BSplinesModel( knots=kn1 )

        print( sm1.npars, sm2.npars )
        self.assertTrue( sm1.npars == sm2.npars )

        par1 = numpy.ones( sm1.npars, dtype=float )
        par2 = numpy.ones( sm2.npars, dtype=float )

        y1  = sm1.result( x, par1 )
        dy1 = sm1.derivative( x, par1 )
        pt1 = sm1.partial( x, par1 )

        y2  = sm2.result( x, par2 )
        dy2 = sm2.derivative( x, par2 )
        pt2 = sm2.partial( x, par2 )

        assertAAE( y1, y2 )
        assertAAE( dy1, dy2 )
        assertAAE( pt1, pt2 )

        if self.doplot :
            k = 0
            plt.plot( x, y1, cc[k] )
            plt.plot( x, y2 + 2, cc[k] )
            for i in range( sm1.npars ) :
                plt.plot( x, pt1[:,i] )
            for i in range( sm2.npars ) :
                plt.plot( x, pt2[:,i] + 2 )
            plt.plot( x, dy1, cc[k+3] )
            plt.plot( x, dy2 + 2, cc[k+3] )

            plt.show()

    def test6c( self ) :
        kn = numpy.asarray( [-10,10], dtype=float )
        for k in range( 5 ) :
            self.bstest5( kn, order=k )

    def test6d( self ) :
        kn = numpy.asarray( [-10, 0, 10], dtype=float )
        self.bstest5( kn )

    def bstest5( self, kn, order=3 ) :
        print( "==== test 6 ====================" )

        x = numpy.linspace( min(kn), max(kn), 101, dtype=float )

        n = 0
        cc = ['k-', 'b-', 'r-', 'g-', 'c-', 'm-']

        sm = BasicSplinesModel( knots=kn, order=order )
        par = numpy.ones( sm.npars, dtype=float )

        ysm = sm.result( x, par )
        pts = sm.partial( x, par )

        print( fmt( numpy.sum( pts, 0 ), max=None ) )

        if self.doplot :

            for k in kn :
                plt.plot( [k,k], [0,1], 'k:' )

            plt.plot( x, ysm, 'k-' )
            for i in range( sm.npars ) :
                plt.plot( x, pts[:,i], cc[3] )

            plt.show()

    def test6a( self ) :
        kn = numpy.linspace( 0, 10, 11, dtype=float )
        self.bstest6( kn )

    def test6a0( self ) :
        kn = numpy.linspace( 0, 10, 11, dtype=float )
        self.bstest6( kn, order=0 )

    def test6a1( self ) :
        kn = numpy.linspace( 0, 10, 11, dtype=float )
        self.bstest6( kn, order=1 )

    def test6a2( self ) :
        kn = numpy.linspace( 0, 10, 11, dtype=float )
        self.bstest6( kn, order=2 )

    def test6a4( self ) :
        kn = numpy.linspace( 0, 10, 11, dtype=float )
        self.bstest6( kn, order=4 )

    def test6b( self ) :
        kn = numpy.asarray( [0,1,2,5,6,8,10], dtype=float )
        self.bstest6( kn )


    def bstest6( self, kn, order=3 ) :
        print( "==== test 6 ====================" )

        x = numpy.linspace( min(kn), max(kn), 101, dtype=float )

        n = 0
        cc = ['k-', 'b-', 'r-', 'g-', 'c-', 'm-']

        sm = BasicSplinesModel( knots=kn, order=order )
        bm = BSplinesModel( knots=kn, order=order )
        par = numpy.ones( bm.npars, dtype=float )

        ysm = sm.result( x, par )
        pts = sm.partial( x, par )

        ybm = bm.result( x, par )
        ptb = bm.partial( x, par )

        print( fmt( numpy.sum( pts, 0 ), max=None ) )
        print( fmt( numpy.sum( ptb, 0 ), max=None ) )

        if self.doplot :

            for k in kn :
                plt.plot( [k,k], [0,1], 'k:' )

            plt.plot( x, ybm, 'b-' )
            plt.plot( x, ysm + 1.1, 'k-' )
            for i in range( bm.npars ) :
#                plt.plot( x, ptb[:,i] - pts[:,i], cc[2] )
                plt.plot( x, ptb[:,i], cc[2] )
                plt.plot( x, pts[:,i]+1.1, cc[3] )

            plt.show()

        assertAAE( ysm, ybm )
        if order > 0 :
            assertAAE( pts, ptb )

    def test7a0( self ) :
        kn = numpy.linspace( 0, 10, 11, dtype=float )
        self.bstest7( kn, order=0 )

    def test7a1( self ) :
        kn = numpy.linspace( 0, 10, 11, dtype=float )
        self.bstest7( kn, order=1 )

    def test7a2( self ) :
        kn = numpy.linspace( 0, 10, 11, dtype=float )
        self.bstest7( kn, order=2 )

    def test7a( self ) :
        kn = numpy.linspace( 0, 10, 11, dtype=float )
        self.bstest7( kn )

    def test7a4( self ) :
        kn = numpy.linspace( 0, 10, 11, dtype=float )
        self.bstest7( kn, order=4 )

    def test7b( self ) :
        kn = numpy.asarray( [0,1,2.1,3,4.4,5,6,8,10], dtype=float )
        self.bstest7( kn )


    def bstest7( self, kn, order=3, plot=False ) :
        print( "==== test 7 ========= order = %d ===========" % ( order ) )

        x = numpy.linspace( 0, 10, 101, dtype=float )

        n = 0
        cc = ['k-', 'b-', 'r-', 'g-', 'c-', 'm-']

        sm = BasicSplinesModel( knots=kn, order=order, border=1 )
        spar = numpy.ones( sm.npars, dtype=float )
        bpar = numpy.linspace( 0.0, 1.0, sm.npars, dtype=float )

        ysm = sm.result( x, spar )
        pts = sm.partial( x, spar )

        ybm = sm.result( x, bpar )
        ptb = sm.partial( x, bpar )

        print( fmt( numpy.sum( pts, 0 ), max=None ) )
        print( fmt( numpy.sum( ptb, 0 ), max=None ) )

        if self.doplot :

            for k in kn :
                plt.plot( [k,k], [0,1], 'k:' )

            plt.plot( x, ybm + 1.1, 'k-' )
            plt.plot( x, ysm, 'k-' )
            for i in range( sm.npars ) :
                plt.plot( x, ptb[:,i] + 1.1, cc[i%6] )
                plt.plot( x, pts[:,i], cc[i%6] )

            plt.show()

        assertAAE( ysm, 1.0 )

    def test8a0( self ) :
        self.bstest8( order=0 )

    def test8a1( self ) :
        self.bstest8( order=1 )

    def test8a2( self ) :
        self.bstest8( order=2 )

    def test8a( self ) :
        self.bstest8( )

    def test8a4( self ) :
        self.bstest8( order=4 )

    def bstest8( self, order=3 ) :
        print( "==== test 8 ========= order %d ===========" % ( order ) )

        x = numpy.linspace( 0, 10, 101, dtype=float )
        cc = ['k-', 'b-', 'r-', 'g-', 'c-', 'm-']

        for k in range( 2, 7 ) :
            knots = numpy.linspace( 0, 10, k, dtype=float )
            print( "Knots  ", fmt( knots, max=None ) )

            bm = BasicSplinesModel( knots=knots, order=order )
            par = numpy.ones( bm.npars, dtype=float )

            ybm = bm.result( x, par )
            ptb = bm.partial( x, par )

            print( fmt( numpy.sum( ptb, 0 ), max=None ) )

            if self.doplot :
                off = 1.1 * ( k - 2 )
                plt.plot( x, ybm + off, 'b-' )
                for i in range( bm.npars ) :
                    plt.plot( x, ptb[:,i] + off, cc[i%6] )

        if self.doplot :
            plt.ylim( -0.1, 6 )
            plt.show()


    def test9( self ) :
        print( "==== test ========= fixed parameters ==========="  )

        fm = BasicSplinesModel( nrknots=8, min=0, max=10, fixed={0:0.0, -1:0.0} )

        print( fm.parlist )
        assertAE( fm.parlist, numpy.arange( 8, dtype=int ) + 1 )
        print( fm.fixed )
        assertAE( list( fm.fixed.keys() ), [0, 9] )

        fm = BasicSplinesModel( nrknots=8, min=0, max=10, fixed={0:0, 1:0, -2:0, -1:0} )

        print( fm.parlist )
        assertAE( fm.parlist, numpy.arange( 6, dtype=int ) + 2 )
        print( fm.fixed )
        assertAE( list( fm.fixed.keys() ), [0, 1, 8, 9] )


    def test10( self ) :
        print( "   Test BasicSplinesModel      " )

        mdl = BasicSplinesModel( knots=[-2.0, 2.1] )

        print( "   Test DynamicModel      " )
        mdl = BasicSplinesModel( knots=[-2.0, 0.0, 2.0] )


    def plot1( self ):
        x = numpy.linspace( 0, 10, 101, dtype=float )
        y = numpy.sin( x )
        kn1 = numpy.linspace( 0, 10, 11, dtype=float )
        sm1 = BasicSplinesModel( knots=kn1 )
        ftr = Fitter( x, sm1 )
        par1 = ftr.fit( y )
        print( fmt( par1, max=None ) )

        plt.plot( x, y, 'k.' )
        plt.plot( x, sm1.result( x, par1 ) )


        plt.show()



    def suite( cls ):
        return unittest.TestCase.suite( Test.__class__ )


if __name__ == '__main__':
    unittest.main( )


