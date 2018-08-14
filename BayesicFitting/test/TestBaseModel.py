# run with : python3 -m unittest TestBaseModel.py

import unittest
import numpy as numpy
from BayesicFitting import *

__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

class TestBaseModel( unittest.TestCase ) :

    def test_init( self ) :
        bm = BaseModel( 5 )
        self.assertTrue( bm.npbase == 5 )
        self.assertTrue( bm.ndim == 1 )
        self.assertTrue( bm.deltaP[0] == 0.00001 )
        self.assertEqual( bm.deltaP.shape, (1,) )
        self.assertTrue( isinstance( bm.deltaP, numpy.ndarray ) )

        self.assertEqual( bm.posIndex.shape, (0,) )
        self.assertTrue( isinstance( bm.posIndex, numpy.ndarray ) )

        self.assertEqual( bm.nonZero.shape, (0,) )
        self.assertTrue( isinstance( bm.nonZero, numpy.ndarray ) )

        bm.posIndex = [2,4]
        bm.nonZero = 3
        self.assertEqual( bm.posIndex.shape, (2,) )
        self.assertTrue( isinstance( bm.posIndex, numpy.ndarray ) )
        self.assertEqual( bm.posIndex[0], 2 )
        self.assertEqual( bm.posIndex[1], 4 )
        self.assertEqual( bm.nonZero.shape, (1,) )
        self.assertTrue( isinstance( bm.nonZero, numpy.ndarray ) )
        self.assertEqual( bm.nonZero[0], 3 )

        cm = BaseModel( copy=bm )

        self.assertTrue( cm.npbase == 5 )
        self.assertTrue( cm.ndim == 1 )
        self.assertTrue( cm.deltaP[0] == 0.00001 )
        self.assertEqual( cm.deltaP.shape, (1,) )
        self.assertTrue( isinstance( cm.deltaP, numpy.ndarray ) )

        self.assertEqual( cm.posIndex.shape, (2,) )
        self.assertTrue( isinstance( cm.posIndex, numpy.ndarray ) )
        self.assertEqual( cm.posIndex[0], 2 )
        self.assertEqual( cm.posIndex[1], 4 )
        self.assertEqual( cm.nonZero.shape, (1,) )
        self.assertTrue( isinstance( cm.nonZero, numpy.ndarray ) )
        self.assertEqual( cm.nonZero[0], 3 )

    def test_parnames( self ) :
        bm = GaussModel( )
#        pm = PolynomialModel( 1 )

        Tools.printclass( bm )
#        Tools.printclass( pm )

#        bm += pm

        self.assertTrue( bm.amplitude == bm.parameters[0] )
        self.assertTrue( bm.center == bm.parameters[1] )
        self.assertTrue( bm.width == bm.parameters[2] )

#        self.assertTrue( bm.parameter_0 == bm.parameters[3] )
#        self.assertTrue( bm.parameter_1 == bm.parameters[4] )




if __name__ == '__main__':
    unittest.main()
