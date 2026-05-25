---
---
<br><br>

<a name="Engine"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class Engine(</strong> object )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py target=_blank>[source]</a></th></tr></thead></table>
<p>

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
<strong>Engine(</strong> walkers, errdis, slow=None, nstep=None, phancol=None, copy=None,
 seed=4213, verbose=0 )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L85-L137 target=_blank>[source]</a></th></tr></thead></table>

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
* nstep  :  None or int
<br>&nbsp;&nbsp;&nbsp;&nbsp; None automatically determine the number of steps
<br>&nbsp;&nbsp;&nbsp;&nbsp; int  use this number of steps
* seed  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; for random number generator
* verbose  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; report about the engines when verbose > 4
* copy  :  Engine
<br>&nbsp;&nbsp;&nbsp;&nbsp; engine to be copied 

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L139-L142 target=_blank>[source]</a></th></tr></thead></table>

Return a copy of this engine. 
<a name="setWalker"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setWalker(</strong> kw, problem, allpars, logL, walker=None, fitIndex=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L144-L178 target=_blank>[source]</a></th></tr></thead></table>
Update the walker with problem, allpars, LogL and logW.

<b>Parameters</b>

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

<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> problem, dval, kpar=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L180-L209 target=_blank>[source]</a></th></tr></thead></table>
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
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L211-L239 target=_blank>[source]</a></th></tr></thead></table>
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
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L241-L251 target=_blank>[source]</a></th></tr></thead></table>
Calculate the starting position and reset

<b>Parameters</b>

* unitStart  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; start position in npars-dimensions in unit space

<a name="calcJourney"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>calcJourney(</strong> unitDistance ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L253-L262 target=_blank>[source]</a></th></tr></thead></table>
Calculate the distance travelled since reset

<b>Parameters</b>

* unitDistance  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; step size in npars-dimensions in unit space

<a name="reportJourney"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportJourney(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L264-L269 target=_blank>[source]</a></th></tr></thead></table>

<a name="makeIndex"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makeIndex(</strong> np, val ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L271-L275 target=_blank>[source]</a></th></tr></thead></table>

<a name="reportCall"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportCall(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L277-L279 target=_blank>[source]</a></th></tr></thead></table>

Store a call to engine 
<a name="reportSuccess"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportSuccess(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L281-L285 target=_blank>[source]</a></th></tr></thead></table>
Add 1 to the number of succesfull steps: logL < lowLhood.

<a name="reportReject"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportReject(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L287-L291 target=_blank>[source]</a></th></tr></thead></table>
Add 1 to the number of rejected steps: logL > lowLhood.

<a name="reportFailed"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportFailed(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L293-L297 target=_blank>[source]</a></th></tr></thead></table>
Add 1 to the number of failed steps: could not construct a step.

<a name="reportBest"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportBest(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L299-L303 target=_blank>[source]</a></th></tr></thead></table>
Add 1 to the number of best likelihoods found upto now.

<a name="printReport"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>printReport(</strong> best=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L305-L311 target=_blank>[source]</a></th></tr></thead></table>

<a name="successRate"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>successRate(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L313-L324 target=_blank>[source]</a></th></tr></thead></table>
Return percentage of success.

<a name="getUnitMinmax"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getUnitMinmax(</strong> problem, lowLhood, nap ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L326-L345 target=_blank>[source]</a></th></tr></thead></table>
Calculate unit minimum and maximum from the Phantoms

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; To extract the unit range for
* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; low likelihood boundary

<a name="getUnitRange"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getUnitRange(</strong> problem, lowLhood, nap ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L347-L374 target=_blank>[source]</a></th></tr></thead></table>
Calculate unit range and minimum from PhantomCollection

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; To extract the unit range for
* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; low likelihood boundary

<a name="execute"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>execute(</strong> kw, lowLhood )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L376-L392 target=_blank>[source]</a></th></tr></thead></table>
Execute the engine for difusing the parameters

<b>Parameters</b>

* kw  :  walker-id
<br>&nbsp;&nbsp;&nbsp;&nbsp; walker to diffuse
* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; low limit on the loglikelihood

<b>Returns</b>

* int  :  number of succesfull moves


<a name="printIter"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>printIter(</strong> iteration=0, repiter=1000 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Engine.py#L394-L413 target=_blank>[source]</a></th></tr></thead></table>
Return True when to print this iteration

<b>Parameters</b>

* iteration  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; iteration number
* repiter  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; if verbose == 4 print every repiter

Endline #L415
