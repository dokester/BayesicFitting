# run with : python3 -m unittest TestEclipsingStarModel

import unittest
import os
import math
import numpy as numpy
from numpy.testing import assert_array_almost_equal as assertAAE
from numpy.testing import assert_allclose as assertAC

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from StdTests import stdModeltest

from BayesicFitting import *
from BayesicFitting import formatter as fmt
from BayesicFitting import formatter_init

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
        formatter_init( linelength=100 )
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )


    def plot1( self ) :
        pi = numpy.pi
        m = EclipsingStarModel( spot=True )
        #                 
        ecc = 0.0
        per = 400 
        fas = 0.4 
        inc = 1.3
        lon = 1.0 
        r1  = 0.4  
        r2  = 0.1  
        L1  = 2.0 
        L2  = 0.6
        L3  = 0.0
        mr  = 0.5

        p = numpy.array( [ecc, per, fas, inc, lon, r1, r2, L1, L2] )

        pars = [ 0.283, 436.167, 3.489, 1.375, 0.168, 0.039, 0.233, 0.607, 7.371, 0.125, 0.011]
        p = pars
        p[-1] = 4.0
        p[-2] = 0.0
        #p[3] += pi/2
        #p[4] += pi
        #p[5], p[6] = ( p[6],p[5] )
        #p[7], p[8] = ( p[8],p[7] )


        m.reportParameters( p, stdevs=p )

        ax = plotEclipsingStar( m, p, show=self.doplot )

        t = numpy.linspace( 0, per, 361 )
        fp = m.fixpar( p )
        x, y, z = m.storbit.getOrbit( t, fp, d3=True )
        rxy = numpy.hypot( x, y )

        f1, f2 = m.spotIllumination( rxy, z, p )

        print( fmt( f1, tail=4 ) )
        print( fmt( f2, tail=4 ) )

        a1, b1, a2, b2 = m.tidalDistortion( rxy, z, p )

        t1, t2 = m.truemajor

        print( fmt( a1, tail=4 ) )
        print( fmt( b1, tail=4 ) )
        print( fmt( a2, tail=4 ) )
        print( fmt( b2, tail=4 ) )
        assertAAE( t1*b1*b1, numpy.ones_like( t1 ) )
        assertAAE( t2*b2*b2, numpy.ones_like( t2 ) )

#        ax.plot( t, f1, 'b-' )
#        ax.plot( t, f1 + f2, 'r-' )
#        ax = plt
        ax.plot( t, 6+a1, 'g-' )
        ax.plot( t, 6+b1, 'g:' )
        ax.plot( t, 6+a2, 'c-' )
        ax.plot( t, 6+b2, 'c:' )
        ax.plot( t, p[-3]*a2*b2, 'c.' )
        plt.show()



    def test1( self ):
        t  = numpy.linspace( 0, 1.0, 101, dtype=float )
        print( "******EclipsingStar test1***************" )
        p2 = numpy.pi * 2
        m = EclipsingStarModel(  )
        self.assertTrue( m.npars == 9 )
        self.assertTrue( m.npbase == 9 )
        par = [0.3, 1, 0.4, 1.5, 0.0, 0.4, 0.1, 3.0, 1.0]
        pran = numpy.array( [0.5, 1.0, p2, p2, p2, 0.5, 0.4, 5, 4] )


        if self.doplot :

            nk = 6
            dp = 1 / nk
            for n in range( 4,5 ) :
                td = numpy.array( [0, 0.2, 0.4, 0.6, 0.8] ) + 0.1
                p = par.copy()
                ax = plotEclipsingStar( m, p, td, show=False )
                for k in range( 1 ) :
                    r = m.result( t, p )
                    ax.plot( t, r, '-' )

                    x,y,z = m.storbit.getOrbit( t, m.fixpar( p ), d3=True )
                    plt.plot( t, x, 'r-' )
                    plt.plot( t, y, 'g-' )
                    plt.plot( t, z, 'b-' )

                ax.set_title( m.getParameterName( n ) )

            plt.show()


    def test2( self ):
        p2 = numpy.pi * 2
        tx = numpy.linspace( 0, 1.0, 101, dtype=float )
        print( "******EclipsingStar test2***************" )
        m = EclipsingStarModel(  )
        self.assertTrue( m.npars == 9 )
        self.assertTrue( m.npbase == 9 )
        p = numpy.array( [0.3, 1.0, 0.3, 1.5, p2, 0.35, 0.2, 5, 4.] )
#        p = numpy.array( [0.5, 1.0, p2, p2, p2, 0.5, 0.4, 5, 4] )
        p = numpy.array( [0.3, 1, 0.4, numpy.pi/2, 0.0, 0.4, 0.1, 3.0, 1.0] )

#        print( "tx   ", fma( tx ) )
        ty = m.result( tx, p )

