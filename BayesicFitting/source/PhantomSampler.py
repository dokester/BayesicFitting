from __future__ import print_function

import numpy as numpy
from astropy import units
import math
from . import Tools
from .Tools import setAttribute as setatt
from .Formatter import formatter as fmt
from .Formatter import fma
from . import Plotter
import sys
import warnings
import matplotlib.pyplot as plt

from .NestedSampler import NestedSampler


from .Explorer import Explorer
from .Model import Model
from .Walker import Walker
from .WalkerList import WalkerList
from .Sample import Sample
from .SampleList import SampleList

from .Problem import Problem
from .ClassicProblem import ClassicProblem
from .ErrorsInXandYProblem import ErrorsInXandYProblem

from .ErrorDistribution import ErrorDistribution
from .ScaledErrorDistribution import ScaledErrorDistribution
from .GaussErrorDistribution import GaussErrorDistribution
from .LaplaceErrorDistribution import LaplaceErrorDistribution
from .PoissonErrorDistribution import PoissonErrorDistribution
from .CauchyErrorDistribution import CauchyErrorDistribution
from .UniformErrorDistribution import UniformErrorDistribution
from .ExponentialErrorDistribution import ExponentialErrorDistribution
#from .BernouilliErrorDistribution import BernouilliErrorDistribution

from .Engine import Engine
from .StartEngine import StartEngine
from .ChordEngine import ChordEngine
from .GibbsEngine import GibbsEngine
from .GalileanEngine import GalileanEngine
from .StepEngine import StepEngine
## for Dynamic Models import the classes
from .BirthEngine import BirthEngine
from .DeathEngine import DeathEngine
## for Modifiable Models:
from .StructureEngine import StructureEngine

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
__version__ = "2.6.2"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Perpetual Beta"

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
#  *    2017 - 2020 Do Kester

