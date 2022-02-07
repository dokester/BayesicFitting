#run with: python3 -m unittest TestModifiable

import unittest
import os
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt

#from StdTests import stdModeltest

from BayesicFitting import *

from BayesicFitting import formatter as fmt

__author__ = "Do Kester"
__year__ = 2018
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
#  *    2016 Do Kester

class Test( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )
        self.dofull = ( "DOFULL" in os.environ and os.environ["DOFULL"] == "1" )

    def makeData( self, npt=51, noise=0.1 ) :
        t = numpy.linspace( 0, 100, npt, dtype=float )
#        ym = numpy.sin( 2 * math.pi * numpy.exp( t / 150 ) )
        ym = 2 * numpy.sin( 2 * math.pi * numpy.exp( t / 80 ) +1 ) * numpy.exp( -0.02 * t )
        y = numpy.random.seed( 12345 )
        y = ym + numpy.random.randn( npt ) * noise

        return t, y


    def test1( self ) :
        print( "1  Test Splines" )

        t, y = self.makeData()
        knots =[0, 20, 40, 60, 75, 90, 100]

        mdl = BasicSplinesModel( knots=knots )
        mdl.setLimits( lowLimits=[-2.0], highLimits=[+2.0] )

        engs = ["galilean", "chord"]

        ns = NestedSampler( t, mdl, y, seed=1234, engines=engs )
        ns.distribution.setLimits( [0.01,100] )
        ns.verbose = 2
        ## Comment next if-statement out for a full run of NestedSampler
        if not self.dofull :
            ns.ensemble = 10

        evid = ns.sample( plot=self.doplot )

    def test2( self ) :
        print( "2  Test Modifiable Splines" )

        t, y = self.makeData()
        knots =[0, 10, 25, 40, 50, 60, 75, 100]

        mdl = SplinesDynamicModel( knots=knots, dynamic=False )
        mdl.setLimits( lowLimits=[-2.0], highLimits=[+2.0] )

        engs = ["galilean", "struct"]

        ns = NestedSampler( t, mdl, y, seed=31234, engines=engs )
        ns.distribution.setLimits( [0.01,100] )
        ns.verbose = 2
#        ns.engines[1].slow = 5
        ## Comment next if-statement out for a full run of NestedSampler
        if not self.dofull :
            ns.ensemble = 10

        evid = ns.sample( plot=self.doplot )

        if not self.doplot : return

        cc = ['k,', 'b,', 'r,', 'g,', 'c,', 'm,']
        sl = ns.samples
        ka = numpy.zeros( ( len( knots ), len( sl ) ), dtype=float )
        for k,s in enumerate( sl ) :
            ka[:,k] = s.model.knots
        for j in range( len( knots ) ) :
            plt.plot( ka[j,:], cc[j % 6] )
        plt.show()

    def test3( self ) :
        print( "3  Test Dynamic Splines" )

        t, y = self.makeData()
        knots =[0, 100]

        mdl = SplinesDynamicModel( knots=knots )
        mdl.setLimits( lowLimits=[-5.0], highLimits=[+5.0] )

        engs = ["galilean", "birth", "death", "struct"]

        ns = NestedSampler( t, mdl, y, seed=1234, engines=engs )
        ns.distribution.setLimits( [0.01,1] )
        ns.verbose = 2
        ## Comment next if-statement out for a full run of NestedSampler
        if not self.dofull :
            ns.ensemble = 10

        evid = ns.sample( plot=self.doplot )

        if not self.doplot : return

        cc = ['k,', 'b,', 'r,', 'g,', 'c,', 'm,']
        sl = ns.samples
#        ka = numpy.zeros( ( len( knots ), len( sl ) ), dtype=float )
        for k,s in enumerate( sl ) :
            kn = s.model.knots
            nn = [k] * len( kn )
            plt.plot( nn, kn, cc[2] )
        wgts = sl.getWeightEvolution()
        mw = max( wgts )
        plt.plot( 100 * wgts / mw, 'k-' )
        plt.show()

    def test4( self ) :
        print( "4  Test Modifiable Splines compound" )

        t, y = self.makeData()
        NP = 41
        t = numpy.linspace( 0, 100, NP, dtype=float )
        dt = GaussModel().result( t, [10.0, 34, 10] )

        ym = numpy.sin( 0.1 * ( t + dt ) )
        y = ym + 0.1 * numpy.random.randn( NP )


        knots =[0, 25, 50, 75, 100]
        xm = SplinesDynamicModel( knots=knots, dynamic=False )
        xm += PowerModel( 1, fixed={0:1.0} )
        xm.setPrior( 0, LaplacePrior( center=0, scale=4 ) )

        sm = SineModel()
        sm.setLimits( lowLimits=[-2.0], highLimits=[+2.0] )

        mdl = xm | sm

        ns = NestedSampler( t, mdl, y, seed=31234 )
        ns.distribution.setLimits( [0.01,100] )
        ns.verbose = 2
