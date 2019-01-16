## run as : python3 -m unittest TestProblem

from __future__ import print_function

import numpy as numpy
from numpy.testing import assert_array_almost_equal as assertAAE
import unittest
from astropy import units
import math
import sys
import matplotlib.pyplot as plt

from BayesicFitting import *
from BayesicFitting import formatter as fmt
from BayesicFitting import fma


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

class TestProblem( unittest.TestCase ):
    """
    Test harness for Problem classes.

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
        super( ).__init__( name )
        numpy.set_printoptions(formatter={'float': '{: 0.3f}'.format})

    def plot3( self ) :
        self.test3( plot=True )


    def test1( self, plot=False ) :
        print( "====test1 (Classic)Problem============================" )
        nn = 11
        x = numpy.linspace( -1, 1, nn, dtype=float )
        ym = self.x

        model = PolynomialModel( 0 )
        model.parameters = 0.0
        problem = ClassicProblem( model=model, xdata=x, ydata=ym )
#        fitIndex=[0]

        print( problem.shortName() )
        Tools.printclass( problem )

        self.assertTrue( problem.sumweight == problem.ndata )
        self.assertFalse( problem.hasWeights() )
        r = problem.residuals( [0.0] )
        print( fma(r) )
        print( fmt(numpy.sum( r )), fmt(numpy.sum( numpy.abs( r ) )) )
        self.assertAlmostEqual( numpy.sum( r ), 0 )
        self.assertAlmostEqual( numpy.sum( numpy.abs( r ) ), 6 )

        r, s = problem.weightedResiduals( [0.0], extra=True )
        self.assertAlmostEqual( numpy.sum( r ), 0 )
        self.assertAlmostEqual( numpy.sum( numpy.abs( r ) ), 6 )
        self.assertTrue( s[0] == s[4] == -1 )
        self.assertTrue( s[6] == s[10] == 1 )


        r,s = problem.weightedResSq( [0.0], extra=True )
        self.assertAlmostEqual( numpy.sum( r ), 4.4 )
        self.assertAlmostEqual( numpy.sum( numpy.abs( r ) ), 4.4 )
        self.assertTrue( s[0] + s[4] == -1.2 )
        self.assertTrue( s[6] + s[10] == 1.2 )

        problem.weights = self.wgt

        self.assertTrue( problem.sumweight == 16 )
        self.assertTrue( problem.hasWeights() )

        r = problem.residuals( [0.0] )
        self.assertAlmostEqual( numpy.sum( r ), 0 )
        self.assertAlmostEqual( numpy.sum( numpy.abs( r ) ), 6.0 )


        r, s = problem.weightedResiduals( [0.0], extra=True )
        self.assertTrue( numpy.sum( r ) == 0.0 )
        self.assertTrue( numpy.sum( numpy.abs( r ) ) == 8.4 )

        self.assertTrue( s[0] == s[4] == -1 )
        self.assertTrue( s[1] == s[3] == -2 )
        self.assertTrue( s[6] == s[10] == 1 )
        self.assertTrue( s[7] == s[9] == 2 )

        r,s = problem.weightedResSq( [0.0], extra=True )
        self.assertTrue( numpy.sum( r ) == 6.0 )
        self.assertTrue( s[0] + s[4] == -1.2 )
        self.assertTrue( s[6] + s[10] == 1.2 )

        engs = problem.myEngines()
        self.assertTrue( len( engs ) == 1 )
        self.assertTrue( engs[0] == "galilean" )

        self.assertTrue( problem.myStartEngine() == "start" )
        self.assertTrue( problem.myDistribution() == "gauss" )

    def test2( self, plot=False ) :
        print( "====test2 ErrorsInXandYProblem============================" )
        nn = 4
        x = numpy.asarray( [0,2,8,10],dtype=float )
        y = numpy.asarray( [2,0,10,8],dtype=float )


        model = PolynomialModel( 1 )
        par = [0.0, 1.0] + [1.0, 1.0, 9.0, 9.0]
        npar = len( par )

        problem = ErrorsInXandYProblem( model=model, xdata=x, ydata=y )

        print( problem.shortName() )
        Tools.printclass( problem )

        self.assertTrue( problem.sumweight == problem.ndata )
        self.assertFalse( problem.hasWeights() )
        md = problem.result( par )
        print( "mock  ", fma( md ) )
        r = problem.residuals( par, mockdata=md )
        print( "res   ", fma(r) )
        print( "sum   ", fmt(numpy.sum( r )), fmt(numpy.sum( numpy.abs( r ) )) )
        sqrt2 = math.sqrt( 2 )
        self.assertAlmostEqual( numpy.sum( r ), 4*sqrt2 )
        self.assertAlmostEqual( numpy.sum( numpy.abs( r ) ), 4*sqrt2 )

        r, s = problem.weightedResiduals( par, extra=True )
        print( "res   ", fma( r ) )
        print( "      ", fma( s ) )
        self.assertAlmostEqual( numpy.sum( r ), 4*sqrt2 )
        self.assertAlmostEqual( numpy.sum( s ), 0 )
        for k in [1,3,4,6] :
            self.assertAlmostEqual( s[k], -sqrt2/2 )
        for k in [0,2,5,7] :
            self.assertAlmostEqual( s[k],  sqrt2/2 )


        r,s = problem.weightedResSq( par, extra=True )
        print( "res2  ", fma( r ) )
        print( "      ", fma( s ) )
        self.assertAlmostEqual( numpy.sum( r ), 8.0 )
        self.assertAlmostEqual( numpy.sum( s ), 0.0 )

        self.assertAlmostEqual( s[0] + s[2] + s[5] + s[7],  4 )
        self.assertAlmostEqual( s[1] + s[3] + s[4] + s[6], -4 )

        problem.weights = numpy.asarray( [1,1,2,2], dtype=float )

        self.assertTrue( problem.sumweight == 6 )
        self.assertTrue( problem.hasWeights() )

        r,s = problem.weightedResSq( par, extra=True )
        print( "res2w ", fma( r ) )
        print( "      ", fma( s ) )
        self.assertTrue( numpy.sum( r ) == 12.0 )
        self.assertTrue( numpy.sum( s ) == 0 )

        engs = problem.myEngines()
        self.assertTrue( len( engs ) == 2 )
        self.assertTrue( engs[0] == "galilean" )
        self.assertTrue( engs[1] == "gibbs" )

        self.assertTrue( problem.myStartEngine() == "start" )
        self.assertTrue( problem.myDistribution() == "gauss" )

        print( "=======   Try Gauss Error Distribution  ==================" )

        ## reset the weights
#        problem.weights = None

        ged = GaussErrorDistribution( )
        param = numpy.append( par, [1.0] )

        fitIndex = [k for k in range( npar )] + [-1]

        lLdata = ged.logLdata( problem, param )
        print( "ldata ", fma( lLdata ) )

        logL0 = numpy.sum( lLdata )

        logL = ged.logLikelihood( problem, param )
        altL = ged.logLikelihood_alt( problem, param )
        print( "logL  = %8.3f  %8.3f  %8.3f" % ( logL, logL0, altL ) )
        assertAAE( logL, altL )
        assertAAE( logL, logL0 )

        scale = 0.1
        param[-1] = scale
        logL = ged.logLikelihood( problem, param )
        altL = ged.logLikelihood_alt( problem, param )
        print( "logL  = %8.3f  %8.3f" % ( logL, altL ) )
        assertAAE( logL, altL )

        scale = 1.0
        param[-1] = scale
        fitIndex = numpy.asarray( [0,1,-1] )
        dL = ged.partialLogL( problem, param, fitIndex )
        nL = ged.numPartialLogL( problem, param, fitIndex )
        print( "partial = ", dL )
        print( "partalt = ", ged.partialLogL_alt( problem, param, fitIndex ) )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        print( "Using scale = 0.5 and weights." )
        scale = 0.5
        param[-1] = scale
        problem.weights = numpy.asarray( [1,1,2,2], dtype=float )

        logL = ged.logLikelihood( problem, param )

        lLdata = ged.logLdata( problem, param )
        logL0 = numpy.sum( lLdata )
        print( "logL = %8.3f  %8.3f" % ( logL, logL0 ) )
        assertAAE( logL, logL0 )

        dL = ged.partialLogL( problem, param, fitIndex )
        print( "partalt = ", ged.partialLogL_alt( problem, param, fitIndex ) )
        nL = ged.numPartialLogL( problem, param, fitIndex )
        print( "partial = ", dL )
        print( "numpart = ", nL )
        assertAAE( dL, nL, 5 )

        scale = 1.0
        for i in range( 11 ) :
            param = numpy.asarray( [0.2*i-1,0,1,1,9,9,1], dtype=float )
            print( param, "  :  ", end="" )
            for k in range( 9 ):
                print( " %8.3f" % ged.logLikelihood( problem, param ), end="" )
                param[1] += 0.2
            print( "" )

    def test3( self, plot=False ) :
        print( "====test3 ErrorsInXandYProblem============================" )

        x = numpy.array( [0,1,2,3,4,5,5,6,7,8,9,10], dtype=float )
        y = numpy.array( [1,0,3,2,5,4,6,5,8,7,10,9], dtype=float )

#        x = numpy.append( x, x + 1 )
#        y = numpy.append( y, y + 1 )

#        x = numpy.append( x, x - 0.5 )
#        y = numpy.append( y, y - 0.5 )

        pm = PolynomialModel( 1 )
        ftr = Fitter( x, pm )
        par = ftr.fit( y )
        yfit = pm( x )
        plt.figure( "x-opt", figsize=(6,6) )
        #plt.plot( x, yfit, 'r-' )


        mdl = PolynomialModel( 1 )
        mdl.setLimits( -10, 10 )

        ns = NestedSampler( x, mdl, y, problem="errors", verbose=2, limits=[0.1,1] )
        ns.setEngines( ["galilean", "gibbs"] )
        ns.problem.prior = UniformPrior( limits=[-2.0,2.0] )
        #ns.minimumIterations = 1000

        Tools.printclass( ns.problem )
        Tools.printclass( ns.distribution )
        ns.verbose = 2
        ns.end = 4.0

        # find the parameters
        #keep = {0:0, 1:1, 3:0.5, 4:9.5, 5:9.5}
        evid = ns.sample( )

        print( "Parameters :", fmt( ns.parameters, max=10 ) )
        print( "StDevs     :", fmt( ns.stdevs, max=10 ) )
        xopt = ns.samples.nuisance
        print( "xdata      :", fmt( x, max=10 ))
        print( "Nuisance   :", fmt( xopt, max=10 ) )
        print( "StdevNuis  :", fmt( ns.samples.stdevNuis, max=10 ))
        print( "Scale      :", fmt( ns.scale ) )


        print( "ftrpars    :", fmt( par, max=10 ) )
        mlap = ns.samples[-1].allpars
        print( "ML pars    :", fmt( mlap[:2], max=10 ) )
        print( "ML Nuis    :", fmt( mlap[2:-1], max=10 ) )
        print( "ML scale   :", fmt( mlap[-1], max=10 ) )

        assertAAE( mlap[:2], [0,1], 2 )
        assertAAE( mlap[2:-1], ( x + y ) / 2, 1 )



        print( "ML logL    :", fmt( ns.samples[-1].logL ) )

        print( "ML logL    :", fmt( ns.distribution.logLikelihood( ns.problem, mlap ) ) )
        mlap[:2] = [0.0,1.0]
        print( "ML allp    :", fmt( mlap, max=10 ) )
        print( "ML logL    :", fmt( ns.distribution.logLikelihood( ns.problem, mlap ) ) )

        mlap[2:-1] = ( x + y ) / 2
        print( "ML allp    :", fmt( mlap, max=10 ) )
        print( "ML logL    :", fmt( ns.distribution.logLikelihood( ns.problem, mlap ) ) )

        nd = len( x )

        if not plot :
            return

        yopt = mdl.result( xopt, ns.parameters )
        plt.plot( xopt, yopt, 'k-' )
        for k in range( 0, nd, 1 ):
            plt.plot( [x[k],xopt[k]], [y[k],yopt[k]], 'g-')

        plt.show()


    def test4( self, plot=False ) :
        print( "====test4 ErrorsInXandYProblem============================" )
        x = numpy.array( [0,1,9,10], dtype=float )
        y = numpy.array( [1,0,10,9], dtype=float )

        mdl = PolynomialModel( 1 )
        mdl.setLimits( -10, 10 )

        ns = NestedSampler( x, mdl, y, problem="errors", verbose=2, limits=[0.1,1] )
        ns.setEngines( ["galilean", "gibbs"] )
        ns.problem.prior = UniformPrior( limits=[-2.0,2.0] )

        Tools.printclass( ns.problem )
        Tools.printclass( ns.distribution )
        ns.verbose = 2
        #ns.end = 4.0

        # find the parameters
        keep = {0:0, 1:1, 3:0.5, 4:9.5, 5:9.5}
        evid = ns.sample( keep=keep )

        if not plot :
            return

        xopt = ns.samples.nuisance
        yopt = mdl.result( xopt, ns.parameters )
        plt.plot( xopt, yopt, 'k-' )
        for k in range( 4 ):
            plt.plot( [x[k],xopt[k]], [y[k],yopt[k]], 'g-')
        plt.show()

    def test5( self, plot=False ) :
        print( "====test4 ErrorsInXandYProblem============================" )
        x = numpy.array( [0,1,2,3], dtype=float )
        y = numpy.array( [[1,0],[0,1],[-1,0],[0,-1]], dtype=float )
        w = numpy.array( [0.9,1.0,1.1,1.2], dtype=float )

        mdl = StellarOrbitModel( )
        p = [ 0.0, 1.1, 4.0, 0.01, 0.0, 0.0, 0.0]

        problem = MultipleOutputProblem( model=mdl, xdata=x, ydata=y, weights=w )

        print( problem.weights )

        ym = problem.result( p )

        print( y.flatten() )
        print( ym.flatten() )

        res = problem.residuals( p )

        print( res.flatten() )

        dmdx = problem.derivative( p )
        print( dmdx )
        sh = dmdx.shape
        self.assertTrue( sh[0] == 4 and sh[1] == 2 )

        parts = mdl.partial( x, p )
        print( parts[0] )
        sh = parts[1].shape
        self.assertTrue( sh[0] == 4 and sh[1] == 7 )

        partial = problem.partial( p )
        print( partial )
        sh = partial.shape
        self.assertTrue( sh[0] == 8 and sh[1] == 7 )

        a0 = numpy.arange( 6 ).reshape( 3, 2 )
        a1 = numpy.arange( 6 ).reshape( 3, 2 ) + 10
        a2 = numpy.arange( 6 ).reshape( 3, 2 ) + 20

        aa = numpy.append( a0, a1, 1 )
        aa = numpy.append( aa, a2, 1 )

        print( a0 )
        print( aa )
        print( aa.reshape( -1, 2 ) )


    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( ErrorDistributionTest.__class__ )


