#run with: python3 -m unittest TestMonteCarlo

import unittest
import numpy as numpy
from numpy.testing import assert_array_almost_equal as assertAAE

from astropy import units
import math
import matplotlib.pyplot as pyplot


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
#  *  2016 Do Kester

class TestMonteCarlo( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author:      Do Kester

    """
    def testMonteCarlo1( self ):
        print( "====== MonteCarlo 1 ===================" )

        N = 100
        ran = numpy.random
        ran.seed( 12345 )
        noise = ran.standard_normal( N )
        x = numpy.arange( N, dtype=float ) - 3
        nn = 0.1
        for k in range( 5 ) :
            y = noise * nn

            m = PolynomialModel( 0 )
            ftr = Fitter( x, m )
            par = ftr.fit( y )
            std = ftr.getStandardDeviations()
            chisq = ftr.chisq

            mc = MonteCarlo( x, m, ftr.covariance )
            mc.mcycles = 1000
            lmce = ftr.monteCarloError( monteCarlo=mc )

            print( "noise  : ", fmt( nn ), "===========================================" )
            print( "params : ", fmt( par, format="%8.5f" ) )
            print( "stdevs : ", fmt( std, format="%8.5f" ) )
            print( "scale  : ", fmt( ftr.scale, format="%8.5f" ), fmt( nn ) )
            print( "chisq  : ", fmt( chisq, format="%8.5f" ),
                fmt( mc._eigenvalues, format="%8.5f" ), fmt( mc._eigenvectors, format="%8.5f" ) )
            print( "covar  : ", fmt( ftr.covariance, format="%8.5f" ) )
            print( "mcerr  : ", fmt( lmce[0], format="%8.5f" ) )
            self.assertTrue( abs( std[0] - lmce[0] ) < 0.1 * std[0] )
            self.assertTrue( par[0] < 0.05 * nn )
            nn *= 10



#        self.assertAlmostEqual( par, 0.0 )
#        self.assertAlmostEqual( par, 0.1 )
#        self.assertAlmostEqual( chisq, 0.857142857143 )

    def plotMonteCarlo2( self ):
        self.testMonteCarlo2( doplot=True )

    def testMonteCarlo2( self, doplot=False ):
        print( "====== MonteCarlo 2 ===================" )

        x = numpy.arange( 7, dtype=float ) - 3
        y = numpy.asarray( [-1,-1,-1,0,1,1,1], dtype=float )
        m = PolynomialModel( 1 )
        ftr = Fitter( x, m )
        par = ftr.fit( y )
        std = ftr.getStandardDeviations()
        yfit = m.result( x )
        chisq = ftr.chisq
        hes = ftr.hessian
#        mc = MonteCarlo( x, m, chisq, hessian=hes )
        mc = MonteCarlo( x, m, ftr.covariance )
        mc.mcycles = 1000
        lmce = ftr.monteCarloError( monteCarlo=mc )

        print( "params : ", par )
        print( "stdevs : ", std )
        print( "scale  : ", ftr.getScale() )
        print( "chisq  : ", chisq )
        print( "evals  : ", mc._eigenvalues )
        print( mc._eigenvectors )
        print( "hessi  :\n", ftr.hessian )
        print( "covar  :\n", ftr.covariance )
        print( "mcerr  : ", lmce )

        numpy.testing.assert_array_almost_equal( par, numpy.asarray([0.0,0.42857142857142855]) )
#        numpy.testing.assert_array_almost_equal( std, numpy.asarray([0.1564921592871903,0.07824607964359515]) )
        self.assertAlmostEqual( chisq, 0.857142857143 )

        if doplot :
            pyplot.plot( x, y, 'k*' )
            pyplot.plot( x, yfit, 'g-' )
            pyplot.plot( x, yfit+lmce, 'r-' )
            pyplot.plot( x, yfit-lmce, 'r-' )
            pyplot.show()

    def plotMonteCarlo3( self ):
        self.testMonteCarlo3( doplot=True )

    def testMonteCarlo3( self, doplot=False ):
        print( "====== MonteCarlo 3 ===================" )

        N = 101
        x = numpy.arange( N, dtype=float ) * 0.1
        ran = numpy.random
        ran.seed( 1235 )
        noise = ran.standard_normal( N )

        ym = x * x + 0.03 * x + 0.05
        y1 = ym + 10 * noise

        pm = PolynomialModel( 2 )

        ftr = Fitter( x, pm )

        pars1 = ftr.fit( y1 )
        stdv1 = ftr.getStandardDeviations( )
        print( "parameters : ", pars1 )
        print( "std devs   : ", stdv1 )
        print( "chisquared : ", ftr.chisq )

        lmce = ftr.monteCarloError( )
        chisq = ftr.chisq

        mce = MonteCarlo( x, pm, ftr.covariance )
        mce1 = mce.getError( )
        assertAAE( lmce, mce1 )

        yfit = pm.result( x )
        s2 = numpy.sum( numpy.square( ( yfit - ym ) / lmce ) )
        print( s2, math.sqrt( s2 / N ) )

        integral = numpy.sum( yfit )
        s1 = 0
        s2 = 0
        k = 0
        for k in range( 1, 100001 ):
            rv = mce.randomVariant( x )
            s1 += numpy.sum( rv )
            s2 += numpy.sum( numpy.square( rv - yfit ) )
            if k % 10000 == 0:
                print( "%6d  %10.3f %10.3f %10.3f" % ( k, integral, s1/k, math.sqrt( s2/k ) ) )

        ### TBC  dont know why the factor 1000 is there. ########
        print( abs( integral - s1/k ), math.sqrt( s2/( k * 1000 ) ) )
        self.assertTrue( abs( integral - s1/k ) < math.sqrt( s2/( k * 1000 ) ) )

        if doplot :
            pyplot.plot( x, y1, 'b.' )

            pyplot.plot( x, ym, 'k-' )
            pyplot.plot( x, yfit, 'g-' )
            pyplot.plot( x, yfit+lmce, 'r-' )
            pyplot.plot( x, yfit-lmce, 'r-' )
            pyplot.show()

    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestMonteCarlo.__class__ )


if __name__ == '__main__':
    unittest.main()


