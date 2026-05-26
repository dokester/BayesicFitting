import numpy as numpy
import math as math
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from cycler import cycler
from . import Tools

from .Formatter import formatter as fmt

__author__ = "Do Kester"
__year__ = 2026
__license__ = "GPL3"
__version__ = "3.3.0"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Perpetual Beta"

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
#   2017 - 2026 Do Kester

# Module Plotter
"""
    This module contains several methods to plot the results of some class 

     + a fit by a Fitter.
     + a fit by a Sampler.
     + a fit to a StellarOrbit
     + iteration samples from NestedSampler(s)
     + 3D plot of a stellar orbit
     + Eclipsing stars

    The fits are invoked when Fitter.fit() or Sampler.sample() are called with plot=True.
 
""" 


def plotFit( x, data=None, yfit=None, model=None, fitter=None, show=True,
             residuals=False, xlabel=None, ylabel=None, title=None, figsize=[7,5], 
             xlim=None, ylim=None, filename=None, transparent=False ) :
    """
    Plot the data of a fit.

    Parameters
    ----------
    x : array_like
        xdata of the problem
    data : array_like
        ydata of the problem
    yfit : array_like
        fit of the data to the model
    model : Model
        the model the data are fitted to at x
    fitter : BaseFitter
        the fitter being used
        If set it displays a confidence region for the fit
    show : bool
        display the plot
    residuals : bool
        plot the residuals in a separate panel
    xlabel : None or str
        use as xlabel
    ylabel : None or str
        use as ylabel
    title  : None or str
        use as title
    xlim : None or list of 2 floats
        limits on x-axis
    ylim : None or list of 2 floats
        limits on y-axis
    figsize : list of 2 floats
        size of the figure
    filename  : None or str
        name of png file; otherwise show
    transparent : bool
        make the png file transparent
    """

    if xlabel is None : xlabel = "xdata"
    if ylabel is None : ylabel = "ydata"

    plt.figure( "Fitter Results", figsize=figsize )

    minx = numpy.min( x )
    maxx = numpy.max( x )
    ax0 = plt

    if yfit is None and model is not None :
        yfit = model( x )

    if residuals :
        plt.subplots_adjust( hspace=0.001 )
        gs = gridspec.GridSpec( 2, 1, height_ratios=[4, 1])

        ax1 = plt.subplot( gs[1] )
        res = data - yfit
        nd = int( math.log10( len( data ) ) )
        mrksz = ( 5 - nd ) if nd < 4 else 1
        ax1.plot( x, res, 'k.', markersize=mrksz )
        ax1.margins( 0.05, 0.05 )
        xt = plt.ylim()
        xtk = Tools.nicenumber( ( xt[1] - xt[0] ) / 4 )

        plt.yticks( [-xtk, 0.0, xtk] )
        plt.ylabel( "residual" )
        plt.xlabel( xlabel )

        ax0 = plt.subplot( gs[0] )
        xticklabels = ax0.get_xticklabels()
        plt.setp( xticklabels, visible=False )

    if data is not None :
        nd = int( math.log10( len( data ) ) )
        mrksz = ( 5 - nd ) if nd < 4 else 1
        ax0.plot( x, data, 'k.', markersize=mrksz )

    if model is not None :
        xx = numpy.linspace( minx, maxx, 10 * len( x ) )
        yy = model( xx )
        if fitter is not None :
            err = fitter.monteCarloError( xx, scale=2.0 )
            ax0.fill_between( xx, yy - err, yy + err, color='#BFFFBF' )
            err = fitter.monteCarloError( xx )
            ax0.fill_between( xx, yy - err, yy + err, color='#08FF08' )
            # ax0.plot( xx, yy - err, 'g-' )
            # ax0.plot( xx, yy + err, 'g-' )
        ax0.plot( xx, yy, 'r-' )
    elif yfit is not None :
        ax0.plot( x, yfit, 'r-' )

    ax0.margins( 0.05, 0.05 )
    plt.ylabel( ylabel )
    if not residuals :
        plt.xlabel( xlabel )

    if xlim is not None :
        plt.xlim( xlim[0], xlim[1] )
    if ylim is not None :
        plt.ylim( ylim[0], ylim[1] )

    if title is None and fitter is not None :
        title = fitter.__str__()

    if title is not None :
        plt.title( title )

    if filename is None :
        if show : 
            plt.show()
    else :
        plt.savefig( filename, transparent=transparent )


