#run with: python3 -m unittest TestCompoundModel

import unittest
import os
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt

from StdTests import stdModeltest

from BayesicFitting import *
from BayesicFitting import formatter as fmt

__author__ = "Do Kester"
__year__ = 2018
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
#  *    2016 Do Kester

class TestDynamicModel( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

    def testDynamic( self ) :
        print( "  Test Dynamic" )
        dyn = Dynamic( dynamic=False )
        self.assertFalse( dyn.isDynamic() )

        dyn = Dynamic(  )
        self.assertTrue( dyn.isDynamic() )

        par = numpy.arange( 8, dtype=float ) * 0.1
        print( "par      ", fmt( par, max=None ) )
        par = dyn.alterParameters( par, 3, 1, 2, value=1.0 )
        print( "par      ", fmt( par, max=None ) )
        par = dyn.alterParameters( par, 4, -1, 2 )
        print( "par      ", fmt( par, max=None ) )
        par = dyn.alterParameters( par, 6, 2, 2, value=[1.0,2.0] )
        print( "par      ", fmt( par, max=None ) )
        par = dyn.alterParameters( par, 8, -1, 2 )
        print( "par      ", fmt( par, max=None ) )
        par = dyn.alterParameters( par, 6, -1, 2 )
        print( "par      ", fmt( par, max=None ) )

        fin = [0,1,2,3,4,5,-2,-1]
        print( "fin      ", fmt( fin, max=None ) )
        fin = dyn.alterFitindex( fin, 3, 1, 2 )
        print( "fin      ", fmt( fin, max=None ) )
        fin = dyn.alterFitindex( fin, 3, -1, 2 )
        print( "fin      ", fmt( fin, max=None ) )
        fin = dyn.alterFitindex( fin, 4, 1, 2 )
        print( "fin      ", fmt( fin, max=None ) )
        fin = dyn.alterFitindex( fin, 5, -1, 2 )
        print( "fin      ", fmt( fin, max=None ) )

        fin = [0,2,3,4,5,-2,-1]
        print( "fin      ", fmt( fin, max=None ) )
        fin = dyn.alterFitindex( fin, 2, 1, 2 )
        print( "fin      ", fmt( fin, max=None ) )
        fin = dyn.alterFitindex( fin, 2, -1, 2 )
        print( "fin      ", fmt( fin, max=None ) )
        fin = dyn.alterFitindex( fin, 3, 1, 2 )
        print( "fin      ", fmt( fin, max=None ) )
        fin = dyn.alterFitindex( fin, 4, -1, 2 )
        print( "fin      ", fmt( fin, max=None ) )


    def test1Model1( self ):
        print( "  Test PolynomialDynamicModel" )
        m = PolynomialDynamicModel( 0 )
        self.growshrink( m, dnp=1 )

    def test1Model2( self ):
        print( "  Test HarmonicDynamicModel" )
        m = HarmonicDynamicModel( 1 )
        self.growshrink( m, dnp=2 )

    def test1Model3( self ):
        print( "  Test RepeatingModel 3" )
        m = GaussModel()
        r = RepeatingModel( 1, m  )
        rc = r.copy()

        self.growshrink( rc, dnp=3 )

    def test1Model4( self ):
        print( "  Test RepeatingModel 4" )
        m = GaussModel()
        r = RepeatingModel( 1, m, same=[2]  )
        self.assertTrue( isinstance( r.growPrior, ExponentialPrior ) )

        rc = r.copy()
        self.assertTrue( isinstance( rc.growPrior, ExponentialPrior ) )

        self.assertTrue( rc.same[0] == 2 )
        self.assertTrue( len( rc.same ) == 1 )

        self.assertTrue( rc.index[0] == 0 )
        self.assertTrue( rc.index[1] == 1 )
        self.assertTrue( len( rc.index ) == 2 )

        Tools.printclass( r )

        self.assertTrue( r.grow() )
        self.assertTrue( r.npbase == 5 )
        self.assertTrue( r.shrink() )
        self.assertTrue( r.npbase == 3 )
        r.shrink()
        self.assertTrue( r.npbase == 0 )
        r.grow()
        self.assertTrue( r.npbase == 3 )


        rc.grow()
        rc.grow()
        self.assertTrue( rc.npbase == 7 )
        self.assertTrue( rc.ncomp == 3 )

    def test1Model5( self ):
        print( "  Test RepeatingModel 6" )
        m = GaussModel()
        r = RepeatingModel( 1, m, same=2, minComp=1, maxComp=3  )

        pars = numpy.asarray( [1.0, -0.4, 0.1] )
        self.assertTrue( isinstance( r.growPrior, UniformPrior ) )
        self.assertTrue( r.grow() )
        self.assertTrue( r.npbase == 5 )

        pars = numpy.asarray( [1.0, -0.4, 0.1, 0.5, 0.0] )
        self.assertTrue( r.grow() )
        self.assertTrue( r.npchain == 7 )

        pars = numpy.asarray( [1.0, -0.4, 0.1, 0.5, 0.0, 0.3, 0.4] )
        self.assertFalse( r.grow() )
        self.assertTrue( r.npbase == 7 )

        pars = numpy.asarray( [1.0, -0.4, 0.1, 0.5, 0.0, 0.3, 0.4] )

        ## location is removed in BirthEngine, normally
        del( r.location )
        stdModeltest( r, pars )


        r.parameters = pars
        print( r.parameters )
        self.assertTrue( r.shrink() )
        self.assertTrue( r.npbase == 5 )
        print( r.parameters )

        self.assertTrue( r.shrink() )
        self.assertTrue( r.npbase == 3 )
        print( r.parameters )

        self.assertFalse( r.shrink() )
        self.assertTrue( r.npbase == 3 )
        print( r.parameters )

    def test1Model6( self ):
        print( "  Test RepeatingModel 6" )
        m = GaussModel()
        r = RepeatingModel( 1, m, same=[2], minComp=1, maxComp=1  )
        self.assertFalse( r.isDynamic() )
        self.assertFalse( r.grow() )
        self.assertTrue( r.npbase == 3 )
        self.assertFalse( r.shrink() )
        self.assertTrue( r.npbase == 3 )

        p = RepeatingModel( 1, m, same=[2], dynamic=False  )
        self.assertFalse( p.isDynamic() )
        self.assertFalse( p.grow() )
        self.assertTrue( p.npbase == 3 )
        self.assertFalse( p.shrink() )
        self.assertTrue( p.npbase == 3 )

    def test1Model7( self ):
        print( "  Test RepeatingModel 7" )
        m = GaussModel()
        r = RepeatingModel( 1, m, minComp=1, maxComp=3  )

        self.assertTrue( isinstance( r.growPrior, UniformPrior ) )
        self.assertTrue( r.grow() )
        self.assertTrue( r.npbase == 6 )
        self.assertTrue( r.grow() )
        self.assertTrue( r.npchain == 9 )

        pars = numpy.asarray( [1.0, 0.1, 0.01, 2.0, 0.2, 0.02, 3.0, 0.3, 0.03] )

        r.parameters = pars
        print( r.parameters )
        self.assertTrue( r.shrink() )
        self.assertTrue( r.npbase == 6 )
        print( r.parameters )
        self.assertTrue( r.shrink() )
        self.assertTrue( r.npbase == 3 )
        print( r.parameters )


    def test1Model8( self ):
        print( "  Test RepeatingModel 8" )
        m = GaussModel()
        r = RepeatingModel( 3, m )

        pars = numpy.arange( 9, dtype=float )
        rng = numpy.random.RandomState( 12345 )
        pars = r.shuffle( pars, 0, 9, rng )
        print( pars )
        p0 = pars[0]
        for k,p in enumerate( pars[1:] ) :
            self.assertTrue( p == p0+1 or k%3 == 2 )
            p0 = p

        pars = numpy.arange( 12, dtype=float )
        rng = numpy.random.RandomState( 12345 )
        pars = r.shuffle( pars, 2, 9, rng )
        print( pars )
        self.assertTrue( pars[0]==0 and pars[1]==1 and pars[-1]==11 )

    def test1Model9( self ):
        print( "  Test RepeatingModel 9" )
        m = GaussModel()
        r = RepeatingModel( 3, m, same=1 )

        pars = numpy.array( [0,1,2,3,5,6,8], dtype=float )
        rng = numpy.random.RandomState( 12345 )
        pars = r.shuffle( pars, 0, 7, rng )
        print( pars )
        self.assertTrue( pars[1] == 1 )
        self.assertTrue( pars[2] == pars[0]+2 )
        self.assertTrue( pars[4] == pars[3]+2 )
        self.assertTrue( pars[6] == pars[5]+2 )


        pars = numpy.array( [0,1,2,3,4,5,7,8,10,11], dtype=float )
        rng = numpy.random.RandomState( 12345 )
        pars = r.shuffle( pars, 2, 7, rng )
        print( pars )
        self.assertTrue( pars[0]==0 and pars[1]==1 and pars[-1]==11 )
        self.assertTrue( pars[3] == 3 )
        self.assertTrue( pars[4] == pars[2]+2 )
        self.assertTrue( pars[6] == pars[5]+2 )
        self.assertTrue( pars[8] == pars[7]+2 )

    def test1Model10( self ):
        print( "  Test SplinesDynamicModel" )
        knots = numpy.linspace( 0, 1, 3 )
        m = SplinesDynamicModel( knots=knots )
        m.setLimits( [-10.0], [10.0] )
        m.parameters = numpy.arange( m.npars, dtype=float )
        rng  = numpy.random.RandomState( 123456 )
        m = self.growshrink( m, dnp=1, npf=4, rng=rng, prnt=True )

        print( "Change Structure" )
        for k in range( 6 ) :
            m.vary( rng=rng )
            self.report( m, prnt=True )

        cm = m.copy()
        Tools.printclass( cm )

    def test1Model11( self ):
        print( "  Test SplinesDynamicModel shrink" )
        xx = numpy.linspace( 0, 10, 501, dtype=float )
        kn1 = numpy.linspace( 0, 10, 16, dtype=float )
        m1 = BasicSplinesModel( knots=kn1 )
        p1 = numpy.zeros( 18, dtype=float )
        p1[7:9] = 1.0

        kn2 = numpy.append( numpy.append( kn1[:7], [5.0] ), kn1[9:] )
        m2 = BasicSplinesModel( knots=kn2 )
        p2 = numpy.zeros( 17, dtype=float )
        p2[7] = 1.4
        print( fmt( kn1, max=None ) )
        print( fmt( kn2, max=None ) )


        if self.doplot :
            plt.plot( xx, m1.result( xx, p1 ) )
            plt.plot( xx, m2.result( xx, p2 ) )
            plt.show()


    def constrainPos( self, logL, problem, allpars, logLlow ):
        xx = numpy.arange( 101, dtype=float )
        yy = problem.model.result( xx, allpars )
        if numpy.any( yy < 0 ):
            return logLlow - 1
        else :
            return logL

    def testNS( self ) :
        ky = numpy.arange( 100, dtype=int )
        py = numpy.asarray( [0,0,0,0.3,0.5,1.1,3.9,13.4,20.6,23.1] )

        perc = py[ ky // 10 ]
        year = numpy.asarray( ky, dtype=float )

        print( "  Test SplinesDynamicModel in NestedSampler" )

        # We need initial knot settings
        knots =[0, 50, 100]

        mdl = SplinesDynamicModel( knots=knots, maxKnots=5 )
        mdl.setLimits( lowLimits=[-20.0,-20.0], highLimits=[+30.0,30.0] )

        ns = NestedSampler( year, mdl, perc, seed=1234 )
        ns.distribution.setLimits( [0.01,100] )
        ns.distribution.constrain = self.constrainPos
        ns.verbose = 2
        evid = ns.sample( plot=self.doplot )

        sl = ns.samples
        ay = numpy.linspace( 0, 100, 101, dtype=float )
        res = sl.average( ay )
        self.assertTrue( all( res >= 0 ) )


    def growshrink( self, m0, dnp=1, npf=0, rng=None, prnt=False ) :
        Tools.printclass( m0 )

        self.assertTrue( m0.npchain == npf + dnp )
        self.assertTrue( m0.npbase == npf + dnp )
        self.report( m0, prnt=prnt )

        npf += dnp
        m = m0.copy()
        if m.grow( rng=rng ) :
            self.report( m, prnt=prnt )
            m0 = m
            npf += dnp
        else :
            print( "grow   failed" )

        m = m0.copy()
        if m.grow( rng=rng ) :
            self.report( m, prnt=prnt )
            m0 = m
            npf += dnp
        else :
            print( "grow   failed" )

        m = m0.copy()
        if m.grow( rng=rng ) :
            self.report( m, prnt=prnt )
            m0 = m
            npf += dnp
        else :
            print( "grow   failed" )

        print( m.npchain, m.npbase, m.npmax, npf )
        self.assertTrue( m.npchain == npf )
        self.assertTrue( m.npbase == npf )

        m = m0.copy()
        if m.grow( rng=rng ) :
            self.report( m, prnt=prnt )
            m0 = m
            npf += dnp
        else :
            print( "grow   failed" )

        m = m0.copy()
        if m.shrink( rng=rng ) :
            self.report( m, prnt=prnt )
            m0 = m
            npf -= dnp
        else :
            print( "shrink failed" )

        self.assertTrue( m.npchain == npf )
        self.assertTrue( m.npbase == npf )

        m = m0.copy()
        if m.shrink( rng=rng ) :
            self.report( m, prnt=prnt )
            m0 = m
            npf -= dnp
        else :
            print( "shrink failed" )

        self.assertTrue( m.npchain == npf )
        self.assertTrue( m.npbase == npf )

        m = m0.copy()
        if m.grow( rng=rng ) :
            self.report( m, prnt=prnt )
            m0 = m
            npf += dnp
        else :
            print( "grow   failed" )

        m = m0.copy()
        if m.grow( rng=rng ) :
            self.report( m, prnt=prnt )
            m0 = m
            npf += dnp
        else :
            print( "grow   failed" )

        return m

    def report( self, m, prnt=False ) :
        if prnt :
            print( "Knots  ", fmt( m.knots, max=None ) )
            print( "Param  ", fmt( m.parameters, max=None ) )

    def test2Model( self ):
        print( "========================" )
        print( "  Test two models" )
        print( "========================" )

        self.assertRaises( ValueError, PolynomialDynamicModel, 0, minDegree=2, maxDegree=4 )

        m = GaussModel( )
        p = PolynomialDynamicModel( 1, minDegree=1, maxDegree=4 )

        print( m.isDynamic(), p.isDynamic() )

        print( p.growPrior )
        m += p

        self.assertTrue( m.isDynamic() )
        self.assertFalse( isinstance( m, Dynamic ) )
        self.assertTrue( isinstance( m._next, Dynamic ) )

        lolim = [-10, -1, 0, -10]
        hilim = [+10, +1, 10, 10]
        m.setLimits( lowLimits=lolim, highLimits=hilim )
        Tools.printclass( m )
        Tools.printclass( p )

        par = numpy.asarray( [1,-0.2,0.3,-1.2,0.2] )
        x = numpy.linspace( -1.0, 1.0, 11 )
        y = numpy.linspace( 0.0, 2.3, 11 )

        problem = ClassicProblem( model=m, xdata=x, ydata=y )

        print( problem.myEngines() )
        print( problem.myStartEngine() )
        print( problem.myDistribution() )

        self.assertTrue( "galilean" in problem.myEngines() )
        self.assertTrue( "birth" in problem.myEngines() )
        self.assertTrue( "death" in problem.myEngines() )

        errdis = GaussErrorDistribution( limits=[0.01,100] )

        allpars = numpy.append( par, [1.0] )
        fitIndex = [0,1,2,3,4,-1]
        sl = WalkerList( problem, 10, allpars, fitIndex )

        print( m.npchain, m.npbase, m._next.npbase, len( allpars ) )
        print( "====================" )

        seng = StartEngine( sl, errdis )
        for k, s in enumerate( sl ) :
            print( "Walker  ", s.id, s.problem.npars, s.problem.model.npars, s.problem.model.npchain )
            seng.execute( k, 0.0 )

        logl = sl.getLogLikelihoodEvolution()
        lowl = numpy.min( logl )
        print( "logl  ", fmt( logl, max=None ) )
        print( "lowl  ", fmt( lowl ) )

        beng = BirthEngine( sl, errdis )
        deng = DeathEngine( sl, errdis )
        print( "start  np ", m.npchain )
        for k, s in enumerate( sl ) :
            Tools.printclass( s )
            suc = beng.execute( k, lowl )
            print( "Birth  ", suc, s.problem.npars, s.problem.model.npars, s.problem.model.npchain )
            Tools.printclass( s )
            suc = deng.execute( k, lowl )
            print( "Death  ", suc, s.problem.npars, s.problem.model.npars, s.problem.model.npchain )


    def testNestedSampler( self ) :
        print( "========================" )
        print( "  Test Nested Sampler" )
        print( "========================" )

        numpy.random.seed( 1315 )
        N = 21
        x = numpy.linspace( -2.0, 3.0, N, dtype=float )
        y = 1.2 + 0.5 * x + 0.33 * x * x + 0.27 * x * x * x
        noise = numpy.random.randn( N )
        y += 0.02 * noise

        pm = PolynomialDynamicModel( 0 )
        lolim = [-10]
        hilim = [+10]
        pm.setLimits( lowLimits=lolim, highLimits=hilim )
        Tools.printclass( pm )

        engines = None
        ns = NestedSampler( x, pm, y, seed=2031967, engines=engines )

        ns.distribution.setLimits( [0.01, 100] )

        logE = ns.sample( plot=self.doplot )


    def testNestedSampler2( self ) :
        print( "========================" )
        print( "  Test Nested Sampler 2" )
        print( "========================" )

        numpy.random.seed( 1315 )
        N = 40
        x = numpy.arange( N, dtype=float ) / 10
        y = [0, 1, 3, 4, 6, 7, 5, 8, 9, 2, -2,-9,-8,-5,-7,-6,-4,-3,-1, 0] * 2
        y - numpy.asarray( y, dtype=float )
#        y = numpy.linspace( 0.0, 4.0, N, dtype=float ) % 2
        noise = numpy.random.randn( N )
        y += 0.3 * noise

        pm = HarmonicDynamicModel( 1, period=2.0 )
        pm.growPrior.scale = 6

        lolim = [-10]
        hilim = [+10]
        pm.setLimits( lowLimits=lolim, highLimits=hilim )
        Tools.printclass( pm )

        ns = NestedSampler( x, pm, y, seed=2031967 )
#        ns.verbose = 4

        ns.distribution.setLimits( [0.01, 100] )
#        ns.distribution.scale = 0.02

        logE = ns.sample( plot=self.doplot )
        print( "scale  ", ns.scale )

    def testNestedSampler3( self ) :
        print( "========================" )
        print( "  Test Nested Sampler 3" )
        print( "========================" )

        numpy.random.seed( 1315 )
        N = 200
        x = numpy.arange( N, dtype=float ) / 40
        y = 0.1 * numpy.random.randn( N )
        gm = GaussModel()
        for k in range( 1, 6 ) :
            par = [5.0/k, k-0.5, 0.1]
            y += gm.result( x, par )

        pm = RepeatingModel( 1, gm )
        pm.growPrior.scale = 5
        lolim = [0.0,0.0,0.0]
        hilim = [+10,5.0,1.0]
        pm.setLimits( lowLimits=lolim, highLimits=hilim )
        Tools.printclass( pm )

        ns = NestedSampler( x, pm, y, seed=2031967 )
        ns.distribution.setLimits( [0.01, 100] )
#        ns.distribution.scale = 0.02

        logE = ns.sample( plot=self.doplot )
        sl = ns.samples
        print( "maxlik   ", fmt( sl.maxLikelihoodParameters, max=None ) )
        print( "median   ", fmt( sl.medianParameters, max=None ) )
        print( "modus    ", fmt( sl.modusParameters, max=None ) )
        print( "scale    ", fmt( ns.scale ) )


    def suite( cls ):
        return unittest.TestCase.suite( TestDynamicModel.__class__ )


if __name__ == '__main__':
    unittest.main()

