# run with : python3 -m unittest TestRobustShell

import unittest
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt
from numpy.testing import assert_array_almost_equal as assertAAE

from BayesicFitting import *
from BayesicFitting import formatter as fmt

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
#  *    2004 SRON, Do Kester

class TestRobustShell( unittest.TestCase ):
    """
    Test harness for RobustShell.

    Author       Do Kester

    """
    def plot1( self ) :
        self.test1( plot=True )
        plt.show()

    def plot2( self ) :
        self.test2( plot=True )
        plt.show()

    #  **************************************************************
    def test1( self, plot=False ):
        """     #   test slope fit  """

        print( "\n   Robust fitter Test 1  \n" )

        ndata = 101
        aa = 5.0            #  average offset
        bb = 2.0            #  slope
        ss = 0.3            #  noise Normal distr.

        x = numpy.linspace( -1, +1, ndata, dtype=float )
        numpy.random.seed( 12345 )
        y = aa + bb * x + ss * numpy.random.randn( ndata )

        model = PolynomialModel( 1 )
        fitter = Fitter( x, model )

        print( "Testing Straight Line fit" )

        par = fitter.fit( y )
        std = fitter.stdevs
        chisq = fitter.chisq
        print( "truth   " + fmt( aa ) + fmt( bb ) )
        print( "params  " + fmt( par ) )
        print( "stdevs  " + fmt( std ) )
        print( "chisq   " + fmt( chisq ) )
        assertAAE( par, numpy.asarray( [aa, bb] ), 2 )

        if plot :
            plt.plot( x, y, 'k.' )
            plt.plot( x, model( x ), 'k-' )

        # make some outliers
        ko = [10*k+4 for k in range( 10 )]
        ko = numpy.asarray( ko )
        y[ko] += numpy.linspace( -5, 2, 10 )

        romod = PolynomialModel( 1 )
        altfit = Fitter( x, romod )
        alt = altfit.fit( y )
        ast = altfit.stdevs
        altch = altfit.chisq
        print( "params  " + fmt( alt ) )
        print( "stdevs  " + fmt( ast ) )
        print( "chisq   " + fmt( altch ) )

        if plot :
            plt.plot( x, romod( x ), 'b-' )

        rf = RobustShell( altfit )
        Tools.printclass( rf )

        alt = rf.fit( y )
        ast = altfit.stdevs
        altch = altfit.chisq
        print( rf )
        print( "params  " + fmt( alt ) )
        print( "stdevs  " + fmt( ast ) )
        print( "chisq   " + fmt( altch ) + fmt( rf.scale ) )
        print( "weight  " + fmt( rf.weights[ko], max=None ) )
        if plot :
            plt.plot( x, romod( x ), 'g-' )
            plt.plot( x, rf.weights, 'g-' )
        assertAAE( par, alt, 1 )
        assertAAE( std, ast, 1 )

        rf = RobustShell( altfit, kernel=Cosine(), domain=4.0 )
        alt = rf.fit( y )
        ast = altfit.stdevs
        altch = altfit.chisq
        print( rf )
        print( "params  " + fmt( alt ) )
        print( "stdevs  " + fmt( ast ) )
        print( "chisq   " + fmt( altch ) + fmt( rf.scale ) )
        print( "weight  " + fmt( rf.weights[ko], max=None ) )
        if plot :
            plt.plot( x, romod( x ), 'r-' )
            plt.plot( x, rf.weights, 'r-' )
        assertAAE( par, alt, 1 )
        assertAAE( std, ast, 1 )

        rf = RobustShell( altfit, kernel=Huber, domain=1.0 )
