#!/usr/bin/env python

import numpy as numpy
import math as math
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from numpy.testing import assert_array_almost_equal as assertAAE

# This file is part of the BayesicFitting package.
#
# BayesicFitting is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or ( at your option ) any later version.
#
# BayesicFitting is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# The GPL3 license can be found at <http://www.gnu.org/licenses/>.
#
# 2016 Do Kester

def plotFit( x, data=None, model=None, ftr=None, truth=None, show=True,
             residuals=False ) :

    minx = numpy.min( x )
    maxx = numpy.max( x )
    np = 1
    plt.figure( "fit" )
    ax0 = plt

    if residuals :
        plt.subplots_adjust( hspace=0.001 )
        np = 2
        gs = gridspec.GridSpec( 2, 1, height_ratios=[4, 1])

        ax1 = plt.subplot( gs[1] )
        yfit = model( x )
        res = data - yfit
        ax1.plot( x, res, 'k-' )
        ax1.margins( 0.05, 0.05 )
        plt.ylabel( "residual" )
        plt.xlabel( "x" )

        ax0 = plt.subplot( gs[0] )
        xticklabels = ax0.get_xticklabels()
        plt.setp( xticklabels, visible=False )

    if truth is not None :
        ax0.plot( x, truth, 'b+' )
    if data is not None :
        ax0.plot( x, data, 'k.' )

    if model is not None :
        xx = numpy.linspace( minx, maxx, 10 * len( x ) )
        yy = model( xx )
        if ftr is not None :
            err = ftr.monteCarloError( xx )
            ax0.plot( xx, yy - err, 'g-' )
            ax0.plot( xx, yy + err, 'g-' )
        ax0.plot( xx, yy, 'r-' )

    ax0.margins( 0.05, 0.05 )
    plt.ylabel( "y" )
    if not residuals :
        plt.xlabel( "x" )

    if show :
        plt.show()

def plotModel( model, par ) :
    xx = numpy.linspace( -1, +1, 1001 )
    plt.plot( xx, model.result( xx, par ), '-', linewidth=2 )
    x2 = numpy.linspace( -1, +1, 11 )
    dy = model.derivative( x2, par )
    yy = model.result( x2, par )
    for k in range( 11 ) :
        x3 = numpy.asarray( [-0.05, +0.05] )
        y3 = x3 * dy[k] + yy[k]
        plt.plot( x2[k] + x3, y3, 'r-' )

    plt.show()




def plotErrdis( errdis, model, limits=[-10,10], max=None, plot=None ) :
    np = 2001
    map = numpy.ndarray( np, dtype=float )

    par = model.parameters
    pars = numpy.append( par, errdis.hypar )
    r0 = numpy.linspace( limits[0], limits[1], np, dtype=float )

    for k, p in enumerate( r0 ) :
        pars[0] = p
        map[k] = errdis.logLikelihood( model, pars )

    if max is None :
        max = numpy.max( map )

    map = numpy.exp( map - max )
    if plot :
        plt.figure( str( errdis ) )
        plt.plot( r0, map, 'k-' )

    return ( math.log( numpy.sum( map ) / np ) + max, max )


def plotErrdis2d( errdis, model, limits=[-10,10], nslim=None, max=None,
                plot=None ) :

    np = 201
    map = numpy.ndarray( (np,np), dtype=float )

    par = model.parameters
    pars = numpy.append( par, errdis.hypar )
    r0lo = limits[0]
    r0hi = limits[1]
    r0 = numpy.linspace( r0lo, r0hi, np, dtype=float )
    if nslim is None :
        r1lo, r1hi = ( r0lo, r0hi )
        r1 = numpy.linspace( r1lo, r1hi, np, dtype=float )
        prior1 = numpy.zeros_like( r1 ) + 1 / ( r1hi - r1lo )
    else :
        r1lo, r1hi = ( nslim[0], nslim[1] )
        r1 = numpy.linspace( r1lo, r1hi, np, dtype=float )
        cp = math.log( r1hi / r1lo )                # integral of Jeffreys
        prior1 = 1 / ( cp * r1 )


    pixsz = ( r0hi - r0lo ) * ( r1hi - r1lo ) / ( np * np )
    prior0 = numpy.zeros_like( r0 ) + 1 / ( r0hi - r0lo )
    prior = numpy.outer( prior1, prior0 ) * pixsz
    zp = numpy.sum( prior )
#    print( numpy.sum( prior0 ), numpy.sum( prior1 ), zp )
    assertAAE( zp, 1.0, 2 )

#    print( prior.shape, prior[0,0], ( 1.0/ ( r0hi - r0lo ) ) )

    for k1,p1 in enumerate( r1 ) :
        pars[1] = p1
        for k0,p0 in enumerate( r0 ) :
            pars[0] = p0
            map[k1,k0] = errdis.logLikelihood( model, pars )

    logl = numpy.max( map )
#    print( prior.shape, prior[0,0], 2*math.log( 1.0/ ( r0hi - r0lo ) ) )
#    print( pixsz )

    map += numpy.log( prior )

    if max is None :
        max = numpy.max( map )

    map = numpy.exp( map - max )

    if plot :
        plt.figure( str( errdis ) )

        # More colormaps in matplotlib: docs->Matplotlib examples->color Examples

        plt.imshow( map, aspect=None, cmap='viridis', origin='lower',
                extent=(r0lo,r0hi,r1lo,r1hi) )
        plt.xlabel( "parameter 0" )
        plt.ylabel( "parameter 1" )

    return ( ( math.log( numpy.sum( map ) ) + max ), logl )



