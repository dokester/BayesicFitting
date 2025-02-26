---
---
<br><br><br>

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
    It walks all (super)parameters in a fixed direction for about 5 steps.<br>
    When a step ends outside the high likelihood region the direction is<br>
    mirrored on the lowLikelihood edge and continued.<br>

2. ChordEngine.
    It draws a randomly oriented line through a point inside the region,<br>
    until it reaches outside the restricted likelihood region on both sides.<br>
    A random point is selected on the line until it is inside the likelihood region.<br>
    This process runs several times<br>

3. GibbsEngine.
    It moves each of the parameters by a random step, one at a time.<br>
    It is a randomwalk.<br>

4. StepEngine.
    It moves all parameters in a random direction. It is a randomwalk.<br>

For dynamic models 2 extra engines are defined

6. BirthEngine.
    It tries to increase the number of parameters.<br>
    It can only be switched on for Dynamic Models.<br>

7. DeathEngine.
    It tries to decrease the number of parameters.<br>
    It can only be switched on for Dynamic Models.<br>

For modifiable models 1 engine is defined.

8. StructureEngine.
    It alters the internal structure of the model.<br>
    It can only be switched on for Modifiable Models.<br>

<b>Attributes</b>

* xdata  :  array_like<br>
    array of independent input values<br>
* model  :  Model<br>
    the model function to be fitted<br>
* ydata  :  array_like<br>
    array of dependent (to be fitted) data<br>
* weights  :  array_like (None)<br>
    weights pertaining to ydata<br>
* problem  :  Problem (ClassicProblem)<br>
    to be solved (container of model, xdata, ydata and weights)<br>
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
* minimumIterations  :  int (100)<br>
    minimum number of iterations (adapt when starting problems occur)<br>
* end  :  float (2.0)<br>
    stopping criterion<br>
* tolerance  :  float (-12)<br>
    stopping criterion: stop if log( dZ / Z ) < tolerance<br>
* verbose  :  int<br>
    level of blabbering<br>
* walkers  :  WalkerList<br>
    ensemble of walkers that explore the likelihood space<br>
* samples  :  SampleList<br>
    Samples resulting from the exploration<br>
* engines  :  list of Engine<br>
    Engine that move the walkers around within the given constraint: logL > lowLogL<br>
* initialEngine  :  Engine<br>
    Engine that distributes the walkers over the available space<br>
* restart  :  StopStart (TBW)<br>
    write intermediate results to (optionally) start from.<br>

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
    array of independent input values<br>
* model  :  Model<br>
    the model function to be fitted<br>
    the model needs priors for the parameters and (maybe) limits<br>
* ydata  :  array_like<br>
    array of dependent (to be fitted) data<br>
* weights  :  array_like (None)<br>
    weights pertaining to ydata<br>
* accuracy  :  float or array_like<br>
    accuracy scale for the datapoints<br>
    all the same or one for each data point<br>
* problem  :  None or string or Problem<br>
    Defines the kind of problem to be solved.<br>

    None        same as "classic"<br>
    "classic" 	ClassicProblem<br>
    "errors"	ErrorsInXandYProblem<br>
    "multiple"	MultipleOutputProblem<br>

    Problem     Externally defined Problem. When Problem has been provided,<br>
                xdata, model, weights and ydata are not used.<br>
* keep  :  None or dict of {int:float}<br>
    None of the model parameters are kept fixed.<br>
    Dictionary of indices (int) to be kept at a fixed value (float).<br>
    Hyperparameters follow model parameters.<br>
    The values will override those at initialization.<br>
    They are used in this instantiation, unless overwritten at the call to sample()<br>
* distribution  :  None or String or ErrorDistribution<br>
    Defines the ErrorDistribution to be used<br>
    When the hyperpar(s) are not to be kept fixed, they need `Prior` and maybe limits.<br>

    None            same as "gauss"<br>
    "gauss"         GaussErrorDistribution with (fixed) scale equal to 1.0<br>
    "laplace"       LaplaceErrorDistribution with 1 hyperpar scale<br>
    "poisson"       PoissonErrorDistribution no hyperpar<br>
    "cauchy"        CauchyErrorDstribution with 1 hyperpar scale<br>
    "uniform"       UniformErrorDistribution with 1 hyperpar scale<br>
    "bernoulli"     BernoulliErrorDistribution no hyperpar<br>
    "exponential"   ExponentialErrorDistribution with 2 hyperpar (scale, power)<br>

    ErrorDistribution Externally defined ErrorDistribution<br>
