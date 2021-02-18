# run with : python3 -m unittest TestEngine2

import unittest
import os
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt

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
#  *  2006 Do Kester

class TestEngine2( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author       Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )


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

    def testRandomEngine( self ):
        print( "\n   Random Engine Test\n" )
        self.stdenginetest( RandomEngine, iter=200, nsamp=10, plot=self.doplot )

    def testGibbsEngine( self ):
        print( "\n   Gibbs Engine Test\n" )
        self.stdenginetest( GibbsEngine, iter=101, nsamp=10, plot=self.doplot )

    def testStepEngine( self ):
        print( "\n   Step Engine Test\n" )
        self.stdenginetest( StepEngine, iter=1001, nsamp=10, plot=self.doplot )

#    def testCrossEngine( self ):
#        print( "\n   Cross Engine Test\n" )
#        self.stdenginetest( CrossEngine, iter=800, nsamp=100, plot=self.doplot )

    def testGalileanEngine( self ):
        print( "\n   Galilean Engine Test\n" )
        self.stdenginetest( GalileanEngine, iter=201, nsamp=10, plot=self.doplot )

    def testChordEngine( self ):
        print( "\n   Chord Engine Test\n" )
        self.stdenginetest( ChordEngine, iter=100, nsamp=10, plot=self.doplot )

    def stdenginetest( self, myengine, nsamp=4, iter=100, plot=False ) :
        m, xdata, data = self.initEngine()
        problem = ClassicProblem( m, xdata=xdata, ydata=data )

        Tools.printclass( problem )
        errdis = GaussErrorDistribution( scale=0.5 )
        Tools.printclass( errdis )

        allpars = numpy.append( m.parameters, [0.5] )
        fitIndex = [0,1]
        wl = WalkerList( problem, nsamp, allpars, fitIndex )

        map = numpy.ndarray( (41,21), dtype=float )
        mmx = -math.inf
        for k0 in range( 21 ) :
            for k1 in range( 41 ) :
                pl = [k0-10, 0.25*k1, 0.5]
                map[k1,k0] = errdis.logLikelihood( problem, pl )
                if map[k1,k0] > mmx :
                    mmx = map[k1,k0]
                    mk1 = k1 / 4
                    mk0 = k0 - 10

#        print( map )
        print( mk0, mk1, mmx )

        ax = numpy.linspace( -10, 10, 21 )
        ay = numpy.linspace(   0, 10, 41 )
        v = [-500000,-100000,-50000,-10000,-5000, -3000, -1000, -500, -300, -200]

        engine = StartEngine( wl, errdis )
        Tools.printclass( engine.walkers[0] )
        for kw in range( len( engine.walkers ) ) :
            engine.execute( kw, -math.inf )

        pevo = wl.getParameterEvolution()
        if plot :
            plt.figure( str( myengine ) )
            plt.contour( ax, ay, map, v )
            plt.plot( [mk0], [mk1], 'k*' )
            plt.plot( pevo[:,0], pevo[:,1], 'k.' )

        col = ['k-', 'r-', 'g-', 'b-']
        engine = myengine( wl, errdis )
        for k in range( iter ) :
            lowL, klo = wl.getLowLogL()
            p0 = wl[klo].allpars[:2]
            engine.calculateUnitRange()
            while True :
                kok = engine.rng.randint( 0, nsamp )
                if kok != klo :
                    wl[klo].allpars = wl[kok].allpars.copy()
                    break

            engine.execute( klo, lowL )
            p1 = wl[klo].allpars[:2]
            if k % 100 == 0 :
                print( k, klo, fmt(p1), fmt(wl[klo].logL) )

            if plot :
                plt.plot( [p0[0],p1[0]], [p0[1],p1[1]], col[klo%4] )

        print( lowL, p1 )
        print( mmx, mk0, mk1 )
        engine.printReport()


#        engine.printReport()
        if plot :
            pevo = wl.getParameterEvolution()
            plt.plot( pevo[:,0], pevo[:,1], 'r.' )
            plt.show()

        print( lowL, mmx )
        print( p1[0], mk0, abs( p1[0] - mk0 ) )
        print( p1[1], mk1, abs( p1[1] - mk1 ) )

        self.assertTrue( lowL > mmx )
        self.assertTrue( abs( p1[0] - mk0 ) < 1 )
        self.assertTrue( abs( p1[1] - mk1 ) < 1 )


    def suite( cls ):
        return unittest.TestCase.suite( TestEngine2.__class__ )


if __name__ == '__main__':
    unittest.main( )


