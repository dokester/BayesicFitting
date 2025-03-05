---
---
<br><br>

<a name="LaplacePrior"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class LaplacePrior(</strong> <a href="./Prior.html">Prior</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/LaplacePrior.py target=_blank>Source</a></th></tr></thead></table>
<p>

Laplace prior distribution.

&nbsp;&nbsp;&nbsp;&nbsp; Pr( x ) = 1 / ( 2 s ) exp( - |x - c| / s )<br>

By default: c = center = 0.0 and s = scale = 1.

It can also have a limited domain.
By default the domain is [-Inf,+Inf].
In computational practice the domain is limited to about [-36,36] scale units

Equivalent to a double-sided exponential prior

domain2unit: u = 0.5 * exp( ( d - c ) / scale )             if d < c
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1.0 - 0.5 * exp( ( c - d ) / scale )       otherwise<br>
unit2domain: d = c + log( 2 * u ) * scale                   if u < 0.5
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; c - log( 2 * ( 1 - u ) ) * scale           otherwise<br>

<b>Examples</b>

    pr = LaplacePrior()                         # center=0, scale=1
    pr = LaplacePrior( center=1.0, scale=0.5 )
    pr = LaplacePrior( limits=[0,None] )        # limites to values >= 0
    pr = LaplacePrior( center=1, circular=3 )   # circular between 0.5 and 2.5

<b>Attributes</b>

* center  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; center of the Laplace prior<br>
* scale  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; scale of the Laplace prior<br>

<b>Attributes from Prior</b>

lowLimit, highLimit, deltaP, _lowDomain, _highDomain

lowLimit and highLimit cannot be used in this implementation.


<a name="LaplacePrior"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>LaplacePrior(</strong> center=0.0, scale=1.0, limits=None, circular=False, prior=None )
</th></tr></thead></table>
<p>

Constructor.

<b>Parameters</b>

* center  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; of the prior<br>
* scale  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; of the prior<br>
* limits  :  None or list of 2 float/None<br>
&nbsp;&nbsp;&nbsp;&nbsp; None : no limits.<br>
&nbsp;&nbsp;&nbsp;&nbsp; 2 limits, resp low and high<br>
* circular  :  bool or float<br>
&nbsp;&nbsp;&nbsp;&nbsp; bool : y|n circular with period from limits[0] to limits[1]<br>
&nbsp;&nbsp;&nbsp;&nbsp; float :period of circularity<br>
* prior  :  LaplacePrior<br>
&nbsp;&nbsp;&nbsp;&nbsp; prior to copy (with new scale if applicable)<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> dval )
</th></tr></thead></table>
<p>

Return a value in [0,1] given a value within the valid domain of
a parameter for a Laplace distribution.

domain2unit: u = 0.5 * exp( ( d - c ) / s ) if d < c else
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1.0 - 0.5 * exp( ( c - d ) / s )<br>

<b>Parameters</b>

* dval  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; value within the domain of a parameter<br>


<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> uval )
</th></tr></thead></table>
<p>

Return a value within the valid domain of the parameter given a value
between [0,1] for a Laplace distribution.

unit2domain: d = c + log( 2 * u ) * scale if u < 0.5 else
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; c - log( 2 * ( 1 - u ) ) * scale;<br>

<b>Parameters</b>

* uval  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; value within [0,1]<br>


<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th></tr></thead></table>
<p>

Return a the result of the distribution function at x.

<b>Parameters</b>

* x  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; value within the domain of a parameter<br>


<a name="logResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logResult(</strong> x )
</th></tr></thead></table>
<p>

Return a the log of the result of the distribution function to p.

<b>Parameters</b>

* x  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; value within the domain of a parameter<br>


<a name="partialLog"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialLog(</strong> x )
</th></tr></thead></table>
<p>

Return partial derivative of log( Prior ) wrt parameter.

<b>Parameters</b>

* x  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; the value<br>


<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th></tr></thead></table>
<p>
Return true if the integral over the prior is bound. 

<a name="shortName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shortName(</strong> ) 
</th></tr></thead></table>
<p>
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