def plotSampleList( sl, xdata, ydata, problem=None, errors=None, npt=10000,
        residuals=False, xlabel=None, ylabel=None, title=None, period=None, figsize=[7,5], 
        xlim=None, ylim=None, filename=None, transparent=False, show=True ) :
    """
    Plot the posterior as npt points from the SampleList.

    Parameters
    ----------
    sl : SampleList
        the samplelist containing samples from the posterior
    xdata : arraylike
        the xdata values; plotted for comparison
    ydata : arraylike
        the ydata values; plotted for comparison
    problem : Problem
        the problem at hand
    errors : None of arraylike
        (No) errors on the ydata are displayed
    npt : int
        number of points from the sample (10000)
    residuals : bool
        plot the residuals in a lower panel (False)
    xlabel : None or str
        use as xlabel
    ylabel : None or str
        use as ylabel
    title  : None or str
        use as title
    xlim : None or list of 2 floats
        limits on x-axis
    ylim : None or list of 2 floats
        limits on y-axis
    period : float or int
        fold over period
        if int the period is taken from sl.parameters[period]
    figsize : list of 2 floats
        size of the figure
    filename  : None or str
        name of png file; otherwise show
    transparent : bool
        make the png file transparent
    show : bool
        show the plot (or not, for testing)

    """
    if xlabel is None : xlabel = "xdata"
    if ylabel is None : ylabel = "ydata"

    mycc = cycler( color=['k','b','y','c','m'] ) 

    if period is not None :
        if isinstance( period, int ) :
            period = sl.parameters[period]
        xdata = xdata.copy() % period

    if residuals :
        fig = plt.figure( figsize=figsize )

        plt.subplots_adjust( hspace=0.001 )
        gs = gridspec.GridSpec( 2, 1, height_ratios=[4,1] )

        ax1 = plt.subplot( gs[1] )

        # set the color cycler
        ax1.set_prop_cycle( mycc )
        # plot zero line
        ax1.plot( [min( xdata ),max( xdata )], [0,0], 'k-' )

        # get residuals
        if problem is None :
            res = ydata - sl.average( xdata )
        else :
            res = problem.cyclicCorrection( ydata - sl.average( xdata ) )
        
        nd = int( math.log10( len( ydata ) ) )
        mrksz = ( 5 - nd ) if nd < 4 else 1
        ax1.plot( xdata, res, '.', markersize=mrksz )
        ax1.margins( 0.05, 0.05 )
        yt = plt.ylim()
        ymx = max( abs( yt[0] ), abs( yt[1] ) )
        ytk = Tools.nicenumber( 0.7 * ymx )

#        print( "Plotter  ", fmt( yt ), fmt( ymx ), fmt( ytk ) )
 
        plt.yticks( [-ytk, 0.0, ytk] )
        plt.ylim( -ymx, ymx )
        plt.ylabel( "residuals" )
        plt.xlabel( xlabel )

        ax0 = plt.subplot( gs[0] )
        xticklabels = ax0.get_xticklabels()
        plt.setp( xticklabels, visible=False )
    else :
        fig, ax0 = plt.subplots( 1, 1, figsize=figsize )

    if xlim is None : 
        xlo = numpy.min( xdata )
        xhi = numpy.max( xdata )
    else :
        xlo, xhi = tuple( xlim )
    xrng = xhi - xlo

    # plot npt samples from posterior
    ntot = 0
    swgt = 0.0

    for s in sl :
        swgt += s.weight * npt
        ns = int( swgt )
        if ns == 0 : continue
    
        #print( s.weight, swgt, ns )
        xs = numpy.random.rand( ns ) * xrng + xlo

        ax0.plot( xs, s.model.result( xs, s.parameters ), 'r.', markersize=2 )
        swgt -= ns
        ntot += ns

    # set color cycle for ax0
    ax0.set_prop_cycle( mycc )

    # plot data
    if errors is None :
        ax0.plot( xdata, ydata, '.' )
    else :
        ax0.errorbar( xdata, ydata, yerr=errors, fmt='.' )
    
    # plot average in green
    xs = numpy.linspace( xlo, xhi, 201 )
    yfit = sl.average( xs )
    ax0.plot( xs, yfit, 'g-' )

    plt.ylabel( ylabel )
    if not residuals :
        plt.xlabel( xlabel )

    if ylim is None :
        ylo = min( numpy.amin( ydata ), numpy.amin( yfit ) )
        yhi = max( numpy.amax( ydata ), numpy.amax( yfit ) )
        ylo -= 0.05 * ( yhi - ylo )
        yhi += 0.05 * ( yhi - ylo )
    else :
        ylo = ylim[0]
        yhi = ylim[1]

    if xlim is None :
        xlo -= 0.05 * xrng
        xhi += 0.05 * xrng
    else : 
        xlo = xlim[0]
        xhi = xlim[1]

    plt.xlim( xlo, xhi )
    plt.ylim( ylo, yhi )

    if title is not None :
        plt.title( title )

    if filename is None :
        if show : 
            plt.show()
    else :
        plt.savefig( filename, transparent=transparent )


