#run with: python3 -m unittest TestPipeModel

import unittest
import os
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt

#from BayesicFitting import PolynomialModel, SineModel
#from Model import Model

from StdTests import stdModeltest

from BayesicFitting import formatter as fmt
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


    def testPipe1( self ) :
        print( "=== testPipe1:  1 ==> 1 ==> 1  pipe_0 and pipe_4 ==============" )

        model = PolynomialModel( 2 )
        model |= SineModel()
        self.pipetest( model, 0, 4 )

        print( model )
        p = numpy.asarray( [0.0, 0.4, 0.2, 1.0, 0.0, 1.0] )
        x = numpy.linspace( 0, 10, 101, dtype=float )

        self.shapetest( model, x, p )

        stdModeltest( model, p, x=x, plot=self.doplot )

    def testPipe2( self ) :
        print( "=== testPipe2:  pipe_0 and pipe_4 ==============" )
        model = PolynomialModel( 2 )
        model |= SineModel()
        model *= ExpModel()
        print( model )
        p = numpy.asarray( [0.0, 0.4, 0.2, 1.0, 0.0, 1.0, 1.3, -0.2] )
        x = numpy.linspace( 0, 10, 101, dtype=float )

        self.shapetest( model, x, p )

        stdModeltest( model, p, x=x, plot=self.doplot )

    def testPipe3( self ) :
        print( "=== testPipe3:  1 ==> 2 ==> 1  pipe_2 and pipe_6 ==============" )
        model = StellarOrbitModel( )
        model |= PolySurfaceModel( 3 )
        self.pipetest( model, 2, 6 )

        p = numpy.asarray( [0.0, 0.4, 0.2, 1.0, 0.0, 0.0, 0.4, 0.2, 1.0, 0.0, 0.0, 0.4,
                            -0.1, -0.2, 0.3, 0.0, 0.0] )
        x = numpy.linspace( 0, 10, 101, dtype=float )

        self.shapetest( model, x, p )
        stdModeltest( model, p, x=x, plot=self.doplot )

    def testPipe4( self ) :
        print( "=== testPipe4:  1 ==> 1 ==> 2  pipe_3 and pipe_7 ==============" )
        model = PolynomialModel( 1 )
        model |= StellarOrbitModel( )
        self.pipetest( model, 3, 7 )

        p = numpy.asarray( [0.1, 1.1, 0.0, 0.4, 0.2, 1.0, 0.0, 0.0, 0.4] )
        x = numpy.linspace( 0, 10, 101, dtype=float )

        self.shapetest( model, x, p )
        stdModeltest( model, p, x=x, plot=self.doplot )

    def testPipe5( self ) :
        print( "=== testPipe5: 2 ==> 1 ==> 2  pipe_3 and pipe_9 ==============" )
        model = PolySurfaceModel( 1 )
        model |= StellarOrbitModel( )
        self.pipetest( model, 3, 9 )

        p = numpy.asarray( [0.1, 1.1, 0.9, 0.0, 0.4, 0.2, 1.0, 0.0, 0.0, 0.4] )
        x = numpy.linspace( 0, 10, 101*model.ndim, dtype=float ).reshape( 101, model.ndim )

        self.shapetest( model, x, p )
        stdModeltest( model, p, x=x, plot=self.doplot )

    def testPipe6( self ) :
        print( "=== testPipe6: 2 ==> 1 ==> 1  pipe_0 and pipe_0 ==============" )
        model = PolySurfaceModel( 1 )
        model |= ArctanModel( )
        self.pipetest( model, 0, 0 )

        p = numpy.asarray( [0.1, 1.1, 0.9, 2.0, 0.4, 0.2] )
        x = numpy.linspace( 0, 10, 101*model.ndim, dtype=float ).reshape( 101, model.ndim )

        self.shapetest( model, x, p )
        stdModeltest( model, p, x=x, plot=self.doplot )

    def testPipe7a( self ) :
        print( "=== testPipe7a: check Raise  ==============" )
        model = SoftMaxModel( ndim=3, ndout=2, normed=False )
        m2 = StellarOrbitModel( )
        self.assertRaises( ValueError, model.appendModel, m2, model.PIP )

    def testPipe7( self ) :
        print( "=== testPipe7: 1 ==> 2 ==> 3  pipe_1 and pipe_5 ==============" )

        nx = 2
        x1 = numpy.zeros( nx, dtype=float ) + 0.03
                
        model1 = StellarOrbitModel()
        p1 = [0.1, 1.0, 2.0, 0.0, 0.0, 0.0, 0.0]
        print( fmt( x1 ) )

        x2 = model1.result( x1, p1 )
        print( fmt( x2 ) )

        model2 = SoftMaxModel( ndim=2, ndout=3, normed=False )

        p2 = numpy.arange( model2.npars, dtype=float ) + 1

        print( fmt( model2.result( x2, p2 ) ) )
        print( fmt( p2, max=None ) )
        print( fmt( model2.partial( x2, p2 ), max=None ) )
        print( fmt( model2.strictNumericPartial( x2, p2 ), max=None ) )
        print( fmt( model2.derivative( x2, p2 ), max=None ) )
        print( fmt( model2.strictNumericDerivative( x2, p2 ), max=None ) )


        model = model1 | model2
        p = numpy.append( p1, p2 )

        printclass( model._next )
        self.pipetest( model, 1, 5 )

        x = x1
        print( fmt( model.result( x, p ) ) )
        print( fmt( p, max=None ) )
        print( fmt( model.partial( x, p ), max=None ) )
        print( fmt( model.strictNumericPartial( x, p ), max=None ) )
        print( fmt( model.derivative( x, p ), max=None ) )
        print( fmt( model.strictNumericDerivative( x, p ), max=None ) )
        

        self.shapetest( model, x, p, nx=nx )

        nx = 11
        x = numpy.zeros( nx, dtype=float ) + 0.03

        stdModeltest( model, p, x=x, plot=self.doplot )


    def testPipe8( self ) :
        print( "=== testPipe8: 3 ==> 2 ==> 1  pipe_2 and pipe_8 ==============" )
        model = SoftMaxModel( ndim=3, ndout=2, normed=False )
        model |= PolySurfaceModel( 1 )
        self.pipetest( model, 2, 8 )

        p = numpy.asarray( [0.1, 1.1, 0.9, 0.0, 0.4, 0.2, 0.1, 1.1, 0.9] )
        x = numpy.linspace( 0, 10, 101*model.ndim, dtype=float ).reshape( 101, model.ndim )

        self.shapetest( model, x, p )
        stdModeltest( model, p, x=x, plot=self.doplot )

    def testPipe9( self ) :
        print( "=== testPipe9: 3 ==> 2 ==> 4  pipe_1 and pipe_1 ==============" )

        model = SoftMaxModel( ndim=3, ndout=2, normed=False )
        model |= SoftMaxModel( ndim=2, ndout=4, normed=False )
        self.pipetest( model, 1, 1 )

        p = numpy.linspace( -1, 1, model.npars )
        x = numpy.linspace( 0, 10, 101*model.ndim, dtype=float ).reshape( 101, model.ndim )

        self.shapetest( model, x, p )
        stdModeltest( model, p, x=x, plot=self.doplot )

    def testPipe10( self ) :
        print( "=== testPipe10: 1 ==> 2 ==> 3  pipe_1 and pipe_5 ==============" )
        model = StellarOrbitModel( )
        model |= SoftMaxModel( ndim=2, ndout=3, normed=False )

        printclass( model._next )
        self.pipetest( model, 1, 5 )

        p = numpy.asarray( [0.0, 0.4, 0.2, 1.0, 0.0, 0.0, 0.4, 0.2, 1.0, 0.0, 0.0, 0.4, 0.5] )
        x = numpy.linspace( 0, 10, 101, dtype=float )

        self.shapetest( model, x, p )
        stdModeltest( model, p, x=x, plot=self.doplot )

    def pipetest( self, model, p, d ) :

        self.assertTrue( "pipe_%d"%p in str( model._next.pipePartial ) )  
        self.assertTrue( "pipe_%d"%d in str( model._next.pipeDeriv ) ) 




    def shapetest( self, model, x, p, nx=101 ) :
        ni = model.ndim
        no = model.lastndout
        np = model.npars

        print( "In %d  Out %d  Xd %d  Np %d" % ( ni, no, nx, np ) )
        xshp = x.shape
        print( "xshape  ", xshp )

        y = model.result( x, p )
        yshp = y.shape
        print( "yshape  ", yshp )
        self.assertTrue( yshp[0] == nx )
        if no > 1 :
            self.assertTrue( yshp[1] == no )

        pp = model.partial( x, p )
        if no > 1 :
            self.assertTrue( len( pp ) == no )
            pshp = pp[0].shape
            print( "pshape  ", len( pp ), pshp )
        else :
            pshp = pp.shape
            print( "pshape  ", pshp )
        self.assertTrue( pshp[0] == nx )
        self.assertTrue( pshp[1] == np )

        dd = model.derivative( x, p )
        if no > 1 and ni > 1 :
            self.assertTrue( len( dd ) == no )
            dshp = dd[0].shape
            print( "dshape  ", len( dd ), dshp )
        else :
            dshp = dd.shape
            print( "dshape  ", dshp )
        self.assertTrue( dshp[0] == nx )
        if no == 1 and ni > 1 :
            self.assertTrue( dshp[1] == ni )
        elif no > 1 and ni == 1 :
            self.assertTrue( dshp[1] == no )


    def suite( cls ):
        return unittest.TestCase.suite( TestPipeModel.__class__ )


if __name__ == '__main__':
    unittest.main()

