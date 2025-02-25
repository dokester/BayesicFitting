---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/JeffreysPrior.py target=_blank>Source</a></span></div>

<a name="JeffreysPrior"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class JeffreysPrior(</strong> <a href="./Prior.html">Prior</a> )
</th></tr></thead></table>
<p>

Jeffreys prior distribution, for scale-like parameters.
Jeffreys prior is a improper prior ( i.e. its integral is unbound ).
Because of that it always needs limits, low and high, such that
0 < low < high < +Inf.

    Pr( x ) = 1.0 / ( x * norm )    if low < x < high<br>
              0.0                   otherwise<br>

where norm = log( high ) - log( low )

No limits are set by default.

domain2unit: u = ( log( d ) - log( lo ) ) / ( log( hi ) - log( lo ) );
unit2domain: d = exp( u * ( log( hi ) - log( lo ) ) + log( lo ) );

<b>Examples</b>

    pr = JeffreysPrior()                       # unbound prior<br>
    pr = JeffreysPrior( limits=[0.1,1.0] )     # limited to the range [0.1,1.0]<br>


<b>Hidden Attributes</b>

* _logLo  :  float<br>
    log( lowLimit )<br>
* _norm  :  float<br>
    log( highLimit / lowLimit )<br>

<b>Attributes from Prior</b>

lowLimit, highLimit, deltaP, _lowDomain, _highDomain

The default of lowLimit and _lowDomain is zero.


<a name="JeffreysPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>JeffreysPrior(</strong> limits=None, prior=None )
</th></tr></thead></table>
<p>

Default constructor.

<b>Parameters</b>

* limits  :  list of 2 floats<br>
    2 limits resp. low and high<br>
* prior  :  JeffreysPrior<br>
    prior to copy (with new limits if applicable)

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
<a name="getIntegral"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>getIntegral(</strong> ) 
</th></tr></thead></table>
<p>

Return the integral of JeffreysPrior from lowLimit to highLimit.

<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> dval )
</th></tr></thead></table>
<p>

Return a value in [0,1] given a value within the valid domain of
a parameter for a Jeffreys distribution.

<b>Parameters</b>

* dval  :  float<br>
    value within the domain of a parameter<br>


<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> uval )
</th></tr></thead></table>
<p>

Return a value within the valid domain of the parameter given a value
between [0,1] for a Jeffreys distribution.

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
<strong>partialLog(</strong> p )
</th></tr></thead></table>
<p>

Return partial derivative of log( Prior ) wrt parameter.

<b>Parameters</b>

* p  :  float<br>
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
* [<strong>getRange(</strong> )](./Prior.md#getRange)
* [<strong>partialDomain2Unit(</strong> p )](./Prior.md#partialDomain2Unit)
* [<strong>logResult(</strong> p ) ](./Prior.md#logResult)
* [<strong>numPartialDomain2Unit(</strong> dval )](./Prior.md#numPartialDomain2Unit)
* [<strong>numPartialLog(</strong> p )](./Prior.md#numPartialLog)
