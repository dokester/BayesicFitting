---
---


<a name="Engine"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th align="left>"
<strong>class Engine(</strong> object )
</th></tr></thead></table>


Engine defines common properties of all Engines.

An Engine moves around a walker in a random way such that its likelood
remain above the low-likelihood-limit.

<b>Attributes</b>

* walkers  : ( WalkerList)<br>
    list of walkers to be diffused
* errdis  : ( ErrorDistribution)<br>
    error distribution to be used
* slow  : ( int)<br>
    If slow > 0, run this engine every slow-th iteration.
* phancol  : ( PhantomCollection)<br>
    Collection of valid walker positions collected during engine execution
* maxtrials  : ( int)<br>
    maximum number of trials for various operations
* rng  : ( numpy.random.RandomState)<br>
    random number generator
* verbose  : ( int)<br>
    if verbose > 4 report about the engines. (mostly for debugging)

* report  : ( list of int (read only))<br>
    reports number of succes, accepted, rejected, failed calls. Plus the total.
* unitRange  : ( array_like (read only))<br>
    present max size of the parameter cloud (in unitspace: [0,1])
* unitMin  : ( array_like (read only))<br>
    present minimum values of the parameter cloud (in unitspace: [0,1])

Author       Do Kester.

<a name="Engine"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>Engine(</strong> walkers, errdis, slow=None, phancol=None, copy=None,
 seed=4213, verbose=0 )
</th></tr></thead></table>


Constructor.

Only one PhantomCollection should be present for all Engines.

<b>Parameters</b>

* walkers  : ( list of Walker)<br>
    walkers to be diffused
* errdis  : ( ErrorDistribution)<br>
    error distribution to be used
* slow  : ( None or int > 0)<br>
    Run this engine every slow-th iteration. None for all.
* phancol  : ( None or PhantomCollection)<br>
    Container for all valid walkers, that have been tried. But were not kept.
    To calculate the spread of the parameters vs likelihood.
* seed  : ( int)<br>
    for random number generator
* verbose  : ( int)<br>
    report about the engines when verbose > 4
* copy  : ( Engine)<br>
    engine to be copied 
<a name="copy"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>copy(</strong> )
</th></tr></thead></table>

Return a copy of this engine. 

<a name="bestBoost"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>bestBoost(</strong> problem, myFitter=None ) 
</th></tr></thead></table>


When a logL is found better that all the rest, try to update
it using a fitter.

Parameters
problem : Problem
    the problem at hand
myFitter : None or Fitter
    None fetches LevenbergMarquardtFitter
    a (non-linear) fitter
<a name="setWalker"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>setWalker(</strong> kw, problem, allpars, logL, walker=None, fitIndex=None ) 
</th></tr></thead></table>


Update the walker with problem, allpars, LogL and logW.

<b>Parameters</b>

* walker  : ( Sample)<br>
    sample to be updated

* kw  : ( int)<br>
    index in walkerlist, of the walker to be replaced
* problem  : ( Problem)<br>
    the problem in the walker
* allpars  : ( array_like)<br>
    list of all parameters
* logL  : ( float)<br>
    log Likelihood
* walker  : ( Walker or None)<br>
    Copy this walker or create new one
* fitIndex  : ( array_like)<br>
    (new) fitIndex
<a name="noBoost"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>noBoost(</strong> walker ) 
</th></tr></thead></table>
<a name="doBoost"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>doBoost(</strong> walker ) 
</th></tr></thead></table>


Check if walker is best in phancol and try to optimize.

<b>Parameters</b>

* walker  : ( Walker)<br>
    new walker to be checked
<a name="domain2Unit"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>domain2Unit(</strong> problem, dval, kpar=None ) 
</th></tr></thead></table>


Return value in [0,1] for the selected parameter.

<b>Parameters</b>

* problem  : ( Problem)<br>
    the problem involved
* dval  : ( float)<br>
    domain value for the selected parameter
* kpar  : ( None or array_like)<br>
    selected parameter index, where kp is index in [parameters, hyperparams]
    None means all
<a name="unit2Domain"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>unit2Domain(</strong> problem, uval, kpar=None ) 
</th></tr></thead></table>


Return domain value for the selected parameter.

<b>Parameters</b>

