---
---
<br><br>

<a name="GalileanEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class GalileanEngine(</strong> <a href="./Engine.html">Engine</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source// target=_blank>[source]</a></th></tr></thead></table>
<p>

Move all parameters in forward steps, with optional mirroring on the edge.

Move the parameters in a random direction for N iterations; mirror the direction
on the gradient of the logLikelihood when the parameters enter the zone of logLlow.

<b>Attributes</b>

* size  :  float (0.5)
<br>&nbsp;&nbsp;&nbsp;&nbsp; adaptable fraction for the (unit) direction of the stepping
* wiggle  :  float (0.2)
<br>&nbsp;&nbsp;&nbsp;&nbsp; factor to perturb the direction at each step. 
<br>&nbsp;&nbsp;&nbsp;&nbsp; between 0 (no perturbation) and 1 (new direction)

<b>Attributes from Engine</b>

walkers, errdis, maxtrials, nstep, slow, rng, report, phancol, verbose

Author       Do Kester.


<a name="GalileanEngine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>GalileanEngine(</strong> walkers, errdis, copy=None, **kwargs )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L75-L106 target=_blank>[source]</a></th></tr></thead></table>

Default Constructor.

<b>Parameters</b>

* walkers  :  WalkerList
<br>&nbsp;&nbsp;&nbsp;&nbsp; walkers to be diffused
* errdis  :  ErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; error distribution to be used
* copy  :  GalileanEngine
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be copied
* kwargs  :  for Engine
<br>&nbsp;&nbsp;&nbsp;&nbsp; "phancol", "slow", "seed", "verbose"


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L108-L116 target=_blank>[source]</a></th></tr></thead></table>

Return copy of this. 
<a name="execute"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>execute(</strong> kw, lowLhood, iteration=0 )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L118-L275 target=_blank>[source]</a></th></tr></thead></table>
Execute the engine by diffusing the parameters.

<b>Parameters</b>

* kw  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index in walkerlist, of the walker
* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; lower limit in logLikelihood

<b>Returns</b>

* int  :  the number of successfull moves


<a name="incsize"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>incsize(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L277-L280 target=_blank>[source]</a></th></tr></thead></table>

Return increased self.size 
<a name="decsize"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>decsize(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L282-L286 target=_blank>[source]</a></th></tr></thead></table>

Return decreased self.size. 
<a name="findEdge"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>findEdge(</strong> problem, ptry, fitIndex, Lhood, Ltry, lowLhood, um, size,
 plot=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L288-L372 target=_blank>[source]</a></th></tr></thead></table>
Find the edge of the likelihood where logL equals LowLhood. 

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; the problem
* ptry  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters with likelihood outside lowLhood region
* fitIndex  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters that need fitting
* Lhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; last likelihood before going outside
* Ltry  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; likelihood outside (at ptry)
* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; lower limit in logLikelihood
* um  :  UnitMovements (see below)
<br>&nbsp;&nbsp;&nbsp;&nbsp; of this run
* size  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; present size value

<b>Returns</b>

* pedge  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter values at the edge of lowLhood
* restep  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; part of the step outside lowLhood area. 

<a name="quadInterpol"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>quadInterpol(</strong> x, y, lowL, plot=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L374-L415 target=_blank>[source]</a></th></tr></thead></table>
Quadratic interpolation of a function defined by 3 point (x,y) at level
ylow.

<b>Parameters</b>

* x  :  array of 3 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; x-values
* y  :  array of 3 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; y-values   
* ylow  :  float 
<br>&nbsp;&nbsp;&nbsp;&nbsp; find xlow at ylow

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
