---
---


<a name="NestedSampler"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th align="left>"
<strong>class NestedSampler(</strong> object )
</th></tr></thead></table>


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
    It walks all (super)parameters in a fixed direction for about 5 steps.
    When a step ends outside the high likelihood region the direction is
    mirrored on the lowLikelihood edge and continued.

2. ChordEngine.
    It draws a randomly oriented line through a point inside the region,
    until it reaches outside the restricted likelihood region on both sides.
    A random point is selected on the line until it is inside the likelihood region.
    This process runs several times

3. GibbsEngine.
    It moves each of the parameters by a random step, one at a time.
    It is a randomwalk.

4. StepEngine.
    It moves all parameters in a random direction. It is a randomwalk.

For dynamic models 2 extra engines are defined

6. BirthEngine.
    It tries to increase the number of parameters.
    It can only be switched on for Dynamic Models.

7. DeathEngine.
    It tries to decrease the number of parameters.
    It can only be switched on for Dynamic Models.

For modifiable models 1 engine is defined.

8. StructureEngine.
    It alters the internal structure of the model.
    It can only be switched on for Modifiable Models.

<b>Attributes</b>

* xdata  :  array_like<br>
    array of independent input values
* model  :  Model<br>
    the model function to be fitted
* ydata  :  array_like<br>
    array of dependent (to be fitted) data
* weights  :  array_like (None)<br>
    weights pertaining to ydata
* problem  :  Problem (ClassicProblem)<br>
    to be solved (container of model, xdata, ydata and weights)
* distribution  :  ErrorDistribution<br>
    to calculate the loglikelihood
* ensemble  :  int (100)<br>
    number of walkers
* discard  :  int (1)<br>
    number of walkers to be replaced each generation
* rng  :  RandomState<br>
    random number generator
* seed  :  int (80409)<br>
    seed of rng
* rate  :  float (1.0)<br>
    speed of exploration
* maxsize  :  None or int<br>
    maximum size of the resulting sample list (None : no limit)
* minimumIterations  :  int (100)<br>
    minimum number of iterations (adapt when starting problems occur)
* end  :  float (2.0)<br>
    stopping criterion
* tolerance  :  float (-12)<br>
    stopping criterion: stop if log( dZ / Z ) < tolerance
* verbose  :  int<br>
    level of blabbering
* walkers  :  WalkerList<br>
    ensemble of walkers that explore the likelihood space
* samples  :  SampleList<br>
    Samples resulting from the exploration
* engines  :  list of Engine<br>
    Engine that move the walkers around within the given constraint: logL > lowLogL
* initialEngine  :  Engine<br>
    Engine that distributes the walkers over the available space
* restart  :  StopStart (TBW)<br>
    write intermediate results to (optionally) start from.

Author       Do Kester.

<a name="NestedSampler"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>NestedSampler(</strong> xdata=None, model=None, ydata=None, weights=None,
 accuracy=None, problem=None, distribution=None, limits=None,
 keep=None, ensemble=ENSEMBLE, discard=1, seed=80409, rate=RATE,
 bestBoost=False, usePhantoms=True,
 engines=None, maxsize=None, threads=False, verbose=1 ) 
</th></tr></thead></table>


Create a new class, providing inputs and model.

Either (model,xdata,ydata) needs to be provided or a completely filled
problem.

<b>Parameters</b>

* xdata  :  array_like<br>
    array of independent input values
* model  :  Model<br>
    the model function to be fitted
    the model needs priors for the parameters and (maybe) limits
* ydata  :  array_like<br>
    array of dependent (to be fitted) data
* weights  :  array_like (None)<br>
    weights pertaining to ydata
* accuracy  :  float or array_like<br>
    accuracy scale for the datapoints
    all the same or one for each data point
* problem  :  None or string or Problem<br>
    Defines the kind of problem to be solved.

    None        same as "classic"
    "classic" 	ClassicProblem
    "errors"	ErrorsInXandYProblem
    "multiple"	MultipleOutputProblem

    Problem     Externally defined Problem. When Problem has been provided,
                xdata, model, weights and ydata are not used.
