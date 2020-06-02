# run with : python3 -m unittest TestOrthonormalBasis

import unittest
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt
from numpy.testing import assert_array_almost_equal as assertAAE

from BayesicFitting import *
from BayesicFitting import formatter as fmt

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

class TestOrthonormalBasis( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author       Do Kester

    """
    def __init__( self, name ):
        super( TestOrthonormalBasis, self ).__init__( name )


    def testbasis( self ) :
        """
        Numeric values from
        http://www.ecs.umass.edu/ece/ece313/Online_help/gram.pdf

        """

        print( "===== orthonormal basis ================" )

        onb = OrthonormalBasis()

        a1 = numpy.array( [1,0,2,1], dtype=float )
        u1 = onb.normalise( a1 )
        print( "vector  ", fmt( a1 ) )
        print( "ortnor  ", fmt( u1 ) )
        print( "basis  ", fmt( onb.basis, indent=8 ) )
        print( "" )
        assertAAE( u1, a1 / math.sqrt( 6 ) )

        a2 = numpy.array( [2,2,3,1], dtype=float )
        u2 = onb.normalise( a2 )
        print( "vector  ", fmt( a2 ) )
        print( "ortnor  ", fmt( u2 ) )
        print( "basis  ", fmt( onb.basis, indent=8 ) )
        print( "" )
        assertAAE( u2, numpy.array( [1,4,0,-1] ) / ( 3 * math.sqrt( 2 ) ) )

        a3 = numpy.array( [1,1,0,1], dtype=float )
        u3 = onb.normalise( a3 )
        print( "vector  ", fmt( a3 ) )
        print( "ortnor  ", fmt( u3 ) )
        print( "basis  ", fmt( onb.basis, indent=8 ) )
        print( "" )
        assertAAE( u3, numpy.array( [4,1,-6,8] )/ math.sqrt( 117 ) )

        a4 = numpy.array( [2,1,0,1], dtype=float )
        u4 = onb.normalise( a4 )
        print( "vector  ", fmt( a4 ) )
        print( "ortnor  ", fmt( u4 ) )
        print( "basis  ", fmt( onb.basis, indent=8 ) )
        print( "" )
#        assertAAE( u4, numpy.array( [4,1,-6,8] )/ math.sqrt( 117 ) )

        b = onb.basis
        assertAAE( numpy.inner( b[0,:], b[1,:] ), 0.0 )
        assertAAE( numpy.inner( b[0,:], b[2,:] ), 0.0 )
        assertAAE( numpy.inner( b[0,:], b[3,:] ), 0.0 )
        assertAAE( numpy.inner( b[1,:], b[2,:] ), 0.0 )
        assertAAE( numpy.inner( b[1,:], b[3,:] ), 0.0 )
        assertAAE( numpy.inner( b[2,:], b[3,:] ), 0.0 )

        a5 = numpy.array( [1,1,0,2], dtype=float )
        u5 = onb.normalise( a5 )
        print( "vector  ", fmt( a5 ) )
        print( "ortnor  ", fmt( u5 ) )
        print( "basis  ", fmt( onb.basis, indent=8 ) )
        print( "" )
        assertAAE( u5, numpy.array( [1,1,0,2] )/ math.sqrt( 6 ) )

        a6 = numpy.random.rand( 20 ) - 0.5
        u6 = onb.normalise( a6, reset=True )
        print( "vector  ", fmt( a6 ) )
        print( "ortnor  ", fmt( u6 ) )
        print( "basis  ", fmt( onb.basis, indent=8, max=None ) )
        print( "" )

        a7 = numpy.random.rand( 20 ) - 0.5
        u7 = onb.normalise( a7, reset=False )
        print( "vector  ", fmt( a7 ) )
        print( "ortnor  ", fmt( u7 ) )
        print( "basis  ", fmt( onb.basis, indent=8, max=None ) )
        print( "" )

        b = onb.basis
        assertAAE( numpy.inner( b[0,:], b[1,:] ), 0.0 )



    def suite( cls ):
        return unittest.TestCase.suite( TestOrthonormalBasis.__class__ )


if __name__ == '__main__':
    unittest.main( )


