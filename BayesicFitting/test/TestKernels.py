# run with : python3 -m unittest TestKernels

import unittest
import os
import numpy as numpy
from astropy import units
import matplotlib.pyplot as plt
import warnings

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

class TestKernels( unittest.TestCase ):
    """
    Test harness for Models

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )


    def testHuber( self ) :
        kernel = Huber()
        xhm = kernel.fwhm / 2
        self.assertAlmostEqual( kernel.result( xhm ), 0.5 )
        self.assertAlmostEqual( kernel.result( -xhm ), 0.5 )
        if self.doplot :
            self.plotK( [Huber] )



    def testKernels( self ):
        kernels = [Gauss, Lorentz, Sinc, Biweight, Cosine, CosSquare, Parabola, Triangle,
                   Tricube, Triweight, Uniform]
        if self.doplot :
            self.plotK( kernels )

        for kernl in kernels :
            kernel = kernl()
            self.stdKerneltest( kernel, plot=self.doplot )
            self.assertTrue( kernel.isBound() or ( kernl in kernels[:3] ) )


    def testTHC( self ) :
        x = numpy.linspace( -5, 5, 1001 )
        for kc in range( 7 ) :

            kernel = Tophat( nconv=kc )
            print( "****"  , kernel, "  *************************" )

            y = kernel.result( x )
            top = y[500]

            kernin = numpy.sum( y ) / 100
            self.assertAlmostEqual( kernin, kernel.integral )

            print( kc, top, numpy.sum( y )/100 )
            if self.doplot :
                plt.plot( x, kernel.result( x ) )
                plt.plot( x, kernel.partial( x ) )

            self.stdKerneltest( kernel )

        if self.doplot :
            plt.show()

    def testonex( self ) :
        sc = Sinc()
        ysc = sc.result( 0.0 )
        print( "sinc  ", ysc, ysc.__class__ )

        un = Uniform()
        yun = un.result( 0.0 )
        print( "unif  ", yun, yun.__class__ )

        for n in range( 7 ) :
            thc = Tophat( nconv=n )
            ytc = thc.result( 0.0 )
            print( "thc%d  " % n, ytc, ytc.__class__ )



    def stdKerneltest( self, kernel, plot=None ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        x += 0.02

        model = KernelModel( kernel=kernel )
        print( "********************************************" )
        print( model )

        numpy.set_printoptions( precision=3, suppress=False )

        par = [1.0,0.0,1.0]
        print( model.partial( x, par ) )
        model.testPartial( x[5], model.parameters )

        model.testPartial( x[0], par )
        model.xUnit = units.m
        model.yUnit = units.kg
        for k in range( model.getNumberOfParameters() ):
            print( "%d  %-12s  %-12s"%(k, model.getParameterName( k ), model.getParameterUnit( k ) ) )

        xx = numpy.linspace( 0, 101, 101000 )
        yy = model.result( xx )
        sn = numpy.sum( yy ) / 500
        ss = kernel.integral

        print( "Integral   ", sn, model.getIntegralUnit( ) )
        self.assertAlmostEqual( sn, 1.0, 1 )
        self.assertAlmostEqual( ss, 1.0 / model.parameters[0], 4 )

        xhm = kernel.fwhm / 2
        yhm = model.result( xhm )[0]
        self.assertAlmostEqual( yhm, model.result( -xhm ) )
        y0 = model.result( 0.0 )[0]
        print( xhm, yhm, y0, yhm / y0, yhm.__class__ )

        self.assertAlmostEqual( (yhm / y0), 0.5 )

        part = model.partial( x, par )
        nump = model.numPartial( x, par )
        print( part.shape, nump.shape )
        for k in range( 11 ) :
            print( "%3d %8.3f"%(k, x[k]), part[k,:], nump[k,:] )

        k = 0
        np = model.npbase
        for (pp,nn) in zip( part.flatten(), nump.flatten() ) :
            print( "%3d %10.4f  %10.4f %10.4f"%(k, x[k//np], pp, nn) )
            self.assertAlmostEqual( pp, nn, 3 )
            k += 1

        mc = model.copy( )
        for k in range( mc.getNumberOfParameters() ):
            print( "%d  %-12s  %-12s"%(k, mc.getParameterName( k ), mc.getParameterUnit( k ) ) )
        mc.parameters = par
        model.parameters = par

        for (k,xk,r1,r2) in zip( range( x.size ), x, model.result( x ), mc.result( x ) ) :
            print( "%3d %8.3f  %10.3f %10.3f" % ( k, xk, r1, r2 ) )
            self.assertEqual( r1, r2 )

    def plotK( self, kernels ) :
        x = numpy.linspace( -5, +5, 1001 )
        par = [1.0,0.0,1.0]
        for kernel in kernels :
            model = kernel()
            print( model )
            y = model.result( x )
            plt.plot( x, y, '-', linewidth=2 )
            x2 = numpy.linspace( -4, +4, 11 )
            dy = model.partial( x2 )
            print( dy )
            yy = model.result( x2 )
            print( yy )
            for k in range( 11 ) :
                x3 = numpy.asarray( [-0.05, +0.05] )
                y3 = x3 * dy[k] + yy[k]
                plt.plot( x2[k] + x3, y3, 'r-' )

        plt.show()


    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestModels.__class__ )

if __name__ == '__main__':
    unittest.main( )