* limits  :  None or [low,high] or [[low],[high]]<br>
    None    no limits implying fixed hyperparameters of the distribution<br>
    low     low limit on hyperpars<br>
    high    high limit on hyperpars<br>
    When limits are set the hyperpars are not fixed.<br>
* ensemble  :  int<br>
    number of walkers<br>
* discard  :  int<br>
    number of walkers to be replaced each generation<br>
* seed  : int<br>
    seed of random number generator<br>
* rate  :  float<br>
    speed of exploration<br>
* bestBoost  :  bool or Fitter<br>
    False   no updates of best logLikelihood<br>
    True    boost the fit using LevenbergMarquardtFitter<br>
    fitter  boost the fit using this fitter.<br>
* engines  :  None or (list of) string or (list of) Engine<br>
    to randomly move the walkers around, within the likelihood bound.<br>

    None        use a Problem defined selection of engines<br>
    "galilean"  GalileanEngine	move forward and mirror on edges<br>
    "chord"     ChordEngine   	select random point on random line<br>
    "gibbs" 	GibbsEngine 	move one parameter at a time<br>
    "step"  	StepEngine    	move all parameters in arbitrary direction<br>

    For Dynamic models only:<br>
    "birth" 	BirthEngine     increase the parameter list of a walker by one<br>
    "death" 	DeathEngine     decrease the parameter list of a walker by one<br>

    For Modifiable models only:<br>
    "struct"    StructureEngine change the (internal) structure.<br>

    Engine      an externally defined (list of) Engine<br>
* maxsize  :  None or int<br>
    maximum size of the resulting sample list (None : no limit)<br>
* threads  :  bool (False)<br>
    Use Threads to distribute the diffusion of discarded samples over the available cores.<br>
* verbose  :  int (1)<br>
    0   silent<br>
    1   basic information<br>
    2   more about every 100th iteration<br>
    3   more about every iteration<br>
    >4  for debugging<br>



The order in which the main attributes are created.

where       method                  attribute
__init__    setProblem              self.problem
__init__    setErrorDistribution    self.distribution
__init__    setEngines              self.phantoms
                                    self.engines<br>
__init__                            self.samples
sample      initSample
              initWalkers           self.walkers<br>

                setInitialEngine    self.initialEngine



<a name="sample"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>sample(</strong> keep=None, plot=False )
</th></tr></thead></table>
<p>******SAMPLE************************************************************
sample( self, keep=None, plot=False )


keep = self.initSample( keep=keep )

if ( self.problem.hasAccuracy and self.walkers[0].fitIndex[-1] < 0 and 
        not isinstance( self.distribution, GaussErrorDistribution ) ) :<br>
    raise AttributeError( "%s cannot be combined with accuracies and variable scale" %<br>
                            self.distribution ) <br>

 if self.minimumIterations is None :<br>
     self.minimumIterations = 10 * self.ensemble / self.discard<br>

tail = self.initReport( keep=keep )

explorer = Explorer( self, threads=self.threads )

## move all walkers around for initial exploration of the complete space.
if not isinstance( self.problem.model, LinearModel ) 
    self.lowLhood = -sys.float_info.max<br>
    # Explore all walker(s)<br>
    explorer.explore( range( self.ensemble ), self.lowLhood, self.iteration )<br>
    self.iteration = 0                  # reset iteration number<br>


self.logZ = -sys.float_info.max
self.logdZ = 0
self.info = 0
self.logWidth = math.log( 1.0 - math.exp( -1.0 / self.ensemble ) )

 TBD put self.logWidth in the saved file too<br>
 if self.optionalRestart() :<br>
     self.logWidth -= self.iteration * ( 1.0 * self.discard ) / self.ensemble<br>

self.histinsert = []
## iterate until done
 while self.iteration < self.getMaxIter( ):<br>
