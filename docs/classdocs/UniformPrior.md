---
---
<br><br>

<a name="UniformPrior"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class UniformPrior(</strong> <a href="./Prior.html">Prior</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformPrior.py target=_blank>[source]</a></th></tr></thead></table>
<p>

Uniform prior distribution, for location parameters.

A uniform prior is a improper prior ( i.e. its integral is unbound ).
Because of that it always needs limits, low and high, such that
-Inf < low < high < +Inf.

&nbsp;&nbsp;&nbsp;&nbsp; Pr( x ) = 1 / ( high - low )    if low < x < high
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0                     elsewhere

domain2Unit: 
<br>&nbsp;&nbsp;&nbsp;&nbsp; u = ( d - lo ) / range
unit2Domain: 
<br>&nbsp;&nbsp;&nbsp;&nbsp; d = u * range + lo

<b>Examples</b>

    pr = UniformPrior()                                 # unbound prior
    pr = UniformPrior( limits=[0,10] )                  # limited to the range [0,10]
    pr = UniformPrior( circular=math.pi )               # circular between 0 and pi
    pr = UniformPrior( limits=[2,4], circular=True )    # circular between 2 and 4

<b>Attributes</b>

* _range  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; highlimit - lowlimit

<b>Attributes from Prior</b>

lowLimit, highLimit, deltaP, _lowDomain, _highDomain



<a name="UniformPrior"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>UniformPrior(</strong> limits=None, circular=False, prior=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformPrior.py#L69-L84 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

<b>Parameters</b>

* limits  :  None or [float,float]
<br>&nbsp;&nbsp;&nbsp;&nbsp; None    no limits are set
<br>&nbsp;&nbsp;&nbsp;&nbsp; 2 floats    lowlimit and highlimit
* circular  :  bool or float
<br>&nbsp;&nbsp;&nbsp;&nbsp; True : circular with period from limits[0] to limits[1]
<br>&nbsp;&nbsp;&nbsp;&nbsp; float : period of circularity
* prior  :  UniformPrior
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be copied

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformPrior.py#L86-L88 target=_blank>[source]</a></th></tr></thead></table>

Return a (deep) copy of itself. 
<a name="getIntegral"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getIntegral(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformPrior.py#L90-L94 target=_blank>[source]</a></th></tr></thead></table>
Return integral of UniformPrior from lowLimit to highLimit.

<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> dval )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformPrior.py#L96-L108 target=_blank>[source]</a></th></tr></thead></table>
Return the dval as uval

In Prior.limitedDomain2Unit the dval is transformed into a uval

<b>Parameters</b>

* dval  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; value within the domain of a parameter


<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> uval )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformPrior.py#L110-L122 target=_blank>[source]</a></th></tr></thead></table>
Return the uval as dval

In Prior.limitedUnit2Domain the uval is transformed into a dval

<b>Parameters</b>

* uval  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; value within [0,1]


<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformPrior.py#L124-L143 target=_blank>[source]</a></th></tr></thead></table>
Return a the result of the distribution function at x.

<b>Parameters</b>

* x  :  float or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; value within the domain of a parameter


<a name="partialLog"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialLog(</strong> p )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformPrior.py#L145-L158 target=_blank>[source]</a></th></tr></thead></table>
Return partial derivative of log( Prior ) wrt parameter.

<b>Parameters</b>

* p  :  float or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the value


<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformPrior.py#L160-L162 target=_blank>[source]</a></th></tr></thead></table>

Return true if the integral over the prior is bound. 
<a name="shortName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shortName(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformPrior.py#L164-L168 target=_blank>[source]</a></th></tr></thead></table>

Return a string representation of the prior. 
Endline #L170
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
