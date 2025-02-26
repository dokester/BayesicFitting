---
---
<br><br><br>

<a name="Prior"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Prior(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Prior.py target=_blank>Source</a></th></tr></thead></table>
<p>

Base class defining prior distributions.

Two methods need to be defined in specific priors which map
the values between [0,1] on to the domain, and vice versa
unit2Domain and domain2Unit.

    u = domain2Unit( d )<br>
    d = unit2Domain( u )<br>

d is a value in the domain of the prior and u is a vlue in [0,1]

The handling of limits is relegated to this Prior class. Define
    _umin = domain2Unit( lowLimit )<br>
    _urng = domain2Unit( highLimit ) - umin<br>

    u = ( domain2Unit( d ) - umin ) / urange<br>
    d = unit2Domain( u * urange + umin )<br>

Symmetric priors can be used in a circular variant; i.e.
the low and high limits are folded on each other, provided
that the limit values are the same (hence symmetric)

    u = limitedDomain2Unit( d ) + 1 ) / 3<br>
    d = limitedUnit2Domain( ( u * 3 ) % 1 )<br>

The copy method is also necessary.

<b>Attributes</b>

* lowLimit  :  float<br>
    low limit on the Prior<br>
* highLimit  :  float<br>
    high limit on the Prior<br>
* deltaP  :  float<br>
    width of numerical partial derivative calculation<br>
* circular  :  bool or float<br>
    whether circular<br>

<b>Hidden Attributes</b>

* _lowDomain  :  float<br>
    lower limit of the Priors possible values<br>
* _highDomain  :  float<br>
    upper limit of the Priors possible values<br>
* _umin  :  float<br>
    umin lowLimit in unit<br>
* _urng  :  float<br>
    urange (hi-lo) in unit

<a name="Prior"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Prior(</strong> limits=None, circular=False, domain=[-math.inf,math.inf],
 prior=None )
</th></tr></thead></table>
<p>

Default constructor.

<b>Parameters</b>

* limits  :  None or list of 2 floats<br>
    2 limits resp. low and high<br>
* circular  :  bool or float<br>
    False not circular<br>
    True  circular with period from limits[0] to limits[1]<br>
    period of circularity<br>
* domain  :  2 floats<br>
    over which the prior is defined<br>
* prior  :  Prior<br>
    prior to copy (with new limits if applicable)

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> ) 
</th></tr></thead></table>
<p>
Return a copy 

<a name="limitedIntegral"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>limitedIntegral(</strong> center=0, circular=False, limits=None ) 
</th></tr></thead></table>
<p>

Calculate the Integral of the prior where tails are cut off
due to limits or circularity.

<b>Parameters</b>

* center  :  float<br>
    of the prior<br>
* circular  :  bool or float<br>
    bool : y|n circular with period from limits[0] to limits[1]<br>
    float :period of circularity<br>
* limits  :  None or list of 2 float/None<br>
    None : no limits.<br>
    2 limits, resp low and high

<a name="setLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setLimits(</strong> limits=None )
</th></tr></thead></table>
<p>

Set limits.
It is asserted that lowLimit is smaller than highLimit.

<b>Parameters</b>

* limits  :  None or list of any combination of [None, float]<br>
    None : no limit (for both or one)<br>
    float : [low,high] limit<br>

<b>Raises</b>

ValueError when low limit is larger than high limit or out of Domain


<a name="setPriorAttributes"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setPriorAttributes(</strong> limits, circular ) 
</th></tr></thead></table>
<p>

Set circular attributes.

<b>Parameters</b>

* limits  :  None or array of 2 floats<br>
    defining the period<br>
* circular  :  bool or float<br>
    False   pass<br>
    True    Calculate period and center from limits<br>
    float   period

<a name="isCircular"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isCircular(</strong> ) 
</th></tr></thead></table>
<p>

Whether circular

<a name="limitedDomain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>limitedDomain2Unit(</strong> dval ) 
</th></tr></thead></table>
<p>

Shrink domain to value in [0,1]

<a name="limitedUnit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>limitedUnit2Domain(</strong> uval ) 
</th></tr></thead></table>
<p>

Expand value in [0,1] to domain

<a name="circularDomain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>circularDomain2Unit(</strong> dval ) 
</th></tr></thead></table>
<p>

