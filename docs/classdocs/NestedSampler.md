---
---
<br><br>

<a name="NestedSampler"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class NestedSampler(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/NestedSampler.py target=_blank>Source</a></th></tr></thead></table>

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
<br>&nbsp;&nbsp;&nbsp;&nbsp; It walks all (super)parameters in a fixed direction for about 5 steps.
<br>&nbsp;&nbsp;&nbsp;&nbsp; When a step ends outside the high likelihood region the direction is
<br>&nbsp;&nbsp;&nbsp;&nbsp; mirrored on the lowLikelihood edge and continued.

2. ChordEngine.
<br>&nbsp;&nbsp;&nbsp;&nbsp; It draws a randomly oriented line through a point inside the region,
<br>&nbsp;&nbsp;&nbsp;&nbsp; until it reaches outside the restricted likelihood region on both sides.
<br>&nbsp;&nbsp;&nbsp;&nbsp; A random point is selected on the line until it is inside the likelihood region.
<br>&nbsp;&nbsp;&nbsp;&nbsp; This process runs several times

3. GibbsEngine.
<br>&nbsp;&nbsp;&nbsp;&nbsp; It moves each of the parameters by a random step, one at a time.
<br>&nbsp;&nbsp;&nbsp;&nbsp; It is a randomwalk.

4. StepEngine.
<br>&nbsp;&nbsp;&nbsp;&nbsp; It moves all parameters in a random direction. It is a randomwalk.

For dynamic models 2 extra engines are defined

6. BirthEngine.
<br>&nbsp;&nbsp;&nbsp;&nbsp; It tries to increase the number of parameters.
<br>&nbsp;&nbsp;&nbsp;&nbsp; It can only be switched on for Dynamic Models.

7. DeathEngine.
<br>&nbsp;&nbsp;&nbsp;&nbsp; It tries to decrease the number of parameters.
<br>&nbsp;&nbsp;&nbsp;&nbsp; It can only be switched on for Dynamic Models.

For modifiable models 1 engine is defined.

8. StructureEngine.
<br>&nbsp;&nbsp;&nbsp;&nbsp; It alters the internal structure of the model.
<br>&nbsp;&nbsp;&nbsp;&nbsp; It can only be switched on for Modifiable Models.

<b>Attributes</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of independent input values
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model function to be fitted
* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of dependent (to be fitted) data
* weights  :  array_like (None)
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights pertaining to ydata
* problem  :  Problem (ClassicProblem)
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved (container of model, xdata, ydata and weights)
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
* minimumIterations  :  int (100)
<br>&nbsp;&nbsp;&nbsp;&nbsp; minimum number of iterations (adapt when starting problems occur)
* end  :  float (2.0)
<br>&nbsp;&nbsp;&nbsp;&nbsp; stopping criterion
* tolerance  :  float (-12)
<br>&nbsp;&nbsp;&nbsp;&nbsp; stopping criterion: stop if log( dZ / Z ) < tolerance
* verbose  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; level of blabbering
* walkers  :  WalkerList
<br>&nbsp;&nbsp;&nbsp;&nbsp; ensemble of walkers that explore the likelihood space
* samples  :  SampleList
<br>&nbsp;&nbsp;&nbsp;&nbsp; Samples resulting from the exploration
* engines  :  list of Engine
<br>&nbsp;&nbsp;&nbsp;&nbsp; Engine that move the walkers around within the given constraint: logL > lowLogL
* initialEngine  :  Engine
<br>&nbsp;&nbsp;&nbsp;&nbsp; Engine that distributes the walkers over the available space
* restart  :  StopStart (TBW)
<br>&nbsp;&nbsp;&nbsp;&nbsp; write intermediate results to (optionally) start from.

Author       Do Kester.


<a name="NestedSampler"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>NestedSampler(</strong> xdata=None, model=None, ydata=None, weights=None,
 accuracy=None, problem=None, distribution=None, limits=None,
 keep=None, ensemble=ENSEMBLE, discard=1, seed=80409, rate=RATE,
 bestBoost=False,
 engines=None, maxsize=None, threads=False, verbose=1 ) 
</th></tr></thead></table>

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
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; None        same as "classic"
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "classic"   ClassicProblem
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "errors"    ErrorsInXandYProblem
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "multiple"  MultipleOutputProblem
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Problem     Externally defined Problem. When Problem has been provided,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; xdata, model, weights and ydata are not used.
* keep  :  None or dict of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; None of the model parameters are kept fixed.
<br>&nbsp;&nbsp;&nbsp;&nbsp; Dictionary of indices (int) to be kept at a fixed value (float).
<br>&nbsp;&nbsp;&nbsp;&nbsp; Hyperparameters follow model parameters.
<br>&nbsp;&nbsp;&nbsp;&nbsp; The values will override those at initialization.
<br>&nbsp;&nbsp;&nbsp;&nbsp; They are used in this instantiation, unless overwritten at the call to sample()
* distribution  :  None or String or ErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; Defines the ErrorDistribution to be used
<br>&nbsp;&nbsp;&nbsp;&nbsp; When the hyperpar(s) are not to be kept fixed, they need `Prior` and maybe limits.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; None            same as "gauss"
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "gauss"         GaussErrorDistribution with (fixed) scale equal to 1.0
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "laplace"       LaplaceErrorDistribution with 1 hyperpar scale
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "poisson"       PoissonErrorDistribution no hyperpar
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "cauchy"        CauchyErrorDstribution with 1 hyperpar scale
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "uniform"       UniformErrorDistribution with 1 hyperpar scale
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "bernoulli"     BernoulliErrorDistribution no hyperpar
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "exponential"   ExponentialErrorDistribution with 2 hyperpar (scale, power)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ErrorDistribution Externally defined ErrorDistribution
* limits  :  None or [low,high] or [[low],[high]]
<br>&nbsp;&nbsp;&nbsp;&nbsp; None    no limits implying fixed hyperparameters of the distribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; low     low limit on hyperpars
<br>&nbsp;&nbsp;&nbsp;&nbsp; high    high limit on hyperpars
<br>&nbsp;&nbsp;&nbsp;&nbsp; When limits are set the hyperpars are not fixed.
* ensemble  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of walkers
* discard  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of walkers to be replaced each generation
* seed  : int
<br>&nbsp;&nbsp;&nbsp;&nbsp; seed of random number generator
* rate  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; speed of exploration
* bestBoost  :  bool or Fitter
<br>&nbsp;&nbsp;&nbsp;&nbsp; False   no updates of best logLikelihood
<br>&nbsp;&nbsp;&nbsp;&nbsp; True    boost the fit using LevenbergMarquardtFitter
<br>&nbsp;&nbsp;&nbsp;&nbsp; fitter  boost the fit using this fitter.
* engines  :  None or (list of) string or (list of) Engine
<br>&nbsp;&nbsp;&nbsp;&nbsp; to randomly move the walkers around, within the likelihood bound.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; None        use a Problem defined selection of engines
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "galilean"  GalileanEngine  move forward and mirror on edges
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "chord"     ChordEngine     select random point on random line
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "gibbs"     GibbsEngine     move one parameter at a time
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "step"      StepEngine      move all parameters in arbitrary direction
<br>&nbsp;&nbsp;&nbsp;&nbsp; For Dynamic models only
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "birth"     BirthEngine     increase the parameter list of a walker by one
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "death"     DeathEngine     decrease the parameter list of a walker by one
<br>&nbsp;&nbsp;&nbsp;&nbsp; For Modifiable models only
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "struct"    StructureEngine change the (internal) structure.
<br>&nbsp;&nbsp;&nbsp;&nbsp; Engine      an externally defined (list of) Engine
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
</th></tr></thead></table>
Sample the posterior and return the 10log( evidence )

A additional result of this method is a SampleList which contains
samples taken from the posterior distribution.

<b>Parameters</b>

* keep  :  None or dict of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; Dictionary of indices (int) to be kept at a fixed value (float)
<br>&nbsp;&nbsp;&nbsp;&nbsp; Hyperparameters follow model parameters
<br>&nbsp;&nbsp;&nbsp;&nbsp; The values will override those at initialization.
<br>&nbsp;&nbsp;&nbsp;&nbsp; They are only used in this call of fit.
* plot  :  bool or str
<br>&nbsp;&nbsp;&nbsp;&nbsp; bool    show a plot of the final results
<br>&nbsp;&nbsp;&nbsp;&nbsp; "iter" 	show iterations
<br>&nbsp;&nbsp;&nbsp;&nbsp; "all"  	show iterations and final result
<br>&nbsp;&nbsp;&nbsp;&nbsp; "last" 	show final result
<br>&nbsp;&nbsp;&nbsp;&nbsp; "test"      plot iterations but dont show (for testing)

<a name="initSample"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>initSample(</strong> ensemble=None, keep=None ) 
</th></tr></thead></table>

<a name="walkerLogL"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>walkerLogL(</strong> w ) 
</th></tr></thead></table>

<a name="makeFitlist"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makeFitlist(</strong> keep=None ) 
</th></tr></thead></table>
Make list of indices of (hyper)parameters that need fitting.

<b>Parameters</b>

* keep  :  None or dict of {int : float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices that need to be kept at the float value.

<a name="doIterPlot"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>doIterPlot(</strong> plot ) 
</th></tr></thead></table>
<b>Returns</b>

int 0   no plot
<br>&nbsp;&nbsp;&nbsp;&nbsp; 1   plot
<br>&nbsp;&nbsp;&nbsp;&nbsp; 2   plot but dont show (for testing)

<a name="doLastPlot"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>doLastPlot(</strong> plot ) 
</th></tr></thead></table>
<b>Return</b>

True when the last plot is requested (plot equals 'last' or 'all' or True)
False otherwise

<a name="initReport"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>initReport(</strong> keep=None ) 
</th></tr></thead></table>

<a name="iterReport"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>iterReport(</strong> kw, tail, plot=False ) 
</th></tr></thead></table>

<a name="printIterRep"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>printIterRep(</strong> kw, parfmt="%s", tail=0, max=None, indent=0, end="\n" ) 
</th></tr></thead></table>
if self.iteration % 1000 == 0 
<br>&nbsp;&nbsp;&nbsp;&nbsp; print( fmt( pl, max=None ) )
<br>&nbsp;&nbsp;&nbsp;&nbsp; npars = self.walkers[kw].problem.npars
<br>&nbsp;&nbsp;&nbsp;&nbsp; pmn, pmx = self.phantoms.getParamMinmax( self.lowLhood, npars )
<br>&nbsp;&nbsp;&nbsp;&nbsp; print( fmt( pmn, max=None ) )
<br>&nbsp;&nbsp;&nbsp;&nbsp; print( fmt( pmx, max=None ) )
<br>&nbsp;&nbsp;&nbsp;&nbsp; print( fmt( np ), fmt( self.phantoms.length( npars ) ), 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; fmt( self.logdZ, format="%10.3g" ) )
<br>&nbsp;&nbsp;&nbsp;&nbsp; for ky in self.phantoms.phantoms 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( fmt( ky ), fmt( len( self.phantoms.phantoms[ky] ) ) )

<a name="lastReport"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>lastReport(</strong> kw, plot=False ) 
</th></tr></thead></table>

<a name="plotLast"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotLast(</strong> ) 
</th></tr></thead></table>

<a name="getMaxIter"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getMaxIter(</strong> ) 
</th></tr></thead></table>
Return the maximum number of iteration.

<a name="nextIteration"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>nextIteration(</strong> ) 
</th></tr></thead></table>
Return True when a next iteration is needed. False to stop

<a name="optionalRestart"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>optionalRestart(</strong> )
</th></tr></thead></table>
Restart the session from a file. (not yet operational)

<a name="optionalSave"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>optionalSave(</strong> )
</th></tr></thead></table>
Save the session to a file. (not yet operational)

<a name="updateEvidence"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>updateEvidence(</strong> worst ) 
</th></tr></thead></table>
Updates the evidence (logZ) and the information (H)

The walkers need to be sorted to logL

<b>Parameters</b>

* worst  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; Number of walkers used in the update


<a name="copyWalker"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copyWalker(</strong> worst )
</th></tr></thead></table>
Kill worst walker( s ) in favour of one of the others

<b>Parameters</b>

* worst  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of Walkers to copy

<a name="copyWalkerFromPhantoms"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copyWalkerFromPhantoms(</strong> worst )
</th></tr></thead></table>
Kill worst walker( s ) in favour of one of the others

<b>Parameters</b>

* worst  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of Walkers to copy

<a name="copyWalkerFromDynamicPhantoms"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copyWalkerFromDynamicPhantoms(</strong> worst )
</th></tr></thead></table>
Kill worst walker( s ) in favour of one of the others

<b>Parameters</b>

* worst  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of Walkers to copy

<a name="updateWalkers"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>updateWalkers(</strong> explorer, worst ) 
</th></tr></thead></table>
Update the walkerlist in place.

<b>Parameters</b>

* explorer  :  Explorer
<br>&nbsp;&nbsp;&nbsp;&nbsp; Explorer object
* worst  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of walkers to update

<a name="setProblem"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setProblem(</strong> name, model=None, xdata=None, ydata=None, weights=None,
 accuracy=None ) 
</th></tr></thead></table>
Set the problem for this run.

If name is a Problem, then the keyword arguments (xdata,model,ydata,weights)
are overwritten provided they are not None

<b>Parameters</b>

* name  :  string or Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; name of problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; Problem Use this one
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model to be solved
* xdata  :  array_like or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; independent variable
* ydata  :  array_like or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; dependent variable
* weights  :  array_like or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights associated with ydata
* accuracy  :  float or array_like or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the data


<a name="setErrorDistribution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setErrorDistribution(</strong> name=None, limits=None, scale=1.0, power=2.0 )
</th></tr></thead></table>
Set the error distribution for calculating the likelihood.

<b>Parameters</b>

* name  :  None or string or ErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; None    distribution is Problem dependent.
<br>&nbsp;&nbsp;&nbsp;&nbsp; string  name of distribution; one of
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "gauss", "laplace", "poisson", "cauchy", "uniform",
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "exponential", "gauss2d", "model", "bernoulli"
<br>&nbsp;&nbsp;&nbsp;&nbsp; ErrorDistribution use this one
* limits  :  None or [low,high] or [[low],[high]]
<br>&nbsp;&nbsp;&nbsp;&nbsp; None    no limits implying fixed hyperparameters (scale,power,etc)
<br>&nbsp;&nbsp;&nbsp;&nbsp; low     low limit on hyperpars (needs to be >0)
<br>&nbsp;&nbsp;&nbsp;&nbsp; high    high limit on hyperpars
<br>&nbsp;&nbsp;&nbsp;&nbsp; when limits are set, the hyperpars are *not* fixed.
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

* engines  :  None or [Engine] or [string]
<br>&nbsp;&nbsp;&nbsp;&nbsp; None       engines is Problem dependent
<br>&nbsp;&nbsp;&nbsp;&nbsp; [Engines]  list of Engines to use
<br>&nbsp;&nbsp;&nbsp;&nbsp; [string]   list engine names
* enginedict  :  dictionary of { str : Engine }
<br>&nbsp;&nbsp;&nbsp;&nbsp; connecting names to the Engines

<a name="setInitialEngine"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setInitialEngine(</strong> ensemble, allpars, fitIndex, startdict=None )
</th></tr></thead></table>
Initialize the walkers at random values of parameters and scale

<b>Parameters</b>

* ensemble  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; length of the walkers list

* TBC  :  remove allpars and fitIndex

* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of (hyper)parameters
* fitIndex  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of allpars to be fitted

* startdict  :  dictionary of { str : Engine }
<br>&nbsp;&nbsp;&nbsp;&nbsp; connecting a name to a StartEngine

<a name="initWalkers"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>initWalkers(</strong> ensemble, allpars, fitIndex, startdict=None )
</th></tr></thead></table>
Initialize the walkers at random values of parameters and scale

<b>Parameters</b>

* ensemble  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; length of the walkers list
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of (hyper)parameters
* fitIndex  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of allpars to be fitted
* startdict  :  dictionary of { str : Engine }
<br>&nbsp;&nbsp;&nbsp;&nbsp; connecting a name to a StartEngine

<a name="plotResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotResult(</strong> walker, iter, plot=0 )
</th></tr></thead></table>
Plot the results for a walker.

<b>Parameters</b>

* walker  :  Walker
<br>&nbsp;&nbsp;&nbsp;&nbsp; the walker to plot
* iter  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; iteration number
* plot  :  int (one of (0,1,2)
<br>&nbsp;&nbsp;&nbsp;&nbsp; 0 immediate return, no action
<br>&nbsp;&nbsp;&nbsp;&nbsp; 1 plot
<br>&nbsp;&nbsp;&nbsp;&nbsp; 2 plot but dont show (for testing)

<a name="report"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>report(</strong> )
</th></tr></thead></table>
Final report on the run.

