# run with : python3 -m unittest TestEvidence

import unittest
import os
import numpy as np
import math
from numpy.testing import assert_array_almost_equal as assertAAE

import matplotlib.pyplot as plt
from BayesicFitting import *


class TestEvidence( unittest.TestCase  ) :

    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

    def testEvidence( self ) :
        print( "====testEvidence======================" )
        nn = 100
        x = np.arange( nn, dtype=float ) / (nn/2) - 1
        ym = 1.2 + 0.5 * x
        nf = 0.1
        np.random.seed( 2345 )
        noise = np.random.randn( nn )

        y = ym + nf * noise

        pm = PolynomialModel( 1 )
        bf = Fitter( x, pm )
        w = np.ones( nn, dtype=float )

        pars = bf.fit( y, w )
        print( "pars  ", pars )
        yfit = pm.result( x, pars )
        print( "stdv  ", bf.getStandardDeviations() )
        bf.getHessian()
        bf.chiSquared( y, weights=w )
        print( "chisq %f  scale %f  sumwgt %f" % ( bf.chisq, bf.getScale(), bf.sumwgt ) )

        lolim = [-100.0,-100.0]
        hilim = [+100.0,+100.0]
        nslim = [0.01, 100.0]

        print( "=== Evidence for Parameters only; fixedScale is not set" )
        print( "evid %f  occam %f  lhood %f  fixedScale="%
            ( bf.getLogZ(  limits=[lolim,hilim] ),
            bf.logOccam, bf.logLikelihood ), bf.fixedScale )

        if self.doplot :
            plt.plot( x, ym, 'g.' )
            plt.plot( x, y, 'b+' )
            plt.plot( x, yfit, 'r-' )
            plt.show()


        print( "=== Evidence for Parameters and scale; fixedScale not set" )
        print( "evid %f  occam %f  lhood %f  fixedScale="%
            ( bf.getLogZ(  limits=[lolim,hilim], noiseLimits=nslim ),
            bf.logOccam, bf.logLikelihood ), bf.fixedScale )
#        self.assertRaises( ValueError, bf.getLogZ() )
#        self.assertRaises( ValueError, bf.logOccam )
#        self.assertRaises( ValueError, bf.logLikelihood )

        print( "=== Evidence for Parameters and scale; fixedScale=10" )
        bf.fixedScale = 10.0
        print( "evid %f  occam %f  lhood %f  fixeScale=%f" %
            ( bf.getLogZ( limits=[lolim,hilim], noiseLimits=nslim ),
            bf.logOccam, bf.logLikelihood, bf.fixedScale ) )

        print( "=== Evidence for Parameters, fixed scale = 1" )
        print( "evid %f  occam %f  lhood %f  fixeScale=%f" %
            ( bf.getLogZ( limits=[lolim,hilim] ),
            bf.logOccam, bf.logLikelihood, bf.fixedScale ) )

        print( "=== Evidence for Parameters and fixed scale = 0.01" )
        bf.fixedScale = 0.01
        print( "evid %f  occam %f  lhood %f  fixeScale=%f" %
            ( bf.getLogZ( limits=[lolim,hilim] ),
            bf.logOccam, bf.logLikelihood, bf.fixedScale ) )

        print( "=== Evidence for Parameters and fixed scale = 0.1" )
        bf.fixedScale = 0.1
        print( "evid %f  occam %f  lhood %f  fixeScale=%f" %
            ( bf.getLogZ( limits=[lolim,hilim] ),
            bf.logOccam, bf.logLikelihood, bf.fixedScale ) )

        print( "=== Evidence for Parameters and fixed scale = 1.0" )
        bf.fixedScale = 1.0
        print( "evid %f  occam %f  lhood %f  fixeScale=%f" %
            ( bf.getLogZ( limits=[lolim,hilim] ),
            bf.logOccam, bf.logLikelihood, bf.fixedScale ) )

        print( "=== Evidence for Parameters and fixed scale = 10.0" )
        bf.fixedScale = 10.0
        print( "evid %f  occam %f  lhood %f  fixeScale=%f" %
            ( bf.getLogZ( limits=[lolim,hilim] ),
            bf.logOccam, bf.logLikelihood, bf.fixedScale ) )

        pm.setLimits( lolim, hilim )
        print( "limits par[0]  ", pm.priors[0].lowLimit, pm.priors[0].highLimit )
        print( "limits par[1]  ", pm.priors[1].lowLimit, pm.priors[1].highLimit )

        print( "=== Evidence for Parameters and fixed scale = 10.0" )
        bf.fixedScale = 10.0
        print( "evid %f  occam %f  lhood %f  fixeScale=%f" %
            ( bf.getLogZ( ),
            bf.logOccam, bf.logLikelihood, bf.fixedScale ) )


    def testSimple1( self ) :
        print( "====testEvidence for Gauss (Simple) ====" )
        np.random.seed( 2345 )
        nn = 100
        x = np.arange( nn, dtype=int ) // 20
