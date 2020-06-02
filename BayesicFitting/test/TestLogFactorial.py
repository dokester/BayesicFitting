# run with : python3 -m unittest TestLogFactorial

import unittest
import numpy as numpy
import math
from numpy.testing import assert_array_almost_equal as assertAAE
from astropy import units
import matplotlib.pyplot as plt
import warnings

from BayesicFitting import logFactorial

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

class TestLogFactorial( unittest.TestCase ):
    """
    Test harness for LogFactorial

    Author:      Do Kester

    """
    def testLogFactorial( self ):

        print( "====LogFactorial ===================" )
        self.assertTrue( logFactorial( 0 ) == 0 )
        self.assertTrue( logFactorial( 1 ) == 0 )
        self.assertTrue( logFactorial( 3 ) == 1.7917594692280550 )
        self.assertTrue( logFactorial( 10 ) == 15.1044125730755159 )
        print( logFactorial( 99 ), logFactorial( 100 ), logFactorial( 101 ) )
        self.assertTrue( logFactorial( 99 ) == 359.1342053695754544 )
        lf = 359.1342053695754544 + math.log( 100 )
        assertAAE( logFactorial( 100 ), lf )

        kk = [3, 5, 7]
        print( logFactorial( kk ) )
        self.assertTrue( isinstance( kk, list ) )

        data = numpy.arange( 100, dtype=int ) + 40

        logd = numpy.log( data )

        lf1 = numpy.cumsum( logd ) + logFactorial( 39 )
        lf2 = logFactorial( data )

        k = [0,10,20,30,40,50,60,70,80,90]
        print( lf1[k] )
        print( lf2[k] )
        assertAAE( lf1, lf2 )


    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestLogFactorial.__class__ )

if __name__ == '__main__':
    unittest.main( )


