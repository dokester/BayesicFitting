# run with : python3 -m unittest TestPrior
# or :       python3 -m unittest TestPrior.Test.testUniformPrior

import unittest
import numpy as numpy
from numpy.testing import assert_array_almost_equal as assertAAE
import math

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

class Test( unittest.TestCase ) :
    """
    Test harness for Fitter class.

    @author Do Kester

    """
    def testUniformPrior( self ):

        print( "===== Uniform Prior Tests ==========================\n" )
#        self.assertWarns( UserWarning, UniformPrior )
        prior = UniformPrior( )
        print( prior )
        self.assertTrue( prior._lowDomain == -math.inf )
        self.assertTrue( prior._highDomain == +math.inf )
        self.assertFalse( prior.isBound() )
#        self.assertRaises( AttributeError, prior.unit2Domain, 0.0 )
#        self.assertRaises( AttributeError, prior.domain2Unit, 0.0 )
#        self.assertRaises( AttributeError, prior.result, 1.0 )

        prior.setLimits( [0,5] )
        print( "lowlim %f  highlim %f range %f"%( prior.lowLimit, prior.highLimit, prior._urng ) )
        self.assertTrue( prior._urng == prior.getIntegral() )
        print( prior )

        values = {0.0:0.0, 0.5:2.5, 1.0:5.0 }
        self.stdTestPrior( prior, values=values )

        cp = prior.copy( )
        print( cp )
        self.stdTestPrior( cp, values=values )

        prior = UniformPrior( numpy.asarray( [6.,48.] ) )
        print( prior )
        values = {0.0:6, 0.5:27, 1.0:48 }
        self.stdTestPrior( prior, values=values )

        print( prior.domain2Unit( prior.unit2Domain(0.1) ) )
        print( prior.domain2Unit( prior.unit2Domain(0.3) ) )
        print( prior.domain2Unit( prior.unit2Domain(0.8) ) )
        self.assertAlmostEqual( prior.domain2Unit( prior.unit2Domain( 0.1 ) ), 0.1 )
        self.assertAlmostEqual( prior.domain2Unit( prior.unit2Domain( 0.3 ) ), 0.3 )
        self.assertAlmostEqual( prior.domain2Unit( prior.unit2Domain( 0.8 ) ), 0.8 )
        print( prior.partialDomain2Unit( 5.9 ) )
        print( prior.partialDomain2Unit( 10.3 ) )
        print( prior.partialDomain2Unit( 48.8 ) )
        self.assertTrue( prior.partialDomain2Unit( 5.9 ) == 0.0 )
        self.assertTrue( prior.partialDomain2Unit( 10.3 ) == 1.0 / ( 48 - 6) )
        self.assertTrue( prior.partialDomain2Unit( 48.1 ) == 0.0 )
        self.assertAlmostEqual( prior.partialDomain2Unit( 18.9 ), prior.numPartialDomain2Unit( 18.9 ) )

    def testCircularUniformPrior( self ):

        print( "===== CircularUniform Prior Tests ==========================\n" )
#        self.assertWarns( UserWarning, CircularUniformPrior )
        prior = CircularUniformPrior( )
        printclass( prior )
        self.assertTrue( prior._lowDomain == -math.inf )
        self.assertTrue( prior._highDomain == +math.inf )
        self.assertFalse( prior.isBound() )

        prior.setLimits( [0,5] )
        print( "lowlim %f  highlim %f range %f"%( prior.lowLimit, prior.highLimit, prior._urng ) )
        printclass( prior )

        values = {0.0:0.0, 0.5:2.5, 1.0:5.0 }
        self.stdTestPrior( prior, values=values, utest=False )

        prior = UniformPrior( limits=[1,4], circular=True )
        printclass( prior )
        self.stdTestPrior( prior )

        prior = UniformPrior( circular=4 )
        printclass( prior )
        self.stdTestPrior( prior )



        cp = prior.copy( )
        print( cp )
        self.stdTestPrior( cp )

        prior = UniformPrior( numpy.asarray( [6.,48.] ) )
        printclass( prior )
        values = {0.0:6, 0.5:27, 1.0:48 }
        self.stdTestPrior( prior, values=values, utest=False )

        print( prior.domain2Unit( prior.unit2Domain(0.1) ) )
        print( prior.domain2Unit( prior.unit2Domain(0.3) ) )
        print( prior.domain2Unit( prior.unit2Domain(0.8) ) )
        self.assertAlmostEqual( prior.domain2Unit( prior.unit2Domain( 0.1 ) ), 0.1 )
        self.assertAlmostEqual( prior.domain2Unit( prior.unit2Domain( 0.3 ) ), 0.3 )
        self.assertAlmostEqual( prior.domain2Unit( prior.unit2Domain( 0.8 ) ), 0.8 )
        print( prior.partialDomain2Unit( 5.9 ) )
        print( prior.partialDomain2Unit( 10.3 ) )
        print( prior.partialDomain2Unit( 48.8 ) )
        self.assertTrue( prior.partialDomain2Unit( 5.9 ) == 0.0 )
        self.assertTrue( prior.partialDomain2Unit( 10.3 ) == 1.0 / ( 48 - 6) )
        self.assertTrue( prior.partialDomain2Unit( 48.1 ) == 0.0 )
        self.assertAlmostEqual( prior.partialDomain2Unit(8.9 ), prior.numPartialDomain2Unit( 8.9 ) )

    def testJeffreysPrior( self ):
        print( "===== Jeffreys Prior Tests ===========================\n" )
