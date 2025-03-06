---
---
<br><br>

<a name="NestedSampler"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class NestedSampler(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/NestedSampler.py target=_blank>Source</a></th></tr></thead></table>
<p>

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
&nbsp;&nbsp;&nbsp;&nbsp; It walks all (super)parameters in a fixed direction for about 5 steps.<br>
&nbsp;&nbsp;&nbsp;&nbsp; When a step ends outside the high likelihood region the direction is<br>
&nbsp;&nbsp;&nbsp;&nbsp; mirrored on the lowLikelihood edge and continued.<br>

2. ChordEngine.
&nbsp;&nbsp;&nbsp;&nbsp; It draws a randomly oriented line through a point inside the region,<br>
&nbsp;&nbsp;&nbsp;&nbsp; until it reaches outside the restricted likelihood region on both sides.<br>
&nbsp;&nbsp;&nbsp;&nbsp; A random point is selected on the line until it is inside the likelihood region.<br>
&nbsp;&nbsp;&nbsp;&nbsp; This process runs several times<br>

3. GibbsEngine.
&nbsp;&nbsp;&nbsp;&nbsp; It moves each of the parameters by a random step, one at a time.<br>
&nbsp;&nbsp;&nbsp;&nbsp; It is a randomwalk.<br>

4. StepEngine.
&nbsp;&nbsp;&nbsp;&nbsp; It moves all parameters in a random direction. It is a randomwalk.<br>

For dynamic models 2 extra engines are defined

6. BirthEngine.
&nbsp;&nbsp;&nbsp;&nbsp; It tries to increase the number of parameters.<br>
&nbsp;&nbsp;&nbsp;&nbsp; It can only be switched on for Dynamic Models.<br>

7. DeathEngine.
&nbsp;&nbsp;&nbsp;&nbsp; It tries to decrease the number of parameters.<br>
&nbsp;&nbsp;&nbsp;&nbsp; It can only be switched on for Dynamic Models.<br>

For modifiable models 1 engine is defined.

8. StructureEngine.
&nbsp;&nbsp;&nbsp;&nbsp; It alters the internal structure of the model.<br>
&nbsp;&nbsp;&nbsp;&nbsp; It can only be switched on for Modifiable Models.<br>

<b>Attributes</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; array of independent input values<br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model function to be fitted<br>
* ydata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; array of dependent (to be fitted) data<br>
* weights  :  array_like (None)<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights pertaining to ydata<br>
* problem  :  Problem (ClassicProblem)<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be solved (container of model, xdata, ydata and weights)<br>
* distribution  :  ErrorDistribution<br>
&nbsp;&nbsp;&nbsp;&nbsp; to calculate the loglikelihood<br>
* ensemble  :  int (100)<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of walkers<br>
* discard  :  int (1)<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of walkers to be replaced each generation<br>
* rng  :  RandomState<br>
&nbsp;&nbsp;&nbsp;&nbsp; random number generator<br>
* seed  :  int (80409)<br>
&nbsp;&nbsp;&nbsp;&nbsp; seed of rng<br>
* rate  :  float (1.0)<br>
&nbsp;&nbsp;&nbsp;&nbsp; speed of exploration<br>
* maxsize  :  None or int<br>
&nbsp;&nbsp;&nbsp;&nbsp; maximum size of the resulting sample list (None : no limit)<br>
* minimumIterations  :  int (100)<br>
&nbsp;&nbsp;&nbsp;&nbsp; minimum number of iterations (adapt when starting problems occur)<br>
* end  :  float (2.0)<br>
&nbsp;&nbsp;&nbsp;&nbsp; stopping criterion<br>
* tolerance  :  float (-12)<br>
&nbsp;&nbsp;&nbsp;&nbsp; stopping criterion: stop if log( dZ / Z ) < tolerance<br>
* verbose  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; level of blabbering<br>
* walkers  :  WalkerList<br>
&nbsp;&nbsp;&nbsp;&nbsp; ensemble of walkers that explore the likelihood space<br>
* samples  :  SampleList<br>
&nbsp;&nbsp;&nbsp;&nbsp; Samples resulting from the exploration<br>
* engines  :  list of Engine<br>
&nbsp;&nbsp;&nbsp;&nbsp; Engine that move the walkers around within the given constraint: logL > lowLogL<br>
* initialEngine  :  Engine<br>
&nbsp;&nbsp;&nbsp;&nbsp; Engine that distributes the walkers over the available space<br>
* restart  :  StopStart (TBW)<br>
&nbsp;&nbsp;&nbsp;&nbsp; write intermediate results to (optionally) start from.<br>

Author       Do Kester.


<a name="NestedSampler"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>NestedSampler(</strong> xdata=None, model=None, ydata=None, weights=None,
 accuracy=None, problem=None, distribution=None, limits=None,
 keep=None, ensemble=ENSEMBLE, discard=1, seed=80409, rate=RATE,
 bestBoost=False,
 engines=None, maxsize=None, threads=False, verbose=1 ) 
</th></tr></thead></table>
<p>

Create a new class, providing inputs and model.

Either (model,xdata,ydata) needs to be provided or a completely filled
problem.

<b>Parameters</b>

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

&nbsp;&nbsp;&nbsp;&nbsp; None        same as "classic"<br>
&nbsp;&nbsp;&nbsp;&nbsp; "classic" 	ClassicProblem<br>
&nbsp;&nbsp;&nbsp;&nbsp; "errors"	ErrorsInXandYProblem<br>
&nbsp;&nbsp;&nbsp;&nbsp; "multiple"	MultipleOutputProblem<br>

&nbsp;&nbsp;&nbsp;&nbsp; Problem     Externally defined Problem. When Problem has been provided,<br>
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

&nbsp;&nbsp;&nbsp;&nbsp; None            same as "gauss"<br>
&nbsp;&nbsp;&nbsp;&nbsp; "gauss"         GaussErrorDistribution with (fixed) scale equal to 1.0<br>
&nbsp;&nbsp;&nbsp;&nbsp; "laplace"       LaplaceErrorDistribution with 1 hyperpar scale<br>
&nbsp;&nbsp;&nbsp;&nbsp; "poisson"       PoissonErrorDistribution no hyperpar<br>
&nbsp;&nbsp;&nbsp;&nbsp; "cauchy"        CauchyErrorDstribution with 1 hyperpar scale<br>
&nbsp;&nbsp;&nbsp;&nbsp; "uniform"       UniformErrorDistribution with 1 hyperpar scale<br>
&nbsp;&nbsp;&nbsp;&nbsp; "bernoulli"     BernoulliErrorDistribution no hyperpar<br>
&nbsp;&nbsp;&nbsp;&nbsp; "exponential"   ExponentialErrorDistribution with 2 hyperpar (scale, power)<br>

&nbsp;&nbsp;&nbsp;&nbsp; ErrorDistribution Externally defined ErrorDistribution<br>
* limits  :  None or [low,high] or [[low],[high]]<br>
&nbsp;&nbsp;&nbsp;&nbsp; None    no limits implying fixed hyperparameters of the distribution<br>
&nbsp;&nbsp;&nbsp;&nbsp; low     low limit on hyperpars<br>
&nbsp;&nbsp;&nbsp;&nbsp; high    high limit on hyperpars<br>
&nbsp;&nbsp;&nbsp;&nbsp; When limits are set the hyperpars are not fixed.<br>
* ensemble  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of walkers<br>
* discard  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of walkers to be replaced each generation<br>
* seed  : int<br>
&nbsp;&nbsp;&nbsp;&nbsp; seed of random number generator<br>
* rate  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; speed of exploration<br>
* bestBoost  :  bool or Fitter<br>
&nbsp;&nbsp;&nbsp;&nbsp; False   no updates of best logLikelihood<br>
&nbsp;&nbsp;&nbsp;&nbsp; True    boost the fit using LevenbergMarquardtFitter<br>
&nbsp;&nbsp;&nbsp;&nbsp; fitter  boost the fit using this fitter.<br>
* engines  :  None or (list of) string or (list of) Engine<br>
&nbsp;&nbsp;&nbsp;&nbsp; to randomly move the walkers around, within the likelihood bound.<br>

&nbsp;&nbsp;&nbsp;&nbsp; None        use a Problem defined selection of engines<br>
&nbsp;&nbsp;&nbsp;&nbsp; "galilean"  GalileanEngine	move forward and mirror on edges<br>
&nbsp;&nbsp;&nbsp;&nbsp; "chord"     ChordEngine   	select random point on random line<br>
&nbsp;&nbsp;&nbsp;&nbsp; "gibbs" 	GibbsEngine 	move one parameter at a time<br>
&nbsp;&nbsp;&nbsp;&nbsp; "step"  	StepEngine    	move all parameters in arbitrary direction<br>

&nbsp;&nbsp;&nbsp;&nbsp; For Dynamic models only:<br>
&nbsp;&nbsp;&nbsp;&nbsp; "birth" 	BirthEngine     increase the parameter list of a walker by one<br>
&nbsp;&nbsp;&nbsp;&nbsp; "death" 	DeathEngine     decrease the parameter list of a walker by one<br>

&nbsp;&nbsp;&nbsp;&nbsp; For Modifiable models only:<br>
&nbsp;&nbsp;&nbsp;&nbsp; "struct"    StructureEngine change the (internal) structure.<br>

&nbsp;&nbsp;&nbsp;&nbsp; Engine      an externally defined (list of) Engine<br>
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



The order in which the main attributes are created.

where       method                  attribute
__init__    setProblem              self.problem
__init__    setErrorDistribution    self.distribution
__init__    setEngines              self.phantoms
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.engines<br>
__init__                            self.samples
sample      initSample
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; initWalkers           self.walkers<br>

                setInitialEngine    self.initialEngine



<a name="sample"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>sample(</strong> keep=None, plot=False )
</th></tr></thead></table>
<p>******SAMPLE************************************************************
sample( self, keep=None, plot=False )


keep = self.initSample( keep=keep )

if ( self.problem.hasAccuracy and self.walkers[0].fitIndex[-1] < 0 and 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; not isinstance( self.distribution, GaussErrorDistribution ) ) :<br>
&nbsp;&nbsp;&nbsp;&nbsp; raise AttributeError( "%s cannot be combined with accuracies and variable scale" %<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.distribution ) <br>

&nbsp; if self.minimumIterations is None :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.minimumIterations = 10 * self.ensemble / self.discard<br>

tail = self.initReport( keep=keep )

explorer = Explorer( self, threads=self.threads )

## move all walkers around for initial exploration of the complete space.
if not isinstance( self.problem.model, LinearModel ) 
&nbsp;&nbsp;&nbsp;&nbsp; self.lowLhood = -sys.float_info.max<br>
&nbsp;&nbsp;&nbsp;&nbsp; # Explore all walker(s)<br>
&nbsp;&nbsp;&nbsp;&nbsp; explorer.explore( range( self.ensemble ), self.lowLhood, self.iteration )<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.iteration = 0                  # reset iteration number<br>


self.logZ = -sys.float_info.max
self.logdZ = 0
self.info = 0
self.logWidth = math.log( 1.0 - math.exp( -1.0 / self.ensemble ) )

&nbsp; TBD put self.logWidth in the saved file too<br>
&nbsp; if self.optionalRestart() :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.logWidth -= self.iteration * ( 1.0 * self.discard ) / self.ensemble<br>

self.histinsert = []
## iterate until done
&nbsp; while self.iteration < self.getMaxIter( ):<br>
while self.nextIteration() 

&nbsp;&nbsp;&nbsp;&nbsp; self.walkers.sort( key=self.walkerLogL )    # sort the walker list on logL<br>

&nbsp;&nbsp;&nbsp;&nbsp; worst = self.worst                      # the worst are low in the sorted ensemble<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.lowLhood = self.walkers[worst-1].logL<br>

&nbsp;&nbsp;&nbsp;&nbsp; self.updateEvidence( worst )            # Update Z and H and store posterior samples<br>

&nbsp;&nbsp;&nbsp;&nbsp; self.iterReport( worst - 1, tail, plot=plot ) # some output when needed<br>

&nbsp;&nbsp;&nbsp;&nbsp; self.samples.weed( self.maxsize )       # remove overflow in samplelist<br>

&nbsp;&nbsp;&nbsp;&nbsp; self.iteration += 1<br>

&nbsp;&nbsp;&nbsp;&nbsp; self.updateWalkers( explorer, worst )<br>

&nbsp;&nbsp;&nbsp;&nbsp; newL = self.walkers[worst-1].logL<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.histinsert += [self.walkers.firstIndex( newL )]<br>

&nbsp;&nbsp;&nbsp;&nbsp; self.optionalSave( )<br>


# End of Sampling: Update and store the remaining walkers
self.updateEvidence( self.ensemble )        # Update Evidence Z and Information H

# Calculate weighted average and stdevs for the parameters;
self.samples.LogZ = self.logZ
self.samples.info = self.info
self.samples.normalize( )

# put the info into the model
if self.problem.model and not self.problem.isDynamic() 
&nbsp;&nbsp;&nbsp;&nbsp; self.problem.model.parameters = self.samples.parameters<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.problem.model.stdevs = self.samples.stdevs<br>

self.lastReport( -1, plot=plot )

return self.evidence

<a name="initSample"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>initSample(</strong> ensemble=None, keep=None ) 
</th></tr></thead></table>
<p>
initSample( self, ensemble=None, keep=None ) 

if keep is None 
&nbsp;&nbsp;&nbsp;&nbsp; keep = self.keep<br>
fitIndex, allpars = self.makeFitlist( keep=keep )

if ensemble is None 
&nbsp;&nbsp;&nbsp;&nbsp; ensemble = self.ensemble<br>
self.initWalkers( ensemble, allpars, fitIndex )

for eng in self.engines 
&nbsp;&nbsp;&nbsp;&nbsp; eng.walkers = self.walkers<br>
&nbsp;&nbsp;&nbsp;&nbsp; eng.lastWalkerId = len( self.walkers )<br>
&nbsp;&nbsp;&nbsp;&nbsp; if self.bestBoost :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; eng.bestBoost( self.problem, myFitter=self.myFitter )<br>

self.distribution.ncalls = 0                      #  reset number of calls

return keep

in Use
&nbsp; sortLogL( self, walkers ) :<br>
&nbsp; return numpy.argsort( [w.logL for w in walkers] )<br>

<a name="walkerLogL"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>walkerLogL(</strong> w ) 
</th></tr></thead></table>
<p>
walkerLogL( self, w ) 
return w.logL

<a name="makeFitlist"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makeFitlist(</strong> keep=None ) 
</th></tr></thead></table>
<p>
makeFitlist( self, keep=None ) 


allpars = numpy.zeros( self.problem.npars + self.distribution.nphypar,
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; dtype=self.problem.partype )<br>

np = self.problem.npars
fitlist = [k for k in range( np )]
nh = -self.distribution.nphypar
for sp in self.distribution.hyperpar 
&nbsp;&nbsp;&nbsp;&nbsp; if not sp.isFixed and sp.isBound() :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; fitlist += [nh]                             # it is to be optimised<br>
&nbsp;&nbsp;&nbsp;&nbsp; elif self.problem.hasAccuracy and nh == -self.distribution.nphypar :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; allpars[nh] = 0                             # fix (model)scale at 0<br>
&nbsp;&nbsp;&nbsp;&nbsp; else :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; allpars[nh] = self.distribution.hypar[nh]   # fill in the fixed value<br>

&nbsp;&nbsp;&nbsp;&nbsp; nh += 1<br>

nh = self.distribution.nphypar
if keep is not None 
&nbsp;&nbsp;&nbsp;&nbsp; fitl = []<br>
&nbsp;&nbsp;&nbsp;&nbsp; kkeys = list( keep.keys() )<br>
&nbsp;&nbsp;&nbsp;&nbsp; for k in range( np + nh ) :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if k in kkeys :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; allpars[k] = keep[k]                    # save keep.value in allpars<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; elif fitlist[k] in kkeys :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; allpars[k] = keep[fitlist[k]]           # save keep.value in allpars<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; else :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; fitl += [fitlist[k]]                    # list of pars to be fitted<br>
&nbsp;&nbsp;&nbsp;&nbsp; fitlist = fitl<br>

return ( fitlist, allpars )


<a name="doIterPlot"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>doIterPlot(</strong> plot ) 
</th></tr></thead></table>
<p>
doIterPlot( self, plot ) 


if isinstance( plot, str ) 
&nbsp;&nbsp;&nbsp;&nbsp; if plot == 'iter' or plot == 'all' :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return 1<br>
&nbsp;&nbsp;&nbsp;&nbsp; elif plot == 'test' :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return 2<br>
&nbsp;&nbsp;&nbsp;&nbsp; else :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return 0<br>
else 
&nbsp;&nbsp;&nbsp;&nbsp; return 0<br>

<a name="doLastPlot"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>doLastPlot(</strong> plot ) 
</th></tr></thead></table>
<p>
doLastPlot( self, plot ) 


if isinstance( plot, str ) 
&nbsp;&nbsp;&nbsp;&nbsp; return plot == 'last' or plot == 'all'<br>
else 
&nbsp;&nbsp;&nbsp;&nbsp; return plot == True<br>


<a name="initReport"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>initReport(</strong> keep=None ) 
</th></tr></thead></table>
<p>
initReport( self, keep=None ) 

if self.verbose >= 1 
&nbsp;&nbsp;&nbsp;&nbsp; fitIndex = self.walkers[0].fitIndex<br>
&nbsp;&nbsp;&nbsp;&nbsp; print( "Fit", ( "all" if keep is None<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; else fitIndex ), "parameters of" )<br>
&nbsp;&nbsp;&nbsp;&nbsp; if self.problem.model :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( " ", self.problem.model._toString( "  " ) )<br>
&nbsp;&nbsp;&nbsp;&nbsp; else :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( " ", self.problem )<br>
&nbsp;&nbsp;&nbsp;&nbsp; print( "Using a", self.distribution, end="" )<br>
&nbsp;&nbsp;&nbsp;&nbsp; np = -1<br>
&nbsp;&nbsp;&nbsp;&nbsp; cstr = " with "<br>
&nbsp;&nbsp;&nbsp;&nbsp; for name,hyp in zip( self.distribution.PARNAMES, self.distribution.hyperpar ) :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( cstr, end="" )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if np in fitIndex :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( "unknown %s" % name, end="" )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; else :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( "%s = %7.2f " % (name, hyp.hypar), end="" )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; np -= 1<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; cstr = " and "<br>
&nbsp;&nbsp;&nbsp;&nbsp; print( "\nMoving the walkers with ", end="" )<br>
&nbsp;&nbsp;&nbsp;&nbsp; for eng in self.engines :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( " ", eng, end="" )<br>
&nbsp;&nbsp;&nbsp;&nbsp; print( "" )<br>
&nbsp;&nbsp;&nbsp;&nbsp; if self.threads :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( "Using threads." )<br>

tail = 0
if self.verbose > 1 
&nbsp;&nbsp;&nbsp;&nbsp; while fitIndex is not None and fitIndex[-tail-1] < 0 and len( fitIndex ) > tail + 1 : <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; tail += 1<br>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; tail = self.distribution.nphypar<br>
&nbsp;&nbsp;&nbsp;&nbsp; if tail == 0 :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( "Iteration     logZ        H       LowL     npar parameters" )<br>
&nbsp;&nbsp;&nbsp;&nbsp; else :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( "Iteration     logZ        H       LowL     npar parameters", end="" )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; for k in range( 1,  min( 5, len( fitIndex ) - tail ) ) :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( "        ", end="" )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; for k in range( tail ) :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( "   %s" %self.distribution.hyparname( k ), end="" )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( "" )<br>

return tail

<a name="iterReport"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>iterReport(</strong> kw, tail, plot=False ) 
</th></tr></thead></table>
<p>
iterReport( self, kw, tail, plot=False ) 

if self.verbose >= 3 or ( self.verbose >= 1 and
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.iteration % self.repiter == 0 ):<br>
&nbsp;&nbsp;&nbsp;&nbsp; if self.verbose == 1 :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if ( self.iteration / self.repiter ) % 50 == 49 :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; nwln = "\n"<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; else :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; nwln = ""<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( ">", end=nwln, flush=True )<br>
&nbsp;&nbsp;&nbsp;&nbsp; else :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.printIterRep( kw, tail=tail, max=4 )<br>

&nbsp;&nbsp;&nbsp;&nbsp; self.plotResult( self.walkers[kw], self.iteration, plot=self.doIterPlot( plot ) )<br>


<a name="printIterRep"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>printIterRep(</strong> kw, parfmt="%s", tail=0, max=None, indent=0, end="\n" ) 
</th></tr></thead></table>
<p>
printIterRep( self, kw, parfmt="%s", tail=0, max=None, indent=0, end="\n" ) 

pl = self.walkers[kw].allpars
fi = self.walkers[kw].fitIndex
if fi is not None : 
&nbsp;&nbsp;&nbsp;&nbsp; pl = pl[fi]<br>
np = len( pl )

print( "%8d %#10.3g %8.1f %#10.3g %6d "%( self.iteration, self.logZ,
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.info, self.lowLhood, np ), <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; parfmt % fmt( pl, max=max, tail=tail, indent=indent ), end=end )<br>




<a name="lastReport"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>lastReport(</strong> kw, plot=False ) 
</th></tr></thead></table>
<p>
lastReport( self, kw, plot=False ) 

if self.verbose > 0 
&nbsp;&nbsp;&nbsp;&nbsp; if self.verbose == 1 :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( "\nIteration     logZ        H       LowL     npar" )<br>

&nbsp;&nbsp;&nbsp;&nbsp; self.printIterRep( kw, max=None, indent=13, parfmt="\nParameters  %s" )<br>


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; pl = self.walkers[kw].allpars<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; fi = self.walkers[kw].fitIndex<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if fi is not None : <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; pl = pl[fi]<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; np = len( pl )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( "%8d %#10.3g %8.1f %#10.3g %6d "%( self.iteration, self.logZ,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.info, self.lowLhood, np ) )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( "Parameters  ", fmt( pl, max=None, indent=13 ) )<br>

if self.verbose >= 1 
&nbsp;&nbsp;&nbsp;&nbsp; self.report()<br>

if self.doLastPlot( plot ) 
&nbsp;&nbsp;&nbsp;&nbsp; self.plotLast()<br>

<a name="plotLast"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotLast(</strong> ) 
</th></tr></thead></table>
<p>
plotLast( self ) 
Plotter.plotSampleList( self.samples, self.problem.xdata, self.problem.ydata, 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; figsize=[12,8], residuals=True )<br>

<a name="getMaxIter"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getMaxIter(</strong> ) 
</th></tr></thead></table>
<p>
getMaxIter( self ) 


maxi = ( self.iteration if self.logdZ < self.tolerance else 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.end * self.ensemble * self.info / self.worst )<br>
maxi = max( self.minimumIterations, maxi )
return maxi if self.maxIterations is None else min( maxi, self.maxIterations )

<a name="nextIteration"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>nextIteration(</strong> ) 
</th></tr></thead></table>
<p>
nextIteration( self ) 


if self.iteration < self.minimumIterations 
&nbsp;&nbsp;&nbsp;&nbsp; return True<br>
if self.logdZ < self.tolerance 
&nbsp;&nbsp;&nbsp;&nbsp; return False<br>
if self.maxIterations is not None and self.iteration > self.maxIterations 
&nbsp;&nbsp;&nbsp;&nbsp; return False<br>
if self.iteration > self.end * self.ensemble * self.info / self.worst 
&nbsp;&nbsp;&nbsp;&nbsp; return False<br>
return True

<a name="optionalRestart"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>optionalRestart(</strong> )
</th></tr></thead></table>
<p>
optionalRestart( self )


if self.restart is not None and self.restart.wantRestore( )
&nbsp;&nbsp;&nbsp;&nbsp; self.walkers, self.samples = self.restart.restore( self.walkers, self.samples )<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.logZ = self.walkers.logZ<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.info = self.walkers.info<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.iteration = self.walkers.iteration<br>
&nbsp;&nbsp;&nbsp;&nbsp; return True<br>
return False

<a name="optionalSave"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>optionalSave(</strong> )
</th></tr></thead></table>
<p>
optionalSave( self )


if self.restart is not None and self.restart.wantSave( ) and self.iteration % 100 == 0
&nbsp;&nbsp;&nbsp;&nbsp; self.walkers.logZ = self.logZ<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.walkers.info = self.info<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.walkers.iteration = self.iteration<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.restart.save( self.walkers, self.samples )<br>


<a name="updateEvidence"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>updateEvidence(</strong> worst ) 
</th></tr></thead></table>
<p>
updateEvidence( self, worst ) 



for kw in range( worst ) 
&nbsp;&nbsp;&nbsp;&nbsp; logWeight = self.logWidth + self.walkers[kw].logL + self.walkers[kw].logPrior<br>

&nbsp;&nbsp;&nbsp;&nbsp; # update evidence, logZ<br>
&nbsp;&nbsp;&nbsp;&nbsp; logZnew = numpy.logaddexp( self.logZ, logWeight )<br>

&nbsp;&nbsp;&nbsp;&nbsp; # update Information, H<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.info = ( math.exp( logWeight - logZnew ) * self.lowLhood +<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; math.exp( self.logZ - logZnew ) * ( self.info + self.logZ ) - logZnew )<br>

&nbsp;&nbsp;&nbsp;&nbsp; if math.isnan( self.info ) :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.info = 0.0<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.logZ = logZnew<br>

&nbsp;&nbsp;&nbsp;&nbsp; # store posterior samples<br>
&nbsp;&nbsp;&nbsp;&nbsp; smpl = self.walkers[kw].toSample( logWeight )<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.samples.add( smpl )<br>

&nbsp;&nbsp;&nbsp;&nbsp; self.logWidth -= 1.0 / ( self.ensemble - kw )<br>

self.logdZ = logWeight - self.logZ

return

<a name="copyWalker"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copyWalker(</strong> worst )
</th></tr></thead></table>
<p>
copyWalker( self, worst )


for k in range( worst ) 
&nbsp;&nbsp;&nbsp;&nbsp; kcp = self.rng.randint( worst, self.ensemble )<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.walkers.copy( kcp, k, start=self.iteration )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; setatt( self.walkers[k], "parent", kcp )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; setatt( self.walkers[k], "start", self.iteration )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; setatt( self.walkers[k], "step", 0 )<br>

<a name="copyWalkerFromPhantoms"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copyWalkerFromPhantoms(</strong> worst )
</th></tr></thead></table>
<p>
copyWalkerFromPhantoms( self, worst )


plen = self.phantoms.length()

for k in range( worst ) 
&nbsp;&nbsp;&nbsp;&nbsp; while True :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; kcp = self.rng.randint( plen )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if self.phantoms.phantoms[kcp].logL > self.lowLhood :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; break<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.walkers.copy( kcp, k, wlist=self.phantoms.phantoms,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; start=self.iteration )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; setatt( self.walkers[k], "parent", kcp )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; setatt( self.walkers[k], "start", self.iteration )<br>

<a name="copyWalkerFromDynamicPhantoms"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copyWalkerFromDynamicPhantoms(</strong> worst )
</th></tr></thead></table>
<p>
copyWalkerFromDynamicPhantoms( self, worst )


plen = self.phantoms.length()
for k in range( worst ) 
&nbsp;&nbsp;&nbsp;&nbsp; while True :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; kcp = self.rng.randint( plen )<br>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; for pk in self.phantoms.phantoms.keys() :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; pklen = self.phantoms.length( np=pk )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if kcp < pklen :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; break<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; kcp -= pklen<br>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if self.phantoms.phantoms[pk][kcp].logL > self.lowLhood :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; break<br>

&nbsp;&nbsp;&nbsp;&nbsp; self.walkers.copy( kcp, k, wlist=self.phantoms.phantoms[pk],<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; start=self.iteration )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; setatt( self.walkers[k], "parent", kcp )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; setatt( self.walkers[k], "start", self.iteration )<br>



<a name="updateWalkers"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>updateWalkers(</strong> explorer, worst ) 
</th></tr></thead></table>
<p>
updateWalkers( self, explorer, worst ) 


self.copyWalker( worst )

# Explore the copied walker(s)
wlist = [k for k in range( worst )]
explorer.explore( wlist, self.lowLhood, self.iteration )



<a name="setProblem"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setProblem(</strong> name, model=None, xdata=None, ydata=None, weights=None,
********INTERNALS***************************************************
 accuracy=None ) 
</th></tr></thead></table>
<p>setProblem( self, name, model=None, xdata=None, ydata=None, weights=None,
            accuracy=None ) 


problemdict = {
&nbsp;&nbsp;&nbsp;&nbsp; "classic"  : ClassicProblem,<br>
&nbsp;&nbsp;&nbsp;&nbsp; "errors"   : ErrorsInXandYProblem,<br>
&nbsp;&nbsp;&nbsp;&nbsp; "multiple" : MultipleOutputProblem,<br>
&nbsp;&nbsp;&nbsp;&nbsp; "evidence" : EvidenceProblem<br>
}
&nbsp;&nbsp;&nbsp;&nbsp; "salesman" : SalesmanProblem<br>
&nbsp;&nbsp;&nbsp;&nbsp; "order" : OrderProblem<br>

if isinstance( name, Problem ) 
&nbsp;&nbsp;&nbsp;&nbsp; self.problem = name<br>
&nbsp;&nbsp;&nbsp;&nbsp; if model is not None : self.problem.model = model<br>
&nbsp;&nbsp;&nbsp;&nbsp; if xdata is not None : self.problem.xdata = numpy.asarray( xdata )<br>
&nbsp;&nbsp;&nbsp;&nbsp; if ydata is not None : self.problem.ydata = numpy.asarray( ydata )<br>
&nbsp;&nbsp;&nbsp;&nbsp; if weights is not None : self.problem.weights = numpy.asarray( weights )<br>
&nbsp;&nbsp;&nbsp;&nbsp; if accuracy is not None : self.problem.setAccuracy( accuracy=accuracy )<br>
&nbsp;&nbsp;&nbsp;&nbsp; return<br>

if not isinstance( name, str ) 
&nbsp;&nbsp;&nbsp;&nbsp; raise ValueError( "Cannot interpret ", name, " as string or Problem" )<br>

name = str.lower( name )
try 
&nbsp;&nbsp;&nbsp;&nbsp; myProblem = problemdict[name]<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.problem = myProblem( model, xdata=xdata, ydata=ydata, weights=weights,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; accuracy=accuracy )<br>
except 
&nbsp;&nbsp;&nbsp;&nbsp; raise <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; raise ValueError( "Unknown problem name %s" % name )<br>




<a name="setErrorDistribution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setErrorDistribution(</strong> name=None, limits=None, scale=1.0, power=2.0 )
</th></tr></thead></table>
<p>********DISTRIBUTIONS***************************************************
setErrorDistribution( self, name=None, limits=None, scale=1.0, power=2.0 )


if name is None 
&nbsp;&nbsp;&nbsp;&nbsp; name = self.problem.myDistribution()<br>
elif isinstance( name, ErrorDistribution ) 
&nbsp;&nbsp;&nbsp;&nbsp; self.distribution = name<br>
&nbsp;&nbsp;&nbsp;&nbsp; return<br>

if not isinstance( name, str ) 
&nbsp;&nbsp;&nbsp;&nbsp; raise ValueError( "Cannot interpret ", name, " as string or ErrorDistribution" )<br>

name = str.lower( name )
&nbsp; print( name )<br>
if name == "gauss" 
&nbsp;&nbsp;&nbsp;&nbsp; self.distribution = GaussErrorDistribution( scale=scale, limits=limits )<br>
elif name == "laplace" 
&nbsp;&nbsp;&nbsp;&nbsp; self.distribution = LaplaceErrorDistribution( scale=scale, limits=limits )<br>
elif name == "poisson" 
&nbsp;&nbsp;&nbsp;&nbsp; self.distribution = PoissonErrorDistribution()<br>
elif name == "cauchy" 
&nbsp;&nbsp;&nbsp;&nbsp; self.distribution = CauchyErrorDistribution( scale=scale, limits=limits )<br>
elif name == "uniform" 
&nbsp;&nbsp;&nbsp;&nbsp; self.distribution = UniformErrorDistribution( scale=scale, limits=limits )<br>
elif name == "exponential" 
&nbsp;&nbsp;&nbsp;&nbsp; self.distribution = ExponentialErrorDistribution( scale=scale, power=power, limits=limits )<br>
elif name == "gauss2d" 
&nbsp;&nbsp;&nbsp;&nbsp; self.distribution = Gauss2dErrorDistribution( scale=scale, limits=limits )<br>
elif name == "model" 
&nbsp;&nbsp;&nbsp;&nbsp; self.distribution = ModelDistribution( scale=scale, limits=limits )<br>
elif name == "bernoulli" 
&nbsp;&nbsp;&nbsp;&nbsp; self.distribution = BernoulliErrorDistribution()<br>
else 
&nbsp;&nbsp;&nbsp;&nbsp; raise ValueError( "Unknown error distribution %s" % name )<br>

<a name="setEngines"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setEngines(</strong> engines=None, enginedict=None ) 
</th></tr></thead></table>
<p>
setEngines( self, engines=None, enginedict=None ) 


## the same for all engines. 
self.phantoms = PhantomCollection( dynamic=self.problem.isDynamic() )

if enginedict is None 
&nbsp;&nbsp;&nbsp;&nbsp; enginedict = {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "galilean" : GalileanEngine,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "chord" : ChordEngine,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "birth" : BirthEngine,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "death" : DeathEngine,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "struct": StructureEngine,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "gibbs" : GibbsEngine,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "random": RandomEngine,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "step"  : StepEngine }<br>

if engines is None 
&nbsp;&nbsp;&nbsp;&nbsp; engines = self.problem.myEngines()<br>

self.engines = []
if isinstance( engines, str ) 
&nbsp;&nbsp;&nbsp;&nbsp; engines = [engines]<br>
for name in engines 
&nbsp;&nbsp;&nbsp;&nbsp; if isinstance( name, Engine ) :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; engine = name<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; engine.walkers  = self.walkers<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; engine.errdis   = self.distribution<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; engine.phantoms = self.phantoms<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; engine.verbose  = self.verbose<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.engines   += [engine]<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; continue<br>

&nbsp;&nbsp;&nbsp;&nbsp; if not isinstance( name, str ) :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; raise ValueError( "Cannot interpret ", name, " as string or as Engine" )<br>

&nbsp;&nbsp;&nbsp;&nbsp; try :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Eng = enginedict[name]<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; seed = self.rng.randint( self.TWOP31 )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; engine = Eng( self.walkers, self.distribution, seed=seed, <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; phantoms=self.phantoms, verbose=self.verbose )<br>
&nbsp;&nbsp;&nbsp;&nbsp; except :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; raise ValueError( "Unknown Engine name : %10s" % name )<br>

&nbsp;&nbsp;&nbsp;&nbsp; self.engines += [engine]<br>



<a name="setInitialEngine"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setInitialEngine(</strong> ensemble, allpars, fitIndex, startdict=None )
</th></tr></thead></table>
<p>********INITIALIZATION***************************************************
setInitialEngine( self, ensemble, allpars, fitIndex, startdict=None )


if startdict is None 
&nbsp;&nbsp;&nbsp;&nbsp; startdict = { "start" : StartEngine }<br>

# Make the walkers list
&nbsp; walker = Walker( 0, self.problem, numpy.asarray( allpars ), fitIndex )<br>
&nbsp; self.walkers = WalkerList( walker=walker, ensemble=ensemble )<br>

if self.initialEngine is not None
&nbsp;&nbsp;&nbsp;&nbsp; # decorate with proper information<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.initialEngine.walkers = self.walkers<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.initialEngine.errdis = self.distribution<br>

else 
&nbsp;&nbsp;&nbsp;&nbsp; try :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; name = self.problem.myStartEngine()<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; StartEng = startdict[name]<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; seed = self.rng.randint( self.TWOP31 )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.initialEngine = StartEng( self.walkers, self.distribution,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; seed=seed )<br>
&nbsp;&nbsp;&nbsp;&nbsp; except :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; raise ValueError( "Unknown StartEngine name : %10s" % name )<br>

# Calculate logL for all walkers.
self.distribution.lowLhood = -math.inf

# pass the PhantomCollection to the initial engine
self.initialEngine.phantoms = self.phantoms

<a name="initWalkers"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>initWalkers(</strong> ensemble, allpars, fitIndex, startdict=None )
</th></tr></thead></table>
<p>
initWalkers( self, ensemble, allpars, fitIndex, startdict=None )


# Make the walkers list
walker = Walker( 0, self.problem, numpy.asarray( allpars ), fitIndex )
self.walkers = WalkerList( walker=walker, ensemble=ensemble )

self.setInitialEngine( ensemble, allpars, fitIndex, startdict=startdict )

for walker in self.walkers 
&nbsp;&nbsp;&nbsp;&nbsp; self.initialEngine.execute( walker.id, -math.inf )<br>

&nbsp; for w in self.walkers :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print( w.id, w.problem.model.npars, len( w.problem.model.parameters), len( w.allpars) )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; w.check( nhyp=self.distribution.nphypar )<br>


<a name="plotResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotResult(</strong> walker, iter, plot=0 )
</th></tr></thead></table>
<p>
plotResult( self, walker, iter, plot=0 )


if plot == 0 
&nbsp;&nbsp;&nbsp;&nbsp; return<br>

plt.figure( 'iterplot' )

if self.line is not None 
&nbsp;&nbsp;&nbsp;&nbsp; ax = plt.gca()<br>
&nbsp;&nbsp;&nbsp;&nbsp; if plot < 2 :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; plt.pause( 0.02 )       ## updates and displays the plot before pause<br>
&nbsp;&nbsp;&nbsp;&nbsp; ax.remove( )<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.text.set_text( "Iteration %d" % iter )<br>

if self.ymin is None 
&nbsp;&nbsp;&nbsp;&nbsp; self.ymin = numpy.min( self.problem.ydata )<br>
&nbsp;&nbsp;&nbsp;&nbsp; self.ymax = numpy.max( self.problem.ydata )<br>

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


<a name="report"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>report(</strong> )
</th></tr></thead></table>
<p>
report( self )


&nbsp; print( "Rate        %f" % self.rate )<br>
print( "Engines              success     reject     failed", end="" )
if self.bestBoost 
&nbsp;&nbsp;&nbsp;&nbsp; print( "       best", end="" )<br>
print( "      calls" )

for engine in self.engines 
&nbsp;&nbsp;&nbsp;&nbsp; print( "%-16.16s " % engine, end="" )<br>
&nbsp;&nbsp;&nbsp;&nbsp; engine.printReport( best=self.bestBoost )<br>
print( "Calls to LogL     %10d" % self.distribution.ncalls, end="" )
if self.distribution.nparts > 0 
&nbsp;&nbsp;&nbsp;&nbsp; print( "   to dLogL %10d" % self.distribution.nparts )<br>
else 
&nbsp;&nbsp;&nbsp;&nbsp; print( "" )<br>

print( "Samples  %10d" % len( self.samples ) )
print( "Evidence    %10.3f +- %10.3f" % (self.evidence, self.precision ) )



