# run with : python3 -m unittest TestWeights

import unittest
import numpy as np
import math
import os

from numpy.testing import assert_array_equal as assertAE
from numpy.testing import assert_array_almost_equal as assertAAE

import matplotlib.pyplot as plt
from BayesicFitting import *
from BayesicFitting import formatter as fmt


class Test( unittest.TestCase  ) :

    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

    def testWeights1( self ) :
        print( "====testWeights 1====================" )

        self.stdtst1( Fitter )

    def testWeights2( self ) :
        print( "====testWeights 1====================" )

        self.stdtst2( Fitter, verbose=0 )

    def testWeights3( self ) :
        print( "====testWeights 3====================" )

        self.stdtst1( LevenbergMarquardtFitter )

    def testWeights4( self ) :
        print( "====testWeights 4====================" )

        self.stdtst1( QRFitter )

    def testWeights5( self ) :
        print( "====testWeights 5====================" )

        self.stdtst1( CurveFitter )

### Test is OK but fails exact outcomes.
### because we need order = 1 on AmoebaFitter.
#    def testWeights6( self ) :
#        print( "====testWeights 6====================" )
#
#        self.stdtst1( AmoebaFitter, order=1 )


    def testPlot( self ) :
        if not self.doplot :
            return

        nn = 5
        x = np.arange( nn, dtype=float )
        y = 2 * ( x % 2 ) - 1
        y[2] = 0.0
        x4 = np.arange( 4 * nn, dtype=float )
        y4 = np.append( y, y )
        y4 = np.append( y4, y4 )

        upr = UniformPrior( limits=[-10,10] )

        pm = PolynomialModel( 0 )
        pm.priors = upr

        bf = Fitter( x, pm )
        par = bf.fit( y )
        evi = bf.evidence

        print( "evidence   %8.3f" % evi )

        s = 0
        ns = 10
        sam = numpy.zeros( ns, dtype=float )
        for k in range( ns ):
            evid1, prec1, logL1 = self.nstst( x, y, pm, seed=2345+k*56 )
            print( "%4d  NSevid  %8.3f +- %.3f" % ( k, evid1, prec1 ) )
            sam[k] = evid1
            s += evid1
        aver = s / ns
        print( "aver   %8.3f" % aver )

        nbin = 5
        plt.hist( sam, nbin, facecolor='g', alpha=0.5 )
        plt.plot( [evi,evi], [0, ns/nbin], 'r-' )
        plt.plot( [aver,aver], [0, ns/nbin], 'b-' )
        plt.show()

    def nstdtst( self, x, y, mdl, ftr, wgt=None, acc=None, verbose=0 ) :
        par = ftr.fit( y, weights=wgt, accuracy=acc )
        std = ftr.stdevs
        cov = ftr.covariance
        hes = ftr.hessian
        var = ftr.makeVariance()
        chi = ftr.chisq
        scl = ftr.scale
        swt = ftr.sumwgt

        print( "pars  ", par, "stdv  ", std, "hess  ", hes, "cov  ", cov )
        print( "chisq  %8.3f  scale   %8.3f sumwgt  %8.3f" % ( chi, scl, swt ) )

        assertAE( par, ftr.parameters )
        assertAE( std, np.sqrt( np.diag( cov ) ) )
        assertAE( scl, np.sqrt( var ) )

        evi = ftr.evidence
        lgl = ftr.logLikelihood
        lgo = ftr.logOccam
        print( "Evid    %8.3f  logL    %8.3f logOcc    %8.3f" % ( evi, lgl, lgo ) )


        ns = NestedSampler( x, mdl, y, weights=wgt, accuracy=acc, verbose=verbose, 
                            limits=[0.01,10] )

        nevi = ns.sample()

        npar = ns.parameters
        nstd = ns.stdevs
        nlgl = ns.walkers[0].logL
        prec = ns.precision 

        print( "NSpars  ", ns.parameters, "stdv  ", ns.stdevs )
        print( "NSevid  %8.3f +- %.3f   logL %.3f" % ( nevi, prec, lgl ) )

        assertAAE( par, npar )
        assertAAE( std, nstd )
        assertAAe( lgl, nlgl )
        self.assertTrue( abs( evi - nevi ) < 2 * prec )

        return ( par, std, scl, var, chi, swt )



    def stdtst( self, y, pm, bf, wgt=None, acc=None ) :
        par = bf.fit( y, weights=wgt, accuracy=acc )
        std = bf.stdevs
        cov = bf.covariance
        hes = bf.hessian
        var = bf.makeVariance()
        chi = bf.chisq
        scl = bf.scale
        swt = bf.sumwgt

        print( "pars  ", par, "stdv  ", std, "hess  ", hes, "cov  ", cov )
        print( "chisq  %8.3f  scale   %8.3f sumwgt  %8.3f" % ( chi, scl, swt ) )

        assertAE( par, bf.parameters )
        assertAE( std, np.sqrt( np.diag( cov ) ) )
        assertAE( scl, np.sqrt( var ) )

        if pm.hasPriors() :
            evi = bf.evidence
            print( "Evid    %8.3f  logL    %8.3f logOcc    %8.3f" % ( evi, bf.logLikelihood, bf.logOccam ) )

        return ( par, std, scl, var, chi, swt )

    def nstst( self, x, y, mdl, wgt=None, acc=None, verbose=0, seed=2023 ) :
        ns = NestedSampler( x, mdl, y, weights=wgt, accuracy=acc, verbose=verbose, seed=seed )
        evi = ns.sample()

        print( "NSpars  ", ns.parameters, "stdv  ", ns.stdevs )
        
        return ( evi, ns.precision, ns.walkers[0].logL )


    def stdtst2( self, myFitter, verbose=0 ) :
        nn = 5
        x = np.arange( nn, dtype=float )
        y = 2 * ( x % 2 ) - 1
        y[2] = 0.0
        x4 = np.arange( 4 * nn, dtype=float )
        y4 = np.append( y, y )
        y4 = np.append( y4, y4 )

        upr = UniformPrior( limits=[-10,10] )

        pm = PolynomialModel( 0 )
        pm.priors = upr
        bf = myFitter( x, pm )

        print( "\n    %s" % bf )
    
        wgt = None
        print( "\n======= 5 data points; weighs = ", wgt )
        print( "ydata  ", y )
        ( par1, std1, scl1, var1, chi1, swt1 ) = self.stdtst( y, pm, bf, wgt=wgt )
        evi1 = bf.evidence
        evid1, prec1, logL1 = self.nstst( x, y, pm, wgt=wgt, verbose=verbose )
        print( "NSevid  %8.3f +- %.3f   logL %.3f" % ( evid1, prec1, logL1 ) )

        print( "\n======= 20 data points; weights = ", wgt )
        print( "ydata  ", y4 )
        pm = PolynomialModel( 0 )
        pm.priors = upr
        bf = myFitter( x4, pm )
        ( par2, std2, scl2, var2, chi2, swt2 ) = self.stdtst( y4, pm, bf )
        evid2, prec2, logL2 = self.nstst( x4, y4, pm, verbose=verbose )
        print( "NSevid  %8.3f +- %.3f   logL %.3f" % ( evid2, prec2, logL2 ) )

        sq15 = 1.0 / math.sqrt( 1.5 )
        acc = np.asarray( [2, 0.5, sq15, 2.0, 0.5], dtype=float )
        wgt = 1.0 / ( acc * acc )
        # normalize to weights to nn (=5)
        # making case 3 completely the same as case 1 (also for the evidence
        wgt *= 5 / np.sum( wgt )
        acc = 1 / np.sqrt( wgt )
        y *= acc


        print( "\n======= 5 data points; weights = ", fmt( wgt, max=None ) )
        print( "ydata  ", y )
        pm = PolynomialModel( 0 )
        pm.priors = upr
        bf = myFitter( x, pm )
        ( par3, std3, scl3, var3, chi3, swt3 ) = self.stdtst( y, pm, bf, wgt=wgt )
        evi3 = bf.evidence
        evid3, prec3, logL3 = self.nstst( x, y, pm, wgt=wgt, verbose=verbose )
        print( "NSevid  %8.3f +- %.3f   logL %.3f" % ( evid3, prec3, logL3 ) )

        print( "\n======= 5 data points; accuracy = ", fmt( acc, max=None ) )
        print( "ydata  ", y )
        pm = PolynomialModel( 0 )
        pm.priors = upr
        bf = myFitter( x, pm )
        ( par4, std4, scl4, var4, chi4, swt4 ) = self.stdtst( y, pm, bf, acc=acc )
        evid4, prec4, logL4 = self.nstst( x, y, pm, acc=acc, verbose=verbose )
        print( "NSevid  %8.3f +- %.3f   logL %.3f" % ( evid4, prec4, logL4 ) )

        ## all parameters are the same
        assertAAE( par1, par2 )
        assertAAE( par3, par4 )
        assertAAE( par1, par4 )

        assertAAE( evi1, evi3 )

        assertAAE( chi1, chi3 )
        assertAAE( chi1, chi4 )
        assertAAE( scl1, scl3 )
        assertAAE( scl1, scl4 )
        assertAAE( swt1, swt3 )
        assertAAE( swt1, swt4 )
        assertAAE( std1, std3 )
        assertAAE( std1, std4 )


    def stdtst1( self, myFitter, order=0 ) :
        nn = 5
        x = np.arange( nn, dtype=float )
        y = x % 2
        y[2] = 0.5
        x4 = np.arange( 4*nn, dtype=float )
        y4 = x4 % 2
        y4[range(2,20,5)] = 0.5

        upr = UniformPrior( limits=[-10,10] )
