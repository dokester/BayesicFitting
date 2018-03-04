# run with : python3 -m unittest TestEngine3

import unittest
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

class TestEngine3( unittest.TestCase ):
    """
    Test harness for Engines

    Author       Do Kester

    """
    def __init__( self, name ):
        super( TestEngine3, self ).__init__( name )


    def plotRandomEngine( self ):
        self.testRandomEngine(plot=True )

    def testRandomEngine( self, plot=False ):
        print( "\n   Random Engine Test\n" )
        self.stdenginetest( RandomEngine, nsamp=10, plot=plot )

    def plotGibbsEngine( self ):
        self.testGibbsEngine( plot=True )

    def testGibbsEngine( self, plot=False ):
        print( "\n   Gibbs Engine Test\n" )
        self.stdenginetest( GibbsEngine, nsamp=10, plot=plot )

    def plotGibbsEngine2( self ):
        self.testGibbsEngine2( plot=True )

    def testGibbsEngine2( self, plot=False ):
        print( "\n   Gibbs Engine Test 2\n" )
        self.stdenginetest2( GibbsEngine, nsamp=10, lowL=-200, plot=plot )
        self.stdenginetest2( GibbsEngine, nsamp=10, lowL=-170, plot=plot )
        self.stdenginetest2( GibbsEngine, nsamp=10, lowL=-165, plot=plot )
        self.stdenginetest2( GibbsEngine, nsamp=10, lowL=-163, plot=plot )

    def plotStepEngine( self ):
        self.testStepEngine( plot=True )

    def testStepEngine( self, plot=False ):
        print( "\n   Step Engine Test 2\n" )
        self.stdenginetest2( StepEngine, nsamp=10, lowL=-200, plot=plot )
        self.stdenginetest2( StepEngine, nsamp=10, lowL=-170, plot=plot )
        self.stdenginetest2( StepEngine, nsamp=10, lowL=-165, plot=plot )
        self.stdenginetest2( StepEngine, nsamp=10, lowL=-163, plot=plot )

    def plotGalileanEngine( self ):
        self.testGalileanEngine( plot=True )

    def testGalileanEngine( self, plot=False ):
        print( "\n   Galilean Engine Test\n" )
        self.stdenginetest( GalileanEngine, nsamp=10, plot=plot )

    def plotGalileanEngine2( self ):
        self.testGalileanEngine2( plot=True )

    def testGalileanEngine2( self, plot=False ):
        print( "\n   Galilean Engine Test 2\n" )
        self.stdenginetest2( GalileanEngine, nsamp=10, lowL=-200, plot=plot )
        self.stdenginetest2( GalileanEngine, nsamp=10, lowL=-170, plot=plot )
        self.stdenginetest2( GalileanEngine, nsamp=10, lowL=-165, plot=plot )
        self.stdenginetest2( GalileanEngine, nsamp=10, lowL=-163, plot=plot )

    def initEngine( self, order=1, np=101 ):
        m = PolynomialModel( order )

        up1 = UniformPrior( limits=[-1.0,1.0])
        up2 = UniformPrior( limits=[-1.0,1.0] )

        m.priors = [up1, up2]

        xdata = numpy.linspace( -1.0, 1.0, np, dtype=float )
        data = -0.4 * xdata + 0.5

        numpy.random.seed( 345345 )
        numpy.set_printoptions( precision=3, suppress=True )
        return ( m, xdata, data )

    def stdenginetest( self, myengine, nsamp=4, plot=False ) :
        m, xdata, data = self.initEngine()
        sigma = 2.0
        errdis = GaussErrorDistribution( xdata, data )
        errdis.keepFixed( {0: sigma} )
        sl = SampleList( m, nsamp, errdis )
        map = numpy.ndarray( (21,21), dtype=float )
        mmx = -math.inf
        for k0 in range( 21 ) :
            for k1 in range( 21 ) :
                pl = [k0/10-1, k1/10-1, sigma]
                map[k1,k0] = errdis.logLikelihood( m, pl )
                if map[k1,k0] > mmx :
                    mmx = map[k1,k0]
                    mk1 = k1/10 - 1
                    mk0 = k0/10 - 1

