# run with : python3 -m unittest TestImageAssistant

import unittest
import numpy as numpy
from numpy.testing import assert_array_almost_equal as assertAAE
from astropy import units
import matplotlib.pyplot as plt
import warnings

from BayesicFitting import PolySurfaceModel
from BayesicFitting import ImageAssistant

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

class TestImageAssistant( unittest.TestCase ):
    """
    Test harness for 2d-Models

    Author:      Do Kester

    """
    def testImageAssistantC( self, plot=False ):

        print( "====ImageAssistant C ===================" )
        ymap = numpy.arange( 6, dtype=float ).reshape( 2, 3 )
        print( ymap )
        ia = ImageAssistant()
        xdata = ia.getIndices( ymap )
        print( xdata )
        print( xdata.shape )
        for k in range( 6 ) :
            assertAAE( xdata[k,:], [k//3,k%3] )
            self.assertTrue( ymap[xdata[k,0],xdata[k,1]] == k )
        ydata = ia.getydata( ymap )
        print( ydata )
        ydata += 1
        ymap1 = ia.resizeData( ydata )
        print( ymap1 )
        assertAAE( ymap1, ymap + 1 )

    def testImageAssistantF( self, plot=False ):

        print( "====ImageAssistant F ===================" )
        ymap = numpy.arange( 6, dtype=float ).reshape( 2, 3 )
        print( ymap )
        ia = ImageAssistant( order='F')
        xdata = ia.getIndices( ymap )
        print( xdata )
        for k in range( 6 ) :
            assertAAE( xdata[k,:], [k%3,k//3] )
            self.assertTrue( ymap[xdata[k,1],xdata[k,0]] == k )
        ydata = ia.getydata( ymap )
        print( ydata )
        ydata += 1
        ymap1 = ia.resizeData( ydata, shape=ymap.shape )
        print( ymap1 )
        assertAAE( ymap1, ymap + 1 )

    def testImageAssistant3dC( self, plot=False ):

        print( "====ImageAssistant 3d C ===================" )
        ymap = numpy.arange( 24, dtype=float ).reshape( 2, 3, 4 )
        print( ymap )
        ia = ImageAssistant( order='C')
        xdata = ia.getIndices( ymap )
        print( xdata )
        ydata = ia.getydata( ymap )
        print( ydata )
        ydata += 1
        ymap1 = ia.resizeData( ydata, shape=ymap.shape )
        print( ymap1 )
        assertAAE( ymap1, ymap + 1 )

    def testImageAssistant3dF( self, plot=False ):

        print( "====ImageAssistant 3d F ===================" )
        ymap = numpy.arange( 24, dtype=float ).reshape( 2, 3, 4 )
        print( ymap )
        ia = ImageAssistant( order='F')
        xdata = ia.getIndices( ymap )
        print( xdata )
        ydata = ia.getydata( ymap )
        print( ydata )
        ydata += 1
        ymap1 = ia.resizeData( ydata )
        print( ymap1 )
        assertAAE( ymap1, ymap + 1 )

    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestImageAssistant.__class__ )

if __name__ == '__main__':
    unittest.main( )


