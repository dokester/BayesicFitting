import unittest
import os
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt
from BayesicFitting import formatter as fmt

from BayesicFitting import *


class TestPlot( unittest.TestCase ):
    "A few simple tests for HelpPlot"

    def __init__( self, testname ):
        super( ).__init__( testname )
        print( os.environ )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

        print( "DP  ", self.doplot )

    def test( self ):
        print( "==== test 1 ========" )
        a = numpy.arange( 11, dtype=float )
        b = numpy.arange( 11, dtype=float )
#        self.assertEqual(a, b)
        self.assertTrue( True )
        print( "DPi ", self.doplot )
        if self.doplot :
            plt.plot( a, b )
            plt.show()
        else :
            print( "no plot" )

if __name__ == '__main__':
    unittest.main()

