# run with : python3 -m unittest TestLMFitter

import unittest
import os
import numpy as numpy
from numpy.testing import assert_array_almost_equal as assertAAE

import matplotlib.pyplot as plt

from BayesicFitting import *
from BayesicFitting import LevenbergMarquardtFitter as LMFitter

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
#  *  2017        Do Kester

class Test( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )


    def makeData( self, bg=False ) :

        p = [3.2, -0.1, 0.3, 1.1, 2.1]
        ss = 0.3

        ndata = 101
        x = numpy.linspace( -1, +1, ndata, dtype=float )
        y = ( x - p[1] ) / p[2]
        numpy.random.seed( 3456 )
        y = p[0] * numpy.exp( -y * y ) + ss * numpy.random.randn( ndata )
        if not bg :
            return (x,y,p[:3])

        y += ( p[3] + p[4] * x )
        return (x,y,p)

    def eq( self, a, b, eps=1e-10 ) :
        if ( a + b ) != 0 :
            return abs( a - b ) / abs( a + b ) < eps
        else :
            return abs( a - b ) < eps


################################################################################
    def test1( self ):

        x,y,p1 = self.makeData()

        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )
        print( "Testing Nonlinear Fitters: LevenbergMarquardt (lm)" )
        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )
        modl1 = GaussModel( )

        amfit = LMFitter( x, modl1 )

        print( "truth   ", fmt( p1 ) )
        par1 = amfit.fit( y )

        print( "pars1   ", fmt( par1 ) )
        assertAAE( par1, p1, 1 )
        print( "chisq1  ", amfit.chisq )
        print( "hessian \n", fmt( amfit.hessian ) )
        print( "design  \n", fmt( amfit.design[-4:,:], max=None ) )



        print( "With background" )
        x,z,p2 = self.makeData( bg=True )

        modl2 = GaussModel( )
        modl2.addModel( PolynomialModel(1) )

        modl2.parameters = numpy.append( par1, [0,0] )
        lmfit = LMFitter( x, modl2 )

        par2 = lmfit.fit( z )
        print( "truth   ", fmt( p2 ) )
        print( "pars2   ", fmt( par2 ) )

        print( "chisq2  ", lmfit.chisq )

        assertAAE( par2, p2, 1 )

        print( "hessian \n", fmt( lmfit.hessian ) )
        print( "design  \n", fmt( lmfit.design[-4:,:], max=None ) )

        if self.doplot :
            xx = numpy.linspace( -1, +1, 1001 )
            plt.plot( x, y, 'k+' )
            plt.plot( xx, modl1.result( xx ), 'k-' )
            plt.plot( x, z, 'r+' )
            plt.plot( xx, modl2.result( xx ), 'r-' )
            plt.show()


    def test2( self ):

        x,y,p1 = self.makeData()

        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )
        print( "Testing LevenbergMarquardt (normalized)" )
        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )
        modl1 = GaussModel( )

        amfit = LMFitter( x, modl1 )

        par1 = amfit.fit( y )

        bmfit = LMFitter( x, modl1 )

        conpr1 = numpy.asarray( [1.0,0.0,0.0] )

        bmfit.normalize( conpr1, p1[0], weight=10.0 )

        print( "Normweight = ", bmfit.normweight )

        print( "truth  ", fmt( p1 ) )

        par3 = bmfit.fit( y )
        print( "pars3  ", fmt( par3 ) )
        print( "chisq  ", fmt( bmfit.chisq ) )

        hes1 = amfit.getHessian( params=par3 )
        print( "hessian\n", fmt( hes1 ) )
        hes3 = bmfit.getHessian( params=par3 )
        print( "hessian\n", fmt( hes3 ) )

        f = bmfit.normweight
        for h1,h3 in zip( hes1.flat, hes3.flat ) :
            self.assertTrue( abs( h1 + f - h3 ) < 1e-8 )
            f = 0.0

        if self.doplot :
            xx = numpy.linspace( -1, +1, 1001 )
            plt.plot( x, y, 'k+' )
            plt.plot( xx, modl1.result( xx ), 'g-' )
            plt.show()


    def test3( self ):

        x,y,p1 = self.makeData( bg=True )

        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )
        print( "Testing Linear Fitter with limits" )
        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )


        print( "   1. no limits and keep in fit " )

        modl1 = GaussModel( )
        modl1.addModel( PolynomialModel(1) )

        amfit = LMFitter( x, modl1 )