keep : None or dict of {int:float}
    None of the model parameters are kept fixed.
    Dictionary of indices (int) to be kept at a fixed value (float).
    Hyperparameters follow model parameters.
    The values will override those at initialization.
    They are used in this instantiation, unless overwritten at the call to sample()
* distribution  :  None or String or ErrorDistribution<br>
    Defines the ErrorDistribution to be used
    When the hyperpar(s) are not to be kept fixed, they need `Prior` and maybe limits.

    None            same as "gauss"
    "gauss"         GaussErrorDistribution with (fixed) scale equal to 1.0
    "laplace"       LaplaceErrorDistribution with 1 hyperpar scale
    "poisson"       PoissonErrorDistribution no hyperpar
    "cauchy"        CauchyErrorDstribution with 1 hyperpar scale
    "uniform"       UniformErrorDistribution with 1 hyperpar scale
    "bernoulli"     BernoulliErrorDistribution no hyperpar
    "exponential"   ExponentialErrorDistribution with 2 hyperpar (scale, power)

    ErrorDistribution Externally defined ErrorDistribution
* limits  :  None or [low,high] or [[low],[high]]<br>
    None    no limits implying fixed hyperparameters of the distribution
    low     low limit on hyperpars
    high    high limit on hyperpars
    When limits are set the hyperpars are not fixed.
* ensemble  :  int<br>
    number of walkers
* discard  :  int<br>
    number of walkers to be replaced each generation
* seed  : int<br>
    seed of random number generator
* rate  :  float<br>
    speed of exploration
* bestBoost  :  bool or Fitter<br>
    False   no updates of best logLikelihood
    True    boost the fit using LevenbergMarquardtFitter
    fitter  boost the fit using this fitter.
* usePhantoms  :  bool<br>
    True    Copy starting walkers from phantoms
    False   Copy starting walkers from walkers
* engines  :  None or (list of) string or (list of) Engine<br>
    to randomly move the walkers around, within the likelihood bound.

    None        use a Problem defined selection of engines
    "galilean"  GalileanEngine	move forward and mirror on edges
    "chord"     ChordEngine   	select random point on random line
    "gibbs" 	GibbsEngine 	move one parameter at a time
    "step"  	StepEngine    	move all parameters in arbitrary direction

    For Dynamic models only
    "birth" 	BirthEngine     increase the parameter list of a walker by one
    "death" 	DeathEngine     decrease the parameter list of a walker by one

    For Modifiable models only
    "struct"    StructureEngine change the (internal) structure.

    Engine      an externally defined (list of) Engine
* maxsize  :  None or int<br>
    maximum size of the resulting sample list (None : no limit)
* threads  :  bool (False)<br>
    Use Threads to distribute the diffusion of discarded samples over the available cores.
* verbose  :  int (1)<br>
    0   silent
    1   basic information
    2   more about every 100th iteration
    3   more about every iteration
    >4  for debugging



The order in which the main attributes are created.

where       method                  attribute
__init__    setProblem              self.problem
__init__    setErrorDistribution    self.distribution
__init__    setEngines              self.phancol
                                    self.engines
__init__                            self.samples
sample      initSample
              initWalkers           self.walkers


                setInitialEngine    self.initialEngine


<a name="sample"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>sample(</strong> keep=None, plot=False )
</th></tr></thead></table>
******SAMPLE************************************************************
sample( self, keep=None, plot=False )


keep = self.initSample( keep=keep )

if ( self.problem.hasAccuracy and self.walkers[0].fitIndex[-1] < 0 and 
        not isinstance( self.distribution, GaussErrorDistribution ) ) 
    raise AttributeError( "%s cannot be combined with accuracies and variable scale" %
                            self.distribution ) 

self.logUnitDomain = 0
if self.usePhantoms 
    self.copyWalker = self.copyWalkerFromPhantoms

