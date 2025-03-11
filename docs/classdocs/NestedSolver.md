---
---
<br><br>

<a name="NestedSolver"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class NestedSolver(</strong> <a href="./NestedSampler.html">NestedSampler</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/NestedSolver.py target=_blank>Source</a></th></tr></thead></table>

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

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of independent input values
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model function to be fitted
* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of dependent (to be fitted) data
* weights  :  array_like (None)
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights pertaining to ydata
* distribution  :  ErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; to calculate the loglikelihood
* ensemble  :  int (100)
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of walkers
* discard  :  int (1)
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of walkers to be replaced each generation
* rng  :  RandomState
<br>&nbsp;&nbsp;&nbsp;&nbsp; random number generator
* seed  :  int (80409)
<br>&nbsp;&nbsp;&nbsp;&nbsp; seed of rng
* rate  :  float (1.0)
<br>&nbsp;&nbsp;&nbsp;&nbsp; speed of exploration
* maxsize  :  None or int
<br>&nbsp;&nbsp;&nbsp;&nbsp; maximum size of the resulting sample list (None : no limit)
* end  :  float (2.0)
<br>&nbsp;&nbsp;&nbsp;&nbsp; stopping criterion
* verbose  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; level of blabbering

* walkers  :  SampleList
<br>&nbsp;&nbsp;&nbsp;&nbsp; ensemble of Samples that explore the likelihood space
* samples  :  SampleList
<br>&nbsp;&nbsp;&nbsp;&nbsp; Samples resulting from the exploration
* engines  :  list of Engine
<br>&nbsp;&nbsp;&nbsp;&nbsp; Engine that move the walkers around within the given constraint: logL > lowLogL
* initialEngine  :  Engine
<br>&nbsp;&nbsp;&nbsp;&nbsp; Engine that distributes the walkers over the available space
* restart  :  StopStart (TBW)
<br>&nbsp;&nbsp;&nbsp;&nbsp; write intermediate results to (optionally) start from.


Author       Do Kester.



<a name="NestedSolver"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>NestedSolver(</strong> problem, distribution=None, keep=None,
 ensemble=100, discard=1, seed=80409, rate=1.0, engines=None,
 maxsize=None, threads=False, verbose=1 ) 
</th></tr></thead></table>

Create a new class, providing inputs and model.

<b>Parameters</b>

* problem  :  OrderProblem
<br>&nbsp;&nbsp;&nbsp;&nbsp; Problem with integer parameters
* keep  :  None or dict of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; None : none of the model parameters are kept fixed.
<br>&nbsp;&nbsp;&nbsp;&nbsp; Dictionary of indices (int) to be kept at a fixed value (float).
<br>&nbsp;&nbsp;&nbsp;&nbsp; Hyperparameters follow model parameters.
<br>&nbsp;&nbsp;&nbsp;&nbsp; The values will override those at initialization.
<br>&nbsp;&nbsp;&nbsp;&nbsp; They are used in this instantiation, unless overwritten at the call to sample()
* distribution  :  None or String or ErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; None   : DistanceCostFunction is chosen.

&nbsp;&nbsp;&nbsp;&nbsp; "distance" : `DistanceCostFunction`      no hyperpar

&nbsp;&nbsp;&nbsp;&nbsp; errdis : A class inheriting from ErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; which implements logLikelihood

&nbsp;&nbsp;&nbsp;&nbsp; When the hyperpar(s) are not to be kept fixed, they need `Prior` and maybe limits.
* ensemble  :  int (100)
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of walkers
* discard  :  int (1)
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of walkers to be replaced each generation
* seed  :  int (80409)
<br>&nbsp;&nbsp;&nbsp;&nbsp; seed of rng
* rate  :  float (1.0)
<br>&nbsp;&nbsp;&nbsp;&nbsp; speed of exploration
* engines  :  None or (list of) string or (list of) Engine
<br>&nbsp;&nbsp;&nbsp;&nbsp; to randomly move the walkers around, within the likelihood bound.

&nbsp;&nbsp;&nbsp;&nbsp; "move"    : insert a snippet of parameters at another location
<br>&nbsp;&nbsp;&nbsp;&nbsp; "reverse" : reverse the order of a snippet of parameters
<br>&nbsp;&nbsp;&nbsp;&nbsp; "shuffle" : shuffle part of the parameter list
<br>&nbsp;&nbsp;&nbsp;&nbsp; "switch"  : switch two elements
<br>&nbsp;&nbsp;&nbsp;&nbsp; "loop"    : find two paths that cross, then uncross them
<br>&nbsp;&nbsp;&nbsp;&nbsp; "near"    : find the nearest location and go there first. 

&nbsp;&nbsp;&nbsp;&nbsp; None    : take default [all of above].

&nbsp;&nbsp;&nbsp;&nbsp; engine  : a class inheriting from Engine. At least implementing
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; execute( walker, lowLhood )
* maxsize  :  None or int
<br>&nbsp;&nbsp;&nbsp;&nbsp; maximum size of the resulting sample list (None : no limit)
* threads  :  bool (False)
<br>&nbsp;&nbsp;&nbsp;&nbsp; Use Threads to distribute the diffusion of discarded samples over the available cores.
* verbose  :  int (1)
<br>&nbsp;&nbsp;&nbsp;&nbsp; 0 : silent
<br>&nbsp;&nbsp;&nbsp;&nbsp; 1 : basic information
<br>&nbsp;&nbsp;&nbsp;&nbsp; 2 : more about every 100th iteration
<br>&nbsp;&nbsp;&nbsp;&nbsp; 3 : more about every iteration


<a name="solve"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>solve(</strong> keep=None, plot=False )
</th></tr></thead></table>
Solve an order problem.

Return the last sample, representing the best solution.

The more sammples (with solutions) can be found in the sample list.

<b>Parameters</b>

* keep  :  None or dict of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; Dictionary of indices (int) to be kept at a fixed value (float)
<br>&nbsp;&nbsp;&nbsp;&nbsp; Hyperparameters follow model parameters
<br>&nbsp;&nbsp;&nbsp;&nbsp; The values will override those at initialization.
<br>&nbsp;&nbsp;&nbsp;&nbsp; They are only used in this call of fit.
* plot  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; Show a plot of the results


<a name="setErrorDistribution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setErrorDistribution(</strong> name=None, scale=1.0, power=2.0 )
</th></tr></thead></table>
Set the error distribution for calculating the likelihood.

<b>Parameters</b>

* name  :  string
<br>&nbsp;&nbsp;&nbsp;&nbsp; name of distribution
* scale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; fixed scale of distribution
* power  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; fixed power of distribution


<a name="setEngines"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setEngines(</strong> engines=None, enginedict=None ) 
</th></tr></thead></table>
initialize the engines.

<b>Parameters</b>

* engines  :  list of string
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of engine names
* enginedict  :  dictionary of { str : Engine }
<br>&nbsp;&nbsp;&nbsp;&nbsp; connecting names to Engines


<a name="initWalkers"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>initWalkers(</strong> ensemble, allpars, fitIndex, startdict=None )
</th></tr></thead></table>
Initialize the walkers at random values of parameters and scale

<b>Parameters</b>

* ensemble  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; length od the walkers list
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of parameters
* fitIndex  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of allpars to be fitted
* startdict  :  dictionary of { str : Engine }
<br>&nbsp;&nbsp;&nbsp;&nbsp; connecting a name to a StartEngine

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./NestedSampler.html">NestedSampler</a></th></tr></thead></table>


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
* [<strong>getMaxIter(</strong> ) ](./NestedSampler.md#getMaxIter)
* [<strong>nextIteration(</strong> ) ](./NestedSampler.md#nextIteration)
* [<strong>optionalRestart(</strong> )](./NestedSampler.md#optionalRestart)
* [<strong>optionalSave(</strong> )](./NestedSampler.md#optionalSave)
* [<strong>updateEvidence(</strong> worst ) ](./NestedSampler.md#updateEvidence)
* [<strong>copyWalker(</strong> worst )](./NestedSampler.md#copyWalker)
* [<strong>copyWalkerFromPhantoms(</strong> worst )](./NestedSampler.md#copyWalkerFromPhantoms)
* [<strong>copyWalkerFromDynamicPhantoms(</strong> worst )](./NestedSampler.md#copyWalkerFromDynamicPhantoms)
* [<strong>updateWalkers(</strong> explorer, worst ) ](./NestedSampler.md#updateWalkers)
* [<strong>setProblem(</strong> name, model=None, xdata=None, ydata=None, weights=None,](./NestedSampler.md#setProblem)
* [<strong>setInitialEngine(</strong> ensemble, allpars, fitIndex, startdict=None )](./NestedSampler.md#setInitialEngine)
* [<strong>plotResult(</strong> walker, iter, plot=0 )](./NestedSampler.md#plotResult)
* [<strong>report(</strong> )](./NestedSampler.md#report)
