---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/SineDriftModel.py target=_blank>Source</a></span></div>

<a name="SineDriftModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class SineDriftModel(</strong> <a href="./NonLinearModel.html">NonLinearModel</a> )
</th></tr></thead></table>
<p>

Sinusoidal Model with drifting frequency.

    f( x:p ) = p_1 * cos( phi ) + p_2 * sin( phi )<br>
       phi = 2 * pi * x * ( p_0 + x * p_3 )<br>

where p_0 = frequency, p_3 = is the drift in frequency,
      p_1 = amplitude cosine and p_2 = amplitude sine.<br>
As always x = input.

The parameters are initialized at {1.0, 1.0, 1.0, 0.0}. It is a non-linear model.

<b>Examples</b>

    sine = SineDriftModel( )<br>
    print( sine.npchain )<br>
    pars = [0.1,0,1,0.0]<br>
    sine.parameters = pars<br>
    print( sine( numpy.arange( 101, dtype=float ) ) )     # 10 sine periods, no drift<br>
    pars = [0.1,0,1,0.001]<br>
    sine.parameters = pars<br>
    print( sine( numpy.arange( 101, dtype=float ) ) )     # 10 sine periods, drifting<br>


<b>Attributes</b>

    No attributes of its own.<br>

<b>Attributes from Model</b>

    npchain, parameters, stdevs, xUnit, yUnit<br>

<b>Attributes from FixedModel</b>

    npmax, fixed, parlist, mlist<br>

<b>Attributes from BaseModel</b>

    npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames<br>


<a name="SineDriftModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>SineDriftModel(</strong> copy=None, **kwargs )
</th></tr></thead></table>
<p>

Sinusiodal model with drifting frequency.

Number of parameters is 4.

<b>Parameters</b>

* copy  :  SineDriftModel<br>
    to be copied<br>
* fixed  :  dictionary of {int:float}<br>
    int     list if parameters to fix permanently. Default None.<br>
    float   list of values for the fixed parameters.<br>
    Attribute fixed can only be set in the constructor.<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Copy method. 

<a name="baseResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>baseResult(</strong> xdata, params )
</th></tr></thead></table>
<p>

Returns the result of the model function.

<b>Parameters</b>

* xdata  :  array_like<br>
    values at which to calculate the result<br>
* params  :  array_like<br>
    values for the parameters.<br>


<a name="baseDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>baseDerivative(</strong> xdata, params )
</th></tr></thead></table>
<p>

Returns the derivative of f to x (df/dx) at the input values.

<b>Parameters</b>

* xdata  :  array_like<br>
    values at which to calculate the result<br>
* params  :  array_like<br>
    values for the parameters.<br>


<a name="basePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>basePartial(</strong> xdata, params, parlist=None )
</th></tr></thead></table>
<p>

Returns the partials at the input values.

<b>Parameters</b>

* xdata  :  array_like<br>
    values at which to calculate the result<br>
* params  :  array_like<br>
    values for the parameters.<br>
* parlist  :  array_like<br>
    list of indices active parameters (or None for all)<br>


<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>
<p>

Returns a string representation of the model.


<a name="baseParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>baseParameterUnit(</strong> k )
</th></tr></thead></table>
<p>

Return the name of a parameter.

<b>Parameters</b>

* k  :  int<br>
    the kth parameter.<br>


<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./NonLinearModel.html">NonLinearModel</a></th></tr></thead></table>


* [<strong>setMixedModel(</strong> lindex )](./NonLinearModel.md#setMixedModel)
* [<strong>isMixed(</strong> )](./NonLinearModel.md#isMixed)
* [<strong>getNonLinearIndex(</strong> )](./NonLinearModel.md#getNonLinearIndex)
* [<strong>partial(</strong> xdata, param=None, useNum=False )](./NonLinearModel.md#partial)


<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
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


<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./FixedModel.html">FixedModel</a></th></tr></thead></table>


* [<strong>select(</strong> params ) ](./FixedModel.md#select)
* [<strong>selectNames(</strong> names ) ](./FixedModel.md#selectNames)
* [<strong>expand(</strong> xdata, param ) ](./FixedModel.md#expand)


<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./BaseModel.html">BaseModel</a></th></tr></thead></table>


* [<strong>checkParameter(</strong> param ) ](./BaseModel.md#checkParameter)
* [<strong>checkPositive(</strong> param ) ](./BaseModel.md#checkPositive)
* [<strong>checkZeroParameter(</strong> param )](./BaseModel.md#checkZeroParameter)
* [<strong>isModifiable(</strong> ) ](./BaseModel.md#isModifiable)
* [<strong>basePrior(</strong> kpar ) ](./BaseModel.md#basePrior)
* [<strong>baseParameterName(</strong> kpar ) ](./BaseModel.md#baseParameterName)
