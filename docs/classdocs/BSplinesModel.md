---
---
<br><br>

<a name="BSplinesModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class BSplinesModel(</strong> <a href="./LinearModel.html">LinearModel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BSplinesModel.py target=_blank>Source</a></th></tr></thead></table>

General b-splines model of arbitrary order and with arbitrary knot settings.

It encapsulates the bspline package of John Foster and Juha Jeronen,
at http://github.com/johnfoster/bspline.

B-splines have some advantages over natural splines as implemented in
SplinesModel. Specificly the parameters are much more easily
interpreted as the amplitudes of spline-like blobs. The disadvantage of
BSplinesModel is that the x-values need to fall strictly within the range
spanned by the knots.

It is a linear model.

| order |behaviour between knots | continuity at knots                |
|:-----:|:-----------------------|:-----------------------------------|
|   0   | piecewise constant     | not continuous at all              |
|   1   | piecewise linear       | lines are continuous               |
|   2   | parabolic pieces       | 1st derivatives are also continuous|
|   3   | cubic pieces           | 2nd derivatives are also continuous|
|  n>3  | n-th order polynomials | (n-1)th derivatives are continuous |

The user lays out a number ( << datapoints ) of knots on the x-axis at
arbitrary position, generally more knots where the curvature is higher.
The knots need to be monotonuously increasing in x.
Alternatively one can ask this class to do the lay-out which is then
equidistant in x over the user-provided range.
Through these knots a splines function is obtained which best
fits the datapoints. One needs at least 2 knots, one smaller and one
larger than the x-values in the dataset.

Contrary to the SplinesModel here the xdata need to be strictly inside the range
spanned by the knots: knots[0] <= xdata < knots[-1]

This model is NOT for (cubic) spline interpolation.

<b>Examples</b>

    knots = numpy.arange( 17, dtype=float ) * 10    # make equidistant knots from 0 to 160
    csm = BSplinesModel( knots=knots, order=2 )
    print csm.getNumberOfParameters( )
    18
    # or alternatively
    csm = BSplinesModel( nrknots=17, order=2, min=0, max=160 )    # automatic layout of knots
    print csm.getNumberOfParameters( )
    18
    # or alternatively
    npt = 161                                               # to include both 0 and 160.
    x = numpy.arange( npt, dtype=float )                    # x-values
    csm = BSplinesModel( nrknots=17, order=2, xrange=x )     # automatic layout of knots
    print csm.getNumberOfParameters( )
    18

<b>Attributes</b>

* knots  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; a array of arbitrarily positioned knots
* order  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; order of the spline. Default 3 (cubic splines)
* eps  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; small number to enable inclusion of endpoints. Default 0.0.


<b>Attributes from Model</b>

&nbsp;&nbsp;&nbsp;&nbsp; parameters, stdevs, xUnit, yUnit, npchain

<b>Attributes from FixedModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist

<b>Attributes from BaseModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames



<b>Limitations</b>

Dont put the knots too closely so that there are no datapoints in between.


<a name="BSplinesModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>BSplinesModel(</strong> knots=None, order=3, nrknots=None, min=None, max=None, xrange=None,
 copy=None, fixed=None, **kwargs )
</th></tr></thead></table>

Splines on a given set of knots and a given order.

The number of parameters is ( length( knots ) + order - 1 )

<b>Parameters</b>

* knots  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; a array of arbitrarily positioned knots
* order  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; order of the spline. Default 3 (cubic splines)
* nrknots  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of knots, equidistantly posited over xrange or [min,max]
* min  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; minimum of the knot range
* max  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; maximum of the knot range
* xrange  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; range of the xdata
* copy  :  BSplinesModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to be copied.
* fixed  :  dict
<br>&nbsp;&nbsp;&nbsp;&nbsp; If not None, raise AttributeError.


<b>Raises</b>

* ValueError  :  At least either ('knots') or ('nrnkots', 'min', 'max') or
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ('nrknots', 'xrange') must be provided to define a valid model.
* AttributeErrr  :  When fixed is not None

<b>Notes</b>

The BSplinesModel is only strictly valid inside the domain defined by the
minmax of knots. It does not exist outside that domain.


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>

<a name="basePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePartial(</strong> xdata, params, parlist=None )
</th></tr></thead></table>
Returns the partials at the input value.

The partials are the powers of x (input) from 0 to degree.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; value at which to calculate the partials
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters to the model (ignored in LinearModels)
* parlist  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of indices active parameters (or None for all)

<b>Raises</b>

ValueError when xdata < knots[0] or xdata > knots[1]


<a name="baseDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseDerivative(</strong> xdata, params ) 
</th></tr></thead></table>
Return the derivative df/dx at each xdata (=x).

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; value at which to calculate the partials
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters to the model


<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>

Returns a string representation of the model. 
<a name="baseParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseParameterUnit(</strong> k )
</th></tr></thead></table>
Return the units of the parameter.

<b>Parameters</b>

* k  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index of the parameter.

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
