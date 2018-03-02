# run with : python3 -m unittest TestModels.TestModels.testGaussModel

import unittest
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
    def testToString( self ) :
        model = PadeModel( 1, 2 )
        model += PolynomialModel( 0 )
        name = model.__str__()
        print( name )
        self.assertTrue( name[-1] == '4' )

        model = PadeModel( 1, 2 )
        model += PolynomialModel( 1 )
        print( model )

    def plotArctanModel( self ) :
        self.testArctanModel( plot=True )

    def plotConstantModel( self ) :
        self.testConstantModel( plot=True )

    def plotEtalonModel( self ) :
        self.testEtalonModel( plot=True )

    def plotExpModel( self ) :
        self.testExpModel( plot=True )

    def plotVoigtModel( self ) :
        self.testVoigtModel( )
        xx = numpy.linspace( -1, +1, 1001 )
        par = numpy.asarray( [1.2,-0.2,0.3,0.3], dtype=float )
        plt.plot( xx, VoigtModel().result( xx, par ), '-', linewidth=2 )
        plt.plot( xx, GaussModel().result( xx, par[[0,1,2]] ), 'r-' )
        pg = par.copy()
        pg[3] = 0
        plt.plot( xx, VoigtModel().result( xx, pg ), 'r--' )
        plt.plot( xx, LorentzModel().result( xx, par[[0,1,3]] ), 'g-' )
        pg = par.copy()
        pg[2] = 0
        plt.plot( xx, VoigtModel().result( xx, pg ), 'g--' )
        plt.show()

    def plotLorentzModel( self ) :
        self.testLorentzModel( plot=True )

    def plotFreeShapeModel( self ) :
        self.XtestFreeShapeModel( plot=True )

    def plotGaussModel( self ) :
        self.testGaussModel( plot=True )

    def plotGaussPlusBackgroundModel( self ) :
        self.testGaussPlusBackgroundModel( plot=True )

    def plotHarmonicModel( self ) :
        self.testHarmonicModel( plot=True )

    def plotPolynomialModel( self ) :
        self.testPolynomialModel( plot=True )

    def plotChebyshevPolynomialModel( self ) :
        self.testChebyshevPolynomialModel( plot=True )

    def plotPadeModel( self ) :
        self.testPadeModel( plot=True )

    def plotPowerLawModel( self ) :
        self.testPowerLawModel( plot=True )

    def plotPowerModel( self ) :
        self.testPowerModel( plot=True )

    def plotSincModel( self ) :
        self.testSincModel( plot=True )

    def plotSineModel( self ) :
        self.testSineModel( plot=True )

    def plotSineAmpModel( self ) :
        self.testSineAmpModel( plot=True )

    def plotSineSplineModel( self ) :
        self.testSineSplineModel( plot=True )

    def plotSineSplineDriftModel( self ) :
        self.testSineSplineDriftModel( plot=True )

    def plotSineDriftModel( self ) :
        self.testSineDriftModel( plot=True )

    def plotBSplinesModel( self ) :
        self.testBSplinesModel( plot=True )

    def plotSplinesModel( self ) :
        self.testSplinesModel( plot=True )


    def testArctanModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******ARCTAN***********************" )
        m = ArctanModel( )
        p = numpy.asarray( [1.2,-0.1,30], dtype=float )

        stdModeltest( m, p, plot=plot )

    def testArctanFixedModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******ARCTAN FIXED******************" )
        m = ArctanModel( fixed={1:-1.2} )
        p = numpy.asarray( [1.2,30], dtype=float )

        stdModeltest( m, p, plot=plot )

    def testConstantModel( self, plot=False ):
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
        stdModeltest( m, p, plot=plot )

    def testEtalonModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******ETALON***********************" )
        m = EtalonModel( )
        p = numpy.asarray( [1.2, 0.6, 2.0, 0.2], dtype=float )

        stdModeltest( m, p, plot=plot )

    def testExpModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******EXP**************************" )
        m = ExpModel( )
        p = numpy.asarray( [1.2,-0.1], dtype=float )

        stdModeltest( m, p, plot=plot )

    def testLorentzModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******LORENTZ***********************" )
        m = LorentzModel( )
        p = numpy.asarray( [1.2,-0.2,0.3], dtype=float )

        stdModeltest( m, p, plot=plot )

    def testVoigtModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******VOIGT***********************" )
        m = VoigtModel( )
        p = numpy.asarray( [1.2,0.2,0.3,0.4], dtype=float )
        print( p )
        stdModeltest( m, p, plot=plot, warn=["nopart"] )

    def XtestFreeShapeModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******FREESHAPE********************" )
        m = FreeShapeModel( 5, pixperbin=1, xlo=-1, xhi=1.1 )
        self.assertTrue( m.npbase == 5 )
        p = numpy.asarray( [1.2,0.2,1.0,0.5,0.3], dtype=float )

        stdModeltest( m, p, plot=plot )

    def testGaussModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******GAUSS*************************" )
        m = GaussModel( )
        p = numpy.asarray( [1.2,-0.2,0.3], dtype=float )

        stdModeltest( m, p, plot=plot )

    def testGaussPlusBackgroundModel( self, plot=False ):
        print( "******GAUSS + BG**********************" )
        gm = GaussModel( )
        print( gm )
        print( gm.parameters )
        pm = PolynomialModel( 1 )
        print( pm )
        print( pm.parameters )
        gm.addModel( pm )
        par = numpy.asarray( [3,0.2,0.2,0.1,0.1], dtype=float )

        stdModeltest( gm, par, plot=plot )

    def testHarmonicModel( self, plot=False ):
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

        stdModeltest( m, p, plot=plot )

    def testPolynomialModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******POLYNOMIAL**********************" )
        m = PolynomialModel( 3 )
        self.assertTrue( m.getNumberOfParameters( ) == 4 )
        self.assertTrue( m.npbase == 4 )
        p = numpy.asarray( [1,-2,3,-2], dtype=float )
        stdModeltest( m, p, plot=plot )

    def testFixedPolynomialModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******POLYNOMIAL FIXED****************" )
        m = PolynomialModel( 5, fixed={1:0.4, 3:-1.2} )
        self.assertTrue( m.getNumberOfParameters( ) == 4 )
        self.assertTrue( m.npbase == 4 )
        self.assertTrue( m.npmax == 6 )
        p = numpy.asarray( [1,-2,3,-2], dtype=float )
        stdModeltest( m, p, plot=plot )

    def testChebyshevPolynomialModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******CHEBYSHEV POLYNOMIAL*************" )
        m = ChebyshevPolynomialModel( 4 )
        self.assertTrue( m.getNumberOfParameters( ) == 5 )
        self.assertTrue( m.npbase == 5 )
        p = numpy.asarray( [1,-2,3,-2,0.3], dtype=float )
        stdModeltest( m, p, plot=plot )

    def testPadeModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******PADE**********************" )
        m = PadeModel( 3, 2 )
        self.assertTrue( m.getNumberOfParameters( ) == 6 )
        self.assertTrue( m.npbase == 6 )
        p =  numpy.asarray( [1,-2,3,-2,0.3,1], dtype=float )
        stdModeltest( m, p, plot=plot )

    def testPowerLawModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******POWERLAW*******************" )
        m = PowerLawModel( )
        self.assertTrue( m.npchain == 3 )
        self.assertTrue( m.npbase == 3 )
        p = [2.3, -1.1, 0.5]
        stdModeltest( m, p, plot=plot )

    def testPowerModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******POWER**********************" )
        m = PowerModel( 3 )
        self.assertTrue( m.getNumberOfParameters( ) == 1 )
        self.assertTrue( m.npbase == 1 )
        p = [2.3]
        stdModeltest( m, p, plot=plot )

    def testSincModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINC***********************" )
        m = SincModel( )
        self.assertTrue( m.npchain == 3 )
        self.assertTrue( m.npbase == 3 )
        p = [2.3, -1.1, 0.5]
        stdModeltest( m, p, plot=plot )

    def testSineModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINE***********************" )
        m = SineModel( )
        self.assertTrue( m.npchain == 3 )
        self.assertTrue( m.npbase == 3 )
        p = [1.3, -1.1, 0.5]
        stdModeltest( m, p, plot=plot )

    def testSineAmpModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINEAMP********************" )
        m = SineAmpModel( 1.3 )
        self.assertTrue( m.npchain == 2 )
        self.assertTrue( m.npbase == 2 )
        p = [-1.1, 0.5]
        stdModeltest( m, p, plot=plot )

    def testSineSplineModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINESPLINE******************" )
        knots = numpy.arange( 3, dtype=float ) - 1
        m = SineSplineModel( 1.3, knots )
        self.assertTrue( m.npchain == 10 )
        self.assertTrue( m.npbase == 10 )
        p = [0.0, 0.5, -0.1, 0.5, -0.1, 0.0, +1.1, 0.5, -1.1, -0.5]
        amp = m.getAmplitudes( x, p )
        print( amp[0], amp[1] )
        stdModeltest( m, p, plot=plot )

    def testSineSplineDriftModel( self, plot=False ):
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
        stdModeltest( m, p, plot=plot )

    def testSineDriftModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINEDRIFT******************" )
        m = SineDriftModel( )
        self.assertTrue( m.npchain == 4 )
        self.assertTrue( m.npbase == 4 )
        p = [1.1, 0.5, 0.8, 0.4 ]
        stdModeltest( m, p, plot=plot )

    def testBSplinesModel( self, plot=False ):
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

        m1 = BSplinesModel( nrknots=5, order=3, min=-1, max=1 )
        p = numpy.asarray( [2,1,2,1,2,1,2], dtype=float )
        p = p[:m1.npchain]
        print( m1.npchain, p )
        stdModeltest( m1, p, plot=plot )

    def testSplinesModel( self, plot=False ):
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
        stdModeltest( m1, p, plot=plot )



    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestModels.__class__ )

if __name__ == '__main__':
    unittest.main( )


