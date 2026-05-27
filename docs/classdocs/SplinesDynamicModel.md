---
---
<br><br>

<a name="SplinesDynamicModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class SplinesDynamicModel(</strong> <a href="./Modifiable.html">Modifiable,</a><a href="./Dynamic.html">Dynamic,</a><a href="./BasicSplinesModel.html">BasicSplinesModel</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/SplinesDynamicModel.py target=_blank>[source]</a></th></tr></thead></table>
<p>

BasicSplinesModel that is modifiable (knot locations) and dynamic (in number
of knots)


<b>Examples</b>

    # make dynamic splinesmodel, initially with 4 equidistant knots from 0 to 10
    knots = numpy.linspace( 0, 10, 4, dtype=float )
    csm = SplinesDynamicModel( knots=knots, modifiable=False )
    print csm.getNumberOfParameters( )
    6
    # or similarly, also modifiable
    csm = SplinesDynamicModel( nrknots=4, min=0, max=10 )
    print csm.getNumberOfParameters( )
    6
    # or periodic and not dynamic
    x = numpy.arange( npt, dtype=float )
    knots = numpy.linspace( 0, 10, 4, dtype=float )
    csm = SplinesDynamicModel( knots=knots, border=1, dynamic=False )
    print csm.getNumberOfParameters( )
    5

<b>Attributes</b><br>
* minKnots  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; minimum number of knots
* maxKnots  :  int or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; maximum number of knots
* minDistance  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; minimum distance between knots
* border  :  int (0)
<br>&nbsp;&nbsp;&nbsp;&nbsp; 0,1,2 as in BasicSplinesModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; 3 periodic (as 1) with flexible period
* flexPeriod  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; flexible period when the model is periodic

<b>Attributes from Modifiable</b><br>
&nbsp;&nbsp;&nbsp;&nbsp; modifiable

<b>Attributes from Dynamic</b><br>
&nbsp;&nbsp;&nbsp;&nbsp; dynamic, ncomp, deltaNpar, minComp, maxComp, growPrior

<b>Attributes from BasicSplinesModel</b><br>
&nbsp;&nbsp;&nbsp;&nbsp; border, period

<b>Attributes from SplinesModel</b><br>
&nbsp;&nbsp;&nbsp;&nbsp; knots, order

<b>Attributes from Model</b><br>
&nbsp;&nbsp;&nbsp;&nbsp; npchain, parameters, stdevs, xUnit, yUnit

<b>Attributes from FixedModel</b><br>
&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist

<b>Attributes from BaseModel</b><br>
&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames


<b>Limitations</b><br>
Dont construct the knots so closely spaced, that there are no datapoints in between.


<a name="SplinesDynamicModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>SplinesDynamicModel(</strong> modifiable=True, dynamic=True, growPrior=None, minKnots=2, maxKnots=None,
 minDistance=0.01, border=0, copy=None, **kwargs )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/SplinesDynamicModel.py#L105-L173 target=_blank>[source]</a></th></tr></thead></table>

Splines on a given set of knots and a given order.

The number of parameters is ( length( knots ) + order - 1 )

<b>Parameters</b><br>
* modifiable  :  bool (True)
<br>&nbsp;&nbsp;&nbsp;&nbsp; if True allow changement of the knot locations
* dynamic  :  bool (True)
<br>&nbsp;&nbsp;&nbsp;&nbsp; if True allow growth and shrinkage of number of knots
* minKnots  :  int (2)
<br>&nbsp;&nbsp;&nbsp;&nbsp; minimum number of knots
* maxKnots  :  None or int
<br>&nbsp;&nbsp;&nbsp;&nbsp; maximum number of Knots
* minDistance  :  float ( 0.01 * mean knot separation )
<br>&nbsp;&nbsp;&nbsp;&nbsp; minimum distance between knots, provided as fraction of average knot distance.
* border  :  int (0)
<br>&nbsp;&nbsp;&nbsp;&nbsp; 0,1,2 as in BasicSplinesModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; 3 periodic (as 1) with flexible period
* growPrior  :  None or Prior
<br>&nbsp;&nbsp;&nbsp;&nbsp; governing the birth and death.
<br>&nbsp;&nbsp;&nbsp;&nbsp; ExponentialPrior (scale=2) if  maxDegree is None else UniformPrior
* copy  :  PolynomialDynamicModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to copy

<b>Parameters for SplinesModel</b><br>
knots, order, nrknots, min, max, xrange

<b>Raises</b><br>
ValueError if not minKnots <= nrknots <= maxKnots


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> modifiable=None, dynamic=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/SplinesDynamicModel.py#L175-L193 target=_blank>[source]</a></th></tr></thead></table>
Make a copy of the model, optionally unchangeable.

<b>Parameters</b><br>
* modifiable  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; is a modifiable model
* dynamic  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; is a dynamic model

<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/SplinesDynamicModel.py#L218-L223 target=_blank>[source]</a></th></tr></thead></table>

