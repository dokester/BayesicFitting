---
---
<br><br>

<a name="CauchyPrior"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class CauchyPrior(</strong> <a href="./Prior.html">Prior</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/CauchyPrior.py target=_blank>Source</a></th></tr></thead></table>

Cauchy prior distribution.

Pr( x ) =  s / ( &pi; * ( s<sup>2</sup> + ( x - c )<sup>2</sup> )

By default: c = center = 0 and s = scale = 1.

It can also have a limited domain.
By default the domain is [-Inf,+Inf].
In computational practice it is limited to [-1e16, 1e16]

&nbsp; domain2unit: 
<br>&nbsp;&nbsp;&nbsp;&nbsp; u = arctan( ( d - c ) / s ) / &pi; + 0.5
<br>&nbsp; unit2domain: 
<br>&nbsp;&nbsp;&nbsp;&nbsp; d = tan( ( u - 0.5 ) * &pi; ) * s + c

<b>Examples</b>

    pr = CauchyPrior()                         # center=0, scale=1
    pr = CauchyPrior( center=1.0, scale=0.5 )
    pr = CauchyPrior( limits=[0,None] )        # lowlimit=0, highlimit=inf
    pr = CauchyPrior( center=1, circular=3 )   # circular between 0.5 and 2.5

<b>Attributes</b>

* center  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; center of the Cauchy prior
* scale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; scale of the Cauchy prior

<b>Attributes from Prior</b>

lowLimit, highLimit, deltaP, _lowDomain, _highDomain


<a name="CauchyPrior"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>CauchyPrior(</strong> center=0.0, scale=1, limits=None, circular=False, prior=None )
</th></tr></thead></table>

Constructor.

<b>Parameters</b>

* center  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the prior
* scale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the prior
* limits  :  None or [float,float]
<br>&nbsp;&nbsp;&nbsp;&nbsp; None    no limits are set
<br>&nbsp;&nbsp;&nbsp;&nbsp; 2 floats    lowlimit and highlimit
* circular  :  bool or float
<br>&nbsp;&nbsp;&nbsp;&nbsp; bool : y|n circular with period from limits[0] to limits[1]
<br>&nbsp;&nbsp;&nbsp;&nbsp; float : period of circularity
* prior  :  CauchyPrior
<br>&nbsp;&nbsp;&nbsp;&nbsp; prior to copy (with new scale if applicable)


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>

<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> dval )
</th></tr></thead></table>
Return a value in [0,1] given a value within the valid domain of
a parameter for a Cauchy distribution.

u = arctan( ( d - c ) / s ) / &pi; + 0.5

<b>Parameters</b>

* dval  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; value within the domain of a parameter


<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> uval )
</th></tr></thead></table>
Return a value within the valid domain of the parameter given a value
between [0,1] for a Cauchy distribution.

d = tan( ( u - 0.5 ) * &pi; ) * s + c

<b>Parameters</b>

* uval  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; value within [0,1]


<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th></tr></thead></table>
Return a the result of the distribution function at x.

<b>Parameters</b>

* x  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; value within the domain of a parameter


<a name="partialLog"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialLog(</strong> x )
</th></tr></thead></table>
Return partial derivative of log( Prior ) wrt parameter.

<b>Parameters</b>

* x  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the value

<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th></tr></thead></table>

Return true if the integral over the prior is bound. 
<a name="shortName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shortName(</strong> )
</th></tr></thead></table>

Return a string representation of the prior. 
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
* [<strong>logResult(</strong> p ) ](./Prior.md#logResult)
* [<strong>numPartialDomain2Unit(</strong> dval )](./Prior.md#numPartialDomain2Unit)
* [<strong>numPartialLog(</strong> p )](./Prior.md#numPartialLog)
