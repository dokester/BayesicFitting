## run as : python3 -m unittest TestErrorDistribution

from __future__ import print_function

import numpy as numpy
from numpy.testing import assert_array_almost_equal as assertAAE
import unittest
import os
import math
import matplotlib.pyplot as plt

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

class Test( unittest.TestCase ):
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

    # Define acc as accuracies
    acc0 = 0.7
    acc1 = 1.0 / numpy.sqrt( wgt )

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
            scale = errdis.getScale( problem, allpars )
            sigma = errdis.toSigma( scale )
            print( fmt( k ), fmt( nf ), fmt( scale ), fmt( sigma ) )
            nf *= 10
        if self.doplot:
            self.ploterrdis( noise, errdis, problem, allpars, num_bins=40 )

        nf = 0.01
        errdis = LaplaceErrorDistribution( )
        print( errdis )
        for k in range( 5 ) :
            noise = numpy.random.laplace( size=nn )
            y = ym + nf * noise
            problem.ydata = y
            scale = errdis.getScale( problem, allpars )
            sigma = errdis.toSigma( scale )
            print( fmt( k ), fmt( nf ), fmt( scale ), fmt( sigma ) )
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
            scale = errdis.getScale( problem, allpars )
            sigma = errdis.toSigma( scale )
            print( fmt( k ), fmt( nf ), fmt( scale ), fmt( sigma ) )
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
            noise = numpy.maximum( noise, -20 )
            noise = numpy.minimum( noise, +20 )
            y = ym + nf * noise
            problem.ydata = y
            scale = errdis.getScale( problem, allpars )
            sigma = errdis.toSigma( scale )
            print( fmt( k ), fmt( nf ), fmt( scale ), fmt( sigma ) )
            nf *= 10
        if self.doplot :
            self.ploterrdis( noise, errdis, problem, allpars, num_bins=200 )


        nf = 0.01
        errdis = ExponentialErrorDistribution( )
        power = 1.0
        allpars = [0.0, 1.0, 1.0]
        print( errdis, "  power=1" )
        for k in range( 5 ) :
            noise = numpy.random.laplace( size=nn )
            y = ym + nf * noise
            problem.ydata = y
            scale = errdis.getScale( problem, allpars )
            sigma = errdis.toSigma( [scale,power] )
            print( fmt( k ), fmt( nf ), fmt( scale ), fmt( sigma ) )
            nf *= 10
        if self.doplot :
            self.ploterrdis( noise, errdis, problem, allpars, num_bins=200 )

        nf = 0.01
        errdis = ExponentialErrorDistribution( )
        allpars = [0.0, 1.0, 2.0]
        power = 2
        print( errdis, "  power=2"  )
        for k in range( 5 ) :
            noise = numpy.random.randn( nn )
            y = ym + nf * noise
            problem.ydata = y
            scale = errdis.getScale( problem, allpars )
            sigma = errdis.toSigma( [scale,power] )
            print( fmt( k ), fmt( nf ), fmt( scale ), fmt( sigma ) )
            nf *= 10
        if self.doplot :
            self.ploterrdis( noise, errdis, problem, allpars, num_bins=200 )

        nf = 0.01
        power = 10
        errdis = ExponentialErrorDistribution ( )
        allpars = [0.0, 1.0, 10.0]
        print( errdis, "  power=%d" % power  )
        for k in range( 5 ) :
            noise = 2 * numpy.random.rand( nn ) - 1.0
            y = ym + nf * noise
            problem.ydata = y
            scale = errdis.getScale( problem, allpars )
            sigma = errdis.toSigma( [scale,power] )
            print( fmt( k ), fmt( nf ), fmt( scale ), fmt( sigma ) )
            nf *= 10
        if self.doplot :
            self.ploterrdis( noise, errdis, problem, allpars, num_bins=200 )


    def ploterrdis( self, noise, errdis, problem, allpars, num_bins=20 ) :

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


    def stdtest( self, errdis, problem, param, fitIndex ) :

        chisq = errdis.getChisq( problem, param )
        print( "chisq = %8.3f"%( chisq ) )
        lLdata = errdis.logLdata( problem, param )
        logL0 = numpy.sum( lLdata )

        logL = errdis.logLikelihood( problem, param )
        altL = errdis.logLikelihood_alt( problem, param )
        print( "logL0 ", fmt( logL0 ) )
        print( "logL  ", fmt( logL ) )
        print( "altL  ", fmt( altL ) )
        assertAAE( logL, altL )
        assertAAE( logL, logL0 )

        dL = errdis.partialLogL( problem, param, fitIndex )
        aL = errdis.partialLogL_alt( problem, param, fitIndex )
        nL = errdis.numPartialLogL( problem, param, fitIndex )
        print( "partial = ", dL )
        print( "partalt = ", aL )
        print( "numpart = ", nL )
        assertAAE( dL, aL, 5 )
        assertAAE( dL, nL, 5 )



    def testGaussErrorDistribution( self ):

        print( "=======   Test Gauss Error Distribution  ==================" )

        poly = PolynomialModel( 1 )
        param = numpy.asarray( [1,10,1], dtype=float )
        ged = GaussErrorDistribution( )
        self.assertTrue( ged.acceptWeight() )

        problem = ClassicProblem( model=poly, xdata=self.x, ydata=self.data,
                  accuracy=self.acc0 )

        #   data = { -11, -9, -5, -5, -1, 1, 1, 5, 5, 8, 11 }
        #   f( x ) = { -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10 }
        #   f - d=     1   1  -1   1  -1 -1  1 -1  1  0  -1

        print( "Using variable scale = 1.0 and accuracies" )
        fitIndex = [0,1,-1]
        self.stdtest( ged, problem, param, fitIndex )

        print( "Using variable scale = 0.1 and accuracies" )
        scale = 0.1
        param[2] = scale
        self.stdtest( ged, problem, param, fitIndex )


        print( "Using fixed scale = 1.0 and accuracies" )
        scale = 1.0
        param[2] = scale
        fitIndex = numpy.asarray( [0,1] )
        self.stdtest( ged, problem, param, fitIndex )


        print( "Using fixed scale = 0.5 and accuracies nad weights." )
        scale = 0.5
        param[2] = scale
        problem.weights = self.wgt
        self.stdtest( ged, problem, param, fitIndex )


        scale = 1.0
        for i in range( 11 ) :
            param = numpy.asarray( [i-5,5,1], dtype=float )
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

        problem = ClassicProblem( model=gm, xdata=self.x, ydata=self.data, accuracy=self.acc1 )
        fitIndex = [0,1,2,3,4,-1]

        ged = GaussErrorDistribution( )
        Tools.printclass( ged )
        np = gm.npchain
        self.stdtest( ged, problem, param, fitIndex )


        scale = 0.1
        param[np] = scale
        self.stdtest( ged, problem, param, fitIndex )


        scale = 1.0
        param[np] = scale
        self.stdtest( ged, problem, param, fitIndex )


        fitIndex = numpy.asarray( [0,2,3,4] )
        self.stdtest( ged, problem, param, fitIndex )


        scale = 0.5
        param[np] = scale
        fitIndex = numpy.asarray( [0,1,2,3,4,-1] )
        problem.weights = self.wgt
        self.stdtest( ged, problem, param, fitIndex )


        scale = 0.5
        param[np] = scale
        fitIndex = numpy.asarray( [0,1,2,4,-1] )
        self.stdtest( ged, problem, param, fitIndex )

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
        ged = ExponentialErrorDistribution( )

        param = numpy.asarray( [1, 10, 0.2, 1.4], dtype=float )
        print( "par   ", param )
        self.stdEDtest( ged, param )


        param = numpy.asarray( [1, 10, 1.2, 3.4], dtype=float )
        print( "par   ", param )
        self.stdEDtest( ged, param )

    def stdEDtest( self, ged, param ) :

        poly = PolynomialModel( 1 )

        print( "---%s with fixed single scale-------" % ged )
        problem = ClassicProblem( model=poly, xdata=self.x, ydata=self.data, accuracy=self.acc0 )
        fitIndex = [0,1]
        self.stdtest( ged, problem, param, fitIndex )

        print( "---%s with fixed single scale and weights-------" %ged )
        problem.weights = self.wgt
        self.stdtest( ged, problem, param, fitIndex )


        print( "---%s with fixed scale per data-------" % ged )
        problem = ClassicProblem( model=poly, xdata=self.x, ydata=self.data, accuracy=self.acc1 )
        self.stdtest( ged, problem, param, fitIndex )

        print( "---%s with fixed scale and weights-------" % ged )
        problem.weights = self.wgt
        self.stdtest( ged, problem, param, fitIndex )


    def testCauchyErrorDistribution( self ):
        print( "\n   Test Cauchy Error Distribution\n" )
        poly = PolynomialModel( 1 )

        problem = ClassicProblem( model=poly, xdata=self.x, ydata=self.data )

        param = numpy.asarray( [1,10,1], dtype=float )

        ced = CauchyErrorDistribution( )

        self.stdEDtest( ced, param ) 


    def testLaplaceErrorDistribution( self ):
        print( "\n   Test Laplace Error Distribution\n" )
        poly = PolynomialModel( 1 )

        problem = ClassicProblem( model=poly, xdata=self.x, ydata=self.data )

        param = numpy.asarray( [1,10,1], dtype=float )
        ced = LaplaceErrorDistribution( )

        self.stdEDtest( ced, param ) 

    def testUniformErrorDistribution( self ):
        print( "\n   Test Uniform Error Distribution\n" )
        poly = PolynomialModel( 1 )

        problem = ClassicProblem( model=poly, xdata=self.x, ydata=self.data )

        self.acc0 *= 5
        self.acc1 *= 5

        ced = UniformErrorDistribution( )

        param = numpy.asarray( [0.3,11,4], dtype=float )
        self.stdEDtest( ced, param ) 



    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( ErrorDistributionTest.__class__ )


