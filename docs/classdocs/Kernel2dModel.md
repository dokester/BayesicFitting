---
---
<br><br>

<a name="Kernel2dModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Kernel2dModel(</strong> <a href="./NonLinearModel.html">NonLinearModel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Kernel2dModel.py target=_blank>Source</a></th></tr></thead></table>
<p>

Two dimensional Kernel Model.

The Kernel2dModel is defined as

<br>&nbsp; f( x:p ) = p<sub>0</sub> * K( r )<br>

where K( r ) is a selectable kernel function and r is the distance to the center.

<br>&nbsp; r = sqrt( u<sup>2</sup> + v<sup>2</sup> ).<br>

There are 3 options for u and v

1. CIRCULAR has 4 parameters<br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; Circular shape with only one width.<br>
&nbsp;&nbsp;&nbsp;&nbsp; u = ( x - p<sub>1</sub> ) / p<sub>3</sub><br>
&nbsp;&nbsp;&nbsp;&nbsp; v = ( x - p<sub>2</sub> ) / p<sub>3</sub><br>
2. ELLIPTIC has 5 parameters<br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; Elliptic shape aligned along the axes; 2 widths.<br>
&nbsp;&nbsp;&nbsp;&nbsp; u = ( x - p<sub>1</sub> ) / p<sub>3</sub><br>
&nbsp;&nbsp;&nbsp;&nbsp; v = ( x - p<sub>2</sub> ) / p<sub>4</sub><br>
3. ROTATED has 6 parameters<br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; Rotated elliptical shape with 2 width and a rotational angle.<br>
&nbsp;&nbsp;&nbsp;&nbsp; u = ( ( x - p<sub>1</sub> )*cos( p<sub>5</sub> ) - ( y - p<sub>2</sub> )*sin( p<sub>5</sub>) ) / p<sub>3</sub><br>
&nbsp;&nbsp;&nbsp;&nbsp; v = ( ( x - p<sub>1</sub> )*sin( p<sub>5</sub> ) + ( y - p<sub>2</sub> )*cos( p<sub>5</sub>) ) / p<sub>4</sub><br>

The "center" parameters ( 1&2 ) and the "angle" parameter ( 5 ) are initilized as 0.
The rotational angle is measured counterclockwise from the x-axis.
The "width" parameters ( 3&4 ) are initialized as 1.0, except for the ROTATED case;
then they need to be different ( 2.0 and 0.5 resp. ).
Otherwise the model parameter "angle" is degenerate.
The "amplitude" parameter is set to 1.0.

Several kernel functions, K( x ) are defined in the directory fit/kernels.

Beware: These models are unaware of anything outside their range.

Author:      Do Kester

<b>Example</b><br>
    model = Kernel2dModel( )                                 # default: circular Gauss
    model.setKernelShape( Lorentz(), 'Elliptic'  )             # elliptic Lorentz model.
    model = Kernel2dModel( shape=3 )                         # rotated Gauss

* Category :     mathematics/Fitting<br>


<a name="Kernel2dModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Kernel2dModel(</strong> kernel=Gauss(), shape=1, copy=None, **kwargs )
</th></tr></thead></table>
<p>

Kernel Model.

Default model: Gauss with Circular shape.

<b>Parameters</b><br>
* kernel  :  Kernel<br>
&nbsp;&nbsp;&nbsp;&nbsp; the kernel to be used<br>
* shape  :  1 | 2 | 3 | 'circular' | 'elliptic' | 'rotated'<br>
&nbsp;&nbsp;&nbsp;&nbsp; int : resp.: circular elliptic, rotated<br>
&nbsp;&nbsp;&nbsp;&nbsp; str : case insensitive; only the first letter matters.<br>
&nbsp;&nbsp;&nbsp;&nbsp; shape defaults to 'circular' when misunderstood<br>
* copy  :  Kernel2dModel<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be copied<br>
* fixed  :  None or dictionary of {int:float|Model}<br>
&nbsp;&nbsp;&nbsp;&nbsp; int         index of parameter to fix permanently.<br>
&nbsp;&nbsp;&nbsp;&nbsp; float|Model values for the fixed parameters.<br>
&nbsp;&nbsp;&nbsp;&nbsp; Attribute fixed can only be set in the constructor.<br>
&nbsp;&nbsp;&nbsp;&nbsp; See: [FixedModel](./FixedModel.md)<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Copy method. 

<a name="parseShape"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>parseShape(</strong> shape ) 
</th></tr></thead></table>
<p>
<a name="setKernelShape"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setKernelShape(</strong> kernel, shape ) 
</th></tr></thead></table>
<p>
<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>
<p>
Returns a string representation of the model. 

<a name="baseResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseResult(</strong> xdata, params )
</th></tr></thead></table>
<p>

Returns the result of the model function.

<b>Parameters</b><br>
* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; value at which to calculate the result<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters<br>


<a name="baseDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseDerivative(</strong> xdata, params )
</th></tr></thead></table>
<p>

Returns df/dx of the model function.

<b>Parameters</b><br>
* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; value at which to calculate the result<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters<br>


<a name="basePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePartial(</strong> xdata, params, parlist=None )
</th></tr></thead></table>
<p>

Returns the partials at the xdata value.

<b>Parameters</b><br>
* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; value at which to calculate the partials<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters to the model (ignored in LinearModels)<br>
* parlist  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of indices of active parameters<br>


<a name="baseParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseParameterUnit(</strong> k )
</th></tr></thead></table>
<p>

Return the unit of a parameter.
<b>Parameters</b><br>
* k  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; the kth parameter.<br>


<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th></tr></thead></table>
<p>
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
