# run with : python3 -m unittest TestScale

import unittest
import os
import numpy as numpy
from astropy import units
import math
from numpy.testing import assert_array_almost_equal as assertAAE


from BayesicFitting import *
from BayesicFitting import formatter as fmt

import matplotlib.pyplot as plt

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
#  *  2006 Do Kester

class TestWeight2( unittest.TestCase ):
    """
    Test harness for Engines

    Author       Do Kester

    """
    def __init__( self, name ):
        super( TestWeight2, self ).__init__( name )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )


    def test1( self ):

        numpy.random.seed( 345347 )

        bs = 100
        bof = 6 * bs
        xof = 0.5 / bs
        nbin = 2 * bof + 1

        for np in [10, 100, 1000, 10000, 100000] :
            mdl1 = PolynomialModel( 0 )
            x = numpy.random.randn( np )

            ftr1 = Fitter( x, mdl1 )
            p1 = ftr1.fit( x )[0]
            s1 = ftr1.scale
            t1 = ftr1.stdevs[0]
            r1 = ftr1.stdevScale
            c1 = ftr1.chisq
            h1 = ftr1.hessian
            v1 = ftr1.covariance
            e1a = ftr1.getEvidence( limits=[-10,10], noiseLimits=[0.1,10] )
            o1a = ftr1.logOccam
            l1a = ftr1.logLikelihood
            e1b = ftr1.getEvidence( limits=[-10,10] )
            o1b = ftr1.logOccam
            l1b = ftr1.logLikelihood

            yy = numpy.zeros( nbin )
            xs = numpy.array( bs * x + bof, dtype=int )
            unq, cnt = numpy.unique( xs, return_counts=True )
            yy[unq] += cnt
            xx = numpy.linspace( -6, +6, nbin )
#            print( x )
#            print( unq )
#            print( xx[unq] )
#            print( cnt )
            mdl2 = PolynomialModel( 0 )
            ftr2 = Fitter( xx, mdl2 )
            p2 = ftr2.fit( xx, weights=yy )[0]

            s2 = ftr2.scale
            t2 = ftr2.stdevs[0]
            r2 = ftr2.stdevScale
            c2 = ftr2.chisq
            h2 = ftr2.hessian
            v2 = ftr2.covariance
            e2a = ftr2.getEvidence( limits=[-10,10], noiseLimits=[0.1,10] )
            o2a = ftr2.logOccam
            l2a = ftr2.logLikelihood
            e2b = ftr2.getEvidence( limits=[-10,10] )
            o2b = ftr2.logOccam
            l2b = ftr2.logLikelihood

            print( "Points  ", fmt( np ) )
            print( "Params  ", fmt( p1 ), " +- ", fmt( t1 ) )
            print( "Params  ", fmt( p2 ), " +- ", fmt( t2 ) )
            print( "Scale   ", fmt( s1 ), " +- ", fmt( r1 ) )
            print( "Scale   ", fmt( s2 ), " +- ", fmt( r2 ) )
            print( "Chisq   ", fmt( c1 ) )
            print( "Chisq   ", fmt( c2 ) )
            print( "Hessian ", fmt( h1 ) )
            print( "Hessian ", fmt( h2 ) )
            print( "Covar   ", fmt( v1 ) )
            print( "Covar   ", fmt( v2 ) )
            print( "Evid 1a ", fmt(e1a ), fmt( o1a ), fmt( l1a ) )
            print( "Evid 1b ", fmt(e1b ), fmt( o1b ), fmt( l1b ) )
            print( "Evid 2a ", fmt(e2a ), fmt( o2a ), fmt( l2a ) )
            print( "Evid 2b ", fmt(e2b ), fmt( o2b ), fmt( l2b ) )
            print( "         " )

            self.assertAlmostEqual( p1, p2, 1 )
            self.assertAlmostEqual( t1, t2, 2 )
            self.assertAlmostEqual( s1, s2, 1 )
            self.assertAlmostEqual( r1, r2, 2 )
