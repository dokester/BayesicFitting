# run with : python3 -m unittest TestEngine3

import unittest
import numpy as numpy
from astropy import units
import math

from BayesicFitting import *
from BayesicFitting import formatter as fmt
from Sphere import Sphere

import matplotlib.pyplot as plt


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

    def plotRandomEngine( self ):
        self.testRandomEngine(plot=True )

    def testRandomEngine( self, plot=False ):
        print( "\n   Random Engine Test\n" )
        self.stdenginetest( RandomEngine, nsamp=10, plot=plot )

    def plotGibbsEngine( self ):
        self.testGibbsEngine( plot=True )

    def testGibbsEngine( self, plot=False ):
        print( "\n   Gibbs Engine Test\n" )
        self.stdenginetest( GibbsEngine, nsamp=100, seed=789, plot=plot )
        self.stdenginetest( GibbsEngine, nsamp=10, seed=456, plot=plot )
        self.stdenginetest( GibbsEngine, nsamp=10, seed=123, plot=plot )

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
        print( "\n   Step Engine Test\n" )
        self.stdenginetest( StepEngine, nsamp=100, seed=321, plot=plot )
        self.stdenginetest( StepEngine, nsamp=100, seed=654, plot=plot )
        self.stdenginetest( StepEngine, nsamp=100, seed=987, plot=plot )
        self.stdenginetest( StepEngine, nsamp=100, seed=100, plot=plot )

    def plotGalileanEngine( self ):
        self.testGalileanEngine( plot=True )

    def testGalileanEngine( self, plot=False ):
        print( "\n   Galilean Engine Test\n" )
        self.stdenginetest( GalileanEngine, nsamp=100, seed=121, plot=plot )
        self.stdenginetest( GalileanEngine, nsamp=100, seed=132, plot=plot )
        self.stdenginetest( GalileanEngine, nsamp=100, seed=142, plot=plot )

    def plotGalileanEngine2( self ):
        self.testGalileanEngine2( plot=True )

    def testGalileanEngine2( self, plot=False ):
        print( "\n   Galilean Engine Test 2\n" )
        self.stdenginetest2( GalileanEngine, nsamp=10, lowL=-200, plot=plot )
        self.stdenginetest2( GalileanEngine, nsamp=10, lowL=-170, plot=plot )
        self.stdenginetest2( GalileanEngine, nsamp=10, lowL=-165, plot=plot )
        self.stdenginetest2( GalileanEngine, nsamp=10, lowL=-163, plot=plot )

    def testGalileanEngine3( self, plot=False ):
        print( "\n   Galilean Engine Test 3\n" )
#        self.stdenginetest3( GalileanEngine, nsamp=1000, order=2, plot=2 )
#        self.stdenginetest3( GalileanEngine, nsamp=4, order=10, plot=2 )
        self.stdenginetest3( GalileanEngine, nsamp=100, order=100, plot=1 )


    def plotChordEngine( self ):
        self.testChordEngine( plot=True )

    def testChordEngine( self, plot=False ):
        print( "\n   Chord Engine Test\n" )
        self.stdenginetest( ChordEngine, nsamp=100, seed=4213, plot=plot )
        self.stdenginetest( ChordEngine, nsamp=100, seed=4214, plot=plot )
        self.stdenginetest( ChordEngine, nsamp=100, seed=4215, plot=plot )

    def plotChordEngine2( self ):
        self.testChordEngine2( plot=True )

    def testChordEngine2( self, plot=False ):
        print( "\n   Chord Engine Test 2\n" )
        self.stdenginetest2( ChordEngine, nsamp=10, lowL=-200, plot=plot )
        self.stdenginetest2( ChordEngine, nsamp=10, lowL=-170, plot=plot )
        self.stdenginetest2( ChordEngine, nsamp=10, lowL=-165, plot=plot )
        self.stdenginetest2( ChordEngine, nsamp=10, lowL=-163, plot=plot )

    def testChordEngine3( self, plot=False ):
        print( "\n   Chord Engine Test 3\n" )
