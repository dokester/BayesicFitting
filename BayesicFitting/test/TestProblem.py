## run as : python3 -m unittest TestProblem

from __future__ import print_function

import numpy as numpy
import os
from numpy.testing import assert_array_almost_equal as assertAAE
import unittest
import math
import matplotlib.pyplot as plt

from BayesicFitting import *
from BayesicFitting import formatter as fmt
from BayesicFitting import fma

__author__ = "Do Kester"
__year__ = 2021
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

class Test( unittest.TestCase ):
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
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

    def test1( self ) :
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
        self.assertFalse( problem.hasAccuracy )
        r = problem.residuals( [0.0] )
        print( fma(r) )
        print( fmt(numpy.sum( r )), fmt(numpy.sum( numpy.abs( r ) )) )
        self.assertAlmostEqual( numpy.sum( r ), 0 )
        self.assertAlmostEqual( numpy.sum( numpy.abs( r ) ), 6 )

#        r, s = problem.weightedResiduals( [0.0], extra=True )
#        self.assertAlmostEqual( numpy.sum( r ), 0 )
#        self.assertAlmostEqual( numpy.sum( numpy.abs( r ) ), 6 )
#        self.assertTrue( s[0] == s[4] == -1 )
#        self.assertTrue( s[6] == s[10] == 1 )


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


#        r, s = problem.weightedResiduals( [0.0], extra=True )
#        self.assertTrue( numpy.sum( r ) == 0.0 )
#        self.assertTrue( numpy.sum( numpy.abs( r ) ) == 8.4 )