#        ns.engines[2].verbose = 5
        ns.engines[2].slow = 5
        ## Comment next if-statement out for a full run of NestedSampler
        if not self.dofull :
            ns.ensemble = 10

        evid = ns.sample( plot=self.doplot )

        return

        if not self.doplot : return

        cc = ['k,', 'b,', 'r,', 'g,', 'c,', 'm,']
        sl = ns.samples
        yfit = numpy.zeros( NP, dtype=float )
        for s in sl :
            knts = s.model.knots
            yft = BasicSplinesModel( knts ).result( t, s.parameters[:7] )
            yfit += yft * s.weight
        plt.plot( t, yfit, 'b-' )
        plt.plot( t, ns.yfit, 'g-' )
        plt.plot( t, y, 'k.' )
        plt.show()


    def test5( self ) :
        print( "5  Test Dynamic Modifiable Splines: evidence with fixed scale " )

        t, y = self.makeData()

#        npt = 201
#        t = numpy.linspace( 0, 100, npt, dtype=float )
#        ym = 2 * numpy.sin( 2 * math.pi * numpy.exp( t / 80 ) +1 ) * numpy.exp( -0.02 * t )
#        y = numpy.random.seed( 12345 )
#        y = ym + numpy.random.randn( npt ) * 0.05

        knots =[0, 100]
        mxk = 15
        mdl = SplinesDynamicModel( knots=knots, dynamic=True, maxKnots=mxk, minDistance=0.04 )
        mdl.setLimits( lowLimits=[-10.0], highLimits=[+10.0] )
        
        ep = EvidenceProblem( model=mdl, xdata=t, ydata=y )
        distr = ModelDistribution( scale=0.1 )
        
        ns = NestedSampler( problem=ep, distribution=distr )
        
        ns.verbose = 2
        ns.minimumIterations = 2000
        ## Comment next if-statement out for a full run of NestedSampler
        if not self.dofull :
            ns.ensemble = 10
            ns.minimumIterations = 500
        
        evid = ns.sample( plot=self.doplot )

        if not self.doplot : return

        ## Plot the evolutie of knots and sample weights
        cc = ['k,', 'b,', 'r,', 'g,', 'c,', 'm,']
        sl = ns.samples
        ka = numpy.zeros( ( mxk, len( sl ) ), dtype=float )
        plt.figure( 1, figsize=[14,8] )
        for k,s in enumerate( sl ) :
            n = len( s.model.knots )
            ka[:n,k] = s.model.knots
        for j in range( mxk ) :
            plt.plot( ka[j,:], cc[j%6] )
        wgts = sl.getWeightEvolution()
        mw = max( wgts )
        plt.plot( 100 * wgts / mw, 'k-' )
        plt.xlabel( "Iteration number" )
        plt.ylabel( "Knot position cq. sample weight")
        plt.show()

        plt.figure( 2, figsize=[14,8] )
        plt.plot( t, y, 'k.' )
        cc = ['k-', 'b-', 'r-', 'g-', 'c-', 'm-', 'y-']
        cp = ['k*', 'b*', 'r*', 'g*', 'c*', 'm*', 'y*']
        for k in range( 0, 2100, 200 ) :
            kc = k % 7
            s = sl[k]
            mdl = s.model
            kn = mdl.knots
            plt.plot( kn, [-1+k/1000]*len( kn ), cp[kc] )
            plt.plot( t, mdl( t ), cc[kc] )
            print( fmt( k ) )
            print( fmt( kn, max=None ) )
            print( fmt( mdl.parameters, max= None ), fmt( s.logL ) )

            m = BasicSplinesModel( knots=kn )
            ftr = Fitter( t, m, fixedScale=0.05 )
            par = ftr.fit( y )
            lz0 = ftr.getLogZ( limits=[-10,+10] )
            print( fmt( par, max=None ), fmt( lz0 ) )

            m = BasicSplinesModel( knots=kn )
            ftr = Fitter( t, m )
            par = ftr.fit( y )
            lz0 = ftr.getLogZ( limits=[-10,+10] )
            print( fmt( par, max=None ), fmt( lz0 ) )

            m = BasicSplinesModel( knots=kn )
            ftr = Fitter( t, m )
            par = ftr.fit( y )
            lz0 = ftr.getLogZ( limits=[-10,+10], noiseLimits=[0.01,1] )
            print( fmt( par, max=None ), fmt( lz0 ) )

        plt.show()

    def test6( self ) :
        npt = 401

        t, y = self.makeData()

        t = numpy.linspace( 0, 100, npt, dtype=float )
        ym = 2 * numpy.sin( 2 * math.pi * numpy.exp( t / 60 ) +1 ) * numpy.exp( -0.02 * t )
        y = numpy.random.seed( 12345 )
        y = ym + numpy.random.randn( npt ) * 0.05

        kn = [0,25,50,60,70,80,90,100]  
        kn = [0.000,17.254,33.456,42.755,61.243,62.538,74.369,89.854,93.388,100.000]

        m = BasicSplinesModel( knots=kn )
        ftr = Fitter( t, m, fixedScale=0.05 )
        par = ftr.fit( y )
        lz0 = ftr.getLogZ( limits=[-10,+10] )
        print( fmt( par, max=None ), fmt( lz0 ) )

        m = BasicSplinesModel( knots=kn )
        ftr = Fitter( t, m )
        par = ftr.fit( y )
        lz0 = ftr.getLogZ( limits=[-10,+10] )
        print( fmt( par, max=None ), fmt( lz0 ) )

        m = BasicSplinesModel( knots=kn )
        ftr = Fitter( t, m )
        par = ftr.fit( y )
        lz0 = ftr.getLogZ( limits=[-10,+10], noiseLimits=[0.01,1] )
        print( fmt( par, max=None ), fmt( lz0 ) )

    def test7( self ) :
        print( "7  Test Dynamic Modifiable Splines: evidence unknown scale" )

        t, y = self.makeData()

        knots =[0, 100]
        mxk = 15
        mdl = SplinesDynamicModel( knots=knots, dynamic=True, maxKnots=mxk, minDistance=0.01 )
        mdl.setLimits( lowLimits=[-10.0], highLimits=[+10.0] )
        
        ep = EvidenceProblem( model=mdl, xdata=t, ydata=y )
        distr = ModelDistribution( limits=[0.01,1] )
        #ns = NestedSampler( t, mdl, y, seed=1235, engines=eng, distribution=distr )
        #print( ns.problem )
        #print( ns.model )
        #print( fmt( ns.xdata ) )
        #print( fmt( ns.ydata ) )
        
        ns = NestedSampler( problem=ep, distribution=distr )
        
        print( ns.problem )
        print( ns.model )
        print( fmt( ns.xdata ) )
        print( fmt( ns.ydata ) )
        ns.verbose = 2

        ## Comment next if-statement out for a full run of NestedSampler
        if not self.dofull :
            ns.ensemble = 10
            ns.minimumIterations = 500 
       
        evid = ns.sample( plot=self.doplot )

        if not self.doplot : return

        ## Plot the evolutie of knots and sample weights
        cc = ['k,', 'b,', 'r,', 'g,', 'c,', 'm,']
        sl = ns.samples
        ka = numpy.zeros( ( mxk, len( sl ) ), dtype=float )
        plt.figure( 1, figsize=[14,8] )
        for k,s in enumerate( sl ) :
            n = len( s.model.knots )
            ka[:n,k] = s.model.knots
        for j in range( mxk ) :
            plt.plot( ka[j,:], cc[j%6] )
        wgts = sl.getWeightEvolution()
        mw = max( wgts )
        plt.plot( 100 * wgts / mw, 'k-' )
        plt.xlabel( "Iteration number" )
        plt.ylabel( "Knot position cq. sample weight")
        plt.show()

        plt.figure( 2, figsize=[14,8] )
        plt.plot( t, y, 'k.' )
        cc = ['k-', 'b-', 'r-', 'g-', 'c-', 'm-', 'y-']
        cp = ['k*', 'b*', 'r*', 'g*', 'c*', 'm*', 'y*']
        for k in range( 0, 2100, 200 ) :
            kc = k % 7
            s = sl[k]
            mdl = s.model
            kn = mdl.knots
            plt.plot( kn, [-1+k/1000]*len( kn ), cp[kc] )
            plt.plot( t, mdl( t ), cc[kc] )
            print( fmt( k ) )
            print( fmt( kn, max=None ) )
            print( fmt( mdl.parameters, max= None ), fmt( s.logL ) )

        plt.show()

    def test8( self ) :
        print( "8  Test Dynamic Modifiable Splines: evidence scale = 1.0" )

        t,y = self.makeData()

        knots =[0, 100]
        mxk = 15
        mdl = SplinesDynamicModel( knots=knots, dynamic=True, maxKnots=mxk, minDistance=0.01 )
        mdl.setLimits( lowLimits=[-10.0], highLimits=[+10.0] )
        
        ep = EvidenceProblem( model=mdl, xdata=t, ydata=y )
        distr = ModelDistribution( )
        
        ns = NestedSampler( problem=ep, distribution=distr )
        
        ns.verbose = 2

        ## Comment next if-statement out for a full run of NestedSampler
        if not self.dofull :
            ns.ensemble = 10
            ns.minimumIterations = 500

        
        evid = ns.sample( plot=self.doplot )

        if not self.doplot : return

        ## Plot the evolutie of knots and sample weights
        cc = ['k,', 'b,', 'r,', 'g,', 'c,', 'm,']
        sl = ns.samples
        ka = numpy.zeros( ( mxk, len( sl ) ), dtype=float )
        plt.figure( 1, figsize=[14,8] )
        for k,s in enumerate( sl ) :
            n = len( s.model.knots )
            ka[:n,k] = s.model.knots
        for j in range( mxk ) :
            plt.plot( ka[j,:], cc[j%6] )
        wgts = sl.getWeightEvolution()
        mw = max( wgts )
        plt.plot( 100 * wgts / mw, 'k-' )
        plt.xlabel( "Iteration number" )
        plt.ylabel( "Knot position cq. sample weight")
        plt.show()

    def suite( cls ):
        return unittest.TestCase.suite( TestModifiable.__class__ )


if __name__ == '__main__':
    unittest.main()

