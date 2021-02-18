# run with : python3 -m unittest TestModels.TestModels.testGaussModel

import unittest
import os
import numpy as numpy
from astropy import units
import matplotlib.pyplot as plt
import warnings

from StdTests import stdModeltest

from BayesicFitting import *


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

class TestModels( unittest.TestCase ):
    """
    Test harness for Models

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

    def testToString( self ) :
        model = PadeModel( 1, 2 )
        model += PolynomialModel( 0 )
        name = model.__str__()
        print( name )
        self.assertTrue( name[-1] == '4' )

        model = PadeModel( 1, 2 )
        model += PolynomialModel( 1 )
        print( model )
        print( model.shortName() )

    def testArctanModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******ARCTAN***********************" )
        m = ArctanModel( )
        p = numpy.asarray( [1.2,-0.1,30], dtype=float )

        stdModeltest( m, p, plot=self.doplot )

    def testArctanFixedModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******ARCTAN FIXED******************" )
        m = ArctanModel( fixed={1:-1.2} )
        p = numpy.asarray( [1.2,30], dtype=float )

        stdModeltest( m, p, plot=self.doplot )

    def testConstantModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******NULL***********************" )
        m = ConstantModel( )
        self.assertTrue( m.npchain == 0 )
        p = []
        stdModeltest( m, p )

        print( "******CONSTANT*******************" )
        m = ConstantModel( values = 5.5 )
        stdModeltest( m, p )

        print( "******COMPOUND*******************" )
        m = ConstantModel( values = 1.0 )
        m.addModel( ExpModel() )
        self.assertTrue( m.npbase == 0 )
        self.assertTrue( m.npchain == 2 )
        p = [1.0, -3.0]
        stdModeltest( m, p, plot=self.doplot )

    def testEtalonModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******ETALON***********************" )
        m = EtalonModel( )
        p = numpy.asarray( [1.2, 0.6, 2.0, 0.2], dtype=float )

        stdModeltest( m, p, plot=self.doplot )

    """
    def testEtalonVarModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******ETALON VAR***********************" )
        m = EtalonVarModel( )
        p = numpy.asarray( [1.2, 0.6, 2.0, 0.2], dtype=float )

        stdModeltest( m, p, plot=self.doplot )

    def testEtalonVarModel2( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******ETALON VAR 2***********************" )
        pm = BasicSplinesModel( knots=[-1.0, 0.1, 1.0] )
        m = EtalonVarModel( fixed={1:pm} )
        p = numpy.asarray( [1.0, 5.5, 0.2, 0.03, 0.04, 0.05, 0.02, 0.01], dtype=float )

        stdModeltest( m, p, plot=self.doplot )
    """
    def testExpModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******EXP**************************" )
        m = ExpModel( )
        p = numpy.asarray( [1.2,-0.1], dtype=float )

        stdModeltest( m, p, plot=self.doplot )

        print( "******DECAY************************" )

        m = ExpModel( decay=True )
        p = numpy.asarray( [1.2,0.1], dtype=float )

        stdModeltest( m, p, plot=self.doplot )

    def testLogisticModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******LOGISTIC***********************" )
        m = LogisticModel( )
        p = numpy.asarray( [1.2,-0.2,0.3], dtype=float )

        stdModeltest( m, p, plot=self.doplot )

    def testLorentzModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******LORENTZ***********************" )
        m = LorentzModel( )
        p = numpy.asarray( [1.2,-0.2,0.3], dtype=float )

        stdModeltest( m, p, plot=self.doplot )

    def testVoigtModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******VOIGT***********************" )
        m = VoigtModel( )
        p = numpy.asarray( [1.2,0.2,0.3,0.4], dtype=float )
        print( p )

        stdModeltest( m, p, plot=self.doplot ) #, warn=["nopart"] )

    def testPseudoVoigtModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******PSEUDOVOIGT***********************" )
        m = PseudoVoigtModel( )
        p = numpy.asarray( [1.2,0.2,0.3,0.4], dtype=float )
        print( p )

        stdModeltest( m, p, plot=self.doplot )

    def testFreeShapeModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******FREESHAPE********************" )
        m = FreeShapeModel( 5, pixperbin=1, xlo=-1, xhi=1.1, nconvolve=2 )
        self.assertTrue( m.npbase == 5 )
        p = numpy.asarray( [1.2,0.2,1.0,0.5,0.3], dtype=float )

        stdModeltest( m, p, plot=self.doplot )

    def testGaussModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******GAUSS*************************" )
        m = GaussModel( )
        p = numpy.asarray( [1.2,-0.2,0.3], dtype=float )

        stdModeltest( m, p, plot=self.doplot )

    def testGaussPlusBackgroundModel( self ):
        print( "******GAUSS + BG**********************" )
        gm = GaussModel( )
        print( gm )
        print( gm.parameters )
        pm = PolynomialModel( 1 )
        print( pm )
        print( pm.parameters )
        gm.addModel( pm )
        par = numpy.asarray( [3,0.2,0.2,0.1,0.1], dtype=float )

        stdModeltest( gm, par, plot=self.doplot )

    def testHarmonicModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******HARMONIC**********************" )
        m = HarmonicModel( 1 )
        self.assertTrue( m.order == 1 )
        self.assertTrue( m.npbase == 2 )
        self.assertTrue( m.period == 1.0 )

        m = HarmonicModel( order=3, period=0.4 )
        self.assertTrue( m.order == 3 )
        self.assertTrue( m.npbase == 6 )
        self.assertTrue( m.period == 0.4 )

        p = numpy.asarray( [1.2,-0.2,0.3,1.2,-0.2,0.3], dtype=float )

        stdModeltest( m, p, plot=self.doplot )

    def testPolynomialModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******POLYNOMIAL**********************" )
        m = PolynomialModel( 3 )
        self.assertTrue( m.getNumberOfParameters( ) == 4 )
        self.assertTrue( m.npbase == 4 )
        p = numpy.asarray( [1,-2,3,-2], dtype=float )

        stdModeltest( m, p, plot=self.doplot )

    def testFixedPolynomialModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******POLYNOMIAL FIXED****************" )
        m = PolynomialModel( 5, fixed={1:0.4, 3:-1.2} )
        self.assertTrue( m.getNumberOfParameters( ) == 4 )
        self.assertTrue( m.npbase == 4 )
        self.assertTrue( m.npmax == 6 )
        p = numpy.asarray( [1,-2,3,-2], dtype=float )

        stdModeltest( m, p, plot=self.doplot )

    def testChebyshevPolynomialModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******CHEBYSHEV POLYNOMIAL*************" )
        m = ChebyshevPolynomialModel( 4 )
        self.assertTrue( m.getNumberOfParameters( ) == 5 )
        self.assertTrue( m.npbase == 5 )
        p = numpy.asarray( [1,-2,3,-2,0.3], dtype=float )

        stdModeltest( m, p, plot=self.doplot )

    def testPadeModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******PADE**********************" )
        m = PadeModel( 3, 2 )
        self.assertTrue( m.getNumberOfParameters( ) == 6 )
        self.assertTrue( m.npbase == 6 )
        p =  numpy.asarray( [1,-2,3,-2,0.3,1], dtype=float )
        stdModeltest( m, p, plot=self.doplot )

    def testPowerLawModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******POWERLAW*******************" )
        m = PowerLawModel( )
        self.assertTrue( m.npchain == 3 )
        self.assertTrue( m.npbase == 3 )
        p = [2.3, -1.1, 0.5]
        stdModeltest( m, p, plot=self.doplot )

    def testPowerModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******POWER**********************" )
        m = PowerModel( 3 )
        self.assertTrue( m.getNumberOfParameters( ) == 1 )
        self.assertTrue( m.npbase == 1 )
        p = [2.3]
        stdModeltest( m, p, plot=self.doplot )

    def testRadialVelocityModel( self ):
        x  = numpy.linspace( 0, 1400, 1401, dtype=float )
        print( "******RADIALVELOCITY***************" )
        m = RadialVelocityModel( )
        self.assertTrue( m.npars == 5 )
        self.assertTrue( m.npbase == 5 )
        p = [0.67, 130, 1200.0, 4.0, 3.0]
        if self.doplot :
            for p3 in range( 7 ) :
                p[4] = 0.7 + 0.5 * p3
                y = m.result( x, p )
                plt.plot( x, y + 100 * p3, '-' )
#                yo = m.baseResultXXX( x, p )
#                plt.plot( x, yo + 100 * p3, '.' )

            plt.show()

        stdModeltest( m, p, plot=self.doplot )

    def testRadialVelocityModel_2( self ):
        x  = numpy.linspace( 0, 1400, 1401, dtype=float )
        print( "******RADIALVELOCITY***************" )
        m = RadialVelocityModel( spherical=False )
        self.assertTrue( m.npars == 5 )
        self.assertTrue( m.npbase == 5 )
        p = [0.67, 130, 1200.0, 4.0, 3.0]
        if self.doplot :
            for p3 in range( 7 ) :
                p[4] = 0.7 + 0.5 * p3
                y = m.result( x, p )
                plt.plot( x, y + 100 * p3, '-' )
#                yo = m.baseResultXXX( x, p )
#                plt.plot( x, yo + 100 * p3, '.' )

            plt.show()

        stdModeltest( m, p, plot=self.doplot )

    def testSincModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINC***********************" )
        m = SincModel( )
        self.assertTrue( m.npchain == 3 )
        self.assertTrue( m.npbase == 3 )
        p = [2.3, -1.1, 0.5]
        stdModeltest( m, p, plot=self.doplot )

    def testSineModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINE***********************" )
        m = SineModel( )
        self.assertTrue( m.npchain == 3 )
        self.assertTrue( m.npbase == 3 )
        p = [1.3, -1.1, 0.5]
        stdModeltest( m, p, plot=self.doplot )

    def testPhaseSineModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINE***********************" )
        m = SineModel( phase=True )
        self.assertTrue( m.npchain == 3 )
        self.assertTrue( m.npbase == 3 )
        p = [1.3, -1.1, 0.5]
        stdModeltest( m, p, plot=self.doplot )

    def testSineAmpModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINEAMP********************" )
        m = SineAmpModel( 1.3 )
        self.assertTrue( m.npchain == 2 )
        self.assertTrue( m.npbase == 2 )
        p = [-1.1, 0.5]
        stdModeltest( m, p, plot=self.doplot )

    def testSineSplineModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINESPLINE******************" )
        knots = numpy.arange( 3, dtype=float ) - 1
        m = SineSplineModel( 1.3, knots )
        self.assertTrue( m.npchain == 10 )
        self.assertTrue( m.npbase == 10 )
        p = [0.0, 0.5, -0.1, 0.5, -0.1, 0.0, +1.1, 0.5, -1.1, -0.5]
        amp = m.getAmplitudes( x, p )
        print( amp[0], amp[1] )
        stdModeltest( m, p, plot=self.doplot )

    def testSineSplineDriftModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINESPLINEDRIFT*************" )
        knots = numpy.arange( 3, dtype=float ) - 1
        m = SineSplineDriftModel( knots, degree=1 )
        print( m.npchain )
        self.assertTrue( m.npchain == 12 )
        self.assertTrue( m.npbase == 12 )
        p = [0.0, 0.1, 0.0, 0.5, -0.1, 0.5, -0.1, 0.0, +1.1, 0.5, -1.1, -0.5]
        amp = m.getAmplitudes( x, p )
        print( amp[0], amp[1] )
        stdModeltest( m, p, plot=self.doplot )

    def testSineDriftModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINEDRIFT******************" )
        m = SineDriftModel( )
        self.assertTrue( m.npchain == 4 )
        self.assertTrue( m.npbase == 4 )
        p = [1.1, 0.5, 0.8, 0.4 ]
        stdModeltest( m, p, plot=self.doplot )

    def testBSplinesModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******B-SPLINES*************************" )
        knots = numpy.arange( 11, dtype=float )
        m0 = BSplinesModel( knots=knots )
        self.assertTrue( m0.order == 3 )
        self.assertTrue( m0.getNumberOfParameters( ) == 13 )
        self.assertTrue( m0.npbase == 13 )
        m1 = BSplinesModel( nrknots=5, min=-1, max=1 )
        self.assertTrue( m1.order == 3 )
        self.assertTrue( m1.getNumberOfParameters( ) == 7 )
        self.assertTrue( m1.npbase == 7 )
        for k in range( len( m1.knots ) ) :
            self.assertTrue( m1.knots[k] == -1 + k / 2 )
        xin = numpy.linspace( 0, 10, 101, dtype = float )
        m2 = BSplinesModel( xrange=xin, order=2, nrknots=11 )
        self.assertTrue( m2.order == 2 )
        self.assertTrue( m2.getNumberOfParameters( ) == 12 )
        self.assertTrue( m2.npbase == 12 )
        for k in range( len( m2.knots ) ) : self.assertTrue( m2.knots[k] == k )

        self.assertRaises( ValueError, BSplinesModel )

        m1 = BSplinesModel( nrknots=5, order=3, min=-1.01, max=1.01 )
        p = numpy.asarray( [2,1,2,1,2,1,2], dtype=float )
        p = p[:m1.npchain]
        print( m1.npchain, p )
        stdModeltest( m1, p, plot=self.doplot )

    def testBasicSplinesModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******BASICSPLINES*************************" )
        knots = numpy.arange( 11, dtype=float )
        m0 = BasicSplinesModel( knots=knots )
        self.assertTrue( m0.order == 3 )
        self.assertTrue( m0.getNumberOfParameters( ) == 13 )
        self.assertTrue( m0.npbase == 13 )

        m1 = BasicSplinesModel( nrknots=5, min=-1, max=1 )
        self.assertTrue( m1.order == 3 )
        self.assertTrue( m1.getNumberOfParameters( ) == 7 )
        self.assertTrue( m1.npbase == 7 )
        for k in range( len( m1.knots ) ) :
            self.assertTrue( m1.knots[k] == -1 + k / 2 )

        xin = numpy.linspace( 0, 10, 101, dtype = float )
        m2 = BasicSplinesModel( xrange=xin, order=2, nrknots=11 )
        self.assertTrue( m2.order == 2 )
        self.assertTrue( m2.getNumberOfParameters( ) == 12 )
        self.assertTrue( m2.npbase == 12 )
        for k in range( len( m2.knots ) ) :
            self.assertTrue( m2.knots[k] == k )

        self.assertRaises( ValueError, BasicSplinesModel )

        m1 = BasicSplinesModel( nrknots=5, order=3, min=-1.01, max=1.01 )
        p = numpy.asarray( [2,1,2,1,2,1,2], dtype=float )
        print( m1.npchain, p )
        stdModeltest( m1, p, plot=self.doplot )

    def testSplinesModel( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SPLINES*************************" )
        knots = numpy.arange( 11, dtype=float )
        m0 = SplinesModel( knots=knots )
        self.assertTrue( m0.order == 3 )
        self.assertTrue( m0.getNumberOfParameters( ) == 13 )
        self.assertTrue( m0.npbase == 13 )

        m1 = SplinesModel( nrknots=5, min=-1, max=1 )
        self.assertTrue( m1.order == 3 )
        self.assertTrue( m1.getNumberOfParameters( ) == 7 )
        self.assertTrue( m1.npbase == 7 )
        for k in range( len( m1.knots ) ) :
            self.assertTrue( m1.knots[k] == -1 + k / 2 )

        xin = numpy.linspace( 0, 10, 101, dtype = float )
        m2 = SplinesModel( xrange=xin, order=2, nrknots=11 )
        self.assertTrue( m2.order == 2 )
        self.assertTrue( m2.getNumberOfParameters( ) == 12 )
        self.assertTrue( m2.npbase == 12 )
        for k in range( len( m2.knots ) ) : self.assertTrue( m2.knots[k] == k )

        self.assertRaises( ValueError, SplinesModel )

        p = numpy.asarray( [0,1,0,1,0,1,0], dtype=float )
        stdModeltest( m1, p, plot=self.doplot )



    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestModels.__class__ )

if __name__ == '__main__':
    unittest.main( )


