# run with : python3 -m unittest TestEvidence2

import unittest
import os
import numpy
import math
from numpy.testing import assert_array_almost_equal as assertAAE

import matplotlib.pyplot as plt

from BayesicFitting import *
from BayesicFitting import formatter as fmt

from FitPlot import plotFit
from FitPlot import plotErrdis
from FitPlot import plotErrdis2d


class Test( unittest.TestCase  ) :

    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )


    def test1( self ) :
        print( "====test1============================" )
        nn = 100
        x = numpy.zeros( nn, dtype=float )
        ym = 0.2 + 0.5 * x
        nf = 1.0
        nf = 0.1
        numpy.random.seed( 2345 )
        noise = numpy.random.randn( nn )

        y = ym + nf * noise
        limits = [-2,2]

        pm = PolynomialModel( 0 )
        bf = Fitter( x, pm )

        pars = bf.fit( y )
        logz0 = bf.getLogZ( limits=limits )
        logl0 = bf.logLikelihood
        print( "pars  ", fmt( pars ) )
        print( "stdv  ", fmt( bf.stdevs ) )
        print( "logZ  ", fmt( logz0 ), "   logl  ", fmt( logl0 ) )

        errdis = GaussErrorDistribution( )
        problem = ClassicProblem( pm, xdata=x, ydata=y )
        logz1, maxll = plotErrdis( errdis, problem, limits=limits,
                                    max=0, plot=self.doplot )

        print( "logZ  ", fmt( logz1 ) )

        model = PolynomialModel( 0 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )
        ns = NestedSampler( x, model, y, verbose=0 )

        logE = ns.sample()

        par2 = ns.parameters
        stdv = ns.stdevs
        logz2 = ns.logZ
        dlz2 = ns.logZprecision
        print( "pars  ", fmt( par2 ) )
        print( "stdv  ", fmt( stdv ) )
        print( "logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

        self.assertTrue( abs( logz2 - logz0 ) < 2*dlz2 )

        samples = ns.samples
        parevo =samples.getParameterEvolution()
        llevo = samples.getLogLikelihoodEvolution()
        lwevo = samples.getLogWeightEvolution()

        assertAAE( numpy.sum( numpy.exp( lwevo ) ), 1.0 )

        if self.doplot :
            plt.plot( parevo, numpy.exp( llevo ), 'r,' )

            mxl = numpy.exp( numpy.max( llevo ) ) * 1.2
            plt.plot( [pars,pars], [0.0,mxl], 'b-' )
            plt.plot( [par2,par2], [0.0,mxl], 'r-' )
            plt.plot( [par2,par2]+stdv, [0.0,mxl], 'g-' )
            plt.plot( [par2,par2]-stdv, [0.0,mxl], 'g-' )

            plt.show()

    def test1a( self ) :
        print( "====test1a============================" )
        nn = 100
        x = numpy.zeros( nn, dtype=float )
        ym = 0.2 + 0.5 * x
        nf = 1.0
        nf = 0.1
        numpy.random.seed( 2345 )
        noise = numpy.random.randn( nn )

        y = ym + nf * noise
        limits = [-20,20]

        pm = PolynomialModel( 0 )
        bf = Fitter( x, pm )

        pars = bf.fit( y )
        logz0 = bf.getLogZ( limits=limits )
        logl0 = bf.logLikelihood
        print( "pars  ", fmt( pars ) )
        print( "stdv  ", fmt( bf.stdevs ) )
        print( "logZ  ", fmt( logz0 ), "   logl  ", fmt( logl0 ) )

        errdis = GaussErrorDistribution( )
        problem = ClassicProblem( pm, xdata=x, ydata=y )
        logz1, maxll = plotErrdis( errdis, problem, limits=limits,
                                    max=0, plot=self.doplot )

        print( "logZ  ", fmt( logz1 ) )

        model = PolynomialModel( 0 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )
        ns = NestedSampler( x, model, y, verbose=0 )

        logE = ns.sample()

        par2 = ns.parameters
        stdv = ns.stdevs
        logz2 = ns.logZ
        dlz2 = ns.logZprecision
        print( "pars  ", fmt( par2 ) )
        print( "stdv  ", fmt( stdv ) )
        print( "logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

        self.assertTrue( abs( logz2 - logz0 ) < 2*dlz2 )

        samples = ns.samples
        parevo =samples.getParameterEvolution()
        llevo = samples.getLogLikelihoodEvolution()
        lwevo = samples.getLogWeightEvolution()

        assertAAE( numpy.sum( numpy.exp( lwevo ) ), 1.0 )


    def TBDtestGP( self ) :
        gp = GaussPrior( center=0, scale=1 )

        xx = numpy.linspace( -6, 6, 1201, dtype=float )

        s = 0.0
        t = 0.0
        ss = numpy.zeros_like( xx )
        for k,x in enumerate( xx ) :
            ss[k] = gp.result( x )
            s += gp.result( x )
            t += math.exp( gp.logResult( x ) )

        print( s )
        print( t )

        ge = GaussErrorDistribution( scale=1 )
        model = PolynomialModel(0)
        yy = numpy.zeros_like( xx )
        problem = ClassicProblem( xdata=yy, model=model, ydata=xx )
        pars = [0.0, 1.0] 
        le = ge.logLdata( problem, pars )
        ee = numpy.exp( le )
        e = numpy.sum( ee )
        print( e )

        if self.doplot :
            plt.plot( xx, ss, 'k-' )
            plt.plot( xx, ee, 'r-' )
            plt.show()



    def addPrior( self, logL, problem, allpars, logLlow ):
        return logL + self.prior.logResult( allpars[0] ) + math.log( self.limits[1] - self.limits[0] )

    def TBDtest1b( self ) :

        print( "====test1b============================" )
        nn = 1
        x = numpy.zeros( nn, dtype=float )
        ym = x + 0.5

        nf = 0.1
        numpy.random.seed( 2345 )
        noise = numpy.random.randn( nn )
        y = ym + nf * noise

        self.limits = [-10,10]
        pm = PolynomialModel( 0 )

        self.prior = GaussPrior( center=5, scale=3 )
        self.stdtest( x, pm, y, nr=10 )

    def stdtest( self, x, model, y, nr=0 ) :

        print( "+++NS  %s +++++++" % str( self.prior ) )

        model.setPrior( 0, self.prior )

        ns = NestedSampler( x, model, y, verbose=2 )
#        ns.minimumIterations = 500
        logE = ns.sample()

        par1 = ns.parameters
        std1 = ns.stdevs
        logz1 = ns.logZ
        dlz1 = ns.logZprecision
        print( "pars  ", fmt( par1 ) )
        print( "stdv  ", fmt( std1 ) )
        print( "logZ  ", fmt( logz1 ), " +- ", fmt( dlz1 ) )
        for k in range( nr ) :
            ns = NestedSampler( x, model, y, verbose=0, seed=k )
            evi = ns.sample()
            p = ns.parameters
            s = ns.stdevs
            lz = ns.logZ
            er = ns.logZprecision
            print( fmt( k ), fmt( p ), fmt( s ), fmt( lz ), fmt( er ) )

        print( "+++NS  %s alt +++++++" % str( self.prior ) )

        model.setPrior( 0, UniformPrior( limits=self.limits ) )

        ed = GaussErrorDistribution( )
        ed.constrain = self.addPrior
        ns = NestedSampler( x, model, y, verbose=2, distribution=ed )

        logE = ns.sample()

        par2 = ns.parameters
        std2 = ns.stdevs
        logz2 = ns.logZ
        dlz2 = ns.logZprecision
        print( "pars  ", fmt( par2 ) )
        print( "stdv  ", fmt( std2 ) )
        print( "logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )
        for k in range( nr ) :
            ns = NestedSampler( x, model, y, verbose=0, distribution=ed, seed=k )
            evi = ns.sample()
            p = ns.parameters
            s = ns.stdevs
            lz = ns.logZ
            er = ns.logZprecision
            print( fmt( k ), fmt( p ), fmt( s ), fmt( lz ), fmt( er ) )

        self.assertTrue( abs( logz1 - logz2 ) < dlz2 )

    def TBDtest1c( self ) :

        print( "====test1c============================" )
        nn = 100
        x = numpy.zeros( nn, dtype=float )
        ym = x + 0.5

        nf = 0.1
        numpy.random.seed( 2345 )
        noise = numpy.random.randn( nn )
        y = ym + nf * noise

        self.limits = [-100,100]
        pm = PolynomialModel( 0 )

        self.prior = UniformPrior( limits=self.limits )
        self.stdtest( x, pm, y, nr=0 )

    def TBDtest1d( self ) :

        print( "====test1d============================" )
        nn = 100
        x = numpy.zeros( nn, dtype=float )
        ym = x + 0.5

        nf = 0.1
        numpy.random.seed( 2345 )
        noise = numpy.random.randn( nn )
        y = ym + nf * noise

        self.limits = [-100,100]
        pm = PolynomialModel( 0 )

        self.prior = LaplacePrior( center=4.4, scale=2 )
        self.stdtest( x, pm, y, nr=0 )

    def TBDtest1e( self ) :

        print( "====test1e============================" )
        nn = 100
        x = numpy.zeros( nn, dtype=float )
        ym = x + 0.5

        nf = 0.1
        numpy.random.seed( 2345 )
        noise = numpy.random.randn( nn )
        y = ym + nf * noise

        self.limits = [-100,100]
        pm = PolynomialModel( 0 )

        self.prior = CauchyPrior( center=4.4, scale=2 )
        self.stdtest( x, pm, y, nr=0 )


    def test2( self ) :
        print( "====test2============================" )
        nn = 100
        x = numpy.arange( nn, dtype=float ) / 50
        ym = 0.4 + 0.5 * x
        nf = 0.5
        numpy.random.seed( 2345 )
        noise = numpy.random.randn( nn )

        y = ym + nf * noise
        limits = [-1,2]

        pm = PolynomialModel( 1 )
        bf = Fitter( x, pm )

        pars = bf.fit( y )
        logz0 = bf.getLogZ( limits=limits )
        logl0 = bf.logLikelihood
        print( "pars  ", fmt( pars ) )
        print( "logZ  ", fmt( logz0 ), "   logl  ", fmt( logl0 ) )

        errdis = GaussErrorDistribution( )
        problem = ClassicProblem( pm, xdata=x, ydata=y )

        logz1, logl1 = plotErrdis2d( errdis, problem, limits=limits, max=0,
                    plot=self.doplot )

        if self.doplot :
            plt.plot( pars[0], pars[1], 'k.' )

        print( "logZ  ", fmt( logz1 ) )

        model = PolynomialModel( 1 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )
        ns = NestedSampler( x, model, y, verbose=0 )

        logE = ns.sample()

        par2 = ns.parameters
        logz2 = ns.logZ
        dlz2 = ns.logZprecision
        print( "pars  ", fmt( par2 ) )
        print( "stdv  ", fmt( ns.stdevs ) )
        print( "logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

        self.assertTrue( abs( logz2 - logz0 ) < 1.0 )
#        print( logz0 - logz1, logz0 - logz2 )

        samples = ns.samples
        parevo =samples.getParameterEvolution()
        llevo = samples.getLogLikelihoodEvolution()
        lwevo = samples.getLogWeightEvolution()

        assertAAE( numpy.sum( numpy.exp( lwevo ) ), 1.0 )

        if self.doplot :
            plt.show()

    def test2_1( self ) :
        print( "====test2_1============================" )
        nn = 100
        x = numpy.arange( nn, dtype=float ) / 50
        ym = 0.2 + 0.5 * x
        nf = 0.1
        numpy.random.seed( 2345 )
        noise = numpy.random.randn( nn )

        y = ym + nf * noise
        limits = [-1,2]

        pm = PolynomialModel( 1 )
        bf = Fitter( x, pm )

        pars = bf.fit( y )
        logz0 = bf.getLogZ( limits=limits )
        logl0 = bf.logLikelihood
        print( "pars  ", fmt( pars ) )
        print( "stdv  ", fmt( bf.stdevs ) )
        print( "logZ  ", fmt( logz0 ), "   logL  ", fmt( logl0 ) )

        errdis = GaussErrorDistribution( )
        problem = ClassicProblem( pm, xdata=x, ydata=y )

        logz1, logl1 = plotErrdis2d( errdis, problem, limits=limits, max=0,
                    plot=self.doplot )
        if self.doplot :
            plt.plot( pars[0], pars[1], 'k.' )

        print( "logZ  ", fmt( logz1 ), "   logL  ", fmt( logl1 ) )

        model = PolynomialModel( 1 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )
        ns = NestedSampler( x, model, y, verbose=0 )

        logE = ns.sample()

        par2 = ns.parameters
        logz2 = ns.logZ
        dlz2 = ns.logZprecision
        print( "pars  ", fmt( par2 ) )
        print( "stdv  ", fmt( ns.stdevs ) )
        print( "logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

        self.assertTrue( abs( logz2 - logz0 ) < 1.0 )
#        print( logz0 - logz1, logz0 - logz2 )

        samples = ns.samples
        parevo =samples.getParameterEvolution()
        llevo = samples.getLogLikelihoodEvolution()
        lwevo = samples.getLogWeightEvolution()

        assertAAE( numpy.sum( numpy.exp( lwevo ) ), 1.0 )

        if self.doplot :
            plt.show()

    def test3( self ) :
        print( "====test3======fixed noisescale======================" )
        plot = self.doplot

        nn = 10
        x = numpy.linspace( 0, 2, nn, dtype=float )
        ym = 0.3 + 0.5 * x
        nf = 0.2
        numpy.random.seed( 2345 )
        noise = numpy.random.randn( nn )

        y = ym + nf * noise
        limits = [-1,2]

        pm = PolynomialModel( 1 )
        bf = Fitter( x, pm, fixedScale=nf )

        pars = bf.fit( y )
        logz0 = bf.getLogZ( limits=limits )
        logl0 = bf.logLikelihood
        print( "pars  ", fmt( pars ) )
        print( "stdv  ", fmt( bf.stdevs ) )
        print( "logZ  ", fmt( logz0 ), "   logL  ", fmt( logl0 ) )

        if plot :
            plt.figure( "model" )
            plotFit( x, data=y, model=pm, ftr=bf, truth=ym, show=False )

        errdis = GaussErrorDistribution( scale=nf )
        problem = ClassicProblem( pm, xdata=x, ydata=y )

        logz1, logl1 = plotErrdis2d( errdis, problem, limits=limits, max=0,
                        plot=plot )

        if plot :
            plt.plot( pars[0], pars[1], 'k.' )

        print( "logZ  ", fmt( logz1 ), "   logL  ", fmt( logl1 ) )

        model = PolynomialModel( 1 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )

        dis = GaussErrorDistribution( scale=nf )
        ns = NestedSampler( x, model, y, distribution=dis, verbose=0, seed=3451 )

        logE = ns.sample()
        par2 = ns.parameters
        logz2 = ns.logZ
        dlz2 = ns.logZprecision
        print( "pars  ", fmt( par2 ) )
        print( "stdv  ", fmt( ns.stdevs ) )
        print( "logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

#        print( logz0 - logz1, logz0 - logz2 )
        self.assertTrue( abs( logz2 - logz0 ) < 2 * dlz2 )

        samples = ns.samples
        parevo =samples.getParameterEvolution()
        llevo = samples.getLogLikelihoodEvolution()
        lwevo = samples.getLogWeightEvolution()

        assertAAE( numpy.sum( numpy.exp( lwevo ) ), 1.0 )

        if plot :
            plt.plot( parevo[:,0], parevo[:,1], 'k,' )

            plt.figure( "model" )			# grab again
            yfit = ns.modelfit
            err = samples.monteCarloError( x )
            plt.plot( x, yfit + err, 'b-' )
            plt.plot( x, yfit - err, 'b-' )

            plt.show()

    def test4( self ) :
        print( "====test4===unknown noisescale=========================" )
        plot = self.doplot

        nn = 100
        x = numpy.arange( nn, dtype=float ) / 50
        ym = 0.4 + 0.0 * x
        nf = 0.5
        numpy.random.seed( 2345 )
        noise = numpy.random.randn( nn )

        y = ym + nf * noise
        limits = [0,1]
        nslim  = [0.1,1.0]

        pm = PolynomialModel( 0 )
        bf = Fitter( x, pm )

        pars = bf.fit( y )
        scale = bf.scale
        logz0 = bf.getLogZ( limits=limits, noiseLimits=nslim )
        logl0 = bf.logLikelihood
        print( "pars  ", fmt( pars ), "  scale  ", fmt( scale ) )
        print( "stdv  ", fmt( bf.stdevs ) )
        print( "logZ  ", fmt( logz0 ), "   logL  ", fmt( logl0 ) )

        if plot :
            plt.figure( "model" )
            plotFit( x, data=y, model=pm, ftr=bf, truth=ym, show=False )

        errdis = GaussErrorDistribution( )
        problem = ClassicProblem( pm, xdata=x, ydata=y )

        logz1, logl1 = plotErrdis2d( errdis, problem, limits=limits, nslim=nslim,
                        plot=plot )
        if plot :
            plt.plot( pars[0], scale, 'k.' )

        print( "logZ  ", fmt( logz1 ), "   logL  ", fmt( logl1 ) )

        model = PolynomialModel( 0 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )

        dis = GaussErrorDistribution( )
        dis.setLimits( nslim )
        ns = NestedSampler( x, model, y, distribution=dis, verbose=0 )

        logE = ns.sample()
        par2 = ns.parameters
        scl2 = ns.scale
        logz2 = ns.logZ
        dlz2 = ns.logZprecision
        print( "pars  ", fmt( par2 ), "  scale  ", fmt( scl2 ) )
        print( "stdv  ", fmt( ns.stdevs ) )
        print( "logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

        self.assertTrue( abs( logz2 - logz1 ) < 2 * dlz2 )

        samples = ns.samples
        parevo =samples.getParameterEvolution()
        scevo =samples.getScaleEvolution()
        llevo = samples.getLogLikelihoodEvolution()
        lwevo = samples.getLogWeightEvolution()

        assertAAE( numpy.sum( numpy.exp( lwevo ) ), 1.0 )

        if plot :
            plt.plot( parevo[:,0], scevo, 'k,' )

            plt.figure( "model" )			# grab again
            yfit = ns.yfit
            err = samples.monteCarloError( x )
            plt.plot( x, yfit + err, 'b-' )
            plt.plot( x, yfit - err, 'b-' )

            plt.show()


    def test5( self ) :
        print( "====test5============================" )
        plot = self.doplot

        nn = 10
        x = numpy.linspace( 0, 2, nn, dtype=float )
        ym = 0.3 + 0.5 * x
        nf = 0.1
        numpy.random.seed( 2345 )
        noise = numpy.random.randn( nn )

        y = ym + nf * noise
        limits = [-1,2]

        model = PolynomialModel( 1 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )

        s = 0.0
        s2 = 0.0
        mr = 10
        for k in range( mr ) :
            dis = GaussErrorDistribution( scale=0.5 )
            ns = NestedSampler( x, model, y, distribution=dis, verbose=0, seed=k )

            logE = ns.sample()
            par2 = ns.parameters
            logz2 = ns.logZ
            dlz2 = ns.logZprecision
            s += logz2
            s2 += logz2 * logz2
            print( "pars  ", fmt( par2 ), "  logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

        logz = s / mr
        dlz = math.sqrt( s2 / mr - logz * logz )

        print( "Average  ", fmt( logz ), " +- ", fmt( dlz ) )

    def test5a( self ) :
        print( "====test5a==discard===================" )
        plot = self.doplot

        nn = 10
        x = numpy.linspace( 0, 2, nn, dtype=float )
        ym = 0.3 + 0.5 * x
        nf = 0.1
        numpy.random.seed( 2345 )
        noise = numpy.random.randn( nn )

        y = ym + nf * noise
        limits = [-1,2]

        model = PolynomialModel( 1 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )

        s = 0.0
        s2 = 0.0
        mr = 5
        for k in [1,5,10,20,40] :
            dis = GaussErrorDistribution( scale=0.5 )
            ns = NestedSampler( x, model, y, distribution=dis, verbose=0, discard=k )

            logE = ns.sample()
            par2 = ns.parameters
            logz2 = ns.logZ
            dlz2 = ns.logZprecision
            s += logz2
            s2 += logz2 * logz2
            print( fmt( k ), "  pars  ", fmt( par2 ), "  logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

        logz = s / mr
        dlz = math.sqrt( s2 / mr - logz * logz )

        print( "Average  ", fmt( logz ), " +- ", fmt( dlz ) )

    def test6( self ) :
        print( "====test6  Laplace ================" )
        plot = self.doplot

        nn = 20
        x = numpy.linspace( 0, 2, nn, dtype=float )
        ym = 0.3 + 0.5 * x
        nf = 0.9
        numpy.random.seed( 12345 )
        noise = numpy.random.laplace( size=nn )

        y = ym + nf * noise
        limits = [-1,2]

        if plot :
            plt.plot( x, ym, 'k-' )
            plt.plot( x, y, 'r.' )

        model = PolynomialModel( 1 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )

        bf = AmoebaFitter( x, model, errdis="laplace" )

        pars = bf.fit( y, tolerance=1e-20 )
        print( "pars  ", fmt( pars ) )
        print( "stdv  ", fmt( bf.stdevs ) )
        logz0 = bf.getLogZ( limits=limits )
        logl0 = bf.logLikelihood
        print( "logZ  ", fmt( logz0 ), "   logL  ", fmt( logl0 ) )

        errdis = LaplaceErrorDistribution( scale=nf )
        problem = ClassicProblem( model, xdata=x, ydata=y )
        logz1, logl1 = plotErrdis2d( errdis, problem, limits=limits, max=0,
                plot=plot )
        if plot :
            plt.plot( pars[0], pars[1], 'k.' )

        print( "logZ  ", fmt( logz1 ), "   logL  ", fmt( logl1 ) )

        model = PolynomialModel( 1 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )
        ns = NestedSampler( x, model, y, distribution='laplace', seed=8945,
                    verbose=0, rate=0.5 )

        logE = ns.sample()

        par2 = ns.parameters
        logE = ns.logZ
        dlz2 = ns.logZprecision
        logz2 = ns.logZ
        print( "pars  ", fmt( par2 ) )
        print( "stdv  ", fmt( ns.stdevs ) )
        print( "logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

        self.assertTrue( abs( logz2 - logz1 ) < 4 * dlz2 )
#        print( logz0 - logz1, logz0 - logz2 )

        samples = ns.samples
        parevo =samples.getParameterEvolution()
        llevo = samples.getLogLikelihoodEvolution()
        lwevo = samples.getLogWeightEvolution()

        assertAAE( numpy.sum( numpy.exp( lwevo ) ), 1.0 )

        if plot :
            plt.plot( parevo[:,0], parevo[:,1], 'k,' )

            plt.show()

    def test6_0( self ) :
        print( "====test6_0  Laplace ================" )
        plot = self.doplot

        nn = 20
        x = numpy.linspace( 0, 2, nn, dtype=float )
        ym = 0.3 + 0.0 * x
        nf = 0.9
        numpy.random.seed( 2345 )
        noise = numpy.random.laplace( size=nn )

        y = ym + nf * noise
        limits = [-1,2]

        if plot :
            plt.plot( x, ym, 'k-' )
            plt.plot( x, y, 'r.' )

        model = PolynomialModel( 0 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )

        bf = PowellFitter( x, model, errdis="laplace" )

        pars = bf.fit( y, tolerance=1e-20 )
        print( "pars  ", pars )
        print( "stdv  ", fmt( bf.stdevs ) )
        logz0 = bf.getLogZ( limits=limits )
        logl0 = bf.logLikelihood
        print( "logZ  ", fmt( logz0 ), "   logL  ", fmt( logl0 ) )

        errdis = LaplaceErrorDistribution( scale=nf )
        problem = ClassicProblem( model, xdata=x, ydata=y )
        logz1, logl1 = plotErrdis( errdis, problem, limits=limits, max=0,
                plot=plot )
        if plot :
            plt.plot( pars[0], logl1, 'k.' )

        print( "logZ  ", fmt( logz1 ), "   logL  ", fmt( logl1 ) )


        model = PolynomialModel( 0 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )
        ns = NestedSampler( x, model, y, distribution='laplace', verbose=0 )

        logE = ns.sample()

        par2 = ns.parameters
        stdv = ns.stdevs
        logE = ns.logZ
        dlz2 = ns.logZprecision
        logz2 = ns.logZ
        print( "pars  ", fmt( par2 ) )
        print( "stdv  ", fmt( stdv ) )
        print( "logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

#        self.assertTrue( abs( logz2 - logz0 ) < dlz2 )
        print( logz1 - logz2 )

        samples = ns.samples
        parevo =samples.getParameterEvolution()
        llevo = samples.getLogLikelihoodEvolution()
        lwevo = samples.getLogWeightEvolution()

        assertAAE( numpy.sum( numpy.exp( lwevo ) ), 1.0 )

        if plot :
            plt.plot( parevo, numpy.exp( llevo ), 'r,' )

            mxl = numpy.exp( numpy.max( llevo ) ) * 1.2
            plt.plot( [pars,pars], [0.0,mxl], 'b-' )
            plt.plot( [par2,par2], [0.0,mxl], 'r-' )
            plt.plot( [par2,par2]+stdv, [0.0,mxl], 'g-' )
            plt.plot( [par2,par2]-stdv, [0.0,mxl], 'g-' )

            plt.show()


    def test7( self ) :
        print( "====test7  Poisson ================" )
        plot = self.doplot

        nn = 100
        x = numpy.linspace( 0, 10, nn, dtype=float )
        ym = 1.9 + 2.2 * x
        numpy.random.seed( 23415 )
        y = numpy.random.poisson( ym, size=nn )

        limits = [0,4]

        if plot :
            plt.plot( x, ym, 'k-' )
            plt.plot( x, y, 'r.' )

        model = PolynomialModel( 1 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )

        bf = AmoebaFitter( x, model, errdis="poisson" )

        pars = bf.fit( y, tolerance=1e-20 )
        print( "pars  ", fmt( pars ) )
        print( "stdv  ", fmt( bf.stdevs ) )
        logz0 = bf.getLogZ( limits=limits )
        logl0 = bf.logLikelihood
        print( "logZ  ", fmt( logz0 ), "   logl  ", fmt( logl0 ) )

        errdis = PoissonErrorDistribution( )
        problem = ClassicProblem( model, xdata=x, ydata=y )
        logz1, logl1 = plotErrdis2d( errdis, problem, limits=limits, max=0,
                    plot=plot )
        if plot :
            plt.plot( pars[0], pars[1], 'k.' )

        print( "logZ  ", fmt( logz1 ), "   logL  ", fmt( logl1 ) )

        model = PolynomialModel( 1 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )
        ns = NestedSampler( x, model, y, distribution='poisson', verbose=0, seed=123 )

        logE = ns.sample()

        par2 = ns.parameters
        logE = ns.logZ
        dlz2 = ns.logZprecision
        logz2 = ns.logZ
        samples = ns.samples

        print( "pars  ", fmt( par2 ), fmt( samples.maxLikelihoodParameters ) )
        print( "stdv  ", fmt( ns.stdevs ) )
        print( "logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

        self.assertTrue( abs( logz2 - logz1 ) < 3 * dlz2 )

        parevo =samples.getParameterEvolution()
        llevo = samples.getLogLikelihoodEvolution()
        lwevo = samples.getLogWeightEvolution()

        assertAAE( numpy.sum( numpy.exp( lwevo ) ), 1.0 )

        if plot :
            plt.plot( parevo[:,0], parevo[:,1], 'k,' )
            plt.show()


    def test8( self ) :
        print( "====test8  Uniform ================" )
        plot = self.doplot

        nn = 200
        x = numpy.linspace( 0, 2, nn, dtype=float )
        ym = 0.3 + 5.4 * x

        y = numpy.round( ym )

        limits = [-1,2]

        model = PolynomialModel( 1 )
        model.setLimits( lowLimits=[0,0], highLimits=[10,10] )

        ns = NestedSampler( x, model, y, distribution='uniform', verbose=1,
            engines=["chord"] )
#            engines=["galilean"] )

#        ns.engines[0].debug = True
        ns.distribution.setLimits( [0.1, 1000] )
        ns.minimumIterations = 501

        logE = ns.sample( plot=plot )
        plt.show()

        par2 = ns.parameters
        logE = ns.logZ
        dlz2 = ns.logZprecision
        logz2 = ns.logZ
        print( "pars  ", fmt( par2 ) )
        print( "stdv  ", fmt( ns.stdevs ) )
        print( "logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

        eng = ns.engines[0]
        nap = eng.walkers[0].nap
        print( "Uran  ", eng.getUnitRange( ns.problem, ns.lowLhood, nap ) )
#        print( eng.unitRange )
#        print( eng.unitMin )

        for w in ns.walkers :
            pars = w.allpars
            up = eng.domain2Unit( ns.problem, pars )
#            print( pars, up )
#            plt.plot( [up[0]], [up[1]], 'k.' )
#            plt.plot( [up[2]], [up[0]], 'r.' )
#            plt.plot( [up[1]], [up[2]], 'g.' )


#        plt.show()

        if plot :
            plt.show()

    def TBDtest9( self ) :
        print( "====test9  Bernoulli ================" )
        plot = self.doplot

        nn = 61
        x = numpy.linspace( -3, 3, nn, dtype=float )
        numpy.random.seed( 124 )
        xp = x + numpy.random.randn( nn )
        y = numpy.where( xp > 0, 1, 0 )
        print( fmt( x, max=None ) )
        print( fmt( xp, max=None ) )
        print( fmt( y, max=None ) )


        model = LogisticModel( fixed={0:1} )

        model.setLimits( lowLimits=[-3,-2], highLimits=[3,2] )

        ns = NestedSampler( x, model, y, distribution='bernoulli', verbose=2 )
#            engines=["chord"] )
#            engines=["galilean"] )

#        ns.engines[0].debug = True
        ns.minimumIterations = 501

        logE = ns.sample( )

        yfit1 = model( x )
        par2 = ns.parameters
        logz = ns.logZ
        dlz  = ns.logZprecision
        print( "pars  ", fmt( par2 ) )
        print( "stdv  ", fmt( ns.stdevs ) )
        print( "logZ  ", fmt( logz ), " +- ", fmt( dlz ) )
        print( "logL  ", fmt( ns.distribution.logLikelihood( ns.problem, par2 ) ) )

        bf = AmoebaFitter( x, model, errdis="bernoulli" )

        pars = bf.fit( y, tolerance=1e-20 )
        print( "pars  ", fmt( pars ) )
        print( "stdv  ", fmt( bf.stdevs ) )

#        limits = [6,4]
        logz0 = bf.getLogZ()        # limits=limits )
        logl0 = bf.logLikelihood
        print( "logZ  ", fmt( logz0 ), "   logL  ", fmt( logl0 ) )

        yfit2 = model( x )

        plt.plot( x, y, 'k.' )
        plt.plot( x, yfit1, 'r-' )
        plt.plot( x, yfit2, 'g-' )
        plt.show()

    def TBDtest10( self ) :
        print( "====test10  Bernoulli ================" )
        plot = self.doplot

        nn = 1000
        x = numpy.linspace( 0, 10, nn )
        y = numpy.zeros( nn )
        y[:300] = 1
        y[900:] = 1
        y[400:600] = 2

#        Tools.printclass( UniformPrior( limits=[0,1] ) )

        dtm = DecisionTreeModel( ndim=1, kdim=[0], depth=1, dynamic=False )
#        print( dtm.result( x, [0,1] ) )

#        Tools.printclass( dtm )

        problem = CategoricalProblem( model=dtm, xdata=x, ydata=y )
        print( problem.npars, problem.ncateg )
        print( problem.ydata.shape )

        ns = NestedSampler( problem=problem, distribution='bernoulli' )
        ns.verbose = 2

#        Tools.printclass( ns )

        logE = ns.sample( )

#        yfit1 = model( x )
        par2 = ns.parameters
        logz = ns.logZ
        dlz  = ns.logZprecision
        print( "pars  ", fmt( par2 ) )
        print( "stdv  ", fmt( ns.stdevs ) )
        print( "logZ  ", fmt( logz ), " +- ", fmt( dlz ) )
        print( "logE  ", fmt( logE ) )
        print( "logL  ", fmt( ns.distribution.logLikelihood( ns.problem, par2 ) ) )

        bf = CategoricalFitter( problem )

        pars = bf.fit( )
        print( "pars  ", fmt( pars ) )
        print( "stdv  ", fmt( bf.stdevs ) )

#        limits = [6,4]
        logz0 = bf.getLogZ( pars )
        logl0 = bf.logLikelihood
        print( "logZ  ", fmt( logz0 ), "   logL  ", fmt( logl0 ) )

#        yfit2 = model( x )

#        plt.plot( x, y, 'k.' )
#        plt.plot( x, yfit1, 'r-' )
#        plt.plot( x, yfit2, 'g-' )
#        plt.show()



if __name__ == '__main__':
    unittest.main( )

