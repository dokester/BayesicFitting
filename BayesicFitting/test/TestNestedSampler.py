# run with : python3 -m unittest TestNestedSampler
# or :       python3 -m unittest TestNestedSampler.TestNestedSampler.test1

import unittest
import os
import time
import numpy as numpy
from astropy import units
import math
from numpy.testing import assert_array_almost_equal as assertAAE
from FitPlot import plotFit

from BayesicFitting import *
from BayesicFitting import formatter as fmt
from BayesicFitting import fma
#from BayesicFitting import NestedSampler1 as NestedSampler

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

class TestNestedSampler( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author       Do Kester

    """

    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )
        self.dofull = ( "DOFULL" in os.environ and os.environ["DOFULL"] == "1" )

    def makeData( self, n=3 ) :

        N = 201
        a0 = 8.0
        x0 = 0.7
        s0 = 0.4
        b0 = 1.0
        b1 = 0.2
        p0 = 1.3
        cs = 0.3
        cc = 0.2
        r0 = 0.1

        x = numpy.arange( N, dtype=float ) / 25 - 2
        w = numpy.full( N, 2.0, dtype=float )

        g = ( x - x0 ) / s0
        g *= -0.5 * g
        g = a0 * numpy.exp( g )

        b = b1 * x + b0

        s = 2 * math.pi * p0 * x
        s = cs * numpy.sin( s ) + cc * numpy.cos( s )

        numpy.random.seed( 13456 )

        r = r0 * numpy.random.randn( N )
        if n == 1 :
            y0 = g
            pp = numpy.asarray( [a0,x0,s0], dtype=float )
        elif n == 2 :
            y0 = g + b
            pp = numpy.asarray( [a0,x0,s0,b0,b1], dtype=float )
        else :
            y0 = g + b + s
            pp = numpy.asarray( [a0,x0,s0,b0,b1,p0,cc,cs], dtype=float )

        y = y0 + r

        return pp, y0, x, y, w


    def test1( self ):
        print( "=========== Nested Sampler test 1 ======================" )

        plot = self.doplot

        pp, y0, x, y, w = self.makeData( n=1 )

        gm = GaussModel( )

        print( gm.shortName( ) )

        lolim = numpy.asarray( [-10,-10,  0], dtype=float )
        hilim = numpy.asarray( [ 10, 10, 10], dtype=float )

        gm.setLimits( lolim, hilim )

        ns = NestedSampler( x, gm, y, w, threads=True, engines=["galilean", "gibbs"] )
#        ns.verbose = 4

        self.dofit( ns, pp )

        sl = ns.samples

        printclass( sl[0] )

        plotSampleList( sl, x, y, residuals=True, show=plot )

#        start = time.time()
#        SampleMovie( sl, problem=ns.problem, kpar=[1,0] )
#        endt = time.time()

#        print( "Elapsed ", endt - start )

    def test2a( self ):
        print( "=========== Nested Sampler test 2a ======================" )

        plot = self.doplot

        pp, y0, x, y, w = self.makeData( 2 )

        x = numpy.append( x, x )
        y = numpy.append( y, y )

        gm = GaussModel( )
        gm.addModel( PolynomialModel(1) )

        print( gm.shortName( ) )
        print( gm._next.shortName( ) )

        lolim = numpy.asarray( [-10,-10,  0,-10,-10], dtype=float )
        hilim = numpy.asarray( [ 10, 10, 10, 10, 10], dtype=float )

        gm.setLimits( lolim, hilim )

        lmf = LevenbergMarquardtFitter( x, gm )
        pars = lmf.fit( y )
        print( "LMFpars ", fmt( pars, max=None ) )
        print( "LMFstdv ", fmt( lmf.stdevs, max=None ) )

        ns = NestedSampler( x, gm, y )
        ns.verbose = 2

        evi = ns.sample()
        print( "NS pars ", fmt( ns.parameters ) )
        print( "NS stdv ", fmt( ns.stdevs ) )
        print( "NS scal ", fmt( ns.scale ) )

    def test2b( self ):
        print( "=========== Nested Sampler test 2b ======================" )

        plot = self.doplot

        pp, y0, x, y, w = self.makeData( 2 )

        x = numpy.append( x, x )
        y = numpy.append( y, y )

        gm = GaussModel( )
        gm.addModel( PolynomialModel(1) )

        print( gm.shortName( ) )
        print( gm._next.shortName( ) )

        lolim = numpy.asarray( [-10,-10,  0,-10,-10], dtype=float )
        hilim = numpy.asarray( [ 10, 10, 10, 10, 10], dtype=float )

        gm.setLimits( lolim, hilim )
        ns = NestedSampler( x, gm, y )
        ns.verbose = 2
        ns.distribution.setLimits( [0.01, 100] )


        evi = ns.sample()
        print( "NS pars ", fmt( ns.parameters ) )
        print( "NS stdv ", fmt( ns.stdevs ) )
        print( "NS scal ", fmt( ns.scale ) )

    def test2c( self ):
        print( "=========== Nested Sampler test 2c ======================" )

        plot = self.doplot

        pp, y0, x, y, w = self.makeData( 2 )

        x = numpy.append( x, x )
        y = numpy.append( y, y )

        gm = GaussModel( )
        gm.addModel( PolynomialModel(1) )

        print( gm.shortName( ) )
        print( gm._next.shortName( ) )

        lolim = numpy.asarray( [-10,-10,  0,-10,-10], dtype=float )
        hilim = numpy.asarray( [ 10, 10, 10, 10, 10], dtype=float )

        gm.setLimits( lolim, hilim )
        ns = NestedSampler( x, gm, y, discard=10 )
        ns.distribution.setLimits( [0.01, 100] )
        ns.verbose = 2

        evi = ns.sample()
        print( "NS pars ", fmt( ns.parameters ) )
        print( "NS stdv ", fmt( ns.stdevs ) )
        print( "NS scal ", fmt( ns.scale ) )

        plotSampleList( ns.samples, x, y, residuals=True, show=plot )

#        print( "truth  ", pp )
#        self.dofit( ns, pp, plot=plot )

    def test4( self ):
        print( "=========== Nested Sampler test 4 ======================" )

        pp = 0.0
        numpy.random.seed( 13456 )

        for N in [10, 40, 160, 640, 2560] :
            print( "======= ", N, " points ======" )
            x = numpy.linspace( -1.0, 1.0, N, dtype=float )
            y = numpy.random.randn( N )

            pm = PolynomialModel( 1 )

            lolim = numpy.asarray( [-10], dtype=float )
            hilim = numpy.asarray( [ 10], dtype=float )

            pm.setLimits( lolim, hilim )

            lmf = LevenbergMarquardtFitter( x, pm )
            pars = lmf.fit( y )
            lmfevid = lmf.getEvidence( limits=[lolim,hilim], noiseLimits=[0.01,100] )
            print( "LMFpars ", fmt( pars, max=None ) )
            print( "LMFstdv ", fmt( lmf.stdevs, max=None ) )
            print( "LMFscal ", fmt( lmf.scale ) )
            print( "LMFevid ", fmt( lmfevid ) )

            ns = NestedSampler( x, pm, y, verbose=0 )
            ns.distribution.setLimits( [0.01, 100] )

            evi = ns.sample()
            print( "NS pars ", fmt( ns.parameters ) )
            print( "NS stdv ", fmt( ns.stdevs ) )
            print( "NS scal ", fmt( ns.scale ) )
            print( "NS evid ", fmt( evi ), " +- ", fmt( ns.precision ) )



    def test3( self ):
        print( "=========== Nested Sampler test 3 ======================" )

        plot = self.doplot

        pp, y0, x, y, w = self.makeData( 3 )

        gm = GaussModel( )
        gm.addModel( PolynomialModel(1) )
        gm.addModel( SineModel() )

        print( gm.shortName( ) )
        print( gm._next.shortName( ) )
        print( gm._next._next.shortName( ) )
        print( gm._next._next._next )

        lolim = numpy.asarray( [-10,-10,  0,-10,-10, 0.5,-10,-10], dtype=float )
        hilim = numpy.asarray( [ 10, 10, 10, 10, 10, 2.5, 10, 10], dtype=float )

        gm.setLimits( lolim, hilim )

        ns = NestedSampler( x, gm, y, w )
        ns.distribution.setLimits( [0.01, 10] )

        self.dofit( ns, pp )

        plotSampleList( ns.samples, x, y, show=plot )

    def dofit( self, ns, pp, plot=False ) :
        logE = ns.sample( plot=plot )

        par = ns.parameters
        std = ns.standardDeviations
        mlp = ns.samples.maxLikelihoodParameters
        scale = ns.scale
        scdev = ns.stdevScale
        print( "truth  ", fma( pp ) )
        print( "par    ", fma( par ) )
        print( "st dev ", fma( std ) )
        print( "ML par ", fma( mlp ) )
        print( "scale  ", fmt( scale ) )
#        ns.report( )


        self.assertTrue( all( numpy.abs( par - mlp ) < 2 * std ) )
        self.assertTrue( all( numpy.abs( par - pp ) < 2 * std ) )
#        assertAAE( par, pp, 2 )

    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( NestedSampler1Test.__class__ )