class PhantomSampler( NestedSampler ):
    """
    PhantomSampler is a version of NestedSampler that removes step walkers from
    the list. It uses a selection of the intermediate (phantom) positions which
    are created inside the engines as valid walker points.
    These phantoms are added to the walkerlist, until it fills the
    ensemble to its initial value.

    Each iteration a percentage of the walkers is used to update the evidence
    and are subsequently transferred to the list of posterior samples.

    In principle it speeds up the calculations by a factor step, of course it
    pays in exploratory power and precision.


    Attributes
    ----------
    step : int (< 10)
        percentage of the walkers to replace

    Attributes from NestedSampler
    -----------------------------
    xdata, model, ydata, weights, problem, distribution, ensemble, discard, rng, seed,
    rate, maxsize, minimumIterations, end, verbose, walkers, samples, engines,
    initialEngine

    Author       Do Kester.

    """
    ENSEMBLE = 100

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, xdata=None, model=None, ydata=None, weights=None,
                problem=None, distribution=None, limits=None, keep=None, ensemble=100,
                seed=80409, rate=1.0, engines=None, maxsize=None,
                threads=False, verbose=1, step=4 ) :
        """
        Create a new class, providing inputs and model.

        Either (model,xdata,ydata) needs to be provided or a completely filled
        problem.

        Parameters
        ----------
        step : int
            percentage of walkers to use

        Parameters from NestedSampler
        -----------------------------
        xdata : array_like
            array of independent input values
        model : Model
            the model function to be fitted
            the model needs priors for the parameters and (maybe) limits
        ydata : array_like
            array of dependent (to be fitted) data
        weights : array_like (None)
            weights pertaining to ydata
        problem : None or string or Problem
            Defines the kind of problem to be solved.

            None        same as "classic"
            "classic" 	ClassicProblem
            "errors"	ErrorsInXandYProblem
            "multiple"	MultipleOutputProblem

            Problem     Externally defined Problem. When Problem has been provided,
                        xdata, model, weights and ydata are not used.
        keep : None or dict of {int:float}
            None of the model parameters are kept fixed.
            Dictionary of indices (int) to be kept at a fixed value (float).
            Hyperparameters follow model parameters.
            The values will override those at initialization.
            They are used in this instantiation, unless overwritten at the call to sample()
        distribution : None or String or ErrorDistribution
            Defines the ErrorDistribution to be used
            When the hyperpar(s) are not to be kept fixed, they need `Prior` and maybe limits.

            None            same as "gauss"
            "gauss"         GaussErrorDistribution with (fixed) scale equal to 1.0
            "laplace"       LaplaceErrorDistribution with 1 hyperpar scale
            "poisson"       PoissonErrorDistribution no hyperpar
            "cauchy"        CauchyErrorDstribution with 1 hyperpar scale
            "uniform"       UniformErrorDistribution with 1 hyperpar scale
            "exponential"   ExponentialErrorDistribution with 2 hyperpar (scale, power)
            "bernouilli"    BernouilliErrorDistribution no hyperpar (NOTYET)

            ErrorDistribution Externally defined ErrorDistribution
        limits : None or [low,high] or [[low],[high]]
            None    no limits implying fixed hyperparameters of the distribution
            low     low limit on hyperpars
            high    high limit on hyperpars
            When limits are set the hyperpars are not fixed.
        ensemble : int
            number of walkers
        seed : int
            seed of random number generator
        rate : float
            speed of exploration
        engines : None or (list of) string or (list of) Engine
            to randomly move the walkers around, within the likelihood bound.

            None        use a Problem defined selection of engines
            "galilean"  GalileanEngine	move forward and mirror on edges
            "chord"     ChordEngine   	select random point on random line
            "gibbs" 	GibbsEngine 	move one parameter at a time
            "step"  	StepEngine    	move all parameters in arbitrary direction

            For Dynamic models only:
            "birth" 	BirthEngine     increase the parameter list of a walker by one
            "death" 	DeathEngine     decrease the parameter list of a walker by one

            For Modifiable models only:
            "struct"    StructureEngine change the (internal) structure.

            Engine      an externally defined (list of) Engine
        maxsize : None or int
            maximum size of the resulting sample list (None : no limit)
        threads : bool (False)
            Use Threads to distribute the diffusion of discarded samples over the available cores.
        verbose : int (1)
            0   silent
            1   basic information
            2   more about every 100th iteration
            3   more about every iteration
            >4  for debugging

        """
        if step <= 10 :
            self.step = step
        else :
            raise ValueError( "Please keep step <= 10" )

        self.initEnsemble = ensemble
        self.usePhantoms = True
#        self.walkers = []

        super().__init__( xdata=xdata, model=model, ydata=ydata, weights=weights,
                problem=problem, distribution=distribution, limits=limits, keep=keep,
                ensemble=None, seed=seed, rate=rate, engines=engines, maxsize=maxsize,
                threads=threads, verbose=verbose )


    def __getattr__( self, name ) :
        if name == "worst" :
            return int( ( len( self.walkers ) * self.step ) // 100 )
        else :
            return super().__getattr__( name )

    def initSample( self, ensemble=None, keep=None ) :

        return super().initSample( ensemble=self.initEnsemble, keep=keep )


    def updateWalkers( self, explorer, worst ) :
        """
        Update the walkerlist while appending the new (phantom) walkers to the list

        Parameters
        ----------
        explorer : Explorer
            Explorer object
        worst : int
            number of walkers to update
        """
        self.walkers[:worst] = []

        e0 = self.engines[0]
#        print( "updateW  ", worst, len( self.walkers ), fma( e0.unitRange, linelength=200 ) )

        while len( self.walkers ) <= self.initEnsemble :
            # Explore the copied walker(s)
            wlist = [self.rng.randint( worst, self.ensemble )]
            explorer.explore( wlist, self.lowLhood, self.iteration )
#            if self.iteration >= 1755 :
#                print( "explore   ", wlist, self.ensemble, e0.size, min(e0.unitRange), max( e0.unitRange) )


        while len( self.walkers ) > self.initEnsemble :
            ks = self.initEnsemble - self.step
            k = ks + self.rng.randint( self.ensemble - ks - 1 )
#            print( k, self.ensemble, len( self.walkers ), self.walkers[-1].logL )
            del( self.walkers[k] )


