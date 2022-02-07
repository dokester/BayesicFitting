# run with : python3 -m unittest TestSoftMaxModel.Test.test1

import unittest
import os
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt
import warnings

from numpy.testing import assert_array_almost_equal as assertAAE
from StdTests import stdModeltest

from BayesicFitting import *
from BayesicFitting import formatter as fmt

__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

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

class Test( unittest.TestCase ):
    """
    Test harness for SoftMax Model

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )
        self.dofull = ( "DOFULL" in os.environ and os.environ["DOFULL"] == "1" )


    def test1( self ):

        print( "****** SOFTMAX test 1 ***************" )

        m = SoftMaxModel( ndim=5, ndout=2, offset=False )
        self.assertTrue( m.npbase == 10 )
        self.assertFalse( m.offset )
        self.assertTrue( m.in2out == 10 )
        self.assertTrue( m.ndim == 5 )
        self.assertTrue( m.ndout == 2 )
        cm = m.copy()
        self.assertTrue( cm.npbase == 10 )
        self.assertFalse( cm.offset )
        self.assertTrue( cm.in2out == 10 )
        self.assertTrue( cm.ndim == 5 )
        self.assertTrue( cm.ndout == 2 )

        m = SoftMaxModel( ndim=7, ndout=3, offset=True )
        self.assertTrue( m.npbase == 24 )
        self.assertTrue( m.offset )
        self.assertTrue( m.in2out == 21 )
        self.assertTrue( m.ndim == 7 )
        self.assertTrue( m.ndout == 3 )
        cm = m.copy()
        self.assertTrue( cm.npbase == 24 )
        self.assertTrue( cm.offset )
        self.assertTrue( cm.in2out == 21 )
        self.assertTrue( cm.ndim == 7 )
        self.assertTrue( cm.ndout == 3 )

    def test1a( self ) :
        model = SoftMaxModel( ndim=1, ndout=1, offset=True )

        print( model.npars )
        p = numpy.asarray( [1.0, 1.0] )
        x = numpy.linspace( 0, 10, 101, dtype=float )

        stdModeltest( model, p, x=x, plot=self.doplot )
 
    def test1b( self ) :
        model = SoftMaxModel( ndim=1, ndout=2, offset=True, normed=False )

        print( model.npars )
        p = numpy.asarray( [1.0, 1.0, 2.0, 2.0] )
        x = numpy.linspace( 0, 10, 101, dtype=float )

        stdModeltest( model, p, x=x, plot=self.doplot )
 


    def makeData( self, nin, npt, ndout ) :
        nn = npt // ndout
        xc = numpy.asarray( [k for k in range( ndout )] * nn, dtype=float )
        numpy.random.seed( 12345 )
        x = xc + 0.3 * numpy.random.randn( nin*npt ).reshape( nin, npt )
        return ( x.transpose(), xc )


    def test2a( self ) :
        nin = 5
        npt = 9
        ndout = 3

        x, y = self.makeData( nin, npt, ndout )

        print( "****** SOFTMAX test 2a False **************" )

        m = SoftMaxModel( ndim=nin, ndout=ndout, normed=False )

        p = numpy.linspace( -1.0, 1.0, m.npars )
        print( " In %d  ND %d  NP %d  Out %d" % (nin, npt, m.npars, ndout) )

        print( "param  ", p )

        stdModeltest( m, p, x=x, plot=self.doplot )


    def test2b( self ) :
        nin = 5
        npt = 9
        ndout = 3

        x, y = self.makeData( nin, npt, ndout )

        print( "****** SOFTMAX test 2b True ***************" )

        m = SoftMaxModel( ndim=nin, ndout=ndout, normed=True )

        p = numpy.linspace( -1.0, 1.0, m.npars )
        print( " In %d  ND %d  NP %d  Out %d" % (nin, npt, m.npars, ndout) )

        print( "param  ", p )

        stdModeltest( m, p, x=x, plot=self.doplot )



    def test3( self ) :
        nin = 5
        npt = 9
        ndout = 3
        x, y = self.makeData( nin, npt, ndout )

        print( fma( x ) )

        print( "****** SOFTMAX test 2 ***************" )
        m = SoftMaxModel( ndim=nin, ndout=ndout, offset=True )

        p = numpy.linspace( -1.0, 1.0, m.npars )
        print( "param  ", p )

        stdModeltest( m, p, x=x, plot=self.doplot )

    def xxxdtest( self, x, m, p ) :

        f = m.result( x, p )
        print( "Result   ", f.shape )
        print( fma( f ) )

        if self.doplot :
            for k in range( x.shape[1] ) :
                plt.plot( x[:,k], 'k-' )
            for n in range( f.shape[1] ) :
                plt.plot( f[:,n], 'r-' )
            plt.show()


        dfdx = m.derivative( x, p )
        print( "DfDx     ", dfdx.shape )

        for k in range( x.shape[1] ) :
            xp = x.copy()
            xm = x.copy()

            xp[:,k] += 0.00001
            xm[:,k] -= 0.00001

            yp = m.result( xp, p )
            ym = m.result( xm, p )

            numx = ( yp - ym ) / 0.00002
            numx = numx.transpose()

            print( k )
            print( "dx0   ", fma( dfdx[:,:,k], indent=7 ) )
            print( "nm0   ", fma( numx, indent=7 ) )
            assertAAE( dfdx[:,:,k], numx )

        part = m.basePartial( x, p )
        for pk in part :
            print( "Partial  ", pk.shape, id( pk ) )
            print( fmt( pk, tail=6 ) )

        for k in range( m.npars ) :
            print( "parameter ", k, "  ", m.parNames[k] )
            pp = p.copy()
            pp[k] += 0.0001
            pm = p.copy()
            pm[k] -= 0.0001
            yp = m.result( x, pp )
            ym = m.result( x, pm )

            num = ( yp - ym ) / 0.0002

            mm = k // m.ndim
            if mm >= m.ndout : 
                mm = k - m.in2out

            print( "In ", k, "  Out ", mm )
            print( "part  ", fmt( part[mm][:,k], tail=3 ) )
            print( "nm0   ", fmt( num[:,mm], tail=3 ) )
            assertAAE( part[mm][:,k], num[:,mm], 4 )



    def test4a( self ) :
        self.dotest4( 1, 3, 2, True, True )

    def test4b( self ) :
        self.dotest4( 2, 4, 3, False, False )

    def test4c( self ) :
        self.dotest4( 3, 3, 2, True, False )

    def test4d( self ) :
        self.dotest4( 2, 3, 2, False, True )


    def dotest4( self, nin, npt, ndout, offset, normed ) :

        m = SoftMaxModel( ndim=nin, ndout=ndout, offset=offset, normed=normed )

        print( "****** SOFTMAX test 4 **** ", m.ndim, m.in2out, m.ndout, "***********" )
        print( "******** offset=", m.offset, "  normed=", m.normed )

#        x, y = self.makeData( nin, npt, ndout )
        
#        x = numpy.array( [[0,0,0,0,0],[1,2,3,4,5]], dtype=float )
        numpy.random.seed( 12345 )

        x = numpy.random.randn( npt, nin )
        y = numpy.random.randint( 0, high=ndout, size=npt )

        pars = numpy.random.randn( m.npars )
        print( "Pars  ", fma( pars ) )
        par = pars[:m.in2out]

        print( "X     ", fma( x, indent=7 ) )
        print( "Y     ", fma( y ) )
        print( "Res   ", fma( m.result( x, pars ), indent=7 ) )

        mprob = MultipleOutputProblem( m, x, y )
        prob = ClassicProblem( m, x, y )

        ppart = prob.partial( pars )
        print( "problem partial" )
        print( fmt( ppart, tail=6 ) ) 

        npart = m.strictNumericPartial( x, pars )
        print( "problem numpart" )
        print( fmt( npart, tail=6 ) ) 

        assertAAE( ppart, npart )


        bed = BernoulliErrorDistribution()

        logLdata = bed.logLdata( mprob, pars )
        print( "LLdata ", fma( logLdata ) )
        logLdata = bed.logLdata( prob, pars )
        print( "LLdata ", fma( logLdata ) )

        logL = bed.logLikelihood( prob, pars )
        print( "LogL   ", fma( logL ) )
        altL = bed.logLikelihood_alt( prob, pars )
        print( "altL   ", fma( altL ) )


        fi = [k for k in range( m.npars )]
        dL = bed.partialLogL_alt( prob, pars, fi )

        nL = numpy.zeros_like( dL )

        pg = bed.nextPartialData( prob, pars, fi )
        np = len( fi )
        pL = numpy.zeros( np, dtype=float )


        for k in range( m.npars ) :
            pp = pars.copy()
            pp[k] += 0.001
            pm = pars.copy()
            pm[k] -= 0.001
            Lp = bed.logLikelihood( prob, pp )
            Lm = bed.logLikelihood( prob, pm )

            nL[k] = ( Lp - Lm ) / 0.002

            pL[k] = numpy.sum( next( pg ) )

            print( fmt(k), fmt(pars[k]), fmt(dL[k]), fmt(nL[k]), fmt(pL[k]) )


        print( fma( dL ) )
        print( fma( nL ) )
        print( fma( pL ) )
        print( fma( bed.numPartialLogL( prob, pars, fi ) ) )

        assertAAE( dL, pL )



    def test5( self ) :
        nin = 5
        npt = 9
        ndout = 3

        x, y = self.makeData( nin, npt, ndout )

        print( "****** SOFTMAX test 5 ***************" )
        m = SoftMaxModel( ndim=nin, ndout=ndout, offset=True )
        m.setLimits( -10, 10 )

        problem = ClassicProblem( model=m, xdata=x, ydata=y )

        erdis = "bernoulli"
        ns = NestedSampler( problem=problem, distribution=erdis, verbose=2 )

        ## Comment next if-statement out for a full run of NestedSampler
        if not self.dofull :
            ns.ensemble = 10

        loge = ns.sample()

        sl = ns.samples
        pars = ns.parameters

        print( fma( y ) )
        print( fma( m.result( x, pars ).T ) )

        self.plotresults( x, m, y, pars )

    def test6a( self ) :
        npt = 30
        ninp = [1, 1, 8, 8]
        nout = [1, 1, 1, 3]
        nhid = [1, 5, 5, 5]

        for (ni,no,nh) in zip( ninp, nout, nhid ):
            print( ni, no, nh, npt )
            problem = self.makeModel( ni, no, nh, npt )
            

    def makeModel( self, nin, ndout, ndhid, npt ) :
        x, y = self.makeData( nin, npt, ndout )

        m1 = SoftMaxModel( ndim=nin, ndout=ndhid, offset=True )
        m1.setLimits( -10, 10 )

        p1 = numpy.random.random( m1.npars ) * 20 - 10
        print( m1.npars, fmt( m1.result( x, p1 ) ) )

        m2 = SoftMaxModel( ndim=ndhid, ndout=ndout, offset=True )
        m2.setLimits( -10, 10 )

        m = m1 | m2

        pp = numpy.random.random( m.npars ) * 20 - 10
        print( m.npars, fmt( m.result( x, pp ) ) )


        problem = ClassicProblem( model=m, xdata=x, ydata=y )
        return problem


    def test6( self ) :
        print( "****** SOFTMAX test 6 ***************" )

        nin = 8
        npt = 30
        ndout = 3
        nhid = 5

        problem = self.makeModel( nin, ndout, nhid, npt )
        x, y = self.makeData( nin, npt, ndout )

        erdis = "bernoulli"
        ns = NestedSampler( problem=problem, distribution=erdis, verbose=2 )

        ## Comment next if-statement out for a full run of NestedSampler
        if not self.dofull :
            ns.ensemble = 10

        loge = ns.sample()

        sl = ns.samples
        pars = ns.parameters

        print( fma( y ) )
        m = problem.model
        print( fma( m.result( x, pars ).T ) )


        self.plotresults( x, m, y, pars )


    def makeMap( self, npt, ndout ) :
        nn = npt // ndout
        t = []
        x = []

        numpy.random.seed( 12345 )
#        cen4 = [[0.5,0.5],[0,0],[0,1],[1,0],[1,1]]
        cen4 = [[0,1],[1,1],[0,0]]
        for n in range( ndout ) :
            t += [n] * nn

            cen = numpy.random.random( 2 )
            rot = numpy.random.random( 4 )
            rot[1:3] = ( rot[1] + rot[2] ) / 2
            rot[1:3] = 0.0
            rot[0] = 0.1
            rot[3] = 0.1

            cen = cen4[n]
            rot = rot.reshape( 2, 2 )
            xx = numpy.random.randn( 2 * nn ).reshape( nn, 2 )
            xx = numpy.inner( xx, rot )
            x = ( xx + cen ) if n == 0 else numpy.append( x, xx + cen, axis=0 )

        x = numpy.where( x > 1, 2 - x, x )
        x = numpy.where( x < 0, -x, x )

#        print( fma( x.T ) )
#        print( fma( t ) )
 
        return ( x, numpy.array( t ) )

    def test7( self ) :
        nin = 2
        npt = 600
        ndout = 3

        x, y = self.makeMap( npt, ndout )

        print( "****** SOFTMAX test 7 ***************" )
        m = SoftMaxModel( ndim=nin, ndout=ndout, offset=True )
        m.setLimits( -10, 10 )

        problem = ClassicProblem( model=m, xdata=x, ydata=y )

        erdis = "bernoulli"
        ns = NestedSampler( problem=problem, distribution=erdis, verbose=2 )

        ## Comment next if-statement out for a full run of NestedSampler
        if not self.dofull :
            ns.ensemble = 10

        loge = ns.sample()

        sl = ns.samples
        pars = ns.parameters

#        print( fma( y ) )
#        print( fma( m.result( x, pars ).T ) )

        if not self.doplot : return

#        cc = ['r.', 'g.', 'b.', 'c.', 'm.', 'y.', 'o.']
        cc = ['black', 'red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'orange']
        for k in range( ndout ) :
            q = numpy.where( y == k )
            plt.plot( x[q,1], x[q,0], color=cc[k], marker='.' )

        map = numpy.zeros( (21,21), dtype=float )
        ias = ImageAssistant()
        xx = ias.getIndices( map ) / 20.0

        yy = m.result( xx, pars )
        ax = numpy.linspace( 0, 1, 21 )
        v = numpy.linspace( 0.05, 0.95, 3 )
        v = [0.15, 0.55, 0.95]
        for k in range( ndout ) :
            map = ias.resizeData( yy[:,k], shape=[21,21] )
            plt.contour( ax, ax, map, v, colors=cc[k] )


        plt.show()        






    def plotresults( self, x, model, y, pars ) :

        if not self.doplot : return

        t = numpy.arange( len( y ), dtype=float )
#        print( fmt( t, max=10 ) )
        tt = numpy.append( t, t + 0.99 )
        ii = numpy.argsort( tt )
#        print( fmt( tt[ii], max=10 ) )
        yh = numpy.append( y, y )
#        print( fmt( y, max=10 ) )
#        print( fmt( yh[ii], max=10 ) )

        plt.plot( tt[ii], yh[ii] + 1, 'k-' )
	
        yfit = model.result( x, pars )
        dt = 1 / model.lastndout 
        t0 = 0.5 * dt
        cc = ['r.', 'g.', 'b.']
        for k in range( model.lastndout ) :
            plt.plot( t + 0.5, y + yfit[:,k], cc[k] )
#            t0 += dt

        plt.show()






    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestSoftMaxModel.__class__ )

if __name__ == '__main__':
    unittest.main( )