#        self.stdenginetest3( ChordEngine, nsamp=10, order=2, plot=1 )
#        self.stdenginetest3( ChordEngine, nsamp=10, order=10, plot=1 )
        self.stdenginetest3( ChordEngine, nsamp=100, order=100, plot=1 )

    def testCompare3( self, plot=False ):
        print( "\n   Compare Galilean and Chord Engine Test 3\n" )
        self.stdenginetest3( GalileanEngine, nsamp=100, order=2, plot=1 )
        self.stdenginetest3( ChordEngine, nsamp=100, order=2, plot=1 )
        self.stdenginetest3( GalileanEngine, nsamp=100, order=10, plot=1 )
        self.stdenginetest3( ChordEngine, nsamp=100, order=10, plot=1 )
        self.stdenginetest3( GalileanEngine, nsamp=100, order=100, plot=1 )
        self.stdenginetest3( ChordEngine, nsamp=100, order=100, plot=1 )

    def testEngine( self, myengine, plot=False ) :
        print( "\n   Uniform Engine Test\n" )

        numpy.random.seed( 123456789 )

        np = 10     ## number of parameters
        knots = numpy.arange( np+1, dtype=float )
        mdl = SplinesModel( knots=knots, order=0 )
        mdl.setLimits( lowLimits=-2, highLimits=2 )

        nd = 10
        nx = nd * np
        xdata = ( numpy.arange( nx, dtype=float ) + 0.5 ) / nd
        yd = numpy.random.rand( nx )
        yd -= numpy.mean( yd )
        ydata = numpy.arange( 0, dtype=float )
        for k in nd :
            ydata = numpy.append( ydata, yd )
        problem = ClassicProblem( xdata=xdata, model=mdl, ydata=ydata )
        errdis = GaussErrorDistribution( scale=1.0 )

        allpars = numpy.ones( np, dtype=float )
        Llow = errdis.logLikelihood( problem, allpars )

        allpars = numpy.random.rand( np ) * 2 - 1
        fitIndex = [k for k in range( np )]
        wl = WalkerList( problem, 2, allpars, fitIndex )




    def stdenginetest3( self, myengine, nsamp=100, order=1, plot=0 ) :
        m = Sphere( order )
        m.priors = [ UniformPrior( limits=[-1.0,1.0] ) ]
        xdata = numpy.array( [0.0] )
        data = numpy.array( [0.0] )

        sigma = 1.0
        problem = ClassicProblem( xdata=xdata, model=m, ydata=data )
        errdis = GaussErrorDistribution( scale=sigma )

        allpars = numpy.array( [0.0] * (m.npars) + [sigma] )
        nap = m.npars + 1
        fitIndex = [k for k in range( m.npars )]
        wl = WalkerList( problem, 2, allpars, fitIndex )

        ## determine lowLhood at edge of unit sphere
        allpars[0] = 1.0
        Llow = errdis.logLikelihood( problem, allpars )

        ## starting position
        allpars[0] = 0.9
        wl[0].allpars = allpars.copy()
        wl[0].logL = errdis.logLikelihood( problem, allpars )
        print( nsamp, order, fmt(allpars), Llow, wl[0].logL )

        if plot == 1 :
            plt.figure( order, figsize=[6,6] )

        engine = myengine( wl, errdis )
        engine.nstep = 15
        engine.size = 1.0
        if plot == 2 :
            engine.plotter = Plotter()
        engine.verbose = 5 if nsamp < 10 else 0

        engine.calculateUnitRange()
        engine.unitRange = numpy.array( [1.0] * m.npars )
        engine.unitMin = numpy.array( [0.0] * m.npars )
        engine.unitMean = numpy.array( [0.5] * m.npars )
        engine.maxtrials = 20

        count = numpy.zeros( order, dtype=int )

        rh = math.pow( 0.5, 1/order )
        kp0 = 0
        kp1 = 1
        rcnt = 0
        for k in range( nsamp ) :
            w = wl[0]
            w.allpars = allpars.copy()
            engine.execute( 0, Llow )
            pars = wl[0].allpars[:-1]
            if plot == 1 :
                plt.plot( pars[kp0], pars[kp1], 'r.' )

            count = numpy.where( pars > 0, count+1, count )
            rad = math.sqrt( numpy.sum( numpy.square( pars ) ) )
            if rad > rh :
                rcnt += 1
