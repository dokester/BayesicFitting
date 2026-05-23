import unittest
import os
import math
import numpy as numpy
from astropy.io import ascii
import matplotlib.pyplot as plt
from numpy.testing import assert_allclose as assertAC

from BayesicFitting import *


class Test( unittest.TestCase ):
    "A few simple tests for HelpPlot"

    def __init__( self, testname ):
        super( ).__init__( testname )
#        print( os.environ )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

#        print( "DP  ", self.doplot )

    def test1( self ):
        print( "==== test 1 ========" )

        TWOPI = 2 * math.pi

        esm = EclipsingStarModel()
        np = esm.npars
        rng = numpy.random.default_rng( seed=345678 )
        for k in range( 4 ) :
            par = rng.normal( scale=0.1, size=np )
            par[0] = abs( par[0] )
            par[1] = 1 + 100 * abs( par[1] )
            par[2] = rng.uniform( 0, TWOPI, 1 )[0]
            par[3] += math.pi / 2
            par[4] = rng.uniform( 0, TWOPI, 1 )[0]
            par[5] = abs( 0.2 + par[5] )
            par[6] = abs( 0.1 + par[6] )
            par[7:] = rng.uniform( 2, 5, 2 )
    
            nd = 1200
            days = numpy.linspace( 0, 700, nd ) + rng.random( nd )
            flux = esm.result( days, par ) + rng.normal( scale=0.2, size=nd )

            self.ptest( days, flux, period=par[1], plot=False, verbose=False )
            print( "truth  :", fma( par ) )

        
    def ptest( self, days, flux, period=None, plot=0, verbose=False ) :

        ps = PeriodicScout( )

        per, scale = ps.findPeriod( days, flux, pmax=200, verbose=verbose )
        print( "Period   ", fma( per ), fma( scale ) )

        pars = ps.findParameters( days, flux, per, verbose=verbose )
        ecc, per, phase, incl, long, r1, r2, f1, f2 = pars

        print( "found  :", fma( pars ) )

        esm = EclipsingStarModel( spot=True )
        epar = [ecc, per, phase, incl, long, r1, r2, f1, f2, 0.0, 0.0 ]

        if plot : 
            plotEclipsingStar( esm, epar, xdata=days, ydata=flux )

        if period is not None :
            tol = 0.01
            assertAC( period, per, tol )


if __name__ == '__main__':
    unittest.main()