#        printclass( upr )

        pm = PolynomialModel( order )
        pm.priors = upr
#        printclass( pm )


        bf = myFitter( x, pm )

        print( "\n    %s" % bf )
    
        print( "\n======= 5 data points; no weights ===" )
        ( par1, std1, scl1, var1, chi1, swt1 ) = self.stdtst( y, pm, bf )
        evid1, prec1, logL1 = self.nstst( x, y, pm )
        print( "NSevid  %8.3f +- %.3f   logL %.3f" % ( evid1, prec1, logL1 ) )

#        ( par1, std1, scl1, var1, chi1, swt1 ) = self.nstdtst( x, y, pm, bf )

        print( "\n======= 20 data points; no weights ===" )
        pm = PolynomialModel( order )
        pm.priors = upr
        bf = myFitter( x4, pm )
        ( par2, std2, scl2, var2, chi2, swt2 ) = self.stdtst( y4, pm, bf )

        print( "\n======= 5 data points; weights = 4 ===" )
        pm = PolynomialModel( order )
        pm.priors = upr
        bf = myFitter( x, pm )
        w = np.zeros( nn, dtype=float ) + 4
        ( par3, std3, scl3, var3, chi3, swt3 ) = self.stdtst( y, pm, bf, wgt=w )

        print( "\n======= 5 data points; accuracy = 0.5 ===" )
        pm = PolynomialModel( order )
        pm.priors = upr
        bf = myFitter( x, pm )
        acc = np.ones( nn, dtype=float ) / 2
#        acc = np.ones( nn, dtype=float )
        print( "ydata  ", y )
        ( par4, std4, scl4, var4, chi4, swt4 ) = self.stdtst( y, pm, bf, acc=acc )
        evid4, prec4, logL4 = self.nstst( x, y, pm, acc=acc )
        print( "NSevid  %8.3f +- %.3f    logL %.3f" % ( evid4, prec4, logL4 ) )

        ## all parameters are the same
        assertAAE( par1, par2 )
        assertAAE( par3, par4 )
        assertAAE( par1, par4 )

        ## 2 and 3 are completely equal
        assertAAE( std2, std3 )
        assertAAE( chi2, chi3 )
        assertAAE( scl2, scl3 )
        assertAAE( var2, var3 )
        assertAAE( swt2, swt3 )

        assertAAE( std1, std4 )
        assertAAE( scl1 * 2, scl4 ) 




        





if __name__ == '__main__':
    unittest.main( )

