---
---
<br><br>

<a name="HarmonicDynamicModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class HarmonicDynamicModel(</strong> <a href="./HarmonicModel.html">HarmonicModel,</a><a href="./Dynamic.html">Dynamic</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/HarmonicDynamicModel.py target=_blank>Source</a></th></tr></thead></table>
<p>

Harmonic oscillator Model of adaptable order.

f( x:p ) = &sum;<sub>j</sub> ( p<sub>k</sub> cos( 2 &pi; j x ) + p<sub>k</sub>+1 sin( 2 &pi; j x ) )

j = 1, N; k = 0, 2N

The parameters are initialized at 1.0. It is a linear model.

Author       Do Kester

<b>Attributes</b><br>
* minOrder  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; minimum degree of polynomial (def=1)<br>
&nbsp;&nbsp;&nbsp;&nbsp; Can also be read as minComp<br>
* maxOrder  :  None or int<br>
&nbsp;&nbsp;&nbsp;&nbsp; maximum degree of polynomial (def=None)<br>
&nbsp;&nbsp;&nbsp;&nbsp; Can also be read as maxComp<br>

<b>Attributes from Dynamic</b><br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; ncomp (= order), deltaNpar, minComp (= minOrder), maxComp (= maxComp), growPrior<br>

<b>Attributes from HarmonicModel</b><br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; order, period<br>

<b>Attributes from Model</b><br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; npchain, parameters, stdevs, xUnit, yUnit<br>

<b>Attributes from FixedModel</b><br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist<br>

<b>Attributes from BaseModel</b><br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames<br>


<b>Examples</b><br>
    harm = HarmonicDynamicModel( 3 )            # period = 1
    print harm.getNumberOfParameters( )         # 6
    harm = HarmonicModel( 4, period=2.7 )       # period = 2.7

Category     mathematics/Fitting


<a name="HarmonicDynamicModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>HarmonicDynamicModel(</strong> order, minOrder=1, maxOrder=None, period=1.0, fixed=None,
 growPrior=None, copy=None, **kwargs )
</th></tr></thead></table>
<p>

Harmonic of a adaptable order.

The model starts as a HarmonicModel of order = 1
Growth of the model is governed by a prior.

<b>Parameters</b><br>
* order  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; order to start with. It should be minOrder <= order <= maxOrder<br>
* minOrder  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; minimum degree of polynomial (def=1)<br>
* maxOrder  :  None or int<br>
&nbsp;&nbsp;&nbsp;&nbsp; maximum degree of polynomial (def=None)<br>
* period  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; period of the oscilation<br>
* fixed  :  None<br>
&nbsp;&nbsp;&nbsp;&nbsp; If fixed is not None an AttributeError is raised<br>
* growPrior  :  None or Prior<br>
&nbsp;&nbsp;&nbsp;&nbsp; governing the birth and death.<br>
&nbsp;&nbsp;&nbsp;&nbsp; ExponentialPrior (scale=2) if  maxOrder is None else UniformPrior<br>
* copy  :  HarmonicDynamicModel<br>
&nbsp;&nbsp;&nbsp;&nbsp; model to copy<br>

<b>Raises</b><br>
AttributeError when fixed parameters are requested
ValueError when order is outside [min..max] range


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Copy method. 

<a name="isDynamic"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isDynamic(</strong> ) 
</th></tr></thead></table>
<p>
<a name="changeNComp"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>changeNComp(</strong> dn ) 
</th></tr></thead></table>
<p>
<a name="basePrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePrior(</strong> k )
</th></tr></thead></table>
<p>

Return the prior for parameter k.

<b>Parameters</b><br>
* k  :  int<br>
    the parameter to be selected.

<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>
<p>
Return a string representation of the model. 

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./HarmonicModel.html">HarmonicModel,</a></th></tr></thead></table>


* [<strong>basePartial(</strong> xdata, params, parlist=None )](./HarmonicModel.md#basePartial)
* [<strong>baseDerivative(</strong> xdata, params )](./HarmonicModel.md#baseDerivative)
* [<strong>baseParameterName(</strong> k )](./HarmonicModel.md#baseParameterName)
* [<strong>baseParameterUnit(</strong> k )](./HarmonicModel.md#baseParameterUnit)


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