Returns a string representation of the model. 
<a name="changeNComp"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>changeNComp(</strong> dn ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/SplinesDynamicModel.py#L225-L226 target=_blank>[source]</a></th></tr></thead></table>

<a name="grow"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>grow(</strong> offset=0, rng=None, force=False, **kwargs )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/SplinesDynamicModel.py#L228-L293 target=_blank>[source]</a></th></tr></thead></table>
Increase the degree by one upto maxComp ( if present ).

<b>Parameters</b><br>
* offset  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index where the params of the Dynamic model start
* rng  :  random number generator (obligatory)
<br>&nbsp;&nbsp;&nbsp;&nbsp; to generate a new parameter.
* force  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; dont check maxKnots (only for varyAlt())

<b>Return</b><br>
* bool  :   succes


<a name="shrink"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shrink(</strong> offset=0, rng=None, **kwargs )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/SplinesDynamicModel.py#L295-L366 target=_blank>[source]</a></th></tr></thead></table>
Decrease the degree by one downto minComp ( default 1 ).

<b>Parameters</b><br>
* offset  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index where the params of the Dynamic model start
* rng  :  random number generator
<br>&nbsp;&nbsp;&nbsp;&nbsp; to generate a new parameter (obligatory)

<b>Return</b><br>
* bool  :  succes


<a name="vary"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>vary(</strong> rng=None, location=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/SplinesDynamicModel.py#L368-L426 target=_blank>[source]</a></th></tr></thead></table>
Vary the structure of a Modifiable Model


<b>Parameters</b><br>
* rng  :  RNG
<br>&nbsp;&nbsp;&nbsp;&nbsp; random number generator
* location  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index of the item to be modified; otherwise random
* kwargs  :  keyword arguments
<br>&nbsp;&nbsp;&nbsp;&nbsp; for specific implementations


<a name="varyAlt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>varyAlt(</strong> offset=0, rng=None, **kwargs ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/SplinesDynamicModel.py#L428-L444 target=_blank>[source]</a></th></tr></thead></table>
Vary the structure of a Modifiable Model


<b>Parameters</b><br>
* offset  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index where the params of the Modifiable model start
* rng  :  RNG
<br>&nbsp;&nbsp;&nbsp;&nbsp; random number generator
* kwargs  :  keyword arguments
<br>&nbsp;&nbsp;&nbsp;&nbsp; for specific implementations

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Modifiable.html">Modifiable,</a></th></tr></thead></table>


* [<strong>isModifiable(</strong> ) ](./Modifiable.md#isModifiable)
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Dynamic.html">Dynamic,</a></th></tr></thead></table>


* [<strong>isDynamic(</strong> ) ](./Dynamic.md#isDynamic)
* [<strong>setGrowPrior(</strong> growPrior=None, min=1, max=None, name="Comp" ) ](./Dynamic.md#setGrowPrior)
* [<strong>setDynamicAttribute(</strong> name, value ) ](./Dynamic.md#setDynamicAttribute)
* [<strong>alterParameterNames(</strong> dnp ) ](./Dynamic.md#alterParameterNames)
* [<strong>alterParameterSize(</strong> dnp, offset, location=None, value=0 ) ](./Dynamic.md#alterParameterSize)
* [<strong>alterParameters(</strong> param, location, dnp, offset, value=None ) ](./Dynamic.md#alterParameters)
* [<strong>alterFitindex(</strong> findex, location, dnp, offset ) ](./Dynamic.md#alterFitindex)
* [<strong>shuffle(</strong> param, offset, np, rng ) ](./Dynamic.md#shuffle)
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./BasicSplinesModel.html">BasicSplinesModel</a></th></tr></thead></table>


* [<strong>makeBaseBasis(</strong> ) ](./BasicSplinesModel.md#makeBaseBasis)
* [<strong>makeDist(</strong> knotix ) ](./BasicSplinesModel.md#makeDist)
* [<strong>makePeriodicBasis(</strong> ) ](./BasicSplinesModel.md#makePeriodicBasis)
* [<strong>normalizeBasis(</strong> basis ) ](./BasicSplinesModel.md#normalizeBasis)
* [<strong>findParameters(</strong> knotix, dist, kpar=0 ) ](./BasicSplinesModel.md#findParameters)
* [<strong>baseResult(</strong> xdata, params )](./BasicSplinesModel.md#baseResult)
* [<strong>basePartial(</strong> xdata, params, parlist=None )](./BasicSplinesModel.md#basePartial)
* [<strong>makeKnotIndices(</strong> xdata ) ](./BasicSplinesModel.md#makeKnotIndices)
* [<strong>basicBlob(</strong> xdata, basis, x2k, poly ) ](./BasicSplinesModel.md#basicBlob)
* [<strong>baseDerivative(</strong> xdata, params ) ](./BasicSplinesModel.md#baseDerivative)
* [<strong>baseParameterUnit(</strong> k )](./BasicSplinesModel.md#baseParameterUnit)


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
* [<strong>basePrior(</strong> kpar ) ](./BaseModel.md#basePrior)
* [<strong>getParameterIndex(</strong> parname ) ](./BaseModel.md#getParameterIndex)
* [<strong>getParameterValue(</strong> param, name, default=None ) ](./BaseModel.md#getParameterValue)
* [<strong>baseParameterName(</strong> kpar ) ](./BaseModel.md#baseParameterName)
