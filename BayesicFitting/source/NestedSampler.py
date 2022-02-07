from __future__ import print_function

import numpy as numpy
from astropy import units
import math
from . import Tools
from .Tools import setAttribute as setatt
from .Formatter import formatter as fmt
from . import Plotter
import sys
import warnings
import matplotlib.pyplot as plt

from .Explorer import Explorer
from .Model import Model
from .Walker import Walker
from .WalkerList import WalkerList
from .Sample import Sample
from .SampleList import SampleList

from .Problem import Problem
from .ClassicProblem import ClassicProblem
from .ErrorsInXandYProblem import ErrorsInXandYProblem
from .MultipleOutputProblem import MultipleOutputProblem
from .EvidenceProblem import EvidenceProblem

from .ErrorDistribution import ErrorDistribution
from .ScaledErrorDistribution import ScaledErrorDistribution
from .GaussErrorDistribution import GaussErrorDistribution
from .LaplaceErrorDistribution import LaplaceErrorDistribution
from .PoissonErrorDistribution import PoissonErrorDistribution
from .CauchyErrorDistribution import CauchyErrorDistribution
from .UniformErrorDistribution import UniformErrorDistribution
from .ExponentialErrorDistribution import ExponentialErrorDistribution
from .ModelDistribution import ModelDistribution
from .BernoulliErrorDistribution import BernoulliErrorDistribution

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
__year__ = 2022
__license__ = "GPL3"
__version__ = "3.0.0"
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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2017 - 2022 Do Kester

