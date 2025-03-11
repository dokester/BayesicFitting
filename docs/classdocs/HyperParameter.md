---
---
<br><br>

<a name="HyperParameter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class HyperParameter(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/HyperParameter.py target=_blank>Source</a></th></tr></thead></table>
<p>

Values and priors for the parameter(s) of an ErrorDistribution.

Hyperparameters are not directly related to the model, they are
parameters of the error distribution.

Information about the scale of the noise is stored in a derived class,
noiseScale.

The full use of priors is reserved for Bayesian calculations as
in NestedSampler

<b>Attributes</b><br>
* hypar  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; the value of the hyperparameter.  Default: 1.0<br>
* stdev  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; the standard deviation of the hyperparameter.  Default: None<br>
* prior  :  Prior<br>
&nbsp;&nbsp;&nbsp;&nbsp; the prior for the hyperparameter.<br>
* isFixed  :  boolean<br>
&nbsp;&nbsp;&nbsp;&nbsp; keep the hyperparameter fixed at the value given by hypar.<br>
&nbsp;&nbsp;&nbsp;&nbsp; default: True<br>


<a name="HyperParameter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>HyperParameter(</strong> hypar=1, isFixed=True, prior=None, limits=None,
 copy=None )
</th></tr></thead></table>
<p>

Constructor.

<b>Parameters</b><br>
* hypar  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; value of the hyperparameter<br>
* isFixed  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; True:   Consider the hyperparameter as fixed<br>
&nbsp;&nbsp;&nbsp;&nbsp; False:  Optimize the parameter too (when relevant)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; It might need a prior and/or limits to be set<br>
* prior  :  None or Prior<br>
&nbsp;&nbsp;&nbsp;&nbsp; None : no prior is set if no limits are given else JeffreysPrior<br>
&nbsp;&nbsp;&nbsp;&nbsp; prior probability on the hyperparameter<br>
* limits  :  None or list of 2 floats [lo,hi]<br>
&nbsp;&nbsp;&nbsp;&nbsp; low limit and high limit on hypar.<br>
* copy  :  HyperParameter<br>
&nbsp;&nbsp;&nbsp;&nbsp; HyperParameter to copy<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Return a copy. 

<a name="checkPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>checkPrior(</strong> ) 
</th></tr></thead></table>
<p>

<b>Raises</b><br>
ValueError when no prior has been set.

<a name="setLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setLimits(</strong> limits )
</th></tr></thead></table>
<p>

Set the limits on the scale within the prior.

<b>Parameters</b><br>
* limits  :  list of 2 float<br>
&nbsp;&nbsp;&nbsp;&nbsp; the [low,high] limits.<br>


<a name="getLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLimits(</strong> )
</th></tr></thead></table>
<p>
Return the limits on the scale. 

<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> ) 
</th></tr></thead></table>
<p>
Return true is the itergral over the prior is bound. 

<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> dval )
</th></tr></thead></table>
<p>

Return a value in [0,1] given a value within the valid domain of
a parameter for the prior distribution.

<b>Parameters</b><br>
* dval  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; value within the domain of a parameter<br>


<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> uval )
</th></tr></thead></table>
<p>

Return a value within the valid domain of the parameter given a value
between [0,1] for the prior distribution.

<b>Parameters</b><br>
* uval  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; value within [0,1]<br>


<a name="partialDomain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialDomain2Unit(</strong> dval )
</th></tr></thead></table>
<p>

Return a the derivate of the domain2Unit function to dval.

<b>Parameters</b><br>
* dval  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; value within the domain of a parameter<br>


