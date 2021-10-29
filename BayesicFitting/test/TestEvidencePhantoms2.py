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


class TestEvidence2( unittest.TestCase  ) :

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
        ns = PhantomSampler( x, model, y, verbose=0 )

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
        ns = PhantomSampler( x, model, y, verbose=0 )

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
        ns = PhantomSampler( x, model, y, verbose=0 )

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
        ns = PhantomSampler( x, model, y, distribution=dis, verbose=0 )

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
        ns = PhantomSampler( x, model, y, distribution=dis, verbose=0 )
        ns.step = 1

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

    def test5_1( self ) :
        self.dotest5( step=1 )
    def test5_2( self ) :
        self.dotest5( step=2 )
    def test5_4( self ) :
        self.dotest5( step=4 )
    def test5_5( self ) :
        self.dotest5( step=5 )
    def test5_10( self ) :
        self.dotest5( step=10 )


    def dotest5( self, step=10 ) :
        print( "====test5====step=%d========================" % step )
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
            ns = PhantomSampler( x, model, y, distribution=dis, verbose=0, seed=k+12*step )
            ns.step = step

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

    def test6( self ) :
        print( "====test6  Laplace ================" )
        plot = self.doplot

        nn = 20
        x = numpy.linspace( 0, 2, nn, dtype=float )
        ym = 0.3 + 0.5 * x
        nf = 0.9
        numpy.random.seed( 2345 )
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
        ns = PhantomSampler( x, model, y, distribution='laplace', seed=8907,
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
        ns = PhantomSampler( x, model, y, distribution='laplace', verbose=0 )

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
        numpy.random.seed( 2345 )
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
        ns = PhantomSampler( x, model, y, distribution='poisson', verbose=0, seed=23456 )

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

        ns = PhantomSampler( x, model, y, distribution='uniform', verbose=1,
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
        eng.calculateUnitRange()
        print( eng.unitRange )
        print( eng.unitMin )

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

    def XXXtest9( self ) :
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

        ns = PhantomSampler( x, model, y, distribution='bernoulli', verbose=2 )
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

    def XXXtest10( self ) :
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

        ns = PhantomSampler( problem=problem, distribution='bernoulli' )
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

