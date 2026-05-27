---
---
<br><br>

<a name="StructureEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class StructureEngine(</strong> <a href="./Engine.html">Engine</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StructureEngine.py target=_blank>[source]</a></th></tr></thead></table>
<p>

The StructureEngine varies the internal structure of the model.

Only for Models that are Modifiable.

The member is kept when the logLikelihood > lowLhood.

<b>Attributes</b><br>
None of its own

<b>Attributes from Engine</b><br>
walkers, errdis, slow, maxtrials, rng, report, phantoms, verbose

Author       Do Kester.


<a name="StructureEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>StructureEngine(</strong> walkers, errdis, copy=None, **kwargs ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StructureEngine.py#L52-L69 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

<b>Parameters</b><br>
* walkers  :  list of Walker
<br>&nbsp;&nbsp;&nbsp;&nbsp; walkers to be diffused
* errdis  :  ErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; error distribution to be used
* copy  :  StructureEngine
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be copied
* kwargs  :  for Engine
<br>&nbsp;&nbsp;&nbsp;&nbsp; "phantoms", "slow", "seed", "verbose"


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StructureEngine.py#L71-L74 target=_blank>[source]</a></th></tr></thead></table>


<a name="execute"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>execute(</strong> kw, lowLhood, iteration=0 )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StructureEngine.py#L79-L107 target=_blank>[source]</a></th></tr></thead></table>
Execute the engine by changing a component.

<b>Parameters</b><br>
* kw  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index of walker to diffuse
* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; lower limit in logLikelihood
* append  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; set walker in place or append in walkerlist
* iteration  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; iteration number

<b>Returns</b><br>
* int  :  the number of successfull moves


<a name="executeOnce"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>executeOnce(</strong> wlkrid, lowLhood, location=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StructureEngine.py#L109-L153 target=_blank>[source]</a></th></tr></thead></table>
One execution call.

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