tail = self.initReport( keep=keep )

explorer = Explorer( self, threads=self.threads )

## move all walkers around for initial exploration of the complete space.
if not isinstance( self.problem.model, LinearModel ) or self.usePhantoms 
     print( "BURNIN PHASE STARTS =================================" )
    self.lowLhood = -sys.float_info.max
    # Explore all walker(s)
    explorer.explore( range( self.ensemble ), self.lowLhood, self.iteration )
    self.iteration = 0                  # reset iteration number
     print( "BURNIN PHASE ENDS ===================================" )


self.walkers.sort( key=self.walkerLogL )    # sort the walker list on logL

self.logZ = -sys.float_info.max
self.logdZ = 0
self.info = 0
self.logWidth = math.log( 1.0 - math.exp( -1.0 / self.livepointcount ) )

 TBD put self.logWidth in the saved file too
 if self.optionalRestart() 
     self.logWidth -= self.iteration * ( 1.0 * self.discard ) / self.ensemble

self.histinsert = []        ### TBC   what is this
self.sumWidth = 0.0

## iterate until done
while self.nextIteration() 

    worst = self.worst                      # the worst are low in the sorted ensemble
    self.lowLhood = self.walkers[worst-1].logL

    self.updateEvidence( worst )            # Update Z and H and store posterior samples

    self.iterReport( worst - 1, tail, plot=plot ) # some output when needed

    self.samples.weed( self.maxsize )       # remove overflow in samplelist

    self.iteration += 1

    self.updateWalkers( explorer, worst )

    newL = self.walkers[worst-1].logL
    self.histinsert += [self.walkers.firstIndex( newL )]

    self.optionalSave( )

    self.walkers.sort( key=self.walkerLogL )    # sort the walker list on logL



# End of Sampling: Update and store the remaining walkers
self.updateEvidence( self.ensemble )        # Update Evidence Z and Information H

# Calculate weighted average and stdevs for the parameters;
self.samples.LogZ = self.logZ
self.samples.info = self.info
self.samples.normalize( )

# put the info into the model
if self.problem.model and not self.problem.isDynamic() 
    self.problem.model.parameters = self.samples.parameters
    self.problem.model.stdevs = self.samples.stdevs

self.lastReport( -1, plot=plot )

return self.evidence
<a name="initSample"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>initSample(</strong> ensemble=None, keep=None ) 
</th></tr></thead></table>

initSample( self, ensemble=None, keep=None ) 

if keep is None 
    keep = self.keep
fitIndex, allpars = self.makeFitlist( keep=keep )

if ensemble is None 
    ensemble = self.ensemble
self.initWalkers( ensemble, allpars, fitIndex )

for eng in self.engines 
    eng.walkers = self.walkers
    eng.lastWalkerId = len( self.walkers )
    if self.bestBoost 
        eng.bestBoost( self.problem, myFitter=self.myFitter )

self.distribution.ncalls = 0                      #  reset number of calls

return keep

in Use
 sortLogL( self, walkers ) 
 return numpy.argsort( [w.logL for w in walkers] )
<a name="walkerLogL"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>walkerLogL(</strong> w ) 
</th></tr></thead></table>

walkerLogL( self, w ) 
return w.logL
<a name="makeFitlist"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>makeFitlist(</strong> keep=None ) 
</th></tr></thead></table>

makeFitlist( self, keep=None ) 


allpars = numpy.zeros( self.problem.npars + self.distribution.nphypar,
                       dtype=self.problem.partype )

np = self.problem.npars
fitlist = [k for k in range( np )]
nh = -self.distribution.nphypar
for sp in self.distribution.hyperpar 
    if not sp.isFixed and sp.isBound() 
        fitlist += [nh]                             # it is to be optimised
    elif self.problem.hasAccuracy and nh == -self.distribution.nphypar 
        allpars[nh] = 0                             # fix (model)scale at 0
    else 
        allpars[nh] = self.distribution.hypar[nh]   # fill in the fixed value

    nh += 1

