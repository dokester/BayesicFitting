# run with : python3 -m unittest TestTools

import unittest
import numpy as numpy
import math
from datetime import date

from BayesicFitting import Tools

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

class TestTools( unittest.TestCase ) :
    """
    Test harness for Fitter class.

    @author Do Kester

    """
    def testtoday( self ):
        print( date.today() )

    def testMakeNext( self ):
        print( "===== makeNext ===========================" )
        x = 2
        xgen = Tools.makeNext( x, 0 )
        for k in range( 10 ) :
            nx = next( xgen )
            print( k, nx )
            self.assertTrue( nx == 2 )
        xgen.close()

        x = [2,3,4,5]
        xgen = Tools.makeNext( x, 0 )
        for k in range( 10 ) :
            nx = next( xgen )
            print( k, nx )
            self.assertTrue( ( nx == (k+2) and k < 4 ) or nx == 5 )
        xgen.close()

        x = [2,3,4,5,6,7,8,9,10,11]
        xgen = Tools.makeNext( x, 0 )
        for k in range( 10 ) :
            nx = next( xgen )
            print( k, nx )
            self.assertTrue( nx == (k+2) )

        x = [2,3,4,5]
        xgen = Tools.makeNext( x, 2 )
        for k in range( 10 ) :
            nx = next( xgen )
            print( k, nx )
            self.assertTrue( ( nx == (k+4) and k < 6 ) or nx == 5 )
        xgen.close()

    def testLength( self ) :
        print( "===== length ================================" )
        x = 3.0
        self.assertTrue( Tools.length( x ) == 1 )
        x = [2,3,4,5]
        self.assertTrue( Tools.length( x ) == 4 )
        x = numpy.asarray( [2,3,4,5] )
        self.assertTrue( Tools.length( x ) == 4 )
        x.resize( 2, 2 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( Tools.length( x ) == 2 )
        x = [2,3,4,5]
        x = numpy.asarray( [x] )
        print( x, x.shape, x.__class__ )
        self.assertTrue( Tools.length( x ) == 1 )

    def testToArray( self ) :
        print( "===== toArray ================================" )
        x = Tools.toArray( 3 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 1 )
        x = Tools.toArray( 3.0 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 1 )
        x = Tools.toArray( [3,4,5,6] )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 1 )
        x = Tools.toArray( [3,4.5,5,6], ndim=1 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 1 )
        x = Tools.toArray( [3,4.5], ndim=2 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 2 )

    @classmethod
    def suite( cls ):
        return ConfiguredTestCase.suite( PriorTest.__class__ )

if __name__ == '__main__':
    unittest.main( )