#        print( map )
#        print( mk0, mk1, mmx )

        ay = numpy.linspace( -1, 1, 21 )
        ax = numpy.linspace( -1, 1, 21 )
        v = [-200, -170, -165, -163]

        lowL = -170

        engine = StartEngine( sl, errdis )
        for samp in engine.walkers :
            while True :
                engine.execute( samp, -math.inf )
                if samp.logL > lowL : break

        engine = myengine( sl, errdis )
        engine.plotter = Plotter()

        pevo = sl.getParameterEvolution()
        for k in range( 5 ) :
            engine.plotter.iter = 1
            plt.figure( str( myengine ) )
            plt.contour( ax, ay, map, v )
            plt.plot( [mk0], [mk1], 'k*' )

            klo = engine.rng.randint( 0, nsamp )

            p0 = sl[klo].allpars[:2]
            plt.plot( p0[0], p0[1], 'k.' )
            engine.calculateUnitRange()

            engine.execute( sl[klo], lowL )
            p1 = sl[klo].allpars[:2]

            print( klo, p1, sl[klo].logL )
            plt.show()


    def stdenginetest2( self, myengine, nsamp=4, lowL=-170, plot=False ) :
        m, xdata, data = self.initEngine()
        sigma = 2.0
        errdis = GaussErrorDistribution( xdata, data )
        errdis.keepFixed( {0: sigma} )
        sl = SampleList( m, nsamp, errdis )

        engine = StartEngine( sl, errdis )
        for samp in engine.walkers :
            while True :
                engine.execute( samp, -math.inf )
                if samp.logL > lowL : break

        pevo = sl.getParameterEvolution()
#        print( fmt( pevo ) )
        pmin = numpy.min( pevo, 0 )
        pmax = numpy.max( pevo, 0 )
        pran = ( pmax - pmin ) / 2
#        print( fmt( pmin ), fmt( pmax ), fmt( pran ) )
        pmin -= pran
        pmax += pran

        map = numpy.ndarray( (21,21), dtype=float )
        mmx = -math.inf
#        print( fmt(pmin), fmt(pmax) )
#        print( fmt(m.priors[0].lowLimit), fmt(m.priors[0].highLimit) )
#        print( fmt(m.priors[1].lowLimit), fmt(m.priors[1].highLimit) )

        ax = numpy.linspace( max( pmin[0], m.priors[0].lowLimit ),
                min( pmax[0], m.priors[0].highLimit ), 21 )
        ay = numpy.linspace( max( pmin[1], m.priors[1].lowLimit ),
                min( pmax[1], m.priors[1].highLimit ), 21 )

        for k0,p0 in enumerate( ax ) :
            for k1,p1 in enumerate( ay ) :
                pl = [p0, p1, sigma]
                map[k1,k0] = errdis.logLikelihood( m, pl )
                if map[k1,k0] > mmx :
                    mmx = map[k1,k0]
                    mk1 = p1
                    mk0 = p0

#        print( map )
        print( mk0, mk1, mmx )



        plt.figure( str( myengine ) )
        v = [-200, -170, -165, -163]
        plt.contour( ax, ay, map, v )
#        plt.plot( [mk0], [mk1], 'k*' )
        plt.xlabel( "Param[0]" )
        plt.ylabel( "Param[1]" )

        engine = myengine( sl, errdis )
        klo = engine.rng.randint( 0, nsamp )

        p0 = sl[klo].allpars[:2]
        engine.calculateUnitRange()

        for k in range( 100 ) :
            sl[klo].allpars[:2] = p0
            engine.execute( sl[klo], lowL )
            p1 = sl[klo].allpars[:2]
            plt.plot( p1[0], p1[1], 'r.' )

        plt.plot( p0[0], p0[1], 'k*' )
        plt.show()

    def suite( cls ):
        return unittest.TestCase.suite( TestEngine2.__class__ )


class Plotter( object ) :

    def __init__( self, iter=1 ) :
        self.iter = iter
        self.col = ['k-', 'r-', 'g-', 'b-', 'm->']

    def start( self ):
        """ start the plot. """
        pass

    def move( self, param, ptry, col=None ):
        """
        Move parameters at position param to ptry using color col.
        """
        plt.plot( [param[0], ptry[0]], [param[1], ptry[1]], self.col[col] )
        plt.text( ptry[0], ptry[1], "%d"%self.iter )
        self.iter += 1

    def stop( self ):
        """ Stop (show) the plot. """
        pass


if __name__ == '__main__':
    unittest.main( )