#        self.assertTrue( s[0] == s[4] == -1 )
#        self.assertTrue( s[1] == s[3] == -2 )
#        self.assertTrue( s[6] == s[10] == 1 )
#        self.assertTrue( s[7] == s[9] == 2 )

        r,s = problem.weightedResSq( [0.0], extra=True )
        self.assertTrue( numpy.sum( r ) == 6.0 )
        self.assertTrue( s[0] + s[4] == -1.2 )
        self.assertTrue( s[6] + s[10] == 1.2 )

        engs = problem.myEngines()
        self.assertTrue( len( engs ) == 2 )
        self.assertTrue( engs[0] == "galilean" )
        self.assertTrue( engs[1] == "chord" )

        self.assertTrue( problem.myStartEngine() == "start" )
        self.assertTrue( problem.myDistribution() == "gauss" )

    def test2a( self ) :
        print( "====test2a ErrorsInXandYProblem============================" )
        nn = 4
        x = numpy.asarray( [0,2,8,10],dtype=float )
        y = numpy.asarray( [2,0,10,8],dtype=float )

        model = PolynomialModel( 1 )
        par = [0.0, 1.0] + [1.0, 1.0, 9.0, 9.0]

        problem = ErrorsInXandYProblem( model=model, xdata=x, ydata=y )
        Tools.printclass( problem )

        self.assertFalse( problem.hasAccuracy )
        self.assertTrue( problem.determinant == 0 )
        self.assertTrue( problem.varyy == 0 )
        self.assertTrue( problem.varxx == 0 )
        self.assertTrue( problem.varxy == 0 )
        self.assertTrue( problem.sumweight == 4 )

        self.stdtest( problem, par )

    def test2b( self ) :
        print( "====test2b ErrorsInXandYProblem============================" )
        nn = 4
        x = numpy.asarray( [0,2,8,10],dtype=float )
        y = numpy.asarray( [2,0,10,8],dtype=float )
        model = PolynomialModel( 1 )
        par = [0.0, 1.0] + [1.0, 1.0, 9.0, 9.0]

        wgt = [2,1,1,2]
        problem = ErrorsInXandYProblem( model=model, xdata=x, ydata=y, weights=wgt )
        Tools.printclass( problem )

        self.assertFalse( problem.hasAccuracy )
        self.assertTrue( problem.determinant == 0 )
        self.assertTrue( problem.varyy == 0 )
        self.assertTrue( problem.varxx == 0 )
        self.assertTrue( problem.varxy == 0 )
        self.assertTrue( problem.sumweight == 6 )

        self.stdtest( problem, par )

    def test2c( self ) :
        print( "====test2c ErrorsInXandYProblem============================" )
        nn = 4
        x = numpy.asarray( [0,2,8,10],dtype=float )
        y = numpy.asarray( [2,0,10,8],dtype=float )
        model = PolynomialModel( 1 )
        par = [0.0, 1.0] + [1.0, 1.0, 9.0, 9.0]

        problem = ErrorsInXandYProblem( model=model, xdata=x, ydata=y, covar=[[1,0],[0,2]] )
        Tools.printclass( problem )

        self.assertTrue( problem.hasAccuracy )
        self.assertTrue( problem.determinant == 2 )
        self.assertTrue( problem.varyy == 1 )
        self.assertTrue( problem.varxx == 2 )
        self.assertTrue( problem.varxy == 0 )
        self.assertTrue( problem.sumweight == 4 )

        self.stdtest( problem, par, plot=self.doplot )

    def test2d( self ) :
        print( "====test2d ErrorsInXandYProblem============================" )
        nn = 4
        x = numpy.asarray( [0,2,8,10],dtype=float )
        y = numpy.asarray( [2,0,10,8],dtype=float )
        model = PolynomialModel( 1 )
        par = [0.0, 1.0] + [1.0, 1.0, 8.0, 8.0]

        acc = numpy.array( [1.0, 1.0, -0.5] )
        cov = numpy.array( [[1.0,-0.5],[-0.5,1]], dtype=float )

        problem = ErrorsInXandYProblem( model=model, xdata=x, ydata=y, accuracy=acc )
        Tools.printclass( problem )

        self.assertTrue( problem.hasAccuracy )
        self.assertTrue( problem.determinant == 0.75 )
        self.assertTrue( problem.varyy == 1 )
        self.assertTrue( problem.varxx == 1 )
        self.assertTrue( problem.varxy == -0.5 )
        self.assertTrue( problem.sumweight == 4 )

        self.stdtest( problem, par, covar=cov, plot=self.doplot )

    def test2e( self ) :
        print( "====test2e ErrorsInXandYProblem============================" )
        nn = 4
        x = numpy.asarray( [0,2,8,10],dtype=float )
        y = numpy.asarray( [2,0,10,8],dtype=float )
        model = PolynomialModel( 1 )
        par = [0.0, 1.0] + [1.0, 1.0, 9.0, 9.0]

        clst = [[[0.8,0.4],[0.4,1]], [[0.3,-0.4],[-0.4,1]], [[1.8,0.7],[0.7,1]], [[1.2,-0.1],[-0.1,1]]]
        cov = numpy.array( clst, dtype=float )
        print( cov )

        problem = ErrorsInXandYProblem( model=model, xdata=x, ydata=y, covar=cov )
        Tools.printclass( problem )

        self.assertTrue( problem.hasAccuracy )
        assertAAE( problem.determinant, [0.64, 0.14, 1.31, 1.19], 3  )
        assertAAE( problem.varyy, [0.8, 0.3, 1.8, 1.2] )
        assertAAE( problem.varxx, [1.0, 1.0, 1.0, 1.0] )
        assertAAE( problem.varxy, [0.4,-0.4, 0.7,-0.1] )
        self.assertTrue( problem.sumweight == 4 )

        self.stdtest( problem, par, covar=cov, plot=self.doplot )

    def test2f( self ) :
        print( "====test2e ErrorsInXandYProblem============================" )
        nn = 4
        x = numpy.asarray( [0,2,8,10],dtype=float )
        y = numpy.asarray( [2,0,10,8],dtype=float )
        model = PolynomialModel( 1 )
        par = [0.0, 1.0] + [1.0, 1.0, 9.0, 9.0]

        alst = [[1, 1, 0.4], [2,1,-0.1], [1, 2, 0], [3, 3, -0.9]]
        acc = numpy.array( alst, dtype=float )
        print( acc )

        problem = ErrorsInXandYProblem( model=model, xdata=x, ydata=y, accuracy=acc )
        Tools.printclass( problem )

        self.assertTrue( problem.hasAccuracy )
        assertAAE( problem.determinant, [0.84, 3.96, 4.0, 15.39], 3  )
        assertAAE( problem.varyy, [1.0, 4.0, 1.0, 9.0] )
        assertAAE( problem.varxx, [1.0, 1.0, 4.0, 9.0] )
        assertAAE( problem.varxy, [0.4,-0.2, 0.0,-8.1] )
        self.assertTrue( problem.sumweight == 4 )

        self.stdtest( problem, par, plot=self.doplot )

    def xxxtest0b( self ) :
        print( "====test0b ErrorsInXandYProblem============================" )

        numpy.random.seed( 123456 )
        xx = numpy.random.randn( 100 ) * 0.6
        yy = numpy.random.randn( 100 ) * 0.4
        zz = numpy.random.randn( 100 ) * 0.5
        cov = numpy.cov( xx - zz, - ( yy - zz ) )
        val, vec = numpy.linalg.eig( cov )
        print( cov )
        print( val )
        print( vec )

        c = vec[0,0]
        s = vec[1,0]
        a = val[0]
        b = val[1]
        print( c )
        print( s )
        
        c2 = c * c
        s2 = s * s
        a2 = a * a
        b2 = b * b
        NP = 21
        map = numpy.zeros( (NP, NP), dtype=float )

        for k in range( NP ) :
            x = 0.4 * ( k - 10 )
            x2 = x * x
            for i in range( NP ) :
                y = 0.4 * ( i - 10 )
                y2 = y * y
                r2 = ( a2 * x2 * s2 + b2 * x2 * c2 + 
                       2 * ( b2 - a2 ) * c * s * x * y +
                       a2 * y2 * c2 + b2 * y2 * s2 ) / ( a2 * b2 )
                map[i,k] = r2

        plt.figure( 2, figsize=(6,6) )
        plt.plot( xx - zz, zz - yy, 'k.' )

        ay = numpy.linspace( -4, 4, NP )
        ax = numpy.linspace( -4, 4, NP )

        cnts = [0.5, 1.0, 2.0, 4.0, 10, 20]

