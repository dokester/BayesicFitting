---
---
<br><br>

<a name="RadialVelocityModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class RadialVelocityModel(</strong> <a href="./NonLinearModel.html">NonLinearModel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/RadialVelocityModel.py target=_blank>Source</a></th></tr></thead></table>

Model for the radial velocity variations of a star caused by a orbiting planet.

| par | symbol | name         | description               | limits    | comment      |
|-----|--------|--------------|---------------------------|-----------|--------------|
| p<sub>0</sub> |   e    | eccentricity | of the elliptic orbit     | 0<e<1     | 0 = circular |
| p<sub>1</sub> |   a    | amplitude    | of the velocity variation |   a>0     |  | 
| p<sub>2</sub> |   P    | period       | of the velocity variation |   P>0     |  |
| p<sub>3</sub> |   T    | phase        | phase since periastron    | 0<T<2&pi; |  |
| p<sub>4</sub> | &omega;| periastron   | longitude of periastron   | 0<&omega;<2&pi; |  |

This class uses [Kepplers2ndLaw](./Kepplers2ndLaw.md) to find radius and true anomaly.

Note
The velocity of the star system is not included in this model. See example.

The parameters are initialized at [0.0, 1.0, 1.0, 0.0, 0.0].
It is a non-linear model.

<b>Attributes</b>

* keppler  :  Kepplers2ndLaw()
<br>&nbsp;&nbsp;&nbsp;&nbsp; to calculate the radius and true anomaly

<b>Examples</b>

    rv = RadialVelocityModel( )
    print( rv.npars )
    5
    rv += PolynomialModel( 0 )          # add a constant system velocity


<a name="RadialVelocityModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>RadialVelocityModel(</strong> copy=None, **kwargs )
</th></tr></thead></table>

Radial velocity model.

Number of parameters is 5

<b>Parameters</b>

* copy  :  RadialVelocityModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to copy
* fixed  :  dictionary of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; int     list if parameters to fix permanently. Default None.
<br>&nbsp;&nbsp;&nbsp;&nbsp; float   list of values for the fixed parameters.
<br>&nbsp;&nbsp;&nbsp;&nbsp; Attribute fixed can only be set in the constructor.


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>

Copy method. 
<a name="getMsini"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getMsini(</strong> stellarmass ) 
</th></tr></thead></table>
Return the mass of the exoplanet in Jupiter masses.

<b>Parameters</b>

* stellarmass  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; mass of the host star in solar masses.

<a name="baseResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseResult(</strong> xdata, params )
</th></tr></thead></table>
Returns the result of the model function.

f(x:p) = p<sub>1</sub> * ( cos( v + p<sub>4</sub> ) + p<sub>0</sub> * cos( p<sub>4</sub> ) )

where v is the true anomaly

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.


<a name="basePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePartial(</strong> xdata, params, parlist=None )
</th></tr></thead></table>
Returns the partials at the input value.

f(x:p) = p<sub>1</sub> * ( cos( v + p<sub>4</sub> ) + p<sub>0</sub> * cos( p<sub>4</sub> ) )

&nbsp; df/dp<sub>0</sub> = p<sub>1</sub> * ( - sin( v + p<sub>4</sub> ) dv/dp<sub>0</sub> + cos( p<sub>4</sub> ) )
<br>&nbsp; df/dp<sub>1</sub> = cos( v + p<sub>4</sub> ) + p<sub>0</sub> * cos( p<sub>4</sub> )
<br>&nbsp; df/dp<sub>2</sub> = - p<sub>1</sub> * sin( v + p<sub>4</sub> ) dv/dp<sub>2</sub>
<br>&nbsp; df/dp<sub>3</sub> = - p<sub>1</sub> * sin( v + p<sub>4</sub> ) dv/dp<sub>3</sub>
<br>&nbsp; df/dp<sub>4</sub> = - p<sub>1</sub> * ( sin( v + p<sub>4</sub> ) + p<sub>0</sub> * sin( p<sub>4</sub> ) )

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.
* parlist  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of indices active parameters (or None for all)


<a name="baseDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseDerivative(</strong> xdata, params )
</th></tr></thead></table>
Returns the derivative of f to x (df/dx) at the input values.

dfdx = - p<sub>1</sub> * sin( v + p<sub>4</sub> ) * dvdx

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.


<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>
Returns a string representation of the model.


<a name="baseParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseParameterUnit(</strong> k )
</th></tr></thead></table>
Return the unit of a parameter.

<b>Parameters</b>

* k  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; the kth parameter.


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./NonLinearModel.html">NonLinearModel</a></th></tr></thead></table>


