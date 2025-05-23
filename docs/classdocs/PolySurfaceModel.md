---
---
<br><br>

<a name="PolySurfaceModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class PolySurfaceModel(</strong> <a href="./LinearModel.html">LinearModel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PolySurfaceModel.py target=_blank>Source</a></th></tr></thead></table>

General polynomial surface model of arbitrary degree.

&nbsp; f( x,y:p ) = &sum;<sub>d</sub> &sum;<sub>k</sub> p<sub>n</sub> * x<sup>d-k</sup> * y<sup>k</sup> )

where the first sum is over d running from 0 to degree ( inclusive )
and the second sum is over k running from 0 to d ( inclusive ).
The index n is just incrementing, making all p's different.

It is a 2-dimensional linear model.

<b>Examples</b>

    poly = PolySurfaceModel( 3 )         # 3rd degree polynomial
    print poly.getNumberOfParameters( )        # 10

Author      Do Kester

<b>Attributes</b>

* degree  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; degree of the polynomial

<b>Attributes from Model</b>

&nbsp;&nbsp;&nbsp;&nbsp; npchain, parameters, stdevs, xUnit, yUnit

<b>Attributes from FixedModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist

<b>Attributes from BaseModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames



<a name="PolySurfaceModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>PolySurfaceModel(</strong> degree, copy=None, **kwargs )
</th></tr></thead></table>

Polynominal surface of a certain degree. Two dimensions.

| degree |  polysurface                                               |
|:------:|:-----------------------------------------------------------|
| 0 | p<sub>0</sub>                                                             |
| 1 | p<sub>0</sub> + p<sub>1</sub> * x + p<sub>2</sub> * y                                         |
| 2 | p<sub>0</sub> + p<sub>1</sub> * x + p<sub>2</sub> * y + p<sub>3</sub> * x<sup>2</sup> + p<sub>4</sub> * x * y + p<sub>5</sub> * y<sup>2</sup>   |
| 3 | p<sub>0</sub> + p<sub>1</sub> * x + p<sub>2</sub> * y + p<sub>3</sub> * x<sup>2</sup> + p<sub>4</sub> * x * y + p<sub>5</sub> * y<sup>2</sup> + |
|   |        p<sub>6</sub> * x<sup>3</sup> + p<sub>7</sub> * x<sup>2</sup> * y + p<sub>8</sub> * x * y<sup>2</sup> + p<sub>9</sub> * y<sup>3</sup>    |
|etc|                                                                 |

The number of parameters is ( degree+2 ) * ( degree+1 ) / 2

<b>Parameters</b>

* degree  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; the degree of the polynomial.
* copy  :  PolySurfaceModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to be copied
* fixed  :  dictionary of {int:float|Model}
<br>&nbsp;&nbsp;&nbsp;&nbsp; int             list if parameters to fix permanently. Default None.
<br>&nbsp;&nbsp;&nbsp;&nbsp; float|Model     list of values for the fixed parameters.
<br>&nbsp;&nbsp;&nbsp;&nbsp; Attribute fixed can only be set in the constructor.
<br>&nbsp;&nbsp;&nbsp;&nbsp; See [FixedModel](./FixedModel.md)


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>

Copy method. 
<a name="basePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePartial(</strong> xdata, params, parlist=None )
</th></tr></thead></table>
Returns the partials at the input values.

The partials are the powers of x,y ( xdata ) from 0 to degree.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.


<a name="baseDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseDerivative(</strong> xdata, params ) 
</th></tr></thead></table>
Return the derivative df/dx at each input (=x).

| degree | df/dx |
|:------:|:------|
| 0 | 0          |
| 1 | p<sub>1</sub>        |
| 2 | p<sub>1</sub> + 2 * p<sub>3</sub> * x + p<sub>4</sub> * y |
| 3 | p<sub>1</sub> + 2 * p<sub>3</sub> * x + p<sub>4</sub> * y + 3 * p<sub>6</sub> * x<sup>2</sup> + 2 * p<sub>7</sub> * x * y + p<sub>8</sub> * y<sup>2</sup> |

| degree | df/dy |
|:------:|:------|
| 0 | 0          |
| 1 | p<sub>2</sub>        | 
| 2 | p<sub>2</sub> + p<sub>4</sub> * x + 2 * p<sub>5</sub> * y |
| 3 | p<sub>2</sub> + p<sub>4</sub> * x + 2 * p<sub>5</sub> * y + p<sub>7</sub> * x<sup>2</sup> + 2 * p<sub>8</sub> * x * y + 3 * p<sub>9</sub> * y<sup>2</sup> |


<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the partials
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model.


<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>
Returns a string representation of the model.


<a name="baseParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseParameterUnit(</strong> k )
</th></tr></thead></table>
Return the unit of the indicated parameter.
Parameters  k    parameter number.


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./LinearModel.html">LinearModel</a></th></tr></thead></table>


* [<strong>baseResult(</strong> xdata, params )](./LinearModel.md#baseResult)


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
* [<strong>partial(</strong> xdata, param, useNum=False )](./Model.md#partial)
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
* [<strong>isMixed(</strong> )](./Model.md#isMixed)
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
