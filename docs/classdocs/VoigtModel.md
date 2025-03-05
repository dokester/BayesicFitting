---
---
<br><br>

<a name="VoigtModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class VoigtModel(</strong> <a href="./NonLinearModel.html">NonLinearModel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/VoigtModel.py target=_blank>Source</a></th></tr></thead></table>
<p>

Voigt's Gauss Lorentz convoluted model for line profiles.

The Voigt function is a convolution of a Gauss and a Lorentz function.
Physicaly it is the result of thermal and pressure broadening of a spectral
line.

The models takes 4 parameters: amplitude, center frequency, half-width of
the Gaussian, and half-width of the Lorentzian.
These are initialised to [1, 0, 1, 1].
Parameters 2 & 3 ( widths ) is always kept positive ( >=0 ).

The implementation uses the Faddeeva function from scipy.special.wofz.

<b>Examples</b>

    voigt = VoigtModel( )
    voigt.setParameters( [5, 4, 1, 2] )
    print( voigt( numpy.arange(  41 , dtype=float ) / 5 ) )      # from [0,8]


<b>Attributes</b>

&nbsp;&nbsp;&nbsp;&nbsp; none of its own<br>

<b>Attributes from Model</b>

&nbsp;&nbsp;&nbsp;&nbsp; npchain, parameters, stdevs, xUnit, yUnit<br>

<b>Attributes from FixedModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist<br>

<b>Attributes from BaseModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames<br>



<a name="VoigtModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>VoigtModel(</strong> copy=None, **kwargs )
</th></tr></thead></table>
<p>

Voigt model.

Number of parameters is 4.

<b>Parameters</b>

* copy  :  VoigtModel<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be copied<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Copy method. 

<a name="baseResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseResult(</strong> xdata, params )
</th></tr></thead></table>
<p>

Returns the result of the model function.

Note: both width in the parameter array ( items 2 & 3 ) are kept
strictly positive. I.e. they are changed when upon input they are negative.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.<br>


<a name="basePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePartial(</strong> xdata, params, parlist=None )
</th></tr></thead></table>
<p>

Returns the partials at the input value.

&nbsp;&nbsp;&nbsp;&nbsp; z = ( x - p1 + 1j * p3 ) / ( p2 * sqrt2 )<br>
&nbsp;&nbsp;&nbsp;&nbsp; z0 = 1j * p3 / ( p2 * sqrt2 )<br>

&nbsp;&nbsp;&nbsp;&nbsp; vgt = p0 * R( wofzz ) / R( wofz0 )<br>

&nbsp;&nbsp;&nbsp;&nbsp; dvdp = dvdz * dzdp<br>

&nbsp;&nbsp;&nbsp;&nbsp; dvdz = p0 * ( R(dwdz) * R(wofz0) - R(dwd0) * R(wofzz) ) / R(wofz0)^2<br>
&nbsp;&nbsp;&nbsp;&nbsp; dvdp = p0 * ( R(dwdz * dzdp) * R(wofz0) - R(dwd0 * d0dp) * R(wofzz) ) / R(wofz0)^2<br>

&nbsp;&nbsp;&nbsp;&nbsp; dwdz = 2j / sqrt(pi) - 2 * z  * wofzz<br>
&nbsp;&nbsp;&nbsp;&nbsp; dwd0 = 2j / sqrt(pi) - 2 * z0 * wofz0<br>

&nbsp;&nbsp;&nbsp;&nbsp; ## p0 and p1 have no influence in wofz0<br>
&nbsp;&nbsp;&nbsp;&nbsp; dzdp0 = 0<br>
&nbsp;&nbsp;&nbsp;&nbsp; dzdp1 = -1 / ( p2 * sqrt2 )<br>
&nbsp;&nbsp;&nbsp;&nbsp; d0dp2 = - ( 1j * p3 / ( p2^2 * sqrt2 )              = -z0 / p2<br>
&nbsp;&nbsp;&nbsp;&nbsp; dzdp2 = - ( ( x - p1 + 1j * p3 ) / ( p2^2 * sqrt2 ) = -z  / p2<br>
&nbsp;&nbsp;&nbsp;&nbsp; dzdp3 = d0dp3 = 1j / ( p2 * sqrt2 )<br>

&nbsp;&nbsp;&nbsp;&nbsp; dvdp0 = R(wofzz) / R(wofz0)<br>
&nbsp;&nbsp;&nbsp;&nbsp; ## The other partial follow from calculating dvdp for the parameters 1..3<br>

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the partials<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.<br>
* parlist  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of indices active parameters (or None for all)<br>


<a name="baseDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseDerivative(</strong> xdata, params ) 
</th></tr></thead></table>
<p>

Return the derivative df/dx at each xdata (=x).

&nbsp;&nbsp;&nbsp;&nbsp; z = ( x - p1 + 1j * p3 ) / ( p2 * sqrt2 )<br>
&nbsp;&nbsp;&nbsp;&nbsp; z0 = 1j * p3 / ( p2 * sqrt2 )<br>

&nbsp;&nbsp;&nbsp;&nbsp; vgt = p0 / wofz0 * re( wofzz )<br>
&nbsp;&nbsp;&nbsp;&nbsp; dvdx = dvdz * dzdx<br>

&nbsp;&nbsp;&nbsp;&nbsp; dvdz = p0 / wofz0 * dwdz<br>
&nbsp;&nbsp;&nbsp;&nbsp; dwdz = 2j / sqrt(pi) - 2 * z * wofzz<br>

&nbsp;&nbsp;&nbsp;&nbsp; dzdx = 1 / ( p2 * sqrt2 )<br>

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.<br>


<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>
<p>

Returns a string representation of the model.

<a name="baseParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseParameterUnit(</strong> k )
</th></tr></thead></table>
<p>

Return the name of a parameter.

<b>Parameters</b>

* k  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameter number.<br>


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
