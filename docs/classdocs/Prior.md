---
---
<br><br>

<a name="Prior"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Prior(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Prior.py target=_blank>Source</a></th></tr></thead></table>

Base class defining prior distributions.

Two methods need to be defined in specific priors which map
the values between [0,1] on to the domain, and vice versa
unit2Domain and domain2Unit.

&nbsp;&nbsp;&nbsp;&nbsp; u = domain2Unit( d )
<br>&nbsp;&nbsp;&nbsp;&nbsp; d = unit2Domain( u )

d is a value in the domain of the prior and u is a vlue in [0,1]

The handling of limits is relegated to this Prior class. 

&nbsp; Define
<br>&nbsp;&nbsp;&nbsp;&nbsp; umin = domain2Unit( lowLimit )
<br>&nbsp;&nbsp;&nbsp;&nbsp; urange = domain2Unit( highLimit ) - umin

&nbsp;&nbsp;&nbsp;&nbsp; u = ( domain2Unit( d ) - umin ) / urange
<br>&nbsp;&nbsp;&nbsp;&nbsp; d = unit2Domain( u * urange + umin )

Symmetric priors can be used in a circular variant; i.e.
the low and high limits are folded on each other, provided
that the limit values are the same (hence symmetric)

&nbsp;&nbsp;&nbsp;&nbsp; u = limitedDomain2Unit( d ) + 1 ) / 3
<br>&nbsp;&nbsp;&nbsp;&nbsp; d = limitedUnit2Domain( ( u * 3 ) % 1 )

The copy method is also necessary.

<b>Attributes</b>

* lowLimit  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; low limit on the Prior
* highLimit  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; high limit on the Prior
* deltaP  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; width of numerical partial derivative calculation
* circular  :  bool or float
<br>&nbsp;&nbsp;&nbsp;&nbsp; whether circular

<b>Hidden Attributes</b>

* _lowDomain  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; lower limit of the Priors possible values
* _highDomain  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; upper limit of the Priors possible values
* _umin  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; umin lowLimit in unit
* _urng  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; urange (hi-lo) in unit

<a name="Prior"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Prior(</strong> limits=None, circular=False, domain=[-math.inf,math.inf],
 prior=None )
</th></tr></thead></table>

Default constructor.

<b>Parameters</b>

* limits  :  None or list of 2 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; 2 limits resp. low and high
* circular  :  bool or float
<br>&nbsp;&nbsp;&nbsp;&nbsp; False not circular
<br>&nbsp;&nbsp;&nbsp;&nbsp; True  circular with period from limits[0] to limits[1]
<br>&nbsp;&nbsp;&nbsp;&nbsp; period of circularity
* domain  :  2 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; over which the prior is defined
* prior  :  Prior
<br>&nbsp;&nbsp;&nbsp;&nbsp; prior to copy (with new limits if applicable)

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> ) 
</th></tr></thead></table>

Return a copy 
<a name="limitedIntegral"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>limitedIntegral(</strong> center=0, circular=False, limits=None ) 
</th></tr></thead></table>
Calculate the Integral of the prior where tails are cut off
due to limits or circularity.

<b>Parameters</b>

* center  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the prior
* circular  :  bool or float
<br>&nbsp;&nbsp;&nbsp;&nbsp; bool : y|n circular with period from limits[0] to limits[1]
<br>&nbsp;&nbsp;&nbsp;&nbsp; float :period of circularity
* limits  :  None or list of 2 float/None
<br>&nbsp;&nbsp;&nbsp;&nbsp; None : no limits.
<br>&nbsp;&nbsp;&nbsp;&nbsp; 2 limits, resp low and high

<a name="setLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setLimits(</strong> limits=None )
</th></tr></thead></table>
Set limits.
It is asserted that lowLimit is smaller than highLimit.

<b>Parameters</b>

* limits  :  None or list of any combination of [None, float]
<br>&nbsp;&nbsp;&nbsp;&nbsp; None : no limit (for both or one)
<br>&nbsp;&nbsp;&nbsp;&nbsp; float : [low,high] limit

<b>Raises</b>

ValueError when low limit is larger than high limit or out of Domain


<a name="setPriorAttributes"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setPriorAttributes(</strong> limits, circular ) 
</th></tr></thead></table>
Set circular attributes.

<b>Parameters</b>

