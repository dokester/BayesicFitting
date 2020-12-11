#run with: python3 -m unittest TestModifiable

import unittest
import os
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt

#from StdTests import stdModeltest

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

class TestModifiable( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

    def test1( self ) :
        print( "  Test Splines" )

        t = numpy.linspace( 0, 100, 201, dtype=float )
        y = numpy.sin( 2 * math.pi * numpy.exp( t / 150 ) )

        knots =[0, 25, 50, 75, 100]

        mdl = BasicSplinesModel( knots=knots )
        mdl.setLimits( lowLimits=[-2.0], highLimits=[+2.0] )

        engs = ["galilean", "chord"]

        ns = NestedSampler( t, mdl, y, seed=1234, engines=engs )
        ns.distribution.setLimits( [0.01,100] )
        ns.verbose = 2

        evid = ns.sample( plot=self.doplot )

    def test2( self ) :
        print( "  Test Modifiable Splines" )

#        t = numpy.linspace( 0, 100, 201, dtype=float )
        t = numpy.linspace( 0, 100, 41, dtype=float )
        y = numpy.sin( 2 * math.pi * numpy.exp( t / 70 ) )

        knots =[0, 10, 25, 40, 50, 60, 75, 100]

        mdl = SplinesDynamicModel( knots=knots, dynamic=False )
        mdl.setLimits( lowLimits=[-2.0], highLimits=[+2.0] )

        engs = ["galilean", "struct"]

        ns = NestedSampler( t, mdl, y, seed=31234, engines=engs )
        ns.distribution.setLimits( [0.01,100] )
        ns.verbose = 2
#        ns.engines[1].slow = 5

        evid = ns.sample( plot=self.doplot )

        if not self.doplot : return

        cc = ['k,', 'b,', 'r,', 'g,', 'c,', 'm,']
        sl = ns.samples
        ka = numpy.zeros( ( len( knots ), len( sl ) ), dtype=float )
        for k,s in enumerate( sl ) :
            ka[:,k] = s.model.knots
        for j in range( len( knots ) ) :
            plt.plot( ka[j,:], cc[j % 6] )
        plt.show()

    def test3( self ) :
        print( "  Test Dynamic Splines" )

        t = numpy.linspace( 0, 100, 201, dtype=float )
        y = numpy.sin( 2 * math.pi * numpy.exp( t / 150 ) )

        knots =[0, 25, 50, 75, 100]

        mdl = SplinesDynamicModel( knots=knots )
        mdl.setLimits( lowLimits=[-2.0], highLimits=[+2.0] )

#        engs = ["galilean", "chord", "struct"]
        engs = ["galilean", "birth", "death", "struct"]

        ns = NestedSampler( t, mdl, y, seed=1234, engines=engs )
        ns.distribution.setLimits( [0.01,100] )
        ns.verbose = 2

        evid = ns.sample( plot=self.doplot )

    def test4( self ) :
        print( "  Test Modifiable Splines compound" )

        NP = 41
        t = numpy.linspace( 0, 100, NP, dtype=float )
        dt = GaussModel().result( t, [10.0, 34, 10] )

        ym = numpy.sin( 0.1 * ( t + dt ) )
        y = ym + 0.1 * numpy.random.randn( NP )

        knots =[0, 25, 50, 75, 100]
        xm = SplinesDynamicModel( knots=knots, dynamic=False )
        xm += PowerModel( 1, fixed={0:1.0} )
        xm.setPrior( 0, LaplacePrior( center=0, scale=4 ) )

        sm = SineModel()
        sm.setLimits( lowLimits=[-2.0], highLimits=[+2.0] )

        mdl = xm | sm

        ns = NestedSampler( t, mdl, y, seed=31234 )
        ns.distribution.setLimits( [0.01,100] )
        ns.verbose = 2
#        ns.engines[2].verbose = 5
        ns.engines[2].slow = 5

        evid = ns.sample( plot=self.doplot )

        if not self.doplot : return

        cc = ['k,', 'b,', 'r,', 'g,', 'c,', 'm,']
        sl = ns.samples
        yfit = numpy.zeros( NP, dtype=float )
        for s in sl :
            knts = s.model.knots
            yft = BasicSplinesModel( knts ).result( t, s.parameters[:7] )
            yfit += yft * s.weight
        plt.plot( t, yfit, 'b-' )
        plt.plot( t, ns.yfit, 'g-' )
        plt.plot( t, y, 'k.' )
        plt.show()


    def suite( cls ):
        return unittest.TestCase.suite( TestModifiable.__class__ )


if __name__ == '__main__':
    unittest.main()