nh = self.distribution.nphypar
if keep is not None 
    fitl = []
    kkeys = list( keep.keys() )
    for k in range( np + nh ) 
        if k in kkeys 
            allpars[k] = keep[k]                    # save keep.value in allpars
        elif fitlist[k] in kkeys 
            allpars[k] = keep[fitlist[k]]           # save keep.value in allpars
        else 
            fitl += [fitlist[k]]                    # list of pars to be fitted
    fitlist = fitl

return ( fitlist, allpars )

<a name="doIterPlot"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>doIterPlot(</strong> plot ) 
</th></tr></thead></table>

doIterPlot( self, plot ) 


if isinstance( plot, str ) 
    if plot == 'iter' or plot == 'all' 
        return 1
    elif plot == 'test' 
        return 2
    else 
        return 0
else 
    return 0
<a name="doLastPlot"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>doLastPlot(</strong> plot ) 
</th></tr></thead></table>

doLastPlot( self, plot ) 


if isinstance( plot, str ) 
    return plot == 'last' or plot == 'all'
else 
    return True if plot else False

<a name="initReport"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>initReport(</strong> keep=None ) 
</th></tr></thead></table>

initReport( self, keep=None ) 

if self.verbose >= 1 
    fitIndex = self.walkers[0].fitIndex
    print( "Fit", ( "all" if keep is None else fitIndex ),
            ( "(nuisance)" if self.problem.nuispars > 0 else "" ), 
            "parameters of" ) 
    if self.problem.model 
        print( " ", self.problem.model._toString( "  " ) )
    else 
        print( " ", self.problem )
    print( "Using a", self.distribution, end="" )
    np = -1
    cstr = " with "
    for name,hyp in zip( self.distribution.PARNAMES, self.distribution.hyperpar ) 
        print( cstr, end="" )
        if np in fitIndex 
            print( "unknown %s" % name, end="" )
        else 
            print( "%s = %7.2f " % (name, hyp.hypar), end="" )
        np -= 1
        cstr = " and "
    print( "\nMoving the walkers with ", end="" )
    for eng in self.engines 
        print( " ", eng, end="" )
    print( "" )
    if self.threads 
        print( "Using threads." )

tail = 0
if self.verbose > 1 
    while fitIndex is not None and fitIndex[-tail-1] < 0 and len( fitIndex ) > tail + 1 : 
        tail += 1

     tail = self.distribution.nphypar
    if tail == 0 
        print( "Iteration     logZ        H       LowL     npar parameters" )
    else 
        print( "Iteration     logZ        H       LowL     npar parameters", end="" )
        for k in range( 1,  min( 5, len( fitIndex ) - tail ) ) 
            print( "        ", end="" )
        for k in range( tail ) 
            print( "   %s" %self.distribution.hyparname( k ), end="" )
        print( "" )

return tail
<a name="iterReport"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>iterReport(</strong> kw, tail, plot=False ) 
</th></tr></thead></table>

iterReport( self, kw, tail, plot=False ) 

if self.verbose >= 3 or ( self.verbose >= 1 and
                          self.iteration % self.repiter == 0 )
    if self.verbose == 1 
        if ( self.iteration / self.repiter ) % 50 == 49 
            nwln = "\n"
        else 
            nwln = ""
        print( ">", end=nwln, flush=True )
    else 
        self.printIterRep( kw, tail=tail, max=4 )

    self.plotResult( self.walkers[kw], self.iteration, plot=self.doIterPlot( plot ) )

<a name="printIterRep"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>printIterRep(</strong> kw, parfmt="%s", tail=0, max=None, indent=0, end="\n" ) 
</th></tr></thead></table>

printIterRep( self, kw, parfmt="%s", tail=0, max=None, indent=0, end="\n" ) 

pl = self.walkers[kw].allpars
fi = self.walkers[kw].fitIndex
if fi is not None : 
    pl = pl[fi]
np = len( pl )