* limits  :  None or array of 2 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; defining the period
* circular  :  bool or float
<br>&nbsp;&nbsp;&nbsp;&nbsp; False   pass
<br>&nbsp;&nbsp;&nbsp;&nbsp; True    Calculate period and center from limits
<br>&nbsp;&nbsp;&nbsp;&nbsp; float   period

<a name="isCircular"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isCircular(</strong> ) 
</th></tr></thead></table>
Whether circular

<a name="limitedDomain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>limitedDomain2Unit(</strong> dval ) 
</th></tr></thead></table>
Shrink domain to value in [0,1]

<a name="limitedUnit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>limitedUnit2Domain(</strong> uval ) 
</th></tr></thead></table>
Expand value in [0,1] to domain

<a name="circularDomain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>circularDomain2Unit(</strong> dval ) 
</th></tr></thead></table>
Make domain circular in unit by shrinking: domain ==> unit ==> [1/3,2/3]

<a name="circularUnit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>circularUnit2Domain(</strong> uval ) 
</th></tr></thead></table>
Unpack circular unit to domain: [1/3,2/3] ==> unit ==> domain

<a name="unsetLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unsetLimits(</strong> )
</th></tr></thead></table>

Remove all limits. 
<a name="setAttributes"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setAttributes(</strong> limits=None, scale=None ) 
</th></tr></thead></table>
Set possible attributes for a Prior.

<b>Parameters</b>

* limits  :  float or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; [low,high] limit
* scale  :  float or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; scale factor

<a name="isOutOfLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isOutOfLimits(</strong> par )
</th></tr></thead></table>
True if the parameter is out of limits

<b>Parameters</b>

* par  :  float or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the parameter to check


<a name="checkLimit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>checkLimit(</strong> par )
</th></tr></thead></table>
Check whether the parameter is within limits.

<b>Parameters</b>

* par  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the parameter to check

<b>Raises</b>

&nbsp;&nbsp;&nbsp;&nbsp; ValueError when outside limits.


<a name="stayInLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>stayInLimits(</strong> par )
</th></tr></thead></table>
Return lower limit or upper limit when parameter is outside.

<b>Parameters</b>

* par  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the parameter to check


<a name="hasLowLimit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasLowLimit(</strong> )
</th></tr></thead></table>

Return true if the prior has its low limits set. 
<a name="hasHighLimit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasHighLimit(</strong> )
</th></tr></thead></table>

Return true if the prior has its high limits set. 
<a name="hasLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasLimits(</strong> )
</th></tr></thead></table>

Return true if it has any limits. 
<a name="getLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLimits(</strong> )
</th></tr></thead></table>

Return the limits. 
<a name="getIntegral"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getIntegral(</strong> ) 
</th></tr></thead></table>
Return the integral of the prior over the valid range.

Default: 1.0 (for bound priors)

<a name="getRange"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getRange(</strong> )
</th></tr></thead></table>

Return the range. 
<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> dval )
</th></tr></thead></table>
Return a value in [0,1] given a value within the valid domain of
a parameter for a distribution.

<b>Parameters</b>

* dval  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; value within the domain of a parameter


<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> uval )
</th></tr></thead></table>
Return a value within the valid domain of the parameter given a value
between [0,1] for a distribution.

<b>Parameters</b>

* uval  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; value within [0,1]


<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> p )
</th></tr></thead></table>
Return value of the Prior at a given value.

If result is not defined, fall back to numerical derivative of Domain2Unit.

<b>Parameters</b>

* p  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the value


<a name="partialDomain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialDomain2Unit(</strong> p )
</th></tr></thead></table>
Return the derivative of Domain2Unit, aka the result of the distribution at p

<b>Parameters</b>

* p  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the value


<a name="logResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logResult(</strong> p ) 
</th></tr></thead></table>
Return the log of the result; -inf when p == 0.

<b>Parameters</b>

* p  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the value


<a name="numPartialDomain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>numPartialDomain2Unit(</strong> dval )
</th></tr></thead></table>
Return a the numeric derivate of the domain2Unit function to dval.

<b>Parameters</b>

* dval  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; value within the domain of a parameter


<a name="partialLog"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialLog(</strong> p )
</th></tr></thead></table>
Return partial derivative of log( Prior ) wrt parameter.
default numPartialLog

<b>Parameters</b>

* p  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the value


<a name="numPartialLog"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>numPartialLog(</strong> p )
</th></tr></thead></table>
Return the numeric partial derivative of log( Prior ) wrt parameter.
<b>Parameters</b>

* p  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the value


<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th></tr></thead></table>

Return true if the integral over the prior is bound. 
