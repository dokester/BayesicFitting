# run with : python3 -m unittest TestKepplers2ndLaw

import unittest
import os
import numpy as numpy
import math
from astropy import units
import matplotlib.pyplot as plt
import warnings
from numpy.testing import assert_array_almost_equal as assertAAE

from StdTests import stdModeltest

from BayesicFitting import *
from BayesicFitting import formatter as fmt

__author__ = "Do Kester"
__year__ = 2019
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

class TestKepplers2ndLaw( unittest.TestCase ):
    """
    Test harness for Kepplers 2nd law

    Author:      Do Kester

    """
    TWOPI = 2 * math.pi

    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )

    def test1( self ):
        x  = numpy.linspace( 0.0, 10, 101, dtype=float )
        print( "******KEPPLERS LAW***************" )
        KL = Kepplers2ndLaw( )

        # eccen, semimajor, period, periastron
        p = [0.0, 1.0, 10.0, 0.0]
        m = KL.meanAnomaly( x, p )
        e = KL.eccentricAnomaly( x, p )
        r, v = KL.radiusAndTrueAnomaly( x, p )
        v = numpy.where( v < 0, v + self.TWOPI, v )
        print( "Mean ", fmt( m ) )
        print( "Ecce ", fmt( e ) )
        print( "True ", fmt( v ) )
        print( "Rad  ", fmt( r ) )

        se = KL.sinE
        ce = KL.cosE

        for k in range( 101 ) :
            print( fmt(k), fmt(m[k]), fmt(e[k]), fmt(v[k]), fmt(se[k]), fmt(ce[k]) )

        assertAAE( m, e )
        assertAAE( e, v )
        x0 = r * numpy.cos( v )
        y0 = r * numpy.sin( v )


        p = [0.5, 0.8, 1.4, 1.3]
        m = KL.meanAnomaly( x, p )
        e = KL.eccentricAnomaly( x, p )
        r, v = KL.radiusAndTrueAnomaly( x, p )
        v = numpy.where( v < 0, v + self.TWOPI, v )
        print( "Mean ", fmt( m ) )
        print( "Ecce ", fmt( e ) )
        print( "True ", fmt( v ) )
        print( "Rad  ", fmt( r ) )
        x1 = r * numpy.cos( v )
        y1 = r * numpy.sin( v )


        if self.doplot :
            plt.figure( 1, figsize=[6,6] )
            plt.plot( x0, y0, 'k-' )
            plt.plot( x1, y1, 'r-' )

            plt.show()

    def test2( self ):
        x  = numpy.linspace( 0, 10, 1001, dtype=float )
        print( "******KEPPLERS LAW test 2***************" )
        KL = Kepplers2ndLaw( )

        # eccen, semimajor, period, periastron
        p = [0.0, 1.0, 10.0, 0.0]
        e2 = None
        for k in range( 10 ) :
            e0 = KL.eccentricAnomaly0( x, p )
            i0 = KL.iter
            e1 = KL.eccentricAnomaly1( x, p )
            i1 = KL.iter
            e2 = KL.eccentricAnomaly2( x, p, Estart=e2 )
            i2 = KL.iter
            print( "Eccentricity  ", fmt(p[0]), fmt(i0), fmt(i1), fmt(i2) )
            p[0] += 0.1


        p[0] = 0.6
        e = KL.eccentricAnomaly( x, p, Estart=e2 )
        print( "Eccentricity  ", fmt(p[0]), "                   ", fmt( KL.iter ) )
        p[0] = 0.999999999
        e = KL.eccentricAnomaly( x, p, Estart=e2 )
        print( "Eccentricity  ", p[0], "                 ", fmt( KL.iter ) )

    def test3( self ):
        x  = numpy.linspace( 0, 10, 1001, dtype=float )
        print( "******KEPPLERS LAW test 3***************" )
        KL = Kepplers2ndLaw( )

        # eccen, semimajor, period, periastron
        p = [0.0, 2.0, 10.0, 0.0]

        for k in range( 10 ) :
            r, v = KL.radiusAndTrueAnomaly( x, p )

            a = 0.5 * ( r[0] + r[501] )
            b = math.sqrt( r[0] * r[501] )
            e = math.sqrt( a * a - b * b ) / a

            xx = r * numpy.cos( v )
            yy = r * numpy.sin( v )

            if self.doplot :
                plt.plot( xx, yy )

            print( fmt( p[0] ), fmt( e ), fmt( a ), fmt( b ), fmt( KL.iter ) )
            assertAAE( p[0], e )

            p[0] += 0.1

        if self.doplot :
            plt.plot( [0], [0], 'k.' )
            plt.show()


    def test4( self ):
        x  = numpy.linspace( 0, 10, 11, dtype=float )
        xp = x + 0.0001
        xm = x - 0.0001
        print( "******KEPPLERS LAW test 4***************" )
        KL = Kepplers2ndLaw( )

        print( "  Derivatives to x" )
        # eccen, semimajor, period, periastron
        p = [0.2, 2.0, 10.0, 0.3]

        mp = KL.meanAnomaly( xp, p )
        mm = KL.meanAnomaly( xm, p )
        nm = ( mp - mm ) / 0.0002
        dm = KL.dMdx( x, p )
        print( "dMdx  ", fma( dm ) )
        print( "Numer ", fma( nm ) )
        assertAAE( dm, nm )

        ep = KL.eccentricAnomaly( xp, p )
        em = KL.eccentricAnomaly( xm, p )
        ea = KL.eccentricAnomaly( x, p )
        cosE = numpy.cos( ea )
        ne = ( ep - em ) / 0.0002
        de = KL.dEdx( x, p, cosE )
        print( "dEdx  ", fma( de ) )
        print( "Numer ", fma( ne ) )
        assertAAE( de, ne )

        rp, vp = KL.radiusAndTrueAnomaly( xp, p )
        rm, vm = KL.radiusAndTrueAnomaly( xm, p )
        nr = ( rp - rm ) / 0.0002
        nv = ( vp - vm ) / 0.0002
        sinE = numpy.sin( ea )
        dr, dv = KL.drvdx( x, p, cosE, sinE )
        print( "drdx  ", fma( dr ) )
        print( "Numer ", fma( nr ) )
        assertAAE( dr, nr )
        print( "dvdx  ", fma( dv ) )
        print( "Numer ", fma( nv ) )
        assertAAE( dv, nv )


        print( "  Partials to parameters" )
        drde, drda, drdP, drdp, dvde, dvdP, dvdp = KL.drvdpar( x, p, ea, cosE, sinE )

        pp = p[:]
        pp[0] += 0.0001
        pm = p[:]
        pm[0] -= 0.0001

        rp, vp = KL.radiusAndTrueAnomaly( x, pp )
        rm, vm = KL.radiusAndTrueAnomaly( x, pm )
        nr = ( rp - rm ) / 0.0002
        nv = ( vp - vm ) / 0.0002

        print( "drde  ", fma( drde ) )
        print( "Numer ", fma( nr ) )
        assertAAE( drde, nr )
        print( "dvde  ", fma( dvde ) )
        print( "Numer ", fma( nv ) )
        assertAAE( dvde, nv )

        pp = p[:]
        pp[1] += 0.0001
        pm = p[:]
        pm[1] -= 0.0001

        rp, vp = KL.radiusAndTrueAnomaly( x, pp )
        rm, vm = KL.radiusAndTrueAnomaly( x, pm )
        nr = ( rp - rm ) / 0.0002
        nv = ( vp - vm ) / 0.0002

        print( "drda  ", fma( drda ) )
        print( "Numer ", fma( nr ) )
        assertAAE( drda, nr )
        dvda = numpy.zeros_like( drda )
        print( "dvda  ", fma( dvda ) )
        print( "Numer ", fma( nv ) )
        assertAAE( dvda, nv )

        pp = p[:]
        pp[2] += 0.0001
        pm = p[:]
        pm[2] -= 0.0001

        rp, vp = KL.radiusAndTrueAnomaly( x, pp )
        rm, vm = KL.radiusAndTrueAnomaly( x, pm )
        nr = ( rp - rm ) / 0.0002
        nv = ( vp - vm ) / 0.0002

        print( "drdP  ", fma( drdP ) )
        print( "Numer ", fma( nr ) )
        assertAAE( drdP, nr )
        print( "dvdP  ", fma( dvdP ) )
        print( "Numer ", fma( nv ) )
        assertAAE( dvdP, nv )

        pp = p[:]
        pp[3] += 0.0001
        pm = p[:]
        pm[3] -= 0.0001

        rp, vp = KL.radiusAndTrueAnomaly( x, pp )
        rm, vm = KL.radiusAndTrueAnomaly( x, pm )
        nr = ( rp - rm ) / 0.0002
        nv = ( vp - vm ) / 0.0002

        print( "drdp  ", fma( drdp ) )
        print( "Numer ", fma( nr ) )
        assertAAE( drdp, nr )
        print( "dvdp  ", fma( dvdp ) )
        print( "Numer ", fma( nv ) )
        assertAAE( dvdp, nv )



    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestKepplers2ndLaw.__class__ )

if __name__ == '__main__':
    unittest.main( )