print( "%8d %#10.3g %8.1f %#10.3g %6d "%( self.iteration, self.logZ,
        self.info, self.lowLhood, np ), 
        parfmt % fmt( pl, max=max, tail=tail, indent=indent ), 
         fmt( self.sumWidth ), fmt( self.livepointcount ), fmt( self.phancol.length() ),
        end=end )

<a name="lastReport"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>lastReport(</strong> kw, plot=False ) 
</th></tr></thead></table>

lastReport( self, kw, plot=False ) 

 print( "SumWidth   ", fmt( self.sumWidth ) )

if self.verbose > 0 
    if self.verbose == 1 
        print( "\nIteration     logZ        H       LowL     npar" )

    self.printIterRep( kw, max=None, indent=13, parfmt="\nParameters  %s" )


     pl = self.walkers[kw].allpars
     fi = self.walkers[kw].fitIndex
     if fi is not None : 
         pl = pl[fi]
     np = len( pl )
     print( "%8d %#10.3g %8.1f %#10.3g %6d "%( self.iteration, self.logZ,
             self.info, self.lowLhood, np ) )
     print( "Parameters  ", fmt( pl, max=None, indent=13 ) )

if self.verbose >= 1 
    self.report()

if self.doLastPlot( plot ) 
    self.plotLast()
<a name="plotLast"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>plotLast(</strong> ) 
</th></tr></thead></table>

plotLast( self ) 
Plotter.plotSampleList( self.samples, self.problem.xdata, self.problem.ydata, 
            figsize=[12,8], residuals=True )
<a name="XXXgetMaxIter"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>XXXgetMaxIter(</strong> ) 
</th></tr></thead></table>

XXXgetMaxIter( self ) 


maxi = ( self.iteration if self.logdZ < self.tolerance else 
         self.end * self.ensemble * self.info / self.worst )
maxi = max( self.minimumIterations, maxi )
return maxi if self.maxIterations is None else min( maxi, self.maxIterations )
<a name="nextIteration"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>nextIteration(</strong> ) 
</th></tr></thead></table>

nextIteration( self ) 


if self.walkers[0].logL >= self.walkers[-1].logL 
    return False
if self.iteration < self.minimumIterations 
    return True
if self.maxIterations is not None and self.iteration >= self.maxIterations 
    return False
if self.sumWidth < 0.999 
    return True
if self.logdZ < self.tolerance 
    return False
if self.iteration > self.end * self.ensemble * self.info / self.worst 
    return False
return True
<a name="__str__"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>__str__(</strong> )
</th></tr></thead></table>


Return the name of this sampler. 
__str__( self )

return str( "NestedSampler" )


<a name="optionalRestart"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>optionalRestart(</strong> )
</th></tr></thead></table>
==============================================================================
optionalRestart( self )


if self.restart is not None and self.restart.wantRestore( )
    self.walkers, self.samples = self.restart.restore( self.walkers, self.samples )
    self.logZ = self.walkers.logZ
    self.info = self.walkers.info
    self.iteration = self.walkers.iteration
    return True
return False
<a name="optionalSave"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>optionalSave(</strong> )
</th></tr></thead></table>

optionalSave( self )


if self.restart is not None and self.restart.wantSave( ) and self.iteration % 100 == 0
    self.walkers.logZ = self.logZ
    self.walkers.info = self.info
    self.walkers.iteration = self.iteration
    self.restart.save( self.walkers, self.samples )

<a name="updateEvidence"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>updateEvidence(</strong> worst ) 
</th></tr></thead></table>

updateEvidence( self, worst ) 



for kw in range( worst ) 
    logWeight = self.logWidth + self.walkers[kw].logL + self.walkers[kw].logPrior

    # update evidence, logZ
    logZnew = numpy.logaddexp( self.logZ, logWeight )

    # update Information, H
    self.info = ( math.exp( logWeight - logZnew ) * self.lowLhood +
            math.exp( self.logZ - logZnew ) * ( self.info + self.logZ ) - logZnew )

    if math.isnan( self.info ) 
        self.info = 0.0
    self.logZ = logZnew

    # store posterior samples
    smpl = self.walkers[kw].toSample( logWeight )
    self.samples.add( smpl )

    self.sumWidth += math.exp( self.logWidth )

     self.logWidth -= 1.0 / ( self.ensemble - kw )
    self.logWidth -= 1.0 / self.ensemble