* problem  : ( Problem)<br>
    the problem involved
* uval  : ( array_like)<br>
    unit value for the selected parameter
* kpar  : ( None or array_like)<br>
    selected parameter indices, where kp is index in [parameters, hyperparams]
    None means all.
<a name="startJourney"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>startJourney(</strong> unitStart ) 
</th></tr></thead></table>


Calculate the starting position and reset

<b>Parameters</b>

* unitStart  : ( array_like)<br>
    start position in npars-dimensions in unit space
<a name="calcJourney"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>calcJourney(</strong> unitDistance ) 
</th></tr></thead></table>


Calculate the distance travelled since reset

<b>Parameters</b>

* unitDistance  : ( array_like)<br>
    step size in npars-dimensions in unit space
<a name="unitTripSquare"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>unitTripSquare(</strong> unitDistance ) 
</th></tr></thead></table>


Return the squared unit distance 

<b>Parameters</b>

* unitDistance  : ( array_like)<br>
    step size in npars-dimensions in unit space
<a name="reportJourney"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>reportJourney(</strong> ) 
</th></tr></thead></table>
<a name="makeIndex"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>makeIndex(</strong> np, val ) 
</th></tr></thead></table>
<a name="reportCall"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>reportCall(</strong> )
</th></tr></thead></table>

Store a call to engine 

<a name="reportSuccess"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>reportSuccess(</strong> )
</th></tr></thead></table>


Add 1 to the number of succesfull steps: logL < lowLhood.
<a name="reportReject"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>reportReject(</strong> )
</th></tr></thead></table>


Add 1 to the number of rejected steps: logL > lowLhood.
<a name="reportFailed"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>reportFailed(</strong> )
</th></tr></thead></table>


Add 1 to the number of failed steps: could not construct a step.
<a name="reportBest"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>reportBest(</strong> )
</th></tr></thead></table>


Add 1 to the number of best likelihoods found upto now.
<a name="printReport"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>printReport(</strong> best=False ) 
</th></tr></thead></table>
<a name="successRate"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>successRate(</strong> ) 
</th></tr></thead></table>


Return percentage of success.
<a name="getUnitMinmax"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>getUnitMinmax(</strong> problem, lowLhood, nap ) 
</th></tr></thead></table>


Calculate unit minimum and maximum from the Phantoms

<b>Parameters</b>

* problem  : ( Problem)<br>
    To extract the unit range for
* lowLhood  : ( float)<br>
    low likelihood boundary
* nap  : ( int)<br>
    number of all parameters
<a name="getUnitRange"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>getUnitRange(</strong> problem, lowLhood, nap ) 
</th></tr></thead></table>


Calculate unit range and minimum from PhantomCollection

<b>Parameters</b>

* problem  : ( Problem)<br>
    To extract the unit range for
* lowLhood  : ( float)<br>
    low likelihood boundary
* nap  : ( int)<br>
    number of all parameters
<a name="__str__"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>__str__(</strong> ) 
</th></tr></thead></table>
<a name="execute"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>execute(</strong> kw, lowLhood )
</th></tr></thead></table>


Execute the engine for difusing the parameters

<b>Parameters</b>

* kw  : ( walker-id)<br>
    walker to diffuse
* lowLhood  : ( float)<br>
    low limit on the loglikelihood

<b>Returns</b>

* int  : ( number of succesfull moves)<br>



<a name="DummyPlotter"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th align="left>"
<strong>class DummyPlotter(</strong> object ) 
</th></tr></thead></table>
<a name="Engine"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>Engine(</strong> iter=1 ) 
</th></tr></thead></table>
<a name="start"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>start(</strong> param=None, ulim=None )
</th></tr></thead></table>

start the plot. 

<a name="point"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>point(</strong> param, col=None, sym=0 )
</th></tr></thead></table>


Place a point at position param using color col and symbol sym.
<a name="move"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>move(</strong> param, ptry, col=None, sym=None )
</th></tr></thead></table>


Move parameters at position param to ptry using color col.
<a name="stop"></a>
<table><thead style="background-color:#D0D0FF; width:100%"><tr><th style="align:left">
<strong>stop(</strong> param=None, name=None )
</th></tr></thead></table>

Stop (show) the plot. 


