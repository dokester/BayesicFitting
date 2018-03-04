# helper methods for Model testing

from __future__ import print_function
import unittest
import numpy as numpy
from astropy import units
from numpy.testing import assert_array_almost_equal as assertAAE
from numpy.testing import assert_array_equal as assertAE

import matplotlib.pyplot as plt
import warnings

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

def classequal( cls1, cls2 ) :
    tc = unittest.TestCase()

    atr1 = vars( cls1 )
    ld1 = list( atr1.keys() )
    ld1.sort()
    atr2 = vars( cls2 )
    ld2 = list( atr2.keys() )
    ld2.sort()
    assertAE( ld1, ld2 )
    for key1,key2 in zip( ld1, ld2 ) :
        val1 = atr1[key1]
        val2 = atr2[key2]
#        print( "Cls1  ", key1, val1 )
#        print( "Cls2  ", key2, val2 )
        if isinstance( val1, (list, numpy.ndarray) ) :
            assertAE( val1, val2 )
        elif isinstance( val1, ( int, float, str ) ) :
            tc.assertTrue( val1 == val2 )

#    print( "Both classes equal" )


def stdModeltest( model, par, x=None, plot=None, warn=[] ):
        tc = unittest.TestCase()

        print( "***StdModelTest***************" )
        if x is None :
            x  = numpy.asarray( [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )

        Tools.printclass( model )
        if "nopart" in warn :
            print( par )
            tc.assertWarns( UserWarning, model.basePartial, x, par )
            print( model.shortName() + ": Further no-partial warnings ignored." )
            warnings.simplefilter( "ignore" )

        numpy.set_printoptions( precision=3, suppress=True )
        print( "result:\n", model.result( x, par ) )

        print( "partial:\n", model.partial( x, par ) )

        tc.assertTrue( model.testPartial( x[1], par ) == 0 )
        tc.assertTrue( model.testPartial( x[4], model.parameters ) == 0 )

        tc.assertTrue( model.testPartial( x[1], par ) == 0 )
        model.xUnit = units.m
        model.yUnit = units.kg
        print( model.parlist )
        for k in range( model.getNumberOfParameters() ):
            print( "%d  %-12s  %-12s"%(k, model.getParameterName( k ),
                    model.getParameterUnit( k ) ) )

        print( "Integral   ", model.getIntegralUnit( ) )
        tc.assertTrue( model.testPartial( x, par ) == 0 )
        """
        part = model.partial( x, par )
        nump = model.numPartial( x, par )
        k = 0
        for (pp,nn) in zip( part.flatten(), nump.flatten() ) :
            print( k, pp, nn )
            tc.assertAlmostEqual( pp, nn, 3 )
            k += 1
        """
        mc = model.copy( )
#        Tools.printclass( model )
#        Tools.printclass( mc )
        classequal( model, mc )
        print( "model and copy are the same" )


        for k in range( mc.getNumberOfParameters() ):
            print( "%d  %-12s  %-12s"%(k, mc.getParameterName( k ), mc.getParameterUnit( k ) ) )
        mc.parameters = par
        model.parameters = par

        for (k,xk,r1,r2) in zip( range( x.size ), x, model.result( x ), mc.result( x ) ) :
            print( "%3d %8.3f  %10.3f %10.3f" % ( k, xk, r1, r2 ) )
            tc.assertAlmostEqual( r1, r2 )
        tc.assertTrue( mc.testPartial( x, par ) == 0 )

        if plot :
            plotModel( model, par, xx=x )


def std2dModeltest( model, par, x=None, plot=None, warn=[] ):
        tc = unittest.TestCase()
        numpy.set_printoptions( precision=3, suppress=True )

        print( "***Std2dModelTest***************" )
        if x is None :
            x  = numpy.asarray( [[-1.0, -0.8], [-0.6, -0.4], [-0.2, 0.0], [0.2, 0.4], [0.6, 0.8]] )

        Tools.printclass( model )

        if "nopart" in warn :
            tc.assertWarns( UserWarning, model.basePartial, x, par )
            print( model.shortName() + ": Further no-partial warnings ignored." )
            warnings.simplefilter( "ignore" )

        tc.assertTrue( model.ndim == 2 )

        print( model.result( x, par ) )

        print( model.partial( x, par ) )
        print( x[5] )
        print( "npchain  ", model.npchain )
        tc.assertTrue( model.testPartial( x[5], model.parameters ) == 0 )

        tc.assertTrue( model.testPartial( x[1], par ) == 0 )
        model.xUnit = units.m
        model.yUnit = units.kg
        for k in range( model.getNumberOfParameters() ):
            print( "%d  %-12s  %-12s"%(k, model.getParameterName( k ),
                    model.getParameterUnit( k ) ) )

        print( "Integral   ", model.getIntegralUnit( ) )
        tc.assertTrue( model.testPartial( x, par ) == 0 )
        """
        part = model.partial( x, par )
        nump = model.numPartial( x, par )
        k = 0
        for (pp,nn) in zip( part.flatten(), nump.flatten() ) :
            print( k, pp, nn )
            tc.assertAlmostEqual( pp, nn, 3 )
            k += 1
        """
        mc = model.copy( )
        classequal( model, mc )
        print( "model and copy are the same" )


        for k in range( mc.getNumberOfParameters() ):
            print( "%d  %-12s  %-12s"%(k, mc.getParameterName( k ), mc.getParameterUnit( k ) ) )
        mc.parameters = par
        model.parameters = par
#        Tools.printclass( model )
#        Tools.printclass( mc )

        for (k,xk,r1,r2) in zip( range( x.size ), x, model.result( x ), mc.result( x ) ) :
            print( "%3d " % k, end="" )
            if model.ndim == 1 :
                print( "%8.3f  " % xk, end="" )
            else :
                for xki in xk :
                    print( "%8.3f " % xki, end="" )
            print( "  %10.3f %10.3f" % ( r1, r2 ) )
            tc.assertAlmostEqual( r1, r2 )
        tc.assertTrue( mc.testPartial( x, par ) == 0 )

        if plot :
            plotModel( model, par, xx=x )

def plotModel( model, par, xx=None ) :
        print( xx )
        if xx is None :
            xx = numpy.linspace( -1, +1, 1001 )
            x2 = numpy.linspace( -1, +1, 11 )
            nx = 11
            ff = 1
        else :
            x2 = xx
            nx = xx.size
            mnx = numpy.min( xx )
            mxx = numpy.max( xx )
            ff = 0.5 * ( mxx - mnx )
            xx = numpy.linspace( mnx, mxx, 100 * nx, dtype=float )
        print( xx )
        plt.plot( xx, model.result( xx, par ), '-', linewidth=2 )
        try :
            dy = model.derivative( x2, par )
            yy = model.result( x2, par )
            for k in range( nx ) :
                x3 = numpy.asarray( [-0.05, +0.05] ) * ff
                y3 = x3 * dy[k] + yy[k]
                plt.plot( x2[k] + x3, y3, 'r-' )
        except :
            print( "No derivative" )
            pass
        plt.show()

def stdFittertest( myfitter, npt, xmin=-10.0, xmax=10.0, noise=0.1, plot=False,
            map=False, keep=None, errdis=None, scale=None, power=2.0, options={} ) :

    numpy.set_printoptions( precision=3, suppress=True )
    tc = unittest.TestCase()

    ## make data
    x = numpy.linspace( xmin, xmax, npt, dtype=float )
    m = SincModel()
    p = [3.0, 1.0, 2.0]
    ym = m.result( x, p )
    numpy.random.seed( 5753258 )
    y = ym + noise * numpy.random.randn( npt )

    knots = numpy.linspace( xmin, xmax, 13, dtype=float )
    lmdl = BSplinesModel( knots )

    lftr = Fitter( x, lmdl )
    lpar = lftr.fit( y )
    lchi = lftr.chisq
    lfit = lmdl( x )


    mdl = BSplinesModel( knots )
    ftr = myfitter( x, mdl, map=map, keep=keep, errdis=errdis, scale=scale, power=power )

    print( "###############  Test ", ftr, '  ###################################' )

    par = ftr.fit( y, **options )
    chi = ftr.chisq
    yfit = mdl( x )

    print( "lpar ", fmt( lpar, indent=4 ) )
    print( "lstd ", fmt( lftr.stdevs, indent=4 ) )
    print( "lchi ", fmt( lchi ), "  scale ", fmt( lftr.scale ) )

    print( "par   ", fmt( par, indent=4 ) )
    print( "std   ", fmt( ftr.stdevs, indent=4 ) )
    print( "chi   ", fmt( chi ), "  scale ", fmt( ftr.scale ),  "  iter ", fmt( ftr.iter ) )

    lmce = ftr.monteCarloError( x )

#    tc.assertTrue( abs( lchi - chi ) < noise )
#    tc.assertTrue( numpy.all( numpy.abs( yfit - lfit ) < 2 * lmce ) )

    if plot :
        plt.figure( str( ftr ) )
        plt.plot( x, ym, 'k-' )
        plt.plot( x, y, 'k*' )
        plt.plot( x, lfit, 'g-' )
        plt.plot( x, yfit, 'r-' )
        plt.plot( x, yfit - lmce, 'm-' )
        plt.plot( x, yfit + lmce, 'm-' )


