---
---
<br><br>

<a name="StepEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class StepEngine(</strong> <a href="./Engine.html">Engine</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StepEngine.py target=_blank>[source]</a></th></tr></thead></table>
<p>

Move a walker in a random direction.

The StepEngine tries to move the parameters at most 4 times in
a random direction.

<b>Attributes from Engine</b>

walkers, errdis, maxtrials, nstep, slow, rng, report, phantoms, verbose   


Author       Do Kester.


<a name="StepEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>StepEngine(</strong> walkers, errdis, copy=None, **kwargs ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StepEngine.py#L52-L69 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

<b>Parameters</b>

* walkers  :  WalkerList
<br>&nbsp;&nbsp;&nbsp;&nbsp; walkers to be diffused
* errdis  :  ErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; error distribution to be used
* copy  :  StepEngine
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be copied
* kwargs  :  for Engine
<br>&nbsp;&nbsp;&nbsp;&nbsp; "phantoms", "slow", "seed", "verbose"

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StepEngine.py#L71-L78 target=_blank>[source]</a></th></tr></thead></table>

Return copy of this. 
<a name="execute"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>execute(</strong> kw, lowLhood, iteration=0 )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StepEngine.py#L80-L182 target=_blank>[source]</a></th></tr></thead></table>
Execute the engine by diffusing the parameters.

<b>Parameters</b>

* kw  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index of walker to diffuse
* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; lower limit in logLikelihood
* append  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; set walker in place or append
* iteration  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; iteration number

<b>Returns</b>

* int  :  the number of successfull steps


Endline #L184
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Engine.html">Engine</a></th></tr></thead></table>


* [<strong>setWalker(</strong> kw, problem, allpars, logL, walker=None, fitIndex=None ) ](./Engine.md#setWalker)
* [<strong>domain2Unit(</strong> problem, dval, kpar=None ) ](./Engine.md#domain2Unit)
* [<strong>unit2Domain(</strong> problem, uval, kpar=None ) ](./Engine.md#unit2Domain)
* [<strong>startJourney(</strong> unitStart ) ](./Engine.md#startJourney)
* [<strong>calcJourney(</strong> unitDistance ) ](./Engine.md#calcJourney)
* [<strong>reportJourney(</strong> ) ](./Engine.md#reportJourney)
* [<strong>makeIndex(</strong> np, val ) ](./Engine.md#makeIndex)
* [<strong>reportCall(</strong> )](./Engine.md#reportCall)
* [<strong>reportSuccess(</strong> )](./Engine.md#reportSuccess)
* [<strong>reportReject(</strong> )](./Engine.md#reportReject)
* [<strong>reportFailed(</strong> )](./Engine.md#reportFailed)
* [<strong>reportBest(</strong> )](./Engine.md#reportBest)
* [<strong>printReport(</strong> best=False ) ](./Engine.md#printReport)
* [<strong>successRate(</strong> ) ](./Engine.md#successRate)
* [<strong>getUnitMinmax(</strong> problem, lowLhood, nap ) ](./Engine.md#getUnitMinmax)
* [<strong>getUnitRange(</strong> problem, lowLhood, nap ) ](./Engine.md#getUnitRange)
* [<strong>printIter(</strong> iteration=0, repiter=1000 ) ](./Engine.md#printIter)
