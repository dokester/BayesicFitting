---
---
<br><br>

<a name="ScaledErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class ScaledErrorDistribution(</strong> <a href="./ErrorDistribution.html">ErrorDistribution</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source// target=_blank>[source]</a></th></tr></thead></table>
<p>

Base class that defines methods common to error distributions with a scale.

&nbsp; GaussErrorDistribution
<br>&nbsp; LaplaceErrorDistribution
<br>&nbsp; CauchyErrorDistribution
<br>&nbsp; ExponentialErrorDistribution
<br>&nbsp; UniformErrorDistribution

Author       Do Kester.


<a name="ScaledErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>ScaledErrorDistribution(</strong> scale=1.0, limits=None, fixed=None, copy=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L53-L82 target=_blank>[source]</a></th></tr></thead></table>

Default Constructor.

<b>Parameters</b>

* scale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; noise scale
* limits  :  None or list of 2 floats [low,high]
<br>&nbsp;&nbsp;&nbsp;&nbsp; None : no limits implying fixed scale
<br>&nbsp;&nbsp;&nbsp;&nbsp; low     low limit on scale (needs to be >0)
<br>&nbsp;&nbsp;&nbsp;&nbsp; high    high limit on scale
<br>&nbsp;&nbsp;&nbsp;&nbsp; when limits are set, the scale is to be fitted
* fixed  :  dictionary of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; int     list if parameters to fix permanently. Default None.
<br>&nbsp;&nbsp;&nbsp;&nbsp; float   list of values for the fixed parameters.

* copy  :  ScaledErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; distribution to be copied.


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L84-L86 target=_blank>[source]</a></th></tr></thead></table>

Return copy of this. 
<a name="setLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setLimits(</strong> limits ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L88-L129 target=_blank>[source]</a></th></tr></thead></table>
Set limits for scale.

<b>Parameters</b>

* limits  :  [low,high]
<br>&nbsp;&nbsp;&nbsp;&nbsp; low : float or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; low limits
<br>&nbsp;&nbsp;&nbsp;&nbsp; high : float or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; high limits


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
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
* [<strong>hyparname(</strong> k ) ](./ErrorDistribution.md#hyparname)
