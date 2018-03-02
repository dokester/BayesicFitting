# run with : python3 -m unittest TestFixedModels.TestFixedModels.testGaussModel

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

class TestFixedModels( unittest.TestCase ):
    """
    Test harness for Models

    Author:      Do Kester

    """
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

    def plotSplinesModel( self ) :
        self.testSplinesModel( plot=True )


    def testArctanModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******ARCTAN******************" )
        m = ArctanModel( fixed={1:-1.2} )
        p = numpy.asarray( [1.2,30], dtype=float )

        stdModeltest( m, p, plot=plot )

    def testEtalonModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******ETALON***********************" )
        m = EtalonModel( fixed={0:1.5})
        p = numpy.asarray( [30.0, 2.0, 0.2], dtype=float )

        stdModeltest( m, p, plot=plot )

    def testEtalonModel2( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******ETALON 2***********************" )
        fm = PolynomialModel( 1 )
        m = EtalonModel( fixed={0:1.5, 1:fm})
        p = numpy.asarray( [2.0, 0.2, 1.0, 0.9], dtype=float )

        stdModeltest( m, p, plot=plot )

    def testEtalonModel3( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******ETALON 2***********************" )
        fm = PolynomialModel( 1 )
        fm += SineModel()
        am = SplinesModel( nrknots=2, min=-1, max=1 )
        m = EtalonModel( fixed={0:am, 1:fm})
        par = [10.0, 0.2, 1.0, 0.1, 0.0, 0.02, 1.0, 0.5, 2.0, 0.1, 0.0]
        p = numpy.asarray( par, dtype=float )

        stdModeltest( m, p, plot=plot )

    def testExpModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******EXP**************************" )
        m = ExpModel( fixed={1:0.1} )
        p = numpy.asarray( [1.2], dtype=float )

        stdModeltest( m, p, plot=plot )

    def testLorentzModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******LORENTZ***********************" )
        m = LorentzModel( fixed={0:4} )
        p = numpy.asarray( [-0.2,0.3], dtype=float )

        stdModeltest( m, p, plot=plot )

    def testVoigtModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******VOIGT***********************" )
        m = VoigtModel( fixed={1:0.2,2:0.3} )
        p = numpy.asarray( [1.2,0.4], dtype=float )
        print( m.parameters )
        print( m.expand( x, m.parameters ) )

        stdModeltest( m, p, plot=plot, warn=["nopart"] )

    def XtestFreeShapeModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******FREESHAPE********************" )

        self.assertRaises( AttributeError, FreeShapeModel,  5, pixperbin=1, xlo=-1,
                    xhi=1.1, fixed={3:1.1} )

    def testGaussModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******GAUSS*************************" )
        m = GaussModel( fixed={2:0.3} )
        p = numpy.asarray( [1.2,-0.2], dtype=float )

        stdModeltest( m, p, plot=plot )

    def testGaussPlusBackgroundModel( self, plot=False ):
        print( "******GAUSS + BG**********************" )
        gm = GaussModel( fixed={1:0.1} )
        print( gm )
        print( gm.parameters )
        pm = PolynomialModel( 2, fixed={0:2.9} )
        print( pm )
        print( pm.parameters )
        gm.addModel( pm )
        self.assertTrue( gm.npchain == 4 )
        par = numpy.asarray( [3,0.2,0.1,0.1], dtype=float )

        stdModeltest( gm, par, plot=plot )

    def testHarmonicModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******HARMONIC**********************" )
        m = HarmonicModel( order=3, period=0.4, fixed={0:1.0,2:1.0,4:1.0} )
        self.assertTrue( m.order == 3 )
        self.assertTrue( m.npbase == 3 )
        self.assertTrue( m.npmax == 6 )
        self.assertTrue( m.period == 0.4 )

        p = numpy.asarray( [1.2,0.3,1.2], dtype=float )

        stdModeltest( m, p, plot=plot )

    def testPolynomialModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******POLYNOMIAL*********************" )
        sm = SineModel()
        m = PolynomialModel( 2, fixed={0:sm} )
        Tools.printclass( m )
        self.assertTrue( m.getNumberOfParameters( ) == 5 )
        self.assertTrue( m.npbase == 5 )
        self.assertTrue( m.npmax == 3 )
        p = numpy.asarray( [0.2,0.1,1.9,-1.2,1.3], dtype=float )
        print( sm.partial( x, p[2:] ) )
        print( m.partial( x, p ) )
        pm = PolynomialModel( 2, fixed={0:1.0} )
        pm *= SineModel()
        print( pm )
        print( pm.result( x, p ) )
        print( m )
        print( m.result( x, p ) )
        stdModeltest( m, p, plot=plot )

    def testChebyshevPolynomialModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******CHEBYSHEV POLYNOMIAL*************" )
        m = ChebyshevPolynomialModel( 4, fixed={4:0.1} )
        self.assertTrue( m.getNumberOfParameters( ) == 4 )
        self.assertTrue( m.npbase == 4 )
        p = numpy.asarray( [1,-2,3,-2], dtype=float )
        stdModeltest( m, p, plot=plot )

    def testPadeModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******PADE***********************" )
        m = PadeModel( 3, 2, fixed={0:1} )
        self.assertTrue( m.getNumberOfParameters( ) == 6 )
        self.assertTrue( m.npbase == 6 )
        self.assertTrue( m.npmax == 7 )
        p =  numpy.asarray( [-2, 3, -2, 0.3, 1, 0.2], dtype=float )
        stdModeltest( m, p, plot=plot )

    def testPowerLawModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******POWERLAW*******************" )
        m = PowerLawModel( fixed={1:-2} )
        self.assertTrue( m.npchain == 2 )
        self.assertTrue( m.npbase == 2 )
        p = [2.3, 0.5]
        stdModeltest( m, p, plot=plot )

    def testPowerModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******POWER**********************" )
        m = PowerModel( 3, fixed={0:1.2} )
        self.assertTrue( m.getNumberOfParameters( ) == 0 )
        self.assertTrue( m.npbase == 0 )
        p = []
        stdModeltest( m, p, plot=plot )

    def testSincModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINC***********************" )
        m = SincModel( fixed={2:0.1,1:2} )
        self.assertTrue( m.npchain == 1 )
        self.assertTrue( m.npbase == 1 )
        p = [2.3]
        stdModeltest( m, p, plot=plot )

    def testSineModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINE***********************" )
        m = SineModel( fixed={0:1})
        self.assertTrue( m.npchain == 2 )
        self.assertTrue( m.npbase == 2 )
        p = [-1.1, 0.5]
        stdModeltest( m, p, plot=plot )

    def testSineAmpModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINEAMP********************" )
        m = SineAmpModel( 1.3, fixed={1:1} )
        self.assertTrue( m.npchain == 1 )
        self.assertTrue( m.npbase == 1 )
        p = [-1.1]
        stdModeltest( m, p, plot=plot )

    def testSineDriftModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINEDRIFT******************" )

        m = SineDriftModel( fixed={2:0.8} )
        self.assertTrue( m.npmax == 4 )
        self.assertTrue( m.npchain == 3 )
        self.assertTrue( m.npbase == 3 )
        p = [1.1, 0.5, 0.8, 0.4 ]
        stdModeltest( m, p, plot=plot )

    def testSplinesModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SPLINES*************************" )
        knots = numpy.arange( 11, dtype=float )
        self.assertRaises( AttributeError, SplinesModel, knots, fixed={3:1.1} )

    def testSineSplineModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINESPLINE******************" )
        knots = numpy.arange( 3, dtype=float ) - 1
        freq = 150.0
        self.assertRaises( AttributeError, SineSplineModel, freq, knots, fixed={3:1.1} )


    def testSineSplineDriftModel( self, plot=False ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "******SINESPLINEDRIFT*************" )
        knots = numpy.arange( 3, dtype=float ) - 1
        self.assertRaises( AttributeError, SineSplineDriftModel, knots, fixed={3:1.1} )




    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestModels.__class__ )

if __name__ == '__main__':
    unittest.main( )


