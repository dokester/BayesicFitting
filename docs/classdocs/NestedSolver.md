---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/NestedSolver.py target=_blank>Source</a></span></div>

<a name="NestedSolver"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class NestedSolver(</strong> <a href="./NestedSampler.html">NestedSampler</a> )
</th></tr></thead></table>
<p>

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

* xdata  :  array_like<br>
    array of independent input values<br>
* model  :  Model<br>
    the model function to be fitted<br>
* ydata  :  array_like<br>
    array of dependent (to be fitted) data<br>
* weights  :  array_like (None)<br>
    weights pertaining to ydata<br>
* distribution  :  ErrorDistribution<br>
    to calculate the loglikelihood<br>
* ensemble  :  int (100)<br>
    number of walkers<br>
* discard  :  int (1)<br>
    number of walkers to be replaced each generation<br>
* rng  :  RandomState<br>
    random number generator<br>
* seed  :  int (80409)<br>
    seed of rng<br>
* rate  :  float (1.0)<br>
    speed of exploration<br>
* maxsize  :  None or int<br>
    maximum size of the resulting sample list (None : no limit)<br>
* end  :  float (2.0)<br>
    stopping criterion<br>
* verbose  :  int<br>
    level of blabbering<br>

* walkers  :  SampleList<br>
    ensemble of Samples that explore the likelihood space<br>
* samples  :  SampleList<br>
    Samples resulting from the exploration<br>
* engines  :  list of Engine<br>
    Engine that move the walkers around within the given constraint: logL > lowLogL<br>
* initialEngine  :  Engine<br>
    Engine that distributes the walkers over the available space<br>
* restart  :  StopStart (TBW)<br>
    write intermediate results to (optionally) start from.<br>


Author       Do Kester.



<a name="NestedSolver"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>NestedSolver(</strong> problem, distribution=None, keep=None,
 ensemble=100, discard=1, seed=80409, rate=1.0, engines=None,
 maxsize=None, threads=False, verbose=1 ) 
</th></tr></thead></table>
<p>

Create a new class, providing inputs and model.

<b>Parameters</b>

* problem  :  OrderProblem<br>
    Problem with integer parameters<br>
* keep  :  None or dict of {int:float}<br>
    None : none of the model parameters are kept fixed.<br>
    Dictionary of indices (int) to be kept at a fixed value (float).<br>
    Hyperparameters follow model parameters.<br>
    The values will override those at initialization.<br>
    They are used in this instantiation, unless overwritten at the call to sample()<br>
* distribution  :  None or String or ErrorDistribution<br>
    None   : DistanceCostFunction is chosen.<br>

    "distance" : `DistanceCostFunction`      no hyperpar<br>

    errdis : A class inheriting from ErrorDistribution<br>
             which implements logLikelihood<br>

    When the hyperpar(s) are not to be kept fixed, they need `Prior` and maybe limits.<br>
* ensemble  :  int (100)<br>
    number of walkers<br>
* discard  :  int (1)<br>
    number of walkers to be replaced each generation<br>
* seed  :  int (80409)<br>
    seed of rng<br>
* rate  :  float (1.0)<br>
    speed of exploration<br>
* engines  :  None or (list of) string or (list of) Engine<br>
    to randomly move the walkers around, within the likelihood bound.<br>

    "move"    : insert a snippet of parameters at another location<br>
    "reverse" : reverse the order of a snippet of parameters<br>
    "shuffle" : shuffle part of the parameter list<br>
    "switch"  : switch two elements<br>
    "loop"    : find two paths that cross, then uncross them<br>
    "near"    : find the nearest location and go there first. <br>

    None    : take default [all of above].<br>

    engine  : a class inheriting from Engine. At least implementing<br>
              execute( walker, lowLhood )<br>
* maxsize  :  None or int<br>
    maximum size of the resulting sample list (None : no limit)<br>
* threads  :  bool (False)<br>
    Use Threads to distribute the diffusion of discarded samples over the available cores.<br>
* verbose  :  int (1)<br>
    0 : silent<br>
    1 : basic information<br>
    2 : more about every 100th iteration<br>
    3 : more about every iteration<br>


<a name="solve"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>solve(</strong> keep=None, plot=False )
</th></tr></thead></table>
<p>

Solve an order problem.

Return the last sample, representing the best solution.

The more sammples (with solutions) can be found in the sample list.

<b>Parameters</b>

* keep  :  None or dict of {int:float}<br>
    Dictionary of indices (int) to be kept at a fixed value (float)<br>
    Hyperparameters follow model parameters<br>
    The values will override those at initialization.<br>
    They are only used in this call of fit.<br>
* plot  :  bool<br>
    Show a plot of the results<br>


<a name="setErrorDistribution"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>setErrorDistribution(</strong> name=None, scale=1.0, power=2.0 )
</th></tr></thead></table>
<p>

Set the error distribution for calculating the likelihood.

<b>Parameters</b>

* name  :  string<br>
    name of distribution<br>
* scale  :  float<br>
    fixed scale of distribution<br>
* power  :  float<br>
    fixed power of distribution<br>


<a name="setEngines"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>setEngines(</strong> engines=None, enginedict=None ) 
</th></tr></thead></table>
<p>

initialize the engines.

<b>Parameters</b>

* engines  :  list of string<br>
    list of engine names<br>
* enginedict  :  dictionary of { str : Engine }<br>
    connecting names to Engines<br>


<a name="initWalkers"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>initWalkers(</strong> ensemble, allpars, fitIndex, startdict=None )
</th></tr></thead></table>
<p>

Initialize the walkers at random values of parameters and scale

<b>Parameters</b>

* ensemble  :  int<br>
    length od the walkers list<br>
* allpars  :  array_like<br>
    array of parameters<br>
* fitIndex  :  array_like<br>
    indices of allpars to be fitted<br>
* startdict  :  dictionary of { str : Engine }<br>
    connecting a name to a StartEngine

<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
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
