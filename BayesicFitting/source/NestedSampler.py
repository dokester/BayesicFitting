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
from .LinearModel import LinearModel
from .ErrorsInXandYProblem import ErrorsInXandYProblem
from .MultipleOutputProblem import MultipleOutputProblem
from .EvidenceProblem import EvidenceProblem
from .PhantomCollection import PhantomCollection

from .ErrorDistribution import ErrorDistribution
from .ScaledErrorDistribution import ScaledErrorDistribution
from .GaussErrorDistribution import GaussErrorDistribution
from .Gauss2dErrorDistribution import Gauss2dErrorDistribution
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
from .RandomEngine import RandomEngine
## for Dynamic Models import the classes
from .BirthEngine import BirthEngine
from .DeathEngine import DeathEngine
## for Modifiable Models:
from .StructureEngine import StructureEngine

from .BaseFitter import BaseFitter

__author__ = "Do Kester"
__year__ = 2024
__license__ = "GPL3"
__version__ = "3.2.1"
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
#  *    2017 - 2024 Do Kester

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
    tolerance : float (-12)
        stopping criterion: stop if log( dZ / Z ) < tolerance
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
    TOLERANCE = -12
    END = 2
    RATE = 1.0

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, xdata=None, model=None, ydata=None, weights=None,
                accuracy=None, problem=None, distribution=None, limits=None, 
                keep=None, ensemble=ENSEMBLE, discard=1, seed=80409, rate=RATE,
                bestBoost=False,
                engines=None, maxsize=None, threads=False, verbose=1 ) :
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
        seed :int
            seed of random number generator
        rate : float
            speed of exploration
        bestBoost : bool or Fitter
            False   no updates of best logLikelihood
            True    boost the fit using LevenbergMarquardtFitter
            fitter  boost the fit using this fitter.
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

        self.setProblem( problem, model=model, xdata=xdata, ydata=ydata, weights=weights,
                         accuracy=accuracy )

        if model is None :
            model = self.problem.model

        if model is not None and not model.hasPriors() and model.npars > 0:
            warnings.warn( "Model needs priors and/or limits" )

        self.keep = keep

        if ensemble is not None :
            self.ensemble = ensemble

        self.minimumIterations = 100            # to prvent premature stops
        self.maxIterations = None               # only for testing
        self.repiter = 100                      # report status every repiter
        self.tolerance = self.TOLERANCE
        self.discard = discard

        self.rng = numpy.random.RandomState( seed )
        self.seed = seed
        self.maxsize = maxsize
        object.__setattr__( self, "verbose", verbose )
        self.rate = rate
        self.restart = None                     ## TBD

        self.bestBoost = bestBoost

        self.end = self.END
        self.maxtrials = 5
        self.threads = threads

        self.iteration = 0

        if distribution is not None :
            self.setErrorDistribution( distribution, limits=limits )
        elif limits is not None :
            self.setErrorDistribution( limits=limits )
        else :
            self.setErrorDistribution( scale=1.0 )

        self.setEngines( engines )

        ## Initialize the sample list
        self.samples = SampleList( model, 0, ndata=self.problem.ndata )

        """
        The order in which the main attributes are created.

        where       method                  attribute
        __init__    setProblem              self.problem
        __init__    setErrorDistribution    self.distribution
        __init__    setEngines              self.phantoms
                                            self.engines
        __init__                            self.samples
        sample      initSample
                      initWalkers           self.walkers
                        setInitialEngine    self.initialEngine
        """                                            
    
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
            "test"      plot iterations but dont show (for testing)
        """
        keep = self.initSample( keep=keep )

        if ( self.problem.hasAccuracy and self.walkers[0].fitIndex[-1] < 0 and 
                not isinstance( self.distribution, GaussErrorDistribution ) ) :
            raise AttributeError( "%s cannot be combined with accuracies and variable scale" %
                                    self.distribution ) 

#        if self.minimumIterations is None :
#            self.minimumIterations = 10 * self.ensemble / self.discard

        tail = self.initReport( keep=keep )

        explorer = Explorer( self, threads=self.threads )

        ## move all walkers around for initial exploration of the complete space.
        if not isinstance( self.problem.model, LinearModel ) :
            self.lowLhood = -sys.float_info.max
            # Explore all walker(s)
            explorer.explore( range( self.ensemble ), self.lowLhood, self.iteration )
            self.iteration = 0                  # reset iteration number


        self.logZ = -sys.float_info.max
        self.logdZ = 0
        self.info = 0
        self.logWidth = math.log( 1.0 - math.exp( -1.0 / self.ensemble ) )

#        TBD put self.logWidth in the saved file too
#        if self.optionalRestart() :
#            self.logWidth -= self.iteration * ( 1.0 * self.discard ) / self.ensemble

        self.histinsert = []
        ## iterate until done
#        while self.iteration < self.getMaxIter( ):
        while self.nextIteration() :

            self.walkers.sort( key=self.walkerLogL )    # sort the walker list on logL

            worst = self.worst                      # the worst are low in the sorted ensemble
            self.lowLhood = self.walkers[worst-1].logL

            self.updateEvidence( worst )            # Update Z and H and store posterior samples

            self.iterReport( worst - 1, tail, plot=plot ) # some output when needed

            self.samples.weed( self.maxsize )       # remove overflow in samplelist

            self.iteration += 1

            self.updateWalkers( explorer, worst )

            newL = self.walkers[worst-1].logL
            self.histinsert += [self.walkers.firstIndex( newL )]

            self.optionalSave( )


        # End of Sampling: Update and store the remaining walkers
        self.updateEvidence( self.ensemble )        # Update Evidence Z and Information H

        # Calculate weighted average and stdevs for the parameters;
        self.samples.LogZ = self.logZ
        self.samples.info = self.info
        self.samples.normalize( )

        # put the info into the model
        if self.problem.model and not self.problem.isDynamic() :
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
            if self.bestBoost :
                eng.bestBoost( self.problem, myFitter=self.myFitter )

        self.distribution.ncalls = 0                      #  reset number of calls

        return keep

#   Not in Use
#    def sortLogL( self, walkers ) :
#        return numpy.argsort( [w.logL for w in walkers] )

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
            elif self.problem.hasAccuracy and nh == -self.distribution.nphypar :
                allpars[nh] = 0                             # fix (model)scale at 0
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


    def doIterPlot( self, plot ) :
        """
        Returns
        -------
        int 0   no plot
            1   plot
            2   plot but dont show (for testing)
        """
        if isinstance( plot, str ) :
            if plot == 'iter' or plot == 'all' :
                return 1
            elif plot == 'test' :
                return 2
            else :
                return 0
        else :
            return 0

    def doLastPlot( self, plot ) :
        """
        Return
        ------
        True when the last plot is requested (plot equals 'last' or 'all' or True)
        False otherwise
        """
        if isinstance( plot, str ) :
            return plot == 'last' or plot == 'all'
        else :
            return plot == True


    def initReport( self, keep=None ) :

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
            while fitIndex is not None and fitIndex[-tail-1] < 0 and len( fitIndex ) > tail + 1 : 
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
                                  self.iteration % self.repiter == 0 ):
            if self.verbose == 1 :
                if ( self.iteration / self.repiter ) % 50 == 49 :
                    nwln = "\n"
                else :
                    nwln = ""
                print( ">", end=nwln, flush=True )
            else :
                self.printIterRep( kw, tail=tail, max=4 )

            self.plotResult( self.walkers[kw], self.iteration, plot=self.doIterPlot( plot ) )


    def printIterRep( self, kw, parfmt="%s", tail=0, max=None, indent=0, end="\n" ) :

        pl = self.walkers[kw].allpars
        fi = self.walkers[kw].fitIndex
        if fi is not None : 
            pl = pl[fi]
        np = len( pl )

        print( "%8d %#10.3g %8.1f %#10.3g %6d "%( self.iteration, self.logZ,
                self.info, self.lowLhood, np ), 
                parfmt % fmt( pl, max=max, tail=tail, indent=indent ), end=end )

        """
        if self.iteration % 1000 == 0 :
            print( fmt( pl, max=None ) )
            npars = self.walkers[kw].problem.npars
            pmn, pmx = self.phantoms.getParamMinmax( self.lowLhood, npars )
            print( fmt( pmn, max=None ) )
            print( fmt( pmx, max=None ) )
            print( fmt( np ), fmt( self.phantoms.length( npars ) ), 
                   fmt( self.logdZ, format="%10.3g" ) )
            for ky in self.phantoms.phantoms :
                print( fmt( ky ), fmt( len( self.phantoms.phantoms[ky] ) ) )
        """

    def lastReport( self, kw, plot=False ) :

        if self.verbose > 0 :
            if self.verbose == 1 :
                print( "\nIteration     logZ        H       LowL     npar" )

            self.printIterRep( kw, max=None, indent=13, parfmt="\nParameters  %s" )


#            pl = self.walkers[kw].allpars
#            fi = self.walkers[kw].fitIndex
#            if fi is not None : 
#                pl = pl[fi]
#            np = len( pl )
#            print( "%8d %#10.3g %8.1f %#10.3g %6d "%( self.iteration, self.logZ,
#                    self.info, self.lowLhood, np ) )
#            print( "Parameters  ", fmt( pl, max=None, indent=13 ) )

        if self.verbose >= 1 :
            self.report()

        if self.doLastPlot( plot ) :
            self.plotLast()

    def plotLast( self ) :
        Plotter.plotSampleList( self.samples, self.problem.xdata, self.problem.ydata, 
                    figsize=[12,8], residuals=True )

    def getMaxIter( self ) :
        """
        Return the maximum number of iteration.
        """
        maxi = ( self.iteration if self.logdZ < self.tolerance else 
                 self.end * self.ensemble * self.info / self.worst )
        maxi = max( self.minimumIterations, maxi )
        return maxi if self.maxIterations is None else min( maxi, self.maxIterations )

    def nextIteration( self ) :
        """
        Return True when a next iteration is needed. False to stop
        """
        if self.iteration < self.minimumIterations :
            return True
        if self.logdZ < self.tolerance :
            return False
        if self.maxIterations is not None and self.iteration > self.maxIterations :
            return False
        if self.iteration > self.end * self.ensemble * self.info / self.worst :
            return False
        return True

    def __str__( self ):
        """ Return the name of this sampler.  """
        return str( "NestedSampler" )


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
            logWeight = self.logWidth + self.walkers[kw].logL + self.walkers[kw].logPrior

            # update evidence, logZ
            logZnew = numpy.logaddexp( self.logZ, logWeight )

            # update Information, H
            self.info = ( math.exp( logWeight - logZnew ) * self.lowLhood +
                    math.exp( self.logZ - logZnew ) * ( self.info + self.logZ ) - logZnew )

            if math.isnan( self.info ) :
                self.info = 0.0
            self.logZ = logZnew

            # store posterior samples
            smpl = self.walkers[kw].toSample( logWeight )
            self.samples.add( smpl )

            self.logWidth -= 1.0 / ( self.ensemble - kw )

        self.logdZ = logWeight - self.logZ

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
            self.walkers.copy( kcp, k, start=self.iteration )
#            setatt( self.walkers[k], "parent", kcp )
#            setatt( self.walkers[k], "start", self.iteration )
#            setatt( self.walkers[k], "step", 0 )

    def copyWalkerFromPhantoms( self, worst ):
        """
        Kill worst walker( s ) in favour of one of the others

        Parameters
        ----------
        worst : int
            number of Walkers to copy
        """
        plen = self.phantoms.length()

        for k in range( worst ) :
            while True :
                kcp = self.rng.randint( plen )
                if self.phantoms.phantoms[kcp].logL > self.lowLhood :
                    break
            self.walkers.copy( kcp, k, wlist=self.phantoms.phantoms,
                               start=self.iteration )
#            setatt( self.walkers[k], "parent", kcp )
#            setatt( self.walkers[k], "start", self.iteration )

    def copyWalkerFromDynamicPhantoms( self, worst ):
        """
        Kill worst walker( s ) in favour of one of the others

        Parameters
        ----------
        worst : int
            number of Walkers to copy
        """
        plen = self.phantoms.length()
        for k in range( worst ) :
            while True :
                kcp = self.rng.randint( plen )
    
                for pk in self.phantoms.phantoms.keys() :
                    pklen = self.phantoms.length( np=pk )
                    if kcp < pklen :
                        break
                    kcp -= pklen

                if self.phantoms.phantoms[pk][kcp].logL > self.lowLhood :
                    break

            self.walkers.copy( kcp, k, wlist=self.phantoms.phantoms[pk],
                               start=self.iteration )
#            setatt( self.walkers[k], "parent", kcp )
#            setatt( self.walkers[k], "start", self.iteration )



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
        elif name == "copymode" and value == 1 :
            if self.problem.isDynamic() :
                self.copyWalker = self.copyWalkerFromDynamicPhantoms
            else :
                self.copyWalker = self.copyWalkerFromPhantoms
        elif name == "bestUpdate" :

            self.myFitter = None
            if Tools.subclassof( value, BaseFitter ) :
                object.__setattr__( self, name, True )
                self.myFitter = value
            else :
                object.__setattr__( self, name, value )

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
            return math.sqrt( max( self.info, 0 ) / self.ensemble )
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

    def setProblem( self, name, model=None, xdata=None, ydata=None, weights=None,
                    accuracy=None ) :
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
        accuracy : float or array_like or None
            of the data

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
            if accuracy is not None : self.problem.setAccuracy( accuracy=accuracy )
            return

        if not isinstance( name, str ) :
            raise ValueError( "Cannot interpret ", name, " as string or Problem" )

        name = str.lower( name )
        try :
            myProblem = problemdict[name]
            self.problem = myProblem( model, xdata=xdata, ydata=ydata, weights=weights,
                                      accuracy=accuracy )
        except :
            raise 
#            raise ValueError( "Unknown problem name %s" % name )



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
                    "exponential", "gauss2d", "model", "bernoulli"
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
        elif name == "gauss2d" :
            self.distribution = Gauss2dErrorDistribution( scale=scale, limits=limits )
        elif name == "model" :
            self.distribution = ModelDistribution( scale=scale, limits=limits )
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
        ## the same for all engines. 
        self.phantoms = PhantomCollection( dynamic=self.problem.isDynamic() )

        if enginedict is None :
            enginedict = {
                "galilean" : GalileanEngine,
                "chord" : ChordEngine,
                "birth" : BirthEngine,
                "death" : DeathEngine,
                "struct": StructureEngine,
                "gibbs" : GibbsEngine,
                "random": RandomEngine,
                "step"  : StepEngine }

        if engines is None :
            engines = self.problem.myEngines()

        self.engines = []
        if isinstance( engines, str ) :
            engines = [engines]
        for name in engines :
            if isinstance( name, Engine ) :
                engine = name
                engine.walkers  = self.walkers
                engine.errdis   = self.distribution
                engine.phantoms = self.phantoms
                engine.verbose  = self.verbose
                self.engines   += [engine]
                continue

            if not isinstance( name, str ) :
                raise ValueError( "Cannot interpret ", name, " as string or as Engine" )

            try :
                Eng = enginedict[name]
                seed = self.rng.randint( self.TWOP31 )
                engine = Eng( self.walkers, self.distribution, seed=seed, 
                            phantoms=self.phantoms, verbose=self.verbose )
            except :
                raise ValueError( "Unknown Engine name : %10s" % name )

            self.engines += [engine]


    #  *********INITIALIZATION***************************************************
    def setInitialEngine( self, ensemble, allpars, fitIndex, startdict=None ):
        """
        Initialize the walkers at random values of parameters and scale

        Parameters
        ----------
        ensemble : int
            length of the walkers list

        TBC : remove allpars and fitIndex

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
#        walker = Walker( 0, self.problem, numpy.asarray( allpars ), fitIndex )
#        self.walkers = WalkerList( walker=walker, ensemble=ensemble )

        if self.initialEngine is not None:
            # decorate with proper information
            self.initialEngine.walkers = self.walkers
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

        # pass the PhantomCollection to the initial engine
        self.initialEngine.phantoms = self.phantoms

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
        # Make the walkers list
        walker = Walker( 0, self.problem, numpy.asarray( allpars ), fitIndex )
        self.walkers = WalkerList( walker=walker, ensemble=ensemble )

        self.setInitialEngine( ensemble, allpars, fitIndex, startdict=startdict )

        for walker in self.walkers :
            self.initialEngine.execute( walker.id, -math.inf )

