---
---
<br><br>

<a name="Sample"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Sample(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Sample.py target=_blank>Source</a></th></tr></thead></table>

Sample is weighted random draw from a Posterior distribution as
provided by a Sampler

Each Sample maintains 5 attributes

<b>Attributes</b>

* id  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; identification number
* parent  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; id of the parent (-1 for Adam/Eve)
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model being used
* logL  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; log Likelihood = log Prob( data | params )
* logW  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; log Weights of the log of the weight of the sample.
<br>&nbsp;&nbsp;&nbsp;&nbsp; The weight is the relative contribution to the evidence integral.
<br>&nbsp;&nbsp;&nbsp;&nbsp; logW = logL + log( width )
<br>&nbsp;&nbsp;&nbsp;&nbsp; The logZ, the evidence, equals the log of the sum of the contributions.
<br>&nbsp;&nbsp;&nbsp;&nbsp; logZ = log( sum( exp( logW ) ) )
* parameters  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters (of the model)
* nuisance  :  array_like (optional)
<br>&nbsp;&nbsp;&nbsp;&nbsp; nuisance parameters (of the problem)
* hyper  :  array_like (optional)
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of hyper parameters (of the error distribution)
* fitIndex  :  array_like or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of allpars to be fitted.
* allpars  :  array_like (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of parameters, nuisance parameters and hyperparameters

Author       Do Kester


<a name="Sample"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Sample(</strong> id, parent, start, model, parameters=None, fitIndex=None, copy=None )
</th></tr></thead></table>

Constructor.

<b>Parameters</b>

* id  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; id of the sample
* parent  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; id of the parent (-1 for Adam/Eve)
* start  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; iteration in which the walker was constructed
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model being used. Parameters are copied from this model.
* parameters  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of model parameters
* fitIndex  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of indices in allpars that need fitting
* copy  :  Sample
<br>&nbsp;&nbsp;&nbsp;&nbsp; the sample to be copied


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
Copy.


