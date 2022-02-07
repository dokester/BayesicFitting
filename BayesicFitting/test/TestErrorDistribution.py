## run as : python3 -m unittest TestErrorDistribution

from __future__ import print_function

import numpy as numpy
from numpy.testing import assert_array_almost_equal as assertAAE
import unittest
import os
from astropy import units
import math
import sys
import matplotlib.pyplot as plt
from StdTests import stdModeltest

from BayesicFitting import *
from BayesicFitting import formatter as fmt
#from MultiDimAverageModel import MultiDimAverageModel
#from BoxedErrorDistribution import BoxedErrorDistribution

__author__ = "Do Kester"
__year__ = 2021
__license__ = "GPL3"
__version__ = "2.7.3"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Perpetual Beta"

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
#  *  2017 - 2021  Do Kester

class TestErrorDistribution( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author       Do Kester

    """
    SQRT2 = math.sqrt( 2 )
    LGSQ2 = math.log( SQRT2 )
    LOG2 = math.log( 2 )
    EPSILON = 1e-6

    # Define x independent variable
    x = numpy.asarray( [ -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0], dtype=float )

    # Define y dependent variable
    data = numpy.asarray( [-11.1, -9.2, -5.1, -5.2, -1.1, 1.2, 1.1, 5.2, 5.1, 8.2, 11.2], dtype=float )

    # Define wgt weigth
    wgt = numpy.asarray( [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=float )

    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )
        numpy.set_printoptions(formatter={'float': '{: 0.3f}'.format})

    def test1( self ) :
        print( "====test1============================" )
        nn = 10000
        x = numpy.linspace( 0, 1, nn, dtype=float )
        ym = 0.0 * x
        nf = 0.01

        model = PolynomialModel( 0 )
        model.parameters = 0.0
        problem = ClassicProblem( model=model, xdata=x, ydata=ym )
        fitIndex=[0]

        numpy.random.seed( 2345 )
        noise = numpy.random.randn( nn )

        errdis = GaussErrorDistribution( )
        allpars = [0.0, 1.0]
        print( errdis )
        for k in range( 5 ) :
            noise = numpy.random.randn( nn )
            y = ym + nf * noise
            problem.ydata = y
            print( fmt( k ), fmt( nf ), fmt( errdis.getScale( problem, allpars ) ) )
            nf *= 10
        if self.doplot:
            self.ploterrdis( noise, errdis, problem, allpars )

        nf = 0.01
        errdis = LaplaceErrorDistribution( )
        print( errdis )
        for k in range( 5 ) :
            noise = numpy.random.laplace( size=nn )
            y = ym + nf * noise
            problem.ydata = y
            print( fmt( k ), fmt( nf ), fmt( errdis.getScale( problem, allpars ) ) )
            nf *= 10
        if self.doplot:
            self.ploterrdis( noise, errdis, problem, allpars )

        nf = 0.01
        errdis = UniformErrorDistribution( )
        print( errdis )
        for k in range( 5 ) :
            noise = 0.5 - numpy.random.rand( nn )
            y = ym + nf * noise
            problem.ydata = y
            print( fmt( k ), fmt( nf ), fmt( errdis.getScale( problem, allpars ) ) )
            nf *= 10
        if self.doplot:
            self.ploterrdis( noise, errdis, problem, allpars )

        nf = 0.01
        errdis = CauchyErrorDistribution ( )
        cp = CauchyPrior()
        print( errdis )
        for k in range( 5 ) :
            noise = numpy.random.rand( nn )
            noise = cp.unit2Domain( noise )
            y = ym + nf * noise
            problem.ydata = y
            print( fmt( k ), fmt( nf ), fmt( errdis.getScale( problem, allpars ) ) )
            nf *= 10
        if self.doplot :
            self.ploterrdis( noise, errdis, problem, allpars )


        nf = 0.01
        errdis = ExponentialErrorDistribution( )
        allpars = [0.0, 1.0, 1.0]
        print( errdis, "  power=1" )
        for k in range( 5 ) :
            noise = numpy.random.laplace( size=nn )
            y = ym + nf * noise
            problem.ydata = y
            print( fmt( k ), fmt( nf ), fmt( errdis.getScale( problem, allpars ) ) )
            nf *= 10

        nf = 0.01
        errdis = ExponentialErrorDistribution( )
        allpars = [0.0, 1.0, 2.0]
        print( errdis, "  power=2"  )
        for k in range( 5 ) :
            noise = numpy.random.randn( nn )
            y = ym + nf * noise
            problem.ydata = y
            print( fmt( k ), fmt( nf ), fmt( errdis.getScale( problem, allpars ) ) )
            nf *= 10

        nf = 0.01
        power = 10
        errdis = ExponentialErrorDistribution ( )
        allpars = [0.0, 1.0, 10.0]
        print( errdis, "  power=%d" % power  )
        for k in range( 5 ) :
            noise = 2 * numpy.random.rand( nn ) - 1.0
            y = ym + nf * noise
            problem.ydata = y
            print( fmt( k ), fmt( nf ), fmt( errdis.getScale( problem, allpars ) ) )
            nf *= 10

        allpars = [0.0, 1.0, power]
        if self.doplot :
            self.ploterrdis( noise, errdis, problem, allpars )

    def ploterrdis( self, noise, errdis, problem, allpars ) :
        num_bins = 20
#        plt.hist( noise, num_bins, normed=1, facecolor='g', alpha=0.5 )
        plt.hist( noise, num_bins, facecolor='g', alpha=0.5 )
        xx = numpy.linspace( -0.3, 0.3, 601, dtype=float )
        lik = numpy.zeros_like( xx )
        for k,p in enumerate( xx ) :
            allpars[0] = p
            lik[k] = errdis.logLikelihood( problem, allpars )
        maxlik = numpy.max( lik )
        plt.plot( xx, numpy.exp( lik - maxlik ), 'r-' )
        plt.title( errdis.__str__() )
        plt.show()


    def testGaussErrorDistribution( self ):

        print( "=======   Test Gauss Error Distribution  ==================" )

        poly = PolynomialModel( 1 )
        param = numpy.asarray( [1,10,1], dtype=float )
        ged = GaussErrorDistribution( )
        self.assertTrue( ged.acceptWeight() )

        problem = ClassicProblem( model=poly, xdata=self.x, ydata=self.data,
                weights=self.wgt )

        fitIndex = [0,1,-1]

        #   data = { -11, -9, -5, -5, -1, 1, 1, 5, 5, 8, 11 }
        #   f( x ) = { -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10 }
        #   f - d=     1   1  -1   1  -1 -1  1 -1  1  0  -1

        chisq = ged.getChisq( problem, param )
        print( "chisq = %8.3f"%( chisq ) )
        lLdata = ged.logLdata( problem, param )
        logL0 = numpy.sum( lLdata )

        logL = ged.logLikelihood( problem, param )
        altL = ged.logLikelihood_alt( problem, param )
        print( "logL  = %8.3f  %8.3f  %8.3f" % ( logL, logL0, altL ) )
        assertAAE( logL, altL )
        assertAAE( logL, logL0 )

        scale = 0.1
        param[2] = scale
        logL = ged.logLikelihood( problem, param )
        altL = ged.logLikelihood_alt( problem, param )
        print( "logL  = %8.3f  %8.3f" % ( logL, altL ) )
        assertAAE( logL, altL )

        scale = 1.0
        param[2] = scale
#        fitIndex = numpy.arange( 3 )
        fitIndex = numpy.asarray( [0,1,-1] )
        dL = ged.partialLogL( problem, param, fitIndex )
        nL = ged.numPartialLogL( problem, param, fitIndex )
        print( "partial = ", dL )
        print( "partalt = ", ged.partialLogL_alt( problem, param, fitIndex ) )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        print( "Using scale = 0.5 and weights." )
        scale = 0.5
        param[2] = scale
        problem.weights = self.wgt

        logL = ged.logLikelihood( problem, param )
        print( "logL = %8.3f  %8.3f" % ( logL, logL0 ) )

        lLdata = ged.logLdata( problem, param )
        logL0 = numpy.sum( lLdata )
        assertAAE( logL, logL0 )

        dL = ged.partialLogL( problem, param, fitIndex )
        print( "partalt = ", ged.partialLogL_alt( problem, param, fitIndex ) )
        nL = ged.numPartialLogL( problem, param, fitIndex )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        scale = 1.0
        for i in range( 11 ) :
            param = numpy.asarray( [i-5,5,1], dtype=float )
            print( param, "  :  ", end="" )
            for k in range( 9 ):
                print( " %8.3f" % ged.logLikelihood( problem, param ), end="" )
                param[1] += 1
            print( "" )

    def constrainBox( self, logL, problem, allpars, logLlow ):
        box = [-2,2]
        for p in allpars[:-1] :
            if ( p < box[0] ) or ( p > box[1] ) :
                return logLlow - 1

        return logL

    def XXXtestGaussErrorDistribution1( self ):

        print( "=======   Test Gauss Error Distribution 1 ==================" )

        ndim = 2
        poly = MultiDimAverageModel( ndim )
        param = numpy.asarray( [0,0,1], dtype=float )
        ged = GaussErrorDistribution( )
        ged.constrain = self.constrainBox
        self.assertTrue( ged.acceptWeight() )

        numpy.random.seed( 2345 )
        ydata = numpy.random.randn( ndim * 11 ).reshape( 11, ndim )

        print( fmt( ydata ) )
        problem = MultipleOutputProblem( model=poly, xdata=self.x, ydata=ydata )
#                weights=self.wgt )

        fitIndex = [0,1,-1]

        print( fmt( poly.result( self.x, param[:ndim] ) ) )


        #   data = { -11, -9, -5, -5, -1, 1, 1, 5, 5, 8, 11 }
        #   f( x ) = { -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10 }
        #   f - d=     1   1  -1   1  -1 -1  1 -1  1  0  -1

        chisq = ged.getChisq( problem, param )
        print( "chisq = %8.3f"%( chisq ) )

        pp = numpy.array( [0,0,1], dtype=float )
        print( " 0 0: ", fmt( ged.logLdata( problem, pp ), max=None ) )
        pp = numpy.array( [0,1,1], dtype=float )
        print( " 0 1: ", fmt( ged.logLdata( problem, pp ), max=None ) )
        pp = numpy.array( [1,1,1], dtype=float )
        print( " 1 1: ", fmt( ged.logLdata( problem, pp ), max=None ) )
        pp = numpy.array( [1,0,1], dtype=float )
        print( " 1 0: ", fmt( ged.logLdata( problem, pp ), max=None ) )



        lLdata = ged.logLdata( problem, param )
        logL0 = numpy.sum( lLdata )

        ged.lowLhood = -math.inf        ## is normally set by NS
        logL = ged.logLikelihood( problem, param )
        altL = ged.logLikelihood_alt( problem, param )
        print( "logL  = %8.3f  %8.3f  %8.3f" % ( logL, logL0, altL ) )
#        assertAAE( logL, altL )
        assertAAE( logL, logL0 )

        scale = 0.1
        param[2] = scale
        logL = ged.logLikelihood( problem, param )
        altL = ged.logLikelihood_alt( problem, param )
        print( "logL  = %8.3f  %8.3f" % ( logL, altL ) )
#        assertAAE( logL, altL )

        scale = 1.0
        param[2] = scale
#        fitIndex = numpy.arange( 3 )
        fitIndex = numpy.asarray( [0,1,-1] )
        dL = ged.partialLogL( problem, param, fitIndex )
        nL = ged.numPartialLogL( problem, param, fitIndex )
        print( "partial = ", dL )
#        print( "partalt = ", ged.partialLogL_alt( problem, param, fitIndex ) )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        print( "Using scale = 0.5 and weights." )
        scale = 0.5
        param[2] = scale

        wgts = []
        for k in range( ndim ) :
            wgts = numpy.append( wgts, self.wgt )

        problem.weights = wgts

        logL = ged.logLikelihood( problem, param )
        print( "logL = %8.3f  %8.3f" % ( logL, logL0 ) )

        lLdata = ged.logLdata( problem, param )
        logL0 = numpy.sum( lLdata )
        assertAAE( logL, logL0 )

        dL = ged.partialLogL( problem, param, fitIndex )
#        print( "partalt = ", ged.partialLogL_alt( problem, param, fitIndex ) )
        nL = ged.numPartialLogL( problem, param, fitIndex )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        print( ged.logLikelihood )
        scale = 1.0
        for i in range( 11 ) :
            param = numpy.asarray( [i-5,-4,1], dtype=float )
            print( param, "  :  ", end="" )
            for k in range( 9 ):
                print( " %8.3f" % ged.logLikelihood( problem, param ), end="" )
                param[1] += 1
            print( "" )

    def testGaussErrorDistribution2( self ):
        print( "\n=====   Test 2 Gauss Error Distribution====================" )
        gm = GaussModel( )
        gm.addModel( PolynomialModel(1) )
        param = numpy.asarray( [5, 1, -0.3, 1, 1, 1], dtype=float )
        data2 = self.data.copy( ) * 0.1
        data2[1:5] = [2.3, 5.4, 4.5, 2.0]
        print( data2 )

        problem = ClassicProblem( model=gm, xdata=self.x, ydata=self.data )
        fitIndex = [0,1,2,3,4,-1]

        ged = GaussErrorDistribution( )
        Tools.printclass( ged )
        np = gm.npchain
        chisq = ged.getChisq( problem, param )
        print( "chisq = %8.3f"%( chisq ) )
        logL = ged.logLikelihood( problem, param )
        altL = ged.logLikelihood_alt( problem, param )

        print( "logL  = %8.3f  %8.3f" % ( logL, altL ) )
        assertAAE( logL, altL )

        scale = 0.1
        param[np] = scale
        logL = ged.logLikelihood( problem, param )
        altL = ( -11 * ( 0.5 * math.log( 2 * math.pi ) +
                    math.log( scale ) ) - 0.5 * chisq / ( scale * scale ) )
        print( "logL  = %8.3f  %8.3f" % ( logL, altL ) )
        assertAAE( logL, altL )

        scale = 1.0
        param[np] = scale
        dL = ged.partialLogL( problem, param, fitIndex )
        nL = ged.numPartialLogL( problem, param, fitIndex )
        print( "partial = ", dL )
        print( "partalt = ", ged.partialLogL_alt( problem, param, fitIndex ) )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        fitIndex = numpy.asarray( [0,2,3,4] )
        dL = ged.partialLogL( problem, param, fitIndex )
        nL = ged.numPartialLogL( problem, param, fitIndex )
        print( "partial = ", dL )
        print( "partalt = ", ged.partialLogL_alt( problem, param, fitIndex ) )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        scale = 0.5
        param[np] = scale
        fitIndex = numpy.asarray( [0,1,2,3,4,-1] )
        problem.weights = self.wgt
        dL = ged.partialLogL( problem, param, fitIndex )
        nL = ged.numPartialLogL( problem,  param, fitIndex )
        print( "partial = ", dL )
        print( "partalt = ", ged.partialLogL_alt( problem, param, fitIndex ) )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        scale = 0.5
        param[np] = scale
        fitIndex = numpy.asarray( [0,1,2,4,-1] )

        ged.hyperpar[0] = NoiseScale()
        Tools.printclass( ged )
        ged.keepFixed( fixed={0:2.5} )
        Tools.printclass( ged )
        Tools.printclass( ged.hyperpar[0] )

        dL = ged.partialLogL( problem, param, fitIndex )
        nL = ged.numPartialLogL( problem, param, fitIndex )
        print( "partial = ", dL )
        print( "partalt = ", ged.partialLogL_alt( problem, param, fitIndex ) )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

    def testExponentialErrorDistribution1( self ):

        print( "=======   Test Exponential Error Distribution 1 ==================" )

        poly = PolynomialModel( 1 )
        param = numpy.asarray( [1,10], dtype=float )
        ged = LaplaceErrorDistribution( )
        ggd = ExponentialErrorDistribution( limits=[[0.1,0.5],[10,3]] )
        self.assertTrue( ggd.acceptWeight() )

        self.assertTrue( ggd.hyperpar[0].prior.lowLimit == 0.1 )
        self.assertTrue( ggd.hyperpar[0].prior.highLimit == 10 )
        self.assertTrue( ggd.hyperpar[1].prior.lowLimit == 0.5 )
        self.assertTrue( ggd.hyperpar[1].prior.highLimit == 3 )

        #   data = { -11, -9, -5, -5, -1, 1, 1, 5, 5, 8, 11 }
        #   f( x ) = { -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10 }
        #   f - d=     1   1  -1   1  -1 -1  1 -1  1  0  -1

        problem = ClassicProblem( model=poly, xdata=self.x, ydata=self.data )
        fitIndex = [0,1,2,3,4,-1]


        power = 1.0
        ggscl = 1.0
        lpscl = 1.0
        hypar = [ggscl, power]
        ggsigma = ggd.toSigma( hypar )
        lpsigma = ged.toSigma( lpscl )
        sigma = ggsigma / lpsigma
        print( ggsigma, lpsigma, sigma )

        ff = 1.0 / sigma
        ggpar = numpy.append( param, hypar )
        lppar = numpy.append( param, [lpscl] )
        res = problem.residuals( param )
        chisq = ged.getSumRes( problem, lppar )
        chipp = ggd.getChipow( problem, ggpar )
        print( "chipp = %8.3f   chisq = %8.3f"%( chipp, chisq ) )
        assertAAE( chisq, chipp )

        ggfi = numpy.asarray( [0,1,-2,-1] )
        lpfi = numpy.asarray( [0,1,-1] )
        logL = ged.logLikelihood( problem, lppar )
        lggL = ggd.logLikelihood( problem, ggpar )
        altL = ggd.logLikelihood_alt( problem, ggpar )

        print( "lggL  = %8.3f   logL  = %8.3f   alt  = %8.3f" % ( lggL, logL, altL ) )
        assertAAE( logL, lggL )
        assertAAE( altL, lggL )

        lLdata = ggd.logLdata( problem, ggpar )
        logL0 = numpy.sum( lLdata )
        print( "logL  = %8.3f   ldata = %8.3f" % (logL, logL0 ) )
        assertAAE( logL, logL0 )


        dL = ged.partialLogL( problem, lppar, lpfi )
        nL = ged.numPartialLogL( problem, lppar, lpfi )
        dG = ggd.partialLogL( problem, ggpar, ggfi)
        nG = ggd.numPartialLogL( problem, ggpar, ggfi )

        print( "partial = ", dL )
        print( "partial = ", dG )
        print( "numpart = ", nL )
#        print( "partalt = ", ged.partialLogL_alt( problem, lppar, lpfi ) )
        print( "numpart = ", nG )
        aG = ggd.partialLogL_alt( problem, ggpar, ggfi )
        print( "partalt = ", aG )

        assertAAE( dG, aG, 5 )
        assertAAE( dG[:3], dL, 5 )
        assertAAE( dG, nG, 5 )
        assertAAE( dL, nL, 5 )

        ggscl = 0.1
        hypar = [ggscl, power]
        sigma = ggscl / ff
        ggpar = numpy.append( param, hypar )
        lppar = numpy.append( param, [sigma] )
        logL = ged.logLikelihood( problem, lppar )
        lggL = ggd.logLikelihood( problem, ggpar )
        print( "lggL  = %8.3f   logL  = %8.3f" % ( lggL, logL ) )
        assertAAE( logL, lggL )

        ggscl = 0.5
        hypar = [ggscl, power]
        sigma = ggscl / ff
        print( "Super : ", hypar, "  sigma : ", sigma )
        ggpar = numpy.append( param, hypar )
        lppar = numpy.append( param, [sigma] )

        problem.weights = self.wgt
        dL = ged.partialLogL( problem, lppar, lpfi )
        nL = ged.numPartialLogL( problem, lppar, lpfi )
        dG = ggd.partialLogL( problem, ggpar, ggfi)
        nG = ggd.numPartialLogL( problem, ggpar, ggfi )

        print( "partial = ", dL )
        print( "partial = ", dG )
        print( "numpart = ", nL )
#        print( "partalt = ", ged.partialLogL_alt( problem, lppar, lpfi ) )
        print( "numpart = ", nG )
        print( "partalt = ", ggd.partialLogL_alt( problem, ggpar, ggfi ) )
        assertAAE( dG[:3], dL, 5 )
        assertAAE( dG, nG, 5 )
        assertAAE( dL, nL, 5 )

        for i in range( 11 ) :
            param = numpy.asarray( [i-5, 5, ggscl, power], dtype=float )
            print( param, "  :  ", end="" )
            for k in range( 9 ):
                print( " %8.3f" % ggd.logLikelihood( problem, param ), end="" )
                param[1] += 1
            print( "" )

    def testExponentialErrorDistribution2( self ):

        print( "=======   Test Exponential Error Distribution 2  ==================" )

        poly = PolynomialModel( 1 )
        param = numpy.asarray( [0.9,10], dtype=float )
        ged = GaussErrorDistribution( )
        ggd = ExponentialErrorDistribution( )

        print( str( ged ) )
        print( str( ggd ) )

        self.assertTrue( ggd.acceptWeight() )

        #   data = { -11, -9, -5, -5, -1, 1, 1, 5, 5, 8, 11 }
        #   f( x ) = { -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10 }
        #   f - d=     1   1  -1   1  -1 -1  1 -1  1  0  -1

        data = [ -11, -9, -5, -5, -1, 1, 1, 5, 5, 8, 11 ]
        problem = ClassicProblem( model=poly, xdata=self.x, ydata=data )

        power = 2.0
        scale = 1.0
        hypar = [scale, power]
        sigma = ggd.toSigma( hypar )
        print( hypar, sigma )
        ff = 1 / sigma
        ggpar = numpy.append( param, hypar )
        gapar = numpy.append( param, [sigma] )
#        gapar = numpy.append( param, [1.0] )

        chisq = ged.getChisq( problem, gapar )
        chipp = ggd.getChipow( problem, ggpar )
        print( "chipp = %8.3f   chisq = %8.3f"%( chipp, chisq ) )
#        assertAAE( chipp, chisq )


        logL = ged.logLikelihood( problem, gapar )
        lggL = ggd.logLikelihood( problem, ggpar )

        print( 'gapar  ', gapar )
        print( 'ggpar  ', ggpar )

        print( "lggL  = %8.3f   logL  = %8.3f" % ( lggL, logL ) )
        assertAAE( logL, lggL )

        ggfi = numpy.array( [0,1,-2,-1] )
        lpfi = numpy.array( [0,1,-1] )

        dL = ged.partialLogL( problem, gapar, lpfi )
        nL = ged.numPartialLogL( problem, gapar, lpfi )
        dG = ggd.partialLogL( problem, ggpar, ggfi)
        nG = ggd.numPartialLogL( problem, ggpar, ggfi )

        print( "partial = ", dL )
        print( "numpart = ", nL )
        print( "partalt = ", ged.partialLogL_alt( problem, gapar, lpfi ) )
        print( "partial = ", dG )
        print( "numpart = ", nG )
        print( "partalt = ", ggd.partialLogL_alt( problem, ggpar, ggfi ) )

        print( nG[-2] * ff )

        assertAAE( dG[:2], dL[:2], 5 )
        assertAAE( dG[2]*ff, dL[2], 5 )
        assertAAE( dG, nG, 5 )
        assertAAE( dL, nL, 5 )

        scale = 0.1
        hypar = [scale,power]
        sigma = ggd.toSigma( hypar )
        ggpar = numpy.append( param, hypar )
        gapar = numpy.append( param, [sigma] )
        logL = ged.logLikelihood( problem, gapar )
        lggL = ggd.logLikelihood( problem, ggpar )

        print( "lggL  = %8.3f   logL  = %8.3f" % ( lggL, logL ) )
        assertAAE( logL, lggL )

        dL = ged.partialLogL( problem, gapar, lpfi )
        nL = ged.numPartialLogL( problem, gapar, lpfi )
        dG = ggd.partialLogL( problem, ggpar, ggfi)
        nG = ggd.numPartialLogL( problem, ggpar, ggfi )

        print( "partial = ", dL )
        print( "numpart = ", nL )
        print( "partial = ", dG )
        print( "numpart = ", nG )
        assertAAE( dG[:2], dL[:2], 5 )
        assertAAE( dG[2]*ff, dL[2], 5 )
        assertAAE( dG, nG, 5 )
        assertAAE( dL, nL, 4 )

        scale = 0.5
        hypar = [scale, power]
        sigma = ggd.toSigma( hypar )
        print( "Super : ", hypar, "  sigma : ", sigma )
        ggpar = numpy.append( param, hypar )
        gapar = numpy.append( param, [sigma] )
        problem.weights = self.wgt

        logL = ged.logLikelihood( problem, gapar )
        lggL = ggd.logLikelihood( problem, ggpar )

        print( "lggL  = %8.3f   logL  = %8.3f" % ( lggL, logL ) )
        assertAAE( logL, lggL )

        dL = ged.partialLogL( problem, gapar, lpfi )
        nL = ged.numPartialLogL( problem, gapar, lpfi )
        dG = ggd.partialLogL( problem, ggpar, ggfi)
        nG = ggd.numPartialLogL( problem, ggpar, ggfi )

        print( "partial = ", dL )
        print( "numpart = ", nL )
        print( "partial = ", dG )
        print( "numpart = ", nG )
        assertAAE( dG[:2], dL[:2], 5 )
        assertAAE( dG[2]*ff, dL[2], 5 )
        assertAAE( dG, nG, 5 )
        assertAAE( dL, nL, 5 )

        for i in range( 11 ) :
            param = numpy.asarray( [i-5,5,scale,power], dtype=float )
            print( param, "  :  ", end="" )
            for k in range( 9 ):
                print( " %8.3f" % ggd.logLikelihood( problem, param ), end="" )
                param[1] += 1
            print( "" )

    def testModelDistribution( self ):
        print( "====== Test Model Distribution ======================" )
        poly = PolynomialModel( 1 )
        param = numpy.asarray( [12, 10], dtype=float )
        data = numpy.asarray( self.data + 13, dtype=int )
        print( "Data : ", data )

        problem = ClassicProblem( model=poly, xdata=self.x, ydata=data )

        ed = ModelDistribution( limits=[0.01,10] )
        printclass( ed )







    def testPoissonErrorDistribution( self ):
        print( "====== Test Poisson Error Distribution ======================" )
        poly = PolynomialModel( 1 )
        param = numpy.asarray( [12, 10], dtype=float )
        data = numpy.asarray( self.data + 13, dtype=int )
        print( "Data : ", data )

        problem = ClassicProblem( model=poly, xdata=self.x, ydata=data )

        ped = PoissonErrorDistribution( )
        print( str( ped ) )

        self.assertFalse( ped.acceptWeight() )

        logL = ped.logLikelihood( problem, param )
        print( "logL  = %8.3f"%( logL ) )
        scale = 0.1
        logL = ped.logLikelihood( problem, param )
        mok = problem.result( param )
        altL = ped.logLikelihood_alt( problem, param )

        lLdata = ped.logLdata( problem, param )
        logL0 = numpy.sum( lLdata )
        print( "logL  =  %8.3f  ldata %8.3f  alt %8.3f" % (logL, logL0, altL ) )
        assertAAE( logL, altL )
        assertAAE( logL, logL0 )

        print( "logL  = %8.3f  %8.3f" % ( logL, altL ) )
        assertAAE( logL, altL )

        logL = ped.logLikelihood( problem, [-5, 0] )
        print( "logL  = %8.3f"%( logL ) )
        self.assertTrue( math.isinf( logL ) )

        scale = 1.0
        fitIndex = [0,1]
        dL = ped.partialLogL( problem, param, fitIndex )
        nL = ped.numPartialLogL( problem, param, fitIndex )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        scale = 0.5
        dL = ped.partialLogL( problem, param, fitIndex )
        nL = ped.numPartialLogL( problem, param, fitIndex )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        aG = ped.partialLogL_alt( problem, param, fitIndex )
        print( "partalt = ", aG )
        assertAAE( dL, aG, 5 )

        scale = 1.0
        for i in range( 10 ) :
            param = numpy.asarray( [8+i,4], dtype=float )
            print( param, "  :  ", end="" )
            for k in range( 9 ):
                print( " %8.3f" % ped.logLikelihood( problem, param ), end="" )
                param[1] += 1
            print( "" )


    def testBernoulliErrorDistribution( self ):
        print( "====== Test Bernoulli Error Distribution ======================" )
        poly = LogisticModel( fixed={0:1} )
        param = numpy.asarray( [0.5,1.0], dtype=float )
        data = numpy.asarray( [0,0,0,0,0,1,1,1,1,1,1], dtype=int )
        data = numpy.asarray( [1,1,1,1,1,1,0,0,0,0,0], dtype=int )

        print( "x    : ", fmt( self.x, max=None ) )
        print( "Data : ", fmt( data, max=None ) )
        print( "yfit : ", fmt( poly.result( self.x, param ), max=None ) )

        problem = ClassicProblem( model=poly, xdata=self.x, ydata=data )

        ped = BernoulliErrorDistribution( )
        print( str( ped ) )

        self.assertFalse( ped.acceptWeight() )

        logL = ped.logLikelihood( problem, param )
        print( "logL  = %8.3f"%( logL ) )

        logL = ped.logLikelihood( problem, param )
        mok = problem.result( param )
        altL = ped.logLikelihood_alt( problem, param )

        lLdata = ped.logLdata( problem, param )
        print( "Ldata: ", fmt( lLdata, max=None ) )
        logL0 = numpy.sum( lLdata )
        print( "logL  =  %8.3f  ldata %8.3f  alt %8.3f" % (logL, logL0, altL ) )
        assertAAE( logL, altL )
        assertAAE( logL, logL0 )

        print( "logL  = %8.3f  %8.3f" % ( logL, altL ) )
        assertAAE( logL, altL )

        fitIndex = [0,1]
        dL = ped.partialLogL( problem, param, fitIndex )
        nL = ped.numPartialLogL( problem, param, fitIndex )
        aL = ped.partialLogL_alt( problem, param, fitIndex )
        print( "partial = ", dL )
        print( "altpart = ", aL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        print( "             ", fmt( [4.0/(k+1) for k in range( 9 )], max=None ) )
        for i in range( 10 ) :
            param = numpy.asarray( [i-4,1], dtype=float )
            print( fmt( param[0] ), "  :  ", end="" )
            for k in range( 9 ):
                param[1] = 4.0 / ( k + 1 )
                print( " %8.3f" % ped.logLikelihood( problem, param ), end="" )

            print( "" )


    def testCauchyErrorDistribution( self ):
        print( "\n   Test Cauchy Error Distribution\n" )
        poly = PolynomialModel( 1 )

        problem = ClassicProblem( model=poly, xdata=self.x, ydata=self.data )

        ced = CauchyErrorDistribution( )
        self.assertFalse( ced.acceptWeight() )

        param = numpy.asarray( [1,10,1], dtype=float )
        logL = ced.logLikelihood( problem, param )
        print( "logL  =  %8.3f" % ( logL ) )
        scale = 0.1
        s2 = scale * scale
        param[2] = scale
        logL = ced.logLikelihood( problem, param )
        altL = ced.logLikelihood_alt( problem, param )

        lLdata = ced.logLdata( problem, param )
        logL0 = numpy.sum( lLdata )
        print( "logL  =  %8.3f  ldata %8.3f  alt %8.3f" % (logL, logL0, altL ) )
        assertAAE( logL, altL )
        assertAAE( logL, logL0 )

#        print( "logL  =  %8.3f  alt %8.3f" % (logL, altL ) )
#        assertAAE( logL, altL )

        scale = 1.0
        param[2] = scale
        fi = [0,1,-1]
        dL = ced.partialLogL( problem, param, fi )
        nL = ced.numPartialLogL( problem, param, fi )
        print( "params  = ", param, scale )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 2 )

        scale = 0.5
        param[2] = scale
        dL = ced.partialLogL( problem, param, fi )
        nL = ced.numPartialLogL( problem, param, fi )
        print( "params  = ", param, scale )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 2 )

        aG = ced.partialLogL_alt( problem, param, fi )
        print( "partalt = ", aG )
        assertAAE( dL, aG, 5 )


        for i in range( 11 ):
            param = numpy.asarray( [i-5,5,1], dtype=float )
            print( param, ":  ", end="" )
            for k in range( 9 ):
                print( " %8.3f" % ced.logLikelihood( problem, param ), end="" )
                param[1] += 1
            print( "" )


    def testLaplaceErrorDistribution( self ):
        print( "\n   Test Laplace Error Distribution\n" )
        poly = PolynomialModel( 1 )

        problem = ClassicProblem( model=poly, xdata=self.x, ydata=self.data )

        ced = LaplaceErrorDistribution( )
        print( str( ced ) )

        self.assertTrue( ced.acceptWeight() )

        param = numpy.asarray( [1,10,1], dtype=float )
        logL = ced.logLikelihood( problem, param )
        print( "logL  =  %8.3f" % ( logL ) )
        scale = 0.1
        param[2] = scale
        s2 = scale * scale
        logL = ced.logLikelihood( problem, param )

        altL = ced.logLikelihood_alt( problem, param )

        lLdata = ced.logLdata( problem, param )
        logL0 = numpy.sum( lLdata )
        print( "logL  =  %8.3f  ldata %8.3f  alt %8.3f" % (logL, logL0, altL ) )
        assertAAE( logL, altL )
        assertAAE( logL, logL0 )


        scale = 1.0
        param[2] = scale
        fi = [0,1,-1]
        dL = ced.partialLogL( problem, param, fi )
        nL = ced.numPartialLogL( problem, param, fi )
        print( "params  = ", param, scale )
        print( "partial = ", dL )
        print( "partalt = ", ced.partialLogL_alt( problem, param, fi ) )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 2 )

        scale = 0.5
        param[2] = scale
        problem.weights = self.wgt
        dL = ced.partialLogL( problem, param, fi )
        nL = ced.numPartialLogL( problem, param, fi )
        print( "params  = ", param, scale )
        print( "partial = ", dL )
        print( "partalt = ", ced.partialLogL_alt( problem, param, fi ) )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 2 )

        logL = ced.logLikelihood( problem, param )
        cced = ced.copy()
        logLc = cced.logLikelihood( problem, param )
        print( cced )
        print( "logL  =  %8.3f  copy %8.3f" % (logL, logLc ) )
        dLc = cced.partialLogL( problem, param, fi )
        print( "params  = ", param, scale )
        print( "partial = ", dL )
        assertAAE( logL, logLc, 6 )
        assertAAE( dL, dLc, 6 )

        for i in range( 11 ):
            param = numpy.asarray( [i-5,5,1], dtype=float )
            print( param, ":  ", end="" )
            for k in range( 9 ):
                print( " %8.3f" % ced.logLikelihood( problem, param ), end="" )
                param[1] += 1
            print( "" )

    def testUniformErrorDistribution( self ):
        print( "\n   Test Uniform Error Distribution\n" )
        poly = PolynomialModel( 1 )

        problem = ClassicProblem( model=poly, xdata=self.x, ydata=self.data )

        ced = UniformErrorDistribution( )
        print( str( ced ) )

        print( "x   ", self.x )
        print( "y   ", self.data )
        self.assertTrue( ced.acceptWeight() )

        param = numpy.asarray( [0.3,11,4], dtype=float )
        print( "m   ", problem.result( param ) )
        logL = ced.logLikelihood( problem, param )
        altL = ced.logLikelihood_alt( problem, param )
        print( "logL  =  %8.3f  altL  %8.3f" % ( logL, altL ) )
        assertAAE( logL, altL )

        scale = 1.0
        param[2] = scale
        logL = ced.logLikelihood( problem, param )

        lLdata = ced.logLdata( problem, param )
        logL0 = numpy.sum( lLdata )
        print( "logL  =  %8.3f  ldata %8.3f" % (logL, logL0 ) )
        assertAAE( logL, logL0 )

        print( "logL  =  %12.3g" % (logL) )
        self.assertTrue( logL == -math.inf )

        scale = 4.0
        param[2] = scale
        fi = [0,1,-1]
        dL = ced.partialLogL( problem, param, fi )
        nL = ced.numPartialLogL( problem, param, fi )
        print( "params  = ", param, scale )
        print( "partial = ", dL )
        print( "partalt = ", ced.partialLogL_alt( problem, param, fi ) )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 2 )

        scale = 5
        param[2] = scale
        problem.weights = self.wgt
        dL = ced.partialLogL( problem, param, fi )
        nL = ced.numPartialLogL( problem, param, fi )
        print( "params  = ", param, scale )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 2 )

        logL = ced.logLikelihood( problem, param )
        cced = ced.copy()
        logLc = cced.logLikelihood( problem, param )
        print( cced )
        print( "logL  =  %8.3f  copy %8.3f" % (logL, logLc ) )
        dLc = cced.partialLogL( problem, param, fi )
        print( "params  = ", param, scale )
        print( "partial = ", dL )
        assertAAE( logL, logLc, 6 )
        assertAAE( dL, dLc, 6 )

        for i in range( 11 ):
            param = numpy.asarray( [i-5,5,10], dtype=float )
            print( param, ":  ", end="" )
            for k in range( 9 ):
                print( " %6.2f" % ced.logLikelihood( problem, param ), end="" )
                param[1] += 1
            print( "" )

    def testMixedErrorDistribution0( self ):
        print( "\n   Test Mixed Error Distribution 0\n" )
        m = PolynomialModel( 0 )
        x = numpy.linspace( -10, 10, 201 )
        problem = ClassicProblem( m, x, x )
        ed1 = GaussErrorDistribution( )
#        ed2 = GaussErrorDistribution( )
        ed2 = UniformErrorDistribution( )

        ced = MixedErrorDistribution( ed1, ed2  )
        print( str( ced ) )

        param = numpy.asarray( [0.0, 0.3, 5, 0.7 ], dtype=float )
        if self.doplot :
            for k in range( 5 ) :
                param[3] = 0.25 * k
                lld = ced.logLdata( problem, param )
                plt.plot( x, numpy.exp( lld ) )
            plt.title( ced.__str__() )
            plt.show()



    def testMixedErrorDistribution( self ):
        print( "\n   Test Mixed Error Distribution\n" )
        poly = PolynomialModel( 1 )

        problem = ClassicProblem( model=poly, xdata=self.x, ydata=self.data )

        ed1 = GaussErrorDistribution( )
        ed2 = UniformErrorDistribution( )
        ced = MixedErrorDistribution( ed1, ed2  )

        self.assertTrue( ced.acceptWeight() )

        param = numpy.asarray( [0.3, 11, 1, 4, 0.7 ], dtype=float )

        logL = ced.logLikelihood( problem, param )
        print( "logL  =  %8.3f" % ( logL ) )
#        self.assertTrue( logL == -11 * math.log( 2 * param[2] ) )

        param[2:4] *= 0.097
#        param[4] = 0.7
        logL = ced.logLikelihood( problem, param )


        print( "logL  =  %8.3f" % (logL) )
        print( "lld  ", ced.logLdata( problem, param ) )
        pars = param[:3]
        print( "ll1  ", ced.errdis1.logLdata( problem, pars ) )
        pars[2] = param[3]
        print( "ll2  ", ced.errdis2.logLdata( problem, param ) )


        fi = [0,1,-3,-2,-1]
        dL = ced.partialLogL( problem, param, fi )
        nL = ced.numPartialLogL( problem, param, fi )
        print( "params  = ", param )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 2 )

#        self.assertTrue( logL == -math.inf )

        scale = 2.0
        param[2] = 0.1 * scale      ## gauss
        param[3] = scale            ## uniform
        fi = [0,1,-3,-2,-1]
        dL = ced.partialLogL( problem, param, fi )
        nL = ced.numPartialLogL( problem, param, fi )
        print( "params  = ", param )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 2 )

        scale = 5
        param[2] = scale
        problem.weights = self.wgt
        dL = ced.partialLogL( problem, param, fi )
        nL = ced.numPartialLogL( problem, param, fi )
        print( "params  = ", param, scale )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 2 )

        print( "make a copy" )
        logL = ced.logLikelihood( problem, param )
        cced = ced.copy()
        logLc = cced.logLikelihood( problem, param )
        print( cced )
        print( "logL  =  %8.3f  copy %8.3f" % (logL, logLc ) )
        dLc = cced.partialLogL( problem, param, fi )
        print( "params  = ", param, scale )
        print( "partial = ", dL )
        assertAAE( logL, logLc, 6 )
        assertAAE( dL, dLc, 6 )

        for i in range( 11 ):
            param = numpy.asarray( [i-5,5,0.2,1.0,0.7], dtype=float )
            print( param )
            for k in range( 9 ):
                print( " %10.3g" % ced.logLikelihood( problem, param ), end="" )
                param[1] += 1
            print( "" )


    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( ErrorDistributionTest.__class__ )


