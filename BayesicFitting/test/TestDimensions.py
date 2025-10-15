#run with: python3 -m unittest TestDimensions

import unittest
import os
import numpy as numpy
from numpy.testing import assert_array_almost_equal as assertAAE

#from BayesicFitting import PolynomialModel, SineModel
#from Model import Model

from StdTests import stdModeltest as stdMtest

from BayesicFitting import *

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
#  *    2016 Do Kester

class Test( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )


    def test1( self ) :
        model = PolynomialModel( 2 )
        print( "====Test1===== dimensions  ", model.ndim, model.ndout )

        print( model )

        p = numpy.asarray( [0.0, 0.4, 0.2] )
        x = numpy.linspace( 0, 10, 11, dtype=float )

        stdMtest( model, p, x=x, plot=self.doplot )
        self.stdModeltest( model, p, x=x, plot=self.doplot )
        self.stdModeltest( model, p, x=x[[0]], plot=self.doplot )

    def test2( self ) :
        model = PolySurfaceModel( 2 )
        print( "====Test2===== dimensions  ", model.ndim, model.ndout )

        print( model )

        p = numpy.asarray( [0.0, 0.4, 0.2, 1.0, 0.0, 1.0] )
        x = numpy.linspace( 0, 10, 22, dtype=float ).reshape( (11,2) )

        self.stdModeltest( model, p, x=x, plot=self.doplot )
        self.stdModeltest( model, p, x=x[[0],:], plot=self.doplot )

    def test3( self ) :
        model = StellarOrbitModel( )
        print( "====Test3===== dimensions  ", model.ndim, model.ndout )

        print( model )

        p = numpy.asarray( [0.0, 0.4, 0.2, 1.0, 0.0, 1.0, 2.0] )
        x = numpy.linspace( 0, 10, 11, dtype=float )

        self.stdModeltest( model, p, x=x, plot=self.doplot )
        self.stdModeltest( model, p, x=x[[0]], plot=self.doplot )

    def test4( self ) :
        model = SoftMaxModel( ndim=3, ndout=2 )
        print( "====Test4===== dimensions  ", model.ndim, model.ndout )

        print( model )

        p = numpy.asarray( [0.0, 0.4, 0.2, 1.0, 0.0, 1.0] )
        x = numpy.linspace( 0, 10, 33, dtype=float ).reshape( (11,3) )

        self.stdModeltest( model, p, x=x, plot=self.doplot )
        self.stdModeltest( model, p, x=x[[0],:], plot=self.doplot )

    def XXXtest6( self ) :
        model = AbsoluteValueFilter( ndim=3 )
        print( "====Test6===== dimensions  ", model.ndim, model.ndout )

        print( model )

        p = numpy.asarray( [] )
        x = numpy.linspace( -4, 10, 12, dtype=float ).reshape( (4,3) )

        self.stdModeltest( model, p, x=x, plot=self.doplot )
#        self.stdModeltest( model, p, x=x[[0],:], plot=self.doplot )

    def test5( self ) :
        model = Kernel2dModel( )
        print( "====Test5===== dimensions  ", model.ndim, model.ndout )

        print( model )

        p = numpy.asarray( [0.4, 0.2, 1.0, 2.0] )
        x = numpy.linspace( 0, 10, 22, dtype=float ).reshape( (11,2) )

        self.stdModeltest( model, p, x=x, plot=self.doplot )

    def stdModeltest( self, model, p, x, plot=False ) :

        print( fma( x ) )
        print( x.shape )
        self.assertTrue( x.ndim == 1 or x.shape[1] == model.ndim )

        print( "result:" )
        res = model.result( x, p )
        print( fma( res ) )
        self.assertTrue( res.ndim == 1 or res.shape[1] == model.ndout )

        print( "derivative:" )
        der = model.derivative( x, p )
        print( fma( der ) )
        print( "strict numderiv:" )
        snd = model.strictNumericDerivative( x, p )
        print( fma( snd ) )
        assertAAE( der, snd )

        print( "partial:" )
        prt = model.partial( x, p )
        print( fma( prt ) )
        print( "strict partial:" )
        snp = model.strictNumericPartial( x, p )
        print( fma( snp ) ) 
        assertAAE( prt, snp )

#        print( snd )
#        print( snp )
#        print( "numeric:" )
#        print( fmt( model.numPartial( x, p ) ) )



    def suite( cls ):
        return unittest.TestCase.suite( TestDimensions.__class__ )


if __name__ == '__main__':
    unittest.main()

