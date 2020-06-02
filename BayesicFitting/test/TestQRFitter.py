# run with : python3 -m unittest TestFitter

import numpy as numpy
import os
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

class TestQRFitter( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Compare results of QRFitter with Fitter.

    Author:      Do Kester

    """
    aa = 5              #  average offset
    bb = 2              #  slope
    ss = 0.3            #  noise Normal distr.

    x = numpy.asarray( [ -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
    x += 2
    noise = numpy.asarray( [-0.000996, -0.046035,  0.013656,  0.418449,  0.0295155,  0.273705,
      -0.204794,  0.275843, -0.415945, -0.373516, -0.158084] )

    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

    def eq( self, a, b, eps=1e-10 ) :
        if ( a + b ) != 0 :
            return abs( a - b ) / abs( a + b ) < eps
        else :
            return abs( a - b ) < eps



    #  **************************************************************
    def testStraightLineParameter( self ):
        """
        test slope fit

        1. Compare PolynomialModel(1) with chain of PowerModel(0) + PowerModel(1)

        2. Fix parameters in PolynomialModel

        """
        print( "\n   Fitter Test 1  \n" )
        plot = self.doplot

        model = PolynomialModel( 1 )
        fitter = Fitter( self.x, model )
        model0 = PowerModel( 0 )
        model1 = PowerModel( 1 )
        model0.addModel( model1 )
        altfit = QRFitter( self.x, model0 )
        yy = self.aa + self.bb * self.x
        y = yy + self.noise

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

        print( "   par  ", par, " stdv  ", std, chisq )

        numpy.random.seed( 9876 )
        for k in range( 5 ) :
            y1 = yy + 0.3 * numpy.random.randn( 11 )
            par1 = fitter.fit( y1 )
            std1 = fitter.stdevs
            chi1 = fitter.chisq
            print( k, " par  ", par1, " stdv  ", std1, chi1 )

        altfit.needsNewDecomposition = True
        par1 = altfit.fit( y, keep={0:par[0]} )
        print( par1, par )
        std1 = altfit.stdevs
        print( std, std1 )
        if plot :
            FitPlot.plotFit( self.x, y, model0 )

        self.assertTrue( 2 == len( par1) )
        assertAAE( par, par1 )

        self.assertTrue( model0.npchain == 2 )
        mp = model0.parameters
        print( mp, par, par1 )
        assertAAE( mp, par1 )

        altfit = QRFitter( self.x, model0, keep={0:par[0]+0.001} )


        par1 = altfit.fit( y )
        std1 = altfit.stdevs
        print( par, par1 )
        print( std, std1 )
        if plot :
            FitPlot.plotFit( self.x, y, model0 )

        self.assertTrue( 2 == len( par1) )
        assertAAE( par, par1, 3 )
        self.assertTrue( std1[0] == 0 )

        error1 = altfit.monteCarloError( )
        print( "error = ", error1 )


if __name__ == '__main__':
    unittest.main( )