#            print( rad )
            self.assertTrue( rad <= 1.0000001 )

        engine.printReport()
        print( engine.errdis.ncalls, engine.errdis.nparts )
        print( "Larger  ", count, rcnt, rh )
        print( "Smaller ", nsamp - count, nsamp - rcnt )
        if plot == 1 :
            phi = numpy.linspace( 0, 2 * math.pi, 361, dtype=float )
            xcp = numpy.cos( phi )
            ysp = numpy.sin( phi )

            plt.plot( xcp, ysp, 'k-' )
            plt.plot( rh*xcp, rh*ysp, 'k-' )
            plt.xlabel( "Param %d" % kp0 )
            plt.ylabel( "Param %d" % kp1 )

            plt.xlim( -1.0, 1.0 )
            plt.ylim( -1.0, 1.0 )
            plt.show()


    def stdenginetest( self, myengine, nsamp=4, seed=4213, plot=False ) :
        m, xdata, data = self.initEngine()
        sigma = 2.0
        problem = ClassicProblem( xdata=xdata, model=m, ydata=data )
        errdis = GaussErrorDistribution( )
        errdis.keepFixed( {0: sigma} )
#        Tools.printclass( m )

#        print( m.basePartial( xdata, [0.0,0.0] ) )

        allpars = [0.0,0.0,sigma]
        wl = WalkerList( problem, nsamp, allpars, [0,1]  )
        map = numpy.ndarray( (21,21), dtype=float )
        mmx = -math.inf
        for k0 in range( 21 ) :
            for k1 in range( 21 ) :
                pl = [k0/10-1, k1/10-1, sigma]
                map[k1,k0] = errdis.logLikelihood( problem, pl )
                if map[k1,k0] > mmx :
                    mmx = map[k1,k0]
                    mk1 = k1/10 - 1
                    mk0 = k0/10 - 1

#        print( map )
#        print( mk0, mk1, mmx )

        ay = numpy.linspace( -1, 1, 21 )
        ax = numpy.linspace( -1, 1, 21 )
        v = [-180, -170, -165, -163]

        lowL = -170

        engine = StartEngine( wl, errdis )
        for ks in range( nsamp ) :
            samp = wl[ks]
            while True :
                engine.execute( samp.id, -math.inf )
#                print( fmt( ks ), fmt( wl[ks].logL ), fmt( samp.id ), fmt( samp.logL ) )
                if wl[ks].logL > lowL : break

        engine = myengine( wl, errdis, seed=seed )
        engine.plotter = Plotter()
        engine.nstep = 4
        engine.debug = True
