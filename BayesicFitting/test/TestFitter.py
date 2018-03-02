# run with : python3 -m unittest TestFitter

import numpy as numpy
from numpy.testing import assert_array_almost_equal as assertAAE
from astropy import units
import unittest
import FitPlot

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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *  2004 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2017 Do Kester

class TestFitter( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author:      Do Kester

    """
    aa = 5              #  average offset
    bb = 2              #  slope
    ss = 0.3            #  noise Normal distr.

    x = numpy.asarray( [ -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
    x += 2
    noise = numpy.asarray( [-0.000996, -0.046035,  0.013656,  0.418449,  0.0295155,  0.273705,
      -0.204794,  0.275843, -0.415945, -0.373516, -0.158084] )

    def eq( self, a, b, eps=1e-10 ) :
        if ( a + b ) != 0 :
            return abs( a - b ) / abs( a + b ) < eps
        else :
            return abs( a - b ) < eps

    def plotStraightLineParameter( self ):
        self.testStraightLineParameter( plot=True )


    #  **************************************************************
    def testStraightLineParameter( self, plot=False ):
        """
        test slope fit

        1. Compare PolynomialModel(1) with chain of PowerModel(0) + PowerModel(1)

        2. Fix parameters in PolynomialModel

        """
        print( "\n   Fitter Test 1  \n" )
        model = PolynomialModel( 1 )
        fitter = Fitter( self.x, model )
        model0 = PowerModel( 0 )
        model1 = PowerModel( 1 )
        model0.addModel( model1 )
        altfit = Fitter( self.x, model0 )
        y = self.noise + self.aa + self.bb * self.x

        print( "Testing Straight Line fit" )

        self.assertTrue( model1.npchain == 2 )
        par = fitter.fit( y )
        alt = altfit.fit( y )

        print( "offst = %f  alt = %f  truth = %f"%(par[0], alt[0], self.aa) )
        print( "slope = %f  alt = %f  truth = %f"%(par[1], alt[1], self.bb) )
        assertAAE( par, alt )

        chisq = fitter.chisq
        altch = altfit.chisq
        print( "chisq = %f  alt = %f"%( chisq, altch) )
        self.assertTrue( self.eq(chisq, altch) )

        std = fitter.standardDeviations
        ast = altfit.standardDeviations
        print( "stdev = %f  alt = %f"%(std[0], ast[0]) )
        print( "stdev = %f  alt = %f"%(std[1], ast[1]) )
        assertAAE( std, ast )

        par1 = altfit.fit( y, keep={0:par[0]} )
        if plot :
            FitPlot.plotFit( self.x, y, model0, residuals=True )

        self.assertTrue( 2 == len( par1) )
        assertAAE( par1, par )
        self.assertTrue( model0.npchain == 2 )

        model1 = PolynomialModel( 2, fixed={2:0.0} )

        altfit = Fitter( self.x, model1 )

        par1 = altfit.fit( y )
        print( par, par1 )
        if plot :
            FitPlot.plotFit( self.x, y, model0 )

        self.assertTrue( 2 == len( par1) )
        assertAAE( par, par )

        error1 = altfit.monteCarloError( )
        print( "error = ", error1 )

    #  **************************************************************
    def testNormalize( self, plot=False ):
        """
        test normalized parameter, alternative for keepfixed.

        1.

        2.

        """
        print( "\n   Fitter Test 2 Normalize  \n" )
        model = PolynomialModel( 2 )

        sm = PowerModel( 1.0 )

        x = numpy.linspace( 0.0, 10.0, 101 )
        y = 1.0 + 0.5 * x - 0.2 * x * x +  numpy.random.randn( 101 ) * 0.1

        sm += model                     ## degenerate model par[0] == par[2]
        fitter = Fitter( x, sm )

        self.assertTrue( sm.npchain == 4 )
        self.assertRaises( numpy.linalg.linalg.LinAlgError, fitter.fit, y )

        fitter.normalize( [0.0, 0.0, 1.0, 0.0], 1.0 )       ## fix par[2] at 1.0

        par = fitter.fit( y )

        print( "param = ", sm.parameters )
        assertAAE( par[2], 1.0 )
        assertAAE( par, [ -0.5, 1.0, 1.0, -0.2], 1 )

        chisq = fitter.chisq
        print( "chisq = %f"%( chisq) )

        std = fitter.standardDeviations
        print( "stdev = ", std )

#        assertAAE( std, ast )

if __name__ == '__main__':
    unittest.main( )