while self.nextIteration() 

    self.walkers.sort( key=self.walkerLogL )    # sort the walker list on logL<br>

    worst = self.worst                      # the worst are low in the sorted ensemble<br>
    self.lowLhood = self.walkers[worst-1].logL<br>

    self.updateEvidence( worst )            # Update Z and H and store posterior samples<br>

    self.iterReport( worst - 1, tail, plot=plot ) # some output when needed<br>

    self.samples.weed( self.maxsize )       # remove overflow in samplelist<br>

    self.iteration += 1<br>

    self.updateWalkers( explorer, worst )<br>

    newL = self.walkers[worst-1].logL<br>
    self.histinsert += [self.walkers.firstIndex( newL )]<br>

    self.optionalSave( )<br>


# End of Sampling: Update and store the remaining walkers
self.updateEvidence( self.ensemble )        # Update Evidence Z and Information H

# Calculate weighted average and stdevs for the parameters;
self.samples.LogZ = self.logZ
self.samples.info = self.info
self.samples.normalize( )

# put the info into the model
if self.problem.model and not self.problem.isDynamic() 
    self.problem.model.parameters = self.samples.parameters<br>
    self.problem.model.stdevs = self.samples.stdevs<br>

self.lastReport( -1, plot=plot )

return self.evidence

<a name="initSample"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>initSample(</strong> ensemble=None, keep=None ) 
</th></tr></thead></table>
<p>
initSample( self, ensemble=None, keep=None ) 

if keep is None 
    keep = self.keep<br>
fitIndex, allpars = self.makeFitlist( keep=keep )

if ensemble is None 
    ensemble = self.ensemble<br>
self.initWalkers( ensemble, allpars, fitIndex )

for eng in self.engines 
    eng.walkers = self.walkers<br>
    eng.lastWalkerId = len( self.walkers )<br>
    if self.bestBoost :<br>
        eng.bestBoost( self.problem, myFitter=self.myFitter )<br>

self.distribution.ncalls = 0                      #  reset number of calls

return keep

in Use
 sortLogL( self, walkers ) :<br>
 return numpy.argsort( [w.logL for w in walkers] )<br>

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
                       dtype=self.problem.partype )<br>

np = self.problem.npars
fitlist = [k for k in range( np )]
nh = -self.distribution.nphypar
for sp in self.distribution.hyperpar 
    if not sp.isFixed and sp.isBound() :<br>
        fitlist += [nh]                             # it is to be optimised<br>
    elif self.problem.hasAccuracy and nh == -self.distribution.nphypar :<br>
        allpars[nh] = 0                             # fix (model)scale at 0<br>
    else :<br>
        allpars[nh] = self.distribution.hypar[nh]   # fill in the fixed value<br>

    nh += 1<br>

nh = self.distribution.nphypar
if keep is not None 
    fitl = []<br>
    kkeys = list( keep.keys() )<br>
    for k in range( np + nh ) :<br>
        if k in kkeys :<br>
            allpars[k] = keep[k]                    # save keep.value in allpars<br>
        elif fitlist[k] in kkeys :<br>
            allpars[k] = keep[fitlist[k]]           # save keep.value in allpars<br>
        else :<br>
            fitl += [fitlist[k]]                    # list of pars to be fitted<br>
    fitlist = fitl<br>

return ( fitlist, allpars )


<a name="doIterPlot"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>doIterPlot(</strong> plot ) 
</th></tr></thead></table>
<p>
doIterPlot( self, plot ) 


if isinstance( plot, str ) 
    if plot == 'iter' or plot == 'all' :<br>
        return 1<br>
    elif plot == 'test' :<br>
        return 2<br>
    else :<br>
        return 0<br>
else 
    return 0<br>

<a name="doLastPlot"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>doLastPlot(</strong> plot ) 
</th></tr></thead></table>
<p>
doLastPlot( self, plot ) 


if isinstance( plot, str ) 
    return plot == 'last' or plot == 'all'<br>
else 
    return plot == True<br>


<a name="initReport"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>initReport(</strong> keep=None ) 
</th></tr></thead></table>
<p>
initReport( self, keep=None ) 