#        self.assertWarns( UserWarning, JeffreysPrior )
        prior = JeffreysPrior( )
        print( prior )

        self.assertTrue( prior._lowDomain == 0 )
        self.assertTrue( prior._highDomain == +math.inf )
        self.assertFalse( prior.isBound() )

        prior = JeffreysPrior( limits=[0.01,100] )
        print( prior )
        print( prior._umin, prior._urng )

        self.assertEqual( prior.lowLimit, 0.01 )
        self.assertEqual( prior.highLimit, 100 )
        self.assertTrue( prior._lowDomain == 0 )
        self.assertTrue( prior._highDomain == +math.inf )
        self.assertEqual( prior._umin, math.log( 0.01 ) )
        self.assertEqual( prior._urng, math.log(100) - math.log(0.01) )
        self.assertTrue( prior.isBound() )

        values = {0.0:0.01, 0.5:1.0, 1.0:100.0}
        self.stdTestPrior( prior, values=values )
        self.assertTrue( prior._umin == math.log( 0.01 ) )
        self.assertTrue( prior._urng == math.log( 10000.0 ) )

        prior.setLimits( numpy.asarray( [1.,6.] ) )
        print( prior )
        print( prior._umin, prior._urng )

        self.assertTrue( prior._umin == math.log( 1.0 ) )
        self.assertTrue( prior._urng == math.log( 6.0 ) )
        self.assertTrue( prior._urng == prior.getIntegral() )

        values = {0.0: 1.0, 0.5: 2.449489742783178, 1.0:6.0}
        self.stdTestPrior( prior, values=values )

        cp = prior.copy( )
        print( "Copy : " + str( cp ) )
        self.stdTestPrior( cp, values=values )

        prior = JeffreysPrior( numpy.asarray( [6.,48.] ) )
        print( prior )
        self.assertTrue( prior._umin == math.log( 6.0 ) )
        self.assertTrue( prior._urng == math.log( 48.0 ) - math.log( 6.0 ) )
        values = {0.0:6.0, 1.0:48.0}
        self.stdTestPrior( prior, values=values )


    def stdTestPrior( self, prior, utest=True, values={} ) :
        print( "----- Standard test ----------------------------------------" )

        for ku in range( 11 ) :
            u = 1/3 + 1/30 * ku if prior.isCircular() else 0.1 * ku
            d = prior.unit2Domain( u )

            v = prior.domain2Unit( d )
            f = prior.unit2Domain( v )
            print( "Unit %10.7f %10.7f  Domain %10.7f %10.7f"%( u, v, d, f ) )
            self.assertAlmostEqual( d, f )
            if utest and ku < 10 :
                self.assertAlmostEqual( v, u )

        u = numpy.arange( 10 ) * 0.1
        if prior.isCircular() :
            u = 1/3 * ( u + 1 )
        d = prior.unit2Domain( u )
        v = prior.domain2Unit( d )
        f = prior.unit2Domain( v )
        print( fmt( u, max=None ) )
        print( fmt( v, max=None ) )
        assertAAE( u, v )
        print( fmt( d, max=None ) )
        print( fmt( f, max=None ) )
        assertAAE( d, f )

        lr0 = numpy.log( prior.result( d ) )
        lr1 = prior.logResult( d )
        print( fmt( lr0, max=None ) )
        print( fmt( lr1, max=None ) )
        assertAAE( lr0, lr1 )

        # define a number of x values
        xx = [-10,-5, -1, 0, 1, 3, 6, 6.1, 48, math.inf]
        for x in xx :
            pl = prior.partialLog( x )
            nl = prior.numPartialLog( x )
            print( "Prior at %.3f is %.3f partialLogPrior is %.3f ~= %.3f"%
                 ( x, prior.result(x), pl, nl ) )
            if not ( math.isnan( pl + nl ) or prior.isOutOfLimits( x - prior.deltaP ) or
                     prior.isOutOfLimits( x + prior.deltaP ) ) :
                self.assertAlmostEqual( pl, nl, 4 )
            self.assertTrue( prior.result( x ) == prior.partialDomain2Unit( x ) )

        for v in values.keys() :
            print( "Unit %10.7f %10.7f  Domain %10.7f %10.7f"%
                ( v, prior.domain2Unit( values[v] ), values[v], prior.unit2Domain( v ) ) )
            self.assertAlmostEqual( prior.unit2Domain( v ), values[v] )
            if utest :
                self.assertAlmostEqual( prior.domain2Unit( values[v] ), v )

    def domainTest( self, prior ) :
        print( "----- Domain test ----------------------------------------" )

        print( prior.unit2Domain( 1.0 ) )
        print( prior.unit2Domain( 0.99999999999999993 ) )
        print( prior.unit2Domain( 0.9999999999999999 ) )
        print( prior.unit2Domain( 0.99999999999999 ) )
        print( prior.unit2Domain( 0.999999999999 ) )
        print( prior.unit2Domain( 0.9999999999 ) )
        print( prior.unit2Domain( 0.75 ) )
        print( prior.unit2Domain( 0.50 ) )
        print( prior.unit2Domain( 0.25 ) )
        print( prior.unit2Domain( 0.0000000001 ) )
        print( prior.unit2Domain( 0.000000000001 ) )
        print( prior.unit2Domain( 0.00000000000001 ) )
        print( prior.unit2Domain( 0.0000000000000001 ) )
        print( prior.unit2Domain( 0.00000000000000005 ) )
        print( prior.unit2Domain( 0.0 ) )



    def testExponentialPrior( self ):
        print( "===== Exponential Prior Tests ============================\n" )
        prior = ExponentialPrior( )
        print( prior )
        self.assertTrue( prior.scale == 1.0 )
        self.assertTrue( prior._lowDomain == 0 )
        self.assertTrue( prior._highDomain == +math.inf )
        self.assertTrue( prior.isBound() )

        self.stdTestPrior( prior )
        self.domainTest( prior )

        maxdom = prior.MAXVAL * prior.scale
        print( prior.unit2Domain( 0.5 ) )
        print( prior.unit2Domain( 0.0 ) )
        self.assertAlmostEqual( prior.unit2Domain( 1 - 1.0 / 1024 ), 6.93147180559945 )
        self.assertAlmostEqual( prior.unit2Domain( 0.5 ), 0.693147180559945 )
        self.assertAlmostEqual( prior.unit2Domain( 0.0 ), 0 )
        self.assertTrue( prior.unit2Domain( 1.0 ) == maxdom )

        prior.scale = 10
        print( prior )
        self.stdTestPrior( prior )

        maxdom = prior.MAXVAL * prior.scale
        self.assertTrue( prior.scale == 10.0 )
        self.assertAlmostEqual( prior.unit2Domain( 1 -1.0 / 1024 ), 69.3147180559945 )
        self.assertAlmostEqual( prior.unit2Domain( 0.5 ), 6.93147180559945 )
        self.assertAlmostEqual( prior.unit2Domain( 0.0 ), 0 )
        self.assertTrue( prior.unit2Domain( 1.0 ) == maxdom )

        cp = prior.copy( )
        print( cp )
        self.assertTrue( cp.scale == 10.0 )
        self.assertAlmostEqual( cp.unit2Domain( 1 -1.0 / 1024 ), 69.3147180559945 )
        self.assertAlmostEqual( cp.unit2Domain( 0.5 ), 6.93147180559945 )
        self.assertAlmostEqual( cp.unit2Domain( 0.0 ), 0 )
        self.assertTrue( cp.unit2Domain( 1.0 ) == maxdom )

        self.stdTestPrior( cp )


        cp = ExponentialPrior( prior=prior, scale=10 )
        print( cp )
        maxdom = cp.MAXVAL * cp.scale
        self.assertTrue( cp.scale == 10 )
        print( cp.domain2Unit( 0 ) )
        self.assertAlmostEqual( cp.unit2Domain( 1 - 1.0 / 2048 ), 76.24618986 )
        self.assertAlmostEqual( cp.unit2Domain( 0.75 ), 13.862943611 )
        self.assertAlmostEqual( cp.unit2Domain( 0.4 ), 5.108256237 )
        self.assertTrue( cp.unit2Domain( 1.0 ) == maxdom )

        prior = ExponentialPrior( 2 )
        print( prior )
        maxdom = prior.MAXVAL * prior.scale
        self.assertTrue( prior.scale == 2 )
        self.assertAlmostEqual( prior.unit2Domain(prior.domain2Unit(0.0) ), 0.0 )
        self.assertAlmostEqual( prior.unit2Domain(prior.domain2Unit(3) ), 3 )
        self.assertAlmostEqual( prior.unit2Domain(prior.domain2Unit(50) ), 50.0, 4 )
        self.assertAlmostEqual( prior.unit2Domain(prior.domain2Unit(100) ), maxdom )


    def testLaplacePrior( self ):
        print( "===== Laplace Prior Tests ==============================\n" )

        prior = LaplacePrior( )
        print( prior )
        self.assertTrue( prior.scale == 1 )
        print( prior.unit2Domain( 0.0 ) )
        print( prior.unit2Domain( 0.25 ) )
        print( prior.unit2Domain( 0.50 ) )
        print( prior.unit2Domain( 0.75 ) )
        print( prior.unit2Domain( 1.0 ) )

        self.stdTestPrior( prior )
        self.domainTest( prior )

        maxdom = prior.center + prior.MAXVAL * prior.scale
        self.assertTrue( prior.unit2Domain(1.0 ) == maxdom )
        self.assertAlmostEqual( prior.unit2Domain(0.75 ), 0.693147180559945 )
        self.assertAlmostEqual( prior.unit2Domain(0.5 ), 0 )
        self.assertAlmostEqual( prior.unit2Domain(0.25 ), -0.693147180559945 )
        self.assertAlmostEqual( prior.unit2Domain(1.0 / 2048 ), -6.93147180559945 )
        self.assertTrue( prior.unit2Domain(0.0 ) == -maxdom )

        prior.scale = 10
        print( prior )
        maxdom = prior.center + prior.MAXVAL * prior.scale
        self.assertTrue( prior.scale == 10 )
        self.assertAlmostEqual( prior.unit2Domain(1.0 / 2048 ), -69.3147180559945 )
        self.assertAlmostEqual( prior.unit2Domain(0.25 ), -6.93147180559945 )
        self.assertAlmostEqual( prior.unit2Domain(0.5 ), 0 )
        self.assertTrue( prior.unit2Domain(1.0 ) == maxdom )

        cp = prior.copy( )
        cp.center = 100
        maxdom = cp.center + cp.MAXVAL * cp.scale
        print( cp )
        self.stdTestPrior( cp )
        self.assertTrue( cp.scale == 10.0 )
        self.assertAlmostEqual( cp.unit2Domain(1.0 / 2048 ), 100 - 69.3147180559945 )
        self.assertAlmostEqual( cp.unit2Domain(0.25 ), 100 - 6.93147180559945 )
        self.assertAlmostEqual( cp.unit2Domain(0.5 ), 100 )
        self.assertTrue( cp.unit2Domain(1.0 ) == maxdom )

        prior.scale = 1.0
        print( prior )
        print( "partial 0.0 : ", prior.partialDomain2Unit( 0.0 ) )
        print( "numpart 0.0 : ", prior.numPartialDomain2Unit( 0.0 ) )
        print( "partial 0.1 : ", prior.partialDomain2Unit( 0.1 ) )
        print( "numpart 0.1 : ", prior.numPartialDomain2Unit( 0.1 ) )
        print( "partial  1. : ", prior.partialDomain2Unit( 1.0 ) )
        print( "numpart  1. : ", prior.numPartialDomain2Unit( 1.0 ) )
        print( "partial 10. : ", prior.partialDomain2Unit( 10. ) )
        print( "numpart 10. : ", prior.numPartialDomain2Unit( 10. ) )
        self.assertAlmostEqual( prior.partialDomain2Unit(0.0 ), 0.5 )
        print( prior.partialDomain2Unit( 9 ) )
        print( prior.numPartialDomain2Unit( 9 ) )
        self.assertAlmostEqual( prior.partialDomain2Unit(-9 ), prior.numPartialDomain2Unit( -9 ), 4 )
        self.assertAlmostEqual( prior.partialDomain2Unit(-1 ), prior.numPartialDomain2Unit( -1 ), 4 )
        self.assertAlmostEqual( prior.partialDomain2Unit(9 ), prior.numPartialDomain2Unit( 9 ), 4 )
        self.assertAlmostEqual( prior.partialDomain2Unit(1 ), prior.numPartialDomain2Unit( 1 ), 4 )

    def testLaplacePrior1( self ):
        print( "===== Laplace Prior with limits ==============================\n" )

        prior = LaplacePrior( limits=[-1.5,None], center=1, scale=2 )
        print( prior )
        print( "u2d   ", prior.unit2Domain )
        print( "bu2d  ", prior.baseUnit2Domain )


        self.assertTrue( prior.scale == 2 )
        print( prior.unit2Domain( 0.0 ) )
        print( prior.unit2Domain( 0.25 ) )
        print( prior.unit2Domain( 0.50 ) )
        print( prior.unit2Domain( 0.75 ) )
        print( prior.unit2Domain( 1.0 ) )

        self.stdTestPrior( prior )
        self.domainTest( prior )

    def testLaplacePrior2( self ):
        print( "===== Circular Laplace Prior  ==============================\n" )

        prior = LaplacePrior( circular=math.pi, center=1, scale=2 )
        print( prior )
        self.assertTrue( prior.scale == 2 )
        print( prior.unit2Domain( 0.0 ) )
        print( prior.unit2Domain( 0.25 ) )
        print( prior.unit2Domain( 0.50 ) )
        print( prior.unit2Domain( 0.75 ) )
        print( prior.unit2Domain( 1.0 ) )

        self.stdTestPrior( prior, utest=False )
        self.domainTest( prior )


    def testCauchyPrior( self ):
        print( "===== Cauchy Prior Tests ===========================\n" )

        prior = CauchyPrior( )
        print( prior )
        self.assertTrue( prior.scale == 1 )

        self.domainTest( prior )

        values = {1.0:1.633123935319537e+16, 0.75:1.0, 0.5:0.0, 0.25:-1.0, 0.0:-1.633123935319537e+16}
        self.stdTestPrior( prior, values=values )

        prior.scale = 10
        print( prior )
        self.assertTrue( prior.scale == 10 )
        self.assertAlmostEqual( prior.unit2Domain( 0.25 ), -9.999999999999998 )
        self.assertAlmostEqual( prior.unit2Domain( 0.5 ), 0 )
        self.assertTrue( prior.unit2Domain( 1.0 ) == 1.633123935319537e+17 )

        cp = prior.copy( )
        print( cp )
        self.assertTrue( cp.scale == 10.0 )
        self.assertAlmostEqual( cp.unit2Domain( 0.25 ), -9.999999999999 )
        self.assertAlmostEqual( cp.unit2Domain( 0.5 ), 0 )
        self.assertTrue( cp.unit2Domain( 1.0 ) == 1.633123935319537e+17 )
        print( prior.domain2Unit( 0 ) )
        uval = [0.1*k for k in range(11)]
        for uv in uval :
            print( uv,  prior.unit2Domain( uv ), prior.domain2Unit( prior.unit2Domain(uv) ) )
            self.assertAlmostEqual( prior.domain2Unit(prior.unit2Domain(uv) ), uv, 10 )

        prior.scale = 1.0
        print( prior )
        print( "partial 0.0 : ", prior.partialDomain2Unit( 0.0 ) )
        print( "numpart 0.0 : ", prior.numPartialDomain2Unit( 0.0 ) )
        print( "partial 0.1 : ", prior.partialDomain2Unit( 0.1 ) )
        print( "numpart 0.1 : ", prior.numPartialDomain2Unit( 0.1 ) )
        print( "partial  1. : ", prior.partialDomain2Unit( 1.0 ) )
        print( "numpart  1. : ", prior.numPartialDomain2Unit( 1.0 ) )
        print( "partial 10. : ", prior.partialDomain2Unit( 10. ) )
        print( "numpart 10. : ", prior.numPartialDomain2Unit( 10. ) )
        self.assertAlmostEqual( prior.partialDomain2Unit( 0.0 ), 0.3183098861837907 )
        print( prior.partialDomain2Unit( 9 ) )
        print( prior.numPartialDomain2Unit( 9 ) )
        self.assertAlmostEqual( prior.partialDomain2Unit(-9 ), prior.numPartialDomain2Unit( -9 ), 4 )
        self.assertAlmostEqual( prior.partialDomain2Unit(-1 ), prior.numPartialDomain2Unit( -1 ), 4 )
        self.assertAlmostEqual( prior.partialDomain2Unit(9 ), prior.numPartialDomain2Unit( 9 ), 4 )
        self.assertAlmostEqual( prior.partialDomain2Unit(1 ), prior.numPartialDomain2Unit( 1 ), 4 )

    def testCauchyPrior1( self ):
        print( "===== Cauchy Prior with limits ==============================\n" )

        prior = CauchyPrior( limits=[-1.5,None], center=1, scale=2 )
        print( prior )
        print( "u2d   ", prior.unit2Domain )
        print( "bu2d  ", prior.baseUnit2Domain )


        self.assertTrue( prior.scale == 2 )
        print( prior.unit2Domain( 0.0 ) )
        print( prior.unit2Domain( 0.25 ) )
        print( prior.unit2Domain( 0.50 ) )
        print( prior.unit2Domain( 0.75 ) )
        print( prior.unit2Domain( 1.0 ) )

        self.stdTestPrior( prior )
        self.domainTest( prior )

    def testCauchyPrior2( self ):
        print( "===== Circular Cauchy Prior  ==============================\n" )

        prior = CauchyPrior( circular=math.pi, center=1, scale=2 )
        print( prior )
        self.assertTrue( prior.scale == 2 )
        print( prior.unit2Domain( 0.0 ) )
        print( prior.unit2Domain( 0.25 ) )
        print( prior.unit2Domain( 0.50 ) )
        print( prior.unit2Domain( 0.75 ) )
        print( prior.unit2Domain( 1.0 ) )

        self.stdTestPrior( prior, utest=False )
        self.domainTest( prior )

    def testGaussPrior( self ):
        print( "===== Gauss Prior Tests ===========================\n" )

        prior = GaussPrior( )
        print( prior )
        self.assertTrue( prior.scale == 1 )

        self.stdTestPrior( prior )
        self.domainTest( prior )

        maxdom = prior.center + prior.MAXVAL * prior.scale
        mindom = prior.center - prior.MAXVAL * prior.scale
        print( "Domain from %f to %f" % (mindom, maxdom ) )
        print( prior.unit2Domain( 1.0 ), prior.unit2Domain( 0.75 ) ) 
        self.assertTrue( prior.unit2Domain( 1.0 ) == maxdom )
