# run with : python3 -m unittest TestFormatter

import unittest
import numpy as numpy
import math

from BayesicFitting import formatter as fmt
from BayesicFitting import formatter_init as fmtinit

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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *  2006-2015 Do Kester (JAVA CODE)

class TestFormatter( unittest.TestCase ) :
    """
    Test harness for Fitter class.

    @author Do Kester

    """
    def test1( self ):
        print( "===== formatter test1 ===========================" )

        arr = numpy.asarray( [k for k in range(120)], dtype=float  )
        arr = arr.reshape( (3,40) )

        print( fmt( arr, max=None ) )
        print( "arr", fmt( arr[1], indent=4, format=" %7.2f", max=20 ) )
        print( fmt( arr.reshape( (3,4,10) ), max=2 ) )
        alist = [1,2,3,4,5]
        print( fmt( alist ) )
        self.assertTrue( isinstance( alist, list ) )
        print( fmt( 3 ), fmt( 3.4 ) )

    def test2( self ):
        print( "===== formatter test2 ===========================" )

        arr = numpy.asarray( [k for k in range(36)], dtype=float  )
        arr = arr.reshape( (3,12) )

        fmtinit( max=None )
        print( fmt( arr, max=None ) )
        fmtinit( linelength=60 )
        print( fmt( arr, max=None ) )
        fmtinit( linelength=80, format={"float64" : " %7.2f"} )
        print( fmt( arr, max=None ) )

        print( "arr", fmt( arr, indent=4, format=" %7.2f" ) )
        print( fmt( arr, max=2 ) )
        alist = [1,2,3,4,5]
        print( fmt( alist ) )
        self.assertTrue( isinstance( alist, list ) )
        print( fmt( 3 ), fmt( 3.4 ) )

    def suite( cls ):
        return ConfiguredTestCase.suite( TestFormatter.__class__ )

if __name__ == '__main__':
    unittest.main( )


