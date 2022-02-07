import numpy as numpy
import math as math
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from numpy.testing import assert_array_almost_equal as assertAAE
from . import Tools
from .Formatter import formatter as fmt

__author__ = "Do Kester"
__year__ = 2022
__license__ = "GPL3"
__version__ = "3.0.0"
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
#   2017 - 2022 Do Kester

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
            err = fitter.monteCarloError( xx )
            ax0.plot( xx, yy - err, 'g-' )
            ax0.plot( xx, yy + err, 'g-' )
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

    if title is not None :
        plt.title( title )

    if filename is None :
        if show : plt.show()
    else :
        plt.savefig( filename, transparent=transparent )




def plotSampleList( sl, xdata, ydata, errors=None, npt=10000,
        residuals=False, xlabel=None, ylabel=None, title=None, figsize=[7,5], 
        xlim=None, ylim=None, filename=None, transparent=False, show=True ) :
    """
    Plot the posterior as npt points from the SampleList.

    Parameters
    ==========
    sl : SampleList
        the samplelist containing samples from the posterior
    xdata : arraylike
        the xdata values; plotted for comparison
    ydata : arraylike
        the ydata values; plotted for comparison
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
    figsize : list of 2 floats
        size of the figure
    filename  : None or str
        name of png file; otherwise show
    transparent : bool
        make the png file transparent

    """
    if xlabel is None : xlabel = "xdata"
    if ylabel is None : ylabel = "ydata"

    plt.figure( figsize=figsize )
    ax0 = plt

    km = sl.medianIndex
    smp = sl[km]

    if residuals :
        plt.subplots_adjust( hspace=0.001 )
        gs = gridspec.GridSpec( 2, 1, height_ratios=[4,1] )

        ax1 = plt.subplot( gs[1] )
        # plot zero line
        ax1.plot( [min( xdata ),max( xdata )], [0,0], 'k-' )

        res = ydata - sl.average( xdata )
        nd = int( math.log10( len( ydata ) ) )
        mrksz = ( 5 - nd ) if nd < 4 else 1
        ax1.plot( xdata, res, 'k.', markersize=mrksz )
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

    # plot data
    if errors is None :
        ax0.plot( xdata, ydata, 'k.' )
    else :
        ax0.errorbar( xdata, ydata, yerr=errors, fmt='k.' )
    
    # plot average in green
    xs = numpy.linspace( xlo, xhi, 201 )
    yfit = sl.average( xs )
    ax0.plot( xs, yfit, 'g-' )

    plt.ylabel( ylabel )
    if not residuals :
        plt.xlabel( xlabel )

    if ylim is None :
        ylo = min( min( ydata ), min( yfit ) )
        yhi = max( max( ydata ), max( yfit ) )
        ylo -= 0.05 * ( yhi - ylo )
        yhi += 0.05 * ( yhi - ylo )

    if xlim is None :
        xlo -= 0.05 * xrng
        xhi += 0.05 * xrng

    plt.xlim( xlo, xhi )
    plt.ylim( ylo, yhi )

    if title is not None :
        plt.title( title )

    if filename is None :
        if show : plt.show()
    else :
        plt.savefig( filename, transparent=transparent )


