---
---
<br><br><br>

<a name="SplinesDynamicModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class SplinesDynamicModel(</strong> <a href="./Modifiable.html">Modifiable,</a><a href="./Dynamic.html">Dynamic,</a><a href="./BasicSplinesModel.html">BasicSplinesModel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/SplinesDynamicModel.py target=_blank>Source</a></th></tr></thead></table>
<p>

BasicSplinesModel that is modifiable (knot locations) and dynamic (in number
of knots)


<b>Examples</b>

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

<b>Attributes</b>

* minKnots  :  int<br>
    minimum number of knots<br>
* maxDegree  :  int or None<br>
    maximum number of knots<br>

<b>Attributes from Modifiable</b>

    modifiable<br>

<b>Attributes from Dynamic</b>

    dynamic, ncomp (=degree+1), deltaNpar, minComp (=minDegree+1), maxComp (=maxDegree+1), growPrior<br>

<b>Attributes from SplinesModel</b>

    knots, order<br>

<b>Attributes from Model</b>

    npchain, parameters, stdevs, xUnit, yUnit<br>

<b>Attributes from FixedModel</b>

    npmax, fixed, parlist, mlist<br>

<b>Attributes from BaseModel</b>

    npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames<br>


<b>Limitations</b>

Dont construct the knots so closely spaced, that there are no datapoints in between.


<a name="SplinesDynamicModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>SplinesDynamicModel(</strong> modifiable=True, dynamic=True, growPrior=None, minKnots=2, maxKnots=None,
 minDistance=0.01, copy=None, **kwargs )
</th></tr></thead></table>
<p>

Splines on a given set of knots and a given order.

The number of parameters is ( length( knots ) + order - 1 )

<b>Parameters</b>

* modifiable  :  bool<br>
    if True allow changement of the knot locations<br>
* dynamic  :  bool<br>
    if True allow growth and shrinkage of number of knots<br>
* minKnots  :  int<br>
    minimum number of knots (def=2)<br>
* maxKnots  :  None or int<br>
    maximum number of Knots<br>
* minDistance  :  float<br>
    minimum distance between knots, provided as fraction of average knot distance.<br>
    default is ( 0.01 * ( knots[-1] - knots[0] ) / nrknots )<br>
* growPrior  :  None or Prior<br>
    governing the birth and death.<br>
    ExponentialPrior (scale=2) if  maxDegree is None else UniformPrior<br>
* copy  :  PolynomialDynamicModel<br>
    model to copy<br>

<b>Parameters for SplinesModel</b>

knots, order, nrknots, min, max, xrange

<b>Raises</b>

ValueError if not minKnots <= nrknots <= maxKnots


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> modifiable=None, dynamic=None )
</th></tr></thead></table>
<p>
<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>
<p>
Returns a string representation of the model. 

<a name="changeNComp"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>changeNComp(</strong> dn ) 
</th></tr></thead></table>
<p>
<a name="grow"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>grow(</strong> offset=0, rng=None, force=False, **kwargs )
</th></tr></thead></table>
<p>

Increase the degree by one upto maxComp ( if present ).

<b>Parameters</b>

* offset  :  int<br>
    index where the params of the Dynamic model start<br>
* rng  :  random number generator (obligatory)<br>
    to generate a new parameter.<br>
* force  :  bool<br>
    dont check maxKnots<br>

<b>Return</b>

* bool  :   succes<br>


<a name="shrink"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shrink(</strong> offset=0, rng=None, **kwargs )
</th></tr></thead></table>
<p>

Decrease the degree by one downto minComp ( default 1 ).

<b>Parameters</b>

* offset  :  int<br>
    index where the params of the Dynamic model start<br>
* rng  :  random number generator<br>
    to generate a new parameter (obligatory)<br>

<b>Return</b>

* bool  :  succes<br>


<a name="vary"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>vary(</strong> rng=None, location=None ) 
</th></tr></thead></table>
<p>
<a name="varyAlt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>varyAlt(</strong> offset=0, rng=None, **kwargs ) 
</th></tr></thead></table>
<p>

Vary the structure of a Modifiable Model


<b>Parameters</b>

* offset  :  int<br>
    index where the params of the Modifiable model start<br>
* rng  :  RNG<br>
    random number generator<br>
* kwargs  :  keyword arguments<br>
    for specific implementations

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




<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./LinearModel.html">LinearModel</a></th></tr></thead></table>




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
* [<strong>basePrior(</strong> kpar ) ](./BaseModel.md#basePrior)
* [<strong>baseParameterName(</strong> kpar ) ](./BaseModel.md#baseParameterName)
