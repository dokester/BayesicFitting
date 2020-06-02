# run with : python3 -m unittest TestBracketModel

import unittest
import os
import numpy as numpy
from numpy.testing import assert_array_equal as assertAE
from numpy.testing import assert_array_almost_equal as assertAAE
from astropy import units
import math

from BayesicFitting import *
from BayesicFitting import formatter as fmt
from StdTests import stdModeltest

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

class TestBracketModel( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )



    def testImplicit( self ) :
        print( "====  BracketModel Test =======================" )
        m1 = GaussModel( )
        m1 += PolynomialModel( 0 )              # Gauss on a constant background
        m2 = BracketModel( m1 )
        m3 = SineModel( )
        m3 *= m2                                # sine * ( gauss + const )
        print( "Explicit Use" )
        print( m3 )

        g1 = GaussModel( )
        g1 += PolynomialModel( 0 )              # m1 is a chain of models
        g3 = SineModel( )
        g3 *= g1                                # sine * ( gauss + const )
        print( "Implicit Use" )
        print( g3 )                             # exactly the same

        p = [8.0, 1.0, 0.0, 1.0, 0.0, 0.2, 1.0]
        x = numpy.asarray( [ -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )

        assertAE( g3.result( x, p ), m3.result( x, p ) )
        assertAE( g3.partial( x, p ), m3.partial( x, p ) )
        assertAE( g3.derivative( x, p ), m3.derivative( x, p ) )

        stdModeltest( g3, p, plot=self.doplot )

    def testConstantModel( self ):
        print( "====  BracketModel Test 1 =======================" )
        x = numpy.asarray( [ -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        c = ConstantModel()
        m = BracketModel( c )
        self.assertTrue( m.npbase == 0 )

        p = []
        print( m )
        print( p )
        self.assertTrue( m.testPartial( x[0], p ) == 0 )
        part = m.partial( x, p )
        print( part )
        nump = m.numPartial( x, p )
        print( nump )
        assertAE( part, numpy.ndarray( (11,0), dtype=float ) )
        assertAE( nump, numpy.ndarray( (11,0), dtype=float ) )
        mc = m.copy( )
        mc.parameters = p
        m.parameters = p
        assertAE( m.result( x ), mc.result( x ) )
        self.assertTrue( mc.priors is None )

    def testCompoundConstantModel( self ):
        print( "====  BracketModel Test 2 =======================" )
        x = [ -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        m = ConstantModel( )
        m.fixedModel.parameters= 1
        m.addModel( ExpModel() )
        self.assertTrue( m.getNumberOfParameters( ) == 2 )
        c = BracketModel( m )
        p = [-1.0,-1.0]

        stdModeltest( c, p, plot=self.doplot )

    def testFixedModel( self ):
        print( "====  BracketModel Test 3 =======================" )
        x = [ -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

        fix = {2:0.3, 4:0.01, 7:-0.002}
        pm = PolynomialModel( 8 )
        self.assertRaises( AttributeError, BracketModel, pm, fixed=fix )

    def testPolynomialModel( self ):
        print( "====  BracketModel Test 4 =======================" )
        x = [ -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

        fix = {2:0.3, 4:0.01, 7:-0.002}
        m = BracketModel( PolynomialModel( 8, fixed=fix ) )

        self.assertTrue( m.npmax == 6 )
        self.assertTrue( m.npchain == 6 )
        self.assertTrue( m.npbase == 6 )
        self.assertTrue( m.model.npmax == 9 )
        self.assertTrue( m.model.npchain == 6 )
        self.assertTrue( m.model.npbase == 6 )
        p = [1,-2,-0.2,-0.02,0.003,0.001]

        stdModeltest( m, p, plot=self.doplot )

    def testGaussPlusBackgroundModel( self ):
        print( "====  BracketModel Test 4 =======================" )
        numpy.set_printoptions( precision=3, suppress=True )
        x = [ -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

        mm = GaussModel( )
        p = [1.0, 0.0, -1.0]
        mm.parameters = p
        print( mm )
        print( fmt( mm.parameters, max=None ) )
        lm = LorentzModel()
        lm.tiny = 0.001
        mm.addModel( lm )
        p = [1.0, 0.0, -1.0, 1.0, 1.0, 0.0]
        mm.parameters = p
        print( mm )
        print( fmt( mm.parameters, max=None ) )
        mm += PolynomialModel(1)
        print( mm )
        print( fmt( mm.parameters, max=None ) )
        self.assertTrue( mm.priors is None )

        m = BracketModel( mm )
        p = [1, -2, 0, -1.2, 2, -3, -1.2, 0.2]
        hi = numpy.arange( 8, dtype=float ) + 1
        lo = - hi
        m.setLimits( lo, hi )
        print( m )
        print( m.parameters )
        self.assertTrue( m.priors is None )


        print( "pl    ", len( m.model.priors ), len( m.model._next.priors ),
                         len( m.model._next._next.priors ), m.npchain )
        (lolim,hilim) = m.getLimits()
        print( "Lolim ", lolim )
        print( "Hilim ", hilim )
        self.assertTrue( lolim[7] == -8 )
        self.assertTrue( hilim[7] == 8 )

        self.assertTrue( len( lolim ) == m.npchain )
        self.assertTrue( len( hilim ) == m.npchain )

        errors = m.testPartial( x[3], p )
        self.assertTrue( errors == 0 )
        m.parameters = p


    """
    def testGauss2DRotModel( self ):
        print( "====  BracketModel Test 5 =======================" )
        xy = numpy.asarray( [[-1.0, -0.8], [-0.6, -0.4], [-0.2, 0.0], [0.2, 0.4],
                              [0.6, 0.8]], dtype=float )
        m = BracketModel( Gauss2DRotModel() )
        p = numpy.asarray( [], dtype=float )
        print( m )
        self.assertTrue( m.testPartial( self.xy.get(1).toArray( ), p ) == 0 )
        part = m.partial( self.xy, p )
        nump = m.numPartial( self.xy, p )
        assertTrue( self.assertAAE(part, nump, 4) )
        mc = m.copy( )
        mc.parameters = p
        m.parameters = p
        assertTrue( self.assertAE( m.result(self.xy ), mc.result( self.xy ) ) )
        m.parameters = numpy.asarray( [], dtype=float )
        self.assertTrue( m.getParameters().get(3 ) > 0 )
        self.assertTrue( m.getParameters().get(4 ) > 0 )
        m.parameters = numpy.asarray( [], dtype=float )
        self.assertTrue( m.getParameters().get(3 ) > 0 )
        self.assertTrue( m.getParameters().get(4 ) > 0 )
    """

    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestBracketModel.__class__ )