if self.verbose >= 1 
    fitIndex = self.walkers[0].fitIndex<br>
    print( "Fit", ( "all" if keep is None<br>
                          else fitIndex ), "parameters of" )<br>
    if self.problem.model :<br>
        print( " ", self.problem.model._toString( "  " ) )<br>
    else :<br>
        print( " ", self.problem )<br>
    print( "Using a", self.distribution, end="" )<br>
    np = -1<br>
    cstr = " with "<br>
    for name,hyp in zip( self.distribution.PARNAMES, self.distribution.hyperpar ) :<br>
        print( cstr, end="" )<br>
        if np in fitIndex :<br>
            print( "unknown %s" % name, end="" )<br>
        else :<br>
            print( "%s = %7.2f " % (name, hyp.hypar), end="" )<br>
        np -= 1<br>
        cstr = " and "<br>
    print( "\nMoving the walkers with ", end="" )<br>
    for eng in self.engines :<br>
        print( " ", eng, end="" )<br>
    print( "" )<br>
    if self.threads :<br>
        print( "Using threads." )<br>

tail = 0
if self.verbose > 1 
    while fitIndex is not None and fitIndex[-tail-1] < 0 and len( fitIndex ) > tail + 1 : <br>
        tail += 1<br>

     tail = self.distribution.nphypar<br>
    if tail == 0 :<br>
        print( "Iteration     logZ        H       LowL     npar parameters" )<br>
    else :<br>
        print( "Iteration     logZ        H       LowL     npar parameters", end="" )<br>
        for k in range( 1,  min( 5, len( fitIndex ) - tail ) ) :<br>
            print( "        ", end="" )<br>
        for k in range( tail ) :<br>
            print( "   %s" %self.distribution.hyparname( k ), end="" )<br>
        print( "" )<br>

return tail

<a name="iterReport"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>iterReport(</strong> kw, tail, plot=False ) 
</th></tr></thead></table>
<p>
iterReport( self, kw, tail, plot=False ) 

if self.verbose >= 3 or ( self.verbose >= 1 and
                          self.iteration % self.repiter == 0 ):<br>
    if self.verbose == 1 :<br>
        if ( self.iteration / self.repiter ) % 50 == 49 :<br>
            nwln = "\n"<br>
        else :<br>
            nwln = ""<br>
        print( ">", end=nwln, flush=True )<br>
    else :<br>
        self.printIterRep( kw, tail=tail, max=4 )<br>

    self.plotResult( self.walkers[kw], self.iteration, plot=self.doIterPlot( plot ) )<br>


<a name="printIterRep"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>printIterRep(</strong> kw, parfmt="%s", tail=0, max=None, indent=0, end="\n" ) 
</th></tr></thead></table>
<p>
printIterRep( self, kw, parfmt="%s", tail=0, max=None, indent=0, end="\n" ) 

pl = self.walkers[kw].allpars
fi = self.walkers[kw].fitIndex
if fi is not None : 
    pl = pl[fi]<br>
np = len( pl )

print( "%8d %#10.3g %8.1f %#10.3g %6d "%( self.iteration, self.logZ,
        self.info, self.lowLhood, np ), <br>
        parfmt % fmt( pl, max=max, tail=tail, indent=indent ), end=end )<br>




<a name="lastReport"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>lastReport(</strong> kw, plot=False ) 
</th></tr></thead></table>
<p>
lastReport( self, kw, plot=False ) 

if self.verbose > 0 
    if self.verbose == 1 :<br>
        print( "\nIteration     logZ        H       LowL     npar" )<br>

    self.printIterRep( kw, max=None, indent=13, parfmt="\nParameters  %s" )<br>


     pl = self.walkers[kw].allpars<br>
     fi = self.walkers[kw].fitIndex<br>
     if fi is not None : <br>
         pl = pl[fi]<br>
     np = len( pl )<br>
     print( "%8d %#10.3g %8.1f %#10.3g %6d "%( self.iteration, self.logZ,<br>
             self.info, self.lowLhood, np ) )<br>
     print( "Parameters  ", fmt( pl, max=None, indent=13 ) )<br>

if self.verbose >= 1 
    self.report()<br>