#        print( map )

        plt.contour( ax, ay, map, cnts )

        plt.axis( 'equal' )

        plt.show()


    def stdtest( self, problem, par, covar=None, plot=False, dosample=False ) :
        npar = len( par )

        problem.model.setLimits( -4, 4 )
        problem.prior = GaussPrior( scale=1 )

        print( problem.shortName() )
        print( "xdat   ", fmt( problem.xdata ) )
        print( "ydat   ", fmt( problem.ydata ) )

        if not problem.hasWeights :
            self.assertTrue( problem.sumweight == problem.ndata )

        md = problem.result( par )
        print( "mock  ", fma( md ) )
        r = problem.residuals( par, mockdata=md )
        print( "res   ", fma(r) )
        print( "sum   ", fmt(numpy.sum( r )), fmt(numpy.sum( numpy.abs( r ) )) )
        sqrt2 = math.sqrt( 2 )


        allpar = par + [1.0]
        rs = problem.weightedResSq( allpar, extra=True )
        print( "res2  ", fma( rs[0] ) )
        print( "y x   ", fma( rs[1] ) )
        print( "xr2   ", fma( rs[2] ) )

        wgts = problem.weights
        print( "wgt   ", fmt( wgts ) )
        swgt = problem.sumweight
        print( "swgt  ", fmt( swgt ) )

        if dosample :
            engs = ["gibbs", "chord"]
            ns = NestedSampler( problem=problem, engines=engs )
            ns.distribution.setLimits( [0.1, 10] )
            ns.verbose = 2

            evi = ns.sample()

            paropt = ns.parameters
            print( "Prob npars :", ns.walkers[0].problem.npars )
            print( "Parameters :", fmt( ns.parameters, max=10 ) )
            print( "StDevs     :", fmt( ns.stdevs, max=10 ) )
            xopt = ns.samples.nuisance
            print( "xdata      :", fmt( problem.xdata, max=10 ))
            print( "Nuisance   :", fmt( xopt, max=10 ) )
            print( "StdevNuis  :", fmt( ns.samples.stdevNuis, max=10 ))
            print( "Scale      :", fmt( ns.scale ) )
        

        if not plot : return

        x = problem.xdata
        y = problem.ydata
        nx = len( x )
        plt.figure( 1, figsize=(6,6) )
        plt.plot( x, y, 'k.' )
        plt.plot( x, problem.model.result( x, [0,1] ), 'k-' )

        if dosample :
            plt.plot( xopt, problem.model.result( xopt, paropt ), 'g-' )

        if covar is not None :
            val, vec = numpy.linalg.eig( covar )
            tt = numpy.linspace( 0, 2 * math.pi, 91 )
            if vec.ndim == 2 :
                xx = numpy.append( val[0] * numpy.cos( tt ), val[1] * numpy.sin( tt ) ).reshape( 2, -1 ).T
                xx = numpy.inner( xx, vec )
            for k in range( nx ) :
                if vec.ndim == 3 :
                    xx = numpy.append( val[k,0] * numpy.cos( tt ), val[k,1] * numpy.sin( tt ) ).reshape( 2, -1 ).T
                    xx = numpy.inner( xx, vec[k,:,:] )
                plt.plot( x[k] + xx[:,0], y[k] + xx[:,1], 'r-' ) 

        plt.axis( 'equal' )
        plt.show()


    def test2( self ) :
        print( "====test2 ErrorsInXandYProblem============================" )
        nn = 4
        x = numpy.asarray( [0,2,8,10],dtype=float )
        y = numpy.asarray( [2,0,10,8],dtype=float )

        model = PolynomialModel( 1 )
        par = [0.0, 1.0] + [1.0, 1.0, 9.0, 9.0]
        npar = len( par )

        problem = ErrorsInXandYProblem( model=model, xdata=x, ydata=y )

