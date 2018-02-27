from __future__ import print_function

import numpy as numpy
from astropy import units
import math
from . import Tools
from .Formatter import formatter as fmt
from . import Plotter
import sys
import warnings
import matplotlib.pyplot as plt

from .Model import Model
from .Sample import Sample
from .SampleList import SampleList
from .ErrorDistribution import ErrorDistribution
from .ScaledErrorDistribution import ScaledErrorDistribution
from .GaussErrorDistribution import GaussErrorDistribution
from .LaplaceErrorDistribution import LaplaceErrorDistribution
from .PoissonErrorDistribution import PoissonErrorDistribution
from .CauchyErrorDistribution import CauchyErrorDistribution
from .GenGaussErrorDistribution import GenGaussErrorDistribution
from .Explorer import Explorer
from .Engine import Engine
from .StartEngine import StartEngine
from .GibbsEngine import GibbsEngine
from .GalileanEngine import GalileanEngine
from .StepEngine import StepEngine


## for Dynamic Models import the classes
from .BirthEngine import BirthEngine
from .DeathEngine import DeathEngine

#######  For later #################
## for Order Problems import the classes
#from OrderProblem import OrderProblem
#from DistanceCostFunction import DistanceCostFunction
#from StartOrderEngine import StartOrderEngine
#from OrderEngine import OrderEngine
#from ReverseEngine import ReverseEngine
#from ShuffleEngine import ShuffleEngine
#from SwitchEngine import SwitchEngine


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

