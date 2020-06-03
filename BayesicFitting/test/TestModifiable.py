#run with: python3 -m unittest TestModifiable

import unittest
import os
import numpy as numpy
from astropy import units
import math

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

        t = numpy.linspace( 0, 100, 201, dtype=float )
        y = numpy.sin( 2 * math.pi * numpy.exp( t / 150 ) )

        knots =[0, 25, 50, 75, 100]

        mdl = SplinesDynamicModel( knots=knots, dynamic=False )
        mdl.setLimits( lowLimits=[-2.0], highLimits=[+2.0] )

        engs = ["galilean", "struct"]

        ns = NestedSampler( t, mdl, y, seed=1234, engines=engs )
        ns.distribution.setLimits( [0.01,100] )
        ns.verbose = 2

        evid = ns.sample( plot=self.doplot )

        if not self.doplot : return

        cc = ['k,', 'b,', 'r,', 'g,', 'c,', 'm,']
        sl = ns.samples
        ka = numpy.zeros( ( 5, len( sl ) ), dtype=float )
        for k,s in enumerate( sl ) :
            ka[:,k] = s.model.knots
        for j in range( len( knots ) ) :
            plt.plot( ka[j,:]. cc[j] )
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


    def suite( cls ):
        return unittest.TestCase.suite( TestModifiable.__class__ )


if __name__ == '__main__':
    unittest.main()

