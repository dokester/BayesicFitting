---
---
<a name="NestedSolver"></a>
<table><thead style="background-color:lightred; width:100%"><tr><th>
<strong>class NestedSolver(</strong> NestedSampler )
</th></tr></thead></table>


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


<b>Attributes</b>

* xdata  : ( array_like)<br>
    array of independent input values
* model  : ( Model)<br>
    the model function to be fitted
* ydata  : ( array_like)<br>
    array of dependent (to be fitted) data
* weights  : ( array_like (None))<br>
    weights pertaining to ydata
* distribution  : ( ErrorDistribution)<br>
    to calculate the loglikelihood
* ensemble  : ( int (100))<br>
    number of walkers
* discard  : ( int (1))<br>
    number of walkers to be replaced each generation
* rng  : ( RandomState)<br>
    random number generator
* seed  : ( int (80409))<br>
    seed of rng
* rate  : ( float (1.0))<br>
    speed of exploration
* maxsize  : ( None or int)<br>
    maximum size of the resulting sample list (None : no limit)
* end  : ( float (2.0))<br>
    stopping criterion
* verbose  : ( int)<br>
    level of blabbering

* walkers  : ( SampleList)<br>
    ensemble of Samples that explore the likelihood space
* samples  : ( SampleList)<br>
    Samples resulting from the exploration
* engines  : ( list of Engine)<br>
    Engine that move the walkers around within the given constraint: logL > lowLogL
* initialEngine  : ( Engine)<br>
    Engine that distributes the walkers over the available space
* restart  : ( StopStart (TBW))<br>
    write intermediate results to (optionally) start from.


Author       Do Kester.


<a name="NestedSolver"></a>
<table><thead style="background-color:limegreen; width:100%"><tr><th>
<strong>NestedSolver(</strong> problem, distribution=None, keep=None,
 ensemble=100, discard=1, seed=80409, rate=1.0, engines=None,
 maxsize=None, threads=False, verbose=1 ) 
</th></tr></thead></table>


Create a new class, providing inputs and model.

<b>Parameters</b>

* problem  : ( OrderProblem)<br>
    Problem with integer parameters
keep : None or dict of {int:float}
    None : none of the model parameters are kept fixed.
    Dictionary of indices (int) to be kept at a fixed value (float).
    Hyperparameters follow model parameters.
    The values will override those at initialization.
    They are used in this instantiation, unless overwritten at the call to sample()
* distribution  : ( None or String or ErrorDistribution)<br>
    None   : DistanceCostFunction is chosen.

    "distance" : `DistanceCostFunction`      no hyperpar

    errdis : A class inheriting from ErrorDistribution
             which implements logLikelihood

    When the hyperpar(s) are not to be kept fixed, they need `Prior` and maybe limits.
* ensemble  : ( int (100))<br>
    number of walkers
* discard  : ( int (1))<br>
    number of walkers to be replaced each generation
* seed  : ( int (80409))<br>
    seed of rng
* rate  : ( float (1.0))<br>
    speed of exploration
* engines  : ( None or (list of) string or (list of) Engine)<br>
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
* maxsize  : ( None or int)<br>
    maximum size of the resulting sample list (None : no limit)
* threads  : ( bool (False))<br>
    Use Threads to distribute the diffusion of discarded samples over the available cores.
* verbose  : ( int (1))<br>
    0 : silent
    1 : basic information
    2 : more about every 100th iteration
    3 : more about every iteration

<a name="solve"></a>
<table><thead style="background-color:limegreen; width:100%"><tr><th>
<strong>solve(</strong> keep=None, plot=False )
</th></tr></thead></table>


Solve an order problem.

Return the last sample, representing the best solution.

The more sammples (with solutions) can be found in the sample list.

<b>Parameters</b>

keep : None or dict of {int:float}
    Dictionary of indices (int) to be kept at a fixed value (float)
    Hyperparameters follow model parameters
    The values will override those at initialization.
    They are only used in this call of fit.
* plot  : ( bool)<br>
    Show a plot of the results

<a name="__str__"></a>
<table><thead style="background-color:limegreen; width:100%"><tr><th>
<strong>__str__(</strong> )
</th></tr></thead></table>

Return the name of this sampler. 

<a name="setErrorDistribution"></a>
<table><thead style="background-color:limegreen; width:100%"><tr><th>
<strong>setErrorDistribution(</strong> name=None, scale=1.0, power=2.0 )
</th></tr></thead></table>


Set the error distribution for calculating the likelihood.

<b>Parameters</b>

* name  : ( string)<br>
    name of distribution