def plotWalker( walker, iter, show=False ):
    """
    Plot the results for a walker in an iteration plot.

    Parameters
    ----------
    walker : Walker
        the walker to plot
    iter : int
        iteration number
    show : bool
        show the plot (or not, for testing)
    """
    xdata = walker.problem.xdata
    ydata = walker.problem.ydata
    param = walker.allpars
    model = walker.problem.model
    plotIter( xdata, ydata, model, param, iter, show=show )


def plotIter( xdata, ydata, model, param, iter, show=False ):
    """
    Plot the data and the fit-results in an iteration plot.

    Parameters
    ----------
    xdata : array
        x data points
    ydata : array
        y data points
    model : Model
        the model
    param : array
        the parameters
    iter : int
        iteration number
    show : bool
        show the plot (or not, for testing)
    """
    plt.figure( 'iterplot' )

    if hasattr( plotIter, "line" ) :
        ax = plt.gca()
        if show :
            plt.pause( 0.02 )       ## updates and displays the plot before pause
        ax.remove( )
        plotIter.text.set_text( "Iteration %d" % iter )
    else :
        plotIter.ymin = numpy.min( ydata )
        plotIter.ymax = numpy.max( ydata )
        xmin = numpy.min( xdata )
        xmax = numpy.max( xdata )
        np = len( xdata ) * 10
        plotIter.xx = numpy.linspace( xmin, xmax, np )
        
    mock = model.result( plotIter.xx, param )
    plt.plot( xdata, ydata, 'k.' )
    plotIter.text = plt.title( "Iteration %d" % iter )
    plotIter.line, = plt.plot( plotIter.xx, mock, 'r-' )
    dmin = min( plotIter.ymin, numpy.min( mock ) )
    dmax = max( plotIter.ymax, numpy.max( mock ) )
    dd = 0.05 * ( dmax - dmin )
    plt.ylim( dmin - dd, dmax + dd )


def plotOrbit( som, par, npoint=361, xdata=None, ydata=None, show=True, 
            plot=None, color='k', ls='-', northEast=True ) :
    """
    Plot the orbit of a StellarOrbitModel in N points, a forward 
    pointing arrow at T = 0, the line to the periastron and 
    an extended line of nodes. 

    if ydata is present, plot the datapoints. If also xdata is present, 
    plot the connecting lines too.

    Parameters
    ----------
    som : StellarOrbitModel with spherical=False
        the orbit to plot
    par :  array
        parameter of the model
    npoint : int
        number of points in the orbit
    xdata : array 
        array of times at which the data are measured
    ydata : 2d array 
        array of [x,y] pairs representing the data
    show : bool
        show the plot (or not, for testing)
    plot : None or pyplot
        None    make a self standing plot and show it
        pyplot  operate within thid plot; do not show
    color, ls : color and linestyle
        for the plot
    northEast : bool
        plot North-East pointers 

    """
