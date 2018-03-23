# run with : python3 -m unittest TestKernel2dModel

import unittest
import numpy as numpy
from astropy import units
import math
from numpy.testing import assert_array_almost_equal as assertAAE

from BayesicFitting import formatter as fmt
from BayesicFitting import *

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
#  *  2006 - 2014 Do Kester, SRON (Java code)
#  *  2017        Do Kester


class TestKernel2dModel( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author       Do Kester

    """

    #      * Define x independent variable

    def __init__( self, name ):
        super( TestKernel2dModel, self ).__init__( name )

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def testKernel2dModelDefault( self ):
        print( "*******************************************************" )
        print( "*  Kernel2dModel Circular Gauss                       *" )
        print( "*******************************************************" )

        m = Kernel2dModel( )
        self.assertTrue( m.npchain, 4 )

        x1 = numpy.arange( 101, dtype=float ) / 25.0 - 2.02

        x = x1.copy()
        x = numpy.append( x, x1 + 0.01, 0 ).reshape( 101, 2 )
        print( fmt( x ) )

        p = m.parameters
        print( m )
        print( x[40,:] )
        m.testPartial( [x[40,:]], p )

        for k in range( 4 ) :
            print( "%d  %-12s %-12s"%(k, m.getParameterName(k), m.getParameterUnit( k ) ))

        p = numpy.asarray( [1.0,1.01,3.0,1.2], dtype=float )
        part = m.partial( x, p )
        nump = m.numPartial( x, p )
        assertAAE( part, nump, 4 )
        mc = m.copy( )
        mc.parameters = p
        m.parameters = p
        assertAAE( m.result(x ), mc.result( x ) )
        self.assertTrue( isinstance( mc.kernel, Gauss ) )

    def testKernel2dModelCosine( self ):
        print( "*******************************************************" )
        print( "*  Kernel2dModel Elliptic Cosine                      *" )
        print( "*******************************************************" )

        m = Kernel2dModel( kernel=Cosine(), shape=2 )
        self.assertTrue( m.npchain, 5 )

        x1 = numpy.arange( 101, dtype=float ) / 25.0 - 2.02

        x = x1.copy()
        x = numpy.append( x, x1 + 0.01, 0 ).reshape( 101, 2 )

        p = m.parameters
        print( m )
        m.testPartial( [[0.1,0.2]], p )

        for k in range( m.npbase ) :
            print( "%d  %-12s %-12s"%(k, m.getParameterName(k), m.getParameterUnit( k ) ))

        p = numpy.asarray( [1.0,1.01,3.0,1.2,2.0], dtype=float )
        part = m.partial( x, p )
        nump = m.numPartial( x, p )
        assertAAE( part, nump, 4 )
        mc = m.copy( )
        mc.parameters = p
        m.parameters = p
        assertAAE( m.result(x ), mc.result( x ) )
        self.assertTrue( isinstance( mc.kernel, Cosine ) )


    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestKernel2dModel.__class__ )


if __name__ == '__main__':
    unittest.main()


