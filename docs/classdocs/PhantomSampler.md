---
---
<br><br>

<a name="PhantomSampler"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class PhantomSampler(</strong> <a href="./NestedSampler.html">NestedSampler</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source// target=_blank>[source]</a></th></tr></thead></table>
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

<b>Attributes from NestedSampler</b>

xdata, model, ydata, weights, problem, distribution, ensemble, discard, rng, seed,
rate, maxsize, minimumIterations, end, verbose, walkers, samples, engines,
initialEngine

Author       Do Kester.


<a name="PhantomSampler"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>PhantomSampler(</strong> xdata=None, model=None, ydata=None, weights=None,
 accuracy=None, problem=None, distribution=None, limits=None,
 keep=None, ensemble=ENSEMBLE, seed=80409, rate=1.0, engines=None,
 maxsize=None, threads=False, verbose=1 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L59-L158 target=_blank>[source]</a></th></tr></thead></table>

Create a new class, providing inputs and model.

Either (model,xdata,ydata) needs to be provided or a completely filled
problem.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of independent input values
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model function to be fitted
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model needs priors for the parameters and (maybe) limits
* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of dependent (to be fitted) data
* weights  :  array_like (None)
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights pertaining to ydata
* accuracy  :  float or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; accuracy scale for the datapoints
<br>&nbsp;&nbsp;&nbsp;&nbsp; all the same or one for each data point
* problem  :  None or string or Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; Defines the kind of problem to be solved.

&nbsp;&nbsp;&nbsp;&nbsp; None        same as "classic"
<br>&nbsp;&nbsp;&nbsp;&nbsp; "classic" 	ClassicProblem
<br>&nbsp;&nbsp;&nbsp;&nbsp; "errors"	ErrorsInXandYProblem
<br>&nbsp;&nbsp;&nbsp;&nbsp; "multiple"	MultipleOutputProblem

&nbsp;&nbsp;&nbsp;&nbsp; Problem     Externally defined Problem. When Problem has been provided,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; xdata, model, weights and ydata are not used.
* keep  :  None or dict of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; None of the model parameters are kept fixed.
<br>&nbsp;&nbsp;&nbsp;&nbsp; Dictionary of indices (int) to be kept at a fixed value (float).
<br>&nbsp;&nbsp;&nbsp;&nbsp; Hyperparameters follow model parameters.
<br>&nbsp;&nbsp;&nbsp;&nbsp; The values will override those at initialization.
<br>&nbsp;&nbsp;&nbsp;&nbsp; They are used in this instantiation, unless overwritten at the call to sample()
* distribution  :  None or String or ErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; Defines the ErrorDistribution to be used
<br>&nbsp;&nbsp;&nbsp;&nbsp; When the hyperpar(s) are not to be kept fixed, they need `Prior` and maybe limits.

&nbsp;&nbsp;&nbsp;&nbsp; None            same as "gauss"
<br>&nbsp;&nbsp;&nbsp;&nbsp; "gauss"         GaussErrorDistribution with (fixed) scale equal to 1.0
<br>&nbsp;&nbsp;&nbsp;&nbsp; "laplace"       LaplaceErrorDistribution with 1 hyperpar scale
<br>&nbsp;&nbsp;&nbsp;&nbsp; "poisson"       PoissonErrorDistribution no hyperpar
<br>&nbsp;&nbsp;&nbsp;&nbsp; "cauchy"        CauchyErrorDstribution with 1 hyperpar scale
<br>&nbsp;&nbsp;&nbsp;&nbsp; "uniform"       UniformErrorDistribution with 1 hyperpar scale
<br>&nbsp;&nbsp;&nbsp;&nbsp; "exponential"   ExponentialErrorDistribution with 2 hyperpar (scale, power)
<br>&nbsp;&nbsp;&nbsp;&nbsp; "bernoulli"     BernoulliErrorDistribution no hyperpar

&nbsp;&nbsp;&nbsp;&nbsp; ErrorDistribution Externally defined ErrorDistribution
* limits  :  None or [low,high] or [[low],[high]]
<br>&nbsp;&nbsp;&nbsp;&nbsp; None    no limits implying fixed hyperparameters of the distribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; low     low limit on hyperpars
<br>&nbsp;&nbsp;&nbsp;&nbsp; high    high limit on hyperpars
<br>&nbsp;&nbsp;&nbsp;&nbsp; When limits are set the hyperpars are not fixed.
* ensemble  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of walkers (20)
* seed  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; seed of random number generator
* rate  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; speed of exploration
* engines  :  None or (list of) string or (list of) Engine
<br>&nbsp;&nbsp;&nbsp;&nbsp; to randomly move the walkers around, within the likelihood bound.

&nbsp;&nbsp;&nbsp;&nbsp; None        use a Problem defined selection of engines
<br>&nbsp;&nbsp;&nbsp;&nbsp; "galilean"  GalileanEngine	move forward and mirror on edges
<br>&nbsp;&nbsp;&nbsp;&nbsp; "chord"     ChordEngine   	select random point on random line
<br>&nbsp;&nbsp;&nbsp;&nbsp; "gibbs" 	GibbsEngine 	move one parameter at a time
<br>&nbsp;&nbsp;&nbsp;&nbsp; "step"  	StepEngine    	move all parameters in arbitrary direction

&nbsp;&nbsp;&nbsp;&nbsp; For Dynamic models only
<br>&nbsp;&nbsp;&nbsp;&nbsp; "birth" 	BirthEngine     increase the parameter list of a walker by one
<br>&nbsp;&nbsp;&nbsp;&nbsp; "death" 	DeathEngine     decrease the parameter list of a walker by one

&nbsp;&nbsp;&nbsp;&nbsp; For Modifiable models only
<br>&nbsp;&nbsp;&nbsp;&nbsp; "struct"    StructureEngine change the (internal) structure.

&nbsp;&nbsp;&nbsp;&nbsp; Engine      an externally defined (list of) Engine
* maxsize  :  None or int
<br>&nbsp;&nbsp;&nbsp;&nbsp; maximum size of the resulting sample list (None : no limit)
* threads  :  bool (False)
<br>&nbsp;&nbsp;&nbsp;&nbsp; Use Threads to distribute the diffusion of discarded samples over the available cores.
* verbose  :  int (1)
<br>&nbsp;&nbsp;&nbsp;&nbsp; 0   silent
<br>&nbsp;&nbsp;&nbsp;&nbsp; 1   basic information
<br>&nbsp;&nbsp;&nbsp;&nbsp; 2   more about every 100th iteration
<br>&nbsp;&nbsp;&nbsp;&nbsp; 3   more about every iteration
<br>&nbsp;&nbsp;&nbsp;&nbsp; >4  for debugging


<a name="sample"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>sample(</strong> keep=None, plot=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L160-L168 target=_blank>[source]</a></th></tr></thead></table>
see NestedSampler.sample()

<a name="updateEvidence"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>updateEvidence(</strong> worst ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L170-L269 target=_blank>[source]</a></th></tr></thead></table>
Updates the evidence (logZ) and the information (H)

The walkers need to be sorted to logL

<b>Parameters</b>

* worst  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; Number of walkers used in the update

Updates the evidence (logZ) and the information (H)

The walkers need to be sorted to logL

<b>Parameters</b>

* worst  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; Number of walkers used in the update


HERE ENDS THE DOCUMENTATION 



phansemble = self.livepointcount
kw = 0      ### DONT use enumerate here
* for lowph in self.phancol.nextLowPhantom( self.lowLhood )  : 
<br>&nbsp;&nbsp;&nbsp;&nbsp; logWeight = self.logWidth + lowph.logL + lowph.logPrior

&nbsp;&nbsp;&nbsp;&nbsp; # update evidence, logZ
<br>&nbsp;&nbsp;&nbsp;&nbsp; logZnew = numpy.logaddexp( self.logZ, logWeight )

&nbsp;&nbsp;&nbsp;&nbsp; # update Information, H
<br>&nbsp;&nbsp;&nbsp;&nbsp; self.info = ( math.exp( logWeight - logZnew ) * self.lowLhood +
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; math.exp( self.logZ - logZnew ) * ( self.info + self.logZ ) - logZnew )

&nbsp;&nbsp;&nbsp;&nbsp; if math.isnan( self.info ) 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.info = 0.0
<br>&nbsp;&nbsp;&nbsp;&nbsp; self.logZ = logZnew

&nbsp;&nbsp;&nbsp;&nbsp; # store posterior samples
<br>&nbsp;&nbsp;&nbsp;&nbsp; smpl = lowph.toSample( logWeight )
<br>&nbsp;&nbsp;&nbsp;&nbsp; self.samples.add( smpl )

&nbsp;&nbsp;&nbsp;&nbsp; self.sumWidth += math.exp( self.logWidth )

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.logWidth -= 1.0 / ( phansemble - kw )
<br>&nbsp;&nbsp;&nbsp;&nbsp; self.logWidth -= 1.0 / phansemble
<br>&nbsp;&nbsp;&nbsp;&nbsp; kw += 1

## check if there has something been updated
* if kw > 0  : 
<br>&nbsp;&nbsp;&nbsp;&nbsp; self.logdZ = logWeight - self.logZ

return

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./NestedSampler.html">NestedSampler</a></th></tr></thead></table>


* [<strong>initSample(</strong> ensemble=None, keep=None ) ](./NestedSampler.md#initSample)
* [<strong>walkerLogL(</strong> w ) ](./NestedSampler.md#walkerLogL)
* [<strong>makeFitlist(</strong> keep=None ) ](./NestedSampler.md#makeFitlist)
* [<strong>initReport(</strong> keep=None ) ](./NestedSampler.md#initReport)
* [<strong>iterReport(</strong> kw, tail ) ](./NestedSampler.md#iterReport)
* [<strong>printIterRep(</strong> kw, parfmt="%s", tail=0, max=None, indent=0, end="\n" ) ](./NestedSampler.md#printIterRep)
* [<strong>lastReport(</strong> kw, **kwargs ) ](./NestedSampler.md#lastReport)
* [<strong>setPlotters(</strong> plot ) ](./NestedSampler.md#setPlotters)
* [<strong>plotNot(</strong> kw, show=False ) ](./NestedSampler.md#plotNot)
* [<strong>plotIter(</strong> kw, show=False ) ](./NestedSampler.md#plotIter)
* [<strong>plotLast(</strong> kw, show=False, **kwargs ) ](./NestedSampler.md#plotLast)
* [<strong>nextIteration(</strong> ) ](./NestedSampler.md#nextIteration)
* [<strong>optionalRestart(</strong> )](./NestedSampler.md#optionalRestart)
* [<strong>optionalSave(</strong> )](./NestedSampler.md#optionalSave)
* [<strong>unitDomain(</strong> ) ](./NestedSampler.md#unitDomain)
* [<strong>copyWalker(</strong> worst )](./NestedSampler.md#copyWalker)
* [<strong>copyWalkerFromPhantoms(</strong> worst )](./NestedSampler.md#copyWalkerFromPhantoms)
* [<strong>updateWalkers(</strong> explorer, worst ) ](./NestedSampler.md#updateWalkers)
* [<strong>setProblem(</strong> name, model=None, xdata=None, ydata=None, weights=None,](./NestedSampler.md#setProblem)
* [<strong>setErrorDistribution(</strong> name=None, limits=None, scale=1.0, power=2.0 )](./NestedSampler.md#setErrorDistribution)
* [<strong>setEngines(</strong> engines=None, enginedict=None ) ](./NestedSampler.md#setEngines)
* [<strong>setInitialEngine(</strong> ensemble, allpars, fitIndex, startdict=None )](./NestedSampler.md#setInitialEngine)
* [<strong>initWalkers(</strong> ensemble, allpars, fitIndex, startdict=None )](./NestedSampler.md#initWalkers)
* [<strong>report(</strong> )](./NestedSampler.md#report)