#        self.assertAlmostEqual( prior.unit2Domain( 0.75 ), 0.4769362762044699 )

        # value for the new (better version of GaussPrior
        self.assertAlmostEqual( prior.unit2Domain( 0.75 ), 0.6744897501960818 )
        self.assertAlmostEqual( prior.unit2Domain( 0.5 ), 0 )
        self.assertAlmostEqual( prior.unit2Domain( 0.25 ), -0.6744897501960818 )
#        self.assertAlmostEqual( prior.unit2Domain( 0.25 ), -0.4769362762044699 )
        self.assertTrue( prior.unit2Domain( 0.0 ) == mindom )

        prior.scale = 10
        print( prior )
        maxdom = prior.center + prior.MAXVAL * prior.scale
        self.assertTrue( prior.scale == 10 )
        self.assertAlmostEqual( prior.unit2Domain( 0.25 ), -6.744897501960818 )
#        self.assertAlmostEqual( prior.unit2Domain( 0.25 ), -4.769362762044699 )
        self.assertAlmostEqual( prior.unit2Domain( 0.5 ), 0 )
        self.assertTrue( prior.unit2Domain( 1.0 ) == maxdom )

        cp = prior.copy( )
        print( cp )
        cp.center = 100
        maxdom = cp.center + cp.MAXVAL * cp.scale
        mindom = cp.center - cp.MAXVAL * cp.scale
        self.assertTrue( cp.scale == 10.0 )

        print( cp.unit2Domain( 0.25 ), 100 - 6.744897501960818 )
        print( cp.unit2Domain( 0.5 ), 100 )
        self.assertAlmostEqual( cp.unit2Domain( 0.25 ), 100 - 6.744897501960818 )
