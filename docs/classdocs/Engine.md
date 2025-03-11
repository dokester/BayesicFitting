---
---
<br><br>

<a name="Engine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Engine(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py target=_blank>Source</a></th></tr></thead></table>

Engine defines common properties of all Engines.

An Engine moves around a walker in a random way such that its likelood
remain above the low-likelihood-limit.

<b>Attributes</b>

* walkers  :  WalkerList
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of walkers to be diffused
* errdis  :  ErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; error distribution to be used
* slow  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; If slow > 0, run this engine every slow-th iteration.
* phantoms  :  PhantomCollection
<br>&nbsp;&nbsp;&nbsp;&nbsp; Collection of valid walker positions collected during engine execution
* maxtrials  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; maximum number of trials for various operations
* rng  :  numpy.random.RandomState
<br>&nbsp;&nbsp;&nbsp;&nbsp; random number generator
* verbose  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; if verbose > 4 report about the engines. (mostly for debugging)

* report  :  list of int (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; reports number of succes, accepted, rejected, failed calls. Plus the total.
* unitRange  :  array_like (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; present max size of the parameter cloud (in unitspace: [0,1])
* unitMin  :  array_like (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; present minimum values of the parameter cloud (in unitspace: [0,1])

Author       Do Kester.


<a name="Engine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Engine(</strong> walkers, errdis, slow=None, phantoms=None, copy=None,
 seed=4213, verbose=0 )
</th></tr></thead></table>

Constructor.

Only one PhantomCollection should be present for all Engines.

<b>Parameters</b>

* walkers  :  list of Walker
<br>&nbsp;&nbsp;&nbsp;&nbsp; walkers to be diffused
* errdis  :  ErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; error distribution to be used
* slow  :  None or int > 0
<br>&nbsp;&nbsp;&nbsp;&nbsp; Run this engine every slow-th iteration. None for all.
* phantoms  :  None or PhantomCollection
<br>&nbsp;&nbsp;&nbsp;&nbsp; Container for all valid walkers, that have been tried. But were not kept.
<br>&nbsp;&nbsp;&nbsp;&nbsp; To calculate the spread of the parameters vs likelihood.
* seed  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; for random number generator
* verbose  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; report about the engines when verbose > 4
* copy  :  Engine
<br>&nbsp;&nbsp;&nbsp;&nbsp; engine to be copied 

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>

Return a copy of this engine. 
<a name="bestBoost"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>bestBoost(</strong> problem, myFitter=None ) 
</th></tr></thead></table>
When a logL is found better that all the rest, try to update
it using a fitter.

Parameters
problem : Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; the problem at hand
myFitter : None or Fitter
<br>&nbsp;&nbsp;&nbsp;&nbsp; None fetches LevenbergMarquardtFitter
<br>&nbsp;&nbsp;&nbsp;&nbsp; a (non-linear) fitter

<a name="setWalker"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setWalker(</strong> kw, problem, allpars, logL, walker=None, fitIndex=None ) 
</th></tr></thead></table>
Update the walker with problem, allpars, LogL and logW.

<b>Parameters</b>

* walker  :  Sample
<br>&nbsp;&nbsp;&nbsp;&nbsp; sample to be updated

* kw  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index in walkerlist, of the walker to be replaced
* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; the problem in the walker
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters
* logL  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; log Likelihood
* walker  :  Walker or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; Copy this walker or create new one
* fitIndex  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; (new) fitIndex

<a name="noBoost"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>noBoost(</strong> walker ) 
</th></tr></thead></table>

<a name="doBoost"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>doBoost(</strong> walker ) 
</th></tr></thead></table>
Check if walker is best in phantoms and try to optimize.

<b>Parameters</b>

* walker  :  Walker
<br>&nbsp;&nbsp;&nbsp;&nbsp; new walker to be checked

<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> problem, dval, kpar=None ) 
</th></tr></thead></table>
Return value in [0,1] for the selected parameter.

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; the problem involved
* dval  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; domain value for the selected parameter
* kpar  :  None or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; selected parameter index, where kp is index in [parameters, hyperparams]
<br>&nbsp;&nbsp;&nbsp;&nbsp; None means all

<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> problem, uval, kpar=None ) 
</th></tr></thead></table>
Return domain value for the selected parameter.

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; the problem involved
* uval  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; unit value for the selected parameter
* kpar  :  None or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; selected parameter indices, where kp is index in [parameters, hyperparams]
<br>&nbsp;&nbsp;&nbsp;&nbsp; None means all.

<a name="startJourney"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>startJourney(</strong> unitStart ) 
</th></tr></thead></table>
Calculate the starting position and reset

<b>Parameters</b>

* unitStart  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; start position in npars-dimensions in unit space

<a name="calcJourney"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>calcJourney(</strong> unitDistance ) 
</th></tr></thead></table>
Calculate the distance travelled since reset

<b>Parameters</b>

* unitDistance  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; step size in npars-dimensions in unit space

<a name="reportJourney"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportJourney(</strong> ) 
</th></tr></thead></table>

<a name="makeIndex"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makeIndex(</strong> np, val ) 
</th></tr></thead></table>

<a name="reportCall"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportCall(</strong> )
</th></tr></thead></table>

Store a call to engine 
<a name="reportSuccess"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportSuccess(</strong> )
</th></tr></thead></table>
Add 1 to the number of succesfull steps: logL < lowLhood.

<a name="reportReject"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportReject(</strong> )
</th></tr></thead></table>
Add 1 to the number of rejected steps: logL > lowLhood.

<a name="reportFailed"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportFailed(</strong> )
</th></tr></thead></table>
Add 1 to the number of failed steps: could not construct a step.

<a name="reportBest"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportBest(</strong> )
</th></tr></thead></table>
Add 1 to the number of best likelihoods found upto now.

<a name="printReport"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>printReport(</strong> best=False ) 
</th></tr></thead></table>

<a name="successRate"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>successRate(</strong> ) 
</th></tr></thead></table>
Return percentage of success.

<a name="getUnitMinmax"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getUnitMinmax(</strong> problem, lowLhood ) 
</th></tr></thead></table>
Calculate unit minimum and maximum from the Phantoms

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; To extract the unit range for
* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; low likelihood boundary

<a name="getUnitRange"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getUnitRange(</strong> problem, lowLhood ) 
</th></tr></thead></table>
Calculate unit range and minimum from PhantomCollection

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; To extract the unit range for
* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; low likelihood boundary

<a name="execute"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>execute(</strong> kw, lowLhood )
</th></tr></thead></table>
Execute the engine for difusing the parameters

<b>Parameters</b>

* kw  :  walker-id
<br>&nbsp;&nbsp;&nbsp;&nbsp; walker to diffuse
* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; low limit on the loglikelihood

<b>Returns</b>

* int  :  number of succesfull moves


