---
---
<br><br>

<a name="Explorer"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class Explorer(</strong> object )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Explorer.py target=_blank>[source]</a></th></tr></thead></table>
<p>

Explorer is a helper class of NestedSampler, which contains and runs the
diffusion engines.

It uses Threads to parallelise the diffusion engines.

<b>Attributes</b>

* walkers  :  WalkerList
<br>&nbsp;&nbsp;&nbsp;&nbsp; walkers to be explored
* engines  :  [engine]
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of engines to be used
* errdis  :  ErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be used
* rng  :  numpy.random.RandomState
<br>&nbsp;&nbsp;&nbsp;&nbsp; random number generator
* rate  :  float (1.0)
<br>&nbsp;&nbsp;&nbsp;&nbsp; governs processing speed (vs precision)
* maxtrials  :  int (5)
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of trials
* verbose  :  int (0)
<br>&nbsp;&nbsp;&nbsp;&nbsp; level of blabbering
* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; present low likelihood level
* iteration  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; counting explorer calls

Author       Do Kester.


<a name="Explorer"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Explorer(</strong> ns, threads=False )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Explorer.py#L72-L98 target=_blank>[source]</a></th></tr></thead></table>

Construct Explorer from a NestedSampler object.

<b>Parameters</b>

* ns  :  NestedSampler
<br>&nbsp;&nbsp;&nbsp;&nbsp; the calling NestedSampler. It provides the attributes.


<a name="explore"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>explore(</strong> worst, lowLhood, iteration )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Explorer.py#L100-L145 target=_blank>[source]</a></th></tr></thead></table>
Explore the likelihood function, using threads.

<b>Parameters</b>

* worst  :  [int]
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of walkers to be explored/updated
* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; level of the low likelihood


<a name="exploreWalker"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>exploreWalker(</strong> kw, lowLhood, engines, rng )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Explorer.py#L147-L209 target=_blank>[source]</a></th></tr></thead></table>
Move the walker around until it is randomly distributed over the prior and
higher in logL then lowLhood

<b>Parameters</b>

* kw  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index in walkerlist, of the walker to be explored
* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; minimum value for the log likelihood
* engine  :  list of Engine
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be used
* rng  :  RandomState
<br>&nbsp;&nbsp;&nbsp;&nbsp; random number generator

<a name="selEngines"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>selEngines(</strong> iteration ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Explorer.py#L211-L225 target=_blank>[source]</a></th></tr></thead></table>
Select engines with slowly changing parameters once per so many iterations.

<b>Parameter</b>

* iteration  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; iteration number

<a name="allEngines"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>allEngines(</strong> iteration ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Explorer.py#L227-L236 target=_blank>[source]</a></th></tr></thead></table>
Always use all engines.

<b>Parameters</b>

* iteration  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; iteration number

<a name="checkWalkers"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>checkWalkers(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Explorer.py#L238-L243 target=_blank>[source]</a></th></tr></thead></table>

Perform sanity check on all walkers. 
Endline #L245
