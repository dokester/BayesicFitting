# run with : python3 -m unittest TestNLFitters

import unittest
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
################################################################################
    def plotAmoebaFitter( self ):
        self.testAmoebaFitter( plot=True )
        plt.show()

    def testAmoebaFitter( self, plot=False ):
        options = {"temp": 10.0, "maxiter": 10000 }
        options = {"maxiter": 10000}
        stdFittertest( AmoebaFitter, 201, plot=plot, options=options )

    def testAmoebaFitter2( self, plot=False ):
        options = {"temp": 10.0, "maxiter": 10000, "verbose": 2 }
        stdFittertest( AmoebaFitter, 201, errdis='gauss', plot=plot, options=options )
        plt.show()

    def plotNelderMeadFitter( self ):
        self.testNelderMeadFitter( plot=True )
        plt.show()

    def testNelderMeadFitter( self, plot=False ):
        stdFittertest( NelderMeadFitter, 201, plot=plot, options={"maxiter": 3000} )

    def plotPowellFitter( self ):
        self.testPowellFitter( plot=True )
        plt.show()

    def testPowellFitter( self, plot=False ):
        stdFittertest( PowellFitter, 201, plot=plot )

    def plotConjugateGradientFitter( self ):
        self.testConjugateGradientFitter( plot=True )
        plt.show()

    def testConjugateGradientFitter( self, plot=False ):
        stdFittertest( ConjugateGradientFitter, 201, plot=plot )

    def plotBfgsFitter( self ):
        self.testBfgsFitter( plot=True )
        plt.show()

    def testBfgsFitter( self, plot=False ):
        stdFittertest( BfgsFitter, 201, plot=plot )

    def plotNewtonCgFitter( self ):
        self.testNewtonCgFitter( plot=True )
        plt.show()

    def testNewtonCgFitter( self, plot=False ):
        stdFittertest( NewtonCgFitter, 201, plot=plot )

    def plotLbfgsbFitter( self ):
        self.testLbfgsbFitter( plot=True )
        plt.show()

    def testLbfgsbFitter( self, plot=False ):
        stdFittertest( LbfgsbFitter, 201, plot=plot )

    def plotTncFitter( self ):
        self.testTncFitter( plot=True )
        plt.show()

    def testTncFitter( self, plot=False ):
        stdFittertest( TncFitter, 201, plot=plot )

    def plotCobylaFitter( self ):
        self.testCobylaFitter( plot=True )
        plt.show()

    def testCobylaFitter( self, plot=False ):
        stdFittertest( CobylaFitter, 201, plot=plot )

    def plotSlsqpFitter( self ):
        self.testSlsqpFitter( plot=True )
        plt.show()

    def testSlsqpFitter( self, plot=False ):
        stdFittertest( SlsqpFitter, 201, plot=plot )

    def plotDoglegFitter( self ):
        self.testDoglegFitter( plot=True )
        plt.show()

    def testDoglegFitter( self, plot=False ):
        stdFittertest( DoglegFitter, 201, plot=plot )

    def plotTrustNcgFitter( self ):
        self.testTrustNcgFitter( plot=True )
        plt.show()

    def testTrustNcgFitter( self, plot=False ):
        stdFittertest( TrustNcgFitter, 201, plot=plot )

    def plotall( self ):
        self.testAmoebaFitter( plot=True )
        self.testNelderMeadFitter( plot=True )
        self.testPowellFitter( plot=True )
        self.testConjugateGradientFitter( plot=True )
        self.testBfgsFitter( plot=True )
        self.testNewtonCgFitter( plot=True )
        self.testLbfgsbFitter( plot=True )
        self.testTncFitter( plot=True )
        self.testCobylaFitter( plot=True )
        self.testSlsqpFitter( plot=True )
        self.testDoglegFitter( plot=True )
        self.testTrustNcgFitter( plot=True )
        plt.show()


    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestNLFitters.__class__ )