Make domain circular in unit by shrinking: domain ==> unit ==> [1/3,2/3]

<a name="circularUnit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>circularUnit2Domain(</strong> uval ) 
</th></tr></thead></table>
<p>

Unpack circular unit to domain: [1/3,2/3] ==> unit ==> domain

<a name="unsetLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unsetLimits(</strong> )
</th></tr></thead></table>
<p>
Remove all limits. 

<a name="setAttributes"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setAttributes(</strong> limits=None, scale=None ) 
</th></tr></thead></table>
<p>

Set possible attributes for a Prior.

<b>Parameters</b>

* limits  :  float or None<br>
    [low,high] limit<br>
* scale  :  float or None<br>
    scale factor

<a name="isOutOfLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isOutOfLimits(</strong> par )
</th></tr></thead></table>
<p>

True if the parameter is out of limits

<b>Parameters</b>

* par  :  float or array_like<br>
    the parameter to check<br>


<a name="checkLimit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>checkLimit(</strong> par )
</th></tr></thead></table>
<p>

Check whether the parameter is within limits.

<b>Parameters</b>

* par  :  float<br>
    the parameter to check<br>

<b>Raises</b>

    ValueError when outside limits.<br>


<a name="stayInLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>stayInLimits(</strong> par )
</th></tr></thead></table>
<p>

Return lower limit or upper limit when parameter is outside.

<b>Parameters</b>

* par  :  float<br>
    the parameter to check<br>


<a name="hasLowLimit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasLowLimit(</strong> )
</th></tr></thead></table>
<p>
Return true if the prior has its low limits set. 

<a name="hasHighLimit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasHighLimit(</strong> )
</th></tr></thead></table>
<p>
Return true if the prior has its high limits set. 

<a name="hasLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasLimits(</strong> )
</th></tr></thead></table>
<p>
Return true if it has any limits. 

<a name="getLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLimits(</strong> )
</th></tr></thead></table>
<p>
Return the limits. 

<a name="getIntegral"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getIntegral(</strong> ) 
</th></tr></thead></table>
<p>

Return the integral of the prior over the valid range.

Default: 1.0 (for bound priors)

<a name="getRange"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getRange(</strong> )
</th></tr></thead></table>
<p>
Return the range. 

<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> dval )
</th></tr></thead></table>
<p>

Return a value in [0,1] given a value within the valid domain of
a parameter for a distribution.

<b>Parameters</b>

* dval  :  float<br>
    value within the domain of a parameter<br>


<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> uval )
</th></tr></thead></table>
<p>

Return a value within the valid domain of the parameter given a value
between [0,1] for a distribution.

<b>Parameters</b>

* uval  :  float<br>
    value within [0,1]<br>


<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> p )
</th></tr></thead></table>
<p>

Return value of the Prior at a given value.

If result is not defined, fall back to numerical derivative of Domain2Unit.

<b>Parameters</b>

* p  :  float<br>
    the value<br>


<a name="partialDomain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialDomain2Unit(</strong> p )
</th></tr></thead></table>
<p>

Return the derivative of Domain2Unit, aka the result of the distribution at p

<b>Parameters</b>

* p  :  float<br>
    the value<br>


<a name="logResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logResult(</strong> p ) 
</th></tr></thead></table>
<p>

Return the log of the result; -inf when p == 0.

<b>Parameters</b>

* p  :  float<br>
    the value<br>


<a name="numPartialDomain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>numPartialDomain2Unit(</strong> dval )
</th></tr></thead></table>
<p>

Return a the numeric derivate of the domain2Unit function to dval.

<b>Parameters</b>

* dval  :  float<br>
    value within the domain of a parameter<br>


<a name="partialLog"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialLog(</strong> p )
</th></tr></thead></table>
<p>

Return partial derivative of log( Prior ) wrt parameter.
default numPartialLog

<b>Parameters</b>

* p  :  float<br>
    the value<br>


<a name="numPartialLog"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>numPartialLog(</strong> p )
</th></tr></thead></table>
<p>

Return the numeric partial derivative of log( Prior ) wrt parameter.
<b>Parameters</b>

* p  :  float<br>
    the value<br>


<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th></tr></thead></table>
<p>
Return true if the integral over the prior is bound. 

