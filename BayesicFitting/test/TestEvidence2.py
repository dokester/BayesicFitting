# run with : python3 -m unittest TestEvidence2

import unittest
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

    def plot1( self ) :
        self.test1( plot=True )

    def plot2( self ) :
        self.test2( plot=True )

    def plot3( self ) :
        self.test3( plot=True )

    def plot4( self ) :
        self.test4( plot=True )

    def plot6( self ) :
        self.test6( plot=True )

    def plot7( self ) :
        self.test7( plot=True )

    def test1( self, plot=False ) :
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

        errdis = GaussErrorDistribution ( x, y )

        logz1, maxll = plotErrdis( errdis, pm, limits=limits,
                                    max=0, plot=plot )

        print( "logZ  ", fmt( logz1 ) )

        model = PolynomialModel( 0 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )
        ns = NestedSampler( x, model, y, verbose=0 )

        yfit = ns.sample()

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

        if plot :
            plt.plot( parevo, numpy.exp( llevo ), 'r,' )

            mxl = numpy.exp( numpy.max( llevo ) ) * 1.2
            plt.plot( [pars,pars], [0.0,mxl], 'b-' )
            plt.plot( [par2,par2], [0.0,mxl], 'r-' )
            plt.plot( [par2,par2]+stdv, [0.0,mxl], 'g-' )
            plt.plot( [par2,par2]-stdv, [0.0,mxl], 'g-' )

            plt.show()

    def test2( self, plot=False ) :
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

        errdis = GaussErrorDistribution ( x, y )

        logz1, logl1 = plotErrdis2d( errdis, pm, limits=limits, max=0,
                    plot=plot )

        if plot :
            plt.plot( pars[0], pars[1], 'k.' )

        print( "logZ  ", fmt( logz1 ) )

        model = PolynomialModel( 1 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )
        ns = NestedSampler( x, model, y, verbose=0 )

        yfit = ns.sample()

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

        if plot :
            plt.show()

    def test2_1( self, plot=False ) :
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

        errdis = GaussErrorDistribution ( x, y )

        logz1, logl1 = plotErrdis2d( errdis, pm, limits=limits, max=0,
                    plot=plot )
        if plot :
            plt.plot( pars[0], pars[1], 'k.' )

        print( "logZ  ", fmt( logz1 ), "   logL  ", fmt( logl1 ) )

        model = PolynomialModel( 1 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )
        ns = NestedSampler( x, model, y, verbose=0 )

        yfit = ns.sample()

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

        if plot :
            plt.show()

    def test3( self, plot=False ) :
        print( "====test3============================" )
        nn = 10
        x = numpy.linspace( 0, 2, nn, dtype=float )
        ym = 0.3 + 0.5 * x
        nf = 0.1
        numpy.random.seed( 2345 )
        noise = numpy.random.randn( nn )

        y = ym + nf * noise
        limits = [-1,2]

        pm = PolynomialModel( 1 )
        bf = Fitter( x, pm, fixedScale=0.5 )

        pars = bf.fit( y )
        logz0 = bf.getLogZ( limits=limits )
        logl0 = bf.logLikelihood
        print( "pars  ", fmt( pars ) )
        print( "stdv  ", fmt( bf.stdevs ) )
        print( "logZ  ", fmt( logz0 ), "   logL  ", fmt( logl0 ) )

        if plot :
            plt.figure( "model" )
            plotFit( x, data=y, model=pm, ftr=bf, truth=ym, show=False )

        errdis = GaussErrorDistribution ( x, y, scale=0.5 )

        logz1, logl1 = plotErrdis2d( errdis, pm, limits=limits, max=0,
                        plot=plot )

        if plot :
            plt.plot( pars[0], pars[1], 'k.' )

        print( "logZ  ", fmt( logz1 ), "   logL  ", fmt( logl1 ) )

        model = PolynomialModel( 1 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )

        dis = GaussErrorDistribution( x, y, scale=0.5 )
        ns = NestedSampler( x, model, y, distribution=dis, verbose=0 )

        yfit = ns.sample()
        par2 = ns.parameters
        logz2 = ns.logZ
        dlz2 = ns.logZprecision
        print( "pars  ", fmt( par2 ) )
        print( "stdv  ", fmt( ns.stdevs ) )
        print( "logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

#        print( logz0 - logz1, logz0 - logz2 )
        self.assertTrue( abs( logz2 - logz0 ) < dlz2 )

        samples = ns.samples
        parevo =samples.getParameterEvolution()
        llevo = samples.getLogLikelihoodEvolution()
        lwevo = samples.getLogWeightEvolution()

        assertAAE( numpy.sum( numpy.exp( lwevo ) ), 1.0 )

        if plot :
            plt.plot( parevo[:,0], parevo[:,1], 'k,' )

            plt.figure( "model" )			# grab again
            err = samples.monteCarloError( x )
            plt.plot( x, yfit + err, 'b-' )
            plt.plot( x, yfit - err, 'b-' )

            plt.show()

    def test4( self, plot=False ) :
        print( "====test4============================" )

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

        errdis = GaussErrorDistribution ( x, y )

        logz1, logl1 = plotErrdis2d( errdis, pm, limits=limits, nslim=nslim,
                        plot=plot )
        if plot :
            plt.plot( pars[0], scale, 'k.' )

        print( "logZ  ", fmt( logz1 ), "   logL  ", fmt( logl1 ) )

        model = PolynomialModel( 0 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )

        dis = GaussErrorDistribution( x, y )
        dis.setLimits( nslim )
        ns = NestedSampler( x, model, y, distribution=dis, verbose=0 )

        yfit = ns.sample()
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
            err = samples.monteCarloError( x )
            plt.plot( x, yfit + err, 'b-' )
            plt.plot( x, yfit - err, 'b-' )

            plt.show()


    def test5( self, plot=None ) :
        print( "====test5============================" )
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
            dis = GaussErrorDistribution( x, y, scale=0.5 )
            ns = NestedSampler( x, model, y, distribution=dis, verbose=0, seed=k )

            yfit = ns.sample()
            par2 = ns.parameters
            logz2 = ns.logZ
            dlz2 = ns.logZprecision
            s += logz2
            s2 += logz2 * logz2
            print( "pars  ", fmt( par2 ), "  logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

        logz = s / mr
        dlz = math.sqrt( s2 / mr - logz * logz )

        print( "Average  ", fmt( logz ), " +- ", fmt( dlz ) )

    def test6( self, plot=False ) :
        print( "====test6  Laplace ================" )

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

        errdis = LaplaceErrorDistribution( x, y, scale=nf )
        logz1, logl1 = plotErrdis2d( errdis, model, limits=limits, max=0,
                plot=plot )
        if plot :
            plt.plot( pars[0], pars[1], 'k.' )

        print( "logZ  ", fmt( logz1 ), "   logL  ", fmt( logl1 ) )

        model = PolynomialModel( 1 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )
        ns = NestedSampler( x, model, y, distribution='laplace', verbose=0 )

        yfit = ns.sample()

        par2 = ns.parameters
        logz2 = ns.logZ
        dlz2 = ns.logZprecision
        print( "pars  ", fmt( par2 ) )
        print( "stdv  ", fmt( ns.stdevs ) )
        print( "logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

        self.assertTrue( abs( logz2 - logz1 ) < 2 * dlz2 )
#        print( logz0 - logz1, logz0 - logz2 )

        samples = ns.samples
        parevo =samples.getParameterEvolution()
        llevo = samples.getLogLikelihoodEvolution()
        lwevo = samples.getLogWeightEvolution()

        assertAAE( numpy.sum( numpy.exp( lwevo ) ), 1.0 )

        if plot :
            plt.plot( parevo[:,0], parevo[:,1], 'k,' )

            plt.show()

    def test6_0( self, plot=False ) :
        print( "====test6_0  Laplace ================" )

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

        errdis = LaplaceErrorDistribution( x, y, scale=nf )
        logz1, logl1 = plotErrdis( errdis, model, limits=limits, max=0,
                plot=plot )
        if plot :
            plt.plot( pars[0], logl1, 'k.' )

        print( "logZ  ", fmt( logz1 ), "   logL  ", fmt( logl1 ) )


        model = PolynomialModel( 0 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )
        ns = NestedSampler( x, model, y, distribution='laplace', verbose=0 )

        yfit = ns.sample()

        par2 = ns.parameters
        stdv = ns.stdevs
        logz2 = ns.logZ
        dlz2 = ns.logZprecision
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

    def test6_1( self, plot=False ) :
        print( "====test6_1  Laplace ================" )

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

        errdis = LaplaceErrorDistribution( x, y, scale=nf )
        logz1, logl1 = plotErrdis2d( errdis, model, limits=limits, max=0,
                        plot=plot )
        if plot :
            plt.plot( pars[0], pars[1], 'k.' )

        print( "logZ  ", fmt( logz1 ), "   logL  ", fmt( logl1 ) )


        model = PolynomialModel( 1 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )
        ns = NestedSampler( x, model, y, distribution='laplace', verbose=0 )

        yfit = ns.sample()

        par2 = ns.parameters
        logz2 = ns.logZ
        dlz2 = ns.logZprecision
        print( "pars  ", fmt( par2 ) )
        print( "stdv  ", fmt( ns.stdevs ) )
        print( "logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

        self.assertTrue( abs( logz2 - logz0 ) < 5 * dlz2 )

        samples = ns.samples
        parevo =samples.getParameterEvolution()
        llevo = samples.getLogLikelihoodEvolution()
        lwevo = samples.getLogWeightEvolution()

        assertAAE( numpy.sum( numpy.exp( lwevo ) ), 1.0 )

        if plot :
            plt.plot( parevo[:,0], parevo[:,1], 'k,' )

            plt.show()

    def test7( self, plot=False ) :
        print( "====test7  Poisson ================" )

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

        errdis = PoissonErrorDistribution( x, y )
        logz1, logl1 = plotErrdis2d( errdis, model, limits=limits, max=0,
                    plot=plot )
        if plot :
            plt.plot( pars[0], pars[1], 'k.' )

        print( "logZ  ", fmt( logz1 ), "   logL  ", fmt( logl1 ) )

        model = PolynomialModel( 1 )
        model.setLimits( lowLimits=limits[0], highLimits=limits[1] )
        ns = NestedSampler( x, model, y, distribution='poisson', verbose=0 )

        yfit = ns.sample()

        par2 = ns.parameters
        logz2 = ns.logZ
        dlz2 = ns.logZprecision
        samples = ns.samples

        print( "pars  ", fmt( par2 ), fmt( samples.maxLikelihoodParameters ) )
        print( "stdv  ", fmt( ns.stdevs ) )
        print( "logZ  ", fmt( logz2 ), " +- ", fmt( dlz2 ) )

        self.assertTrue( abs( logz2 - logz1 ) < dlz2 )

        parevo =samples.getParameterEvolution()
        llevo = samples.getLogLikelihoodEvolution()
        lwevo = samples.getLogWeightEvolution()

        assertAAE( numpy.sum( numpy.exp( lwevo ) ), 1.0 )

        if plot :
            plt.plot( parevo[:,0], parevo[:,1], 'k,' )
            plt.show()


if __name__ == '__main__':
    unittest.main( )