#        ym = np.linspace( 1.0, 2.0, nn )
        ym = 1.5
        nf = 0.1
        noise = np.random.normal( 0.0, 1.0, nn )

        y = ym + nf * noise

        pm = PolynomialModel( 0 )
        print( pm.npchain )
        bf = Fitter( x, pm, fixedScale=nf )

        pars = bf.fit( y )
        print( "pars  ", pars )
        yfit = pm.result( x, pars )
        std = bf.stdevs
        print( "stdv  ", std )
        print( "chisq %f  scale %f  sumwgt %f" % ( bf.chisq, bf.scale, bf.sumwgt ) )
        print( bf.chiSquared( y, pars ) )

        lo = 1.40
        hi = 1.60
        logz = bf.getLogZ( limits=[lo,hi] )
        maxloglik = bf.logLikelihood
        lintpr = math.log( hi - lo )

        errdis = GaussErrorDistribution( scale=nf )
        problem = ClassicProblem( model=pm, xdata=x, ydata=y )

        npt = 401
        p0 = np.linspace( lo, hi, npt )

        for i in range( pm.npchain ) :
            L0 = np.ndarray( npt, dtype=float )
            pp = np.append( pars, [nf] )
            for k,p in enumerate( p0 ) :
                pp[i] = p
                L0[k] = errdis.logLikelihood( problem, pp )
            lz = np.log( np.sum( np.exp( L0 ) ) * (hi - lo) / npt )
            maxl = np.max( L0 )
            L0 -= maxloglik

            if self.doplot :
                gm = GaussModel()
                gm.parameters = [1.0, pars[i], std[i]]
                plt.plot( p0, gm( p0 ), 'b-' )
                plt.plot( p0, np.exp( L0 ), 'k-' )

        print( "BF logL  ", maxloglik, bf.logOccam, maxl, np.exp( maxl ), lintpr )
        print( "ED logL  ", errdis.logLikelihood( problem, np.append( pars, [nf] ) ) )
        print( "evid      %f  %f  %f"%( logz, lz - lintpr,
                maxloglik + math.log( 0.01 * math.pi ) - lintpr  ) )
#        print( "evid      %f  %f  %f"%( logz, lz, maxloglik + math.log( 0.01 * math.pi )  ) )

        if self.doplot :
            plt.show()


    def testSimpleLaplace1( self ) :
        print( "====testEvidence for Laplace (Simple 1) ====" )
        np.random.seed( 2345 )
        nn = 1000
        x = np.arange( nn, dtype=int ) // 20
        ym = np.linspace( 1.0, 2.0, nn )
        nf = 0.1
        noise = np.random.laplace( 0.0, 1.0, nn )

        y = ym + nf * noise

        pm = PolynomialModel( 0 )
        print( pm.npchain )
        bf = PowellFitter( x, pm, scale=nf, errdis="laplace" )

        pars = bf.fit( y, tolerance=1e-20 )
        print( "pars  ", pars )
        yfit = pm.result( x, pars )
        std = bf.stdevs
        print( "stdv  ", std )
        print( np.median( y ), np.mean( y ) )
        print( "scale ", bf.fixedScale  )

        print( "scale %f  sumwgt %f" % ( bf.scale, bf.sumwgt ) )


        lo = 1.45
        hi = 1.55
        logz = bf.getLogZ( limits=[lo,hi] )
        maxloglik = bf.logLikelihood
        lintpr = math.log( hi - lo )

        errdis = LaplaceErrorDistribution( scale=nf )
        problem = ClassicProblem( model=pm, xdata=x, ydata=y )

        npt = 101
        p0 = np.linspace( lo, hi, npt )

        for i in range( pm.npchain ) :
            L0 = np.ndarray( npt, dtype=float )
            pp = np.append( pars, [nf] )
            for k,p in enumerate( p0 ) :
                pp[i] = p
                L0[k] = errdis.logLikelihood( problem, pp )
            lz = np.log( np.sum( np.exp( L0 ) ) * (hi - lo) / npt )
            maxl = np.max( L0 )
            L0 -= maxl

            if self.doplot :
                gm = GaussModel()
                gm.parameters = [1.0, pars[i], std[i]]
