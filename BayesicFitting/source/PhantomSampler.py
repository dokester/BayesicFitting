from __future__ import print_function

import numpy as numpy
import math

from .NestedSampler import NestedSampler





## for Dynamic Models import the classes
## for Modifiable Models:

__author__ = "Do Kester"
__year__ = 2025
__license__ = "GPL3"
__version__ = "3.2.5"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Alpha"

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
#  *    2017 - 2025 Do Kester

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

    Attributes from NestedSampler
    -----------------------------
    xdata, model, ydata, weights, problem, distribution, ensemble, discard, rng, seed,
    rate, maxsize, minimumIterations, end, verbose, walkers, samples, engines,
    initialEngine

    Author       Do Kester.

    """
    ENSEMBLE = 20

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, xdata=None, model=None, ydata=None, weights=None,
                accuracy=None, problem=None, distribution=None, limits=None,
                keep=None, ensemble=ENSEMBLE, seed=80409, rate=1.0, engines=None,
                maxsize=None, threads=False, verbose=1 ) :
        """
        Create a new class, providing inputs and model.

        Either (model,xdata,ydata) needs to be provided or a completely filled
        problem.

        Parameters
        ----------
        xdata : array_like
            array of independent input values
        model : Model
            the model function to be fitted
            the model needs priors for the parameters and (maybe) limits
        ydata : array_like
            array of dependent (to be fitted) data
        weights : array_like (None)
            weights pertaining to ydata
        accuracy : float or array_like
            accuracy scale for the datapoints
            all the same or one for each data point
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
            "bernoulli"     BernoulliErrorDistribution no hyperpar

            ErrorDistribution Externally defined ErrorDistribution
        limits : None or [low,high] or [[low],[high]]
            None    no limits implying fixed hyperparameters of the distribution
            low     low limit on hyperpars
            high    high limit on hyperpars
            When limits are set the hyperpars are not fixed.
        ensemble : int
            number of walkers (20)
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
        super().__init__( xdata=xdata, model=model, ydata=ydata, weights=weights,
                accuracy=accuracy, problem=problem, distribution=distribution, limits=limits,
                keep=keep, ensemble=ensemble, seed=seed, rate=rate, engines=engines,
                maxsize=maxsize, usePhantoms=True, threads=threads, verbose=verbose )


    def __str__( self ):
        """ Return the name of this sampler.  """
        return str( "PhantomSampler" )

    def sample( self, keep=None, plot=False ) :
        """
        see NestedSampler.sample()
        """
        self.logUnitDom = 0.0       ## unitDomain = 1

        return super().sample( keep=keep, plot=plot )



    def updateEvidence( self, worst ) :
        """
        Updates the evidence (logZ) and the information (H)

        The walkers need to be sorted to logL

        Parameters
        ----------
        worst : int
            Number of walkers used in the update

        """

        kw = 0      ### DONT use enumerate here
        for lowph in self.phancol.nextLowPhantom( self.lowLhood ) :
            lpc = self.livepointcount
            logWidth = self.logUnitDom - math.log( lpc )
            logWeight = logWidth + lowph.logL + lowph.logPrior

            # update evidence, logZ
            logZnew = numpy.logaddexp( self.logZ, logWeight )

            # update Information, H
            self.info = ( math.exp( logWeight - logZnew ) * self.lowLhood +
                    math.exp( self.logZ - logZnew ) * ( self.info + self.logZ ) - logZnew )

            if math.isnan( self.info ) :
                self.info = 0.0
            self.logZ = logZnew

            # store posterior samples
            smpl = lowph.toSample( logWeight )
            self.samples.add( smpl )

            self.sumWidth += math.exp( logWidth )

            self.logUnitDom = logWidth + math.log( lpc - 1 )

            kw += 1

        ## check if there has something been updated
        if kw > 0 :
            self.logdZ = logWeight - self.logZ

        return


    def updateEvidence0( self, worst ) :
        """
        Updates the evidence (logZ) and the information (H)

        The walkers need to be sorted to logL

        Parameters
        ----------
        worst : int
            Number of walkers used in the update

        """
        phansemble = self.livepointcount
        kw = 0      ### DONT use enumerate here
        for lowph in self.phancol.nextLowPhantom( self.lowLhood ) :
            logWeight = self.logWidth + lowph.logL + lowph.logPrior

            # update evidence, logZ
            logZnew = numpy.logaddexp( self.logZ, logWeight )

            # update Information, H
            self.info = ( math.exp( logWeight - logZnew ) * self.lowLhood +
                    math.exp( self.logZ - logZnew ) * ( self.info + self.logZ ) - logZnew )

            if math.isnan( self.info ) :
                self.info = 0.0
            self.logZ = logZnew

            # store posterior samples
            smpl = lowph.toSample( logWeight )
            self.samples.add( smpl )

            self.sumWidth += math.exp( self.logWidth )

#            self.logWidth -= 1.0 / ( phansemble - kw )
            self.logWidth -= 1.0 / phansemble
            kw += 1

        ## check if there has something been updated
        if kw > 0 :
            self.logdZ = logWeight - self.logZ

        return

    def __getattr__( self, name ) :
        if name == "livepointcount" :
            return self.phancol.length()
        else :
            return super().__getattr__( name )