#        self.assertAlmostEqual( cp.unit2Domain( 0.25 ), 100 - 4.769362762044699 )
        self.assertAlmostEqual( cp.unit2Domain( 0.5 ), 100 )
        self.assertTrue( cp.unit2Domain( 1.0 ) == maxdom )
        self.assertTrue( cp.unit2Domain( 0.0 ) == mindom )

        print( prior.domain2Unit( 0 ) )
        uval = [0.1*k for k in range(11)]
        for uv in uval :
            print( uv,  prior.unit2Domain( uv ), prior.domain2Unit( prior.unit2Domain(uv) ) )
            self.assertAlmostEqual( prior.domain2Unit(prior.unit2Domain(uv) ), uv, 10 )

        prior.scale = 1.0
        print( prior )

        print( "result  0.0 : ", prior.result( 0.0 ) )
        print( "partial 0.0 : ", prior.partialDomain2Unit( 0.0 ) )
        print( "numpart 0.0 : ", prior.numPartialDomain2Unit( 0.0 ) )
        print( "partial 0.1 : ", prior.partialDomain2Unit( 0.1 ) )
        print( "numpart 0.1 : ", prior.numPartialDomain2Unit( 0.1 ) )
        print( "partial  1. : ", prior.partialDomain2Unit( 1.0 ) )
        print( "numpart  1. : ", prior.numPartialDomain2Unit( 1.0 ) )
        print( "partial 10. : ", prior.partialDomain2Unit( 10. ) )
        print( "numpart 10. : ", prior.numPartialDomain2Unit( 10. ) )
        self.assertAlmostEqual( prior.partialDomain2Unit(0.0 ), 0.3989422804014327 )
