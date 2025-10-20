# run with : python3 -m unittest TestFitter

import numpy as numpy
from numpy.testing import assert_array_almost_equal as assertAAE
import unittest
import os
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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *  2004 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2017 Do Kester

class Test( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author:      Do Kester

    """
    aa = 5              #  average offset
    bb = 2              #  slope
    ss = 0.3            #  noise Normal distr.

    x = numpy.asarray( [ -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
    x += 2
    noise = numpy.asarray( [-0.000996, -0.046035,  0.013656,  0.418449,  0.0295155,  0.273705,
      -0.204794,  0.275843, -0.415945, -0.373516, -0.158084] )

    def eq( self, a, b, eps=1e-10 ) :
        if ( a + b ) != 0 :
            return abs( a - b ) / abs( a + b ) < eps
        else :
            return abs( a - b ) < eps

    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

    #  **************************************************************
    def testStraightLineParameter( self ):
        """
        test slope fit

        1. Compare PolynomialModel(1) with chain of PowerModel(0) + PowerModel(1)

        2. Fix parameters in PolynomialModel

        """
        plot = self.doplot

        print( "\n   Fitter Test 1  \n" )
        model = PolynomialModel( 1 )
        fitter = Fitter( self.x, model )
        model0 = PowerModel( 0 )
        model1 = PowerModel( 1 )
        model0.addModel( model1 )
        altfit = Fitter( self.x, model0 )
        y = self.noise + self.aa + self.bb * self.x

        print( "Testing Straight Line fit" )

        self.assertTrue( model1.npchain == 2 )
        par = fitter.fit( y )
        alt = altfit.fit( y )

        plotFit( self.x, data=y, model=model, fitter=fitter, residuals=True, show=self.doplot )


        print( "offst = %f  alt = %f  truth = %f"%(par[0], alt[0], self.aa) )
        print( "slope = %f  alt = %f  truth = %f"%(par[1], alt[1], self.bb) )
        assertAAE( par, alt )

        chisq = fitter.chisq
        altch = altfit.chisq
        print( "chisq = %f  alt = %f"%( chisq, altch) )
        self.assertTrue( self.eq(chisq, altch) )

        std = fitter.standardDeviations
        ast = altfit.standardDeviations
        print( "stdev = %f  alt = %f"%(std[0], ast[0]) )
        print( "stdev = %f  alt = %f"%(std[1], ast[1]) )
        assertAAE( std, ast )

        par1 = altfit.fit( y, keep={0:par[0]} )

        plotFit( self.x, data=y, model=model0, fitter=altfit, residuals=False, 
            figsize=[12,7], xlim=[0,12], ylim=[-10,10], show=self.doplot )

        self.assertTrue( 2 == len( par1) )
        assertAAE( par1, par )
        self.assertTrue( model0.npchain == 2 )

        model1 = PolynomialModel( 2, fixed={2:0.0} )

        altfit = Fitter( self.x, model1 )

        par1 = altfit.fit( y )
        print( par, par1 )

        print( "x  ", self.x )
        print( "y  ", y )

        plotFit( self.x, data=y, model=model0, show=self.doplot )

        self.assertTrue( 2 == len( par1) )
        assertAAE( par, par )

        error1 = altfit.monteCarloError( )
        print( "error = ", error1 )

    #  **************************************************************
    def testNormalize( self ):
        """
        test normalized parameter, alternative for keepfixed.

        1.

        2.

        """
        plot = self.doplot

        print( "\n   Fitter Test 2 Normalize  \n" )
        model = PolynomialModel( 2 )

        sm = PowerModel( 1 )

        numpy.random.seed( 2345 )
        x = numpy.linspace( 0.0, 10.0, 101 )
        y = 1.0 + 0.5 * x - 0.2 * x * x +  numpy.random.randn( 101 ) * 0.1

        sm += model                     ## degenerate model par[0] == par[2]

        print( sm )

        fitter = Fitter( x, sm )

        self.assertTrue( sm.npchain == 4 )

        print( fmt( fitter.hessian ) )

#        ppp = fitter.fit( y, plot=self.doplot )
#        print( ppp )
        self.assertRaises( numpy.linalg.linalg.LinAlgError, fitter.fit, y )

        fitter.normalize( [0.0, 0.0, 1.0, 0.0], 1.0 )       ## fix par[2] at 1.0

        par = fitter.fit( y, plot=self.doplot )

        print( "param = ", sm.parameters )
        assertAAE( par[2], 1.0 )
        assertAAE( par, [ -0.5, 1.0, 1.0, -0.2], 1 )

        print( fmt( fitter.hessian ) )
        print( fmt( fitter.covariance ) )

        chisq = fitter.chisq
        print( "chisq = %f"%( chisq) )

        std = fitter.standardDeviations
        print( "stdev = ", std )

#        assertAAE( std, ast )


    def test3( self ):

        p = [3.2, -0.1, 0.3, 1.1, 2.1]
        ss = 0.3

        ndata = 101
        x = numpy.linspace( -1, +1, ndata, dtype=float )
        y = ( x - p[1] ) / p[2]
        numpy.random.seed( 3456 )
        y = p[0] * numpy.exp( -y * y ) + ss * numpy.random.randn( ndata )
        y += ( p[3] + p[4] * x )
        p1 = p



        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )
        print( "Testing Linear Fitter with limits" )
        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )


        print( "   1. no limits and keep in fit " )
        modl1 = PolynomialModel( 4 )

        amfit = Fitter( x, modl1 )

        par0 = amfit.limitsFit( y )
        print( "pars0   ", fmt( par0 ) )
        print( "stdv0   ", fmt( amfit.stdevs ) )
        print( "chisq0  ", amfit.chisq )
        self.assertTrue( par0[0] != 3.3 )
        self.assertTrue( par0[2] < -7 )

        par1 = amfit.limitsFit( y, keep={0:3.3} )
        print( "pars1   ", fmt( par1 ) )
        print( "stdv1   ", fmt( amfit.stdevs ) )
        print( "chisq1  ", amfit.chisq )
        self.assertTrue( par1[0] == 3.3 )
        self.assertTrue( par1[2] < -7 )

#        printclass( amfit )

        print( "   2. limits and keep in fit " )
        modl2 = PolynomialModel( 4 )
        modl2.setLimits( [-7.0], [7.0] )

        lmfit = Fitter( x, modl2 )

        par2 = lmfit.limitsFit( y )
        print( "pars2   ", fmt( par2 ) )
        print( "stdv2   ", fmt( lmfit.stdevs ) )
        print( "chisq2  ", lmfit.chisq )
        self.assertTrue( par2[0] != 3.3 )
        self.assertTrue( par2[2] == -7.0 )

        par3 = lmfit.limitsFit( y, keep={0:3.3} )
        print( "pars3   ", fmt( par3 ) )
        print( "stdv3   ", fmt( lmfit.stdevs ) )
        print( "chisq3  ", lmfit.chisq )
        self.assertTrue( par3[0] == 3.3 )
        self.assertTrue( par3[2] == -7.0 )

#        printclass( lmfit )
        """
###     For update of BaseFitter  ###        
        print( "   3. limits and keep in fitter and fit " )
        modl3 = PolynomialModel( 4 )
        modl3.setLimits( [-7.0], [7.0] )

        lmfit = Fitter( x, modl3, keep={4:5.0} )

        ## fit is same as limitsFit when limits are set
        par4 = lmfit.fit( y )
        print( "pars4   ", fmt( par4 ) )
        print( "stdv4   ", fmt( lmfit.stdevs ) )
        print( "chisq4  ", lmfit.chisq )
#        printclass( lmfit )
        self.assertTrue( par4[0] != 3.3 )
        self.assertTrue( par4[2] == -7.0 )

        par5 = lmfit.fit( y, keep={0:3.3} )
        print( "pars5   ", fmt( par5 ) )
        print( "stdv5   ", fmt( lmfit.stdevs ) )
        print( "chisq5  ", lmfit.chisq )
        self.assertTrue( par5[0] == 3.3 )
        self.assertTrue( par5[2] == -7.0 )
        self.assertTrue( len( par5 ) == 4  )
        """

        if self.doplot :
            xx = numpy.linspace( -1, +1, 1001 )
            plt.plot( x, y, 'k+' )
            plt.plot( xx, modl1.result( xx ), 'k-' )

            plt.plot( xx, modl2.result( xx ), 'r-' )
            plt.plot( xx, modl3.result( xx ), 'g-' )
            plt.show()

    def test4( self ):

        p = [1.1, 2.1, 3.2, -0.1, 0.3]
        ss = 0.3
        NP = 2

        ndata = 101
        x = numpy.linspace( -1, +1, ndata, dtype=float )
        y = ( p[0] + p[1] * x )
        ex = ( x - p[3] ) / p[4]
        numpy.random.seed( 3456 )
#        y += p[2] * numpy.exp( -ex * ex )
        y += ss * numpy.random.randn( ndata )
        p1 = p[:NP]
        


        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )
        print( "Testing Linear Fitter with Gauss priors" )
        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )


        print( "   Model 1 no priors " )
        modl1 = PolynomialModel( NP-1 )

        amfit = Fitter( x, modl1 )

        par0 = amfit.fit( y )
        print( "pars0   ", fmt( par0 ) )
        print( "stdv0   ", fmt( amfit.stdevs ) )
        print( "chisq0  ", amfit.chisq )

#        printclass( amfit )

        print( "   Model 2 Gaussian Priors " )
        modl2 = PolynomialModel( NP-1 )

        for k in range( modl2.npars ) :
            modl2.setPrior( k, GaussPrior( center=k, scale=1 ) )

        lmfit = Fitter( x, modl2 )
#        lmfit = LevenbergMarquardtFitter( x, modl2 )

        par2 = lmfit.fit( y )
        print( "pars2   ", fmt( par2 ) )
        print( "stdv2   ", fmt( lmfit.stdevs ) )
        print( "chisq2  ", lmfit.chisq )

        c = numpy.sum( numpy.square( y - modl2.result( x, par2 ) ) )
        print( c )

        print( fmt( amfit.getHessian( params=par2 ) ) )
        print( fmt( lmfit.getHessian( params=par2 ) ) )

        print( fmt( amfit.makeVariance() ), fmt( lmfit.makeVariance() ) )

#        amfit.getLogZGP()

#        print( "logZ   ", lmfit.getLogZGP() )

        ns = NestedSampler( x, modl2, y )
        print( "logZns ", fmt( ns.sample() ) )
        sl = ns.samples
        print( "logLns ", fmt( sl[-1].logL ) )

#        printclass( lmfit )


    def test6( self ):
        N = 100
        numpy.random.seed( 1234 )
        x = numpy.random.randn( N )
        x = numpy.append( x, -x )
        print( numpy.mean( x ), numpy.std( x ) )

        mdl = PolynomialModel( 0 )

        lzint = []
        NX = 200
        rx = 1
        xx = numpy.linspace( -rx, rx, NX+1 )
        print( "     center    mean   lZ_true   logLmax    lZ_ana    lZ_fit  logL_fit    logOcc")
        for k in range( 10 ):
            ## the conformal prior acts like just another datapoint at position k
            xd = numpy.append( x, [k] )
            problem = ClassicProblem( mdl, xd, xd )
            ed = GaussErrorDistribution( )
    
            hdx = rx / NX
            dx = 2 * hdx
            ldx = math.log( dx )
            par = [-rx+hdx, 1.0]
            logL = ed.logLikelihood_alt( problem, par )
            lz = ldx + logL
            yy = [logL]
            for p in xx[1:] :
                par[0] = p + hdx
                logL = ed.logLikelihood_alt( problem, par )
                yy += [logL]
                lz = numpy.logaddexp( lz, ldx + logL )
            lzint += [lz]
            pm = numpy.mean( xd )
            std = numpy.std( xd )
            std = 1.0
            stv = std / math.sqrt( 2*N +1 )
            par[0] = pm
            chisq = - numpy.sum( problem.weightedResSq( par ) )
            ll0 = ed.logLikelihood_alt( problem, par )
            lz_ana = math.log( math.sqrt( 2 * math.pi ) * stv ) + ll0
   
    
            ftr = Fitter( xd, mdl )
            par = ftr.fit( xd )
            stdev = ftr.stdevs
            lz_fit = ftr.getLogZ( limits=[0,1] )
            lf_fit = ftr.logLikelihood
            print( fmt( k ), fmt( pm ), fmt( lz ), fmt( ll0), fmt( lz_ana ),
                   fmt( lz_fit ), fmt( lf_fit ), fmt( ftr.logOccam ) )
            print( fmt( par ), fmt( pm ), fmt( stdev ), fmt( stv ) )

#            self.assertTrue( par[0] == pm )
#            self.assertTrue( stdev[0] 

    def test7( self ):
        N = 100
        numpy.random.seed( 1234 )
        x = numpy.random.randn( N )
        x = numpy.append( x, -x )
        print( numpy.mean( x ), numpy.std( x ) )
        w = numpy.ones_like( x )

        mdl = PolynomialModel( 0 )

        scl = 1.0
        s2 = scl * scl
        lzint = []
        NX = 200
        rx = 1
        xx = numpy.linspace( -rx, rx, NX+1 )
        print( "     center    mean   lZ_true   logLmax    lZ_ana    lZ_fit  logL_fit    logOcc")
        for k in range( 10 ):
            ## set a gaussPrior with center at k
            gapr = GaussPrior( center=k, scale=scl )
            mdl.setPrior( 0, gapr )
            problem = ClassicProblem( mdl, x, x )
            ed = GaussErrorDistribution( )
    
            hdx = rx / NX
            dx = 2 * hdx
            ldx = math.log( dx )
            par = [-rx+hdx, 1.0]
            logL = ed.logLikelihood_alt( problem, par )
            lgpr = gapr.logResult( par[0] )
            logL += lgpr
            lz = ldx + logL
            yy = [logL]
            for p in xx[1:] :
                par[0] = p + hdx
                logL = ed.logLikelihood_alt( problem, par )
                lgpr = gapr.logResult( par[0] )
                logL += lgpr
                yy += [logL]
                lz = numpy.logaddexp( lz, ldx + logL )
            lzint += [lz]

            wd = numpy.append( w, [1/s2] )
            xd = numpy.append( x, [k] )
            pm = numpy.average( xd, weights=wd )
            std = numpy.std( xd )
            std = 1.0
            stv = std / math.sqrt( 2*N +1 )
            par[0] = pm
            chisq = - numpy.sum( problem.weightedResSq( par ) )
            ll0 = ed.logLikelihood_alt( problem, par ) + gapr.logResult( par[0] )
            lz_ana = math.log( math.sqrt( 2 * math.pi ) * stv ) + ll0
   
    
            ftr = Fitter( x, mdl )
            par = ftr.fit( x )
            stdev = ftr.stdevs
            lz_fit = ftr.getLogZ( limits=[0,1] )
            lf_fit = ftr.logLikelihood
            print( fmt( k ), fmt( par ), fmt( lz ), fmt( ll0), fmt( lz_ana ),
                   fmt( lz_fit ), fmt( lf_fit ), fmt( ftr.logOccam ) )

### for later when BaseFitter can do logZGP.
#            lz_gpr = ftr.getLogZGP()
#            lf_gpr = ftr.logLikelihood
#            oc_gpr = ftr.logOccam
#            wd_gpr = math.sqrt( numpy.linalg.det( ftr.covariance ) )

#            print( fmt( par ), fmt( pm ), fmt( stdev ), fmt( wd_gpr ), fmt( lz_gpr ),
#                    fmt( lf_gpr ), fmt( oc_gpr ) )



    def xxx():
        self.assertTrue( par2[0] != 3.3 )
        self.assertTrue( par2[2] == -7.0 )

        par3 = lmfit.limitsFit( y, keep={0:3.3} )
        print( "pars3   ", fmt( par3 ) )
        print( "stdv3   ", fmt( lmfit.stdevs ) )
        print( "chisq3  ", lmfit.chisq )
        self.assertTrue( par3[0] == 3.3 )
        self.assertTrue( par3[2] == -7.0 )

#        printclass( lmfit )

        print( "   3. limits and keep in fitter and fit " )
        modl3 = PolynomialModel( 4 )
        modl3.setLimits( [-7.0], [7.0] )

        lmfit = Fitter( x, modl3, keep={4:5.0} )

        ## fit is same as limitsFit when limits are set
        par4 = lmfit.fit( y )
        print( "pars4   ", fmt( par4 ) )
        print( "stdv4   ", fmt( lmfit.stdevs ) )
        print( "chisq4  ", lmfit.chisq )
#        printclass( lmfit )
        self.assertTrue( par4[0] != 3.3 )
        self.assertTrue( par4[2] == -7.0 )

        par5 = lmfit.fit( y, keep={0:3.3} )
        print( "pars5   ", fmt( par5 ) )
        print( "stdv5   ", fmt( lmfit.stdevs ) )
        print( "chisq5  ", lmfit.chisq )
        self.assertTrue( par5[0] == 3.3 )
        self.assertTrue( par5[2] == -7.0 )
        self.assertTrue( len( par5 ) == 4  )


        if self.doplot :
            xx = numpy.linspace( -1, +1, 1001 )
            plt.plot( x, y, 'k+' )
            plt.plot( xx, modl1.result( xx ), 'k-' )

            plt.plot( xx, modl2.result( xx ), 'r-' )
            plt.plot( xx, modl3.result( xx ), 'g-' )
            plt.show()


    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestFitter.__class__ )

if __name__ == '__main__':
    unittest.main( )



