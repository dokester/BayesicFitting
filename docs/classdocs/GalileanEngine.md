---
---
<br><br>

<a name="GalileanEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class GalileanEngine(</strong> <a href="./Engine.html">Engine</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/GalileanEngine.py target=_blank>Source</a></th></tr></thead></table>
<p>

Move all parameters in forward steps, with optional mirroring on the edge.

Move the parameters in a random direction for N iterations; mirror the direction
on the gradient of the logLikelihood when the parameters enter the zone of logLlow.

<b>Attributes</b><br>
* size  :  0.5<br>
&nbsp;&nbsp;&nbsp;&nbsp; of the step<br>

<b>Attributes from Engine</b><br>
walkers, errdis, maxtrials, nstep, slow, rng, report, phantoms, verbose

Author       Do Kester.


<a name="GalileanEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>GalileanEngine(</strong> walkers, errdis, copy=None, **kwargs )
</th></tr></thead></table>
<p>

Default Constructor.

<b>Parameters</b><br>
* walkers  :  WalkerList<br>
&nbsp;&nbsp;&nbsp;&nbsp; walkers to be diffused<br>
* errdis  :  ErrorDistribution<br>
&nbsp;&nbsp;&nbsp;&nbsp; error distribution to be used<br>
* copy  :  GalileanEngine<br>
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

Execute the engine by diffusing the parameters.

<b>Parameters</b><br>
* kw  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index in walkerlist, of the walker<br>
* lowLhood  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; lower limit in logLikelihood<br>
* append  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; set walker in place of append<br>

<b>Returns</b><br>
* int  :  the number of successfull moves<br>


<a name="quadinterpol"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>quadinterpol(</strong> L0, Lm, L1, lowL ) 
</th></tr></thead></table>
<p>

Quadratic interpolation of points (x,y)
x = [0.0, 0.5, 1.0]
y = [L0, Lm, L1]  where L0 > Lm > L1    
interpolation at y = lowL.

<b>Returns</b><br>
* xvalue  :  float<br>
    largest of the two inside [0,1]

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
