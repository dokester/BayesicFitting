import numpy as numpy
from astropy import units
import math
from . import Tools
from .Formatter import formatter as fmt
from . import Plotter
import sys
import warnings
import matplotlib.pyplot as plt

from .Problem import Problem
from .Walker import Walker
from .WalkerList import WalkerList
from .Sample import Sample
from .SampleList import SampleList
from .ErrorDistribution import ErrorDistribution

from .NestedSampler import NestedSampler

## for Order Problems import the classes
from .OrderProblem import OrderProblem
from .DistanceCostFunction import DistanceCostFunction
from .StartOrderEngine import StartOrderEngine
#from .StartNearEngine import StartNearEngine
from .MoveEngine import MoveEngine
from .LoopEngine import LoopEngine
from .ReverseEngine import ReverseEngine
from .ShuffleEngine import ShuffleEngine
from .SwitchEngine import SwitchEngine
from .NearEngine import NearEngine

__author__ = "Do Kester"
__year__ = 2022
__license__ = "GPL3"
__version__ = "3.0.0"
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
#  *    2019 - 2022 Do Kester

class NestedSolver( NestedSampler ):
    """
    NestedSolver is an extension of NestedSampler. It uses the
    likelihood-climbing technique to find a solution in an ordering
    problem. The negative value of the costfunction, commonly defined
    in ordering problems, is maximised. In this sense the costfunction
    is acting as the logLikelihood.

    For more information about this technique see NestedSampler.

    For the random walk of the parameters 4 so-called engines are written.
    By default only he first is switched on.

    MoveEngine    : insert a snippet of parameters at another location
    ReverseEngine : reverse the order of a snippet of parameters
    ShuffleEngine : shuffle part of the parameter list
    SwitchEngine  : switch two elements
    LoopEngine    : uncross a crossing loop
    NearEngine    : find the nearest location and go there first. 

    The last 2 engines are not random. They are mostly (?) taking steps 
    uphill. Mixing them with other engines maintain detailed balance in 
    an overall sense. 


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

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, problem, distribution=None, keep=None,
                ensemble=100, discard=1, seed=80409, rate=1.0, engines=None,
                maxsize=None, threads=False, verbose=1 ) :

        """
        Create a new class, providing inputs and model.

        Parameters
        ----------
        problem : OrderProblem
            Problem with integer parameters
        keep : None or dict of {int:float}
            None : none of the model parameters are kept fixed.
            Dictionary of indices (int) to be kept at a fixed value (float).
            Hyperparameters follow model parameters.
            The values will override those at initialization.
            They are used in this instantiation, unless overwritten at the call to sample()
        distribution : None or String or ErrorDistribution
            None   : DistanceCostFunction is chosen.

            "distance" : `DistanceCostFunction`      no hyperpar

            errdis : A class inheriting from ErrorDistribution
                     which implements logLikelihood

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

            "move"    : insert a snippet of parameters at another location
            "reverse" : reverse the order of a snippet of parameters
            "shuffle" : shuffle part of the parameter list
            "switch"  : switch two elements
            "loop"    : find two paths that cross, then uncross them
            "near"    : find the nearest location and go there first. 

            None    : take default [all of above].

            engine  : a class inheriting from Engine. At least implementing
                      execute( walker, lowLhood )
        maxsize : None or int
            maximum size of the resulting sample list (None : no limit)
        threads : bool (False)
            Use Threads to distribute the diffusion of discarded samples over the available cores.
        verbose : int (1)
            0 : silent
            1 : basic information
            2 : more about every 100th iteration
            3 : more about every iteration

        """
        if distribution is None :
            self.setErrorDistribution( "distance" )


        super().__init__( problem=problem, distribution=distribution, keep=keep,
                ensemble=ensemble, discard=discard, seed=seed, rate=rate,
                engines=engines, maxsize=maxsize, threads=threads, verbose=verbose )

        self.setEngines( engines )


    #  *******SAMPLE************************************************************
    def solve( self, keep=None, plot=False ):
        """
        Solve an order problem.

        Return the last sample, representing the best solution.

        The more sammples (with solutions) can be found in the sample list.

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
        self.sample( keep=keep, plot=plot )

        return self.samples[-1]


    #  *********DISTRIBUTIONS***************************************************
    def setErrorDistribution( self, name, scale=1.0, power=2.0 ):
        """
        Set the error distribution for calculating the likelihood.

        Parameters
        ----------
        name : string
            name of distribution
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
        if name == "distance" :
            self.distribution = DistanceCostFunction( )
        else :
            raise ValueError( "Unknown error distribution %s" % name )

    def setEngines( self, engines=None, enginedict=None ) :
        """
        initialize the engines.

        Parameters
        ----------
        engines : list of string
            list of engine names
        enginedict : dictionary of { str : Engine }
            connecting names to Engines

        """
        if enginedict is None :
            enginedict = {
               "move"    : MoveEngine,
               "reverse" : ReverseEngine,
               "loop"    : LoopEngine,
               "near"    : NearEngine,
               "shuffle" : ShuffleEngine,
               "switch"  : SwitchEngine }

        super().setEngines( engines=engines, enginedict=enginedict )

    #  *********INITIALIZATION***************************************************

    def initWalkers( self, ensemble, allpars, fitIndex, startdict=None ):
        """
        Initialize the walkers at random values of parameters and scale

        Parameters
        ----------
        ensemble : int
            length od the walkers list
        allpars : array_like
            array of parameters
        fitIndex : array_like
            indices of allpars to be fitted
        startdict : dictionary of { str : Engine }
            connecting a name to a StartEngine
        """
        if startdict is None :
            startdict = { "startorder" : StartOrderEngine }

#        print( "initW  ", allpars, fitIndex )

        allpars = numpy.arange( len( allpars ), dtype=int )

        super().initWalkers( ensemble, allpars, fitIndex, startdict=startdict )





