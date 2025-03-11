---
---
<br><br>

<a name="SplinesModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class SplinesModel(</strong> <a href="./LinearModel.html">LinearModel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/SplinesModel.py target=_blank>Source</a></th></tr></thead></table>
<p>

General splines model of arbitrary order and with arbitrary knot settings.
It is a linear model.

order   behaviour between knots     continuity at knots
<br>&nbsp;&nbsp; 0     piecewise constant          not continuous at all<br>
&nbsp;&nbsp; 1     piecewise linear            lines are continuous (connected)<br>
&nbsp;&nbsp; 2     parabolic pieces            1st derivatives are also continuous<br>
&nbsp;&nbsp; 3     cubic pieces                2nd derivatives are also continuous<br>
&nbsp; n>3    n-th order polynomials      (n-1)-th derivatives are also continuous<br>

The user lays out a number ( << datapoints ) of knots on the x-axis at
arbitrary position, generally more knots where the curvature is higher.
The knots need to be monotonuously increasing in x.
Alternatively one can ask this class to do the lay-out which is then
equidistant in x over the user-provided range.
Through these knots a splines function is obtained which best
fits the datapoints. One needs at least 2 knots, one smaller and one
larger than the x-values in the dataset.

If the end knots are put in between the x-values in the dataset, a kind of
extrapoling spline is obtained. It still works more or less. Dont push it.

This model is NOT for (cubic) spline interpolation.

<b>Examples</b><br>
    knots = numpy.arange( 17, dtype=float ) * 10    # make equidistant knots from 0 to 160
    csm = SplinesModel( knots=knots, order=2 )
    print csm.getNumberOfParameters( )
18
* # or alternatively : <br>
    csm = SplinesModel( nrknots=17, order=2, min=0, max=160 )    # automatic layout of knots
    print csm.getNumberOfParameters( )
18
* # or alternatively : <br>
    npt = 161                                               # to include both 0 and 160.
    x = numpy.arange( npt, dtype=float )                    # x-values
    csm = SplinesModel( nrknots=17, order=2, xrange=x )     # automatic layout of knots
    print csm.getNumberOfParameters( )
18

<b>Attributes</b><br>
* knots  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; positions of the spline knots<br>
* order  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; order of the spline. default: 3<br>

<b>Attributes from Model</b><br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; npchain, parameters, stdevs, xUnit, yUnit<br>

<b>Attributes from FixedModel</b><br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist<br>

<b>Attributes from BaseModel</b><br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames<br>


<b>Limitations</b><br>
Dont construct the knots so closely spaced, that there are no datapoints in between.


<a name="SplinesModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>SplinesModel(</strong> knots=None, order=3, nrknots=None, min=None, max=None, xrange=None,
 copy=None, **kwargs )
</th></tr></thead></table>
<p>

Splines on a given set of knots and a given order.

The number of parameters is ( length( knots ) + order - 1 )

<b>Parameters</b><br>
* knots  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; a array of arbitrarily positioned knots<br>
* order  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; order of the spline. Default 3 (cubic splines)<br>
* nrknots  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of knots, equidistantly posited over xrange or [min,max]<br>
* min  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; minimum of the knot range<br>
* max  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; maximum of the knot range<br>
* xrange  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; range of the xdata<br>
* copy  :  SplinesModel<br>
&nbsp;&nbsp;&nbsp;&nbsp; model to be copied.<br>
* fixed  :  None or dictionary of {int:float|Model}<br>
&nbsp;&nbsp;&nbsp;&nbsp; int         index of parameter to fix permanently.<br>
&nbsp;&nbsp;&nbsp;&nbsp; float|Model values for the fixed parameters.<br>
&nbsp;&nbsp;&nbsp;&nbsp; Attribute fixed can only be set in the constructor.<br>
&nbsp;&nbsp;&nbsp;&nbsp; See: [FixedModel](./FixedModel.md)<br>

<b>Raises</b><br>
* ValueError  :  At least either (`knots`) or (`nrknots`, `min`, `max`) or<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (`nrknots`, `xrange`) must be provided to define a valid model.<br>

<b>Notes</b><br>
The SplinesModel is only strictly valid inside the domain defined by the
minmax of knots. It deteriorates fastly going outside the domain.


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
<a name="basePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePartial(</strong> xdata, params, parlist=None )
</th></tr></thead></table>
<p>

Returns the partials at the input value.

The partials are the powers of x (input) from 0 to degree.

<b>Parameters</b><br>
* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; value at which to calculate the partials<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters to the model (ignored in LinearModels)<br>
* parlist  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of indices active parameters (or None for all)<br>


<a name="baseDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseDerivative(</strong> xdata, params ) 
</th></tr></thead></table>
<p>

Return the derivative df/dx at each xdata (=x).

<b>Parameters</b><br>
* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; value at which to calculate the partials<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters to the model<br>


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

Return the name of the parameter.

<b>Parameters</b><br>
* k  :  int<br>
    index of the parameter.

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