#        self.assertAlmostEqual( prior.partialDomain2Unit(0.0 ), 0.5641895835477563 )

        # Value for new (better) GaussPrior.
        # self.assertAlmostEqual( prior.partialDomain2Unit(0.0 ), 0.3989422804014327 )
        print( prior.partialDomain2Unit( 9 ) )
        print( prior.numPartialDomain2Unit( 9 ) )
        self.assertAlmostEqual( prior.partialDomain2Unit(-9 ), prior.numPartialDomain2Unit( -9 ), 4 )
        self.assertAlmostEqual( prior.partialDomain2Unit(-1 ), prior.numPartialDomain2Unit( -1 ), 4 )
        self.assertAlmostEqual( prior.partialDomain2Unit(9 ), prior.numPartialDomain2Unit( 9 ), 4 )
        self.assertAlmostEqual( prior.partialDomain2Unit(1 ), prior.numPartialDomain2Unit( 1 ), 4 )

    def testGaussPrior1( self ):
        print( "===== Gauss Prior with limits ==============================\n" )

        prior = GaussPrior( limits=[-1.5,None], center=1, scale=2 )
        print( prior )
        print( "u2d   ", prior.unit2Domain )
        print( "bu2d  ", prior.baseUnit2Domain )


        self.assertTrue( prior.scale == 2 )
        print( prior.unit2Domain( 0.0 ) )
        print( prior.unit2Domain( 0.25 ) )
        print( prior.unit2Domain( 0.50 ) )
        print( prior.unit2Domain( 0.75 ) )
        print( prior.unit2Domain( 1.0 ) )

        self.stdTestPrior( prior )
        self.domainTest( prior )

    def testGaussPrior2( self ):
        print( "===== Circular Gauss Prior  ==============================\n" )

        prior = GaussPrior( circular=math.pi, center=1, scale=2 )
        print( prior )
        self.assertTrue( prior.scale == 2 )
        print( prior.unit2Domain( 0.0 ) )
        print( prior.unit2Domain( 0.25 ) )
        print( prior.unit2Domain( 0.50 ) )
        print( prior.unit2Domain( 0.75 ) )
        print( prior.unit2Domain( 1.0 ) )

        self.stdTestPrior( prior, utest=False )
        self.domainTest( prior )

    @classmethod
    def suite( cls ):
        return ConfiguredTestCase.suite( PriorTest.__class__ )

if __name__ == '__main__':
    unittest.main( )