#        par0 = amfit.limitsFit( amfit.fit, y )
        par0 = amfit.limitsFit( y )
        print( "pars0   ", fmt( par0 ) )
        print( "stdv0   ", fmt( amfit.stdevs ) )
        print( "chisq0  ", amfit.chisq )

#        par1 = amfit.limitsFit( amfit.fit, y, keep={0:3.3} )
        par1 = amfit.limitsFit( y, keep={0:3.3} )
        print( "pars1   ", fmt( par1 ) )
        print( "stdv1   ", fmt( amfit.stdevs ) )
        print( "chisq1  ", amfit.chisq )

        printclass( amfit )

        print( "   2. limits and keep in fit " )
        gm = GaussModel()
        gm.setLimits( [-3.0, -1.0, 0.1], [3.0, 1.0, 1.0] )
        pm = PolynomialModel( 1 )
        pm.setLimits( [-5], [5] )
        modl2 = gm + pm

        lmfit = LMFitter( x, modl2 )

#        par2 = lmfit.limitsFit( lmfit.fit, y )
        par2 = lmfit.limitsFit( y )
        print( "pars2   ", fmt( par2 ) )
        print( "stdv2   ", fmt( lmfit.stdevs ) )
        print( "chisq2  ", lmfit.chisq )

#        par3 = lmfit.limitsFit( lmfit.fit, y, keep={0:3.3} )
        par3 = lmfit.limitsFit( y, keep={0:3.3} )
        print( "pars3   ", fmt( par3 ) )
        print( "stdv3   ", fmt( lmfit.stdevs ) )
        print( "chisq3  ", lmfit.chisq )

        printclass( lmfit )

        print( "   2. limits and keep in fitter and fit " )
        gm = GaussModel()
        gm.setLimits( [-3.0, -1.0, 0.1], [3.0, 1.0, 1.0] )
        pm = PolynomialModel( 1 )
        pm.setLimits( [-5], [5] )
        modl3 = gm + pm

        lmfit = LMFitter( x, modl3, keep={4:5.0} )

#        par4 = lmfit.limitsFit( lmfit.fit, y )
        par4 = lmfit.limitsFit( y )
        print( "pars4   ", fmt( par4 ) )
        print( "stdv4   ", fmt( lmfit.stdevs ) )
        print( "chisq4  ", lmfit.chisq )

#        par5 = lmfit.limitsFit( lmfit.fit, y, keep={0:3.3} )
        par5 = lmfit.limitsFit( y, keep={0:3.3} )
        print( "pars5   ", fmt( par5 ) )
        print( "stdv5   ", fmt( lmfit.stdevs ) )
        print( "chisq5  ", lmfit.chisq )

        printclass( lmfit )

        if self.doplot :
            xx = numpy.linspace( -1, +1, 1001 )
            plt.plot( x, y, 'k+' )
            plt.plot( xx, modl1.result( xx ), 'k-' )

            plt.plot( xx, modl2.result( xx ), 'r-' )
            plt.show()

    def test5( self ):

        x,y,p1 = self.makeData( bg=True )

        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )
        print( "Testing Nonlinear Fitters: LevenbergMarquardt (lm)" )
        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )
        modl1 = GaussModel( )
        modl1.addModel( PolynomialModel( 1 ) )

        amfit = LMFitter( x, modl1 )

        print( "truth   ", fmt( p1 ) )
#        par1 = amfit.limitsFit( amfit.fit, y )
        par1 = amfit.limitsFit( y )

        print( "pars1   ", fmt( par1 ) )
        assertAAE( par1, p1, 1 )
        print( "chisq1  ", amfit.chisq )
        print( "hessian \n", fmt( amfit.hessian ) )
        print( "design  \n", fmt( amfit.design[-4:,:], max=None ) )


        gm = GaussModel( )
        gm.setLimits( [0.0, -1.0, 0.0], [3.2, 1.0, 1.0] )
        pm = PolynomialModel( 1 )
        pm.setLimits( [0.0, 0.0], [2.0, 2.0] )
        modl2 = gm + pm

        modl2.parameters = par1
        lmfit = LMFitter( x, modl2 )