#        rf.setNoiseScale( 0.3 )
        alt = rf.fit( y )
        ast = altfit.stdevs
        altch = altfit.chisq
        print( rf )
        print( "params  " + fmt( alt ) )
        print( "stdevs  " + fmt( ast ) )
        print( "chisq   " + fmt( altch ) + fmt( rf.scale ) )
        print( "weight  " + fmt( rf.weights[ko], max=None ) )
        if plot :
            plt.plot( x, romod( x ), 'c-' )
            plt.plot( x, rf.weights, 'c-' )
        assertAAE( par, alt, 1 )
        assertAAE( std, ast, 1 )

        rf = RobustShell( altfit, kernel=Uniform )
        alt = rf.fit( y )
        ast = altfit.stdevs
        altch = altfit.chisq
        print( rf )
        print( "params  " + fmt( alt ) )
        print( "stdevs  " + fmt( ast ) )
        print( "chisq   " + fmt( altch ) + fmt( rf.scale ) )
        print( "weight  " + fmt( rf.weights[ko], max=None ) )
        if plot :
            plt.plot( x, romod( x ), 'm-' )
            plt.plot( x, rf.weights, 'm-' )
        assertAAE( par, alt, 1 )
        assertAAE( std, ast, 1 )

    def test2( self, plot=False ):

        ndata = 101
        c0 = 3.2
        c1 = -0.1
        c2 = 0.3
        c3 = 1.1
        c4 = 2.1
        ss = 0.2

        x = numpy.linspace( -1, +1, ndata, dtype=float )
        y = ( x - c1 ) / c2
        numpy.random.seed( 12345 )
        y = c0 * numpy.exp( -0.5 * y * y ) + x * c3 + c4 + ss * numpy.random.randn( ndata )

        print( "Testing Nonlinear Fitters with RobustShell." )

        print( fmt( [c0,c1,c2,c4,c3] ) )

        modl2 = GaussModel( )
        modl2 += PolynomialModel( 1 )

#        lmfit = CurveFitter( x, modl2 )
        lmfit = LevenbergMarquardtFitter( x, modl2 )
        par2 = lmfit.fit( y )
        std2 = lmfit.stdevs
        print( fmt( par2, max=5 ) )
        print( fmt( std2, max=5 ) )

        # make some outliers
        ko = [10*k+4 for k in range( 10 )]
        ko = numpy.asarray( ko )
        y[ko] += numpy.linspace( -5, 2, 10 )

        if plot :
            plt.plot( x, y, 'k.' )
            plt.plot( x, modl2( x ), 'k-' )


#        lmfit = CurveFitter( x, modl2 )
        lmfit = LevenbergMarquardtFitter( x, modl2 )
#        lmfit.setParameters( initpar2 )
        rf = RobustShell( lmfit )
#        rf.setVerbose( 1 )
        print( str( rf ) )
        par1 = rf.fit( y )
        std1 = rf.stdevs
        print( fmt( par1, max=5 ) )
        print( fmt( std1, max=5 ) )
        print( fmt( par2, max=5 ) )
        print( fmt( rf.weights[ko], max=20 ) )
        if plot :
            plt.plot( x, modl2( x ), 'g-' )
            plt.plot( x, rf.weights, 'g-' )
        assertAAE( par2, par1, 1 )
        assertAAE( std2, std1, 1 )



#        lmfit = CurveFitter( x, modl2 )
        lmfit = LevenbergMarquardtFitter( x, modl2 )
#        lmfit.setParameters( initpar2 )
        rf = RobustShell( lmfit, onesided="negative" )
#        rf.setVerbose( 1 )
        print( rf )
        par3 = rf.fit( y )
        std3 = rf.stdevs
        print( fmt( par3, max=5 ) )
        print( fmt( std3, max=5 ) )
        print( fmt( par2, max=5 ) )
        print( fmt( rf.weights[ko], max=20 ) )

        if plot :
            plt.plot( x, modl2( x ), 'r-' )
            plt.plot( x, rf.weights, 'r-' )
        assertAAE( par2, par3, 1 )
        assertAAE( std2, std3, 1 )


    def suite( cls ):
        return unittest.TestCase.suite( TestRobustShell.__class__ )

if __name__ == '__main__':
    unittest.main( )

