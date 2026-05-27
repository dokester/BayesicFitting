---
---
<br><br>

<a name="UniformRatioPrior"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class UniformRatioPrior(</strong> <a href="./Prior.html">Prior</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformRatioPrior.py target=_blank>[source]</a></th></tr></thead></table>
<p>

Distribution of the ratio of two uniform distributed, positive variables.

A uniform ratio prior is a proper prior.
<br>&nbsp;&nbsp;&nbsp;&nbsp; Pr( x ) = 0         if x < 0
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0.5       if 0 < x < 1
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0.5/x**2  if x > 1

domain2Unit.
<br>&nbsp;&nbsp;&nbsp;&nbsp; u = 0.5 d       if 0 < d < 1
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1 - 0.5/d   if d > 1

unit2Domain.
<br>&nbsp;&nbsp;&nbsp;&nbsp; d = 2 u         if 0   < u < 0.5
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1/2(1-u)    if 0.5 < u < 1

The keyword "circular" does not apply to this prior.

<b>Examples</b>

    pr = UniformRatioPrior()

<b>Attributes from Prior</b><br>
lowLimit, highLimit, deltaP, _lowDomain, _highDomain



<a name="UniformRatioPrior"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>UniformRatioPrior(</strong> range=None, median=1.0, limits=None, prior=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformRatioPrior.py#L71-L94 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

<b>Parameters</b><br>
* range  :  None or float
<br>&nbsp;&nbsp;&nbsp;&nbsp; set limits tp [1/range, range]
* median  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; median point of the ratio
* limits  :  None or [float,float]
<br>&nbsp;&nbsp;&nbsp;&nbsp; None    no limits are set
<br>&nbsp;&nbsp;&nbsp;&nbsp; 2 floats    lowlimit and highlimit
* prior  :  UniformRatioPrior
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be copied

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformRatioPrior.py#L96-L100 target=_blank>[source]</a></th></tr></thead></table>
Return a (deep) copy of itself. 

<a name="getIntegral"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getIntegral(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformRatioPrior.py#L102-L106 target=_blank>[source]</a></th></tr></thead></table>
Return integral of UniformRatioPrior from lowLimit to highLimit.

<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> dval )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformRatioPrior.py#L108-L125 target=_blank>[source]</a></th></tr></thead></table>
Return a value in [0,1] given a positive ratio value

<b>Parameters</b><br>
* dval  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; value within the domain of a parameter


<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> uval )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformRatioPrior.py#L127-L146 target=_blank>[source]</a></th></tr></thead></table>
Return a ratio value given a value in [0,1].

<b>Parameters</b><br>
* uval  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; value within [0,1]


<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformRatioPrior.py#L148-L162 target=_blank>[source]</a></th></tr></thead></table>
Return a the result of the distribution function at x.

<b>Parameters</b><br>
* x  :  float or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; value within the domain of a parameter


<a name="logResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logResult(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformRatioPrior.py#L164-L180 target=_blank>[source]</a></th></tr></thead></table>
Return a the log of the result of the distribution function at x.

<b>Parameters</b><br>
* x  :  float or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; value within the domain of a parameter


<a name="partialLog"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialLog(</strong> p )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformRatioPrior.py#L182-L194 target=_blank>[source]</a></th></tr></thead></table>
Return partial derivative of log( Prior ) wrt parameter.

<b>Parameters</b><br>
* p  :  float or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the value


<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformRatioPrior.py#L196-L200 target=_blank>[source]</a></th></tr></thead></table>
Return true if the integral over the prior is bound.  

<a name="shortName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shortName(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformRatioPrior.py#L202-L208 target=_blank>[source]</a></th></tr></thead></table>
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
* [<strong>getRange(</strong> )](./Prior.md#getRange)
* [<strong>partialDomain2Unit(</strong> p )](./Prior.md#partialDomain2Unit)
* [<strong>numPartialDomain2Unit(</strong> dval )](./Prior.md#numPartialDomain2Unit)
* [<strong>numPartialLog(</strong> p )](./Prior.md#numPartialLog)