self.logdZ = logWeight - self.logZ
self.logUnitDomain += self.logDomainFraction 

return
<a name="unitDomain"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>unitDomain(</strong> ) 
</th></tr></thead></table>

unitDomain( self ) 


return math.exp( self.logUnitDomain )

<a name="copyWalker"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>copyWalker(</strong> worst )
</th></tr></thead></table>

copyWalker( self, worst )


for k in range( worst ) 
    kcp = self.rng.randint( worst, self.ensemble )
    self.walkers.copy( kcp, k, start=self.iteration )
     setatt( self.walkers[k], "parent", kcp )
     setatt( self.walkers[k], "start", self.iteration )
     setatt( self.walkers[k], "step", 0 )
<a name="copyWalkerFromPhantoms"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>copyWalkerFromPhantoms(</strong> worst )
</th></tr></thead></table>

copyWalkerFromPhantoms( self, worst )


plen = self.phancol.length()

for k in range( worst ) 
    while True 
        kcp = self.rng.randint( plen )
        if self.phancol.phantoms[kcp].logL > self.lowLhood 
            break
    self.walkers.copy( kcp, k, wlist=self.phancol.phantoms,
                       start=self.iteration )
     setatt( self.walkers[k], "parent", kcp )
     setatt( self.walkers[k], "start", self.iteration )

<a name="updateWalkers"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>updateWalkers(</strong> explorer, worst ) 
</th></tr></thead></table>

updateWalkers( self, explorer, worst ) 


self.copyWalker( worst )

# Explore the copied walker(s)
wlist = [k for k in range( worst )]
explorer.explore( wlist, self.lowLhood, self.iteration )


<a name="__setattr__"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>__setattr__(</strong> name, value ) 
</th></tr></thead></table>
********INTERNALS***************************************************
__setattr__( self, name, value ) 

# for hypar fitting
if name == "scale" and isinstance( self.distribution, ScaledErrorDistribution ) 
    self.distribution.scale = value
elif name == "power" and isinstance( self.distribution, ExponentialErrorDistribution ) 
    self.distribution.power = value
elif name == "copymode" and value == 1 
    self.usePhantoms = True
elif name == "bestUpdate" 

    self.myFitter = None
    if Tools.subclassof( value, BaseFitter ) 
        object.__setattr__( self, name, True )
        self.myFitter = value
    else 
        object.__setattr__( self, name, value )

else 
    object.__setattr__( self, name, value )
    if name == "verbose" 
        for eng in self.engines 
            eng.verbose = value
<a name="__getattr__"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>__getattr__(</strong> name ) 
</th></tr></thead></table>

__getattr__( self, name ) 

if name == "ensemble" or name == "livepointcount" 
    return len( self.walkers )
elif name == "xdata" 
    return self.problem.xdata
elif name == "model" 
    return self.problem.model
elif name == "ydata" 
    return self.problem.ydata
elif name == "weights" 
    return self.problem.weights
elif name == "worst" 
    return self.discard
elif name == "evidence" 
    return self.logZ / math.log( 10.0 )
elif name == "logZprecision" 
    return math.sqrt( max( self.info, 0 ) / self.ensemble )
elif name == "precision" 
    return self.logZprecision / math.log( 10.0 )
elif name == "information" 
    return self.info
elif name == "parameters" 
    return self.samples.getParameters()
elif name == "stdevs" or name == "standardDeviations" 
    self.samples.getParameters()
    return self.samples.stdevs
elif name == "hypars" 
    return self.samples.hypars
elif name == "stdevHypars" 
    return self.samples.stdevHypars
elif name == "scale" 
    return self.samples.hypars[0]
