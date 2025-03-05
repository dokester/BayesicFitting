---
---
<br><br>

<a name="StructureEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class StructureEngine(</strong> <a href="./Engine.html">Engine</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StructureEngine.py target=_blank>Source</a></th></tr></thead></table>
<p>

The StructureEngine varies the internal structure of the model.

Only for Models that are Modifiable.

The member is kept when the logLikelihood > lowLhood.

<b>Attributes</b>

None of its own

<b>Attributes from Engine</b>

walkers, errdis, slow, maxtrials, rng, report, phantoms, verbose

Author       Do Kester.


<a name="StructureEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>StructureEngine(</strong> walkers, errdis, copy=None, **kwargs ) 
</th></tr></thead></table>
<p>

Constructor.

<b>Parameters</b>

* walkers  :  list of Walker<br>
&nbsp;&nbsp;&nbsp;&nbsp; walkers to be diffused<br>
* errdis  :  ErrorDistribution<br>
&nbsp;&nbsp;&nbsp;&nbsp; error distribution to be used<br>
* copy  :  StructureEngine<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be copied<br>
* kwargs  :  for Engine<br>
&nbsp;&nbsp;&nbsp;&nbsp; "phantoms", "slow", "seed", "verbose"<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Return copy of this. 

<a name="execute"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>execute(</strong> kw, lowLhood, append=False, iteration=0 )
</th></tr></thead></table>
<p>

Execute the engine by changing a component.

<b>Parameters</b>

* kw  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index of walker to diffuse<br>
* lowLhood  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; lower limit in logLikelihood<br>
* append  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; set walker in place or append in walkerlist<br>
* iteration  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; iteration number<br>

<b>Returns</b>

* int  :  the number of successfull moves<br>


<a name="executeOnce"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>executeOnce(</strong> wlkrid, lowLhood, update, location=None ) 
</th></tr></thead></table>
<p>

One execution call.

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Engine.html">Engine</a></th></tr></thead></table>


* [<strong>bestBoost(</strong> problem, myFitter=None ) ](./Engine.md#bestBoost)
* [<strong>setWalker(</strong> kw, problem, allpars, logL, walker=None, fitIndex=None ) ](./Engine.md#setWalker)
* [<strong>noBoost(</strong> walker ) ](./Engine.md#noBoost)
* [<strong>doBoost(</strong> walker ) ](./Engine.md#doBoost)
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
* [<strong>getUnitMinmax(</strong> problem, lowLhood ) ](./Engine.md#getUnitMinmax)
* [<strong>getUnitRange(</strong> problem, lowLhood ) ](./Engine.md#getUnitRange)
