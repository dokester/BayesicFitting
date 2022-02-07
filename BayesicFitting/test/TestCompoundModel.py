#run with: python3 -m unittest TestCompoundModel

import unittest
import os
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt

#from BayesicFitting import PolynomialModel, SineModel
#from Model import Model

from StdTests import stdModeltest

from BayesicFitting import formatter as fmt
from BayesicFitting import *

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
#  *    2016 Do Kester

class Test( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

    def testOperations( self ) :
        print( "  Test Operations  " )
        m = GaussModel()
        p = PolynomialModel( 2 )
        m1 = m + p
        self.assertTrue( isinstance( m1, Model ) )
        self.assertTrue( m1.npchain == 6 )

        m = GaussModel()
        p = PolynomialModel( 2 )
        m1 = m - p
        self.assertTrue( isinstance( m1, Model ) )
        self.assertTrue( m1.npchain == 6 )

        m = GaussModel()
        p = PolynomialModel( 2 )
        m1 = m * p
        self.assertTrue( isinstance( m1, Model ) )
        self.assertTrue( m1.npchain == 6 )

        m = GaussModel()
        p = PolynomialModel( 2 )
        m1 = m / p
        self.assertTrue( isinstance( m1, Model ) )
        self.assertTrue( m1.npchain == 6 )

        m = GaussModel()
        p = PolynomialModel( 2 )
        m1 = m | p
        Tools.printclass( m1 )
        self.assertTrue( isinstance( m1, Model ) )
        self.assertTrue( m1.npchain == 6 )


    def testLimits( self ) :
        m = GaussModel()
        m.setLimits( lowLimits=[-10, 5, 0], highLimits=[10, 9, 6] )
        p = PolynomialModel( 3 )
        p.setLimits( lowLimits=[-100], highLimits=[100] )
        m1 = m | p
        print( m1.npchain, m.npchain, p.npchain )
        Tools.printclass( m )
        lo = [m1.getPrior(k).lowLimit for k in range( m1.npchain )]
        print( lo )
        hi = [m1.getPrior(k).highLimit for k in range( m1.npchain )]
        print( hi )

        m1 = p + m
        lo = [m1.getPrior(k).lowLimit for k in range( m1.npchain )]
        print( lo )
        hi = [m1.getPrior(k).highLimit for k in range( m1.npchain )]
        print( hi )

        r = RepeatingModel( 3, m )
        print( r.npchain, m.npchain, m.npbase )
        self.assertTrue( r.npchain == 9 )
        self.assertTrue( r.npbase == 9 )
        self.assertTrue( r.npmax == 9 )
        self.assertTrue( r.ncomp == 3 )
        self.assertTrue( r.deltaNpar == 3 )

        Tools.printclass( r )
        for k in range( r.npchain ) :
            print( k, r.par2model( k ) )
        lo = [r.getPrior(k).lowLimit for k in range( r.npchain )]
        print( lo )
        m1 = p + r
        lo = [m1.getPrior(k).lowLimit for k in range( m1.npchain )]
        print( lo )
        hi = [m1.getPrior(k).highLimit for k in range( m1.npchain )]
        print( hi )

        r = RepeatingModel( 3, m, same=2 )
        print( r.npchain, m.npchain, m.npbase )
        self.assertTrue( r.npchain == 7 )
        self.assertTrue( r.npbase == 7 )
        self.assertTrue( r.npmax == 7 )
        self.assertTrue( r.ncomp == 3 )
        self.assertTrue( r.deltaNpar == 2 )
        Tools.printclass( r )
        for k in range( r.npchain ) :
            print( k, r.par2model( k ) )
        lo = [r.getPrior(k).lowLimit for k in range( r.npchain )]
        print( lo )
        m1 = p + r
        lo = [m1.getPrior(k).lowLimit for k in range( m1.npchain )]
        print( lo )
        hi = [m1.getPrior(k).highLimit for k in range( m1.npchain )]
        print( hi )

        m = GaussModel()
        r = RepeatingModel( 3, m, same=2 )
        r.setLimits( lowLimits=[-10, 5, 0], highLimits=[10, 9, 6] )

        print( r.npchain, m.npchain, m.npbase )
        self.assertTrue( r.npchain == 7 )
        self.assertTrue( r.npbase == 7 )
        self.assertTrue( r.npmax == 7 )
        self.assertTrue( r.ncomp == 3 )
        self.assertTrue( r.deltaNpar == 2 )
        Tools.printclass( r )
        for k in range( r.npchain ) :
            print( k, r.par2model( k ) )
        lo = [r.getPrior(k).lowLimit for k in range( r.npchain )]
        print( lo )
        m1 = p + r
        lo = [m1.getPrior(k).lowLimit for k in range( m1.npchain )]
        print( lo )
        hi = [m1.getPrior(k).highLimit for k in range( m1.npchain )]
        print( hi )

        h = HarmonicModel( 3 )
        h.setLimits( lowLimits=[-110,-111], highLimits=[110,111] )
        m1 = p + h
        lo = [m1.getPrior(k).lowLimit for k in range( m1.npchain )]
        print( lo )
        hi = [m1.getPrior(k).highLimit for k in range( m1.npchain )]
        print( hi )

        h = HarmonicDynamicModel( 3 )
        h.setLimits( lowLimits=[-110,-111], highLimits=[110,111] )
        m1 = p + h
        lo = [m1.getPrior(k).lowLimit for k in range( m1.npchain )]
        print( lo )
        hi = [m1.getPrior(k).highLimit for k in range( m1.npchain )]
        print( hi )


    def testOneModel( self ):
        print( "  Test one model" )
        m = GaussModel( )

        self.assertTrue( m.getNumberOfParameters( ) == 3 )
        self.assertTrue( m.npbase == 3 )

        par = numpy.asarray( [3,4,5], dtype=float )
        m.parameters = par

        numpy.testing.assert_array_equal( m.parameters, par )
        self.assertTrue( m.getNumberOfParameters( ) == 3 )
        self.assertTrue( m.npbase == 3 )
        numpy.testing.assert_array_equal( m.parameters, par )

        self.assertTrue( m.getNumberOfParameters( ) == 3 )
        self.assertTrue( m.npbase == 3 )
        par[1] = 10.0
        numpy.testing.assert_array_equal( m.parameters, par )

        fix = numpy.asarray( [0,1,2] )
        self.assertTrue( m.getNumberOfParameters( ) == 3 )
        self.assertTrue( m.npbase == 3 )

    def testTwoModel( self ):
        print( "  Test two models" )

        m = GaussModel( )
        p = PolynomialModel( 1 )

        m.addModel( p )

        print( m.parameters, p.parameters )


        self.assertTrue( m.getNumberOfParameters( ) == 5 )
        self.assertTrue( m.npbase == 3 )
        self.assertTrue( m._next.npbase == 2 )
        self.assertTrue( len( m.parameters ) == 5 )


        par = numpy.asarray( [1,-2,3,-1.2,0.2] )
        m.parameters = par
        print( m.parameters )
        numpy.testing.assert_array_equal( m.parameters, par )

    def testThreeModel( self ):
        print( "  Test three models" )
        m = GaussModel( )
        self.assertTrue( m.chainLength() == 1 )
        p = PolynomialModel( 1 )
        m.addModel( p )
        self.assertTrue( m.chainLength() == 2 )
        s = VoigtModel( )
        m.addModel( s )
        self.assertTrue( m.chainLength() == 3 )

        params = numpy.arange( 9, dtype=float )
        m.parameters = params

        self.assertTrue( m._next == p )
        self.assertTrue( m._next._next == s )
        self.assertTrue( p._next == s )
        self.assertTrue( s._head == m )
        self.assertTrue( p._head == m )
        self.assertTrue( m._head == m )
        self.assertTrue( m.getNumberOfParameters( ) == 9 )
        self.assertTrue( p.getNumberOfParameters( ) == 9 )
        self.assertTrue( s.getNumberOfParameters( ) == 9 )
        self.assertTrue( m.npbase == 3 )
        self.assertTrue( p.npbase == 2 )
        self.assertTrue( s.npbase == 4 )
        self.assertTrue( len( m.parameters ) == 9  )
        self.assertTrue( p.parameters is None  )
        self.assertTrue( s.parameters is None  )


        print( "Isolate second model into p1" )
        p1 = m.isolateModel( 1 )
        print( p1 )
        print( p1.parameters )
        self.assertTrue( isinstance( p1, PolynomialModel ) )

        self.assertTrue( p1._next == None )
        self.assertTrue( p1._head == p1 )
        self.assertTrue( p1.npbase == 2 )
        self.assertTrue( p1.getNumberOfParameters() == 2 )


        self.assertTrue( m._next == p )
        self.assertTrue( m._next._next == s )
        self.assertTrue( p._next == s )
        self.assertTrue( s._head == m )
        self.assertTrue( p._head == m )
        self.assertTrue( m._head == m )
        self.assertTrue( m.getNumberOfParameters( ) == 9 )
        self.assertTrue( p.getNumberOfParameters( ) == 9 )
        self.assertTrue( s.getNumberOfParameters( ) == 9 )
        self.assertTrue( m.npbase == 3 )
        self.assertTrue( p.npbase == 2 )
        self.assertTrue( s.npbase == 4 )


    def testPipe1( self ) :
        model = PolynomialModel( 2 )
        model |= SineModel()
        print( model )
        p = numpy.asarray( [0.0, 0.4, 0.2, 1.0, 0.0, 1.0] )
        x = numpy.linspace( 0, 10, 101, dtype=float )

        y = model.result( x, p )

        stdModeltest( model, p, x=x, plot=self.doplot )

    def testPipe2( self ) :
        model = PolynomialModel( 2 )
        model |= SineModel()
        model *= ExpModel()
        print( model )
        p = numpy.asarray( [0.0, 0.4, 0.2, 1.0, 0.0, 1.0, 1.3, -0.2] )
        x = numpy.linspace( 0, 10, 101, dtype=float )

        y = model.result( x, p )

        stdModeltest( model, p, x=x, plot=self.doplot )

    def testPipe3( self ) :
        model = StellarOrbitModel( )
        model |= PolySurfaceModel( 3 )

        print( model.npars )
        printclass( model )
        printclass( model._next )

        p = numpy.asarray( [0.0, 0.4, 0.2, 1.0, 0.0, 0.0, 0.4, 0.2, 1.0, 0.0, 0.0, 0.4,
                            -0.1, -0.2, 0.3, 0.0, 0.0] )
        x = numpy.linspace( 0, 10, 101, dtype=float )

        y = model.result( x, p )
        print( y.shape )
        print( fmt( y ) )
        pp = model.partial( x, p )
        print( pp.shape )
        print( fmt( pp ) )
        dd = model.derivative( x, p )
        print( dd.shape )
        print( fmt( dd ) )

        stdModeltest( model, p, x=x, plot=self.doplot )


    def testThreeModelLimits( self ):
        print( "  Test three models: limits and domain <> unit" )

        m = GaussModel( )
        p = PolynomialModel( 1 )
        m.addModel( p )
        s = VoigtModel( )
        m.addModel( s )

        print( m.npchain )

        lo = numpy.zeros( 9 )
        hi = numpy.arange( 9 ) + 10.0
        m.setLimits( lo, hi )

        par = numpy.arange( 9, dtype=float )
        unp = m.domain2Unit( par )
        print( fmt( par, max=None ) )
        print( fmt( lo, max=None ) )
        print( fmt( hi, max=None ) )
        print( fmt( unp, max=None ) )
        print( fmt( par / hi, max=None ) )
        print( fmt( m.unit2Domain( unp ), max=None ) )
        print( fmt( m.partialDomain2Unit( par ), max=None ) )

        numpy.testing.assert_array_almost_equal( m.unit2Domain( unp ), par, 8 )
        self.assertTrue( m.domain2Unit( par[2], 2 ) == unp[2] )
        self.assertTrue( m.domain2Unit( par[3], 3 ) == unp[3] )
        self.assertTrue( m.domain2Unit( par[6], 6 ) == unp[6] )

    def testTwoModelDerivatives( self ):
        print( "  Test two model derivatives" )
        m = GaussModel( )
        m.addModel( PolynomialModel(1) )
        p = numpy.asarray( [1,-2,3,-1.2,0.2] )
        x = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )

        print( m )
        m.testPartial( x[3], p )

        part = m.partial( x, p )
        nump = m.numPartial( x, p )
        numpy.testing.assert_array_almost_equal( part, nump, 4 )

        mc = m.copy( )
        self.assertTrue( mc.getNumberOfParameters( ) == 5 )
        self.assertTrue( mc.getNumberOfFittedParameters( ) == 5 )

        mc.parameters = p
        m.parameters = p

        numpy.testing.assert_array_equal( m.result( x ), mc.result( x ) )

        m.addModel( GaussModel() )
        m.parameters =  numpy.asarray( [1,-2,3,1,-2,2,2,3], dtype=float )
        self.assertTrue( m.parameters[2] > 0 )
        self.assertTrue( m.parameters[7] > 0 )
        m.parameters = numpy.asarray( [1,-2,-3,1,-2,2,2,-3], dtype=float )
        m.result( x )
        self.assertTrue( m.parameters[2] > 0 )
        self.assertTrue( m.parameters[7] > 0 )
        m.parameters = numpy.asarray( [1,-2,0,1,-2,2,2,0], dtype=float )
        self.assertWarns( UserWarning, m.result, x )
        self.assertTrue( m.parameters[2] == m.tiny )
        self.assertTrue( m.parameters[7] == m.tiny )
        m.result( x )

    def testTwoModelSubtractDerivatives( self ):
        print( "  Test two model subtract derivatives" )
        m = GaussModel( )
        m.subtractModel( PolynomialModel(1) )
        p = numpy.asarray( [1,-2,3,-1.2,0.2] )
        x = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )

        print( m )
        m.testPartial( x[3], p )

        part = m.partial( x, p )
        nump = m.numPartial( x, p )
        numpy.testing.assert_array_almost_equal( part, nump, 4 )

        mc = m.copy( )
        self.assertTrue( mc.getNumberOfParameters( ) == 5 )

        mc.parameters = p
        m.parameters = p

        numpy.testing.assert_array_equal( m.result( x ), mc.result( x ) )

    def testTwoModelDerivatives( self ):
        print( "  Test two model multiply derivatives" )
        m = GaussModel( )
        m.multiplyModel( PolynomialModel(1) )
        p = numpy.asarray( [1,-2,3,-1.2,0.2] )
        x = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )

        print( m )
        m.testPartial( x[3], p )

        part = m.partial( x, p )
        nump = m.numPartial( x, p )
        numpy.testing.assert_array_almost_equal( part, nump, 4 )

        mc = m.copy( )
        self.assertTrue( mc.getNumberOfParameters( ) == 5 )

        mc.parameters = p
        m.parameters = p

        numpy.testing.assert_array_equal( m.result( x ), mc.result( x ) )

    def testTwoModelDivideDerivatives( self ):
        print( "  Test two model divide derivatives" )
        m = GaussModel( )
        m.divideModel( PolynomialModel(1) )
        p = numpy.asarray( [1,-2,3,-1.2,0.2] )
        x = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )

        print( m )
        m.testPartial( x[3], p )

        part = m.partial( x, p )
        nump = m.numPartial( x, p )
        numpy.testing.assert_array_almost_equal( part, nump, 4 )

        mc = m.copy( )
        self.assertTrue( mc.getNumberOfParameters( ) == 5 )

        mc.parameters = p
        m.parameters = p

        numpy.testing.assert_array_equal( m.result( x ), mc.result( x ) )

    def testModelName( self ):
        print( "  Test model names" )

        pm = PolynomialModel( 2 )
        gm = GaussModel( fixed={0:pm} )
        sm = SineModel()
        m1 = gm / sm
        self.assertTrue( gm.npbase == 5 )
        self.assertTrue( m1.npchain == 8 )
        print( '-------------------------------------------------------------' )
        print( m1 )

        print( '-------------------------------------------------------------' )
        print( m1._toString( "toS   ", npars=2 ) )

        sm = SplinesModel( [0,1,2] )
        pm = PolynomialModel( 0 )
        lm = LorentzModel( )
        m3 = sm + lm + pm
        print( '-------------------------------------------------------------' )
        print( m3 )




        em = PowerModel( 1, fixed={0:1.0} )
        em += BasicSplinesModel( nrknots=8, min=0, max=10 )
        em += ExpModel()
        m2 = em | m1
        self.assertTrue( em.npbase == 0 )
        self.assertTrue( em.npchain == 12 )
        self.assertTrue( m2.npchain == 20 )
        print( '-------------------------------------------------------------' )
        m2str = m2.__str__()
        print( m2str )

        self.assertTrue( m2str[-30:] == "p_19 * sin( 2PI * x * p_17 ) }" )

        for k in range( m2.npchain ) :
            print( fmt( k ), "%-13.13s"%m2.getParameterName(k), fmt( m2[k] ) )







    def suite( cls ):
        return unittest.TestCase.suite( CompoundModelTest.__class__ )


if __name__ == '__main__':
    unittest.main()