elif name == "stdevScale" 
    return self.samples.stdevHypars[0]
elif name == "modelfit" or name == "yfit" 
    return self.samples.average( self.problem.xdata )

********DISTRIBUTIONS***************************************************
<a name="setProblem"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>setProblem(</strong> name, model=None, xdata=None, ydata=None, weights=None,

 accuracy=None ) 
</th></tr></thead></table>
setProblem( self, name, model=None, xdata=None, ydata=None, weights=None,
            accuracy=None ) 


problemdict = {
    "classic"  : ClassicProblem,
    "errors"   : ErrorsInXandYProblem,
    "multiple" : MultipleOutputProblem,
    "evidence" : EvidenceProblem
}
    "salesman" : SalesmanProblem
    "order" : OrderProblem

if isinstance( name, Problem ) 
    self.problem = name
    if model is not None : self.problem.model = model
    if xdata is not None : self.problem.xdata = numpy.asarray( xdata )
    if ydata is not None : self.problem.ydata = numpy.asarray( ydata )
    if weights is not None : self.problem.weights = numpy.asarray( weights )
    if accuracy is not None : self.problem.setAccuracy( accuracy=accuracy )
    return

if not isinstance( name, str ) 
    raise ValueError( "Cannot interpret ", name, " as string or Problem" )

name = str.lower( name )
try 
    myProblem = problemdict[name]
    self.problem = myProblem( model, xdata=xdata, ydata=ydata, weights=weights,
                              accuracy=accuracy )
except 
    raise 
     raise ValueError( "Unknown problem name %s" % name )



<a name="setErrorDistribution"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>setErrorDistribution(</strong> name=None, limits=None, scale=1.0, power=2.0 )
</th></tr></thead></table>
********DISTRIBUTIONS***************************************************
setErrorDistribution( self, name=None, limits=None, scale=1.0, power=2.0 )


if name is None 
    name = self.problem.myDistribution()
elif isinstance( name, ErrorDistribution ) 
    self.distribution = name
    return

if not isinstance( name, str ) 
    raise ValueError( "Cannot interpret ", name, " as string or ErrorDistribution" )

name = str.lower( name )
 print( name )
if name == "gauss" 
    self.distribution = GaussErrorDistribution( scale=scale, limits=limits )
elif name == "laplace" 
    self.distribution = LaplaceErrorDistribution( scale=scale, limits=limits )
elif name == "poisson" 
    self.distribution = PoissonErrorDistribution()
elif name == "cauchy" 
    self.distribution = CauchyErrorDistribution( scale=scale, limits=limits )
elif name == "uniform" 
    self.distribution = UniformErrorDistribution( scale=scale, limits=limits )
elif name == "exponential" 
    self.distribution = ExponentialErrorDistribution( scale=scale, power=power, limits=limits )
elif name == "gauss2d" 
    self.distribution = Gauss2dErrorDistribution( scale=scale, limits=limits )
elif name == "model" 
    self.distribution = ModelDistribution( scale=scale, limits=limits )
elif name == "bernoulli" 
    self.distribution = BernoulliErrorDistribution()
else 
    raise ValueError( "Unknown error distribution %s" % name )
<a name="setEngines"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>setEngines(</strong> engines=None, enginedict=None ) 
</th></tr></thead></table>

setEngines( self, engines=None, enginedict=None ) 


## the same for all engines. 
self.phancol = PhantomCollection( dynamic=self.problem.isDynamic() )

if enginedict is None 
    enginedict = {
        "galilean" : GalileanEngine,
        "chord" : ChordEngine,
        "birth" : BirthEngine,
        "death" : DeathEngine,
        "struct": StructureEngine,
        "gibbs" : GibbsEngine,
        "random": RandomEngine,
        "step"  : StepEngine }

if engines is None 
    engines = self.problem.myEngines()

self.engines = []
if isinstance( engines, str ) 
    engines = [engines]