if self.doLastPlot( plot ) 
    self.plotLast()<br>

<a name="plotLast"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotLast(</strong> ) 
</th></tr></thead></table>
<p>
plotLast( self ) 
Plotter.plotSampleList( self.samples, self.problem.xdata, self.problem.ydata, 
            figsize=[12,8], residuals=True )<br>

<a name="getMaxIter"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getMaxIter(</strong> ) 
</th></tr></thead></table>
<p>
getMaxIter( self ) 


maxi = ( self.iteration if self.logdZ < self.tolerance else 
         self.end * self.ensemble * self.info / self.worst )<br>
maxi = max( self.minimumIterations, maxi )
return maxi if self.maxIterations is None else min( maxi, self.maxIterations )

<a name="nextIteration"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>nextIteration(</strong> ) 
</th></tr></thead></table>
<p>
nextIteration( self ) 


if self.iteration < self.minimumIterations 
    return True<br>
if self.logdZ < self.tolerance 
    return False<br>
if self.maxIterations is not None and self.iteration > self.maxIterations 
    return False<br>
if self.iteration > self.end * self.ensemble * self.info / self.worst 
    return False<br>
return True

<a name="optionalRestart"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>optionalRestart(</strong> )
</th></tr></thead></table>
<p>
optionalRestart( self )


if self.restart is not None and self.restart.wantRestore( )
    self.walkers, self.samples = self.restart.restore( self.walkers, self.samples )<br>
    self.logZ = self.walkers.logZ<br>
    self.info = self.walkers.info<br>
    self.iteration = self.walkers.iteration<br>
    return True<br>
return False

<a name="optionalSave"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>optionalSave(</strong> )
</th></tr></thead></table>
<p>
optionalSave( self )


if self.restart is not None and self.restart.wantSave( ) and self.iteration % 100 == 0
    self.walkers.logZ = self.logZ<br>
    self.walkers.info = self.info<br>
    self.walkers.iteration = self.iteration<br>
    self.restart.save( self.walkers, self.samples )<br>


<a name="updateEvidence"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>updateEvidence(</strong> worst ) 
</th></tr></thead></table>
<p>
updateEvidence( self, worst ) 



for kw in range( worst ) 
    logWeight = self.logWidth + self.walkers[kw].logL + self.walkers[kw].logPrior<br>

    # update evidence, logZ<br>
    logZnew = numpy.logaddexp( self.logZ, logWeight )<br>

    # update Information, H<br>
    self.info = ( math.exp( logWeight - logZnew ) * self.lowLhood +<br>
            math.exp( self.logZ - logZnew ) * ( self.info + self.logZ ) - logZnew )<br>

    if math.isnan( self.info ) :<br>
        self.info = 0.0<br>
    self.logZ = logZnew<br>

    # store posterior samples<br>
    smpl = self.walkers[kw].toSample( logWeight )<br>
    self.samples.add( smpl )<br>

    self.logWidth -= 1.0 / ( self.ensemble - kw )<br>

self.logdZ = logWeight - self.logZ

return

<a name="copyWalker"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copyWalker(</strong> worst )
</th></tr></thead></table>
<p>
copyWalker( self, worst )


for k in range( worst ) 
    kcp = self.rng.randint( worst, self.ensemble )<br>
    self.walkers.copy( kcp, k, start=self.iteration )<br>
     setatt( self.walkers[k], "parent", kcp )<br>
     setatt( self.walkers[k], "start", self.iteration )<br>
     setatt( self.walkers[k], "step", 0 )<br>

<a name="copyWalkerFromPhantoms"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copyWalkerFromPhantoms(</strong> worst )
</th></tr></thead></table>
<p>
copyWalkerFromPhantoms( self, worst )


plen = self.phantoms.length()

for k in range( worst ) 
    while True :<br>
        kcp = self.rng.randint( plen )<br>
        if self.phantoms.phantoms[kcp].logL > self.lowLhood :<br>
            break<br>
    self.walkers.copy( kcp, k, wlist=self.phantoms.phantoms,<br>
                       start=self.iteration )<br>
     setatt( self.walkers[k], "parent", kcp )<br>
     setatt( self.walkers[k], "start", self.iteration )<br>

