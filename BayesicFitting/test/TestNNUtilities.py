# run with : python3 -m unittest TestNNUtilities

import unittest
import numpy as numpy
from astropy import units
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from BayesicFitting import formatter as fmt

from BayesicFitting import *

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
#  *  2006 Do Kester

class Test( unittest.TestCase ):
    """
    Test harness for NeuralNetUtilities.

    Author       Do Kester

    """
    def __init__( self, name ):
        super( ).__init__( name )


    def test1( self ):
        print( "======= Neural Net Utilities  test 1 ========================" )

        con = NeuralNetUtilities.Connect( ndim=2, ndout=3 )

        print( con.ndim, con.ndout, con.nraster  )

        self.assertTrue( con.nraster == 6 )

        xx = numpy.array( [[1,2], [2,3], [3,4], [4,5]], dtype=float )
        par = numpy.arange( 6, dtype=float ) + 1

        print( fmt( xx ) )
        print( fmt( par, max=None ) )

        res = con.result( xx, par )
        print( "result  ", res.shape )
        print( fmt( res ) )

        partial = con.partial( xx, par )
        print( "partial ", partial.shape )
        print( fmt( partial, max=None ) )
        print( fmt( partial[0], max=None ) )
        print( fmt( partial[1], max=None ) )
        print( fmt( partial[2], max=None ) )


        deriv = con.derivative( xx, par )
        print( "deriv   ", deriv.shape )
        print( fmt( deriv, max=None ) )


    def test2( self ):
        print( "======= Neural Net Utilities  test 2 ========================" )

        con = NeuralNetUtilities.ConnectWithBias( ndim=2, ndout=3 )

        print( con.ndim, con.ndout, con.nraster  )

        self.assertTrue( con.nraster == 6 )

        xx = numpy.array( [[1,2], [2,3], [3,4], [4,5]], dtype=float )
        par = numpy.arange( 9, dtype=float ) + 1

        print( fmt( xx ) )
        print( fmt( par, max=None ) )

        res = con.result( xx, par )
        print( "result  ", res.shape )
        print( fmt( res ) )

        partial = con.partial( xx, par )
        print( "partial ", partial.shape )
        print( fmt( partial, max=None ) )

        deriv = con.derivative( xx, par )
        print( "deriv   ", deriv.shape )
        print( fmt( deriv, max=None ) )

    def test3( self ):
        print( "======= Neural Net Utilities  test 3 ========================" )

        con = NeuralNetUtilities.ConnectWithBias( ndim=2, ndout=3 )
        atn = NeuralNetUtilities.Arctan()

        print( con.ndim, con.ndout, con.nraster  )

        self.assertTrue( con.nraster == 6 )

        xx = numpy.array( [[1,2], [2,3], [3,4], [4,5]], dtype=float )
        par = numpy.arange( 9, dtype=float ) + 1

        print( fmt( xx ) )
        print( fmt( par, max=None ) )

        res = atn.result( con.result( xx, par ), par )
        print( "result  ", res.shape )
        print( fmt( res ) )

        dfdr = atn.derivative( con.result( xx, par ), par )
        drdp = con.partial( xx, par )
        partial = atn.pipe( dfdr, drdp )
        print( "partial ", partial.shape )
        print( fmt( partial, max=None ) )

    def test4( self ):
        print( "======= Neural Net Utilities  test 4 ========================" )

        con = NeuralNetUtilities.ConnectWithBias( ndim=2, ndout=3 )
        atn = NeuralNetUtilities.Logistic()

        print( con.ndim, con.ndout, con.nraster  )

        self.assertTrue( con.nraster == 6 )

        xx = numpy.array( [[1,2], [2,3], [3,4], [4,5]], dtype=float )
        par = numpy.arange( 9, dtype=float ) + 1

        print( fmt( xx ) )
        print( fmt( par, max=None ) )

        res = atn.result( con.result( xx, par ), par )
        print( "result  ", res.shape )
        print( fmt( res ) )

        partial = atn.derivative( con.partial( xx, par ), par )
        print( "partial ", partial.shape )
        print( fmt( partial, max=None ) )

    def test5( self ):
        print( "======= Neural Net Utilities  test 5 ========================" )

        con = NeuralNetUtilities.ConnectWithBias( ndim=2, ndout=3 )
        atn = NeuralNetUtilities.Heaviside()

        print( con.ndim, con.ndout, con.nraster  )

        self.assertTrue( con.nraster == 6 )

        xx = numpy.array( [[1,2], [2,3], [3,4], [4,5]], dtype=float )
        par = numpy.arange( 9, dtype=float ) - 4

        print( fmt( xx ) )
        print( fmt( par, max=None ) )

        res = atn.result( con.result( xx, par ), par )
        print( "result  ", res.shape )
        print( fmt( res ) )

        dfdr = atn.derivative( con.result( xx, par ), par )
        drdp = con.partial( xx, par )
        partial = atn.pipe( dfdr, drdp )

        print( "partial ", partial.shape )
        print( fmt( partial, max=None ) )


    def test6( self ):
        print( "======= Neural Net Utilities  test 6 ========================" )

        con = NeuralNetUtilities.ConnectWithBias( ndim=2, ndout=3 )
        atn = NeuralNetUtilities.Softmax( ndout=3 )

        print( con.ndim, con.ndout, con.nraster  )

        self.assertTrue( con.nraster == 6 )

        xx = numpy.array( [[2,1], [2,3], [3,4], [4,5]], dtype=float )
        par = numpy.arange( 9, dtype=float )
        par[6:] = [0,-1,1]
        par[0],par[5] = par[5],par[0]

        print( fmt( xx ) )
        print( fmt( par, max=None ) )

        sm = SoftMaxModel( ndim=2, ndout=3, offset=True )

        res = con.result( xx, par )
        print( "result  con  ", res.shape )
        print( fmt( res ) )

        res = atn.result( res, par )
        print( "result  atn  ", res.shape )
        print( fmt( res ) )

        print( sm )
        smr = sm.result( xx, par )
        print( "result  sm   ", smr.shape )
        print( fmt( smr ) )


        dzdy = atn.derivative( con.result( xx, par ), par )
        print( "dfdr    ", dzdy.shape )
        print( fmt( dzdy, max=None ) )

        dydx = con.partial( xx, par )
        print( "drdp    ", dydx.shape )
        print( fmt( dydx, max=None ) )

        dzdx = numpy.zeros_like( dydx )

        for k in range( 9 ) :
            for i in range( 4 ) :
                dzdx[:,i,k] = numpy.inner( dzdy[:,i,:], dydx[:,i,k] )
        
#        dzdx = dzdy * dydx
        print( "dfdp    ", dzdx.shape )
        print( fmt( dzdx, max=None ) )

        printclass( sm )
        print( sm.trans.pipe )

        print( "SoftMax partial" )
        print( fmt( sm.partial( xx, par ), max=None ) )

        print( "SoftMax deriv  " )
        print( fmt( sm.derivative( xx, par ), max=None ) )










    def suite( cls ):
        return unittest.TestCase.suite( TestSplines.__class__ )


if __name__ == '__main__':
    unittest.main( )


