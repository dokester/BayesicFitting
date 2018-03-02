# run with : python3 -m unittest TestCombiModel

import unittest
import numpy as numpy
from numpy.testing import assert_array_equal as assertAE
from numpy.testing import assert_array_almost_equal as assertAAE
from astropy import units
import math

from BayesicFitting import *
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

class TestCombiModel( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author       Do Kester

    """

    def plotall( self ) :
        self.test1()
        self.test2( plot=True )
        self.test3( plot=True )
        self.test4( plot=True )
        self.test5( plot=True )
        self.test6( plot=True )

    def test1( self ):
        print( "\n   CombiModel Test 1\n" )
        gm = GaussModel( )
        self.assertRaises( ValueError, CombiModel, gm, 3, oper="xx" )
        cm = CombiModel( gm, 3 )
        self.assertRaises( ValueError, cm.setCombi, [1,2,3] )
        self.assertRaises( ValueError, cm.setCombi, {3:[1,2,3]} )
        self.assertRaises( ValueError, cm.setCombi, {1:[1,2]} )

    def test2( self, plot=False ):
        print( "\n   CombiModel Test 2\n" )
        gm = GaussModel( )
        pars = numpy.linspace( 0.0, 1.0, 3, dtype=float )
        gm.parameters = pars

        cm = CombiModel( gm, 3 )

        self.assertTrue( cm._deep == 1 )
        print( str( cm._head ) )
        self.assertTrue( str( cm._head ) == "Combi of 3 times Gauss" )
        self.assertTrue( cm._next is None )
        self.assertTrue( cm._npchain == 9 and cm.npchain == 9 )
        assertAE( cm.addindex, [] )
        assertAE( cm.addvalue, [] )
        assertAE( cm.mulindex, [] )
        assertAE( cm.mulvalue, [] )
        assertAE( cm.expandindex, numpy.arange( 9, dtype=int ) )
        assertAE( cm.select, numpy.arange( 9, dtype=int ) )
        assertAE( cm.parameters, [0.0,0.5,1.0]*3 )
        p = numpy.ones( 9, dtype=float )
        p[1:9:3] /= 2
        p[2:9:3] /= 10
        stdModeltest( cm, p, plot=plot )

    def test3( self, plot=False ):
        print( "\n   CombiModel Test 3\n" )
        gm = GaussModel( )
        pars = numpy.linspace( 0.0, 1.0, 3, dtype=float )
        gm.parameters = pars
        cm = CombiModel( gm, 4, addCombi={1:[0,0.4,0.8,1.3], 2:[0,0,0,0]} )

        cm.xUnit = units.m
        cm.yUnit = units.kg

        p = numpy.array( [1.0, -0.6, 0.1, 1.0, 1.0, 1.0] )

        stdModeltest( cm, p, plot=plot )

    def test4( self, plot=False ):
        print( "\n   CombiModel Test 4\n" )
        gm = GaussModel( )
        pars = numpy.linspace( 0.0, 1.0, 3, dtype=float )
        gm.parameters = pars
        cm = CombiModel( gm, 4, addCombi={1:[0,0.4,0.8,1.3]}, mulCombi={2:[1,1,1,1]} )

        cm.xUnit = units.m
        cm.yUnit = units.kg

        p = numpy.array( [1.0, -0.6, 0.1, 1.0, 1.0, 1.0] )

        stdModeltest( cm, p, plot=plot )

    def test5( self, plot=False ):
        print( "\n   CombiModel Test 5\n" )
        gm = EtalonModel( )
        pars = numpy.asarray( [1.0,0.5, 10.0, 0.0], dtype=float )
        gm.parameters = pars
        cm = CombiModel( gm, 2, oper="mul", addCombi={2:[0,1]} )

        cm.xUnit = units.m
        cm.yUnit = units.kg

        p = numpy.asarray( [1.0,0.5, 10.0, 0.0, 1.0, 0.4, 0.0] )
        stdModeltest( cm, p, plot=plot )

    def test6( self, plot=False ):
        print( "\n   CombiModel Test 6\n" )
        gm = EtalonModel( )
        pars = numpy.asarray( [1.0,0.5, 10.0, 0.0], dtype=float )
        gm.parameters = pars
        cm = CombiModel( gm, 2, mulCombi={1:[1,1.4]}, addCombi={2:[0,3]} )

        cm.xUnit = units.m
        cm.yUnit = units.kg

        p = numpy.asarray( [1.0,0.5, 10.0, 0.0, 1.0, 0.4, 0.0] )

        stdModeltest( cm, p, plot=plot )



    def suite( cls ):
        return unittest.TestCase.suite( TestCombiModel.__class__ )