#    show = plot is None
    if plot is None :
        plt.figure( "Orbit", figsize=[10,10] )
        plot = plt

    ## make som return rectangular coordinates
    if som.spherical :
        som = som.copy( spherical=False )

    # plot the orbit
    tt = numpy.linspace( 0, par[2], npoint )
    xy = som.result( tt, par )

    x = xy[:,0]
    y = xy[:,1]
    plot.plot( x, y, color=color, ls='-' )

    # arrow at T = 0 in the forward direction.
    xarrow, yarrow = Tools.arrow( x, y, scale=3 )
    plot.fill( xarrow, yarrow, color=color )

    # plot a star at the center
    plot.plot( 0, 0, marker='*', ls=' ', color=color, markersize=10 )

    # plot line to periastron
    yperi = som.result( [par[3] * par[2] / ( 2 * math.pi )], par )
    xpr = yperi[0,0]
    ypr = yperi[0,1]
    plot.plot( [0.0,xpr], [0.0,ypr], color=color, ls=ls )

    # plot line of nodes
    ndx, ndy = lineOfNodes( x, y, par[5], scale=1.4 )
    plot.plot( ndx, ndy, color=color, ls=ls )

    if northEast :
        # plot North-East pointers
        lf, rg, dn, up = plot.axis( "equal" )
        #lf, rg = plot.xlim()
        #dn, up = plot.ylim()

        xr = max( rg - lf, up - dn )
    
        xlf = rg - 0.1 * xr
        ydn = dn + 0.1 * xr

        xar, yar = Tools.arrow( [xlf,xlf + 0.05 * xr], [ydn,ydn], scale=0.1 )
        plot.plot( xar, yar, 'k-' )

        xar, yar = Tools.arrow( [xlf,xlf], [ydn,ydn - 0.05 * xr], scale=0.1 )
        plot.plot( xar, yar, 'k-' )

        plot.text( xlf + 0.06 * xr, ydn, "E" )
        plot.text( xlf, ydn - 0.07 * xr, "N" )

    # plot the data 
    if ydata is not None :
        plot.plot( ydata[:,0], ydata[:,1], 'k.' )

        # plot connecting lines
        if xdata is not None : 
            tt = som.result( xdata, par )
            for k in range( len( xdata ) ) :
                plot.plot( [tt[k,0], ydata[k,0]], [tt[k,1], ydata[k,1]], 
                           'k-', linewidth=0.1 )

    if show :
        plot.axis( "equal" )
        plot.show()

    return

def lineOfNodes( x, y, n2n, scale=1.0, indices=False ) :
    """
    Calculate the line of nodes

    Parameters
    ----------
    x : array
        x-values along the orbit
    y : array
        y-values along the orbit
    n2n : float
        angle from North to Line-of-nodes
    scale : float (1.0)
        extension beyond the orbit
    indices : bool
        return indices in (x,y)

    Returns
    -------
    ( ndx, ndy ) : tuple to 2 lists 
        tuple of x-values and y-values of the nodes
 
    """
    xas, yas = Tools.toRect( ( 1.0, n2n ) )

    xoy = numpy.atan2( y, x )
    xay = math.atan2( yas, xas )
    n1 = numpy.argmin( numpy.abs( xoy - xay ) )
    s1 = math.sqrt( x[n1] ** 2 + y[n1] ** 2 ) * scale

    xay = math.atan2( -yas, -xas )
    n2 = numpy.argmin( numpy.abs( xoy - xay ) )
    s2 = math.sqrt( x[n2] ** 2 + y[n2] ** 2 ) * scale
    ndx = numpy.array( [-xas*s2,xas*s1] )
    ndy = numpy.array( [-yas*s2,yas*s1] )

    if n2 < n1 :
        n1, n2 = n2, n1

    return ( ndx, ndy, n1, n2 ) if indices else ( ndx, ndy )


def plotOrbit3D( som, par, npoint=361, xdata=None, ydata=None, show=True,
            plot=None, color='k', ls='-', northEast=True ) :
    """
    Three dimensional plot of the orbit of a StellarOrbitModel in N points, a forward 
    pointing arrow at T = 0, the line to the periastron and 
    an extended line of nodes. 

    if ydata is present, plot the datapoints. If also xdata is present, 
    plot the connecting lines too.

    Parameters
    ----------
    som : StellarOrbitModel with spherical=False
        the orbit to plot
    par :  array
        parameter of the model
    npoint : int
        number of points in the orbit
    xdata : array 
        array of times at which the data are measured
    ydata : 2d array 
        array of [x,y] pairs representing the data
    show : bool
        show the plot (or not, for testing)
    plot : None or pyplot
        None    make a self standing plot and show it
        pyplot  operate within this plot; do not show
                needs to have  .add_subplot( projection='3d' )
    color, ls : color and linestyle
        for the plot
    northEast : bool
        plot North-East pointers 

    """
