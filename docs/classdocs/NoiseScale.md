---
---
<br><br><br>

<a name="NoiseScale"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class NoiseScale(</strong> <a href="./HyperParameter.html">HyperParameter</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/NoiseScale.py target=_blank>Source</a></th></tr></thead></table>
<p>

Hyperparameter for the scale of a ScaledErrorDistribution

it is a measure of the noise.

Information about the scale of the noise is stored in his class.
It is either in the form of a fixed number, when the noise scale
is known or in the form of a Prior with limits.
By default this prior is a JeffreysPrior..

The full use of priors is reserved for Bayesian calculations as
in NestedSampler

<b>Attributes</b>

* scale  :  float<br>
    the value of the noiseScale.  Default: 1.0<br>
* stdev  :  float<br>
    the standard deviation of the noise scale.  Default: None<br>
* prior  :  Prior<br>
    the prior for the noiseScale.  Default: JeffreysPrior<br>
* fixed  :  boolean<br>
    keep the noise scale fixed at the value given by scale.<br>
    default: True<br>
* minimum  :  boolean<br>
    automatic noise scaling with a minimum. default: False<br>


<a name="NoiseScale"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>NoiseScale(</strong> scale=1.0, isFixed=True, prior=None, limits=None,
 copy=None )
</th></tr></thead></table>
<p>

Constructor.

<b>Parameters</b>

* scale  :  float<br>
    float   value of the noise scale<br>
* isFixed  :  bool<br>
    True:   Consider the hyperparameter as fixed<br>
    False:  Optimize the parameter too (when relevant)<br>
            It might need a prior and/or limits to be set<br>
            The default prior is JeffreysPrior<br>
* prior  :  None or Prior<br>
    None : no prior set<br>
    Prior : the prior probability on scale<br>
* limits  :  None or list of 2 floats<br>
    None : no limits set<br>
    [lo,hi] : limits to be passed to the Prior.<br>
    If limits are set, the default for Prior is JeffreysPrior<br>
* copy  :  NoiseScale<br>
    NoiseScale to copy<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Return a copy. 

<a name="minimumScale"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>minimumScale(</strong> scale=None ) 
</th></tr></thead></table>
<p>

Fit the noise scale with a minimum value.

<b>Parameters</b>

* scale  :  float<br>
    the value of the noise scale. Default: noiseScale.scale<br>


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./HyperParameter.html">HyperParameter</a></th></tr></thead></table>


* [<strong>checkPrior(</strong> ) ](./HyperParameter.md#checkPrior)
* [<strong>setLimits(</strong> limits )](./HyperParameter.md#setLimits)
* [<strong>getLimits(</strong> )](./HyperParameter.md#getLimits)
* [<strong>isBound(</strong> ) ](./HyperParameter.md#isBound)
* [<strong>domain2Unit(</strong> dval )](./HyperParameter.md#domain2Unit)
* [<strong>unit2Domain(</strong> uval )](./HyperParameter.md#unit2Domain)
* [<strong>partialDomain2Unit(</strong> dval )](./HyperParameter.md#partialDomain2Unit)
