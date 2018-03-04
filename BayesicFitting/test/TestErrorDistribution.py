## run as : python3 -m unittest TestErrorDistribution

from __future__ import print_function

import numpy as numpy
from numpy.testing import assert_array_almost_equal as assertAAE
import unittest
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
#  *  2017 Do Kester

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

    def __init__( self, name ):
        super( TestErrorDistribution, self ).__init__( name )
        numpy.set_printoptions(formatter={'float': '{: 0.3f}'.format})

    def test1( self, plot=False ) :
        print( "====test1============================" )
        nn = 10000
        x = numpy.linspace( 0, 1, nn, dtype=float )
        ym = 0.0 * x
        nf = 0.01

        model = PolynomialModel( 0 )
        model.parameters = 0.0
        numpy.random.seed( 2345 )
        noise = numpy.random.randn( nn )

        errdis = GaussErrorDistribution ( x, ym )
        print( errdis )
        for k in range( 5 ) :
            noise = numpy.random.randn( nn )
            y = ym + nf * noise
            errdis.data = y
            print( fmt( k ), fmt( nf ), fmt( errdis.getScale( model ) ) )
            nf *= 10
        allpars = [0.0, 1.0]
        if plot:
            self.ploterrdis( noise, errdis, model, allpars )

        nf = 0.01
        errdis = LaplaceErrorDistribution ( x, ym )
        print( errdis )
        for k in range( 5 ) :
            noise = numpy.random.laplace( size=nn )
            y = ym + nf * noise
            errdis.data = y
            print( fmt( k ), fmt( nf ), fmt( errdis.getScale( model ) ) )
            nf *= 10

        nf = 0.01
        errdis = CauchyErrorDistribution ( x, ym )
        cp = CauchyPrior()
        print( errdis )
        for k in range( 5 ) :
            noise = numpy.random.rand( nn )
            noise = cp.unit2Domain( noise )
            y = ym + nf * noise
            errdis.data = y
            print( fmt( k ), fmt( nf ), fmt( errdis.getScale( model ) ) )
            nf *= 10

        nf = 0.01
        errdis = GenGaussErrorDistribution ( x, ym, power=1 )
        print( errdis, "  power=1" )
        for k in range( 5 ) :
            noise = numpy.random.laplace( size=nn )
            y = ym + nf * noise
            errdis.data = y
            print( fmt( k ), fmt( nf ), fmt( errdis.getScale( model ) ) )
            nf *= 10

        nf = 0.01
        errdis = GenGaussErrorDistribution ( x, ym, power=2 )
        print( errdis, "  power=2"  )
        for k in range( 5 ) :
            noise = numpy.random.randn( nn )
            y = ym + nf * noise
            errdis.data = y
            print( fmt( k ), fmt( nf ), fmt( errdis.getScale( model ) ) )
            nf *= 10

        nf = 0.01
        power = 10
        errdis = GenGaussErrorDistribution ( x, ym, power=power )
        print( errdis, "  power=%d" % power  )
        for k in range( 5 ) :
            noise = 2 * numpy.random.rand( nn ) - 1.0
            y = ym + nf * noise
            errdis.data = y
            print( fmt( k ), fmt( nf ), fmt( errdis.getScale( model ) ) )
            nf *= 10

        allpars = [0.0, 1.0, power]
        if plot :
            self.ploterrdis( noise, errdis, model, allpars )

    def ploterrdis( self, noise, errdis, model, allpars ) :
        num_bins = 20
        plt.hist( noise, num_bins, normed=1, facecolor='g', alpha=0.5 )
        xx = numpy.linspace( -0.3, 0.3, 601, dtype=float )
        lik = numpy.zeros_like( xx )
        for k,p in enumerate( xx ) :
            allpars[0] = p
            lik[k] = errdis.logLikelihood( model, allpars )
        maxlik = numpy.max( lik )
        plt.plot( xx, numpy.exp( lik - maxlik ), 'r-' )
        plt.show()


    def testGaussErrorDistribution( self ):

        print( "=======   Test Gauss Error Distribution  ==================" )

        poly = PolynomialModel( 1 )
        param = numpy.asarray( [1,10,1], dtype=float )
        ged = GaussErrorDistribution( self.x, self.data )
        self.assertTrue( ged.acceptWeight() )

        #   data = { -11, -9, -5, -5, -1, 1, 1, 5, 5, 8, 11 }
        #   f( x ) = { -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10 }
        #   f - d=     1   1  -1   1  -1 -1  1 -1  1  0  -1

        chisq = ged.getChisq( ged.getResiduals( poly, param[:2] ), param[2] )
        print( "chisq = %8.3f"%( chisq ) )
        logL = ged.logLikelihood( poly, param )
        altL = -0.5 * ( 11 * math.log( 2 * math.pi ) + chisq )
        print( "logL  = %8.3f  %8.3f" % ( logL, altL ) )
        assertAAE( logL, altL )

        scale = 0.1
        param[2] = scale
        logL = ged.logLikelihood( poly, param )
        altL = -11 * ( 0.5 * math.log( 2 * math.pi ) +
                    math.log( scale ) ) - 0.5 * chisq / ( scale * scale )
        print( "logL  = %8.3f  %8.3f" % ( logL, altL ) )
        assertAAE( logL, altL )

        scale = 1.0
        param[2] = scale
        fitIndex = numpy.arange( 3 )
        dL = ged.partialLogL( poly, param, fitIndex )
        nL = ged.numPartialLogL( poly, param, fitIndex )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        scale = 0.5
        param[2] = scale
        ged.weights = self.wgt
        dL = ged.partialLogL( poly, param, fitIndex )
        nL = ged.numPartialLogL( poly, param, fitIndex )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        scale = 1.0
        for i in range( 11 ) :
            param = numpy.asarray( [i-5,5,1], dtype=float )
            print( param, "  :  ", end="" )
            for k in range( 9 ):
                print( " %8.3f" % ged.logLikelihood( poly, param ), end="" )
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

        ged = GaussErrorDistribution( self.x, data2 )
        Tools.printclass( ged )
        np = gm.npchain
        chisq = ged.getChisq( ged.getResiduals( gm, param[:np] ), param[np] )
        print( "chisq = %8.3f"%( chisq ) )
        logL = ged.logLikelihood( gm, param )

        print( "logL  = %8.3f  %8.3f" % ( logL, -0.5 * ( 11 * math.log( 2 * math.pi ) + chisq) ) )
        assertAAE( logL, -0.5 * ( 11 * math.log( 2 * math.pi ) + chisq) )

        scale = 0.1
        param[np] = scale
        logL = ged.logLikelihood( gm, param )
        altL = ( -11 * ( 0.5 * math.log( 2 * math.pi ) +
                    math.log( scale ) ) - 0.5 * chisq / ( scale * scale ) )
        print( "logL  = %8.3f  %8.3f" % ( logL, altL ) )
        assertAAE( logL, altL )

        scale = 1.0
        param[np] = scale
        fitIndex = numpy.arange( np+1 )
        dL = ged.partialLogL( gm, param, fitIndex )
        nL = ged.numPartialLogL( gm, param, fitIndex )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        fitIndex = numpy.asarray( [0,2,3,4] )
        dL = ged.partialLogL( gm, param, fitIndex )
        nL = ged.numPartialLogL( gm, param, fitIndex )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        scale = 0.5
        param[np] = scale
        fitIndex = numpy.asarray( [0,1,2,3,4,5] )
        ged.weights = self.wgt
        dL = ged.partialLogL( gm, param, fitIndex )
        nL = ged.numPartialLogL( gm,  param, fitIndex )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        scale = 0.5
        param[np] = scale
        fitIndex = numpy.asarray( [0,1,2,4,5] )
        ged.weights = self.wgt
        ged.hyperpar[0] = NoiseScale()
        Tools.printclass( ged )
        ged.keepFixed( fixed={0:2.5} )
        Tools.printclass( ged )
        Tools.printclass( ged.hyperpar[0] )

        dL = ged.partialLogL( gm, param, fitIndex )
        nL = ged.numPartialLogL( gm, param, fitIndex )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

    def testGenGaussErrorDistribution1( self ):

        print( "=======   Test Gen Gauss Error Distribution 1 ==================" )

        poly = PolynomialModel( 1 )
        param = numpy.asarray( [1,10], dtype=float )
        ged = LaplaceErrorDistribution( self.x, self.data )
        ggd = GenGaussErrorDistribution( self.x, self.data )
        self.assertTrue( ggd.acceptWeight() )

        #   data = { -11, -9, -5, -5, -1, 1, 1, 5, 5, 8, 11 }
        #   f( x ) = { -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10 }
        #   f - d=     1   1  -1   1  -1 -1  1 -1  1  0  -1

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
        res = ggd.getResiduals( poly, param )
        chisq = ged.getSumRes( res, lpscl )
        chipp = ggd.getChisq( res, ggscl, power )
        print( "chipp = %8.3f   chisq = %8.3f"%( chipp, chisq ) )
        ggfi = numpy.arange( 4 )
        lpfi = numpy.arange( 3 )
        logL = ged.logLikelihood( poly, lppar )
        lggL = ggd.logLikelihood( poly, ggpar )

        print( "lggL  = %8.3f   logL  = %8.3f" % ( lggL, logL ) )
        assertAAE( logL, lggL )

        dL = ged.partialLogL( poly, lppar, lpfi )
        nL = ged.numPartialLogL( poly, lppar, lpfi )
        dG = ggd.partialLogL( poly, ggpar, ggfi)
        nG = ggd.numPartialLogL( poly, ggpar, ggfi )

        print( "partial = ", dL )
        print( "partial = ", dG )
        print( "numpart = ", nL )
        print( "numpart = ", nG )
        assertAAE( dG[:3], dL, 5 )
        assertAAE( dG, nG, 5 )
        assertAAE( dL, nL, 5 )

        ggscl = 0.1
        hypar = [ggscl, power]
        sigma = ggscl / ff
        ggpar = numpy.append( param, hypar )
        lppar = numpy.append( param, [sigma] )
        logL = ged.logLikelihood( poly, lppar )
        lggL = ggd.logLikelihood( poly, ggpar )
        print( "lggL  = %8.3f   logL  = %8.3f" % ( lggL, logL ) )
        assertAAE( logL, lggL )

        ggscl = 0.5
        hypar = [ggscl, power]
        sigma = ggscl / ff
        print( "Super : ", hypar, "  sigma : ", sigma )
        ggpar = numpy.append( param, hypar )
        lppar = numpy.append( param, [sigma] )

        ged.weights = self.wgt
        ggd.weights = self.wgt
        dL = ged.partialLogL( poly, lppar, lpfi )
        nL = ged.numPartialLogL( poly, lppar, lpfi )
        dG = ggd.partialLogL( poly, ggpar, ggfi)
        nG = ggd.numPartialLogL( poly, ggpar, ggfi )

        print( "partial = ", dL )
        print( "partial = ", dG )
        print( "numpart = ", nL )
        print( "numpart = ", nG )
        assertAAE( dG[:3], dL, 5 )
        assertAAE( dG, nG, 5 )
        assertAAE( dL, nL, 5 )

        for i in range( 11 ) :
            param = numpy.asarray( [i-5, 5, ggscl, power], dtype=float )
            print( param, "  :  ", end="" )
            for k in range( 9 ):
                print( " %8.3f" % ggd.logLikelihood( poly, param ), end="" )
                param[1] += 1
            print( "" )

    def testGenGaussErrorDistribution2( self ):

        print( "=======   Test Gen Gauss Error Distribution 2  ==================" )

        poly = PolynomialModel( 1 )
        param = numpy.asarray( [1,10], dtype=float )
        ged = GaussErrorDistribution( self.x, self.data )
        ggd = GenGaussErrorDistribution( self.x, self.data )
        self.assertTrue( ggd.acceptWeight() )

        #   data = { -11, -9, -5, -5, -1, 1, 1, 5, 5, 8, 11 }
        #   f( x ) = { -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10 }
        #   f - d=     1   1  -1   1  -1 -1  1 -1  1  0  -1

        power = 2.0
        scale = 1.0
        hypar = [scale, power]
        sigma = ggd.toSigma( hypar )
        print( hypar, sigma )
        ff = 1 / sigma
        ggpar = numpy.append( param, hypar )
        gapar = numpy.append( param, [sigma] )
        res = ggd.getResiduals( poly, param )
        chisq = ged.getChisq( res, scale )
        chipp = ggd.getChisq( res, scale, power )
        print( "chipp = %8.3f   chisq = %8.3f"%( chipp, chisq ) )
        logL = ged.logLikelihood( poly, gapar )
        lggL = ggd.logLikelihood( poly, ggpar )

        print( "lggL  = %8.3f   logL  = %8.3f" % ( lggL, logL ) )
        assertAAE( logL, lggL )

        ggfi = numpy.arange( 4 )
        lpfi = numpy.arange( 3 )
        dL = ged.partialLogL( poly, gapar, lpfi )
        nL = ged.numPartialLogL( poly, gapar, lpfi )
        dG = ggd.partialLogL( poly, ggpar, ggfi)
        nG = ggd.numPartialLogL( poly, ggpar, ggfi )

        print( "partial = ", dL )
        print( "partial = ", dG )
        print( "numpart = ", nL )
        print( "numpart = ", nG )
        assertAAE( dG[:2], dL[:2], 5 )
        assertAAE( dG[2]*ff, dL[2], 5 )
        assertAAE( dG, nG, 5 )
        assertAAE( dL, nL, 5 )

        scale = 0.1
        hypar = [scale,power]
        sigma = ggd.toSigma( hypar )
        ggpar = numpy.append( param, hypar )
        gapar = numpy.append( param, [sigma] )
        logL = ged.logLikelihood( poly, gapar )
        lggL = ggd.logLikelihood( poly, ggpar )

        print( "lggL  = %8.3f   logL  = %8.3f" % ( lggL, logL ) )
        assertAAE( logL, lggL )

        dL = ged.partialLogL( poly, gapar, lpfi )
        nL = ged.numPartialLogL( poly, gapar, lpfi )
        dG = ggd.partialLogL( poly, ggpar, ggfi)
        nG = ggd.numPartialLogL( poly, ggpar, ggfi )

        print( "partial = ", dL )
        print( "partial = ", dG )
        print( "numpart = ", nL )
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
        ged.weights = self.wgt
        ggd.weights = self.wgt

        logL = ged.logLikelihood( poly, gapar )
        lggL = ggd.logLikelihood( poly, ggpar )

        print( "lggL  = %8.3f   logL  = %8.3f" % ( lggL, logL ) )
        assertAAE( logL, lggL )

        dL = ged.partialLogL( poly, gapar, lpfi )
        nL = ged.numPartialLogL( poly, gapar, lpfi )
        dG = ggd.partialLogL( poly, ggpar, ggfi)
        nG = ggd.numPartialLogL( poly, ggpar, ggfi )

        print( "partial = ", dL )
        print( "partial = ", dG )
        print( "numpart = ", nL )
        print( "numpart = ", nG )
        assertAAE( dG[:2], dL[:2], 5 )
        assertAAE( dG[2]*ff, dL[2], 5 )
        assertAAE( dG, nG, 5 )
        assertAAE( dL, nL, 5 )

        for i in range( 11 ) :
            param = numpy.asarray( [i-5,5,scale,power], dtype=float )
            print( param, "  :  ", end="" )
            for k in range( 9 ):
                print( " %8.3f" % ggd.logLikelihood( poly, param ), end="" )
                param[1] += 1
            print( "" )

    def testPoissonErrorDistribution( self ):
        print( "====== Test Poisson Error Distribution ======================" )
        poly = PolynomialModel( 1 )
        param = numpy.asarray( [12, 10], dtype=float )
        data = numpy.asarray( self.data + 12, dtype=int )
        print( "Data : ", data )
        ped = PoissonErrorDistribution( self.x, data )
        self.assertFalse( ped.acceptWeight() )

        logL = ped.logLikelihood( poly, param )
        print( "logL  = %8.3f"%( logL ) )
        scale = 0.1
        logL = ped.logLikelihood( poly, param )
        mok = poly.result( self.x, param )
        altL = numpy.sum( data * numpy.log( mok ) - mok - logFactorial( data ) )

        print( "logL  = %8.3f  %8.3f" % ( logL, altL ) )
        assertAAE( logL, altL )

        logL = ped.logLikelihood( poly, [-5, 0] )
        print( "logL  = %8.3f"%( logL ) )
        self.assertTrue( math.isinf( logL ) )

        scale = 1.0
        fitIndex = [0,1]
        dL = ped.partialLogL( poly, param, fitIndex )
        nL = ped.numPartialLogL( poly, param, fitIndex )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        scale = 0.5
        dL = ped.partialLogL( poly, param, fitIndex )
        nL = ped.numPartialLogL( poly, param, fitIndex )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        scale = 1.0
        for i in range( 10 ) :
            param = numpy.asarray( [8+i,4], dtype=float )
            print( param, "  :  ", end="" )
            for k in range( 9 ):
                print( " %8.3f" % ped.logLikelihood( poly, param ), end="" )
                param[1] += 1
            print( "" )


    def testCauchyErrorDistribution( self ):
        print( "\n   Test Cauchy Error Distribution\n" )
        poly = PolynomialModel( 1 )
        ced = CauchyErrorDistribution( self.x, self.data )
        self.assertFalse( ced.acceptWeight() )

        param = numpy.asarray( [1,10,1], dtype=float )
        logL = ced.logLikelihood( poly, param )
        print( "logL  =  %8.3f" % ( logL ) )
        scale = 0.1
        s2 = scale * scale
        param[2] = scale
        logL = ced.logLikelihood( poly, param )
        altL = math.log( scale / math.pi ) * len( self.data )
        res = ced.getResiduals( poly, param[:2] )
        altL -= numpy.sum( numpy.log( s2 + res * res ) )
        print( "logL  =  %8.3f  alt %8.3f" % (logL, altL ) )
        assertAAE( logL, altL )

        scale = 1.0
        param[2] = scale
        fi = [0,1,2]
        dL = ced.partialLogL( poly, param, fi )
        nL = ced.numPartialLogL( poly, param, fi )
        print( "params  = ", param, scale )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 2 )

        scale = 0.5
        param[2] = scale
        dL = ced.partialLogL( poly, param, fi )
        nL = ced.numPartialLogL( poly, param, fi )
        print( "params  = ", param, scale )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 2 )


        for i in range( 11 ):
            param = numpy.asarray( [i-5,5,1], dtype=float )
            print( param, ":  ", end="" )
            for k in range( 9 ):
                print( " %8.3f" % ced.logLikelihood( poly, param ), end="" )
                param[1] += 1
            print( "" )


    def testLaplaceErrorDistribution( self ):
        print( "\n   Test Laplace Error Distribution\n" )
        poly = PolynomialModel( 1 )
        ced = LaplaceErrorDistribution( self.x, self.data )
        self.assertTrue( ced.acceptWeight() )

        param = numpy.asarray( [1,10,1], dtype=float )
        logL = ced.logLikelihood( poly, param )
        print( "logL  =  %8.3f" % ( logL ) )
        scale = 0.1
        param[2] = scale
        s2 = scale * scale
        logL = ced.logLikelihood( poly, param )

        altL = - len( self.data ) * math.log( 2.0 * scale )
        res = ced.getResiduals( poly, param[:2] )
        altL -= numpy.sum( numpy.abs( res ) ) / scale
        print( "logL  =  %8.3f  alt %8.3f" % (logL, altL ) )
        assertAAE( logL, altL )

        scale = 1.0
        param[2] = scale
        fi = [0,1,2]
        dL = ced.partialLogL( poly, param, fi )
        nL = ced.numPartialLogL( poly, param, fi )
        print( "params  = ", param, scale )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 2 )

        scale = 0.5
        param[2] = scale
        ced.weights = self.wgt
        dL = ced.partialLogL( poly, param, fi )
        nL = ced.numPartialLogL( poly, param, fi )
        print( "params  = ", param, scale )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 2 )

        logL = ced.logLikelihood( poly, param )
        cced = ced.copy()
        logLc = cced.logLikelihood( poly, param )
        print( cced )
        print( "logL  =  %8.3f  copy %8.3f" % (logL, logLc ) )
        dLc = cced.partialLogL( poly, param, fi )
        print( "params  = ", param, scale )
        print( "partial = ", dL )
        assertAAE( logL, logLc, 6 )
        assertAAE( dL, dLc, 6 )

        for i in range( 11 ):
            param = numpy.asarray( [i-5,5,1], dtype=float )
            print( param, ":  ", end="" )
            for k in range( 9 ):
                print( " %8.3f" % ced.logLikelihood( poly, param ), end="" )
                param[1] += 1
            print( "" )


    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( ErrorDistributionTest.__class__ )