#        problem.weights = numpy.asarray( [1,1,2,2], dtype=float )

        yres, xres = problem.getXYresiduals( par )
        print( "yres  ", fma( yres ) )
        print( "xres  ", fma( yres ) )
        print( "res2  ", fma( xres*xres + yres*yres ) )

        print( fmt( problem.varyy ), fmt( problem.varxy ), fmt( problem.varxx ), fmt( problem.determinant ) )

        allpars = par + [1.0]
        rs = problem.weightedResSq( allpars, extra=True )
        print( "res2w ", fma( rs[0] ) )
        print( "      ", fma( rs[1] ) )
        print( "      ", fma( rs[2] ) )
        self.assertFalse( problem.hasAccuracy )
#        self.assertTrue( numpy.sum( rs[0] ) == 12.0 )
        self.assertTrue( numpy.sum( rs[1] ) == 0 )
#        self.assertTrue( problem.sumweight == 6 )
#        self.assertTrue( problem.hasWeights() )

        engs = problem.myEngines()
        self.assertTrue( len( engs ) == 3 )
        self.assertTrue( engs[0] == "galilean" )
        self.assertTrue( engs[1] == "gibbs" )
        self.assertTrue( engs[2] == "chord" )

        self.assertTrue( problem.myStartEngine() == "start" )
        self.assertTrue( problem.myDistribution() == "gauss2d" )

        print( "=======   Try Gauss Error Distribution  ==================" )

        ## reset the weights
#        problem.weights = None

        ged = Gauss2dErrorDistribution( )
#        ged.deltaP = -0.01
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

    def test3( self ) :
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
        if self.doplot :
            plt.figure( "x-opt", figsize=(6,6) )
            plt.plot( x, y, 'k.' )
            plt.plot( x, yfit, 'r-' )


        mdl = PolynomialModel( 1 )
        mdl.setLimits( -10, 10 )

        ns = NestedSampler( x, mdl, y, problem="errors", limits=[0.1,1] )
        ns.setEngines( ["galilean", "gibbs"] )
        ns.problem.prior = UniformPrior( limits=[-2.0,2.0] )
        #ns.minimumIterations = 1000
        self.assertFalse( ns.problem.hasAccuracy )

#        print( ns.problem.npars )

#        Tools.printclass( ns.problem )
#        Tools.printclass( ns.distribution )
#        ns.end = 4.0
        ns.verbose = 2

        # find the parameters
        #keep = {0:0, 1:1, 3:0.5, 4:9.5, 5:9.5}
        evid = ns.sample( )

        print( "Prob npars :", ns.walkers[0].problem.npars )
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

#        assertAAE( mlap[:2], [0,1], 1 )
#        assertAAE( mlap[2:-1], ( x + y ) / 2, 1 )

        print( "ML logL    :", fmt( ns.samples[-1].logL ) )

        print( "ML logL    :", fmt( ns.distribution.logLikelihood( ns.problem, mlap ) ) )
        mlap[:2] = [0.0,1.0]
        print( "ML allp    :", fmt( mlap, max=10 ) )
        print( "ML logL    :", fmt( ns.distribution.logLikelihood( ns.problem, mlap ) ) )

        mlap[2:-1] = ( x + y ) / 2
        print( "ML allp    :", fmt( mlap, max=10 ) )
        print( "ML logL    :", fmt( ns.distribution.logLikelihood( ns.problem, mlap ) ) )

        nd = len( x )

        if not self.doplot :
            return

        yopt = mdl.result( xopt, ns.parameters )
        plt.plot( xopt, yopt, 'k-' )
        for k in range( 0, nd, 1 ):
            plt.plot( [x[k],xopt[k]], [y[k],yopt[k]], 'g-')

        plt.show()


    def test4( self ) :
        print( "====test4 ErrorsInXandYProblem============================" )
        x = numpy.array( [0,1,9,10], dtype=float )
        y = numpy.array( [1,0,10,9], dtype=float )

        mdl = PolynomialModel( 1 )
        mdl.setLimits( -10, 10 )

        ns = NestedSampler( x, mdl, y, problem="errors", limits=[0.1,1] )
