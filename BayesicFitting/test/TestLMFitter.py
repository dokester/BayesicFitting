# run with : python3 -m unittest TestLMFitter

import unittest
import numpy as numpy
from numpy.testing import assert_array_almost_equal as assertAAE
from astropy import units
import math

import matplotlib.pyplot as plt

from BayesicFitting import *
from BayesicFitting import LevenbergMarquardtFitter as LMFitter

from BayesicFitting import formatter as fmt

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
#  *  2017        Do Kester

class TestLMFitter( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author:      Do Kester

    """
    def makeData( self, bg=False ) :

        p = [3.2, -0.1, 0.3, 1.1, 2.1]
        ss = 0.3

        ndata = 101
        x = numpy.linspace( -1, +1, ndata, dtype=float )
        y = ( x - p[1] ) / p[2]
        numpy.random.seed( 3456 )
        y = p[0] * numpy.exp( -y * y ) + ss * numpy.random.randn( ndata )
        if not bg :
            return (x,y,p[:3])

        y += ( p[3] + p[4] * x )
        return (x,y,p)

    def eq( self, a, b, eps=1e-10 ) :
        if ( a + b ) != 0 :
            return abs( a - b ) / abs( a + b ) < eps
        else :
            return abs( a - b ) < eps


################################################################################
    def plot1( self ):
        self.test1( plot=True )

    def test1( self, plot=False ):

        x,y,p1 = self.makeData()

        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )
        print( "Testing Nonlinear Fitters: LevenbergMarquardt (lm)" )
        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )
        modl1 = GaussModel( )

        amfit = LMFitter( x, modl1 )

        print( fmt( p1 ) )
        par1 = amfit.fit( y )

        print( fmt( par1 ) )
        assertAAE( par1, p1, 1 )

        x,z,p2 = self.makeData( bg=True )

        modl2 = GaussModel( )
        modl2.addModel( PolynomialModel(1) )

        modl2.parameters = numpy.append( par1, [0,0] )
        lmfit = LMFitter( x, modl2 )

        par2 = lmfit.fit( z )
        print( fmt( p2 ) )
        print( fmt( par2 ) )

        print( "chisq1 = ", amfit.chisq, "  chisq2 = ", lmfit.chisq )

        assertAAE( par2, p2, 1 )

        if plot :
            xx = numpy.linspace( -1, +1, 1001 )
            plt.plot( x, y, 'k+' )
            plt.plot( xx, modl1.result( xx ), 'k-' )
            plt.plot( x, z, 'r+' )
            plt.plot( xx, modl2.result( xx ), 'r-' )


        print( fmt( amfit.hessian ) )
        print( fmt( amfit.design[-4:,:], max=None ) )


        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )
        print( "Testing LevenbergMarquardt (normalized)" )
        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )
        modl1 = GaussModel( )

        bmfit = LMFitter( x, modl1 )

        conpr1 = numpy.asarray( [1.0,0.0,0.0] )

        bmfit.normalize( conpr1, p1[0], weight=10.0 )

        print( "Normweight = ", bmfit.normweight )

        print( fmt( p1 ) )

        par3 = bmfit.fit( y )
        print( fmt( par1 ) )
        print( fmt( par3 ) )
        print( fmt( amfit.chisq ), fmt( bmfit.chisq ) )

        hes1 = amfit.getHessian( params=par3 )
        hes3 = bmfit.getHessian( params=par3 )
        print( fmt( hes1 ) )
        print( fmt( hes3 ) )

        f = bmfit.normweight
        for h1,h3 in zip( hes1.flat, hes3.flat ) :
            self.assertTrue( abs( h1 + f - h3 ) < 1e-8 )
            f = 0.0

        if plot :
            plt.plot( xx, modl1.result( xx ), 'g-' )
            plt.show()


    def test4( self, plot=False ) :

        self.normalizetest( Fitter )
        self.normalizetest( QRFitter )
        self.normalizetest( CurveFitter )
        self.normalizetest( LMFitter )
        self.assertRaises( NotImplementedError, self.normalizetest, AmoebaFitter )
#        self.assertRaises( NotImplementedError, self.normalizetest, PowellFitter )

    def normalizetest( self, fitter ) :

        p = numpy.asarray( [2.0, 1.3] )
        x = numpy.asarray( [1.0, 1.3, 1.5, 1.8, 2.0] )
        numpy.random.seed( 12345 )
        y = p[0] + p[1] * x + 0.5 * numpy.random.randn( 5 )

        m = PolynomialModel( 1 )

        ftr = fitter( x, m )
        print( "=============================================================" )
        print( str( ftr ) )
        print( fmt( x ) )
        print( fmt( y ) )

        par = ftr.fit( y )
        print( fmt( p ) )
        print( fmt( par ) )

        conpr = numpy.asarray( [1.0,0.0] )
        for w in [0,1,10,100,1000] :
            m2 = m.copy()
            ftr = fitter( x, m2 )

            ftr.normalize( conpr, p[0], weight=w )
            par = ftr.fit( y )
            print( fmt( w ), fmt( par ), fmt( ftr.chisq ) )

        self.assertTrue( abs( p[0] - par[0] ) < 1e-3 )

        print( fmt( ftr.hessian ) )
#        print( fmt( ftr.getVector( y ) ) )




    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestLMFitter.__class__ )