#        print( "ty   ", fma( ty ) )

        if self.doplot :
            plt.plot( tx, ty, 'k.-' )
            plt.show()

#        stdModeltest( m, p, plot=self.doplot )

    def test3( self ):
        p2 = numpy.pi * 2
        tx = numpy.linspace( 0, 1.0, 7, dtype=float )
        print( "******EclipsingStar test3***************" )
        m = EclipsingStarModel(  )

        p = numpy.array( [0.3, 1.0, 0.3, 1.5, p2, 0.35, 0.2, 5, 4.] )
#        p = numpy.array( [0.0, 1, 0.0, numpy.pi/2, 0.0, 0.4, 0.1, 3.0, 1.0] )

        print( "tx   ", fma( tx ) )
        fp = m.fixpar( p )
        print( "fp   ", fma( fp ) )

        ty1 = m.storbit.result( tx, fp )
        ty1 = ty1.T
        print( "xy   ", fma( ty1, indent=6 ) )

        ty2 = m.storbit.getOrbit( tx, fp )
        print( "xy   ", fma( ty2, indent=6 ) )

        ty3 = m.storbit.getOrbit( tx, fp, d3=True )
        print( "xy   ", fma( ty3, indent=6 ) )

        assertAC( ty1, ty2 )
        assertAC( ty2, ty3[:2] )
        assertAC( ty3[:2], ty1 )


    def test4( self ):
        print( "******EclipsingStar test4***************" )

        tt = numpy.linspace( 0.0, 1.0, 101, dtype=float )
        m = EclipsingStarModel( spot=False )

        a80 = numpy.pi * 80 / 180
        par = numpy.array( [0.3, 1, 0.4, a80, 0.0, 0.4, 0.1, 3.0, 1.0] )
        self.dtest1( tt, m, par ) 

    def test4a( self ):
        print( "******EclipsingStar test4a  spot**************" )
        tt = numpy.linspace( 0.0, 1.0, 101, dtype=float )
        m = EclipsingStarModel( spot=True )
        a80 = numpy.pi * 80 / 180
        par = numpy.array( [0.3, 1, 0.4, a80, 0.0, 0.1, 0.4, 3.0, 1.0, 0.7] )
        tt += 0.003
        self.dtest1( tt, m, par ) 

    def test4b( self ):
        print( "******EclipsingStar test4b tides**************" )
        tt = numpy.linspace( 0.0, 1.0, 101, dtype=float )
        m = EclipsingStarModel( tides=True )
        a80 = numpy.pi * 80 / 180
        par = numpy.array( [0.3, 1, 0.4, a80, 0.0, 0.1, 0.4, 3.0, 1.0, 0.7 ] )

        tt += 0.003

        self.dtest1( tt, m, par ) 

    def test4c( self ):
        print( "******EclipsingStar test4c spot & tides******" )
        tt = numpy.linspace( 0.0, 1.0, 101, dtype=float )
        m = EclipsingStarModel( spot=1, tides=True )
        a80 = numpy.pi * 80 / 180
        par = numpy.array( [0.3, 1, 0.4, a80, 0.0, 0.1, 0.4, 3.0, 1.0, 0.7, 0.67] )
        tt += 0.003

        self.dtest1( tt, m, par ) 

    def test4d( self ):
        print( "******EclipsingStar test4d  circular**************" )
        tt = numpy.linspace( 0.0, 1.0, 101, dtype=float )
        m = EclipsingStarModel( circular=True )
        a80 = numpy.pi * 80 / 180
        par = numpy.array( [1, 0.4, a80, 0.1, 0.4, 3.0, 1.0] )

        m.reportParameters( par )
        
        tt += 0.003
        self.dtest1( tt, m, par ) 

        mc = m.copy()

        m.reportParameters( par, 0.02*par, toMags=1e-5 )
        
        tt += 0.003
        self.dtest1( tt, m, par ) 

    


    def test5( self ):
        print( "******EclipsingStar test5***************" )
        m = EclipsingStarModel( spot=True, tides=True, debug=True )

        a75 = numpy.pi * 75 / 180
        par = numpy.array( [0.2, 1, 0.4, a75, 0.0, 0.1, 0.4, 3.0, 1.0, 0.7, 0.67] )
        par = par[:m.npars]
        tt = numpy.linspace( 0., 1.0, 100, dtype=float ) + 0.001

        self.dtest2_TD( tt, m, par )
        self.dtest2_SI( tt, m, par ) 
        self.dtest1( tt, m, par ) 

    def test5a( self ):
        print( "******EclipsingStar test5 a*************" )
        m = EclipsingStarModel( spot=True, tides=True )

        a85 = numpy.pi * 85 / 180
        par = numpy.array( [0.3, 1, 0.4, a85, 0.0, 0.2, 0.1, 3.0, 1.0, 0.1, 0.55] )
        tt = numpy.linspace( 0., 1.0, 52, dtype=float )

        newL = m.distanceConstraint( 1.0, None, par, 0.0 )
        print( newL )

        self.dtest2_SI( tt, m, par ) 
        self.dtest2_LC( tt, m, par ) 
        self.dtest2_OV( tt, m, par ) 

        self.dtest2_TD( tt, m, par ) 

        plotEclipsingStar( m, par, show=self.doplot )
        plt.close()

    def test5b( self ):
        print( "******EclipsingStar test5 b*************" )
        tt = numpy.linspace( 0., 1.0, 101, dtype=float ) + 0.001

        m = EclipsingStarModel( debug=True )

        a85 = numpy.pi * 85 / 180
        par = numpy.array( [0.3, 1, 0.4, a85, 0.0, 0.2, 0.1, 3.0, 1.0] )
        par = par[:m.npars]

        m.partial( tt, par )
        self.dtest1( tt, m, par )

    def test5c( self ):
        print( "******EclipsingStar test5 b*************" )
        tt = numpy.linspace( 0., 1.0, 101, dtype=float ) + 0.001
        a85 = numpy.pi * 85 / 180
        par = numpy.array( [0.3, 1, 0.4, a85, 0.0, 0.3, 0.1, 2.0, 1.0, 0.8, 0.55] )

        m = EclipsingStarModel( spot=True, tides=True, debug=True )