* scale  : ( float)<br>
    fixed scale of distribution
* power  : ( float)<br>
    fixed power of distribution

<a name="setEngines"></a>
<table><thead style="background-color:limegreen; width:100%"><tr><th>
<strong>setEngines(</strong> engines=None, enginedict=None ) 
</th></tr></thead></table>


initialize the engines.

<b>Parameters</b>

* engines  : ( list of string)<br>
    list of engine names
enginedict : dictionary of { str : Engine }
    connecting names to Engines

<a name="initWalkers"></a>
<table><thead style="background-color:limegreen; width:100%"><tr><th>
<strong>initWalkers(</strong> ensemble, allpars, fitIndex, startdict=None )
</th></tr></thead></table>


Initialize the walkers at random values of parameters and scale

<b>Parameters</b>

* ensemble  : ( int)<br>
    length od the walkers list
* allpars  : ( array_like)<br>
    array of parameters
* fitIndex  : ( array_like)<br>
    indices of allpars to be fitted
startdict : dictionary of { str : Engine }
    connecting a name to a StartEngine

<thead style="background-color:dodgerblue; width:100%"><tr><th>
<strong>Methods inherited from NestedSampler</strong></th></tr></thead>



* [<strong>sample(</strong> keep=None, plot=False )](./NestedSampler.md#sample)
* [<strong>initSample(</strong> ensemble=None, keep=None ) ](./NestedSampler.md#initSample)
* [<strong>walkerLogL(</strong> w ) ](./NestedSampler.md#walkerLogL)
* [<strong>makeFitlist(</strong> keep=None ) ](./NestedSampler.md#makeFitlist)
* [<strong>doIterPlot(</strong> plot ) ](./NestedSampler.md#doIterPlot)
* [<strong>doLastPlot(</strong> plot ) ](./NestedSampler.md#doLastPlot)
* [<strong>initReport(</strong> keep=None ) ](./NestedSampler.md#initReport)
* [<strong>iterReport(</strong> kw, tail, plot=False ) ](./NestedSampler.md#iterReport)
* [<strong>printIterRep(</strong> kw, parfmt="%s", tail=0, max=None, indent=0, end="\n" ) ](./NestedSampler.md#printIterRep)
* [<strong>lastReport(</strong> kw, plot=False ) ](./NestedSampler.md#lastReport)
* [<strong>plotLast(</strong> ) ](./NestedSampler.md#plotLast)
* [<strong>XXXgetMaxIter(</strong> ) ](./NestedSampler.md#XXXgetMaxIter)
* [<strong>nextIteration(</strong> ) ](./NestedSampler.md#nextIteration)
* [<strong>__str__(</strong> )](./NestedSampler.md#__str__)
* [<strong>optionalRestart(</strong> )](./NestedSampler.md#optionalRestart)
* [<strong>optionalSave(</strong> )](./NestedSampler.md#optionalSave)
* [<strong>updateEvidence(</strong> worst ) ](./NestedSampler.md#updateEvidence)
* [<strong>unitDomain(</strong> ) ](./NestedSampler.md#unitDomain)
* [<strong>copyWalker(</strong> worst )](./NestedSampler.md#copyWalker)
* [<strong>copyWalkerFromPhantoms(</strong> worst )](./NestedSampler.md#copyWalkerFromPhantoms)
* [<strong>updateWalkers(</strong> explorer, worst ) ](./NestedSampler.md#updateWalkers)
* [<strong>__setattr__(</strong> name, value ) ](./NestedSampler.md#__setattr__)
* [<strong>__getattr__(</strong> name ) ](./NestedSampler.md#__getattr__)
* [<strong>setProblem(</strong> name, model=None, xdata=None, ydata=None, weights=None,](./NestedSampler.md#setProblem)
* [<strong>setErrorDistribution(</strong> name=None, limits=None, scale=1.0, power=2.0 )](./NestedSampler.md#setErrorDistribution)
* [<strong>setEngines(</strong> engines=None, enginedict=None ) ](./NestedSampler.md#setEngines)
* [<strong>setInitialEngine(</strong> ensemble, allpars, fitIndex, startdict=None )](./NestedSampler.md#setInitialEngine)
* [<strong>initWalkers(</strong> ensemble, allpars, fitIndex, startdict=None )](./NestedSampler.md#initWalkers)
* [<strong>plotResult(</strong> walker, iter, plot=0 )](./NestedSampler.md#plotResult)
* [<strong>report(</strong> )](./NestedSampler.md#report)
* [<strong>Methods inherited from object</strong></th></tr></thead>](./NestedSampler.md#report)