class NestedSampler( object ):
    """
    Nested Sampling is a novel technique to do Bayesian calculations.

    Nested Sampling calculates the value of the evidence while it
    simultaneously produces samples from the posterior probability
    distribution of the parameters, given a Model and a
    dataset ( x-values, y-values and optionally weights ).
    The samples are collected in a SampleList.

    NestedSampler is constructed according to the ideas of John Skilling
    and David MacKay ( ref TBD ).

    Internally it contains an ensemble ( by default: 100 ) of trial samples,
    called walkers. Initially they are randomly distributed over the space
    available to the parameters. This randomness is distributed according
    to the prior distribution of the parameters. In most simple cases it
    will be uniform.

    In an iterative process, the sample with the lowest likelihood is
    selected and replaced by a copy of one of the others.
    The parameters of the copy are randomly walked around under the
    condition that its likelihood stays larger than the selected lowest likelihood.
    A new independent trial sample is constructed.
    The original lowest sample is placed, appropriately weighted, into the
    SampleList for output.

    This way the likelihood is climbed until the maximum is found.
    Along the way the integral of the likelihood function is
    calculated, which is equal to the evidence for the model,
    given the dataset.

    There are different likelihood functions available: Gaussian (Normal),
    Laplace (Norm-1), Uniform (Norm-Inf), Poisson (for counting processes),
    Bernoulli (for categories), Cauchy (aka Lorentz) and
    Exponential (generalized Gaussian).
    A mixture of ErrorDistributions can also be defined.
    By default the Gaussian distribution is used.

    Except for Poisson and Bernoulli , all others are ScaledErrorDistributions.
    The scale is a HyperParameter which can either be fixed, by setting the
    attribute errdis.scale or optimized, given the model parameters and the data.
    By default it is optimized for Gaussian and Laplace distributions.
    The prior for the noise scale is a JeffreysPrior.

    The Exponential also has a power as HyperParameter which can be fixed
    or optimized. Its default is 2 (==Gaussian).

    For the randomization of the parameters within the likelihood constraint
    so-called engines are written.
    By default only engines 1 and 2 is switched on.

    1. GalileanEngine.
        It walks all (super)parameters in a fixed direction for about 5 steps.
        When a step ends outside the high likelihood region the direction is
        mirrored on the lowLikelihood edge and continued.

    2. ChordEngine.
        It draws a randomly oriented line through a point inside the region,
        until it reaches outside the restricted likelihood region on both sides.
        A random point is selected on the line until it is inside the likelihood region.
        This process runs several times

    3. GibbsEngine.
        It moves each of the parameters by a random step, one at a time.
        It is a randomwalk.

    4. StepEngine.
        It moves all parameters in a random direction. It is a randomwalk.

    5. CrossEngine.
        The parameters of 2 walkers are mixed in a random way.

    For dynamic models 2 extra engines are defined:

    6. BirthEngine.
        It tries to increase the number of parameters.
        It can only be switched on for Dynamic Models.

    7. DeathEngine.
        It tries to decrease the number of parameters.
        It can only be switched on for Dynamic Models.

    For modifiable models 1 engine is defined.

    8. StructureEngine.
        It alters the internal structure of the model.
        It can only be switched on for Modifiable Models.

    Attributes
    ----------
    xdata : array_like
        array of independent input values
    model : Model
        the model function to be fitted
    ydata : array_like
        array of dependent (to be fitted) data
    weights : array_like (None)
        weights pertaining to ydata
    problem : Problem (ClassicProblem)
        to be solved (container of model, xdata, ydata and weights)
    distribution : ErrorDistribution
        to calculate the loglikelihood
    ensemble : int (100)
        number of walkers
    discard : int (1)
        number of walkers to be replaced each generation
    rng : RandomState
        random number generator
    seed : int (80409)
        seed of rng
    rate : float (1.0)
        speed of exploration
    maxsize : None or int
        maximum size of the resulting sample list (None : no limit)
    minimumIterations : int (100)
        minimum number of iterations (adapt when starting problems occur)
    end : float (2.0)
        stopping criterion
    verbose : int
        level of blabbering
    walkers : WalkerList
        ensemble of walkers that explore the likelihood space
    samples : SampleList
        Samples resulting from the exploration
    engines : list of Engine
        Engine that move the walkers around within the given constraint: logL > lowLogL
    initialEngine : Engine
        Engine that distributes the walkers over the available space
    restart : StopStart (TBW)
        write intermediate results to (optionally) start from.

    Author       Do Kester.

    """
    TWOP31 = 2 ** 31        ## 2 ** 32 raises an error on Windows systems.
    ENSEMBLE = 100

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, xdata=None, model=None, ydata=None, weights=None,
                problem=None, distribution=None, limits=None, keep=None, ensemble=100,
                discard=1, seed=80409, rate=1.0, engines=None, maxsize=None,
                threads=False, verbose=1 ) :
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
            "bernoulli"     BernoulliErrorDistribution no hyperpar
            "exponential"   ExponentialErrorDistribution with 2 hyperpar (scale, power)

            ErrorDistribution Externally defined ErrorDistribution
        limits : None or [low,high] or [[low],[high]]
            None    no limits implying fixed hyperparameters of the distribution
            low     low limit on hyperpars
            high    high limit on hyperpars
            When limits are set the hyperpars are not fixed.
        ensemble : int
            number of walkers
        discard : int
            number of walkers to be replaced each generation
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
        if problem is None :
            problem = "classic"

        self.setProblem( problem, model=model, xdata=xdata, ydata=ydata, weights=weights )

        if model is None :
            model = self.problem.model

        if model is not None and not model.hasPriors() and model.npars > 0:
            warnings.warn( "Model needs priors and/or limits" )

        self.keep = keep

        if ensemble is not None :
            self.ensemble = ensemble

        self.discard = discard

        self.rng = numpy.random.RandomState( seed )
        self.seed = seed
        self.maxsize = maxsize
        object.__setattr__( self, "verbose", verbose )
        self.rate = rate
        self.restart = None                     ## TBD

        self.minimumIterations = 100
        self.end = 2.0
        self.maxtrials = 5
        self.threads = threads

        self.iteration = 0

        if distribution is not None :
            self.setErrorDistribution( distribution, limits=limits )
        elif limits is not None :
            self.setErrorDistribution( self.problem.myDistribution(), limits=limits )
        else :
            self.setErrorDistribution( self.problem.myDistribution(), scale=1.0 )

        self.setEngines( engines )

        ## Initialize the sample list
        self.samples = SampleList( model, 0, ndata=self.problem.ndata )


    #  *******SAMPLE************************************************************
    def sample( self, keep=None, plot=False ):
        """
        Sample the posterior and return the 10log( evidence )

        A additional result of this method is a SampleList which contains
        samples taken from the posterior distribution.

        Parameters
        ----------
        keep : None or dict of {int:float}
            Dictionary of indices (int) to be kept at a fixed value (float)
            Hyperparameters follow model parameters
            The values will override those at initialization.
            They are only used in this call of fit.
        plot : bool or str
            bool    show a plot of the final results
            "iter" 	show iterations
            "all"  	show iterations and final result
            "last" 	show final result

        """
        keep = self.initSample( keep=keep )

        tail = self.initReport( keep=keep, plot=plot )

        explorer = Explorer( self, threads=self.threads )

        self.logZ = -sys.float_info.max
        self.info = 0
        self.logWidth = math.log( 1.0 - math.exp( -1.0 / self.ensemble ) )