class NestedSampler( object ):
    """
    A novel technique to do Bayesian calculation.

    NestedSampler produces `Sample`s from the posterior probability
    distribution of the parameters, given a `Model` and a
    dataset ( x-values, y-values and optionally weights ).
    The Samples are collected in a `SampleList`.

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
    calculated, which is equal to the evidence for the resulting parameters,
    given the dataset.

    There are 5 different likelihood functions available: Gaussian (Normal),
    Laplace (Exponential), Poisson (for counting processes),
    Cauchy (aka Lorentz) and a generalized Gaussian.
    By default the Gaussian distribution is used.

    Except for Poisson, all others are `ScaledErrorDistribution`s. The scale is
    a `HyperParameter` which can either be fixed, by setting the attribute
    errdis.scale or optimized, given the model parameters and the data.
    By default it is optimized for Gaussian and Laplace distributions.
    The prior for the noise scale is a Jeffreys distribution.

    The generalized Gaussian also has a power. It is also a `HyperParameter`
    which can be fixed or optimized. Its default is 2 (==Gaussian).

    For the random walk of the parameters 4 so-called engines are written.
    By default only he first is switched on.

    GalileanEngine. It walks all (super)parameters in a fixed direction
        for about 5 steps. When a step ends outside the high likelihood
        region the direction is mirrored on the lowLikelihood edge and
        continued.

    GibbsEngine. It moves each of the parameters by a random step.
        It is a randomwalk.

    StepEngine. It moves all parameters in a random direction.
        It is a randomwalk.

    CrossEngine. The parameters of 2 walkers are mixed in a random way.

    For dynamic models 2 extra engines are defined:

    BirthEngine. It tries to increase the number of parameters.
    DeathEngine. It tries to decrease the number of parameters.

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
    end : float (2.0)
        stopping criterion
    verbose : int
        level of blabbering

    walkers : SampleList
        ensemble of Samples that explore the likelihood space
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
    TWOP32 = 2 ** 32


    #  *********CONSTRUCTORS***************************************************
    def __init__( self, xdata, model, ydata, weights=None, distribution=None,
                keep=None, ensemble=100, discard=1, seed=80409, rate=1.0,
                limits=None, engines=None, maxsize=None, verbose=1 ) :
        """
        Create a new class, providing inputs and model.

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
        keep : None or dict of {int:float}
            None : none of the model parameters are kept fixed.
            Dictionary of indices (int) to be kept at a fixed value (float).
            Hyperparameters follow model parameters.
            The values will override those at initialization.
            They are used in this instantiation, unless overwritten at the call to sample()
        distribution : None or String or ErrorDistribution
            None   : GaussErrorDistribution is chosen with (fixed) scale equal to 1.0

            "gauss"    : `GaussErrorDistribution`    with 1 hyperpar scale
            "laplace"  : `LaplaceErrorDistribution`  with 1 hyperpar scale
            "poisson"  : `PoissonErrorDistribution`  no hyperpar
            "cauchy"   : `CauchyErrorDstribution`    with 1 hyperpar scale
            "gengauss" : `GenGaussErrorDistribution` with 2 hyperpar (scale, power)
            Only for OrderProblems: (for later)
            "distance" : `DistanceCostFunction`      no hyperpar

            Error distribution class which implements logLikelihood

            When the hyperpar(s) are not to be kept fixed, they need `Prior` and maybe limits.
        ensemble : int (100)
            number of walkers
        discard : int (1)
            number of walkers to be replaced each generation
        seed : int (80409)
            seed of rng
        rate : float (1.0)
            speed of exploration
        engines : None or (list of) string or (list of) Engine
            to randomly move the walkers around, within the likelihood bound.

            "galilean"  : GalileanEngine
            "gibbs" 	: GibbsEngine 	move one parameter at a time
            "step"  	: StepEngine    move all parameters in arbitrary direction

            For OrderProblems (for later)
            "order"   : insert a snippet of parameters at another location
            "reverse" : reverse the order of a snippet of parameters

            For Dynamic models only
            "birth" : BirthEngine   increase the parameter list of a walker by one
            "death" : DeathEngine   decrease the parameter list of a walker by one

            None    : take default ["galilean"]. When the model is Dynamic
                      the list is supplemented with ["birth", "death"]

            engine  : a class inheriting from Engine. At least implementing
                      execute( walker, lowLhood, fitIndex )
        maxsize : None or int
            maximum size of the resulting sample list (None : no limit)
        vebose : int
            0 : silent
            1 : basic information
            2 : more about every 100th iteration
            3 : more about every iteration

        """
        self.xdata = xdata
        self.model = model
        if not ( self.model.priors and all( p.isBound() for p in self.model.priors ) ) :
            warnings.warn( "Model needs priors and/or limits" )
        self.ydata = ydata
        self.weights = weights
        self.keep = keep

        self.ensemble = ensemble
        self.discard = discard
        self.rng = numpy.random.RandomState( seed )
        self.seed = seed
        self.maxsize = maxsize
        self.verbose = verbose
        self.rate = rate
        self.restart = None                     ## TBD

        self.minimumIterations = 100
        self.end = 2.0
        self.maxtrials = 5

        self.iteration = 0

        if distribution is not None :
            self.setErrorDistribution( distribution )
#        elif isinstance( model, OrderProblem ) :
#            self.setErrorDistribution( "distance" )
        else :
            self.setErrorDistribution( "gauss", scale=1.0 )

#        print( distribution.hyperpar[0].getLimits() )
#        print( self.distribution.hyperpar[0].getLimits() )

        self.setEngines( engines )

        ## Initialize the sample list
        self.samples = SampleList( model, 0, self.distribution, ndata=len( ydata ) )

    def makeFitlist( self, keep=None ) :
        """
        Make list of indices of (hyper)parameters that need fitting.

        Parameters
        ----------
        keep : None or dict of {int : float}
            dictionary of indices that need to be kept at the float value.
        """

        np = len( self.model.parameters )
        fitlist = [k for k in range( np )]
        nh = -1
        for sp in self.distribution.hyperpar :
            if not sp.isFixed and sp.isBound() :
                fitlist += [nh]
            nh -= 1

        if keep is not None :
            fitlist = numpy.setxor1d( fitlist, list( keep.keys() ) )
            self.model.parameters[list(keep.keys())] = list( keep.values() )

        return fitlist


    #  *******SAMPLE************************************************************
    def sample( self, keep=None, plot=False ):
        """
        Sample the posterior and return the weighted average result of the
        Model.

        The more sensible result of this method is a SampleList which contains
        samples taken from the posterior distribution.

        Parameters
        ----------
        keep : None or dict of {int:float}
            Dictionary of indices (int) to be kept at a fixed value (float)
            Hyperparameters follow model parameters
            The values will override those at initialization.
            They are only used in this call of fit.
        plot : bool
            Show a plot of the results

        """
        if keep is None :
            keep = self.keep
        fitlist = self.makeFitlist( keep=keep )

        self.initWalkers( fitlist=fitlist )

        for eng in self.engines :
            eng.walkers = self.walkers

        self.distribution.ncalls = 0                      #  reset number of calls

        self.plotData( )

        if self.verbose >= 1 :
            print( "Fit", ( "all" if keep is None else fitlist ), "parameters of" )
            print( " ", self.model._toString( "  " ) )
            print( "Using a", self.distribution, "with", end="" )
            np = -1
            cstr = " with "
            for name,hyp in zip( self.distribution.PARNAMES, self.distribution.hyperpar ) :
                print( cstr, end="" )
                if np in fitlist :
                    print( "unknown %s" % name, end="" )
                else :
                    print( "%s = %7.2f " % (name, hyp.hypar), end="" )
                np -= 1
                cstr = " and "
            print( "\nMoving the walkers with ", end="" )
            for eng in self.engines :
                print( " ", eng, end="" )
            print( "" )


        if self.verbose >= 2:
            print( "Iteration   logZ        H     LowL     npar    parameters" )

        explorer = Explorer( self )

        self.logZ = -sys.float_info.max
        self.info = 0

        logWidth = math.log( 1.0 - math.exp( (-1.0 * self.discard ) / self.ensemble) )

#        for w in self.walkers :
#            print( w.id, w.allpars, w.logL )

        if self.optionalRestart() :
            logWidth -= self.iteration * ( 1.0 * self.discard ) / self.ensemble

        while self.iteration < self.getMaxIter( ):

            #  find worst walker(s) in ensemble
            worst = self.findWorst()
            worstLogW = logWidth + self.walkers[worst[-1]].logL

            # Keep posterior samples
            self.storeSamples( worst, worstLogW - math.log( self.discard ) )

            # Update Evidence Z and Information H
            logZnew = numpy.logaddexp( self.logZ, worstLogW )

            self.info = ( math.exp( worstLogW - logZnew ) * self.lowLhood +
                    math.exp( self.logZ - logZnew ) * ( self.info + self.logZ ) - logZnew )
            self.logZ = logZnew

            if self.verbose >= 3 or ( self.verbose >= 2 and self.iteration % 100 == 0 ):
                kw = worst[0]
                pl = self.walkers[kw].allpars[self.walkers[kw].fitIndex]
                np = len( pl )
                print( "%8d %8.1f %8.1f %8.1f %6d "%( self.iteration, self.logZ, self.info,
                        self.lowLhood, np ), fmt( pl ) )

                self.plotResult( worst[0], self.iteration )

            self.samples.weed( self.maxsize )                # remove overflow in samplelist

            self.copyWalker( worst )

            # Explore the copied walker(s)
#            print( "NS     ", self.walkers[worst[0]].allpars, fitlist )
            explorer.explore( worst, self.lowLhood, fitlist )

            # Shrink the interval
            logWidth -= ( 1.0 * self.discard ) / self.ensemble
            self.iteration += 1

            self.optionalSave( )


        # End of Sampling
        self.addEnsembleToSamples( logWidth )

        # Calculate weighted average and stdevs for the parameters;
        self.samples.LogZ = self.logZ
        self.samples.info = self.info
        self.samples.normalize( )

        # put the info into the model
        if not self.model.isDynamic() :
            self.model.parameters = self.samples.parameters
            self.model.stdevs = self.samples.stdevs

        if self.verbose >= 1 :
            self.report()

#        for eng in self.engines :
#            print( eng )
#            print( " s  ", eng.succ )
#            print( " f  ", eng.fail )

        yfit = self.samples.average( self.xdata )
        if plot :
            Plotter.plotFit( self.xdata, self.ydata, yfit=yfit,
                             residuals=True )

        return yfit

    def getMaxIter( self ) :
        return max( self.minimumIterations, self.end * self.ensemble * self.info / self.discard )


#  ===================================================================================
    def optionalRestart( self ):

        if self.restart is not None and self.restart.wantRestore( ):
            self.walkers, self.samples = self.restart.restore( self.walkers, self.samples )
            self.logZ = self.walkers.logZ
            self.info = self.walkers.info
            self.iteration = self.walkers.iteration
            return True
        return False

    def optionalSave( self ):
        if self.restart is not None and self.restart.wantSave( ) and self.iteration % 100 == 0:
            self.walkers.logZ = self.logZ
            self.walkers.info = self.info
            self.walkers.iteration = self.iteration
            self.restart.save( self.walkers, self.samples )

    def storeSamples( self, worst, worstLogW ):
        for kw in worst :
            self.walkers[kw].logW = worstLogW
            self.samples.add( self.walkers, kw )

    def findWorst( self ):
        """
        Find discard bad points in ensemble. In order worse to better.
        lowLhood is the "best" in the bad points.

        """
        worst = []
        for k in range( self.discard ) :
            self.lowLhood = sys.float_info.max
            for i in range( self.ensemble ):
                if self.walkers[i].logL < self.lowLhood :
                    if i in worst :
                        continue
                    bad = i
                    self.lowLhood = self.walkers[i].logL
            worst += [bad]
        return worst

    def copyWalker( self, worst ):
        """
        Kill worst walker( s ) in favour of one of the others

        """
        sworst = sorted( worst )
#        print( worst, sworst )
        for k in range( self.discard ):
            kcp = self.rng.randint( 0, self.ensemble - self.discard )
            for kk in range( self.discard ):
                if kcp >= sworst[kk] :
                    kcp += 1
            self.walkers.copy( kcp, worst[k] )

    def addEnsembleToSamples( self, logWidth ):
        """
        Add the ensemble walkers to the samples
        """
        done = [False] * self.ensemble

        for nest in range( self.ensemble ):
            # skip walkers already done
            worst = 0
            while done[worst] : worst += 1

            #  find worst walker in ensemble not yet handled
            self.lowLhood = self.walkers[worst].logL
            for i in range( worst+1, self.ensemble ) :
                logl = self.walkers[i].logL
                if logl < self.lowLhood and not done[i]:
                    worst = i
                    self.lowLhood = logl

            worstLogW = logWidth + self.lowLhood
            self.walkers[worst].logW = worstLogW

            # Update Evidence Z and Information H
            logZnew = numpy.logaddexp( self.logZ, worstLogW )
            self.info = ( math.exp( worstLogW - logZnew ) * self.lowLhood +
                math.exp( self.logZ - logZnew ) * ( self.info + self.logZ ) - logZnew )
            self.logZ = logZnew

            # Keep posterior sample
            self.samples.add( self.walkers, worst )

            done[worst] = True


    #  *********INTERNALS***************************************************
    def __setattr__( self, name, value ) :

        ### TBD hypar fitting
        if name == "scale" and isinstance( self.distribution, ScaledErrorDistribution ) :
            self.distribution.scale = value
        elif name == "power" and isinstance( self.distribution, GenGaussErrorDistribution ) :
            self.distribution.power = value
        else :
            object.__setattr__( self, name, value )

    def __getattr__( self, name ) :
        if name == "evidence" :
            return self.logZ / math.log( 10.0 )
        if name == "logZprecision" :
            return math.sqrt( self.info * self.discard / self.ensemble )
        if name == "precision" :
            return self.logZprecision / math.log( 10.0 )
        if name == "information" :
            return self.info

        if name == "parameters" :
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

    #  *********DISTRIBUTIONS***************************************************
    def setErrorDistribution( self, name, scale=1.0, power=2.0 ):
        """
        Set the error distribution for calculating the likelihood.

        Parameters
        ----------
        name : string
            name of distribution: "gauss", "laplace", "poisson", "cauchy", "gengauss"
        scale : float
            fixed scale of distribution
        power : float
            fixed power of distribution

        """
        if isinstance( name, ErrorDistribution ) :
            self.distribution = name
            self.distribution.xdata = self.xdata
            self.distribution.data  = self.ydata
            self.distribution.weights = self.weights
            return

        if not isinstance( name, str ) :
            raise ValueError( "Cannot interpret ", name, " as string or ErrorDistribution" )

        name = str.lower( name )
#        print( name )
        if name == "gauss" :
            self.distribution = GaussErrorDistribution( self.xdata, self.ydata,
                    weights=self.weights, scale=scale )
        elif name == "laplace" :
            self.distribution = LaplaceErrorDistribution( self.xdata, self.ydata,
                    weights=self.weights, scale=scale )
        elif name == "poisson" :
            self.distribution = PoissonErrorDistribution( self.xdata, self.ydata,
                    weights=self.weights )
        elif name == "cauchy" :
            self.distribution = CauchyErrorDistribution( self.xdata, self.ydata,
                    weights=self.weights, scale=scale )
        elif name == "gengauss" :
            self.distribution = GenGaussErrorDistribution( self.xdata, self.ydata,
                    weights=self.weights, scale=scale, power=power )
        elif name == "distance" :
            self.distribution = DistanceCostFunction( self.xdata, self.ydata,
                    weights=self.weights )
        else :
            raise ValueError( "Unknown error distribution %s" % name )

    def setEngines( self, engines ) :
        """
        initialize the engines.

        Parameters
        ----------
        engines : list of string
            list of engine names
        """
        if engines is not None :
            pass
#        elif isinstance( self.model, OrderProblem ) :
#            engines = ["order", "reverse", "shuffle", "switch"]
        else :
            engines = ["galilean"]

        if self.model.isDynamic() :
            engines += ["birth", "death"]


        self.engines = []
        if isinstance( engines, str ) :
            engines = [engines]
        for name in engines :
            if isinstance( name, Engine ) :
                engine = name
                engine.members = self.walkers
                engine.errdis = self.distribution
                self.engines += [engine]
                continue

            if not isinstance( name, str ) :
                raise ValueError( "Cannot interpret ", name, " as string or as Engine" )


            if name == "galilean" :
                seed = self.rng.randint( self.TWOP32 )
#                print( "Galil    ", seed )
                engine = GalileanEngine( self.walkers, self.distribution, seed=seed )
            elif name == "gibbs" :
                seed = self.rng.randint( self.TWOP32 )
                engine = GibbsEngine( self.walkers, self.distribution, seed=seed )
            elif name == "step" :
                seed = self.rng.randint( self.TWOP32 )
                engine = StepEngine( self.walkers, self.distribution, seed=seed )
####        Order Problems (for later)
#            elif name == "order" :
#                seed = self.rng.randint( self.TWOP32 )
#                engine = OrderEngine( self.walkers, self.distribution, seed=seed )
#            elif name == "reverse" :
#                seed = self.rng.randint( self.TWOP32 )
#                engine = ReverseEngine( self.walkers, self.distribution, seed=seed )
#            elif name == "shuffle" :
#                seed = self.rng.randint( self.TWOP32 )
#                engine = ShuffleEngine( self.walkers, self.distribution, seed=seed )
#            elif name == "switch" :
#                seed = self.rng.randint( self.TWOP32 )
#                engine = SwitchEngine( self.walkers, self.distribution, seed=seed )

####        For Dynamic Models
            elif name == "birth" :
                seed = self.rng.randint( self.TWOP32 )
#                print( "Birth    ", seed )
                engine = BirthEngine( self.walkers, self.distribution, seed=seed )
            elif name == "death" :
                seed = self.rng.randint( self.TWOP32 )
#                print( "Death    ", seed )
                engine = DeathEngine( self.walkers, self.distribution, seed=seed )
            else :
                raise ValueError( "Unknown Engine name : %10s" % name )

            self.engines += [engine]


    #  *********INITIALIZATION***************************************************
    def initWalkers( self, fitlist=None ):
        """
        Initialize the walkers at random values of parameters and scale
        """
        self.walkers = SampleList( self.model, self.ensemble, self.distribution,
                fitindex=fitlist )

        if self.initialEngine is not None:
            # decorate with proper information
            self.initialEngine.members = self.walkers
            self.initialEngine.errdis = self.distribution
#        elif isinstance( self.model, OrderProblem ) :
#            seed = self.rng.randint( self.TWOP32 )
#            self.initialEngine = StartOrderEngine( self.walkers, self.distribution,
#                        seed=seed )
        else :
            seed = self.rng.randint( self.TWOP32 )
#            print( "Start    ", seed )
            self.initialEngine = StartEngine( self.walkers, self.distribution,
                        seed=seed )

        for walker in self.walkers :
            self.initialEngine.execute( walker, 0, fitIndex=fitlist )


    def plotData( self ):
        if self.plotter is None:
            return
        inp = self.xdata.getNumericData( )
        self.plotter.plotData( inp, self.data, "Iteration plot" )

    def plotResult( self, walkerId, iter ):
        if self.plotter is None:
            return
        inp = self.xdata.getNumericData( )
        param = self.walkers.getParameters( walkerId )
        model = self.walkers.getModel( walkerId )
        mock = model.result( self.xdata, param )
        self.plotter.plotResult( inp, mock, iter )

    def report( self ):

#        print( "Rate        %f" % self.rate )
        print( "Engines              success     reject     failed      calls" )

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



