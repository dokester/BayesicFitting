---
---
<br><br>

<a name="Walker"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class Walker(</strong> object )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source// target=_blank>[source]</a></th></tr></thead></table>
<p>

Walker is member of the cloud of points used in NestedSampler.

<b>Attributes</b>

* id  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; identification number
* parent  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; id of the parent (-1 for Adam/Eve)
* start  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; iteration in which the walker is constructed
* step  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of randomization steps since copy
* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; the problem being addressed
* logL  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; log Likelihood = log Prob( data | params )
* logPrior  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; log Prior for the model
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of parameters and hyperparameters
* fitIndex  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of (super)parameters to be fitted.
* parameters  :  array_like (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters (of the model)
* hypars  :  array_like (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of hyper parameters (of the error distribution)

Author       Do Kester


<a name="Walker"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Walker(</strong> wid, problem, allpars, fitIndex, logL=0, parent=-1, start=0, copy=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L70-L112 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

Either errdis or copy is obligatory.

<b>Parameters</b>

* id  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; id of the walker
* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; the problem being used. Parameters are copied from its model.
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of parameters and hyperparameters
* fitIndex  :  None or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of allpars to be fitted
<br>&nbsp;&nbsp;&nbsp;&nbsp; None is all
* logL  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; log Likelihood
* parent  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; id of the parent (-1 for Adam/Eve)
* start  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; iteration in which the walker is constructed
* copy  :  Walker
<br>&nbsp;&nbsp;&nbsp;&nbsp; the walker to be copied


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L114-L119 target=_blank>[source]</a></th></tr></thead></table>
Copy.


<a name="toSample"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>toSample(</strong> logW ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L121-L181 target=_blank>[source]</a></th></tr></thead></table>
Return the contents of the Walker as a Sample.

<a name="check"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>check(</strong> errdis ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L183-L237 target=_blank>[source]</a></th></tr></thead></table>
Perform some sanity checks.

<b>Parameters</b>

* errdis  :  ErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; to check logL

