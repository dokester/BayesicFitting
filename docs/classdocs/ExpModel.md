---
---
<br><br>

<a name="ExpModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class ExpModel(</strong> <a href="./NonLinearModel.html">NonLinearModel</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ExpModel.py target=_blank>[source]</a></th></tr></thead></table>
<p>

Exponential Model.

&nbsp; f( x:p ) = p<sub>0</sub> * exp( p<sub>1</sub> * x )

&nbsp; where 
<br>&nbsp;&nbsp;&nbsp;&nbsp; p<sub>0</sub> = amplitude
<br>&nbsp;&nbsp;&nbsp;&nbsp; p<sub>1</sub> = slope
<br>&nbsp; As always 
<br>&nbsp;&nbsp;&nbsp;&nbsp; x = input.

The parameters are initialized at [1.0, -1.0]. It is a non-linear model.

Beware of a positive 2nd parameter; when positive the model is going off
to Infinity very quickly.

When decay is True the model changes into a decay model

&nbsp; f( x:p ) = p<sub>0</sub> * exp( - p<sub>1</sub> * x )

The parameters are initialized at 1.0, 1.0.

<b>Attributes</b>

* sign  :  [-1,1]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Whether decay is True or False.

<b>Attributes from Model</b>

&nbsp;&nbsp;&nbsp;&nbsp; npchain, parameters, stdevs, xUnit, yUnit

<b>Attributes from FixedModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist

<b>Attributes from BaseModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames

<b>Examples</b>

    em = ExpModel( )
    print( em.getNumberOfParameters( ) )
    2

Author  Do Kester


<a name="ExpModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>ExpModel(</strong> decay=False, copy=None, **kwargs )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ExpModel.py#L83-L112 target=_blank>[source]</a></th></tr></thead></table>

Exponential model.
<br>
Number of parameters is 2.

<b>Parameters</b>

* decay  :  boolean
<br>&nbsp;&nbsp;&nbsp;&nbsp; changes sign of parameter[1]
* copy  :  ExpModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be copied
* fixed  :  None or dictionary of {int:float|Model}
<br>&nbsp;&nbsp;&nbsp;&nbsp; int         index of parameter to fix permanently.
<br>&nbsp;&nbsp;&nbsp;&nbsp; float|Model values for the fixed parameters.
<br>&nbsp;&nbsp;&nbsp;&nbsp; Attribute fixed can only be set in the constructor.
<br>&nbsp;&nbsp;&nbsp;&nbsp; See: [FixedModel](./FixedModel.md)


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ExpModel.py#L114-L116 target=_blank>[source]</a></th></tr></thead></table>

Copy method. 
<a name="baseResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseResult(</strong> xdata, params )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ExpModel.py#L118-L130 target=_blank>[source]</a></th></tr></thead></table>
Returns the result of the model function.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; value at which to calculate the result
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters


<a name="basePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePartial(</strong> xdata, params, parlist=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ExpModel.py#L132-L160 target=_blank>[source]</a></th></tr></thead></table>
Returns the partials at the input value.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; value at which to calculate the result
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters
* parlist  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of indices active parameters (or None for all)


<a name="baseDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseDerivative(</strong> xdata, params )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ExpModel.py#L162-L174 target=_blank>[source]</a></th></tr></thead></table>
Returns the derivative df/dx at the input value.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; value at which to calculate the result
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters


<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ExpModel.py#L176-L181 target=_blank>[source]</a></th></tr></thead></table>
Returns a string representation of the model.


<a name="baseParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseParameterUnit(</strong> k )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ExpModel.py#L183-L191 target=_blank>[source]</a></th></tr></thead></table>
Return the unit of the indicated parameter.
Parameters: k    parameter number.


Endline #L193
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