#                gm.parameters = [1.0, pars[i], 2*nf/math.sqrt(nn) ]
                plt.plot( p0, gm( p0 ), 'b-' )
                plt.plot( p0, np.exp( L0 ), 'k-' )

        print( "BF logL  ", maxloglik, bf.logOccam, maxl, np.exp( maxl ), lintpr )
        print( "ED logL  ", errdis.logLikelihood( problem, np.append( pars, [nf] ) ) )
        print( "evid      %f  %f  %f"%( logz, lz - lintpr,
                maxloglik + math.log( 0.01 * math.pi ) - lintpr  ) )
#        print( "evid      %f  %f  %f"%( logz, lz, maxloglik + math.log( 0.01 * math.pi )  ) )

        if self.doplot :
            plt.show()


    def testGauss( self ) :
        print( "====testEvidence for Gauss============" )
        nn = 1000
        x = np.arange( nn, dtype=int ) // 20
        ym = np.linspace( 1.0, 2.0, nn )
        nf = 0.1

        np.random.seed( 2345 )
        noise = np.random.normal( 0.0, 1.0, nn )

        y = ym + nf * noise

#        pm = FreeShapeModel( nn // 20 )
        pm = PolynomialModel( 1 )
        bf = AmoebaFitter( x, pm, errdis="gauss" )

        pars = bf.fit( y )
        print( "pars  ", pars )
        yfit = pm.result( x, pars )
        std = bf.stdevs
        print( "stdv  ", std )
        print( "scale %f  sumwgt %f" % ( bf.scale, bf.sumwgt ) )

        errdis = GaussErrorDistribution( scale=nf )
        problem = ClassicProblem( model=pm, xdata=x, ydata=y )

        p0 = np.linspace( 0.0, 3.0, 301 )
        for i in range( pm.npchain ) :
            L0 = np.ndarray( 301, dtype=float )
            pp = np.append( pars, [0.1] )
            for k,p in enumerate( p0 ) :
                pp[i] = p
                L0[k] = errdis.logLikelihood( problem, pp )
            L0 -= np.max( L0 )

            if self.doplot :
                gm = GaussModel()
                gm.parameters = [1.0, pars[i], std[i]]
                plt.plot( p0, gm( p0 ), 'b-' )
                plt.plot( p0, np.exp( L0 ), 'k-' )

        if self.doplot :
            plt.show()


    def testLaplace( self ) :
        print( "====testEvidence for Laplace============" )
        nn = 100
        x = np.arange( nn, dtype=float ) / (nn/2) - 1
        ym = 1.3
        nf = 0.1
        np.random.seed( 2345 )
        noise = np.random.laplace( 0.0, 1.0, nn )

        y = ym + nf * noise

        pm = PolynomialModel( 0 )
        bf = PowellFitter( x, pm, errdis="laplace" )

        pars = bf.fit( y, tolerance=1e-10 )
        print( "pars  ", pars )
        yfit = pm.result( x, pars )
        std = bf.stdevs
        print( "stdv  ", std )
        print( "scale %f  sumwgt %f" % ( bf.scale, bf.sumwgt ) )

        errdis = LaplaceErrorDistribution( scale=nf )
        problem = ClassicProblem( model=pm, xdata=x, ydata=y )

        p0 = np.linspace( 1.2, 1.5, 201 )
        L0 = np.ndarray( 201, dtype=float )
        for k,p in enumerate( p0 ) :
            pp = [p, 0.1]
            L0[k] = errdis.logLikelihood( problem, pp )
        L0 -= np.max( L0 )

        if self.doplot :
            gm = GaussModel()
            gm.parameters = [1.0, pars[0], std[0]]
            plt.plot( p0, gm( p0 ), 'b-' )
            plt.plot( p0, np.exp( L0 ), 'k-' )

            plt.show()


if __name__ == '__main__':
    unittest.main( )

