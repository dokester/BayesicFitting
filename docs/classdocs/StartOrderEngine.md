---
---
<br><br>

<a name="StartOrderEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class StartOrderEngine(</strong> <a href="./OrderEngine.html">OrderEngine</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source// target=_blank>[source]</a></th></tr></thead></table>
<p>

StartEngine generates a parameter list in random order.

It is used to initialize the set of trial samples.

<b>Attributes from Engine</b>

walkers, errdis, maxtrials, nstep, slow, rng, report, phantoms, verbose

Author       Do Kester.


<a name="StartOrderEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>StartOrderEngine(</strong> walkers, errdis, copy=None, **kwargs )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L43-L59 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

<b>Parameters</b>

* walkers  :  WalkerList
<br>&nbsp;&nbsp;&nbsp;&nbsp; walkers to be diffused
* errdis  :  ErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; error distribution to be used
* copy  :  OrderEngine
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be copied
* kwargs  :  dict for Engine
<br>&nbsp;&nbsp;&nbsp;&nbsp; "phantoms", "slow", "seed", "verbose"


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L61-L67 target=_blank>[source]</a></th></tr></thead></table>

Return copy of this. 
<a name="execute"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>execute(</strong> kw, lowLhood, fitIndex=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L69-L96 target=_blank>[source]</a></th></tr></thead></table>
Execute the engine by a random selection of the parameters.

<b>Parameters</b>

* kw  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; id of waker to diffuse
* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; lower limit in logLikelihood
* fitIndex  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of parameter indices (not active)
<b>Returns</b>

* int  :  the number of successfull moves


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./OrderEngine.html">OrderEngine</a></th></tr></thead></table>


* [<strong>calculateUnitRange(</strong> ) ](./OrderEngine.md#calculateUnitRange)


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
