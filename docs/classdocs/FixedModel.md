---
---
<br><br>

<a name="FixedModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class FixedModel(</strong> <a href="./BaseModel.html">BaseModel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/FixedModel.py target=_blank>Source</a></th></tr></thead></table>
<p>

A FixedModel is a BaseModel where some parameters are permanently fixed.

A parameter can be fixed either with a constant float value or more
dynamically, with another Model. The parameters of this latter model
also appear as parameters of the FixedModel.

The methods result (f(x:p)) and partial (df/dp) are calculated
in here.
Unfortunately the methods derivative (df/dx) is model dependent.
It is reset to numDerivative.

<b>Examples</b>

    m1 = PolynomialModel( 1 )
    m1 += SineModel()
    print( m1.npchain )         # number of params: 2 + 3
5
    fixed = { 0: 1.0, 1: m1 }
    em = EtalonModel( fixed=fixed )
    print( em.npbase, em.npmax, em.npchain )          # ( 4 - 2 ) + 5
7 9 7
    print( em )

<b>Attributes</b>

* npmax  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; maximum number of parameters of the simple (not-fixed) model<br>
* fixed  :  dictionary of {int:float|Model}<br>
&nbsp;&nbsp;&nbsp;&nbsp; int     index of parameter to fix permanently. Default None.<br>
&nbsp;&nbsp;&nbsp;&nbsp; float   value for the fixed parameter.<br>
&nbsp;&nbsp;&nbsp;&nbsp; Model   model to replace the parameter<br>
&nbsp;&nbsp;&nbsp;&nbsp; Attribute fixed can only be set in the constructor.<br>
* parlist  :  array_like or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of active (not-fixed) indices. None is all.<br>
* mlist  :  list of Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of parameter indices which are replaced by a Model in fixed.<br>

<b>Attributes from BaseModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames<br>

Author       Do Kester


<a name="FixedModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>FixedModel(</strong> nparams=0, ndim=1, copy=None, fixed=None,
 names=None, **kwargs ) 
</th></tr></thead></table>
<p>

FixedModel Constructor.

<b>Parameters</b>

* nparams  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; Number of parameters in the model (default: 0)<br>
* ndim  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; Number of dimensions of the input (default: 1)<br>
* copy  :  BaseModel<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be copied<br>
* fixed  :  dictionary of {int:float|Model}<br>
&nbsp;&nbsp;&nbsp;&nbsp; int     index of parameter to fix permanently. Default None.<br>
&nbsp;&nbsp;&nbsp;&nbsp; float   value for the fixed parameter.<br>
&nbsp;&nbsp;&nbsp;&nbsp; Model   model to replace the parameter<br>
&nbsp;&nbsp;&nbsp;&nbsp; Attribute fixed can only be set in the constructor.<br>
* names  :  list of string<br>
&nbsp;&nbsp;&nbsp;&nbsp; names for the parameters<br>
* kwargs for [BaseModel](./BaseModel.md)  : <br>
&nbsp;&nbsp;&nbsp;&nbsp; posIndex, nonZero<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> ) 
</th></tr></thead></table>
<p>
Return a copy. 

<a name="select"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>select(</strong> params ) 
</th></tr></thead></table>
<p>

Select the relevant parameters and store them.

<b>Parameters</b>

* params  :  array of float<br>
    parameters of the head model

<a name="selectNames"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>selectNames(</strong> names ) 
</th></tr></thead></table>
<p>

Select the relevant parameter names and store them.

<b>Parameters</b>

* names  :  list of string<br>
    parameter names of the head model

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> xdata, param )
</th></tr></thead></table>
<p>

Returns the result calculated at the xdatas.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.<br>


<a name="expand"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>expand(</strong> xdata, param ) 
</th></tr></thead></table>
<p>

Returns a complete list of parameters, where the fixed parameters
have been replaced by either a constant value or by the results of
the fixed function.

<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> xdata, param )
</th></tr></thead></table>
<p>

Returns the partial derivatives calculated at the inputs.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.<br>


<a name="numPartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>numPartial(</strong> xdata, params, parlist=None ) 
</th></tr></thead></table>
<p>

Returns numerical partial derivatives of the model to params.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters; default is self.parameters<br>
* parlist  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of indices active parameters (or None for all)<br>


<a name="basePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePartial(</strong> xdata, param, parlist=None ) 
</th></tr></thead></table>
<p>

Replacement for models that dont define a partial.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result<br>
* param  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.<br>
* parlist  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of indices active parameters (or None for all)<br>


<a name="derivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>derivative(</strong> xdata, param ) 
</th></tr></thead></table>
<p>

Returns the derivative of the model to xdata.

It is a numeric derivative as the analytic derivative is not present
in the model.

If `fixed` contains a Model, the derivative cannot be constructed
from the constituent models. Use `numDerivative` instead.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the derivative<br>
* param  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters. (default: self.parameters)<br>


<a name="numDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>numDerivative(</strong> xdata, param ) 
</th></tr></thead></table>
<p>

Returns the numeric derivative of the model to input

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the derivative<br>
* param  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters. (default: self.parameters)<br>

<b>Raises</b>

ValueError when the number of xdata dimensions > 1.


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./BaseModel.html">BaseModel</a></th></tr></thead></table>


* [<strong>checkParameter(</strong> param ) ](./BaseModel.md#checkParameter)
* [<strong>checkPositive(</strong> param ) ](./BaseModel.md#checkPositive)
* [<strong>checkZeroParameter(</strong> param )](./BaseModel.md#checkZeroParameter)
* [<strong>isDynamic(</strong> ) ](./BaseModel.md#isDynamic)
* [<strong>isModifiable(</strong> ) ](./BaseModel.md#isModifiable)
* [<strong>shortName(</strong> )](./BaseModel.md#shortName)
* [<strong>setPrior(</strong> kpar, prior=None, **kwargs ) ](./BaseModel.md#setPrior)
* [<strong>hasPriors(</strong> isBound=True ) ](./BaseModel.md#hasPriors)
* [<strong>getPrior(</strong> kpar ) ](./BaseModel.md#getPrior)
* [<strong>basePrior(</strong> kpar ) ](./BaseModel.md#basePrior)
* [<strong>getParameterName(</strong> kpar ) ](./BaseModel.md#getParameterName)
* [<strong>baseParameterName(</strong> kpar ) ](./BaseModel.md#baseParameterName)
* [<strong>getParameterUnit(</strong> kpar ) ](./BaseModel.md#getParameterUnit)
* [<strong>baseParameterUnit(</strong> kpar ) ](./BaseModel.md#baseParameterUnit)
* [<strong>hasLimits(</strong> fitindex=None ) ](./BaseModel.md#hasLimits)