#            self.assertAlmostEqual( c1, c2, 0 )
            self.assertAlmostEqual( h1, h2, 5 )
            assertAAE( v1, v2, 2 )
            self.assertAlmostEqual( e1a, e2a, 0 )
            self.assertAlmostEqual( e1b, e2b, 0 )
            self.assertAlmostEqual( o1a, o2a, 1 )
            self.assertAlmostEqual( o1b, o2b, 1 )
            self.assertAlmostEqual( l1a, l2a, 0 )
            self.assertAlmostEqual( l1b, l2b, 0 )


    def test2( self ) :

        numpy.random.seed( 345347 )

        bs = 100
        bof = 6 * bs
        xof = 0.5 / bs
        nbin = 2 * bof + 1

        np = 1000
        x0 = numpy.linspace( -9.995, 9.995, np )
        y0 = 0.1 * x0 + 0.3 * numpy.random.randn( np )

        if self.doplot : plt.plot( x0, y0, 'k.' )

        x1 = []
        y1 = []
        w1 = []
        x2 = []
        y2 = []
        w2 = []
        for kx in range( -10, 10 ) :
            qx = numpy.where( numpy.logical_and( x0 >= kx, x0 < (kx+1) ) )
            xq = x0[qx]
            yq = y0[qx]
            for ky in range( 40 ) :
                yk = -2.0 + 0.1 * ky
                q = numpy.where( numpy.logical_and( yq >= yk, yq < (yk+0.1) ) )[0]
                lenq = len( q )
                if lenq == 0: continue
                x1 = x1 + [kx + 0.5]
                y1 = y1 + [yk + 0.05]
                w1 = w1 + [len( q )]

        x2 = numpy.asarray( ( x0 + 20 ), dtype=int ) - 19.5
        y2 = numpy.asarray( ( 10 * y0 + 40 ), dtype=int ) / 10 - 3.95


        print( len(x1) )
        print( "x0 ", fmt( x0, max=8, tail=4 ) )
        print( "x2 ", fmt( x2, max=8, tail=4 ) )
        print( "y0 ", fmt( y0, max=8, tail=4 ) )
        print( "y2 ", fmt( y2, max=8, tail=4 ) )
        print( "x1 ", fmt( x1, max=8, tail=4 ) )
        print( "y1 ", fmt( y1, max=8, tail=4 ) )
        print( "w1 ", fmt( w1, max=8, tail=4 ) )
#        print( fmt( w2, max=10 ) )

        md0 = PolynomialModel( 1 )
        ft0 = Fitter( x0, md0 )
        (np0,par0,std0,scl0,sds0,chi0,hes0,cov0,evi0,occ0,lik0) = self.stdfit( md0, ft0, y0 )

        md1 = PolynomialModel( 1 )
        ft1 = Fitter( x1, md1 )
        (np1,par1,std1,scl1,sds1,chi1,hes1,cov1,evi1,occ1,lik1) = self.stdfit( md1, ft1, y1, w=w1 )

        md2 = PolynomialModel( 1 )
        ft2 = Fitter( x2, md2 )
        (np2,par2,std2,scl2,sds2,chi2,hes2,cov2,evi2,occ2,lik2) = self.stdfit( md2, ft2, y2 )

        self.assertTrue( np0 == np1 == np2 )

        assertAAE( par0, par1, 2 )
        assertAAE( par2, par1 )
        assertAAE( std0, std1, 2 )
        assertAAE( std2, std1 )
        self.assertAlmostEqual( scl0, scl1, 2 )
        self.assertAlmostEqual( scl2, scl1 )
        self.assertAlmostEqual( sds0, sds1, 2 )
        self.assertAlmostEqual( sds2, sds1 )
        self.assertAlmostEqual( chi2, chi1 )
        assertAAE( hes2, hes1 )
        self.assertAlmostEqual( evi2, evi1 )
        self.assertAlmostEqual( occ2, occ1 )
        self.assertAlmostEqual( lik2, lik1 )

        if self.doplot :
            plt.plot( x1, y1, 'r*' )
            plt.plot( x2, y2, 'g+' )
            plt.show()



    def stdfit( self, mdl, ftr, y, w=None ) :

        np = len( y ) if w is None else numpy.sum( w )
        par = ftr.fit( y, weights=w )
        std = ftr.stdevs
        scl = ftr.scale
        sds = ftr.stdevScale
        chi = ftr.chisq
        hes = ftr.hessian
        cov = ftr.covariance
        evi = ftr.getEvidence( limits=[-10,10], noiseLimits=[0.1,10] )
        occ = ftr.logOccam
        lik = ftr.logLikelihood

        print( "Points  ", fmt( np ) )
        print( "Params  ", fmt( par ), " +- ", fmt( std ) )
        print( "Scale   ", fmt( scl ), " +- ", fmt( sds ) )
        print( "Chisq   ", fmt( chi ) )
        print( "Hessian ", fmt( hes, indent=9 ) )
        print( "Covar   ", fmt( cov, indent=9 ) )
        print( "Evid    ", fmt( evi ), fmt( occ ), fmt( lik ) )

        return (np,par,std,scl,sds,chi,hes,cov,evi,occ,lik)

    def suite( cls ):
        return unittest.TestCase.suite( TestWeight2.__class__ )


if __name__ == '__main__':
    unittest.main( )


