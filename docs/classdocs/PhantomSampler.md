---
---
<br><br>

<a name="PhantomSampler"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class PhantomSampler(</strong> <a href="./NestedSampler.html">NestedSampler</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PhantomSampler.py target=_blank>Source</a></th></tr></thead></table>
<p>

PhantomSampler is a version of NestedSampler that removes step walkers from
the list. It uses a selection of the intermediate (phantom) positions which
are created inside the engines as valid walker points.
These phantoms are added to the walkerlist, until it fills the
ensemble to its initial value.

Each iteration a percentage of the walkers is used to update the evidence
and are subsequently transferred to the list of posterior samples.

In principle it speeds up the calculations by a factor step, of course it
pays in exploratory power and precision.


<b>Attributes</b><br>
* step  :  int (< 10)<br>
&nbsp;&nbsp;&nbsp;&nbsp; percentage of the walkers to replace<br>

<b>Attributes from NestedSampler</b><br>
xdata, model, ydata, weights, problem, distribution, ensemble, discard, rng, seed,
rate, maxsize, minimumIterations, end, verbose, walkers, samples, engines,
initialEngine

Author       Do Kester.


<a name="PhantomSampler"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>PhantomSampler(</strong> xdata=None, model=None, ydata=None, weights=None,
 accuracy=None, problem=None, distribution=None, limits=None,
 keep=None, ensemble=100, seed=80409, rate=1.0, engines=None,
 maxsize=None, threads=False, verbose=1, step=4 ) 
</th></tr></thead></table>
<p>

Create a new class, providing inputs and model.

Either (model,xdata,ydata) needs to be provided or a completely filled
problem.

<b>Parameters</b><br>
* step  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; percentage of walkers to use<br>

<b>Parameters from NestedSampler</b><br>
* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; array of independent input values<br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model function to be fitted<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model needs priors for the parameters and (maybe) limits<br>
* ydata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; array of dependent (to be fitted) data<br>
* weights  :  array_like (None)<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights pertaining to ydata<br>
* accuracy  :  float or array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; accuracy scale for the datapoints<br>
&nbsp;&nbsp;&nbsp;&nbsp; all the same or one for each data point<br>
* problem  :  None or string or Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; Defines the kind of problem to be solved.<br>

<br>&nbsp;&nbsp;&nbsp;&nbsp; None        same as "classic"<br>
&nbsp;&nbsp;&nbsp;&nbsp; "classic" 	ClassicProblem<br>
&nbsp;&nbsp;&nbsp;&nbsp; "errors"	ErrorsInXandYProblem<br>
&nbsp;&nbsp;&nbsp;&nbsp; "multiple"	MultipleOutputProblem<br>

<br>&nbsp;&nbsp;&nbsp;&nbsp; Problem     Externally defined Problem. When Problem has been provided,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; xdata, model, weights and ydata are not used.<br>
* keep  :  None or dict of {int:float}<br>
&nbsp;&nbsp;&nbsp;&nbsp; None of the model parameters are kept fixed.<br>
&nbsp;&nbsp;&nbsp;&nbsp; Dictionary of indices (int) to be kept at a fixed value (float).<br>
&nbsp;&nbsp;&nbsp;&nbsp; Hyperparameters follow model parameters.<br>
&nbsp;&nbsp;&nbsp;&nbsp; The values will override those at initialization.<br>
&nbsp;&nbsp;&nbsp;&nbsp; They are used in this instantiation, unless overwritten at the call to sample()<br>
* distribution  :  None or String or ErrorDistribution<br>
&nbsp;&nbsp;&nbsp;&nbsp; Defines the ErrorDistribution to be used<br>
&nbsp;&nbsp;&nbsp;&nbsp; When the hyperpar(s) are not to be kept fixed, they need `Prior` and maybe limits.<br>

<br>&nbsp;&nbsp;&nbsp;&nbsp; None            same as "gauss"<br>
&nbsp;&nbsp;&nbsp;&nbsp; "gauss"         GaussErrorDistribution with (fixed) scale equal to 1.0<br>
&nbsp;&nbsp;&nbsp;&nbsp; "laplace"       LaplaceErrorDistribution with 1 hyperpar scale<br>
&nbsp;&nbsp;&nbsp;&nbsp; "poisson"       PoissonErrorDistribution no hyperpar<br>
&nbsp;&nbsp;&nbsp;&nbsp; "cauchy"        CauchyErrorDstribution with 1 hyperpar scale<br>
&nbsp;&nbsp;&nbsp;&nbsp; "uniform"       UniformErrorDistribution with 1 hyperpar scale<br>
&nbsp;&nbsp;&nbsp;&nbsp; "exponential"   ExponentialErrorDistribution with 2 hyperpar (scale, power)<br>
&nbsp;&nbsp;&nbsp;&nbsp; "bernoulli"     BernoulliErrorDistribution no hyperpar<br>

<br>&nbsp;&nbsp;&nbsp;&nbsp; ErrorDistribution Externally defined ErrorDistribution<br>
* limits  :  None or [low,high] or [[low],[high]]<br>
&nbsp;&nbsp;&nbsp;&nbsp; None    no limits implying fixed hyperparameters of the distribution<br>
&nbsp;&nbsp;&nbsp;&nbsp; low     low limit on hyperpars<br>
&nbsp;&nbsp;&nbsp;&nbsp; high    high limit on hyperpars<br>
&nbsp;&nbsp;&nbsp;&nbsp; When limits are set the hyperpars are not fixed.<br>
* ensemble  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of walkers<br>
* seed  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; seed of random number generator<br>
* rate  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; speed of exploration<br>
* engines  :  None or (list of) string or (list of) Engine<br>
&nbsp;&nbsp;&nbsp;&nbsp; to randomly move the walkers around, within the likelihood bound.<br>

<br>&nbsp;&nbsp;&nbsp;&nbsp; None        use a Problem defined selection of engines<br>
&nbsp;&nbsp;&nbsp;&nbsp; "galilean"  GalileanEngine	move forward and mirror on edges<br>
&nbsp;&nbsp;&nbsp;&nbsp; "chord"     ChordEngine   	select random point on random line<br>
&nbsp;&nbsp;&nbsp;&nbsp; "gibbs" 	GibbsEngine 	move one parameter at a time<br>
&nbsp;&nbsp;&nbsp;&nbsp; "step"  	StepEngine    	move all parameters in arbitrary direction<br>

<br>&nbsp;&nbsp;&nbsp;&nbsp; For Dynamic models only:<br>
&nbsp;&nbsp;&nbsp;&nbsp; "birth" 	BirthEngine     increase the parameter list of a walker by one<br>
&nbsp;&nbsp;&nbsp;&nbsp; "death" 	DeathEngine     decrease the parameter list of a walker by one<br>

<br>&nbsp;&nbsp;&nbsp;&nbsp; For Modifiable models only:<br>
&nbsp;&nbsp;&nbsp;&nbsp; "struct"    StructureEngine change the (internal) structure.<br>

<br>&nbsp;&nbsp;&nbsp;&nbsp; Engine      an externally defined (list of) Engine<br>
* maxsize  :  None or int<br>
&nbsp;&nbsp;&nbsp;&nbsp; maximum size of the resulting sample list (None : no limit)<br>
* threads  :  bool (False)<br>
&nbsp;&nbsp;&nbsp;&nbsp; Use Threads to distribute the diffusion of discarded samples over the available cores.<br>
* verbose  :  int (1)<br>
&nbsp;&nbsp;&nbsp;&nbsp; 0   silent<br>
&nbsp;&nbsp;&nbsp;&nbsp; 1   basic information<br>
&nbsp;&nbsp;&nbsp;&nbsp; 2   more about every 100th iteration<br>
&nbsp;&nbsp;&nbsp;&nbsp; 3   more about every iteration<br>
&nbsp;&nbsp;&nbsp;&nbsp; >4  for debugging<br>


<a name="initSample"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>initSample(</strong> ensemble=None, keep=None ) 
</th></tr></thead></table>
<p>
<a name="updateWalkers"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>updateWalkers(</strong> explorer, worst ) 
</th></tr></thead></table>
<p>

Update the walkerlist while appending the new (phantom) walkers to the list

<b>Parameters</b><br>
* explorer  :  Explorer<br>
&nbsp;&nbsp;&nbsp;&nbsp; Explorer object<br>
* worst  :  int<br>
    number of walkers to update

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./NestedSampler.html">NestedSampler</a></th></tr></thead></table>


* [<strong>sample(</strong> keep=None, plot=False )](./NestedSampler.md#sample)
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
* [<strong>setProblem(</strong> name, model=None, xdata=None, ydata=None, weights=None,](./NestedSampler.md#setProblem)
* [<strong>setErrorDistribution(</strong> name=None, limits=None, scale=1.0, power=2.0 )](./NestedSampler.md#setErrorDistribution)
* [<strong>setEngines(</strong> engines=None, enginedict=None ) ](./NestedSampler.md#setEngines)
* [<strong>setInitialEngine(</strong> ensemble, allpars, fitIndex, startdict=None )](./NestedSampler.md#setInitialEngine)
* [<strong>initWalkers(</strong> ensemble, allpars, fitIndex, startdict=None )](./NestedSampler.md#initWalkers)
* [<strong>plotResult(</strong> walker, iter, plot=0 )](./NestedSampler.md#plotResult)
* [<strong>report(</strong> )](./NestedSampler.md#report)