#        TBD put self.logWidth in the saved file too
#        if self.optionalRestart() :
#            self.logWidth -= self.iteration * ( 1.0 * self.discard ) / self.ensemble

        ## iterate until done
        while self.iteration < self.getMaxIter( ):

            self.walkers.sort( key=self.walkerLogL )    # sort the walker list on logL

            self.calculateUnitRange()

            worst = self.worst                      # the worst are low in the sorted ensemble
            self.lowLhood = self.walkers[worst].logL

            self.updateEvidence( worst )            # Update Z and H and store posterior samples

            self.iterReport( worst - 1, tail, plot=plot ) # some output when needed

            self.samples.weed( self.maxsize )       # remove overflow in samplelist

            self.iteration += 1

            self.updateWalkers( explorer, worst )

            self.optionalSave( )


        # End of Sampling: Update and store the remaining walkers
        self.updateEvidence( self.ensemble )        # Update Evidence Z and Information H

        # Calculate weighted average and stdevs for the parameters;
        self.samples.LogZ = self.logZ
        self.samples.info = self.info
        self.samples.normalize( )

        # put the info into the model
        if self.problem.model and not self.problem.model.isDynamic() :
            self.problem.model.parameters = self.samples.parameters
            self.problem.model.stdevs = self.samples.stdevs

        self.lastReport( -1, plot=plot )

        return self.evidence

    def initSample( self, ensemble=None, keep=None ) :

        if keep is None :
            keep = self.keep
        fitIndex, allpars = self.makeFitlist( keep=keep )

        if ensemble is None :
            ensemble = self.ensemble
        self.initWalkers( ensemble, allpars, fitIndex )

        for eng in self.engines :
            eng.walkers = self.walkers
            eng.lastWalkerId = len( self.walkers )

        self.distribution.ncalls = 0                      #  reset number of calls

        return keep

    def sortLogL( self, walkers ) :
        return numpy.argsort( [w.logL for w in walkers] )

    def walkerLogL( self, w ) :
        return w.logL

    def makeFitlist( self, keep=None ) :
        """
        Make list of indices of (hyper)parameters that need fitting.

        Parameters
        ----------
        keep : None or dict of {int : float}
            dictionary of indices that need to be kept at the float value.
        """
        allpars = numpy.zeros( self.problem.npars + self.distribution.nphypar,
                               dtype=self.problem.partype )

        np = self.problem.npars
        fitlist = [k for k in range( np )]
        nh = -self.distribution.nphypar
        for sp in self.distribution.hyperpar :
            if not sp.isFixed and sp.isBound() :
                fitlist += [nh]                             # it is to be optimised
            else :
                allpars[nh] = self.distribution.hypar[nh]   # fill in the fixed value

            nh += 1

        nh = self.distribution.nphypar
        if keep is not None :
            fitl = []
            kkeys = list( keep.keys() )
            for k in range( np + nh ) :
                if k in kkeys :
                    allpars[k] = keep[k]                    # save keep.value in allpars
                elif fitlist[k] in kkeys :
                    allpars[k] = keep[fitlist[k]]           # save keep.value in allpars
                else :
                    fitl += [fitlist[k]]                    # list of pars to be fitted
            fitlist = fitl

        return ( fitlist, allpars )

    def calculateUnitRange( self ) :
        self.engines[0].calculateUnitRange()
        for eng in self.engines :
            eng.unitRange = self.engines[0].unitRange
            eng.unitMin   = self.engines[0].unitMin


    def doIterPlot( self, plot ) :
        if isinstance( plot, str ) :
            return plot == 'iter' or plot == 'all'
        else :
            return False

    def doLastPlot( self, plot ) :
        if isinstance( plot, str ) :
            return plot == 'last' or plot == 'all'
        else :
            return plot == True


    def initReport( self, keep=None, plot=False ) :

        self.plotData( plot=self.doIterPlot( plot ) )

        if self.verbose >= 1 :
            fitIndex = self.walkers[0].fitIndex
            print( "Fit", ( "all" if keep is None
                                  else fitIndex ), "parameters of" )
            if self.problem.model :
                print( " ", self.problem.model._toString( "  " ) )
            else :
                print( " ", self.problem )
            print( "Using a", self.distribution, end="" )
            np = -1
            cstr = " with "
            for name,hyp in zip( self.distribution.PARNAMES, self.distribution.hyperpar ) :
                print( cstr, end="" )
                if np in fitIndex :
                    print( "unknown %s" % name, end="" )
                else :
                    print( "%s = %7.2f " % (name, hyp.hypar), end="" )
                np -= 1
                cstr = " and "
            print( "\nMoving the walkers with ", end="" )
            for eng in self.engines :
                print( " ", eng, end="" )
            print( "" )
            if self.threads :
                print( "Using threads." )

        tail = 0
        if self.verbose > 1 :
            while fitIndex is not None and fitIndex[-tail-1] < 0 : 
                tail += 1