* [<strong>setMixedModel(</strong> lindex )](./NonLinearModel.md#setMixedModel)
* [<strong>isMixed(</strong> )](./NonLinearModel.md#isMixed)
* [<strong>getNonLinearIndex(</strong> )](./NonLinearModel.md#getNonLinearIndex)
* [<strong>partial(</strong> xdata, param=None, useNum=False )](./NonLinearModel.md#partial)


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Model.html">Model</a></th></tr></thead></table>


* [<strong>chainLength(</strong> )](./Model.md#chainLength)
* [<strong>isNullModel(</strong> ) ](./Model.md#isNullModel)
* [<strong>isolateModel(</strong> k )](./Model.md#isolateModel)
* [<strong>addModel(</strong> model )](./Model.md#addModel)
* [<strong>subtractModel(</strong> model )](./Model.md#subtractModel)
* [<strong>multiplyModel(</strong> model )](./Model.md#multiplyModel)
* [<strong>divideModel(</strong> model )](./Model.md#divideModel)
* [<strong>pipeModel(</strong> model )](./Model.md#pipeModel)
* [<strong>appendModel(</strong> model, operation )](./Model.md#appendModel)
* [<strong>correctParameters(</strong> params )](./Model.md#correctParameters)
* [<strong>result(</strong> xdata, param=None )](./Model.md#result)
* [<strong>operate(</strong> res, pars, next )](./Model.md#operate)
* [<strong>derivative(</strong> xdata, param, useNum=False )](./Model.md#derivative)
* [<strong>selectPipe(</strong> ndim, ninter, ndout ) ](./Model.md#selectPipe)
* [<strong>pipe_0(</strong> dGd, dHdG ) ](./Model.md#pipe_0)
* [<strong>pipe_1(</strong> dGd, dHdG ) ](./Model.md#pipe_1)
* [<strong>pipe_2(</strong> dGd, dHdG ) ](./Model.md#pipe_2)
* [<strong>pipe_3(</strong> dGd, dHdG ) ](./Model.md#pipe_3)
* [<strong>pipe_4(</strong> dGdx, dHdG ) ](./Model.md#pipe_4)
* [<strong>pipe_5(</strong> dGdx, dHdG ) ](./Model.md#pipe_5)
* [<strong>pipe_6(</strong> dGdx, dHdG ) ](./Model.md#pipe_6)
* [<strong>pipe_7(</strong> dGdx, dHdG ) ](./Model.md#pipe_7)
* [<strong>pipe_8(</strong> dGdx, dHdG ) ](./Model.md#pipe_8)
* [<strong>pipe_9(</strong> dGdx, dHdG ) ](./Model.md#pipe_9)
* [<strong>shortName(</strong> ) ](./Model.md#shortName)
* [<strong>getNumberOfParameters(</strong> )](./Model.md#getNumberOfParameters)
* [<strong>numDerivative(</strong> xdata, param )](./Model.md#numDerivative)
* [<strong>numPartial(</strong> xdata, param )](./Model.md#numPartial)
* [<strong>isDynamic(</strong> ) ](./Model.md#isDynamic)
* [<strong>hasPriors(</strong> isBound=True ) ](./Model.md#hasPriors)
* [<strong>getPrior(</strong> kpar )](./Model.md#getPrior)
* [<strong>setPrior(</strong> kpar, prior=None, **kwargs )](./Model.md#setPrior)
* [<strong>getParameterName(</strong> kpar )](./Model.md#getParameterName)
* [<strong>getParameterUnit(</strong> kpar )](./Model.md#getParameterUnit)
* [<strong>getIntegralUnit(</strong> )](./Model.md#getIntegralUnit)
* [<strong>setLimits(</strong> lowLimits=None, highLimits=None )](./Model.md#setLimits)
* [<strong>getLimits(</strong> ) ](./Model.md#getLimits)
* [<strong>hasLimits(</strong> fitindex=None )](./Model.md#hasLimits)
* [<strong>unit2Domain(</strong> uvalue, kpar=None )](./Model.md#unit2Domain)
* [<strong>domain2Unit(</strong> dvalue, kpar=None )](./Model.md#domain2Unit)
* [<strong>partialDomain2Unit(</strong> dvalue )](./Model.md#partialDomain2Unit)
* [<strong>nextPrior(</strong> ) ](./Model.md#nextPrior)
* [<strong>getLinearIndex(</strong> )](./Model.md#getLinearIndex)
* [<strong>testPartial(</strong> xdata, params, silent=True )](./Model.md#testPartial)
* [<strong>strictNumericPartial(</strong> xdata, params, parlist=None ) ](./Model.md#strictNumericPartial)
* [<strong>assignDF1(</strong> partial, i, dpi ) ](./Model.md#assignDF1)
* [<strong>assignDF2(</strong> partial, i, dpi ) ](./Model.md#assignDF2)
* [<strong>strictNumericDerivative(</strong> xdata, param ) ](./Model.md#strictNumericDerivative)


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./FixedModel.html">FixedModel</a></th></tr></thead></table>


* [<strong>select(</strong> params ) ](./FixedModel.md#select)
* [<strong>selectNames(</strong> names ) ](./FixedModel.md#selectNames)
* [<strong>expand(</strong> xdata, param ) ](./FixedModel.md#expand)


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./BaseModel.html">BaseModel</a></th></tr></thead></table>


* [<strong>checkParameter(</strong> param ) ](./BaseModel.md#checkParameter)
* [<strong>checkPositive(</strong> param ) ](./BaseModel.md#checkPositive)
* [<strong>checkZeroParameter(</strong> param )](./BaseModel.md#checkZeroParameter)
* [<strong>isModifiable(</strong> ) ](./BaseModel.md#isModifiable)
* [<strong>basePrior(</strong> kpar ) ](./BaseModel.md#basePrior)
* [<strong>baseParameterName(</strong> kpar ) ](./BaseModel.md#baseParameterName)