<a name="copyWalkerFromDynamicPhantoms"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copyWalkerFromDynamicPhantoms(</strong> worst )
</th></tr></thead></table>
<p>
copyWalkerFromDynamicPhantoms( self, worst )


plen = self.phantoms.length()
for k in range( worst ) 
    while True :<br>
        kcp = self.rng.randint( plen )<br>

        for pk in self.phantoms.phantoms.keys() :<br>
            pklen = self.phantoms.length( np=pk )<br>
            if kcp < pklen :<br>
                break<br>
            kcp -= pklen<br>

        if self.phantoms.phantoms[pk][kcp].logL > self.lowLhood :<br>
            break<br>

    self.walkers.copy( kcp, k, wlist=self.phantoms.phantoms[pk],<br>
                       start=self.iteration )<br>
     setatt( self.walkers[k], "parent", kcp )<br>
     setatt( self.walkers[k], "start", self.iteration )<br>



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
    "classic"  : ClassicProblem,<br>
    "errors"   : ErrorsInXandYProblem,<br>
    "multiple" : MultipleOutputProblem,<br>
    "evidence" : EvidenceProblem<br>
}
    "salesman" : SalesmanProblem<br>
    "order" : OrderProblem<br>

if isinstance( name, Problem ) 
    self.problem = name<br>
    if model is not None : self.problem.model = model<br>
    if xdata is not None : self.problem.xdata = numpy.asarray( xdata )<br>
    if ydata is not None : self.problem.ydata = numpy.asarray( ydata )<br>
    if weights is not None : self.problem.weights = numpy.asarray( weights )<br>
    if accuracy is not None : self.problem.setAccuracy( accuracy=accuracy )<br>
    return<br>

if not isinstance( name, str ) 
    raise ValueError( "Cannot interpret ", name, " as string or Problem" )<br>

name = str.lower( name )
try 
    myProblem = problemdict[name]<br>
    self.problem = myProblem( model, xdata=xdata, ydata=ydata, weights=weights,<br>
                              accuracy=accuracy )<br>
except 
    raise <br>
     raise ValueError( "Unknown problem name %s" % name )<br>




<a name="setErrorDistribution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setErrorDistribution(</strong> name=None, limits=None, scale=1.0, power=2.0 )
</th></tr></thead></table>
<p>********DISTRIBUTIONS***************************************************
setErrorDistribution( self, name=None, limits=None, scale=1.0, power=2.0 )


if name is None 
    name = self.problem.myDistribution()<br>
elif isinstance( name, ErrorDistribution ) 
    self.distribution = name<br>
    return<br>

if not isinstance( name, str ) 
    raise ValueError( "Cannot interpret ", name, " as string or ErrorDistribution" )<br>

name = str.lower( name )
 print( name )<br>
if name == "gauss" 
    self.distribution = GaussErrorDistribution( scale=scale, limits=limits )<br>
elif name == "laplace" 
    self.distribution = LaplaceErrorDistribution( scale=scale, limits=limits )<br>
elif name == "poisson" 
    self.distribution = PoissonErrorDistribution()<br>
elif name == "cauchy" 
    self.distribution = CauchyErrorDistribution( scale=scale, limits=limits )<br>
elif name == "uniform" 
    self.distribution = UniformErrorDistribution( scale=scale, limits=limits )<br>
elif name == "exponential" 
    self.distribution = ExponentialErrorDistribution( scale=scale, power=power, limits=limits )<br>
elif name == "gauss2d" 
    self.distribution = Gauss2dErrorDistribution( scale=scale, limits=limits )<br>
elif name == "model" 
    self.distribution = ModelDistribution( scale=scale, limits=limits )<br>
elif name == "bernoulli" 
    self.distribution = BernoulliErrorDistribution()<br>
else 
    raise ValueError( "Unknown error distribution %s" % name )<br>

<a name="setEngines"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setEngines(</strong> engines=None, enginedict=None ) 
</th></tr></thead></table>
<p>
setEngines( self, engines=None, enginedict=None ) 


## the same for all engines. 
self.phantoms = PhantomCollection( dynamic=self.problem.isDynamic() )