#            tail = self.distribution.nphypar
            if tail == 0 :
                print( "Iteration     logZ        H       LowL     npar parameters" )
            else :
                print( "Iteration     logZ        H       LowL     npar parameters", end="" )
                for k in range( 1,  min( 5, len( fitIndex ) - tail ) ) :
                    print( "        ", end="" )
                for k in range( tail ) :
                    print( "   %s" %self.distribution.hyparname( k ), end="" )
                print( "" )

        return tail

    def iterReport( self, kw, tail, plot=False ) :

        if self.verbose >= 3 or ( self.verbose >= 1 and
                                  self.iteration % 100 == 0 ):
            if self.verbose == 1 :
                if ( self.iteration / 100 ) % 50 == 49 :
                    nwln = "\n"
                else :
                    nwln = ""
                print( ">", end=nwln, flush=True )
            else :
                pl = self.walkers[kw].allpars
                fi = self.walkers[kw].fitIndex
                if fi is not None : 
                    pl = pl[fi]
                np = len( pl )
#                tail = self.distribution.nphypar
                print( "%8d %#10.3g %8.1f %#10.3g %6d "%( self.iteration, self.logZ,
                    self.info, self.lowLhood, np ), fmt( pl, max=4, tail=tail ) )
#                print( "%-16.16s " % self.engines[1], end="" )
#                self.engines[1].printReport()


            self.plotResult( self.walkers[kw], self.iteration, plot=self.doIterPlot( plot ) )

    def lastReport( self, kw, plot=False ) :

        if self.verbose > 0 :
            if self.verbose == 1 :
                print( "\nIteration   logZ        H     LowL     npar    parameters" )
            pl = self.walkers[kw].allpars
            fi = self.walkers[kw].fitIndex
            if fi is not None : 
                pl = pl[fi]
            np = len( pl )
            print( "%8d %#10.3g %8.1f %#10.3g %6d "%( self.iteration, self.logZ,
                    self.info, self.lowLhood, np ) )
            print( fmt( pl, max=None ) )

        if self.verbose >= 1 :
            self.report()

        if self.doLastPlot( plot ) :
#            Plotter.plotFit( self.problem.xdata, self.problem.ydata, yfit=self.yfit, residuals=True )
            Plotter.plotSampleList( self.samples, self.problem.xdata, self.problem.ydata, 
                    figsize=[12,8], residuals=True )

    def getMaxIter( self ) :
        """
        Return the maximum number of iteration.
        """
        return max( self.minimumIterations, self.end * self.ensemble * self.info / self.worst )

    def getMaxIterMED( self ) :
        """
        Return the maximum number of iteration in case of EvidenceProblem.
        """
        try :
            self.csEvid += [math.exp( self.logZ )]
        except :
            self.csEvid = [math.exp( self.logZ )]

        if self.iteration < self.minimumIterations :
            return self.minimumIterations

        kmed = 0
        medlim = 0.5 * self.csEvid[-1]
        for cs in self.csEvid :
            if cs > medlim : break
            kmed += 1

        return self.end * kmed


    def getMaxIterEP( self ) :
        """
        Return the maximum number of iteration in case of EvidenceProblem.
        """
        if self.iteration < self.minimumIterations :
            return self.minimumIterations
        if ( self.samples[-1].logW < self.samples[-100].logW and 
             self.samples[-1].logW < self.logZ - 16 ) :
            return self.iteration
        else :
            return self.iteration + 100  

#   det getScale( self, walker ) :
#       np = walker.model.npchain
#       return self.distribution.getScale( walker.model, params=walker.allpars[:np] )

