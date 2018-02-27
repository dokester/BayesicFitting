import numpy as numpy
import math
from . import Tools

from .MaxLikelihoodFitter import MaxLikelihoodFitter
from .AnnealingAmoeba import AnnealingAmoeba

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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2017        Do Kester

class AmoebaFitter( MaxLikelihoodFitter ):
    """
    Fitter using the simulated annealing simplex minimum finding algorithm,
    :ref:`AnnealingAmoeba<bayesfit.AnnealingAmoeba>`.

    Author       Do Kester

    Examples
    --------
    # assume x and y are Double1d data arrays.
    >>> x = numpy.arange( 100, dtype=float ) / 10
    >>> y = 3.5 * SIN( x + 0.4 )                    # make sine
    >>> numpy.random.seed( 12345L )                 # Gaussian random number generator
    >>> y += numpy.random.randn( 100 ) * 0.2        # add noise
    >>> sine = SineModel( )                         # sinusiodal model
    >>> lolim = numpy.asarray( [1,-10,-10], dtype=float )
    >>> hilim = numpy.asarray( [100,10,10], dtype=float )
    >>> sine.setLimits( lolim, hilim )              # set limits on the model parameters
    >>> amfit = AmoebaFitter( x, sine )
    >>> param = amfit.fit( y, temp=10 )
    >>> stdev = amfit.getStandardDeviation( )       # stdevs on the parameters
    >>> chisq = amfit.getChiSquared( )
    >>> scale = amfit.getScale( )                 # noise scale
    >>> yfit  = amfit.getResult( )                # fitted values
    >>> yfit  = sine( x )                         # fitted values ( same as previous )
    >>> yband = amfit.monteCarloError( )               # 1 sigma confidence region
    # for diagnostics ( or just for fun )
    >>> amfit = AmoebaFitter( x, sine )
    >>> amfit.setTemperature( 10 )                # set a temperature to escape local minima
    >>> amfit.setVerbose( 10 )                    # report every 10th iteration
    >>> plotter = IterationPlotter( )             # from herschel.ia.toolbox.fit
    >>> amfit.setPlotter( plotter, 20 )            # make a plot every 20th iteration
    >>> param = amfit.fit( y )


    Notes
    -----
    1. AmoebaFitter is <b>not</b> guaranteed to find the global minimum.
    2. The calculation of the evidence is an Gaussian approximation which is
    only exact for linear models with a fixed scale.

    Category     mathematics/Fitting

    """
    #  *************************************************************************
    def __init__( self, xdata, model, **kwargs ):
        """
        Create a new Amoeba class, providing inputs and model.

        Parameters
        ----------
        xdata : array_like
            independent input values
        model : Model
            the model function to be fitted
        kwargs : dict
            Possibly includes keywords from
                MaxLikelihoodFitter :   errdis, scale, power
                IterativeFitter :       maxIter, tolerance, verbose
                BaseFitter :            map, keep, fixedScale

        """
        if model.npchain <= 1 :
            raise ValueError( "AmoebaFitter cannot make a simplex of one parameter" )

        super( AmoebaFitter, self ).__init__( xdata, model, **kwargs )

    #  *************************************************************************
    def fit( self, data, weights=None, par0=None, keep=None, size=None,
                    seed=4567, temp=0, limits=None, maxiter=1000,
                    tolerance=0.0001, cooling=0.95, steps=10,
                    verbose=0, plot=False, callback=None ):
### TBC parameter defaults


        """
        Return Model fitted to the data array.

        When done, it also calculates the hessian matrix and chisq.

        Parameters
        ----------
        data : array_like
             the data vector to be fitted
        weights : array_like
            weights pertaining to the data
            The weights are relative weights unless `scale` is set.
        par0 : array_like
            initial values of teh parameters of the model
            default: from model
        keep : dict of {int:float}
            dictionary of indices (int) to be kept at a fixed value (float)
            The values of keep are only valid for *this* fit
            See also `AmoebaFitter( ..., keep=dict )`
        size : float or array_like
            step size of the simplex
        seed : int
            for random number generator
        temp : float
            temperature of annealing (0 is no annealing)
        limits : None or list of 2 floats or list of 2 array_like
            None : no limits applied
            [lo,hi] : low and high limits for all values
            [la,ha] : low array and high array limits for the values
        maxiter : int
            max number of iterations
        tolerance : float
            stops when ( |hi-lo| / (|hi|+|lo|) ) < tolerance
        cooling : float
            cooling factor when annealing
        steps : int
            number of cycles in each cooling step.
        verbose : int
            0 : silent
            1 : print results to output
            2 : print some info every 100 iterations
            3 : print some info all iterations
        plot : bool
            plot the results.
        callback : callable
            is called each iteration as
            `val = callback( val )`
            where `val` is the minimizable array

        """
        fitIndex = self.fitprolog( data, weights=weights, keep=keep )

        func = self.makeFuncs( data, weights=weights, index=fitIndex, ret=1 )

        if par0 is None :
            par0 = self.model.parameters
        if fitIndex is not None and len( fitIndex ) < len( par0 ) :
            par0 = par0[fitIndex]

        kwargs = {}
        if size is not None :
            kwargs["size"] = size
        if seed is not None :
            kwargs["seed"] = seed
        if temp is not None :
            kwargs["temp"] = temp
        if limits is not None :
            kwargs["limits"] = limits
        if maxiter is not None :
            kwargs["maxiter"] = maxiter
        if tolerance is not None :
            kwargs["reltol"] = tolerance
            kwargs["abstol"] = tolerance
        if cooling is not None :
            kwargs["cooling"] = cooling
        if steps is not None :
            kwargs["steps"] = steps
        if verbose is not None :
            kwargs["verbose"] = verbose
        if callback is not None :
            kwargs["callback"] = callback

        amoeba = AnnealingAmoeba( func, par0, **kwargs )

        par = amoeba.minimize()
        parameters = self.insertParameters( par, index=fitIndex )
        self.model.parameters = parameters

        if self.isChisq :
            self.chisq = amoeba.fopt
        else :
            self.logLikelihood = -amoeba.fopt
            self.chisq = self.chiSquared( data, weights=weights )

        self.iter = amoeba.iter

        self.ntrans = amoeba.ncalls
        self.simplex = amoeba.simplex
        self.values = amoeba.values

#        plot = plot or ( verbose == 2 )
        self.fitpostscript( data, plot=plot )

        return parameters

    def __str__( self ):
        """ Return name of the fitter.  """
        return "AmoebaFitter"


