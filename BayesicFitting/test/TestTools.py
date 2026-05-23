# run with : python3 -m unittest TestTools

import unittest
import numpy as numpy
import math
from datetime import date
from numpy.testing import assert_array_almost_equal as assertAAE


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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *  2006-2015 Do Kester (JAVA CODE)

class ATestClass( object ) :
    def __init__( self, copy=None ) :
        super( ATestClass, self ).__init__( )
        self.setatt( "n1", 4 )
        self.setatt( "n2", 4, type=int )
        self.setatt( "p1", 4.0, type=float, isnone=True )
        self.setatt( "p2", None, type=float, isnone=True )
        self.setatt( "ln", 4, type=int, islist=True )
        self.setatt( "lp", 4, type=float, islist=True )

        try :
            self.setatt( "ep", 4.78, type=int, islist=True )
            assert( False )
        except TypeError :
            assert( True )

    def setatt( self, name, value, type=None, islist=None, isnone=False ) :
        Tools.setAttribute( self, name, value, type=type, islist=islist, isnone=isnone )


class Test( unittest.TestCase ) :
    """
    Test harness for Fitter class.

    @author Do Kester

    """
    def testATestClass( self ) :
        atc = ATestClass()

        Tools.printclass( atc )

    def testSubclassof( self ) :

        self.assertTrue( Tools.subclassof( GaussModel, Model ) ) 
        self.assertTrue( Tools.subclassof( GaussModel, BaseModel ) )
        self.assertTrue( Tools.subclassof( GaussModel, NonLinearModel ) )
        self.assertTrue( Tools.subclassof( Model, object ) )

        self.assertFalse( Tools.subclassof( "GaussModel", BaseModel ) )
        self.assertFalse( Tools.subclassof( GaussModel, VoigtModel ) )
        self.assertFalse( Tools.subclassof( GaussModel, Fitter ) )
        self.assertFalse( Tools.subclassof( GaussModel, LinearModel ) )


    def testPrintClass( self ) :

        mdl = ArctanModel()
        x = numpy.linspace( -1, 1, 101 )
        Tools.printclass( mdl )
#        Tools.printclass( x )

        problem = ClassicProblem( model=mdl, xdata=x, ydata=x )
        Tools.printclass( problem )

        Tools.printclass( Fitter( x, mdl ) )

        prior = UniformPrior()
        Tools.printclass( prior )
        prior = UniformPrior( circular=True, limits=[0,2] )
        Tools.printclass( prior )
        prior = UniformPrior( limits=[0,2] )
        Tools.printclass( prior )

        mdl.setPrior( 0, prior )
        Tools.printclass( NestedSampler( problem=problem ) )

    def testIsBetween( self ) :
        self.assertTrue( Tools.isBetween( 1, 2, 3 ) )
        self.assertTrue( Tools.isBetween( 3, 2, 1 ) )

        self.assertFalse( Tools.isBetween( 2, 1, 3 ) )
        self.assertFalse( Tools.isBetween( 2, 3, 1 ) )


        self.assertTrue( Tools.isBetween( 2, 2, 3 ) )
        self.assertTrue( Tools.isBetween( 1, 2, 2 ) )
        self.assertTrue( Tools.isBetween( 2, 2, 1 ) )
        self.assertTrue( Tools.isBetween( 3, 2, 2 ) )
        self.assertTrue( Tools.isBetween( 2, 2, 2 ) )


    def testBaseModel( self ) :
        atc = BaseModel( 4 )
        atc.posIndex = [1,2]
        print( atc.posIndex )