#  ===================================================================================
    def optionalRestart( self ):
        """
        Restart the session from a file. (not yet operational)
        """
        if self.restart is not None and self.restart.wantRestore( ):
            self.walkers, self.samples = self.restart.restore( self.walkers, self.samples )
            self.logZ = self.walkers.logZ
            self.info = self.walkers.info
            self.iteration = self.walkers.iteration
            return True
        return False

    def optionalSave( self ):
        """
        Save the session to a file. (not yet operational)
        """
        if self.restart is not None and self.restart.wantSave( ) and self.iteration % 100 == 0:
            self.walkers.logZ = self.logZ
            self.walkers.info = self.info
            self.walkers.iteration = self.iteration
            self.restart.save( self.walkers, self.samples )


    def updateEvidence( self, worst ) :
        """
        Updates the evidence (logZ) and the information (H)

        The walkers need to be sorted to logL

        Parameters
        ----------
        worst : int
            Number of walkers used in the update

        """

        for kw in range( worst ) :
            logWeight = self.logWidth + self.walkers[kw].logL

            # update evidence, logZ
            logZnew = numpy.logaddexp( self.logZ, logWeight )

            # update Information, H
            self.info = ( math.exp( logWeight - logZnew ) * self.lowLhood +
                    math.exp( self.logZ - logZnew ) * ( self.info + self.logZ ) - logZnew )

#            print( kw, fmt( self.walkers[kw].logL ), fmt( self.logWidth ), fmt( logWeight ), fmt( logZnew ), fmt( self.info ) )

            if math.isnan( self.info ) :
                self.info = 0.0
            self.logZ = logZnew

            # store posterior samples
            smpl = self.walkers[kw].toSample( logWeight )
            self.samples.add( smpl )

#            self.logWidth -= 1.0 / self.ensemble
            self.logWidth -= 1.0 / ( self.ensemble - kw )

#        self.logWidth -= worst / self.ensemble

        return

    def copyWalker( self, worst ):
        """
        Kill worst walker( s ) in favour of one of the others

        Parameters
        ----------
        worst : int
            number of Walkers to copy
        """
        for k in range( worst ) :
            kcp = self.rng.randint( worst, self.ensemble )
            self.walkers.copy( kcp, k )
            setatt( self.walkers[k], "parent", kcp )
            setatt( self.walkers[k], "start", self.iteration )


    def updateWalkers( self, explorer, worst ) :
        """
        Update the walkerlist in place.

        Parameters
        ----------
        explorer : Explorer
            Explorer object
        worst : int
            number of walkers to update
        """
        self.copyWalker( worst )

        # Explore the copied walker(s)
        wlist = [k for k in range( worst )]
        explorer.explore( wlist, self.lowLhood, self.iteration )


    #  *********INTERNALS***************************************************
    def __setattr__( self, name, value ) :

        # for hypar fitting
        if name == "scale" and isinstance( self.distribution, ScaledErrorDistribution ) :
            self.distribution.scale = value
        elif name == "power" and isinstance( self.distribution, ExponentialErrorDistribution ) :
            self.distribution.power = value
        else :
            object.__setattr__( self, name, value )
            if name == "verbose" :
                for eng in self.engines :
                    eng.verbose = value

    def __getattr__( self, name ) :

        if name == "ensemble" :
            return len( self.walkers )
        elif name == "xdata" :
            return self.problem.xdata
        elif name == "model" :
            return self.problem.model
        elif name == "ydata" :
            return self.problem.ydata
        elif name == "weights" :
            return self.problem.weights
        elif name == "worst" :
            return self.discard
        elif name == "evidence" :
            return self.logZ / math.log( 10.0 )
        elif name == "logZprecision" :
            return math.sqrt( self.info / self.ensemble )
        elif name == "precision" :
            return self.logZprecision / math.log( 10.0 )
        elif name == "information" :
            return self.info
        elif name == "parameters" :
            return self.samples.getParameters()
        elif name == "stdevs" or name == "standardDeviations" :
            self.samples.getParameters()
            return self.samples.stdevs
        elif name == "hypars" :
            return self.samples.hypars
        elif name == "stdevHypars" :
            return self.samples.stdevHypars
        elif name == "scale" :
            return self.samples.hypars[0]
        elif name == "stdevScale" :
            return self.samples.stdevHypars[0]
        elif name == "modelfit" or name == "yfit" :
            return self.samples.average( self.problem.xdata )

    #  *********DISTRIBUTIONS***************************************************

    def setProblem( self, name, model=None, xdata=None, ydata=None, weights=None ) :
        """
        Set the problem for this run.

        If name is a Problem, then the keyword arguments (xdata,model,ydata,weights)
        are overwritten provided they are not None

        Parameters
        ----------
        name : string or Problem
            name of problem
            Problem Use this one
        model : Model
            the model to be solved
        xdata : array_like or None
            independent variable
        ydata : array_like or None
            dependent variable
        weights : array_like or None
            weights associated with ydata

        """
        problemdict = {
            "classic"  : ClassicProblem,
            "errors"   : ErrorsInXandYProblem,
            "multiple" : MultipleOutputProblem,
            "evidence" : EvidenceProblem
        }
