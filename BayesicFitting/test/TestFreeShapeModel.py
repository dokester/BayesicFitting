# run with : python3 -m unittest TestFreeShapeModel

import unittest
import os
import numpy as numpy
from astropy import units
import matplotlib.pyplot as plt
import warnings

from StdTests import stdModeltest

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
#  *  2006 Do Kester

class TestFreeShapeModel( unittest.TestCase ):
    """
    Test harness for Models

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )



    def test1( self ):
        x  = numpy.linspace( 0, 10, 101, dtype=float )
        x += 0.01           ## avoid awkward non-continuities
        print( "****** FREESHAPE test 1 ********************" )
        m = FreeShapeModel( 10 )
        self.assertTrue( m.npbase == 10 )
        p = numpy.asarray( [1.2,0.2,1.0,0.5,0.3,1.2,0.2,1.0,0.5,0.3] )

        stdModeltest( m, p, x=x, plot=self.doplot )

    def test2( self ):
        x  = numpy.linspace( 0, 10, 101, dtype=float )
        x += 0.01           ## avoid awkward non-continuities
        print( "****** FREESHAPE test 2 ********************" )
        m = FreeShapeModel( 10, nconvolve=3, center=0.0 )
        p = numpy.asarray( [1.2,0.2,1.0,0.5,0.3,1.2,0.2,1.0,0.5,0.3] )

        stdModeltest( m, p, x=x, plot=self.doplot )

    def xtest3( self ):
        x  = numpy.arange( 21, dtype=float )
        print( "****** FREESHAPE test 3 ********************" )
        m = FreeShapeModel( 8, convolve=4 )
        print( m.npbase )
        self.assertTrue( m.npbase == 8 )
        p = numpy.asarray( [1.2,0.2,1.1,0.5,0.3,0.1,0.4,0.2], dtype=float )

        stdModeltest( m, p, x=x, plot=self.doplot )

    def test4( self ) :
        print( "****** FREESHAPE test 4 ********************" )
        if not self.doplot :
            return

        x  = numpy.linspace( 0, 10, 101, dtype=float )
        for k in range( 7 ) :
            m = FreeShapeModel( 10, nconvolve=k, center=0.0 )
            self.assertTrue( m.npbase == 10 )
            p = numpy.asarray( [1.2,0.9,0.7,0.5,0.3,0.3,0.6,1.0,0.9,0.9] )
            plt.plot( x, m.result( x, p ) )

        plt.show()

    def test5( self ) :
        print( "****** FREESHAPE test 5 ********************" )
        if not self.doplot :
            return

        x  = numpy.linspace( 0, 10, 101, dtype=float )
        p = numpy.asarray( [1.2,0.9,0.7,0.5,0.3,0.3,0.6,1.0,0.9,0.9] )

        m0 = FreeShapeModel( 10, nconvolve=0, center=0.0 )
        m1 = FreeShapeModel( 10, nconvolve=0, center=0.5 )
        plt.plot( x, m0.result( x, p ) )
        plt.plot( x, m1.result( x, p ) )

        m0 = FreeShapeModel( 10, nconvolve=3, center=0.0 )
        m1 = FreeShapeModel( 10, nconvolve=3, center=0.5 )
        plt.plot( x, m0.result( x, p ) )
        plt.plot( x, m1.result( x, p ) )

        plt.show()

    def xtest9( self ):
        x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
        print( "****** FREESHAPE test 9 ********************" )
        m = FreeShapeModel( 15, pixperbin=3, convolve=2, xlo=-1.1, xhi=1.1 )
        print( m.npbase )
        self.assertTrue( m.npbase == 6 )
        p = numpy.asarray( [1.2,0.2,1.0,0.5,0.3,0.1,0.4], dtype=float )

        stdModeltest( m, p, plot=self.doplot )


    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestFreeShapeModels.__class__ )

if __name__ == '__main__':
    unittest.main( )