#        ns.setEngines( ["galilean", "gibbs"] )
#        ns.setEngines( ["galilean"] )
        ns.problem.prior = UniformPrior( limits=[-2.0,2.0] )
#        ns.verbose=5
        self.assertFalse( ns.problem.hasAccuracy )

        Tools.printclass( ns.problem )
        Tools.printclass( ns.distribution )

        # find the parameters
        keep = {0:0, 1:1, 3:0.5, 4:9.5, 5:9.5}
        keep = {0:0.5, 1:0.9}
        evid = ns.sample( keep=keep )

        if not self.doplot :
            return

        xopt = ns.samples.nuisance
        yopt = mdl.result( xopt, ns.parameters )

        plt.plot( xopt, yopt, 'k-' )
        for k in range( 4 ):
            plt.plot( [x[k],xopt[k]], [y[k],yopt[k]], 'g-')
        plt.axis( 'equal' )
        plt.show()

    def test5( self ) :
        print( "====test5 MultipleOutputProblem============================" )
        x = numpy.array( [0,1,2,3], dtype=float )
        y = numpy.array( [[1,0],[0,1],[-1,0],[0,-1]], dtype=float )
        w = numpy.array( [0.9,1.0,1.1,1.2], dtype=float )

        mdl = StellarOrbitModel( spherical=False )
        p = [ 0.0, 1.1, 4.0, 0.01, 0.0, 0.0, 0.0]

        problem = MultipleOutputProblem( model=mdl, xdata=x, ydata=y, weights=w )
        self.assertFalse( problem.hasAccuracy )

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

    def XXXtest6( self ) :
        print( "====test6 CategoricalProblem============================" )

        x = numpy.array( [[1,4,2,1,3,2,4,2,3,2,1,2,3]], dtype=float ).transpose()
        y = numpy.array( [1,2,2,3,3,2,1,1,2,3,3,2,2] )

#        w = numpy.array( [0.9,1.0,1.1,1.2], dtype=float )

        mdl = DecisionTreeModel( ndim=1, depth=2, kdim=[0,0,0], split=0.5, itypes=[0] )
        p = [ 0.1, 0.5, 0.6, 0.4,
              0.2, 0.3, 0.7, 0.3,
              0.7, 0.2, 0.1, 0.3]
        print( mdl.fullName() )

        problem = CategoricalProblem( model=mdl, xdata=x, ydata=y )

        print( problem.ncateg, problem.npars, fmt( p, max=None ) )
        print( fmt( problem.ydata, max=None ) )
        print( fmt( x, max=None ) )
        print( fmt( mdl.sortXdata( x ), max=None ) )

        lst = [k for k in range( len( p ) )]
        ym = problem.result( p )
        yl = problem.result( lst )
        dy = problem.partial( p )

        print( fmt( ym, max=None ) )
        print( fmt( yl, max=None ) )
        print( fmt( dy, max=None ) )

        res = problem.residuals( p )

        print( fmt( res, max=None ) )

#        dmdx = problem.derivative( p )
#        print( dmdx )

    def test7( self ) :
        print( "====test7 EvidenceProblem============================" )
        nn = 11
        x = numpy.linspace( -1, 1, nn, dtype=float )
        ym = self.x

        model = PolynomialModel( 0 )
        self.assertRaises( ValueError, EvidenceProblem, model=model, xdata=x, ydata=ym )

        model = SplinesDynamicModel( knots=[-1.0, 1.1] )

        problem = EvidenceProblem( model=model, xdata=x, ydata=ym )

        print( problem.shortName() )
        Tools.printclass( problem )
        self.assertFalse( problem.hasAccuracy )

        engs = problem.myEngines()
        self.assertTrue( len( engs ) == 3 )
        self.assertTrue( engs[0] == "birth" )
        self.assertTrue( engs[1] == "death" )
        self.assertTrue( engs[2] == "struct" )

        self.assertTrue( problem.myStartEngine() == "start" )
        self.assertTrue( problem.myDistribution() == "model" )

    def test7a( self ) :
        print( "====test7a EvidenceProblem============================" )
        nn = 11
        x = numpy.linspace( -1, 1, nn, dtype=float )
        ym = self.data

        model = SplinesDynamicModel( knots=[-1.0, 1.0] )
        model.setLimits( lowLimits=-100, highLimits=100 )

        problem = EvidenceProblem( model=model, xdata=x, ydata=ym )