#        atc.posIndex = 1.2

        try :
            atc.posIndex = 1.2
            print( atc.posIndex )
            self.assertTrue( False )
        except TypeError :
            self.assertTrue( True )

        try :
            atc.PosIndex = 1
            self.assertTrue( False )
        except AttributeError :
            self.assertTrue( True )

        try :
            atc.posIndex = None
            self.assertTrue( False )
        except TypeError :
            self.assertTrue( True )


    def testtoday( self ):
        print( date.today() )

    def testMakeNext( self ):
        print( "===== makeNext ===========================" )
        x = 2
        xgen = Tools.makeNext( x, 0 )
        for k in range( 10 ) :
            nx = next( xgen )
            print( k, nx )
            self.assertTrue( nx == 2 )
        xgen.close()

        x = [2,3,4,5]
        xgen = Tools.makeNext( x, 0 )
        for k in range( 10 ) :
            nx = next( xgen )
            print( k, nx )
            self.assertTrue( ( nx == (k+2) and k < 4 ) or nx == 5 )
        xgen.close()

        x = [2,3,4,5,6,7,8,9,10,11]
        xgen = Tools.makeNext( x, 0 )
        for k in range( 10 ) :
            nx = next( xgen )
            print( k, nx )
            self.assertTrue( nx == (k+2) )

        x = [2,3,4,5]
        xgen = Tools.makeNext( x, 2 )
        for k in range( 10 ) :
            nx = next( xgen )
            print( k, nx )
            self.assertTrue( ( nx == (k+4) and k < 6 ) or nx == 5 )
        xgen.close()

    def testFirstIndex( self ) :
        self.assertTrue( Tools.firstIndex( (1,2,3) ) == 0 )
        self.assertTrue( Tools.firstIndex( (1,2,3), condition=lambda x: x % 2 == 0 ) == 1 )
        self.assertRaises( StopIteration, Tools.firstIndex, (1,2,3), lambda x: x == 0 )

    def testLength( self ) :
        print( "===== length ================================" )
        x = 3.0
        self.assertTrue( Tools.length( x ) == 1 )
        x = [2,3,4,5]
        self.assertTrue( Tools.length( x ) == 4 )
        x = numpy.asarray( [2,3,4,5] )
        self.assertTrue( Tools.length( x ) == 4 )
        x.resize( 2, 2 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( Tools.length( x ) == 2 )
        x = [2,3,4,5]
        x = numpy.asarray( [x] )
        print( x, x.shape, x.__class__ )
        self.assertTrue( Tools.length( x ) == 1 )

    def testToArray( self ) :
        print( "===== toArray ================================" )
        x = Tools.toArray( 3 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 1 )
        x = Tools.toArray( 3.0 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 1 )
        x = Tools.toArray( [3,4,5,6] )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 1 )
        x = Tools.toArray( [3,4.5,5,6], ndim=1 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 1 )
        x = Tools.toArray( [3,4.5], ndim=2 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 2 )
        x = Tools.toArray( [3,4.5,5], ndim=3 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 2 )
        x = Tools.toArray( [[3,4.5],[6,5]], ndim=2 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 2 )

    def testAverage( self ) :
        print( "===== Average ================================" )
        xx = numpy.asarray( [10,20,30], dtype=float )
        aver = numpy.average( xx )
        stdv = numpy.std( xx )

        ax1, sx1 = Tools.average( xx )
        print( ax1, sx1 )
        self.assertTrue( ax1 == aver )
        self.assertTrue( sx1 == stdv )

        ax2, sx2 = Tools.average( xx, circular=[0,360] )
        print( ax2, sx2 )
        self.assertAlmostEqual( ax2, aver )
        self.assertAlmostEqual( sx2, stdv )

        ax3, sx3 = Tools.average( xx, circular=[-180,180] )
        print( ax3, sx3 )
        self.assertAlmostEqual( ax3, aver )
        self.assertAlmostEqual( sx3, stdv )

        xx -= 15
        xx[0] += 360
        aver -= 15

        ax1, sx1 = Tools.average( xx )
        print( ax1, sx1 )
        self.assertFalse( ax1 == aver )
        self.assertFalse( sx1 == stdv )

        ax2, sx2 = Tools.average( xx, circular=[0,360] )
        print( ax2, sx2 )
        self.assertAlmostEqual( ax2, aver )
        self.assertAlmostEqual( sx2, stdv )

        ax3, sx3 = Tools.average( xx, circular=[-180,180] )
        print( ax3, sx3 )
        self.assertAlmostEqual( ax3, aver )
        self.assertAlmostEqual( sx3, stdv )

        wgt = numpy.array( [0.7, 1.4, 0.7] )
        stdv = math.sqrt( numpy.average( [100, 0, 100], weights=wgt ) )
        print( aver, stdv )

        ax1, sx1 = Tools.average( xx )
        print( ax1, sx1 )
        self.assertFalse( ax1 == aver )
        self.assertFalse( sx1 == stdv )

        ax2, sx2 = Tools.average( xx, circular=[0,360], weights=wgt )
        print( ax2, sx2 )
        self.assertAlmostEqual( ax2, aver )
        self.assertAlmostEqual( sx2, stdv )

        ax3, sx3 = Tools.average( xx, circular=[-180,180], weights=wgt )
        print( ax3, sx3 )
        self.assertAlmostEqual( ax3, aver )
        self.assertAlmostEqual( sx3, stdv )

    def testNicenumber( self ) :
        self.oneNiceNumbertest( 0.00634, 0.006 )
        self.oneNiceNumbertest( -0.013, -0.01 )
        self.oneNiceNumbertest( 0.13, 0.1 )
        self.oneNiceNumbertest( 0, 0 )
        self.oneNiceNumbertest( 1.3, 1 )
        self.oneNiceNumbertest( 31.3, 30 )
        self.oneNiceNumbertest( 801.3, 800 )

        self.oneNiceNumbertest( -1.3, -1 )
        self.oneNiceNumbertest( -5.3, -5 )
        self.oneNiceNumbertest( -1001.3, -1000 )


    def oneNiceNumbertest( self, x, n ) :
        k = Tools.nicenumber( x )
        print( "nicenumber of %f is %f (%f)" % ( x, k, n ) )
        self.assertTrue( k == n )

    def testtoRect( self ):
        x = numpy.array( [0, 1, 2, 0.4] )
        y = numpy.roll( x, 2 )
        r,p = Tools.toSpher( ( x, y ) )

        a, b = Tools.toRect( r, phi=p )
        assertAAE( a, x )
        assertAAE( b, y )

        s, t = Tools.toSpher( a, b )
        assertAAE( s, r )
        assertAAE( t, p )

        xy = numpy.append( x, y ).reshape( (-1,2) )
        rp = Tools.toSpher( xy )
        print( xy )
        print( rp )
        ab = Tools.toRect( rp )
        print( ab )
        assertAAE( xy, ab )
