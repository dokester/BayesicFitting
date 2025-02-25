---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/CauchyPrior.py target=_blank>Source</a></span></div>

<a name="CauchyPrior"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class CauchyPrior(</strong> <a href="./Prior.html">Prior</a> )
</th></tr></thead></table>
<p>

Cauchy prior distribution.

    Pr( x ) =  s / ( &pi; * ( s^2 + ( x - c )^2 )<br>

By default: c = center = 0 and s = scale = 1.

It can also have a limited domain. (To be done)
By default the domain is [-Inf,+Inf].
In computational practice it is limited to [-1e16, 1e16]

domain2unit: u = arctan( ( d - c ) / s ) / pi + 0.5
unit2domain: d = tan( ( u - 0.5 ) * pi ) * s + c

<b>Examples</b>

    pr = CauchyPrior()                         # center=0, scale=1<br>
    pr = CauchyPrior( center=1.0, scale=0.5 )<br>
    pr = CauchyPrior( limits=[0,None] )        # lowlimit=0, highlimit=inf<br>
    pr = CauchyPrior( center=1, circular=3 )   # circular between 0.5 and 2.5<br>

<b>Attributes</b>

* center  :  float<br>
    center of the Cauchy prior<br>
* scale  :  float<br>
    scale of the Cauchy prior<br>

<b>Attributes from Prior</b>

lowLimit, highLimit, deltaP, _lowDomain, _highDomain

lowLimit and highLimit cannot be used in this implementation.


<a name="CauchyPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>CauchyPrior(</strong> center=0.0, scale=1, limits=None, circular=False, prior=None )
</th></tr></thead></table>
<p>

Constructor.

<b>Parameters</b>

* center  :  float<br>
    of the prior<br>
* scale  :  float<br>
    of the prior<br>
* limits  :  None or [float,float]<br>
    None    no limits are set<br>
    2 floats    lowlimit and highlimit<br>
* circular  :  bool or float<br>
    bool : y|n circular with period from limits[0] to limits[1]<br>
    float : period of circularity<br>
* prior  :  CauchyPrior<br>
    prior to copy (with new scale if applicable)<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> dval )
</th></tr></thead></table>
<p>

Return a value in [0,1] given a value within the valid domain of
a parameter for a Cauchy distribution.

domain2unit: u = arctan( ( d - c ) / s ) / pi + 0.5

<b>Parameters</b>

* dval  :  float<br>
    value within the domain of a parameter<br>


<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> uval )
</th></tr></thead></table>
<p>

Return a value within the valid domain of the parameter given a value
between [0,1] for a Cauchy distribution.

unit2domain: d = tan( ( u - 0.5 ) * pi ) * s + c

<b>Parameters</b>

* uval  :  float<br>
    value within [0,1]<br>


<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th></tr></thead></table>
<p>

Return a the result of the distribution function at x.

<b>Parameters</b>

* x  :  float<br>
    value within the domain of a parameter<br>


<a name="partialLog"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>partialLog(</strong> x )
</th></tr></thead></table>
<p>

Return partial derivative of log( Prior ) wrt parameter.

<b>Parameters</b>

* x  :  float<br>
    the value<br>


<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th></tr></thead></table>
<p>
Return true if the integral over the prior is bound. 

<a name="shortName"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>shortName(</strong> )
</th></tr></thead></table>
<p>
Return a string representation of the prior. 

<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
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
* [<strong>logResult(</strong> p ) ](./Prior.md#logResult)
* [<strong>numPartialDomain2Unit(</strong> dval )](./Prior.md#numPartialDomain2Unit)
* [<strong>numPartialLog(</strong> p )](./Prior.md#numPartialLog)