#        for w in self.walkers :
#            print( w.id, w.problem.model.npars, len( w.problem.model.parameters), len( w.allpars) )
#            w.check( nhyp=self.distribution.nphypar )


    def plotResult( self, walker, iter, plot=0 ):
        """
        Plot the results for a walker.

        Parameters
        ----------
        walker : Walker
            the walker to plot
        iter : int
            iteration number
        plot : int (one of (0,1,2)
            0 immediate return, no action
            1 plot
            2 plot but dont show (for testing)
        """
        if plot == 0 :
            return

        plt.figure( 'iterplot' )

        if self.line is not None :
            ax = plt.gca()
            if plot < 2 :
                plt.pause( 0.02 )       ## updates and displays the plot before pause
            ax.remove( )
            self.text.set_text( "Iteration %d" % iter )

        if self.ymin is None :
            self.ymin = numpy.min( self.problem.ydata )
            self.ymax = numpy.max( self.problem.ydata )

        param = walker.allpars
        model = walker.problem.model
        mock = model.result( self.problem.xdata, param )
        plt.plot( self.problem.xdata, self.problem.ydata, 'k.' )
        self.text = plt.title( "Iteration %d" % iter )
        self.line, = plt.plot( self.problem.xdata, mock, 'r-' )
        dmin = min( self.ymin, numpy.min( mock ) )
        dmax = max( self.ymax, numpy.max( mock ) )
        dd = 0.05 * ( dmax - dmin ) 
        plt.ylim( dmin - dd, dmax + dd )


    def report( self ):
        """
        Final report on the run.
        """
#        print( "Rate        %f" % self.rate )
        print( "Engines              success     reject     failed", end="" )
        if self.bestBoost :
            print( "       best", end="" )
        print( "      calls" )

        for engine in self.engines :
            print( "%-16.16s " % engine, end="" )
            engine.printReport( best=self.bestBoost )
        print( "Calls to LogL     %10d" % self.distribution.ncalls, end="" )
        if self.distribution.nparts > 0 :
            print( "   to dLogL %10d" % self.distribution.nparts )
        else :
            print( "" )

        print( "Samples  %10d" % len( self.samples ) )
        print( "Evidence    %10.3f +- %10.3f" % (self.evidence, self.precision ) )