#        engine.verbose = 5

        pevo = wl.getParameterEvolution()
        for k in range( 5 ) :
            engine.plotter.iter = 1
            plt.figure( str( myengine ), figsize=(4,4) )
            plt.contour( ax, ay, map, v )
            plt.plot( [mk0], [mk1], 'k*' )


            klo = engine.rng.randint( 0, nsamp )

            p0 = [w.allpars[0] for w in wl]
            p1 = [w.allpars[1] for w in wl]
            plt.plot( p0, p1, 'm.' )

            p0 = wl[klo].allpars[:2]
            plt.plot( p0[0], p0[1], 'k.' )


            engine.calculateUnitRange()

            engine.execute( wl[klo].id, lowL )
            p1 = wl[klo].allpars[:2]

            print( klo, fmt( p1 ), fmt( wl[klo].logL ) )
            plt.show()


    def stdenginetest2( self, myengine, nsamp=4, lowL=-170, plot=False ) :
        m, xdata, data = self.initEngine()
        sigma = 2.0
        problem = ClassicProblem( xdata=xdata, model=m, ydata=data )
        errdis = GaussErrorDistribution( )
        errdis.keepFixed( {0: sigma} )

        allpars = [0.0,0.0,sigma]
        wl = WalkerList( problem, nsamp, allpars, [0,1]  )

        engine = StartEngine( wl, errdis )
        for ks in range( nsamp ) :
            samp = wl[ks]
            while True :
                engine.execute( samp.id, -math.inf )
#                print( fmt( ks ), fmt( wl[ks].logL ), fmt( samp.id ), fmt( samp.logL ) )
                if wl[ks].logL > lowL : break

        pevo = wl.getParameterEvolution()
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
                map[k1,k0] = errdis.logLikelihood( problem, pl )
                if map[k1,k0] > mmx :
                    mmx = map[k1,k0]
                    mk1 = p1
                    mk0 = p0

#        print( map )
        print( mk0, mk1, mmx )



        engine = myengine( wl, errdis )
        nstep = 10
        plt.figure( engine.__str__(), figsize=[6,6] )
        v = [-200, -170, -165, -163]
        plt.contour( ax, ay, map, v )
#        plt.plot( [mk0], [mk1], 'k*' )
        plt.xlabel( "Param_0" )
        plt.ylabel( "Param_1" )

        klo = engine.rng.randint( 0, nsamp )

        p0 = wl[klo].allpars[:2]
        engine.calculateUnitRange()

        for k in range( 100 ) :
            wl[klo].allpars[:2] = p0
            engine.execute( wl[klo].id, lowL )
            p1 = wl[klo].allpars[:2]
            plt.plot( p1[0], p1[1], 'r.' )

        plt.plot( p0[0], p0[1], 'k*' )
        plt.show()

    def suite( cls ):
        return unittest.TestCase.suite( TestEngine2.__class__ )


class Plotter( object ) :

    def __init__( self, iter=0, kp=(0,1), figsize=(5,5) ) :
        self.iter = iter
        self.figsize = figsize
        self.k0 = kp[0]
        self.k1 = kp[1]
        self.col = ['k', 'r', 'g', 'b', 'm', 'y']
        self.sym = ['.', ',', 'o', '+', 'x', '*']

    def start( self, param=None ):
        """ start the plot. """
        plt.figure( 1, figsize=(5,5) )
        if param is not None :
            self.point( param, col=1, sym=2 )



    def point( self, param, col=0, sym=0 ) :
        """
        put a point at position param using color col.
        """
        k0 = self.k0
        k1 = self.k1
        cl = self.col[col] + self.sym[sym]
        plt.plot( [param[k0]], [param[k1]], cl )


    def move( self, param, ptry, col=0, sym=None ):
        """
        Move parameters at position param to ptry using color col.
        """
        k0 = self.k0
        k1 = self.k1
        cl = self.col[col] + '-'
        plt.plot( [param[k0], ptry[k0]], [param[k1], ptry[k1]], cl )

        if sym is not None :
            plt.text( ptry[k0], ptry[k1], "%d" % self.iter )
            self.point( ptry, col=col, sym=sym )
            self.iter += 1

    def stop( self, param=None, name=None ):
        """ Stop (show) the plot. """
        if param is not None :
            self.point( param, col=2, sym=2 )
        if name is not None :
            plt.title( name )

#        plt.xlabel( "Param %d" % self.k0 )
#        plt.ylabel( "Param %d" % self.k1 )
        plt.show()



if __name__ == '__main__':
    unittest.main( )


