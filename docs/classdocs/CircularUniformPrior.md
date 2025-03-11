---
---
<br><br>

<a name="CircularUniformPrior"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class CircularUniformPrior(</strong> <a href="./UniformPrior.html">UniformPrior</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/CircularUniformPrior.py target=_blank>Source</a></th></tr></thead></table>

Circular Uniform prior distribution, for location parameters.
The lowLimit is wrapped onto the highLimit.

A wrapper around
<br>&nbsp;&nbsp;&nbsp;&nbsp; UniformPrior( circular=... limits=... )

<b>Examples</b>

    pr = CircularUniformPrior( circular=math.pi )       # circular between [0,pi]
    pr = CircularUniformPrior( limits=[3,10] )          # circular between [3,10]

<b>Attributes from Prior</b>

lowLimit, highLimit, deltaP, circular, _lowDomain, _highDomain, _umin, _urng


<a name="CircularUniformPrior"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>CircularUniformPrior(</strong> circular=None, limits=None, prior=None )
</th></tr></thead></table>

Constructor.

<b>Parameters</b>

* limits  :  array of 2 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; [low,high]  range of the prior. Low is wrapped onto high.
* circular  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; period of circularity
* prior  :  CircularUniformPrior
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be copied.


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>

Return a (deep) copy of itself. 
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./UniformPrior.html">UniformPrior</a></th></tr></thead></table>


* [<strong>getIntegral(</strong> ) ](./UniformPrior.md#getIntegral)
* [<strong>domain2Unit(</strong> dval )](./UniformPrior.md#domain2Unit)
* [<strong>unit2Domain(</strong> uval )](./UniformPrior.md#unit2Domain)
* [<strong>result(</strong> x )](./UniformPrior.md#result)
* [<strong>partialLog(</strong> p )](./UniformPrior.md#partialLog)
* [<strong>isBound(</strong> )](./UniformPrior.md#isBound)
* [<strong>shortName(</strong> )](./UniformPrior.md#shortName)


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Prior.html">Prior</a></th></tr></thead></table>


* [<strong>limitedIntegral(</strong> center=0, circular=False, limits=None ) ](./Prior.md#limitedIntegral)
* [<strong>setLimits(</strong> limits=None )](./Prior.md#setLimits)
* [<strong>setPriorAttributes(</strong> limits, circular ) ](./Prior.md#setPriorAttributes)
* [<strong>isCircular(</strong> ) ](./Prior.md#isCircular)
* [<strong>limitedDomain2Unit(</strong> dval ) ](./Prior.md#limitedDomain2Unit)
* [<strong>limitedUnit2Domain(</strong> uval ) ](./Prior.md#limitedUnit2Domain)
* [<strong>circularDomain2Unit(</strong> dval ) ](./Prior.md#circularDomain2Unit)
* [<strong>circularUnit2Domain(</strong> uval ) ](./Prior.md#circularUnit2Domain)
* [<strong>unsetLimits(</strong> )](./Prior.md#unsetLimits)
* [<strong>setAttributes(</strong> limits=None, scale=None ) ](./Prior.md#setAttributes)
* [<strong>isOutOfLimits(</strong> par )](./Prior.md#isOutOfLimits)
* [<strong>checkLimit(</strong> par )](./Prior.md#checkLimit)
* [<strong>stayInLimits(</strong> par )](./Prior.md#stayInLimits)
* [<strong>hasLowLimit(</strong> )](./Prior.md#hasLowLimit)
* [<strong>hasHighLimit(</strong> )](./Prior.md#hasHighLimit)
* [<strong>hasLimits(</strong> )](./Prior.md#hasLimits)
* [<strong>getLimits(</strong> )](./Prior.md#getLimits)
* [<strong>getRange(</strong> )](./Prior.md#getRange)
* [<strong>partialDomain2Unit(</strong> p )](./Prior.md#partialDomain2Unit)
* [<strong>logResult(</strong> p ) ](./Prior.md#logResult)
* [<strong>numPartialDomain2Unit(</strong> dval )](./Prior.md#numPartialDomain2Unit)
* [<strong>numPartialLog(</strong> p )](./Prior.md#numPartialLog)