for name in engines 
    if isinstance( name, Engine ) 
        engine = name
        engine.walkers  = self.walkers
        engine.errdis   = self.distribution
        engine.phancol = self.phancol
        engine.verbose  = self.verbose
        self.engines   += [engine]
        continue

    if not isinstance( name, str ) 
        raise ValueError( "Cannot interpret ", name, " as string or as Engine" )

    try 
        Eng = enginedict[name]
        seed = self.rng.randint( self.TWOP31 )
        engine = Eng( self.walkers, self.distribution, seed=seed, 
                    phancol=self.phancol, verbose=self.verbose )
    except Exception 
        raise ValueError( "Unknown Engine name : %10s" % name )

    self.engines += [engine]


<a name="setInitialEngine"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>setInitialEngine(</strong> ensemble, allpars, fitIndex, startdict=None )
</th></tr></thead></table>
********INITIALIZATION***************************************************
setInitialEngine( self, ensemble, allpars, fitIndex, startdict=None )


if startdict is None 
    startdict = { "start" : StartEngine }

# Make the walkers list
 walker = Walker( 0, self.problem, numpy.asarray( allpars ), fitIndex )
 self.walkers = WalkerList( walker=walker, ensemble=ensemble )

if self.initialEngine is not None
    # decorate with proper information
    self.initialEngine.walkers = self.walkers
    self.initialEngine.errdis = self.distribution

else 
    try 
        name = self.problem.myStartEngine()
        StartEng = startdict[name]
        seed = self.rng.randint( self.TWOP31 )
        self.initialEngine = StartEng( self.walkers, self.distribution,
                seed=seed )
    except Exception 
        raise ValueError( "Unknown StartEngine name : %10s" % name )

self.initialEngine.verbose = self.verbose

# Calculate logL for all walkers.
self.distribution.lowLhood = -math.inf

# pass the PhantomCollection to the initial engine
self.initialEngine.phancol = self.phancol
<a name="initWalkers"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>initWalkers(</strong> ensemble, allpars, fitIndex, startdict=None )
</th></tr></thead></table>

initWalkers( self, ensemble, allpars, fitIndex, startdict=None )


# Make the walkers list
walker = Walker( 0, self.problem, numpy.asarray( allpars ), fitIndex )
self.walkers = WalkerList( walker=walker, ensemble=ensemble )

self.setInitialEngine( ensemble, allpars, fitIndex, startdict=startdict )

for walker in self.walkers 
    self.initialEngine.execute( walker.id, -sys.float_info.max )

 for w in self.walkers 
     print( w.id, w.problem.model.npars, len( w.problem.model.parameters), len( w.allpars) )
     w.check( nhyp=self.distribution.nphypar )

<a name="plotResult"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>plotResult(</strong> walker, iter, plot=0 )
</th></tr></thead></table>

plotResult( self, walker, iter, plot=0 )


if plot == 0 
    return

plt.figure( 'iterplot' )

if self.line is not None 
    ax = plt.gca()
    if plot < 2 
        plt.pause( 0.02 )       ## updates and displays the plot before pause
    ax.remove( )
    self.text.set_text( "Iteration %d" % iter )

if self.ymin is None 
    self.ymin = numpy.min( self.problem.ydata )
    self.ymax = numpy.max( self.problem.ydata )

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
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>report(</strong> )
</th></tr></thead></table>

report( self )


 print( "Rate        %f" % self.rate )
print( "Engines              success     reject     failed", end="" )
if self.bestBoost 
    print( "       best", end="" )
print( "      calls" )

for engine in self.engines 
    print( "%-16.16s " % engine, end="" )
    engine.printReport( best=self.bestBoost )
print( "Calls to LogL     %10d" % self.distribution.ncalls, end="" )
if self.distribution.nparts > 0 
    print( "   to dLogL %10d" % self.distribution.nparts )
else 
    print( "" )

print( "Samples  %10d" % len( self.samples ) )
print( "Evidence    %10.3f +- %10.3f" % (self.evidence, self.precision ) )