#    show = plot is None
    if plot is None :
        ax = plt.figure( "Orbit", figsize=[7,7] ).add_subplot( projection='3d' )
    else :
        ax = plot

    ## make som return rectangular coordinates
    if som.spherical :
        som = som.copy( spherical=False )

    # plot the orbit. A line when z > 0; dotted when below
    tt = numpy.linspace( 0, par[2], npoint )
    x,y,z = som.getOrbit( tt, par, d3=True )

    ndx, ndy, n1, n2 = lineOfNodes( x, y, par[5], scale=1.4, indices=True )
    la = ['-',':']
    k = 0 if z[(n1+n2)//2] >= 0 else 1
    ax.plot( x[n1:n2], y[n1:n2], z[n1:n2], color=color, ls=la[k] )
    k = 1 if k == 0 else 0
    ax.plot( x[:n1], y[:n1], z[:n1], color=color, ls=la[k] )
    ax.plot( x[n2:], y[n2:], z[n2:], color=color, ls=la[k] )
    
    # arrow at T = 0 in the forward direction.
    sc = 3 * npoint / 361
    xarrow, yarrow, zarrow = Tools.arrow( x, y, z, scale=sc )
    ax.plot( xarrow, yarrow, zarrow, color='r' )

    # plot a star at the center
    ax.plot( 0, 0, 0, marker='*', ls=' ', color=color, markersize=10 )

    # plot line to periastron
    tpr = numpy.array( [par[3] * par[2] / ( 2 * math.pi )] )
    xpr, ypr, zpr = som.getOrbit( tpr, par, d3=True )
    ax.plot( [0.0,xpr[0]], [0.0,ypr[0]], [0.0,zpr[0]], color=color, ls='-' )

    # plot line of nodes
    ax.plot( ndx, ndy, [0.0,0.0], color=color, ls='-' )

    # plot North-East pointers
    lf, rg, fr, bk, dn, up = ax.axis( "equal" )
    if northEast :
        xr = max( rg - lf, bk - fr )
    
        xlf = rg - 0.1 * xr
        ydn = bk + 0.1 * xr
        zlo = dn 

        xar, yar = Tools.arrow( [xlf,xlf + 0.05 * xr], [ydn,ydn], scale=0.2 )
        ax.plot( xar, yar, zlo, 'k-' )

        xar, yar = Tools.arrow( [xlf,xlf], [ydn,ydn - 0.05 * xr], scale=0.2 )
        ax.plot( xar, yar, zlo, 'k-' )

        ax.text( xlf + 0.06 * xr, ydn, zlo, "E" )
        ax.text( xlf - 0.02 * xr, ydn - 0.07 * xr, zlo, "N" )

    # plot the data 
    zlo = 0.0
    if ydata is not None :
        zd = numpy.zeros_like( ydata[:,0] ) + zlo
        ax.plot( ydata[:,0], ydata[:,1], zd, 'k.' )
        ax.plot( x, y, zlo, color=color, ls='-' )

        # plot connecting lines
        if xdata is not None : 
            tt = som.result( xdata, par )
            for k in range( len( xdata ) ) :
                ax.plot( [tt[k,0], ydata[k,0]], [tt[k,1], ydata[k,1]], [zlo,zlo], 
                           'k-', linewidth=0.1 )

    if show :
#        ax.axis( "equal" )
        plt.show()

    return


def plotEclipsingStar( esm, pars, xdata=None, ydata=None, toMags=False, starpos=None, 
                       figsize=[9,6], grid=None, show=True, filename=None ):
    """
    plot of eclipsing stars seen from above. The orientation is irrelevant.

    Parameters
    ----------
    esm : EclipsingStarModel
        containing the stars
    pars : array
        for esm
    xdata : None or array
        of (measured) data points.
    ydata : None or array
        of (measured) data points.
    toMags : bool or float
        true    produce plot in magnitudes (ydata is in mags)
        float   true and use number to scale the fluxes
    starpos : (small) array
        times of star positions to display
    figsize : list of 2 floats
        size of the plot
    grid : GridSpec
        GridSpec where to plot the orbit in
    show : bool
        to show the plot (or not)
    filename : str
        write to filename
    """ 
    ## indices are not at fixed locations for variants of ESM
    per = esm.getParameterValue( pars, "period" )

#    if show is None :
#        show = grid is None

    if grid is None :
        fig = plt.figure( figsize=figsize )
        grid = fig.add_gridspec( 1, 1 )[0,0]

    ax = grid.subgridspec( 1, 1).subplots( )

    ## make 2 insets to display the eclipsing stars
    sperc = "35%"
    axin1 = inset_axes( ax, width=sperc, height=sperc, loc="lower left",
            borderpad=1 )
    axin2 = inset_axes( ax, width=sperc, height=sperc, loc="lower right",
            borderpad=1 )

    t = numpy.linspace( 0, per, 361 )
    r = esm.result( t, pars )

    if toMags :
        fm = float( toMags )
        r = -2.512 * numpy.log10( r * fm )

    ## plot data and result in main frame
    if xdata is not None and ydata is not None :
        xd = xdata % per
        ax.plot( xd, ydata, 'k.' )
        ax.plot( t, r, 'r-' )
    else :
        ax.plot( t, r, 'k-' )

    if toMags :
        ax.yaxis.set_inverted( True )
        ylabel = "Magnitude"
    else :
        ylabel = "Flux"
    ax.set_xlabel( "Days" )
    ax.set_ylabel( ylabel )

    if starpos is None :
        NP = 6
        starpos = numpy.linspace( 0, ( 1 - 1/NP) * per, NP ) + 0.5 / NP

    ## plot example points in main frame
    xl,xh = ax.get_xlim()
    xa = 0.05 * ( xh - xl ) 
    yl,yh = ax.get_ylim()
    ya = 0.05 * ( yh - yl ) 
    yh += 1.5 * ya
    xar, yar = Tools.arrow( [0.0,0.0], [0.0,-1.0], scale=0.2 )
    for k,ts in enumerate( starpos ) :
        ax.plot( xar*xa+ts, yar*ya+yh-ya, 'r-' )
        ax.text( ts+0.1*xa, yh-1.5*ya, "%s"%k, ha="left" )

    axin2 = plotEsmSideView( esm, pars, times=t, starpos=starpos, axin=axin2 )

    axin1 = plotEsmEclipseView( esm, pars, times=t, starpos=starpos, axin=axin1 )

    yl,yh = ax.get_ylim()
    yl -= 0.4 * ( yh - yl )

    ax.set_ylim( yl, yh )

    yl,yh = axin2.get_ylim()
    axin1.set_ylim( yl, yh )

    if filename is not None:
        plt.savefig( filename )

    if show :
        plt.show()
    else : 
        return ax

def plotEsmSideView( esm, pars, times=None, starpos=None, axin=None, figsize=[9,6],
                     show=False ) :
    """
    Plot an EclipsingStarModel in sideways view.

    Parameters
    ----------
    esm : EclipsingStarModel
        containing the stars
    pars : array
        for esm
    times : None or array
        to plot
    starpos : (small) array
        times of star positions to display
    axin : Axes (None)
        to plot in
    figsize : list of 2 floats ([9,6])
        size of the plot
    show : bool (False)
        to show the plot
    """ 
    pi = math.pi
    
    per = esm.getParameterValue( pars, "period" )
    r1  = esm.getParameterValue( pars, "radius_1" )
    r2  = esm.getParameterValue( pars, "radius_2" )
    L1  = esm.getParameterValue( pars, "lumen_1" )
    L2  = esm.getParameterValue( pars, "lumen_2" )
    try :
        L3 = esm.getParameterValue( pars, "spot" )
    except Exception :
        L3 = 0.0

    if axin is None :
        fig, axin = plt.subplots( 1, 1, figsize=figsize )

    if times is None :
        t = numpy.linspace( 0, per, 361 )
    else :
        t = times

    fp = esm.fixpar( pars )
    x, y, z = esm.storbit.getOrbit( t, fp, d3=True )

    miny, maxy, rany, midy = Tools.minmax( -y, range=True, mid=True )
    minz, maxz, ranz, midz = Tools.minmax(  z, range=True, mid=True )

    ## plot sidewise view in inset 2
    axin.plot( z, -y, 'k-', linewidth=0.8 )
    axin.set_title( "side view" )
    yap = miny * 1.5
    xar,yar = Tools.arrow( [-1,1], [yap,yap], scale=0.05 )
    axin.plot( xar, yar, 'k-' )
    axin.text( midz, yap, "observer", ha="center", va="top" )

    phi = t * 2 * pi / per
    rx, ry = Tools.toRect( 1, phi )

    if starpos is None :
        NP = 6
        starpos = numpy.linspace( 0, ( 1 - 1/NP) * per, NP ) + 0.5 / NP

    x2, y2, z2 = esm.storbit.getOrbit( starpos, fp, d3=True )

    phi = numpy.atan2( -y2, z2 )
    ph = phi * 180 / pi
    rho = numpy.sqrt( x2*x2 + y2*y2 + z2*z2 )

    NP = len( starpos )

    a1, b1, a2, b2 = esm.tidalDistortion( rho, z2, pars )

    cc1, cc2, cc3 = starColors( L1, L2, L3 )

    ## plot main star in inset 2
    axin.fill( rx * r1, ry * r1, c=cc1 )

    ## plot the starpos points of star 2
    rmx = max( 1.8 * r2, 0.1 )
    NP = len( starpos )
    for k in range( NP ) :
        kph = int( ph[k] ) + 180
        lz = z2[k]
        ly =-y2[k]
    
        xx = rx * r2 * b2[k]
        yy = ry * r2 * a2[k]

        rr, pp = Tools.toSpher( xx, yy )
        pp += phi[k] - pi / 2
        xx, yy = Tools.toRect( rr, pp )
        xx = numpy.roll( xx, 90 )
        yy = numpy.roll( yy, 90 )


        axin.fill( xx[:181] + lz, yy[:181] + ly, c=cc3 )
        axin.fill( xx[181:] + lz, yy[181:] + ly, c=cc2 )
        kp = ( kph - 90 ) % 360
        xr = lz + rmx * rx[kp]
        yr = ly + rmx * ry[kp]
        axin.text( xr, yr, "%d"%k, ha="center", va="center" )


    ## clean up insets
    yzr = max( rany, ranz ) / 1.4
    axin.set_ylim( midy - yzr, midy + yzr )
    axin.set_xlim( midz - yzr, midz + yzr )
 
    axin.axis( "equal" )
    axin.set_axis_off()

    if show :
        plt.show()
    else : 
        return axin

def starColors( L1, L2, L3 ) :
    """
    Return colors for star 1, star 2 dark side and star 2 spot.

    Parameters
    ----------
    L1, L2, L3 : floats
        luminosities for star 1, 2 and spot
    """
    h = 0.5
    cbr = (1,h,h)               ## color bright red
    cbb = (h,1,1)               ## color bright blue

    b = h if L3 == 0 else 0.0
    cwb = (b,1,1)               ## color weak blue
    cwr = (1,h,b)               ## color weak red

    if L1 > L2 :
        cc1 = cbb
        cc2 = (1,0,0)
        cc3 = cwr if L3 > 0 else cc2
    else :
        cc1 = cbr
        cc2 = (0,0,1)
        cc3 = cwb if L3 > 0 else cc2

    return cc1, cc2, cc3


def plotEsmEclipseView( esm, pars, times=None, starpos=None, axin=None, figsize=[9,6],
                     show=False ) :
    """
    Plot an EclipsingStarModel in eclipsing view.

    Parameters
    ----------
    esm : EclipsingStarModel
        containing the stars
    pars : array
        for esm
    times : None or array
        to plot
    starpos : (small) array
        times of star positions to display
    axin : Axes (None)
        to plot in
    figsize : list of 2 floats ([9,6])
        size of the plot
    show : bool (False)
        to show the plot
    """ 
    pi = math.pi
    
    per = esm.getParameterValue( pars, "period" )
    r1  = esm.getParameterValue( pars, "radius_1" )
    r2  = esm.getParameterValue( pars, "radius_2" )
    L1  = esm.getParameterValue( pars, "lumen_1" )
    L2  = esm.getParameterValue( pars, "lumen_2" )
    try :
        L3 = esm.getParameterVale( pars, "spot" )
    except Exception :
        L3 = 0.0

    if axin is None :
        fig, axin = plt.subplots( 1, 1, figsize=figsize )

    if times is None :
        t = numpy.linspace( 0, per, 361 )
    else :
        t = times

    fp = esm.fixpar( pars )
    x, y, z = esm.storbit.getOrbit( t, fp, d3=True )

    miny, maxy, rany, midy = Tools.minmax( -y, range=True, mid=True )
    minz, maxz, ranz, midz = Tools.minmax(  z, range=True, mid=True )

    ## plot eclipsing view in inset 1
    q = numpy.where( ( x*x + y*y > r1 * r1 ) | ( z > 0 ) )[0]
    if len( q ) < 361 and q[0] == 0 :
        b = numpy.where( q - numpy.roll( q, 1) > 1 )[0]
        q = numpy.roll( q, -b[0] )

    kmz = numpy.argmin( z )
    xkmz = x[kmz]

    dx = 0.01 * ( x[q] - xkmz )
    lw = 0.5
    dix = -2 * dx
    for k in range( 5 ) :
        axin.plot( x[q]+dix, -y[q], 'k-', linewidth=lw )
        dix += dx

    axin.set_title( "eclipsing" )

    phi = t * 2 * pi / per
    rx, ry = Tools.toRect( 1, phi )

    if starpos is None :
        NP = 6
        starpos = numpy.linspace( 0, ( 1 - 1/NP) * per, NP ) + 0.5 / NP

    x2, y2, z2 = esm.storbit.getOrbit( starpos, fp, d3=True )

    phi = numpy.atan2( -y2, z2 )
    ph = phi * 180 / pi
    rho = numpy.sqrt( x2*x2 + y2*y2 + z2*z2 )
    cth = z2 / rho

    NP = len( starpos )

    a1, b1, a2, b2 = esm.tidalDistortion( rho, z2, pars )

    cc1, cc2, cc3 = starColors( L1, L2, L3 )

    ## to display the stellar phases in inset 1
    ran = numpy.linspace( 0, pi, 181 )
    sran = numpy.sin( ran ) * r2
    cran = numpy.cos( ran ) * r2

    ## plot the starpos points of 2, behind the star 1 in inset 1
    rmx = math.copysign( max( 1.8 * r2, 0.1 ), -xkmz )
    for k in range( NP ) :
        kph = int( ph[k] ) + 180
        lz =  x2[k]
        ly = -y2[k]
        xx = numpy.roll( rx, -kph ) * r2
        yy = numpy.roll( ry, -kph ) * r2


        if z2[k] < 0 :
            ctx = -cth[k] * sran
            cty = -cran
            rot = math.atan2( yy[180], xx[180] )
            rtx, ptx = Tools.toSpher( ctx, cty )
            ctx, cty = Tools.toRect( rtx, ptx + rot + pi/2 )

            xs = lz + numpy.append( xx[:181], ctx ) * b2[k]
            ys = ly + numpy.append( yy[:181], cty ) * a2[k]
            axin.fill( xs, ys, c=cc3 )
            xs = lz + numpy.append( numpy.flip( ctx ), xx[181:] ) * b2[k]
            ys = ly + numpy.append( numpy.flip( cty ), yy[181:] ) * a2[k]
            axin.fill( xs, ys, c=cc2 )

            kp = ( kph - 90 ) % 360
            xr = lz + rmx * rx[kp]
            yr = ly + rmx * ry[kp]
            axin.text( xr, yr, "%d"%k, ha="center", va="center" )

    ## plot star 1 in inset 1
    axin.fill( rx * r1, ry * r1, c=cc1, alpha=1.0 )

    ## plot the starpos points of star 2 in front of star 1
    for k in range( NP ) :
        kph = int( ph[k] ) + 180
        lz =  x2[k]
        ly = -y2[k]
        xx = numpy.roll( rx, -kph ) * r2
        yy = numpy.roll( ry, -kph ) * r2

        if z2[k] >= 0 :
            ctx = -cth[k] * sran
            cty = -cran
            rot = math.atan2( yy[180], xx[180] )
            rtx, ptx = Tools.toSpher( ctx, cty )
            ctx, cty = Tools.toRect( rtx, ptx + rot + pi/2 )

            xs = lz + numpy.append( xx[:181], ctx ) * b2[k]
            ys = ly + numpy.append( yy[:181], cty ) * a2[k]
            axin.fill( xs, ys, c=cc3 )
            xs = lz + numpy.append( numpy.flip( ctx ), xx[181:] ) * b2[k]
            ys = ly + numpy.append( numpy.flip( cty ), yy[181:] ) * a2[k]
            axin.fill( xs, ys, c=cc2 )

            kp = ( kph - 90 ) % 360
            xr = lz + rmx * rx[kp]
            yr = ly + rmx * ry[kp]
            axin.text( xr, yr, "%d"%k, ha="center", va="center" )

    ## clean up insets
    yzr = max( rany, ranz ) / 1.4
    axin.set_ylim( midy - yzr, midy + yzr )
    axin.set_xlim( midz - yzr, midz + yzr )

    axin.axis( "equal" )
    axin.set_axis_off()

    if show :
        plt.show()
    else : 
        return axin

