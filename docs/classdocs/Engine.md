---
---
<br><br>

<a name="Engine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Engine(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py target=_blank>Source</a></th></tr></thead></table>
<p>

Engine defines common properties of all Engines.

An Engine moves around a walker in a random way such that its likelood
remain above the low-likelihood-limit.

<b>Attributes</b>

* walkers  :  WalkerList<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of walkers to be diffused<br>
* errdis  :  ErrorDistribution<br>
&nbsp;&nbsp;&nbsp;&nbsp; error distribution to be used<br>
* slow  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; If slow > 0, run this engine every slow-th iteration.<br>
* phantoms  :  PhantomCollection<br>
&nbsp;&nbsp;&nbsp;&nbsp; Collection of valid walker positions collected during engine execution<br>
* maxtrials  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; maximum number of trials for various operations<br>
* rng  :  numpy.random.RandomState<br>
&nbsp;&nbsp;&nbsp;&nbsp; random number generator<br>
* verbose  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; if verbose > 4 report about the engines. (mostly for debugging)<br>

* report  :  list of int (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; reports number of succes, accepted, rejected, failed calls. Plus the total.<br>
* unitRange  :  array_like (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; present max size of the parameter cloud (in unitspace: [0,1])<br>
* unitMin  :  array_like (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; present minimum values of the parameter cloud (in unitspace: [0,1])<br>

Author       Do Kester.


<a name="Engine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Engine(</strong> walkers, errdis, slow=None, phantoms=None, copy=None,
 seed=4213, verbose=0 )
</th></tr></thead></table>
<p>

Constructor.

Only one PhantomCollection should be present for all Engines.

<b>Parameters</b>

* walkers  :  list of Walker<br>
&nbsp;&nbsp;&nbsp;&nbsp; walkers to be diffused<br>
* errdis  :  ErrorDistribution<br>
&nbsp;&nbsp;&nbsp;&nbsp; error distribution to be used<br>
* slow  :  None or int > 0<br>
&nbsp;&nbsp;&nbsp;&nbsp; Run this engine every slow-th iteration. None for all.<br>
* phantoms  :  None or PhantomCollection<br>
&nbsp;&nbsp;&nbsp;&nbsp; Container for all valid walkers, that have been tried. But were not kept.<br>
&nbsp;&nbsp;&nbsp;&nbsp; To calculate the spread of the parameters vs likelihood.<br>
* seed  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; for random number generator<br>
* verbose  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; report about the engines when verbose > 4<br>
* copy  :  Engine<br>
    engine to be copied 

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Return a copy of this engine. 

<a name="bestBoost"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>bestBoost(</strong> problem, myFitter=None ) 
</th></tr></thead></table>
<p>

When a logL is found better that all the rest, try to update
it using a fitter.

Parameters
problem : Problem
&nbsp;&nbsp;&nbsp;&nbsp; the problem at hand<br>
myFitter : None or Fitter
&nbsp;&nbsp;&nbsp;&nbsp; None fetches LevenbergMarquardtFitter<br>
    a (non-linear) fitter

<a name="setWalker"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setWalker(</strong> kw, problem, allpars, logL, walker=None, fitIndex=None ) 
</th></tr></thead></table>
<p>

Update the walker with problem, allpars, LogL and logW.

<b>Parameters</b>

* walker  :  Sample<br>
&nbsp;&nbsp;&nbsp;&nbsp; sample to be updated<br>

* kw  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index in walkerlist, of the walker to be replaced<br>
* problem  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; the problem in the walker<br>
* allpars  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters<br>
* logL  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; log Likelihood<br>
* walker  :  Walker or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; Copy this walker or create new one<br>
* fitIndex  :  array_like<br>
    (new) fitIndex

<a name="noBoost"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>noBoost(</strong> walker ) 
</th></tr></thead></table>
<p>
<a name="doBoost"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>doBoost(</strong> walker ) 
</th></tr></thead></table>
<p>

Check if walker is best in phantoms and try to optimize.

<b>Parameters</b>

* walker  :  Walker<br>
    new walker to be checked

<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> problem, dval, kpar=None ) 
</th></tr></thead></table>
<p>

Return value in [0,1] for the selected parameter.

<b>Parameters</b>

* problem  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; the problem involved<br>
* dval  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; domain value for the selected parameter<br>
* kpar  :  None or array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; selected parameter index, where kp is index in [parameters, hyperparams]<br>
    None means all

<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> problem, uval, kpar=None ) 
</th></tr></thead></table>
<p>

Return domain value for the selected parameter.

<b>Parameters</b>

* problem  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; the problem involved<br>
* uval  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; unit value for the selected parameter<br>
* kpar  :  None or array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; selected parameter indices, where kp is index in [parameters, hyperparams]<br>
    None means all.

<a name="startJourney"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>startJourney(</strong> unitStart ) 
</th></tr></thead></table>
<p>

Calculate the starting position and reset

<b>Parameters</b>

* unitStart  :  array_like<br>
    start position in npars-dimensions in unit space

<a name="calcJourney"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>calcJourney(</strong> unitDistance ) 
</th></tr></thead></table>
<p>

Calculate the distance travelled since reset

<b>Parameters</b>

* unitDistance  :  array_like<br>
    step size in npars-dimensions in unit space

<a name="reportJourney"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportJourney(</strong> ) 
</th></tr></thead></table>
<p>
<a name="makeIndex"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makeIndex(</strong> np, val ) 
</th></tr></thead></table>
<p>
<a name="reportCall"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportCall(</strong> )
</th></tr></thead></table>
<p>
Store a call to engine 

<a name="reportSuccess"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportSuccess(</strong> )
</th></tr></thead></table>
<p>

Add 1 to the number of succesfull steps: logL < lowLhood.

<a name="reportReject"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportReject(</strong> )
</th></tr></thead></table>
<p>

Add 1 to the number of rejected steps: logL > lowLhood.

<a name="reportFailed"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportFailed(</strong> )
</th></tr></thead></table>
<p>

Add 1 to the number of failed steps: could not construct a step.

<a name="reportBest"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportBest(</strong> )
</th></tr></thead></table>
<p>

Add 1 to the number of best likelihoods found upto now.

<a name="printReport"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>printReport(</strong> best=False ) 
</th></tr></thead></table>
<p>
<a name="successRate"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>successRate(</strong> ) 
</th></tr></thead></table>
<p>

Return percentage of success.

<a name="getUnitMinmax"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getUnitMinmax(</strong> problem, lowLhood ) 
</th></tr></thead></table>
<p>

Calculate unit minimum and maximum from the Phantoms

<b>Parameters</b>

* problem  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; To extract the unit range for<br>
* lowLhood  :  float<br>
    low likelihood boundary

<a name="getUnitRange"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getUnitRange(</strong> problem, lowLhood ) 
</th></tr></thead></table>
<p>

Calculate unit range and minimum from PhantomCollection

<b>Parameters</b>

* problem  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; To extract the unit range for<br>
* lowLhood  :  float<br>
    low likelihood boundary

<a name="execute"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>execute(</strong> kw, lowLhood )
</th></tr></thead></table>
<p>

Execute the engine for difusing the parameters

<b>Parameters</b>

* kw  :  walker-id<br>
&nbsp;&nbsp;&nbsp;&nbsp; walker to diffuse<br>
* lowLhood  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; low limit on the loglikelihood<br>

<b>Returns</b>

* int  :  number of succesfull moves<br>


