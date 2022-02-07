# run with : python3 -m unittest TestAstropyModels.Test.test1

import unittest
import os
import numpy as numpy
from astropy import units
from astropy import modeling
#from astropy.modeling.models import Gaussian1D
#from astropy.modeling.models import Polynomial1D
import matplotlib.pyplot as plt
import warnings

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

class Test( unittest.TestCase ):
    """
    Test harness for Models

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

    def test1a( self ):
        print( "******ASTROPY MODEL 1a**********************" )
        gm = modeling.models.Gaussian1D()

#        m = AstropyModel( gm )
        p = numpy.asarray( [1.2, -0.1, 0.3], dtype=float )

#        stdModeltest( m, p, plot=self.doplot )

        x = numpy.linspace( -2, 2, 6, dtype=float )
#        print( gm )
        gr = gm.evaluate( x, *tuple( p ) )
        gp = gm.fit_deriv( x, *tuple( p ) )

        print( gr.shape )
        print( fmt( gr ) )
        print( gp.__class__, gp[0].shape )
        print( fmt( gp, max=None ) )


        hm = modeling.models.Hermite1D( 2 )
        hr = hm.evaluate( x, *tuple( p ) )
        hp = hm.fit_deriv( x, *tuple( p ) )

#        print( hm )
        print( hr.shape )
        print( fmt( hr ) )
        print( hp.__class__, hp[0].shape )
        print( fmt( hp, max=None ) )
                
    def test1b( self ):
        print( "******ASTROPY MODEL 1B**********************" )

        p = numpy.asarray( [1.2, -0.1, 0.3], dtype=float )
        x = numpy.linspace( -2, 2, 6, dtype=float )

        gm = modeling.models.Gaussian1D()
        m1 = AstropyModel( gm )

        gr = m1.result( x, p )
        gp = m1.partial( x, p )

        print( gr.shape )
        print( fmt( gr ) )
        print( gp.__class__, gp.shape )
        print( fmt( gp, max=None ) )


        hm = modeling.models.Hermite1D( 2 )
        m2 = AstropyModel( hm )
        hr = m2.result( x, p )
        hp = m2.partial( x, p )

#        print( hm )
        print( hr.shape )
        print( fmt( hr ) )
        print( hp.__class__, hp.shape )
        print( fmt( hp, max=None ) )
                


    def test2( self ):
        print( "******ASTROPY MODEL 2***********************" )
        gm = modeling.models.Gaussian1D()

        m = AstropyModel( gm, fixed={0:2.6} )
        p = numpy.asarray( [-0.1,30], dtype=float )

        stdModeltest( m, p, plot=self.doplot )

    def test3( self ):
        print( "******ASTROPY MODEL 3***********************" )
        gm = modeling.models.Gaussian1D()

        print( gm.__class__ )
        print( gm )

        m = AstropyModel( gm ) + PolynomialModel( 1 )
        p = numpy.asarray( [1.2,-0.1,30,1.0,0.3], dtype=float )

        stdModeltest( m, p, plot=self.doplot )

    def test4( self ):
        print( "******ASTROPY MODEL 4***********************" )
        gm = modeling.models.Gaussian1D()

#        print( gm.__class__ )
#        print( gm )

        apm = AstropyModel( gm )
        apm.setPrior( 0, ExponentialPrior( scale=10 ) )     
        apm.setPrior( 1, UniformPrior( limits=[-10,10] ) )     
        apm.setPrior( 2, JeffreysPrior( limits=[0.1,10] ) )     

        bfm = PolynomialModel( 1 )
        bfm.setPrior( 0, UniformPrior( limits=[-5,5] ) )

        m = apm + bfm
        p = numpy.asarray( [1.2,-0.1,30,1.0,0.3], dtype=float )

        N = 201
        x = numpy.arange( N, dtype=float ) / 25 - 2

        y = ( x - 0.70 ) / 0.4
        y *= -0.5 * y
        y = 8.0 * numpy.exp( y )
        y += 0.2 * x + 1.0
        numpy.random.seed( 13456 )
        y += 0.5 * numpy.random.randn( N )

        ns = NestedSampler( x, m, y )
        ns.distribution.setLimits( [0.01, 10] )
        ns.verbose = 2

        evi = ns.sample( plot=self.doplot )
        print( "NS pars ", fmt( ns.parameters ) )
        print( "NS stdv ", fmt( ns.stdevs ) )
        print( "NS scal ", fmt( ns.scale ) )


    def test5( self ):
        print( "******ASTROPY MODEL 1***********************" )
        gm = modeling.models.Gaussian2D()

#        print( gm.param_names )
#        print( gm.parameters )

        m = AstropyModel( gm )
        p = numpy.asarray( [1.2, -0.1, 0.2, 3.0, 2.0, 0.0], dtype=float )

        x = numpy.linspace( -5, 5, 11, dtype=float )
        x = numpy.stack( (x, x) ).T
#        print( x )

        stdModeltest( m, p, x=x, plot=self.doplot )

    ## Next one does not work as a AP-CompoundModel is not and AP-FittableModel
    def XXXtest4( self ):
        print( "******ASTROPY MODEL 4***********************" )
        gm = Gaussian1D() + Polynomial1D( 1 )
        
        print( gm.parameters )
        print( gm )

        m = AstropyModel( gm )
        p = numpy.asarray( [1.2,-0.1,30,1.0,0.3], dtype=float )

        stdModeltest( m, p, plot=self.doplot )


    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestAstropyModel.__class__ )

if __name__ == '__main__':
    unittest.main( )


