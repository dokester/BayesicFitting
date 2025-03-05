---
---
<br><br>

<a name="ExponentialPrior"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class ExponentialPrior(</strong> <a href="./LaplacePrior.html">LaplacePrior</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ExponentialPrior.py target=_blank>Source</a></th></tr></thead></table>
<p>

Exponential prior distribution.

&nbsp;&nbsp;&nbsp;&nbsp; Pr( x ) = exp( -x / scale )<br>

By default scale = 1.

The domain is [0,+Inf].
In computational practice the domain is limited to about [0,36] scale units

Wrapper for
LaplacePrior( center=0, scale=scale, limits=[0, hilim] )

<b>Examples</b>

    pr = ExponentialPrior()                     # scale=1.0
    pr = ExponentialPrior( scale=5.0 )          # scale=5

<b>Attributes</b>

* scale  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; scale of the exponential<br>

<b>Attributes from Prior</b>

lowLimit, highLimit, deltaP, _lowDomain, _highDomain

Author: Do Kester.

<a name="ExponentialPrior"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>ExponentialPrior(</strong> scale=1.0, hilimit=math.inf, prior=None )
</th></tr></thead></table>
<p>

Constructor.

Parameters
scale : float
&nbsp;&nbsp;&nbsp;&nbsp; of the exponential<br>
hilimit : float
&nbsp;&nbsp;&nbsp;&nbsp; high limit<br>
prior : ExponentialPrior
&nbsp;&nbsp;&nbsp;&nbsp; prior to copy (with new scale if applicable)<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Copy the prior 

<a name="shortName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shortName(</strong> ) 
</th></tr></thead></table>
<p>
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./LaplacePrior.html">LaplacePrior</a></th></tr></thead></table>


* [<strong>domain2Unit(</strong> dval )](./LaplacePrior.md#domain2Unit)
* [<strong>unit2Domain(</strong> uval )](./LaplacePrior.md#unit2Domain)
* [<strong>result(</strong> x )](./LaplacePrior.md#result)
* [<strong>logResult(</strong> x )](./LaplacePrior.md#logResult)
* [<strong>partialLog(</strong> x )](./LaplacePrior.md#partialLog)
* [<strong>isBound(</strong> )](./LaplacePrior.md#isBound)


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
* [<strong>getIntegral(</strong> ) ](./Prior.md#getIntegral)
* [<strong>getRange(</strong> )](./Prior.md#getRange)
* [<strong>partialDomain2Unit(</strong> p )](./Prior.md#partialDomain2Unit)
* [<strong>numPartialDomain2Unit(</strong> dval )](./Prior.md#numPartialDomain2Unit)
* [<strong>numPartialLog(</strong> p )](./Prior.md#numPartialLog)
