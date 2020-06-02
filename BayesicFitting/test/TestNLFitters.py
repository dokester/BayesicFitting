# run with : python3 -m unittest TestNLFitters

import unittest
import os
import numpy as numpy
from numpy.testing import assert_array_almost_equal as assertAAE
from astropy import units
import math

import matplotlib.pyplot as plt

from BayesicFitting import *

from StdTests import stdFittertest

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
#  *  2004 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2017 Do Kester

class TestNLFitters( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

################################################################################
    def testAmoebaFitter( self ):
        options = {"temp": 10.0, "maxiter": 10000 }
        options = {"maxiter": 10000}
        stdFittertest( AmoebaFitter, 201, plot=self.doplot, options=options )

    def testAmoebaFitter2( self ):
        options = {"temp": 10.0, "maxiter": 10000, "verbose": 1 }
        stdFittertest( AmoebaFitter, 201, errdis='gauss', plot=self.doplot, options=options )

    def testNelderMeadFitter( self ):
        stdFittertest( NelderMeadFitter, 201, plot=self.doplot, options={"maxiter": 3000} )

    def testPowellFitter( self ):
        stdFittertest( PowellFitter, 201, plot=self.doplot )

    def testConjugateGradientFitter( self ):
        stdFittertest( ConjugateGradientFitter, 201, plot=self.doplot )

    def testBfgsFitter( self ):
        stdFittertest( BfgsFitter, 201, plot=self.doplot )

    def testNewtonCgFitter( self ):
        stdFittertest( NewtonCgFitter, 201, plot=self.doplot )

    def testLbfgsbFitter( self ):
        stdFittertest( LbfgsbFitter, 201, plot=self.doplot )

    def testTncFitter( self ):
        stdFittertest( TncFitter, 201, plot=self.doplot )

    def testCobylaFitter( self ):
        stdFittertest( CobylaFitter, 201, plot=self.doplot )

    def testSlsqpFitter( self ):
        stdFittertest( SlsqpFitter, 201, plot=self.doplot )

    def testDoglegFitter( self ):
        stdFittertest( DoglegFitter, 201, plot=self.doplot )

    def testTrustNcgFitter( self ):
        stdFittertest( TrustNcgFitter, 201, plot=self.doplot )

    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestNLFitters.__class__ )


