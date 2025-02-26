---
---
<br><br><br>

<a name="LoopEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class LoopEngine(</strong> <a href="./OrderEngine.html">OrderEngine</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/LoopEngine.py target=_blank>Source</a></th></tr></thead></table>
<p>

The LoopEngine tries to unloop a crossing loop.

Only for 2 dimensional TS problems.

Input order 
     0  1  2  3<br>
    15 14  5  4<br>
     7  6 13 12<br>
     8  9 10 11<br>

The loop crosses between (5,6) and (13,14). By switching the positions
of 6 and 13, and reversing the loop in between, a better solution is
reached (triangle inequality)

output order
     0  1  2  3<br>
    15 14  5  4<br>
    12 13  6  7<br>
    11 10  9  8<br>

This is NOT a random engine as it only steps in the uphill direction.

It belongs to the class of generalized travelling salesman problems
where the parameters of the problem is an ordered list.

The walker is kept when the logLikelihood > lowLhood

<b>Attributes from Engine</b>

walkers, errdis, maxtrials, nstep, slow, rng, report, phantoms, verbose

Author       Do Kester.


<a name="LoopEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>LoopEngine(</strong> walkers, errdis, copy=None, **kwargs )
</th></tr></thead></table>
<p>

Constructor.

<b>Parameters</b>

* walkers  :  SampleList<br>
    walkers to be diffused<br>
* errdis  :  ErrorDistribution<br>
    error distribution to be used<br>
* copy  :  LoopEngine<br>
    to be copied<br>
* kwargs  :  dict for Engine<br>
    "phantoms", "slow", "seed", "verbose"<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Return copy of this. 

<a name="executeOnce"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>executeOnce(</strong> kw, lowLhood, dims=[0,1] ) 
</th></tr></thead></table>
<p>

Execute the LoopEngine one time.

<b>Parameters</b>

* kw  :  int<br>
    walker to diffuse<br>
* lowLhood  :  float<br>
    lower limit in logLikelihood<br>
* dims  :  list of 2 ints<br>
    dimensions to process over

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./OrderEngine.html">OrderEngine</a></th></tr></thead></table>


* [<strong>execute(</strong> kw, lowLhood, append=False, iteration=0 )](./OrderEngine.md#execute)
* [<strong>calculateUnitRange(</strong> ) ](./OrderEngine.md#calculateUnitRange)


<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
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