#        m = EclipsingStarModel( spot=True, debug=True )
        par = par[:m.npars]

        m.partial( tt, par )
        self.dtest1( tt, m, par )

    def plottest8( self ):
        print( "******EclipsingStar plot 8***************" )

        t  = numpy.linspace( 0, 1.0, 101, dtype=float )
        m = EclipsingStarModel( spot=2, tides=True )

        a85 = numpy.pi * 65 / 180
        p1 = numpy.array( [0.0, 1, 0.0, a85, 0.0, 0.3, 0.2, 2.0, 1.0, 0.1, 0.55] )

        # plotEclipsingStar( m, p1 )
        for f in range( 6 ) :
            p1[4] = f
            y = m.result( t, p1 )
            plt.plot( t, y, 'k-' )
        plt.show()



    def test9( self ):
        print( "******EclipsingStar test 9***************" )

        m = EclipsingStarModel( spot=True, tides=True )

        a75 = numpy.pi * 75 / 180
        p1 = numpy.array( [0.3, 1, 0.4, a75, 0.7, 0.4, 0.1, 2.0, 1.0, 0.4, 0.3] )
        a85 = numpy.pi * 85 / 180
        p1 = numpy.array( [0.3, 1, 0.4, a85, 0.0, 0.3, 0.1, 2.0, 1.0, 0.1, 0.6] )

        m.reportParameters( p1, stdevs=0.1*p1, toMags=1e10 )


        t  = numpy.linspace( 0, 5.6, 101, dtype=float )
        numpy.random.seed( 12345 )
        y = m.result( t, p1 ) + numpy.random.randn( 101 ) * 0.2


        plotEclipsingStar( m, p1, xdata=t%p1[1], ydata=y, toMags=1e-8, show=self.doplot )
        plt.close()

        plotEsmSideView( m, p1, show=self.doplot )
        plt.close()

        plotEsmEclipseView( m, p1, show=self.doplot )
        plt.close()


    def plottest8( self ):
        print( "******EclipsingStar test8***************" )

        m = EclipsingStarModel( spot=2 )
        prob = ClassicProblem( model=m )

        NP = 100
        TWOPI = 2 * numpy.pi
        a75 = numpy.pi * 75 / 180
        par = numpy.array( [0.2, 1, 0.4, a75, 0.7, 0.4, 0.1, 2.0, 1.7, 0.4] )
        logL = numpy.zeros( NP, dtype=float ) + 10.0
        lowL = 2.0

        ecc  = numpy.linspace( 0.0, 0.9, NP )
        for k in range( NP ) :
            par[0] = ecc[k]
            logL[k] = m.distanceConstraint( logL[k], prob, par, lowL )
        plt.plot( ecc, logL, 'k-' )

        par[0] = 0.3
        logL = numpy.zeros( NP, dtype=float ) + 10.0
        inc  = numpy.linspace( 0.0, TWOPI, NP )
        for k in range( NP ) :
            par[3] = inc[k]
            logL[k] = m.distanceConstraint( logL[k], prob, par, lowL )
        plt.plot( ecc, logL, 'r-' )

        par[4] = 1.7
        logL = numpy.zeros( NP, dtype=float ) + 10.0
        fas  = numpy.linspace( 0.0, TWOPI, NP )
        for k in range( NP ) :
            par[3] = fas[k]
            logL[k] = m.distanceConstraint( logL[k], prob, par, lowL )
        plt.plot( ecc, logL, 'g-' )

        plt.show()


    def dtest2_LC( self, xdata, m, p, tol=0.001, verbose=False ) :

        print( "====== dtest 2 LightCurve ==============================" )

        kr = m.getParameterIndex( "radius_1" )
        plist = [k for k in range( kr, m.npars )]

        par = m.fixpar( p )
        x, y, z = m.storbit.getOrbit( xdata, par, d3=True )

        rxy = numpy.hypot( x, y )
        flc = m.lightCurve( rxy, z, p )

        dLCdr, dLCdz = m.LCderivative( rxy, z, p )

        xp = rxy + 0.0001
        xm = rxy - 0.0001

        yp = m.lightCurve( xp, z, p )
        ym = m.lightCurve( xm, z, p )
        nm1r = ( yp - ym ) / 0.0002

        if verbose :
            print( "rxy    ", fma( x, indent=8 ) )
            print( "z      ", fma( z, indent=8 ) )
            print( "fLC    ", fma( flc, indent=8 ) )

            print( "dLCdr  ", fma( dLCdr, indent=8 ) )
            print( "nmdr   ", fma( nm1r, indent=8 ) )

        zp = z + 0.0001
        zm = z - 0.0001

        yp = m.lightCurve( rxy, zp, p )
        ym = m.lightCurve( rxy, zm, p )
        nm1z = ( yp - ym ) / 0.0002

        self.assertPAC( dLCdr, nm1r, tol, mess="=== deriv XY" )
        self.assertPAC( dLCdz, nm1z, tol, mess="=== deriv Z"  )
    
        dF = m.LCpartial( rxy, z, p )

        #print( dF.shape )

        for n,k in enumerate( plist ) :
            pp = p.copy()
            pp[k] += 0.001
            pm = p.copy()
            pm[k] -= 0.001

            yp = m.lightCurve( rxy, z, pp )
            ym = m.lightCurve( rxy, z, pm )

            nm1p = ( yp - ym ) / 0.002

            msg = "=== %d = %d == %s ==============" % ( k, n, m.getParameterName( k ) )
            dF1 = dF[:,n]

            self.assertPAC( dF1, nm1p, tol, mess=msg )

    def assertPAC( self, df, nm, tol, mess='' ) :

        q = numpy.where( abs( df - nm ) > ( tol + tol * abs( nm ) ) )[0]
        if len( q ) > 0 :
            print( mess )
            print( "Have   ", fma( df, indent=8 ) )
            print( "Want   ", fma( nm, indent=8 ) )
            print( "errors at  ", fma( q[0], indent=12 ) )
        assertAC( df, nm, tol, tol )



    def SIplusTD( self, m, rxy, z, p, res=0 ) :
        """
        Combine tidalDistortion and spotIllumination.

        res = 0 : return result
        res = 1 : return derivative
        res = 2 : return partial
        """
        ## radii and luminosities of both stars
        r1 = m.getParameterValue( p, "radius_1" )
        r2 = m.getParameterValue( p, "radius_2" )

        ## Calculate tidal distortion: normalized apparent major and minor axis
        ## Need to be scaled with r1 or r2.
        tdresult = m.tidalDistortion( rxy, z, p )
        a1, b1, a2, b2 = tdresult

        ## Find overlap area between two circles of radius r1 and r2
        ##  at distances xy; r1,r2 depend on distortion
        ra1 = r1 * a1
        ra2 = r2 * a2

        f1, f2 = m.spotIllumination( rxy, z, p )

        surf1 = a1 * b1
        surf2 = a2 * b2
        surfs = ( surf1, surf2 )
        F1 = f1 * surf1
        F2 = f2 * surf2

        if res == 0 :
            return ( F1, F2 )

        ( df1dr1, df1dr2, df1df1, df1df2, df1dfs, df2dr1, df2dr2,
          df2df1, df2df2, df2dfs ) = m.SIpartial( rxy, z, p )

        ( dF1dr1, dF1dr2, dF1df1, dF1df2, dF1dfs, dF2dr1, dF2dr2,
          dF2df1, dF2df2, dF2dfs ) = m.SIpartial( rxy, z, p, surface=surfs )

        assertAC( dF1dr1, df1dr1 * surf1 )
        assertAC( dF2dr1, df2dr1 * surf2 )
        assertAC( dF1dr2, df1dr2 * surf1 )
        assertAC( dF2dr2, df2dr2 * surf2 )
        assertAC( dF1df1, df1df1 * surf1 )
        assertAC( dF2df1, df2df1 * surf2 )
        assertAC( dF1df2, df1df2 * surf1 )
        assertAC( dF2df2, df2df2 * surf2 )
        assertAC( dF1dfs, df1dfs * surf1 )
        assertAC( dF2dfs, df2dfs * surf2 )

        tdpart = m.TDpartial( rxy, z, p, TDresult=tdresult )
        da1dm, db1dm, da2dm, db2dm, da1dr, db1dr, da2dr, db2dr = tdpart

        ## Partials of surface to parameters r1, r2, m
        ## dSdr = a * dbdr + b * dadr
        dS1dr1 = a1 * db1dr + b1 * da1dr
        dS2dr2 = a2 * db2dr + b2 * da2dr
        dS1dmr = a1 * db1dm + b1 * da1dm
        dS2dmr = a2 * db2dm + b2 * da2dm

        dF1dr1 += f1 * dS1dr1
        dF1dr2 += f1 * dS2dr2
        dF2dr1 += f2 * dS1dr1
        dF2dr2 += f2 * dS2dr2
 
        dF1dmr = f1 * dS1dmr
        dF2dmr = f2 * dS2dmr
 
        return ( dF1dr1, dF1dr2, dF1df1, dF1df2, dF1dfs, dF1dmr, 
                 dF2dr1, dF2dr2, dF2df1, dF2df2, dF2dfs, dF2dmr )

    def dtest2_SITD( self, xdata, m, p, verbose=False ) :

        print( "====== dtest 2 spot + tides ==============================" )

        plist = [m.getParameterIndex("radius_1"), m.getParameterIndex("radius_2"), 
                 m.getParameterIndex("lumen_1"), m.getParameterIndex("lumen_2")]
        if m.spot :
            plist += [m.getParameterIndex("spot")]
        if m.tides : 
            plist += [m.getParameterIndex("massratio")]   

        par = m.fixpar( p )
        x, y, z = m.storbit.getOrbit( xdata, par, d3=True )
        rxy = numpy.hypot( x, y )

        F1,F2 = self.SIplusTD( m, rxy, z, p, res=0 )

        dF = self.SIplusTD( m, rxy, z, p, res=2 )

        for n,k in enumerate( plist ) :
            pp = p.copy()
            pp[k] += 0.001
            pm = p.copy()
            pm[k] -= 0.001

            yp = self.SIplusTD( m, rxy, z, pp, res=0 )
            ym = self.SIplusTD( m, rxy, z, pm, res=0 )

            nm1p = ( yp[0] - ym[0] ) / 0.002
            nm2p = ( yp[1] - ym[1] ) / 0.002

            dF1 = dF[n]
            dF2 = dF[n+6]

            if verbose :
                print( "=== %d = %d == %s ==============" % ( k, n, m.getParameterName( k ) ) )
                print( fma( pp ) )
                print( fma( pm ) )

                print( "df1dp  ", fma( dF1, indent=8 ) )
                print( "nm1p   ", fma( nm1p, indent=8 ) )
                print( "df2dp  ", fma( dF2, indent=8 ) )
                print( "nm2p   ", fma( nm2p, indent=8 ) )

            assertAAE( dF1, nm1p, 4 )
            assertAAE( dF2, nm2p, 4 )





    def dtest2_SI( self, xdata, m, p, verbose=False ) :

        print( "====== dtest 2 spotIllumination ==============================" )

        plist = [m.getParameterIndex("radius_1"), m.getParameterIndex("radius_2"), 
                 m.getParameterIndex("lumen_1"), m.getParameterIndex("lumen_2"), 
                 m.getParameterIndex("spot")]   
        #, m.getParameterIndex("distortion")]

        par = m.fixpar( p )
        x, y, z = m.storbit.getOrbit( xdata, par, d3=True )
        rxy = numpy.hypot( x, y )

        flc = m.spotIllumination( rxy, z, p )

        surfs = ( 1, 1 )
        df1dr, df2dr, df1dz, df2dz = m.SIderivative( rxy, z, p, surface=surfs )

        xp = rxy + 0.0001
        xm = rxy - 0.0001

        yp = m.spotIllumination( xp, z, p )
        ym = m.spotIllumination( xm, z, p )
        nm1r = ( yp[0] - ym[0] ) / 0.0002
        nm2r = ( yp[1] - ym[1] ) / 0.0002

        zp = z + 0.0001
        zm = z - 0.0001

        yp = m.spotIllumination( rxy, zp, p )
        ym = m.spotIllumination( rxy, zm, p )
        nm1z = ( yp[0] - ym[0] ) / 0.0002
        nm2z = ( yp[1] - ym[1] ) / 0.0002

        if verbose :
            print( "rxy    ", fma( x, indent=8 ) )
            print( "z      ", fma( z, indent=8 ) )
            print( "fSI   ", fma( flc, indent=7 ) )

            print( "df1dr  ", fma( df1dr, indent=8 ) )
            print( "nm1r   ", fma( nm1r, indent=8 ) )
            print( "df2dr  ", fma( df2dr, indent=8 ) )
            print( "nm2r   ", fma( nm2r, indent=8 ) )

            print( "df1dz  ", fma( df1dz, indent=8 ) )
            print( "nm1z   ", fma( nm1z, indent=8 ) )
            print( "df2dz  ", fma( df2dz, indent=8 ) )
            print( "nm2z   ", fma( nm2z, indent=8 ) )

        assertAAE( df1dr, nm1r, 4 )
        assertAAE( df1dz, nm1z, 4 )
        assertAAE( df2dr, nm2r, 4 )
        assertAAE( df2dz, nm2z, 4 )
    

        dF = m.SIpartial( rxy, z, p, surface=surfs )

        for n,k in enumerate( plist ) :
            pp = p.copy()
            pp[k] += 0.001
            pm = p.copy()
            pm[k] -= 0.001

            yp = m.spotIllumination( rxy, z, pp )
            ym = m.spotIllumination( rxy, z, pm )

            nm1p = ( yp[0] - ym[0] ) / 0.002
            nm2p = ( yp[1] - ym[1] ) / 0.002


            dF1 = dF[n]
            dF2 = dF[n+5]

            if verbose :
                print( "=== %d = %d == %s ==============" % ( k, n, m.getParameterName( k ) ) )
                print( fma( pp ) )
                print( fma( pm ) )
                print( "df1dp  ", fma( dF1, indent=8 ) )
                print( "nm1p   ", fma( nm1p, indent=8 ) )
                print( "df2dp  ", fma( dF2, indent=8 ) )
                print( "nm2p   ", fma( nm2p, indent=8 ) )

            assertAAE( dF1, nm1p, 4 )
            assertAAE( dF2, nm2p, 4 )

    def OVplusTD( self, m, rxy, z, p, res=0 ) :
        """
        Combine tidalDistortion and overlap.

        res = 0 : return result
        res = 1 : return derivative
        res = 2 : return partial
        """
        ## radii and luminosities of both stars
        r1 = m.getParameterValue( p, "radius_1" )
        r2 = m.getParameterValue( p, "radius_2" )

        ## Calculate tidal distortion: normalized apparent major and minor axis
        ## Need to be scaled with r1 or r2.
        tdresult = m.tidalDistortion( rxy, z, p )
        a1, b1, a2, b2 = tdresult

        ## Find overlap area between two circles of radius r1 and r2
        ##  at distances xy; r1,r2 depend on distortion
        ra1 = r1 * a1
        ra2 = r2 * a2

        ov = m.overlap( rxy, ra1, ra2 )
        if res == 0 :
            return ov

        tdderiv  = m.TDderivative( rxy, z, p, TDresult=tdresult )

        rr1 = ra1 * ra1
        rr2 = ra2 * ra2

        ## Take in account the dependency of r1,r2 on xy in tidalDistortion
        ## now also in z
        da1dx, db1dx, da2dx, db2dx, da1dz, db1dz, da2dz, db2dz = tdderiv

        dOdx = m.OVderivative( rxy, ra1, ra2 )
        dOdra1, dOdra2 = m.OVpartial( rxy, ra1, ra2 )

        dOdx += dOdra1 * r1 * da1dx + dOdra2 * r2 * da2dx
        dOdz  = dOdra1 * r1 * da1dz + dOdra2 * r2 * da2dz

        if res == 1 :
            return ( dOdx, dOdz )

        dOdra1, dOdra2 = m.OVpartial( rxy, ra1, ra2 )

        tdpart = m.TDpartial( rxy, z, p, TDresult=tdresult )
        da1dm, db1dm, da2dm, db2dm, da1dr, db1dr, da2dr, db2dr = tdpart

        ## Partials of overlap to parameters r1, r2, m
        ## dOdr = dOdra * dradr = dOdra * a
        dOdr1 = dOdra1 * ( a1 + r1 * da1dr )
        dOdr2 = dOdra2 * ( a2 + r2 * da2dr )

        ## dOdm = dOdra1 * dra1da1 * da1dm + dOdra2 * dra2da2 * da2dm
        dOdm  = dOdra1 * r1 * da1dm + dOdra2 * r2 * da2dm

        return ( dOdr1, dOdr2, dOdm )


    def dtest2_OV( self, xdata, m, p, verbose=False ) :

        print( "====== dtest 2 overlap ==============================" )


        par = m.fixpar( p )
        x, y, z = m.storbit.getOrbit( xdata, par, d3=True )
        rxy = numpy.hypot( x, y )

        ov = self.OVplusTD( m, rxy, z, p, res=0 )

        dOdx, dOdz = self.OVplusTD( m, rxy, z, p, res=1 )

        xp = rxy + 0.0001
        xm = rxy - 0.0001

        yp = self.OVplusTD( m, xp, z, p )
        ym = self.OVplusTD( m, xm, z, p )
        nm1r = ( yp - ym ) / 0.0002

        zp = z + 0.0001
        zm = z - 0.0001

        yp = self.OVplusTD( m, rxy, zp, p )
        ym = self.OVplusTD( m, rxy, zm, p )
        nm1z = ( yp - ym ) / 0.0002

        if verbose :
            print( "rxy    ", fma( x, indent=8 ) )
            print( "z      ", fma( z, indent=8 ) )
            print( "over   ", fma( ov, indent=8 ) )

            print( "dOdr   ", fma( dOdx, indent=8 ) )
            print( "nm1r   ", fma( nm1r, indent=8 ) )

            print( "dOdz   ", fma( dOdz, indent=8 ) )
            print( "nm1z   ", fma( nm1z, indent=8 ) )

        assertAAE( dOdx, nm1r, 4 )
        assertAAE( dOdz, nm1z, 4 )
    
        plist = [m.getParameterIndex("radius_1"), m.getParameterIndex("radius_2"), 
                 m.getParameterIndex("mass_1")]

        dO = self.OVplusTD( m, rxy, z, p, res=2 )

        for n,k in enumerate( plist ) :
            pp = p.copy()
            pp[k] += 0.001
            pm = p.copy()
            pm[k] -= 0.001

            yp = self.OVplusTD( m, rxy, z, pp )
            ym = self.OVplusTD( m, rxy, z, pm )

            nm1p = ( yp - ym ) / 0.002

            if verbose :
                print( "=== %d = %d == %s ==============" % ( k, n, m.getParameterName( k ) ) )
    
                print( "dOdp   ", fma( dO[n], indent=8 ) )
                print( "nm1p   ", fma( nm1p, indent=8 ) )

            assertAAE( dO[n], nm1p, 3 )


    def dtest2_TD( self, xdata, m, p, verbose=False ) :

        print( "====== dtest 2 tidalDistortion ==============================" )

        Tools.printclass( m )
        self.assertTrue( m.tides )
        self.assertTrue( m.npars == 11 )
        par = m.fixpar( p )
        x, y, z = m.storbit.getOrbit( xdata, par, d3=True )
        rxy = numpy.hypot( x, y )

        if verbose :
            print( "par   ", fma( p ) )
            print( "rxy   ", fma( rxy, indent=7 ) )
            print( "z     ", fma( z, indent=7 ) )

        self.dtest2_TD_derv( rxy, z, m, p, verbose=verbose )
        self.dtest2_TD_part( rxy, z, m, p, verbose=verbose )

    def dtest2_TD_derv( self, rxy, z, m, p, verbose=False ) :

        if verbose :
            print( "====== dtest 2 TDderiv ==============================" )

        tdresult = m.tidalDistortion( rxy, z, p )
        a1, b1, a2, b2 = tdresult
        t1, t2 = m.truemajor

        if verbose :
            print( "a1    ", fma( a1, indent=7 ) )
            print( "t1    ", fma( t1, indent=7 ) )
            print( "b1    ", fma( b1, indent=7 ) )
            print( "a2    ", fma( a2, indent=7 ) )
            print( "t2    ", fma( t2, indent=7 ) )
            print( "b2    ", fma( b2, indent=7 ) )

            print( "par   ", fma( p ) )

        tdder = m.TDderivative( rxy, z, p, TDresult=tdresult )

        dt1dx = -2 * b1**(-3) * tdder[1]
        dt2dx = -2 * b2**(-3) * tdder[3]
        dt1dz = -2 * b1**(-3) * tdder[5]
        dt2dz = -2 * b2**(-3) * tdder[7]

        dt1 = ( dt1dx, dt1dz )
        dt2 = ( dt2dx, dt2dz )

        name = ["da1d%s", "db1d%s", "da2d%s", "db2d%s"]

        k = 0
        c = "xy"

        for ki in range( 2 ) :
            if ki == 0 :
                xp = rxy + 0.0001
                xm = rxy - 0.0001
                yp = m.tidalDistortion( xp, z, p )
                t1p, t2p = m.truemajor
                ym = m.tidalDistortion( xm, z, p )
                t1m, t2m = m.truemajor
            else :
                zp = z + 0.0001
                zm = z - 0.0001
                yp = m.tidalDistortion( rxy, zp, p )
                t1p, t2p = m.truemajor
                ym = m.tidalDistortion( rxy, zm, p )
                t1m, t2m = m.truemajor

            nmt1 = ( t1p - t1m ) / 0.0002
            nmt2 = ( t2p - t2m ) / 0.0002

            if verbose :
                print( "dt1d%s" % c, " ", fma( dt1[ki], indent=9 ) )
                print( "num%s" % c, "  ", fma( nmt1, indent=9 ) )
                print( "dt2d%s" % c, " ", fma( dt2[ki], indent=9 ) )
                print( "num%s" % c, "  ", fma( nmt2, indent=9 ) )

            tol = 0.01
            assertAC( dt1[ki], nmt1, tol, tol )
            assertAC( dt2[ki], nmt2, tol, tol )
            n = 0
            for pp, mm in zip( yp, ym ) :
                nmr = ( pp - mm ) / 0.0002
