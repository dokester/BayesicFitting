---
---
<br><br>

<a name="ChordEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class ChordEngine(</strong> <a href="./Engine.html">Engine</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ChordEngine.py target=_blank>Source</a></th></tr></thead></table>

Move a a walker in a random direction.

The ChordEngine draws a random line through the walker parameters in
unit space, from unitMin (lowpoint) with lengths unitRange (highpoint).

A random point on the line is selected. If the corresponding parameter
set has a likelihood < LowLhood, it is accepted. Otherwise either the
highpoint is reset to the random point (if randompoint > walkerpoint)
or the lowpoint is replaced by the randompoint (if walker < random).
Then a new random point on the line is selected, until the point is accepted.

When the point is accepted, another random line is constructed
through the new point and orthogonal to (all) previous ones.
(The orthogonality is not implemented now. TBC).

This is an independent implementation inspired by the polychord engine
described in
"POLYCHORD: next-generation nested sampling",
WJ Handley, MP Hobson and AN Lasenby.
MNRAS (2015) Volume 453, Issue 4, p 4384–4398

<b>Attributes</b>

* debug  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; perform the step-out action too

<b>Attributes from Engine</b>

walkers, errdis, slow, maxtrials, nstep, rng, verbose, report, unitRange, unitMin

Author       Do Kester.


<a name="ChordEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>ChordEngine(</strong> walkers, errdis, copy=None, **kwargs ) 
</th></tr></thead></table>

Constructor.

<b>Parameters</b>

* walkers  :  WalkerList
<br>&nbsp;&nbsp;&nbsp;&nbsp; walkers to be diffused
* errdis  :  ErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; error distribution to be used
* copy  :  ChordEngine
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be copied
* kwargs  :  for Engine
<br>&nbsp;&nbsp;&nbsp;&nbsp; "slow", "seed", "verbose"

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>

Return copy of this. 
<a name="execute"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>execute(</strong> kw, lowLhood, append=False, iteration=0 )
</th></tr></thead></table>
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

* int  :  the number of successfull moves


<a name="stepOut"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>stepOut(</strong> problem, ptry, usav, vel, t, tmax, lowLhood, fitIndex ) 
</th></tr></thead></table>
Check if endpoints are indeed outside the lowLhood domain.

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
