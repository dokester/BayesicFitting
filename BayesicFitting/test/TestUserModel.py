# run with : python3 -m unittest TestAstropyModels.Test.test1

import unittest
import os
import math
import numpy as numpy
from astropy import units
from astropy import modeling
#from astropy.modeling.models import Gaussian1D
#from astropy.modeling.models import Polynomial1D
import matplotlib.pyplot as plt
import warnings

from numpy.testing import assert_array_almost_equal as assertAAE
from numpy.testing import assert_array_equal as assertAE
from StdTests import stdModeltest

from BayesicFitting import *
from BayesicFitting import formatter as fmt

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

def ur( x, p ) :
    return p[0] * numpy.sin( p[1] * x + p[2] * numpy.log( x + p[3] ) )


def etalonRes( xdata, params ):
    x = math.pi * xdata * params[2] + params[3]
    sx = numpy.sin( x )
    return params[0] / ( 1.0 + params[1] * sx * sx )


def etalonPart( xdata, params ) :

    partial = numpy.ndarray( ( Tools.length( xdata ), 4 ) )

    x = math.pi * xdata * params[2] + params[3]
    sx = numpy.sin( x )
    s2 = sx * sx
    dd = 1.0 / ( 1 + params[1] * s2 )
    d2 = dd * dd
    p3 = - 2 * params[0] * params[1] * sx * numpy.cos( x ) * d2

    partial[:,0] = dd
    partial[:,1] = -params[0] * s2 * d2
    partial[:,2] = math.pi * xdata * p3
    partial[:,3] = p3

    return partial

def etalonDer( xdata, params ) :

    x = math.pi * xdata * params[2] + params[3]
    sx = numpy.sin( x )
    dd = 1 + params[1] * sx * sx
    dd *= dd
    return - 2 * math.pi * params[0] * params[1] * params[2] * sx * numpy.cos( x ) / dd

def fitfunc(x, p):
    return x[:,0]*p[0] + x[:,1]*p[1] + p[2]


class Test( unittest.TestCase ):
    """
    Test harness for Models

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )


    def test1( self ):
        print( "******USER MODEL 1***********************" )

        m = UserModel( 4, ur, userName="FunkModel" )
        m.parameters = [1, 1, 1, 1]

        p = numpy.asarray( [2.3, 1.1, 3.0, 5.0], dtype=float )

        stdModeltest( m, p, plot=self.doplot )


    def test2( self ):
        print( "******USER MODEL 2***********************" )

        m1 = UserModel( 4, etalonRes, userPartial=etalonPart, userDeriv=etalonDer )
        m1.parameters = [1, 1, 1, 1]

        p = numpy.asarray( [2.3, 1.1, 3.0, 5.0], dtype=float )

        stdModeltest( m1, p, plot=self.doplot )

        N = 201
        x = numpy.arange( N, dtype=float ) / 25 - 2

        m2 = EtalonModel()

        assertAE( m1.result( x, p ), m2.result( x, p ) )        
        assertAE( m1.partial( x, p ), m2.partial( x, p ) )        
        assertAE( m1.derivative( x, p ), m2.derivative( x, p ) )        


    def test3( self ):
        print( "******USER MODEL 2***********************" )

        # Make 10 random 2-dimensional points
        x = numpy.random.rand( 10, 2 )

        # Make fake data + noise
        p = numpy.array( [1,2,3] )
        cleandata = fitfunc( x, p )
        noisedata = cleandata * numpy.random.normal( 1, 0.05, x.shape[0] )

        # Find model parameters from noisy data
        model = UserModel( len(p), fitfunc, ndim=2 )
        fitter = Fitter( x, model )
        param = fitter.fit( noisedata )

        self.assertTrue( model.ndim == 2 )
        print( param )




    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestUserModel.__class__ )

if __name__ == '__main__':
    unittest.main( )


