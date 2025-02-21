---
---


<a name="ChordEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class ChordEngine(</strong> Engine )
</th></tr></thead></table>

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
* reset  :  bool (False)<br>
    always reset othonormal basis <br>
* extend  :  bool (False)<br>
    perform the step-out action until logL < lowL<br>
* plotter  :  <br>
<b>Attributes from Engine</b>
walkers, errdis, slow, maxtrials, nstep, rng, verbose, report, unitRange, unitMin
Author       Do Kester.

<a name="ChordEngine"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>ChordEngine(</strong> walkers, errdis, copy=None, **kwargs ) 
</th></tr></thead></table>

Constructor.
<b>Parameters</b>
* walkers  :  WalkerList<br>
    walkers to be diffused<br>
* errdis  :  ErrorDistribution<br>
    error distribution to be used<br>
* copy  :  ChordEngine<br>
    to be copied<br>
* kwargs  :  for Engine<br>
    "slow", "seed", "verbose"
<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>

Return copy of this. 

<a name="__setattr__"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>__setattr__(</strong> name, value )
</th></tr></thead></table>

Set attributes.

<a name="__str__"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>__str__(</strong> )
</th></tr></thead></table>
<a name="execute"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>execute(</strong> kw, lowLhood, iteration=0 )
</th></tr></thead></table>

Execute the engine by diffusing the parameters.
<b>Parameters</b>
* kw  :  int<br>
    index of walker to diffuse<br>
* lowLhood  :  float<br>
    lower limit in logLikelihood<br>
* iteration  :  int<br>
    iteration number<br>
<b>Returns</b>
* int  :  the number of successfull moves<br>

<a name="stepOut"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>stepOut(</strong> problem, ptry, usav, vel, t, tmax, lowLhood, fitIndex ) 
</th></tr></thead></table>

Check if endpoints are indeed outside the lowLhood domain.
<a name="plotOut"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>plotOut(</strong> problem, usave, vel, t0, t1 ) 
</th></tr></thead></table>
<a name="plotOutDummy"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>plotOutDummy(</strong> problem, usave, vel, t0, t1 ) 
</th></tr></thead></table>

<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
<strong>Methods inherited from Engine</strong></th></tr></thead></table>



* [<strong>copy(</strong> )](./Engine.md#copy)
* [<strong>bestBoost(</strong> problem, myFitter=None ) ](./Engine.md#bestBoost)
* [<strong>setWalker(</strong> kw, problem, allpars, logL, walker=None, fitIndex=None ) ](./Engine.md#setWalker)
* [<strong>noBoost(</strong> walker ) ](./Engine.md#noBoost)
* [<strong>doBoost(</strong> walker ) ](./Engine.md#doBoost)
* [<strong>domain2Unit(</strong> problem, dval, kpar=None ) ](./Engine.md#domain2Unit)
* [<strong>unit2Domain(</strong> problem, uval, kpar=None ) ](./Engine.md#unit2Domain)
* [<strong>startJourney(</strong> unitStart ) ](./Engine.md#startJourney)
* [<strong>calcJourney(</strong> unitDistance ) ](./Engine.md#calcJourney)
* [<strong>unitTripSquare(</strong> unitDistance ) ](./Engine.md#unitTripSquare)
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
* [<strong>__str__(</strong> ) ](./Engine.md#__str__)
* [<strong>execute(</strong> kw, lowLhood )](./Engine.md#execute)
* [<strong>class DummyPlotter(</strong> object ) ](./Engine.md#DummyPlotter)
* [<strong>Engine(</strong> iter=1 ) ](./Engine.md#Engine)
* [<strong>start(</strong> param=None, ulim=None )](./Engine.md#start)
* [<strong>point(</strong> param, col=None, sym=0 )](./Engine.md#point)
* [<strong>move(</strong> param, ptry, col=None, sym=None )](./Engine.md#move)
* [<strong>stop(</strong> param=None, name=None )](./Engine.md#stop)