#           "salesman" : SalesmanProblem
#           "order" : OrderProblem

        if isinstance( name, Problem ) :
            self.problem = name
            if model is not None : self.problem.model = model
            if xdata is not None : self.problem.xdata = numpy.asarray( xdata )
            if ydata is not None : self.problem.ydata = numpy.asarray( ydata )
            if weights is not None : self.problem.weights = numpy.asarray( weights )
            return

        if not isinstance( name, str ) :
            raise ValueError( "Cannot interpret ", name, " as string or Problem" )

        name = str.lower( name )
        try :
            myProblem = problemdict[name]
            self.problem = myProblem( model, xdata=xdata, ydata=ydata, weights=weights )
        except :
            raise ValueError( "Unknown problem name %s" % name )



    #  *********DISTRIBUTIONS***************************************************
    def setErrorDistribution( self, name=None, limits=None, scale=1.0, power=2.0 ):
        """
        Set the error distribution for calculating the likelihood.

        Parameters
        ----------
        name : None or string or ErrorDistribution
            None    distribution is Problem dependent.
            string  name of distribution; one of
                    "gauss", "laplace", "poisson", "cauchy", "uniform",
                    "exponential", "bernoulli"
            ErrorDistribution use this one
        limits : None or [low,high] or [[low],[high]]
            None    no limits implying fixed hyperparameters (scale,power,etc)
            low     low limit on hyperpars (needs to be >0)
            high    high limit on hyperpars
            when limits are set, the hyperpars are *not* fixed.
        scale : float
            fixed scale of distribution
        power : float
            fixed power of distribution

        """
        if name is None :
            name = self.problem.myDistribution()
        elif isinstance( name, ErrorDistribution ) :
            self.distribution = name
            return

        if not isinstance( name, str ) :
            raise ValueError( "Cannot interpret ", name, " as string or ErrorDistribution" )

        name = str.lower( name )
#        print( name )
        if name == "gauss" :
            self.distribution = GaussErrorDistribution( scale=scale, limits=limits )
        elif name == "laplace" :
            self.distribution = LaplaceErrorDistribution( scale=scale, limits=limits )
        elif name == "poisson" :
            self.distribution = PoissonErrorDistribution()
        elif name == "cauchy" :
            self.distribution = CauchyErrorDistribution( scale=scale, limits=limits )
        elif name == "uniform" :
            self.distribution = UniformErrorDistribution( scale=scale, limits=limits )
        elif name == "exponential" :
            self.distribution = ExponentialErrorDistribution( scale=scale, power=power, limits=limits )
        elif name == "model" :
            self.distribution = ModelDistribution( scale=scale, limits=limits )
