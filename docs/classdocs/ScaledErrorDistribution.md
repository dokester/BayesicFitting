---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ScaledErrorDistribution.py target=_blank>Source</a></span></div>

<a name="ScaledErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class ScaledErrorDistribution(</strong> <a href="./ErrorDistribution.html">ErrorDistribution</a> )
</th></tr></thead></table>
<p>

Base class that defines methods common to error distributions with a scale.

GaussErrorDistribution
LaplaceErrorDistribution
CauchyErrorDistribution
ExponentialErrorDistribution
UniformErrorDistribution

Author       Do Kester.


<a name="ScaledErrorDistribution"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>ScaledErrorDistribution(</strong> scale=1.0, limits=None, fixed=None, copy=None )
</th></tr></thead></table>
<p>

Default Constructor.

<b>Parameters</b>

* scale  :  float<br>
    noise scale<br>
* limits  :  None or list of 2 floats [low,high]<br>
    None : no limits implying fixed scale<br>
    low     low limit on scale (needs to be >0)<br>
    high    high limit on scale<br>
    when limits are set, the scale is to be fitted<br>
* fixed  :  dictionary of {int:float}<br>
    int     list if parameters to fix permanently. Default None.<br>
    float   list of values for the fixed parameters.<br>

* copy  :  ScaledErrorDistribution<br>
    distribution to be copied.<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Return copy of this. 

<a name="setLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>setLimits(</strong> limits ) 
</th></tr></thead></table>
<p>

Set limits for scale.

<b>Parameters</b>

* limits  :  [low,high]<br>
    low : float or array_like<br>
        low limits<br>
    high : float or array_like<br>
        high limits

<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./ErrorDistribution.html">ErrorDistribution</a></th></tr></thead></table>


* [<strong>getGaussianScale(</strong> problem, allpars=None ) ](./ErrorDistribution.md#getGaussianScale)
* [<strong>getResiduals(</strong> problem, allpars=None )](./ErrorDistribution.md#getResiduals)
* [<strong>getChisq(</strong> problem, allpars=None )](./ErrorDistribution.md#getChisq)
* [<strong>toSigma(</strong> scale ) ](./ErrorDistribution.md#toSigma)
* [<strong>isBound(</strong> ) ](./ErrorDistribution.md#isBound)
* [<strong>acceptWeight(</strong> )](./ErrorDistribution.md#acceptWeight)
* [<strong>keepFixed(</strong> fixed=None ) ](./ErrorDistribution.md#keepFixed)
* [<strong>setPriors(</strong> priors ) ](./ErrorDistribution.md#setPriors)
* [<strong>domain2Unit(</strong> dval, ks ) ](./ErrorDistribution.md#domain2Unit)
* [<strong>unit2Domain(</strong> uval, ks ) ](./ErrorDistribution.md#unit2Domain)
* [<strong>logCLhood(</strong> problem, allpars )](./ErrorDistribution.md#logCLhood)
* [<strong>logLhood(</strong> problem, allpars )](./ErrorDistribution.md#logLhood)
* [<strong>partialLogL(</strong> problem, allpars, fitIndex ) ](./ErrorDistribution.md#partialLogL)
* [<strong>partialLogL_alt(</strong> problem, allpars, fitIndex ) ](./ErrorDistribution.md#partialLogL_alt)
* [<strong>numPartialLogL(</strong> problem, allpars, fitIndex ) ](./ErrorDistribution.md#numPartialLogL)
* [<strong>updateLogL(</strong> problem, allpars, parval=None )](./ErrorDistribution.md#updateLogL)
* [<strong>setResult(</strong> )](./ErrorDistribution.md#setResult)
* [<strong>hyparname(</strong> k ) ](./ErrorDistribution.md#hyparname)