#        assertAAE( rp[:,0], s )
#        assertAAe( rp[:,1], t )


    def testtoRect3D( self ):
        x = numpy.array( [0, 1, 2, 0.4] )
        y = numpy.roll( x, 2 )
        z = numpy.roll( y, 1 )
        r, p, t = Tools.toSpher3D( x, y, z )

        a, b, c = Tools.toRect3D( r, p, t )
        assertAAE( a, x )
        assertAAE( b, y )
        assertAAE( c, z )

        u, v, w = Tools.toSpher3D( a, b, c )
        assertAAE( u, r )
        assertAAE( v, p )
        assertAAE( w, t )


    def testArrow2d( self ) :


        z = numpy.array( [0,2,4], dtype=float )
        x = numpy.zeros( 3, dtype=float )
        y = numpy.zeros( 3, dtype=float )

        za, ya = Tools.arrow( z, y, scale=1.0 )
        print( fma( za ) )
        print( fma( ya ) )

        x = numpy.linspace( 4, 16, 5 )
        y = x * 1.2333
        xa, ya = Tools.arrow( x, y )
        qa = numpy.asarray( [0,1,4], dtype=int )
        qq = numpy.asarray( [0,1,1] )
        assertAAE( xa[qa], x[qq] ) 
        assertAAE( ya[qa], y[qq] ) 


        xa, ya, za = Tools.arrow( x, y, z, scale=1.0 )
        print( fma( xa ) )
        print( fma( ya ) )
        print( fma( za ) )

        return

    def testArrow3d( self ):

        rng = numpy.random.default_rng( seed=345678 )


        for k in range( 4 ) :
            x = rng.uniform( -1, 1, 2 )
            y = rng.uniform( -1, 1, 2 )
            z = rng.uniform( -1, 1, 2 )
            s = rng.uniform(  0, 1, 1 )[0] + 0.1
            self.arrow3d( x, y, z, s, plot=False )

    def arrow3d( self, x, y, z, s, plot=False ) :

        xa,ya,za = Tools.arrow( x, y, z, scale=s )

        print( fmt( x ) )
        print( fmt( y ) )
        print( fmt( z ) )
        print( fma( xa ) )
        print( fma( ya ) )
        print( fma( za ) )

        qa = numpy.array( [0,1,4,7] )
        qq = numpy.array( [0,1,1,1] )

        assertAAE( xa[qa], x[qq] ) 
        assertAAE( ya[qa], y[qq] ) 
        assertAAE( za[qa], z[qq] ) 

        if plot :
            import matplotlib.pyplot as plt
            ax = plt.figure( "arrow3d", figsize=[7,7] ).add_subplot( projection='3d' )
            ax.plot( x, y, z, 'r-' )
            ax.plot( x[0], y[0], z[0], 'ro' )
            ax.plot( x[1], y[1], z[1], 'r*' )
            ax.plot( xa, ya, za, 'k-' )

            sz = 0.5
            xx = [sz,-sz,-sz]
            yy = [-sz,sz,-sz]
            zz = [-sz,-sz,sz]
            ax.plot( xx, yy, zz, 'b,' )

            ax.set_box_aspect( [1,1,1] )
            plt.show()


    @classmethod
    def suite( cls ):
        return ConfiguredTestCase.suite( PriorTest.__class__ )

if __name__ == '__main__':
    unittest.main( )


