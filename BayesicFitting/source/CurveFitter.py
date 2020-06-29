import numpy as numpy
from astropy import units
from scipy.optimize import curve_fit
import math
from . import Tools
from .Formatter import formatter as fmt

from .ConvergenceError import ConvergenceError
from .BaseFitter import BaseFitter
from .IterativeFitter import IterativeFitter
from .IterationPlotter import IterationPlotter

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
__version__ = "2.5.3"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Perpetual Beta"

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
#  *    2016 - 2020 Do Kester

class CurveFitter( IterativeFitter ):
    """
    CurveFitter implements scipy.optimize.curve_fit.

    Author:      Do Kester.

    Attributes
    ----------
    method : {'lm', 'trf', 'dogbox'}
        'lm'        LevenbergMarquardt (default for no limits)
        'trf'       Trust Region Reflective (default for limits)
        'dogbox'    for small problems with limits

    Raises
    ------
    ConvergenceError    Something went wrong during the convergence if the fit.

    """
    def __init__( self, xdata, model, method=None, fixedScale=None, map=False, keep=None ):
        """
        Create a new class, providing inputs and model.

        Parameters
        ----------
        xdata : array_like
            array of independent input values
        model : Model
            the model function to be fitted
        method : 'lm' | 'trf' | 'dogbox'
            method to be used
        fixedScale : float
            the fixed noise scale.
        map : bool (False)
            When true, the xdata should be interpreted as a map.
            The fitting is done on the pixel indices of the map,
            using ImageAssistant
        keep : dict of {int:float}
            dictionary of indices (int) to be kept at a fixed value (float)
            The values of keep will be used by the Fitter as long as the Fitter exists.
            See also `fit( ..., keep=dict )`

        """
        super( CurveFitter, self ).__init__( xdata, model, map=map, keep=keep,
                            fixedScale=fixedScale )
        self.method = method

    #  *************************************************************************
    def fit( self, ydata, weights=None, inipar=None, keep=None, limits=None,
            plot=False, **kwargs ):
        """
        Return      parameters for the model fitted to the data array.

        Parameters
        ----------
        ydata : array_like
            the data vector to be fitted
        weights : array_like
            weights pertaining to the data
            The weights are relative weights unless fixedScale is set.
        inipar : array_like
            inital parameters (default from Model)
        keep :  dict of {int:float}
            dictionary of indices (int) to be kept at a fixed value (float)
            The values of keep are only valid for *this* fit
            See also `CurveFitter( ..., keep=dict )`
        limits : None or list of 2 floats or list of 2 array_like
            None :        from Model if Model has limits set else no limits
            [-inf,+inf] : no limits applied
            [lo,hi] :     low and high limits for all values
            [la,ha] :     low array and high array limits for the values
        plot : bool
            Plot the results.
        kwargs : dict
            keywords arguments to be passed to :ref:`curve_fit<scipy.optimize.curve_fit>`

        Raises
        ------
            ValueError when ydata or weights contain a NaN
        """
        fitIndex, ydata, weights = self.fitprolog( ydata, weights=weights, keep=keep )

        abssigma = ( self.fixedScale is not None )
        if weights is None :
            sigma = ( None if not abssigma else
                      numpy.full_like( ydata, 1 / math.sqrt( self.fixedScale ), dtype=float ) )
        else :
            wgts = numpy.where( weights == 0, 1e-20, weights )      # avoid division by 0
            sigma = 1 / numpy.sqrt( wgts )

        # Check for limits
        if limits is not None :
            bounds = limits
        elif self.model.priors :
            bounds = ( self.model.lowLimits, self.model.highLimits )
        else :
            bounds = ( -numpy.inf, numpy.inf )

        # Make requested fitIndex; save original one.
        if keep is not None :
            self.fitIndex = self.keepFixed( keep )

        # Make initial parameters
        p0 = self.model.parameters if inipar is None else inipar
        if fitIndex is not None :
            p0 = p0[fitIndex]

        ydat = ydata
        # Normalize the data when needed.
        if hasattr( self, "normdata" ) :
            ydat = numpy.append( ydata, self.normdata )
            if sigma is None :
                sigma = numpy.ones_like( ydata, dtype=float )
            ms = numpy.min( sigma )
            ## avoid zero weights : make then much smaller than the minimum
            nw = numpy.where( self.normweight == 0, ms / 1e10, self.normweight )
            sigma = numpy.append( sigma, 1.0 / numpy.sqrt( nw ) )

        # Call scipy.curve_fit
        out = curve_fit( self.result, self.xdata, ydat, p0=p0,
            sigma=sigma, absolute_sigma=abssigma, bounds=bounds, jac=self.jacobian,
            method=self.method, **kwargs )

        pars = self.insertParameters( out[0], index=fitIndex )
        pcov = out[1]
        self.model.parameters = pars
        self.covariance = pcov
        self.chiSquared( ydata, weights=weights )

        self.fulloutput = out

        self.fitpostscript( ydata, plot=plot )

        return pars

    def __str__( self ) :
        return "CurveFitter"


# ================================================================================
# The following methods `result` and `jacobian` are passed to scipy's curvefit.
#
# Both have a 'starred' fitpar: (*fitpar) as curvefit expect a tuple of parameters.
# We prefer fitpar to be an array_like thing.
# ================================================================================

    def result( self, xdata, *fitpar ) :
        """
        Result method to make connection to the scipy optimizers

        Parameters
        ----------
        xdata : array_like
            input data
        fitpar : tuple of float
            parameters for the model
        """
        params = Tools.toArray( fitpar, dtype=float, ndim=1 )
        params = self.insertParameters( params )
        res = self.model.result( xdata, params )
        if hasattr( self, "normdfdp" ) :
            extra = numpy.inner( self.normdfdp, params )
            res = numpy.append( res, [extra] )

        return res

    def jacobian( self, xdata, *fitpar ) :
        """
        Method to make connection to the scipy optimizers

        Parameters
        ----------
        xdata : array_like
            input data
        fitpar : (tuple of) float
            parameters for the model
        """
        params = Tools.toArray( fitpar, dtype=float, ndim=1 )
        params = self.insertParameters( params )

        design = self.getDesign( params=params, xdata=xdata, index=self.fitIndex )
        return design

