# run with : python3 -m unittest TestEngine2

import unittest
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt

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
#  *  2006 Do Kester

class TestEngine2( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author       Do Kester

    """
    def __init__( self, name ):
        super( TestEngine2, self ).__init__( name )


    def initEngine( self, order=1, np=101 ):
        m = PolynomialModel( order )

        up1 = UniformPrior( limits=[-10,10])
        up2 = UniformPrior( limits=[  0,10] )

        m.priors = [up1, up2]

        xdata = numpy.linspace( 0.0, 10.0, np )
        data = numpy.ceil( numpy.arange( np, dtype=float ) / 2.3 + 2.4 )
        numpy.random.seed( 345345 )
        data += 0.4 * numpy.random.randn( np )
#        print( data )
        numpy.set_printoptions( precision=3, suppress=True )
        return ( m, xdata, data )

    def plotall( self ) :
        self.testRandomEngine( plot=True )
        self.testGibbsEngine( plot=True )
        self.testStepEngine( plot=True )
        self.testGalileanEngine( plot=True )


    def plotRandomEngine( self ):
        self.testRandomEngine( plot=True )

    def testRandomEngine( self, plot=False ):
        print( "\n   Random Engine Test\n" )
        self.stdenginetest( RandomEngine, iter=200, nsamp=10, plot=plot )

    def plotGibbsEngine( self ):
        self.testGibbsEngine( plot=True )

    def testGibbsEngine( self, plot=False ):
        print( "\n   Gibbs Engine Test\n" )
        self.stdenginetest( GibbsEngine, iter=101, nsamp=10, plot=plot )

    def plotStepEngine( self ):
        self.testStepEngine( plot=True )

    def testStepEngine( self, plot=False ):
        print( "\n   Step Engine Test\n" )
        self.stdenginetest( StepEngine, iter=1001, nsamp=10, plot=plot )

#    def plotCrossEngine( self ):
#        self.testCrossEngine( plot=True )

#    def testCrossEngine( self, plot=False ):
#        print( "\n   Cross Engine Test\n" )
#        self.stdenginetest( CrossEngine, iter=800, nsamp=100, plot=plot )

    def plotGalileanEngine( self ):
        self.testGalileanEngine( plot=True )

    def testGalileanEngine( self, plot=False ):
        print( "\n   Galilean Engine Test\n" )
        self.stdenginetest( GalileanEngine, iter=101, nsamp=10, plot=plot )

    def stdenginetest( self, myengine, nsamp=4, iter=100, plot=False ) :
        m, xdata, data = self.initEngine()
        errdis = GaussErrorDistribution( xdata, data, scale=0.5 )
        Tools.printclass( errdis )

        sl = SampleList( m, nsamp, errdis )
        map = numpy.ndarray( (41,21), dtype=float )
        mmx = -math.inf
        for k0 in range( 21 ) :
            for k1 in range( 41 ) :
                pl = [k0-10, 0.25*k1, 0.5]
                map[k1,k0] = errdis.logLikelihood( m, pl )
                if map[k1,k0] > mmx :
                    mmx = map[k1,k0]
                    mk1 = k1 / 4
                    mk0 = k0 - 10

#        print( map )
        print( mk0, mk1, mmx )

        ax = numpy.linspace( -10, 10, 21 )
        ay = numpy.linspace(   0, 10, 41 )
        v = [-500000,-100000,-50000,-10000,-5000, -3000, -1000, -500, -300, -200]

        engine = StartEngine( sl, errdis )
        Tools.printclass( engine.walkers[0] )
        for samp in engine.walkers :
            engine.execute( samp, -math.inf )

        pevo = sl.getParameterEvolution()

        if plot :
            plt.figure( str( myengine ) )
            plt.contour( ax, ay, map, v )
            plt.plot( [mk0], [mk1], 'k*' )
            plt.plot( pevo[:,0], pevo[:,1], 'k.' )

        col = ['k-', 'r-', 'g-', 'b-']
        engine = myengine( sl, errdis )
        for k in range( iter ) :
            lowL, klo = sl.getLowLogL()
            p0 = sl[klo].allpars[:2]
            engine.calculateUnitRange()
            while True :
                kok = engine.rng.randint( 0, nsamp )
#                print( klo, kok )
                if kok != klo :
                    sl[klo].allpars = sl[kok].allpars.copy()
                    break
            engine.execute( sl[klo], lowL )
            p1 = sl[klo].allpars[:2]
            if k % 50 == 0 :
                print( k, klo, p1, sl[klo].logL )

            if plot :
                plt.plot( [p0[0],p1[0]], [p0[1],p1[1]], col[klo%4] )

        print( lowL, p1 )
        print( mmx, mk0, mk1 )

#        engine.printReport()
        if plot :
            pevo = sl.getParameterEvolution()
            plt.plot( pevo[:,0], pevo[:,1], 'r.' )
            plt.show()

        self.assertTrue( lowL > mmx )
        self.assertTrue( abs( p1[0] - mk0 ) < 1 )
        self.assertTrue( abs( p1[1] - mk1 ) < 1 )


    def suite( cls ):
        return unittest.TestCase.suite( TestEngine2.__class__ )


if __name__ == '__main__':
    unittest.main( )


