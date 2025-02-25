---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Explorer.py target=_blank>Source</a></span></div>

<a name="Explorer"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class Explorer(</strong> object )
</th></tr></thead></table>
<p>

Explorer is a helper class of NestedSampler, which contains and runs the
diffusion engines.

It uses Threads to parallelise the diffusion engines.

<b>Attributes</b>

* walkers  :  WalkerList<br>
    walkers to be explored<br>
* engines  :  [engine]<br>
    list of engines to be used<br>
* errdis  :  ErrorDistribution<br>
    to be used<br>
* rng  :  numpy.random.RandomState<br>
    random number generator<br>
* rate  :  float (1.0)<br>
    governs processing speed (vs precision)<br>
* maxtrials  :  int (5)<br>
    number of trials<br>
* verbose  :  int (0)<br>
    level of blabbering<br>
* lowLhood  :  float<br>
    present low likelihood level<br>
* iteration  :  int<br>
    counting explorer calls<br>

Author       Do Kester.


<a name="Explorer"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>Explorer(</strong> ns, threads=False )
</th></tr></thead></table>
<p>

Construct Explorer from a NestedSampler object.

<b>Parameters</b>

* ns  :  NestedSampler<br>
    the calling NestedSampler. It provides the attributes.<br>


<a name="explore"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>explore(</strong> worst, lowLhood, iteration )
</th></tr></thead></table>
<p>

Explore the likelihood function, using threads.

<b>Parameters</b>

* worst  :  [int]<br>
    list of walkers to be explored/updated<br>
* lowLhood  :  float<br>
    level of the low likelihood<br>


<a name="exploreWalker"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>exploreWalker(</strong> kw, lowLhood, engines, rng )
</th></tr></thead></table>
<p>

Move the walker around until it is randomly distributed over the prior and
higher in logL then lowLhood

<b>Parameters</b>

* kw  :  int<br>
    index in walkerlist, of the walker to be explored<br>
* lowLhood  :  float<br>
    minimum value for the log likelihood<br>
* engine  :  list of Engine<br>
    to be used<br>
* rng  :  RandomState<br>
    random number generator

<a name="selEngines"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>selEngines(</strong> iteration ) 
</th></tr></thead></table>
<p>

Select engines with slowly changing parameters once per so many iterations.

<b>Parameter</b>

* iteration  :  int<br>
    iteration number

<a name="allEngines"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>allEngines(</strong> iteration ) 
</th></tr></thead></table>
<p>

Always use all engines.

<b>Parameters</b>

* iteration  :  int<br>
    iteration number

<a name="checkWalkers"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>checkWalkers(</strong> ) 
</th></tr></thead></table>
<p>
<a name="logLcheck"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>logLcheck(</strong> walker ) 
</th></tr></thead></table>
<p>

Sanity check when no moves are found, if the LogL is still the same as the stored logL.

<b>Parameters</b>

* walker  :  Walker<br>
    the one with the stored logL<br>

<b>Raises</b>

ValueError at inconsistency.


