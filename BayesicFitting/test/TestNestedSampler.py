# run with : python3 -m unittest TestNestedSampler
# or :       python3 -m unittest TestNestedSampler.Test.test1

import unittest
import numpy as numpy
from astropy import units
import math
from numpy.testing import assert_array_almost_equal as assertAAE
from FitPlot import plotFit

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

class TestNestedSampler( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author       Do Kester

    """

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


    def plot1( self ):
        self.test1( plot=True )

    def plot2( self ):
        self.test2( plot=True )

    def plot3( self ):
        self.test3( plot=True )


    def test1( self, plot=False ):
        print( "=========== Nested Sampler test 1 ======================" )

        pp, y0, x, y, w = self.makeData( n=1 )

        gm = GaussModel( )

        print( gm.shortName( ) )

        lolim = numpy.asarray( [-10,-10,  0], dtype=float )
        hilim = numpy.asarray( [ 10, 10, 10], dtype=float )

        gm.setLimits( lolim, hilim )

        ns = NestedSampler( x, gm, y, w )
        ns.verbose = 2

        self.dofit( ns, pp )

        if plot :
            plotFit( x, y, gm, ftr=ns.samples )

    def test2( self, plot=False ):
        print( "=========== Nested Sampler test 2 ======================" )

        pp, y0, x, y, w = self.makeData( 2 )

        gm = GaussModel( )
        gm.addModel( PolynomialModel(1) )

        print( gm.shortName( ) )
        print( gm._next.shortName( ) )

        lolim = numpy.asarray( [-10,-10,  0,-10,-10], dtype=float )
        hilim = numpy.asarray( [ 10, 10, 10, 10, 10], dtype=float )

        gm.setLimits( lolim, hilim )

        ns = NestedSampler( x, gm, y )
        ns.verbose = 2

        print( "truth  ", pp )
        self.dofit( ns, pp )

        if plot :
            plotFit( x, y, gm, ftr=ns.samples )

    def test3( self, plot=False ):
        print( "=========== Nested Sampler test 3 ======================" )

        pp, y0, x, y, w = self.makeData( 3 )

        gm = GaussModel( )
        gm.addModel( PolynomialModel(1) )
        gm.addModel( SineModel() )

        print( gm.shortName( ) )
        print( gm._next.shortName( ) )
        print( gm._next._next.shortName( ) )
        print( gm._next._next._next )

        lolim = numpy.asarray( [-10,-10,  0,-10,-10, 0,-10,-10], dtype=float )
        hilim = numpy.asarray( [ 10, 10, 10, 10, 10, 2, 10, 10], dtype=float )

        gm.setLimits( lolim, hilim )

        ns = NestedSampler( x, gm, y, w )
        ns.verbose = 2
        ns.distribution.setLimits( [0.01, 100] )

        Tools.printclass( ns )

        print( "truth  ", pp )
        self.dofit( ns, pp )

        if plot :
            plotFit( x, y, gm, ftr=ns.samples )

    def nytest( self ) :
        print( "=========== Nested Sampler test 2 ======================" )

        nslim = numpy.asarray( [ 0.01, 100], dtype=float )
        gm.getNoiseScale( ).setLimits(nslim )
        ns = NestedSampler( x, gm, y, w )
        ns.setRate( 0.99 )
        ns.setTrials( 10 )
        ns.setInitialisationEngine( RandomEngine() )
        ns.setEngine( CrossEngine() )
        ns.addEngine( FrogEngine() )
        ns.addEngine( ScaleEngine() )
        ns.addEngine( StepEngine() )
        ns.setVerbose( True )
        np = gm.getNumberOfParameters( )
        ns.setMaxSamples( 1000 )

        print( "truth  ", pp )
        self.dofit( ns, pp )


    def dofit( self, ns, pp ) :
        yfit = ns.sample( )

        par = ns.parameters
        std = ns.standardDeviations
        mlp = ns.samples.maxLikelihoodParameters
        scale = ns.scale
        scdev = ns.stdevScale
        print( "truth  ", fmt( pp ) )
        print( "par    ", fmt( par ) )
        print( "st dev ", fmt( std ) )
        print( "ML par ", fmt( mlp ) )
        print( "scale  ", fmt( scale ), " +- ", fmt( scdev ) )
#        ns.report( )


#        assertAAE( par, mlp, 2 )
#        assertAAE( par, pp, 2 )

    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( NestedSampler1Test.__class__ )