#                print( name[n] % c, " ", fma( tdder[k], indent=9 ) )
#                print( "num%s" % c, "  ", fma( nmr, indent=9 ) )
                assertAC( tdder[k], nmr, tol, tol )
                k += 1
                n += 1
            c = "z "

    def dtest2_TD_part( self, rxy, z, m, p, verbose=False ) :

        if verbose :
            print( "====== dtest 2 TDpart  ==============================" )

        tdresult = m.tidalDistortion( rxy, z, p )
        a1, b1, a2, b2 = tdresult
        t1, t2 = m.truemajor

        tdpart = m.TDpartial( rxy, z, p )
        da1dm, db1dm, da2dm, db2dm,  da1dr, db1dr, da2dr, db2dr = tdpart

        r1 = m.getParameterIndex( "radius_1" )
        r2 = m.getParameterIndex( "radius_2" )
        m1 = m.getParameterIndex( "mass_1" )

        name = ["da1d%s", "db1d%s", "da2d%s", "db2d%s"]
        pl = [m1,r1,r2]
        cc = ["m1","r1","r2"]
        k = 0
        tol = 0.01
        for ck, ki in zip( cc, pl ) :
            print( "=== %d === %s ==============" % ( ki, m.getParameterName( ki ) ) )
            pp = p.copy()
            pm = p.copy()
            pp[ki] += 0.0001
            pm[ki] -= 0.0001

            yp = m.tidalDistortion( rxy, z, pp )
            ym = m.tidalDistortion( rxy, z, pm )
            n = 0
            for rp, rm in zip( yp, ym ) :
                nmr = ( rp - rm ) / 0.0002
                if ( ki == r1 and n <= 1 ) or ( ki == r2 and n >= 2 ) or ( ki == m1 ) :
                    if verbose :
                        print( name[n] % ck, " ", fma( tdpart[k], indent=9 ) )
                    assertAC( tdpart[k], nmr, tol, tol )
                    k += 1
                if verbose :
                    print( "dnum%s" % ck, " ", fma( nmr, indent=9 ) )
                n += 1



    def dtest1( self, x, m, p, verbose=False ) :

        self.dtest1_deriv( x, m, p, verbose=verbose )

        self.dtest1_part( x, m, p, verbose=verbose )


    def dtest1_deriv( self, x, m, p, verbose=False ) :

        print( "====== dtest 1 derivative ==============================" )

        r = m.result( x, p )

        if verbose :
            print( "t    ", fma( x ) )
            print( "r    ", fma( r ) )

        dfdx = m.derivative( x, p )

        xp = x + 0.0001
        xm = x - 0.0001

        yp = m.result( xp, p )
        ym = m.result( xm, p )
 
        numx = ( yp - ym ) / 0.0002

        tol = 0.01
        q = numpy.where( abs( dfdx - numx ) > ( tol + tol * abs( numx ) ) )[0]
        if verbose :
            print( "dx     ", fma( dfdx, indent=8 ) )
            print( "nm     ", fma( numx, indent=8 ) )
            if len( q ) > 0 :               
                print( "errors at  ", fma( q, indent=12 ) )

        assertAC( dfdx, numx, tol, tol, verbose=verbose )

    def dtest1_part( self, x, m, p, verbose=False ) :

        print( "====== dtest 1 partial  ==============================" )
        
        dF = m.partial( x, p )
        #print( dF.shape )

        n = 0
        tol = 0.01
        for k in range( len( p ) ) :
            pp = p.copy()
            pp[k] += 0.0001
            pm = p.copy()
            pm[k] -= 0.0001

            yp = m.result( x, pp )
            ym = m.result( x, pm )

            nm1p = ( yp - ym ) / 0.0002

            dFk = dF[:,k]
            if verbose :
                print( "=== %d === %s ==============" % ( k, m.getParameterName( k ) ) )
                print( "dfdp%d  "%k, fma( dFk, indent=8 ) )
                print( "nump%d  "%k, fma( nm1p, indent=8 ) )
#            km = numpy.argmax( abs( dFk - nm1p ) )
#            print( "maxdif ", km, dFk[km], nm1p[km], dFk[km] - nm1p[km] )

            assertAC( dFk, nm1p, tol, tol, verbose=verbose )



    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestEclipsingStarModel.__class__ )

if __name__ == '__main__':
    unittest.main( )