if enginedict is None 
    enginedict = {<br>
        "galilean" : GalileanEngine,<br>
        "chord" : ChordEngine,<br>
        "birth" : BirthEngine,<br>
        "death" : DeathEngine,<br>
        "struct": StructureEngine,<br>
        "gibbs" : GibbsEngine,<br>
        "random": RandomEngine,<br>
        "step"  : StepEngine }<br>

if engines is None 
    engines = self.problem.myEngines()<br>

self.engines = []
if isinstance( engines, str ) 
    engines = [engines]<br>
for name in engines 
    if isinstance( name, Engine ) :<br>
        engine = name<br>
        engine.walkers  = self.walkers<br>
        engine.errdis   = self.distribution<br>
        engine.phantoms = self.phantoms<br>
        engine.verbose  = self.verbose<br>
        self.engines   += [engine]<br>
        continue<br>

    if not isinstance( name, str ) :<br>
        raise ValueError( "Cannot interpret ", name, " as string or as Engine" )<br>

    try :<br>
        Eng = enginedict[name]<br>
        seed = self.rng.randint( self.TWOP31 )<br>
        engine = Eng( self.walkers, self.distribution, seed=seed, <br>
                    phantoms=self.phantoms, verbose=self.verbose )<br>
    except :<br>
        raise ValueError( "Unknown Engine name : %10s" % name )<br>

    self.engines += [engine]<br>



<a name="setInitialEngine"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setInitialEngine(</strong> ensemble, allpars, fitIndex, startdict=None )
</th></tr></thead></table>
<p>********INITIALIZATION***************************************************
setInitialEngine( self, ensemble, allpars, fitIndex, startdict=None )


if startdict is None 
    startdict = { "start" : StartEngine }<br>

# Make the walkers list
 walker = Walker( 0, self.problem, numpy.asarray( allpars ), fitIndex )<br>
 self.walkers = WalkerList( walker=walker, ensemble=ensemble )<br>

if self.initialEngine is not None
    # decorate with proper information<br>
    self.initialEngine.walkers = self.walkers<br>
    self.initialEngine.errdis = self.distribution<br>

else 
    try :<br>
        name = self.problem.myStartEngine()<br>
        StartEng = startdict[name]<br>
        seed = self.rng.randint( self.TWOP31 )<br>
        self.initialEngine = StartEng( self.walkers, self.distribution,<br>
                seed=seed )<br>
    except :<br>
        raise ValueError( "Unknown StartEngine name : %10s" % name )<br>

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
    self.initialEngine.execute( walker.id, -math.inf )<br>

 for w in self.walkers :<br>
     print( w.id, w.problem.model.npars, len( w.problem.model.parameters), len( w.allpars) )<br>
     w.check( nhyp=self.distribution.nphypar )<br>


<a name="plotResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotResult(</strong> walker, iter, plot=0 )
</th></tr></thead></table>
<p>
plotResult( self, walker, iter, plot=0 )


if plot == 0 
    return<br>

plt.figure( 'iterplot' )

if self.line is not None 
    ax = plt.gca()<br>
    if plot < 2 :<br>
        plt.pause( 0.02 )       ## updates and displays the plot before pause<br>
    ax.remove( )<br>
    self.text.set_text( "Iteration %d" % iter )<br>

if self.ymin is None 
    self.ymin = numpy.min( self.problem.ydata )<br>
    self.ymax = numpy.max( self.problem.ydata )<br>

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


 print( "Rate        %f" % self.rate )<br>
print( "Engines              success     reject     failed", end="" )
if self.bestBoost 
    print( "       best", end="" )<br>
print( "      calls" )

for engine in self.engines 
    print( "%-16.16s " % engine, end="" )<br>
    engine.printReport( best=self.bestBoost )<br>
print( "Calls to LogL     %10d" % self.distribution.ncalls, end="" )
if self.distribution.nparts > 0 
    print( "   to dLogL %10d" % self.distribution.nparts )<br>
else 
    print( "" )<br>

print( "Samples  %10d" % len( self.samples ) )
print( "Evidence    %10.3f +- %10.3f" % (self.evidence, self.precision ) )