#            self.getMaxIter = self.getMaxIterEP
#            self.minimumIterations = max( self.minimumIterations, 100 )
        elif name == "bernoulli" :
            self.distribution = BernoulliErrorDistribution()
        else :
            raise ValueError( "Unknown error distribution %s" % name )

    def setEngines( self, engines=None, enginedict=None ) :
        """
        initialize the engines.

        Parameters
        ----------
        engines : None or [Engine] or [string]
            None       engines is Problem dependent
            [Engines]  list of Engines to use
            [string]   list engine names
        enginedict : dictionary of { str : Engine }
            connecting names to the Engines
        """

        if enginedict is None :
            enginedict = {
                "galilean" : GalileanEngine,
                "chord" :    ChordEngine,
                "birth" : 	 BirthEngine,
                "death" : 	 DeathEngine,
                "struct": 	 StructureEngine,
                "gibbs" : 	 GibbsEngine,
                "step"  : 	 StepEngine }

        if engines is None :
            engines = self.problem.myEngines()

        self.engines = []
        usePhantoms = self.step is not None

        if isinstance( engines, str ) :
            engines = [engines]
        for name in engines :
            if isinstance( name, Engine ) :
                engine = name
                engine.members = self.walkers
                engine.errdis = self.distribution
                engine.verbose = self.verbose
                if usePhantoms :
                    engine.setWalker = engine.setWalkerAdd2List
                self.engines += [engine]
                continue

            if not isinstance( name, str ) :
                raise ValueError( "Cannot interpret ", name, " as string or as Engine" )

            try :
                Eng = enginedict[name]
                seed = self.rng.randint( self.TWOP31 )
                engine = Eng( self.walkers, self.distribution,
                              seed=seed, verbose=self.verbose )
            except :
                raise ValueError( "Unknown Engine name : %10s" % name )

            self.engines += [engine]


    #  *********INITIALIZATION***************************************************
    def initWalkers( self, ensemble, allpars, fitIndex, startdict=None ):
        """
        Initialize the walkers at random values of parameters and scale

        Parameters
        ----------
        ensemble : int
            length of the walkers list
        allpars : array_like
            array of (hyper)parameters
        fitIndex : array_like
            indices of allpars to be fitted
        startdict : dictionary of { str : Engine }
            connecting a name to a StartEngine
        """
        if startdict is None :
            startdict = { "start" : StartEngine }

        # Make the walkers list
        self.walkers = WalkerList( self.problem, ensemble, allpars, fitIndex )

        if self.initialEngine is not None:
            # decorate with proper information
            self.initialEngine.members = self.walkers
            self.initialEngine.errdis = self.distribution

        else :
            try :
                name = self.problem.myStartEngine()
                StartEng = startdict[name]
                seed = self.rng.randint( self.TWOP31 )
                self.initialEngine = StartEng( self.walkers, self.distribution,
                        seed=seed )
            except :
                raise ValueError( "Unknown StartEngine name : %10s" % name )

        # Calculate logL for all walkers.
        self.distribution.lowLhood = -math.inf
        for walker in self.walkers :
            self.initialEngine.execute( walker.id, -math.inf )

#        for w in self.walkers :
#            print( w.id, w.problem.model.npars, len( w.problem.model.parameters), len( w.allpars) )
#            w.check( nhyp=self.distribution.nphypar )

    def plotData( self, plot=False ):
        """
        Initialize the plot with data.

        Parameters
        ----------
        plot : bool
            whether to plot.
        """
        if not plot :
            return
        plt.figure( 'iterplot' )
        plt.plot( self.problem.xdata, self.problem.ydata, 'k.' )
        plt.show( block=False )

    def plotResult( self, walker, iter, plot=False ):
        """
        Plot the results for a walker.

        Parameters
        ----------
        walker : Walker
            the walker to plot
        iter : int
            iteration number
        plot : bool
            whether to plot.
        """
        if not plot :
            return

        plt.figure( 'iterplot' )
        if self.line is not None :
            ax = plt.gca()
            plt.pause( 0.02 )
            ax.lines.remove( self.line )
            self.text.set_text( "Iteration %d" % iter )
        else :
            self.text = plt.title( "Iteration %d" % iter )
            self.ymin, self.ymax = plt.ylim()

        param = walker.allpars
        model = walker.problem.model
        mock = model.result( self.problem.xdata, param )
        self.line, = plt.plot( self.problem.xdata, mock, 'r-' )
        dmin = min( self.ymin, numpy.min( mock ) )
        dmax = max( self.ymax, numpy.max( mock ) )
        plt.ylim( dmin, dmax )
        plt.show( block=False )


    def report( self ):
        """
        Final report on the run.
        """
#        print( "Rate        %f" % self.rate )
        print( "Engines              success     reject     failed       best      calls" )

        for engine in self.engines :
            print( "%-16.16s " % engine, end="" )
            engine.printReport()
        print( "Calls to LogL     %10d" % self.distribution.ncalls, end="" )
        if self.distribution.nparts > 0 :
            print( "   to dLogL %10d" % self.distribution.nparts )
        else :
            print( "" )

        print( "Samples  %10d" % len( self.samples ) )
        print( "Evidence    %10.3f +- %10.3f" % (self.evidence, self.precision ) )



