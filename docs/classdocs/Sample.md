---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Sample.py target=_blank>Source</a></span></div>

<a name="Sample"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class Sample(</strong> object )
</th></tr></thead></table>
<p>

Sample is weighted random draw from a Posterior distribution as
provided by a Sampler

Each Sample maintains 5 attributes

<b>Attributes</b>

* id  :  int<br>
    identification number<br>
* parent  :  int<br>
    id of the parent (-1 for Adam/Eve)<br>
* model  :  Model<br>
    the model being used<br>
* logL  :  float<br>
    log Likelihood = log Prob( data | params )<br>
* logW  :  float<br>
    log Weights of the log of the weight of the sample.<br>
    The weight is the relative contribution to the evidence integral.<br>
    logW = logL + log( width )<br>
    The logZ, the evidence, equals the log of the sum of the contributions.<br>
    logZ = log( sum( exp( logW ) ) )<br>
* parameters  :  array_like<br>
    parameters (of the model)<br>
* nuisance  :  array_like (optional)<br>
    nuisance parameters (of the problem)<br>
* hyper  :  array_like (optional)<br>
    list of hyper parameters (of the error distribution)<br>
* fitIndex  :  array_like or None<br>
    list of allpars to be fitted.<br>
* allpars  :  array_like (read only)<br>
    list of parameters, nuisance parameters and hyperparameters<br>

Author       Do Kester


<a name="Sample"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>Sample(</strong> id, parent, start, model, parameters=None, fitIndex=None, copy=None )
</th></tr></thead></table>
<p>

Constructor.

<b>Parameters</b>

* id  :  int<br>
    id of the sample<br>
* parent  :  int<br>
    id of the parent (-1 for Adam/Eve)<br>
* start  :  int<br>
    iteration in which the walker was constructed<br>
* model  :  Model<br>
    the model being used. Parameters are copied from this model.<br>
* parameters  :  array_like<br>
    list of model parameters<br>
* fitIndex  :  array_like<br>
    list of indices in allpars that need fitting<br>
* copy  :  Sample<br>
    the sample to be copied<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>

Copy.


<a name="check"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>check(</strong> nhyp=0 ) 
</th></tr></thead></table>
<p>

