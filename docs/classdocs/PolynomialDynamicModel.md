---
---
<br><br>

<a name="PolynomialDynamicModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class PolynomialDynamicModel(</strong> <a href="./PolynomialModel.html">PolynomialModel,</a><a href="./Dynamic.html">Dynamic</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PolynomialDynamicModel.py target=_blank>Source</a></th></tr></thead></table>

General polynomial model of an adaptable degree.

f( x:p ) = &sum; p<sub>k</sub> * x<sup>k</sup>

where the sum is over k running from 0 to degree ( inclusive ).

It is a linear model.

Author       Do Kester

<b>Examples</b>

    poly = PolynomialDynamicModel( )         # polynomial with unknown degree
    poly.grow( )                         # starts at degree = 0, npar = 1
    poly.grow( )                         # each grow( ) adds 1
    poly.grow( )
    poly.grow( )
    print poly.npchain
    5
    poly.shrink( )                        # shrink( ) deletes 1 degree
    print poly.npbase
    4

<b>Attributes</b>

* minDegree  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; minimum degree of the polynomial
* maxDegree  :  int or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; maximum degree of the polynomial

<b>Attributes from Dynamic</b>

&nbsp;&nbsp;&nbsp;&nbsp; ncomp (=degree+1), deltaNpar, minComp (=minDegree+1), maxComp (=maxDegree+1), growPrior

<b>Attributes from PolynomialModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; degree

<b>Attributes from Model</b>

&nbsp;&nbsp;&nbsp;&nbsp; npchain, parameters, stdevs, xUnit, yUnit

<b>Attributes from FixedModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist

<b>Attributes from BaseModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames


Category     mathematics/Fitting


<a name="PolynomialDynamicModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>PolynomialDynamicModel(</strong> degree, minDegree=0, maxDegree=None, fixed=None,
 growPrior=None, copy=None, **kwargs )
</th></tr></thead></table>

Polynomial of a adaptable degree.

The model starts as a PolynomialModel of degree = 0.
Growth of the model is governed by a exponential prior ( scale=1 ).

<b>Parameters</b>

* degree  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; degree to start with; it should be minDegree <= degree <= maxDegree
* minDegree  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; minimum degree of polynomial (def=0)
* maxDegree  :  None or int
<br>&nbsp;&nbsp;&nbsp;&nbsp; maximum degree of polynomial (def=None)
* growPrior  :  None or Prior
<br>&nbsp;&nbsp;&nbsp;&nbsp; governing the birth and death.
<br>&nbsp;&nbsp;&nbsp;&nbsp; ExponentialPrior (scale=2) if  maxDegree is None else UniformPrior
* copy  :  PolynomialDynamicModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to copy

<b>Raises</b>

AttributeError when fixed parameters are requested
ValueError when degree is outside [min..max] range

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>

Copy method. 
<a name="isDynamic"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isDynamic(</strong> ) 
</th></tr></thead></table>

<a name="changeNComp"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>changeNComp(</strong> dn ) 
</th></tr></thead></table>

<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>

Return a string representation of the model. 
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./PolynomialModel.html">PolynomialModel,</a></th></tr></thead></table>


* [<strong>basePartial(</strong> xdata, params, parlist=None )](./PolynomialModel.md#basePartial)
* [<strong>baseDerivative(</strong> xdata, params ) ](./PolynomialModel.md#baseDerivative)
* [<strong>baseParameterName(</strong> k )](./PolynomialModel.md#baseParameterName)
* [<strong>baseParameterUnit(</strong> k )](./PolynomialModel.md#baseParameterUnit)


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
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Dynamic.html">Dynamic</a></th></tr></thead></table>


* [<strong>setGrowPrior(</strong> growPrior=None, min=1, max=None, name="Comp" ) ](./Dynamic.md#setGrowPrior)
* [<strong>setDynamicAttribute(</strong> name, value ) ](./Dynamic.md#setDynamicAttribute)
* [<strong>grow(</strong> offset=0, rng=None, **kwargs )](./Dynamic.md#grow)
* [<strong>shrink(</strong> offset=0, rng=None, **kwargs )](./Dynamic.md#shrink)
* [<strong>alterParameterNames(</strong> dnp ) ](./Dynamic.md#alterParameterNames)
* [<strong>alterParameterSize(</strong> dnp, offset, location=None, value=0 ) ](./Dynamic.md#alterParameterSize)
* [<strong>alterParameters(</strong> param, location, dnp, offset, value=None ) ](./Dynamic.md#alterParameters)
* [<strong>alterFitindex(</strong> findex, location, dnp, offset ) ](./Dynamic.md#alterFitindex)
* [<strong>shuffle(</strong> param, offset, np, rng ) ](./Dynamic.md#shuffle)
