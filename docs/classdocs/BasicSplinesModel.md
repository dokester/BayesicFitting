---
---
<br><br>

<a name="BasicSplinesModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class BasicSplinesModel(</strong> <a href="./SplinesModel.html">SplinesModel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BasicSplinesModel.py target=_blank>Source</a></th></tr></thead></table>

Splines model consisting of a basis of spline blobs.

The blobs have limited support. Each blob is a segment of polynomial order,
between 2 knots. At the knots they are continuous (differentiable) upto order - 1.
Similarly the edges of the blobs are smoothly connected to 0.

|order |support| behaviour between knots | continuity at knots                |
|:----:|:-----:|:------------------------|:-----------------------------------|
|  0   |   1   | piecewise constant      | not continuous at all              |
|  1   |   2   | piecewise linear        | lines are continuous (connected)   |
|  2   |   3   | parabolic pieces        | 1st derivatives are also continuous|
|  3   |   4   | cubic pieces            | 2nd derivatives are also continuous|
| n>3  |  n+1  | n-th order polynomials  | (n-1)-th derivatives are continuous|

The function result is the sum over all spline blobs, multiplied with
the parameters, the amplitudes of the spline blobs.

The support of the knots defined the domain where the function is defined. They are
hard edges. Consequently the function is not continuous or differentiable at the edges.
The spline blobs at the edges may be different from the ones in the middle.


<b>From SplinesModel</b>

The user lays out a number ( << datapoints ) of knots on the x-axis at
arbitrary position, generally more knots where the curvature is higher.
The knots need to be monotonuously increasing in x.
Alternatively one can ask this class to do the lay-out which is then
equidistant in x over the user-provided range.
Through these knots a splines function is obtained which best
fits the datapoints. One needs at least 2 knots, one smaller and one
larger than the x-values in the dataset.

This model is NOT for (cubic) spline interpolation.

<b>Examples</b>

    knots = numpy.arange( 17, dtype=float ) * 10    # make equidistant knots from 0 to 160
    csm = BasicSplinesModel( knots=knots, order=2 )
    print csm.getNumberOfParameters( )
    18
    # or alternatively
    csm = SplinesModel( nrknots=17, order=2, min=0, max=160 )    # automatic layout of knots
    print csm.getNumberOfParameters( )
    18
    # or alternatively
    npt = 161                                               # to include both 0 and 160.
    x = numpy.arange( npt, dtype=float )                    # x-values
    csm = BasicSplinesModel( nrknots=17, order=2, xrange=x )     # automatic layout of knots
    print csm.getNumberOfParameters( )
    18

<b>Attributes</b>

* knots  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; positions of the spline knots
* order  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; order of the spline. default: 3

<b>Attributes from Model</b>

&nbsp;&nbsp;&nbsp;&nbsp; npchain, parameters, stdevs, xUnit, yUnit

<b>Attributes from FixedModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist

<b>Attributes from BaseModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames


<b>Limitations</b>

Dont construct the knots so closely spaced, that there are no datapoints in between.


<a name="BasicSplinesModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>BasicSplinesModel(</strong> knots=None, order=3, nrknots=None, min=None, max=None, xrange=None,
 border=0, copy=None, **kwargs )
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
* border  :  [0, 1, 2]
<br>&nbsp;&nbsp;&nbsp;&nbsp; defines what happens at the borders of the knot range.
<br>&nbsp;&nbsp;&nbsp;&nbsp; 0 : Just like de Boors b-splines.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; the model is NOT defined outside the knot range.
<br>&nbsp;&nbsp;&nbsp;&nbsp; 1 : periodic, make knot[0] the same as knot[-1]
<br>&nbsp;&nbsp;&nbsp;&nbsp; 2 : easy borders. the model is slightly extensable.
* min  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; minimum of the knot range
* max  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; maximum of the knot range
* xrange  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; range of the xdata
* copy  :  BasicSplinesModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to be copied.
* fixed  :  None or dictionary of {int:float|Model}
<br>&nbsp;&nbsp;&nbsp;&nbsp; int         index of parameter to fix permanently.
<br>&nbsp;&nbsp;&nbsp;&nbsp; float|Model values for the fixed parameters.
<br>&nbsp;&nbsp;&nbsp;&nbsp; Attribute fixed can only be set in the constructor.
<br>&nbsp;&nbsp;&nbsp;&nbsp; See: [FixedModel](./FixedModel.md)

<b>Raises</b>

* ValueError  :  At least either (`knots`) or (`nrknots`, `min`, `max`) or
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (`nrknots`, `xrange`) must be provided to define a valid model.

<b>Notes</b>

The SplinesModel is only strictly valid inside the domain defined by the
minmax of knots. It deteriorates fastly going outside the domain.


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>

<a name="makeBaseBasis"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makeBaseBasis(</strong> ) 
</th></tr></thead></table>
Make a sets of polynomial bases for each of the parameters

<b>Return</b>

* basis  :  3-d array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters to the polynomials that make up the spline blobs


<a name="makeDist"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makeDist(</strong> knotix ) 
</th></tr></thead></table>

<a name="makePeriodicBasis"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makePeriodicBasis(</strong> ) 
</th></tr></thead></table>
Make a sets of polynomial bases for each of the parameters

<b>Return</b>

* basis  :  3-d array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters to the polynomials that make up the spline blobs


<a name="normalizeBasis"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>normalizeBasis(</strong> basis ) 
</th></tr></thead></table>
Normalize the base splines such that a constant value of 1.0
is returned when all model parameters are 1.

<b>Parameters</b>

* basis  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters to the polynomials that make up the spline blobs

<a name="findParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>findParameters(</strong> knotix, dist, kpar=0 ) 
</th></tr></thead></table>
Find the parameters by assuming (order-1) continuous differentials.
At the edges it is less. Normalized to 1.0


<b>Parameters</b>

* knotix  :  int array
<br>&nbsp;&nbsp;&nbsp;&nbsp; knot indices involved in this spline blob
* dist  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; distances between knots
* kpar  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index of parameter for which the spline-blob is constructed

<b>Returns</b>

* par  :  2-d array
<br>&nbsp;&nbsp;&nbsp;&nbsp; sets of poly parameters.

<a name="baseResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseResult(</strong> xdata, params )
</th></tr></thead></table>
Returns the functional result at the input value.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; value at which to calculate the partials
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters to the model (ignored in LinearModels)


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

for kb in range( np ) 
<br>&nbsp;&nbsp;&nbsp;&nbsp; bss = self.basis[:,:,kb]
<br>&nbsp;&nbsp;&nbsp;&nbsp; partial[:,kb] = self.basicBlob( xdata, bss, x2k, self.poly )

return partial

<a name="makeKnotIndices"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makeKnotIndices(</strong> xdata ) 
</th></tr></thead></table>
Return a list of indices of the knots immediately preceeding the xdata.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the indices

<a name="basicBlob"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basicBlob(</strong> xdata, basis, x2k, poly ) 
</th></tr></thead></table>
Calculates a spline blob for all of xdata

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; value at which to calculate the spline
* basis  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; splineParameters
* x2k  :  int_array
<br>&nbsp;&nbsp;&nbsp;&nbsp; pointing to the knot preceeding each xdata point
* poly  :  PolynomialModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to calculate the splines

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
Return the name of the parameter.

<b>Parameters</b>

* k  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index of the parameter.

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./SplinesModel.html">SplinesModel</a></th></tr></thead></table>




<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./LinearModel.html">LinearModel</a></th></tr></thead></table>




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