#        problem = ClassicProblem( model=model, xdata=x, ydata=ym )

        ns = NestedSampler( problem=problem )
        Tools.printclass( problem )
        print( ns.distribution.scale )

        ns.verbose = 2
        logE = ns.sample( plot=self.doplot )

        ns = NestedSampler( problem=problem, limits=[0.1,10.0] )
        ns.verbose = 2
        self.assertFalse( ns.problem.hasAccuracy )

        logE = ns.sample( plot=self.doplot )




    def testcr1( self ) :

        print( "===== cyclic results 1 ================" )

        mdl = PolynomialModel( 1 )
        x = numpy.array( [0,1,9,10], dtype=float )
        y = numpy.array( [1,0,10,9], dtype=float )
        problem = Problem( model=mdl, xdata=x, ydata=y )

        Tools.printclass( mdl )

        r0 = numpy.linspace( -0.7, 1.5, 12 )

        r1 = problem.cyclicCorrection( r0 )

        assertAAE( r0, r1 )

    def testcr2( self ) :

        print( "===== cyclic results 2 ================" )

        mdl = PhaseModel( cyclic=1.0 )

        x = numpy.array( [0,1,9,10], dtype=float )
        y = numpy.array( [1,0,10,9], dtype=float )
        problem = Problem( model=mdl, xdata=x, ydata=y )

        Tools.printclass( problem )

        r0 = numpy.linspace( -0.7, 1.5, 12 )
        print( fmt( r0, max=None ) )
        r1 = problem.cyclicCorrection( r0 )
        print( fmt( r1, max=None ) )

        self.assertTrue( all( numpy.abs( r1 ) <= 0.5 ) )

    def testcr3( self ) :

        print( "===== cyclic results 3 ================" )

        mdl = PhaseModel( cyclic=3.0 )

        x = numpy.array( [0,1,9,10], dtype=float )
        y = numpy.array( [1,0,10,9], dtype=float )
        problem = Problem( model=mdl, xdata=x, ydata=y )

        Tools.printclass( problem )

        r0 = numpy.linspace( -4.2, 4.5, 12 ).reshape(3,4).transpose()
        print( fmt( r0, max=None ) )
        r1 = problem.cyclicCorrection( r0 )
        print( fmt( r1, max=None ) )

        self.assertTrue( all( numpy.abs( r1.flatten() ) <= 1.5 ) )

    def testcr4( self ) :

        print( "===== cyclic results 4 ================" )

        mdl = PhaseModel( cyclic={0:1.0} )

        x = numpy.array( [0,1,9,10], dtype=float )
        y = numpy.array( [1,0,10,9], dtype=float )
        problem = Problem( model=mdl, xdata=x, ydata=y )

        Tools.printclass( problem )

        r0 = numpy.linspace( -0.8, 1.5, 12 ).reshape(2,6).transpose()
        print( fmt( r0, max=None ) )
        r1 = problem.cyclicCorrection( r0 )
        print( fmt( r1, max=None ) )

        assertAAE( r0[:,1], r1[:,1] )
        self.assertTrue( all( numpy.abs( r1[:,0] ) < 0.5 ) )

    def testcr5( self ) :

        print( "===== cyclic results 5 ================" )

        mdl = PhaseModel( cyclic={0: 1.0, 2:1.2} )
        x = numpy.array( [0,1,9,10], dtype=float )
        y = numpy.array( [1,0,10,9], dtype=float )
        problem = Problem( model=mdl, xdata=x, ydata=y )

        r0 = numpy.linspace( -0.8, 1.5, 12 ).reshape(3,4).transpose()
        print( fmt( r0, max=None ) )
        r1 = problem.cyclicCorrection( r0 )
        print( fmt( r1, max=None ) )

        assertAAE( r0[:,1], r1[:,1] )
        self.assertTrue( all( numpy.abs( r1[:,0] ) < 0.5 ) )
        self.assertTrue( all( numpy.abs( r1[:,2] ) < 0.6 ) )




    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( ProblemTest.__class__ )


class PhaseModel( PolynomialModel ) :

    def __init__( self, ndim=1, cyclic=1.0, **kwargs ) :

        super().__init__( degree=0, ndim=ndim, **kwargs )

        Tools.setAttribute( self, "cyclic", cyclic )