#        par2 = lmfit.limitsFit( lmfit.fit, y )
        par2 = lmfit.limitsFit( y )
        print( "pars2   ", fmt( par2 ) )

        print( "chisq2  ", lmfit.chisq )

        assertAAE( par1, par2, 1 )

        print( "hessian \n", fmt( lmfit.hessian ) )
        print( "design  \n", fmt( lmfit.design[-4:,:], max=None ) )

        if self.doplot :
            xx = numpy.linspace( -1, +1, 1001 )
            plt.plot( x, y, 'k+' )
            plt.plot( xx, modl1.result( xx ), 'k-' )

            plt.plot( xx, modl2.result( xx ), 'r-' )
            plt.show()


    def test6( self ) :

        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )
        print( "Testing AmoebaFitter using a map" )
        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )

        N = 71
        b0 = 3.5            # amplitude of source
        b1 = 30             # position
        b2 = 45             # position
        b3 = 13             # size of source
        b4 = 0.3            # background

        sig = 0.2

        x = numpy.arange( N, dtype=float )
        x1 = ( x - b1 ) / b3
        y1 = numpy.exp( - x1 * x1 )
        x2 = ( x - b2 ) / b3
        y2 = numpy.exp( - x2 * x2 )

        y = b0 * numpy.outer( y1, y2 ) + b4
        numpy.random.seed( 130105 )
        y += sig * numpy.random.randn( N, N )

        mdl = Kernel2dModel( kernel=Gauss(), shape='circular' )
        mdl += PolySurfaceModel( 0 )
        print( mdl )
        lo = [0, 0, 0, 0.01, 0 ]
        hi = [10, 70, 70, 70, 10 ]
        #mdl.setLimits( lo, hi )
        par = [5.0,30.0,30.0,30.0,5.0]
        mdl.parameters = par

        fitter = AmoebaFitter( y, mdl, map=True )
        print( "y      ", y.shape )
        print( "xdata  ", fitter.xdata.shape )
 
        # find the parameters
        param = fitter.fit( y, temp=10, maxiter=100000, size=5 )

        print( "yfit   ", fitter.yfit.shape )
        print( "mdlfit ", mdl( fitter.xdata ).shape )
        
        print( "Parameters :", fmt( param, max=None ) )
        print( "StDevs     :", fmt( fitter.stdevs, max=None ) )
        print( "Chisq      :", fmt( fitter.chisq ) )
        print( "Scale      :", fmt( fitter.scale ) )
        print( "Evidence   :", fmt( fitter.getEvidence( limits=[-100,100] ) ) )
        print( "Covar matrix :" )
        print( fmt( fitter.covariance))



    def test4( self ) :

        self.normalizetest( Fitter )
        self.normalizetest( QRFitter )
        self.normalizetest( CurveFitter )
        self.normalizetest( LMFitter )
        self.assertRaises( NotImplementedError, self.normalizetest, AmoebaFitter )
#        self.assertRaises( NotImplementedError, self.normalizetest, PowellFitter )

    def normalizetest( self, fitter ) :

        p = numpy.asarray( [2.0, 1.3] )
        x = numpy.asarray( [1.0, 1.3, 1.5, 1.8, 2.0] )
        numpy.random.seed( 12345 )
        y = p[0] + p[1] * x + 0.5 * numpy.random.randn( 5 )

        m = PolynomialModel( 1 )

        ftr = fitter( x, m )
        print( "=============================================================" )
        print( str( ftr ) )
        print( "xdata  ", fmt( x ) )
        print( "ydata  ", fmt( y ) )

        par = ftr.fit( y )
        print( "truth  ", fmt( p ) )
        print( "param  ", fmt( par ) )

        conpr = numpy.asarray( [1.0,0.0] )
        for w in [0,1,10,100,1000] :
            m2 = m.copy()
            ftr = fitter( x, m2 )

            ftr.normalize( conpr, p[0], weight=w )

            par = ftr.fit( y )
            print( fmt( w ), fmt( par ), fmt( ftr.chisq ) )

        self.assertTrue( abs( p[0] - par[0] ) < 1e-3 )

        print( fmt( ftr.hessian ) )
#        print( fmt( ftr.getVector( y ) ) )




    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestLMFitter.__class__ )


