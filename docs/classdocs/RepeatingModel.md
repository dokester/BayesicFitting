---
---
<br><br>

<a name="RepeatingModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class RepeatingModel(</strong> <a href="./Model.html">Model,</a><a href="./Dynamic.html">Dynamic</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/RepeatingModel.py target=_blank>Source</a></th></tr></thead></table>
<p>

RepeatingModel is a dynamic model, that calls the same model zero or more 
times, each time with the next set of parameters.

RepeatingModel is a Dynamic model that grows and shrinks according to a 
growPrior. The growPrior defaults to ExponentialPrior, unless a maxComp 
(max nr of components) then it defaults to a UniformPrior with limits 
minComp .. maxComp.

When isDynamic is set to False or minComp == maxComp, the RepeatingModel is 
a normal model with a static number of parameters/components.

Priors and/or limits for the RepeatingModel are stored in the (encapsulated)
model. So the priors are taken from the same set for subsequent repetitions
of the model call. 

It can be arranged that all similar parameters are the same, represented by the
same parameters. Use keywords same=.

<b>Attributes</b>

* ncomp  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of repetitions<br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; (encapsulated) model to be repeated<br>
* same  :  None or int or list of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters of model that get identical values<br>
* index  :  list of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of parameter indices not in same.<br>
* isDyna  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; Whether this is a Dynamic Model.<br>

<b>Attributes from Dynamic</b>

&nbsp;&nbsp;&nbsp;&nbsp; ncomp, deltaNpar, minComp, maxComp, growPrior<br>

<b>Attributes from Model</b>

&nbsp;&nbsp;&nbsp;&nbsp; parameters, stdevs, npchain<br>
&nbsp;&nbsp;&nbsp;&nbsp; _next, _head, _operation<br>
&nbsp;&nbsp;&nbsp;&nbsp; xUnit, yUnit (relegated to model)<br>

<b>Attributes from FixedModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist<br>

<b>Attributes from BaseModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames<br>

<b>Example</b>

    # Define a model containing between 1 and 6 VoigtModels, starting with 3
    # and all with the same widths (for Gauss and Cauchy)
    vgt = VoigtModel()
    mdl = RepeatingModel( 3, vgt, minComp=1. maxComp=6, same=[2,3] )
    print( mdl.npbase )             # 4 + 2 + 2
    8
    # Define a static RepeatingModel of 5 GaussModels
    gm = GaussModel()
    mdl = RepeatingModel( 5, gm, isDynamic=False )
    print( mdl.npbase )             # 5 * 3
    15
    # Define a RepeatingModel with and exponential grow prior with scale 10
    mdl = RepeatingModel( 1, gm, growPrior=ExponentialPrior( scale=10 ) )
    print( mdl.npbase )             # 3
    3

Author       Do Kester


<a name="RepeatingModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>RepeatingModel(</strong> ncomp, model, minComp=0, maxComp=None, fixed=None,
 same=None, growPrior=None, dynamic=True, copy=None, **kwargs )
</th></tr></thead></table>
<p>

Repeating the same model several times.

<b>Parameters</b>

* ncomp  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of repetitions<br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; model to be repeated<br>
* minComp  :  int (0)<br>
&nbsp;&nbsp;&nbsp;&nbsp; minimum number of repetitions<br>
* maxComp  :  None or int<br>
&nbsp;&nbsp;&nbsp;&nbsp; maximum number of repetitions<br>
* same  :  None or int or list of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters of model that get identical values<br>

* growPrior  :  None or Prior<br>
&nbsp;&nbsp;&nbsp;&nbsp; governing the birth and death.<br>
&nbsp;&nbsp;&nbsp;&nbsp; ExponentialPrior (scale=2) if  maxOrder is None else UniformPrior<br>
* dynamic  :  bool (True)<br>
&nbsp;&nbsp;&nbsp;&nbsp; Whether this is a Dynamic Model.<br>
* copy  :  RepeatingModel<br>
&nbsp;&nbsp;&nbsp;&nbsp; model to copy<br>

<b>Raises</b>

AttributeError when fixed parameters are requested
ValueError when order is outside [min..max] range


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Copy method. 

<a name="changeNComp"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>changeNComp(</strong> dn ) 
</th></tr></thead></table>
<p>
<a name="setSame"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setSame(</strong> same ) 
</th></tr></thead></table>
<p>

Assign similar parameters the same value.

<b>Parameters</b>

* same  :  None or int or [int]<br>
    similar parameters indicated as an index in encapsulated model.

<a name="grow"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>grow(</strong> offset=0, rng=None, **kwargs )
</th></tr></thead></table>
<p>

Increase the the number of components by 1 (if allowed by maxComp)

<b>Parameters</b>

* offset  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index where the dynamic model starts<br>
* rng  :  RandomState<br>
&nbsp;&nbsp;&nbsp;&nbsp; random numbr generator<br>

<b>Return</b>

* bool  :   succes<br>


<a name="shrink"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shrink(</strong> offset=0, **kwargs )
</th></tr></thead></table>
<p>

Decrease the the number of componenets by 1 (if allowed by minComp)
Remove an arbitrary item.

<b>Parameters</b>

* offset  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index where the dynamic model starts<br>

<b>Return</b>

* bool  :  succes<br>


<a name="shuffle"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shuffle(</strong> param, offset, np, rng ) 
</th></tr></thead></table>
<p>

Shuffle the parameters of the components (if they are equivalent)

<b>Parameters</b>

* param  :  array-like<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters<br>
* offset  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index where the dynamic model starts<br>
* np  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; length of the parameters of the dynamic model<br>
* rng  :  RNG<br>
    random number generator

<a name="isDynamic"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isDynamic(</strong> ) 
</th></tr></thead></table>
<p>
<a name="baseResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseResult(</strong> xdata, params )
</th></tr></thead></table>
<p>

Returns the result of the model function.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; value at which to calculate the result<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters<br>


<a name="basePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePartial(</strong> xdata, params, parlist=None )
</th></tr></thead></table>
<p>

Returns the partials at the input value.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; value at which to calculate the result<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters<br>
* parlist  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of indices of active parameter<br>


<a name="baseDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseDerivative(</strong> xdata, params )
</th></tr></thead></table>
<p>

Returns the derivative df/dx at the input value.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; value at which to calculate the result<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters<br>


<a name="xxxsetLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>xxxsetLimits(</strong> lowLimits=None, highLimits=None ) 
</th></tr></thead></table>
<p>
<a name="setPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setPrior(</strong> kpar, prior=None, **kwargs ) 
</th></tr></thead></table>
<p>

Set the prior for the indicated parameter of the repeated model.

All repeated parameters have the same Prior.

<b>Parameters</b>

* kpar  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameter number of the repeated model.<br>
* prior  :  Prior<br>
&nbsp;&nbsp;&nbsp;&nbsp; prior for parameter kpar<br>
* kwargs  :  keyword arguments<br>
&nbsp;&nbsp;&nbsp;&nbsp; attributes to be passed to the prior<br>

<b>Raise:</b>

IndexException
&nbsp;&nbsp;&nbsp;&nbsp; When more Priors are set than fit inside the repeated model<br>


<a name="hasPriors"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasPriors(</strong> ) 
</th></tr></thead></table>
<p>
<a name="basePrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePrior(</strong> kpar )
</th></tr></thead></table>
<p>

Return the prior for parameter with index kpar.

<b>Parameters</b>

* kpar  :  int<br>
    index of the parameter to be selected.

<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>
<p>
Return a string representation of the model. 

<a name="baseParameterName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseParameterName(</strong> k )
</th></tr></thead></table>
<p>

Return the name of the indicated parameter.

<b>Parameters</b>

* k  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameter number.<br>


<a name="baseParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseParameterUnit(</strong> k )
</th></tr></thead></table>
<p>

Return the unit of the indicated parameter.

<b>Parameters</b>

* k  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameter number.<br>


<a name="par2model"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>par2model(</strong> k ) 
</th></tr></thead></table>
<p>

Return index in model and repetition nr for param k

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Model.html">Model,</a></th></tr></thead></table>


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
* [<strong>getPrior(</strong> kpar )](./Model.md#getPrior)
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
* [<strong>alterParameterNames(</strong> dnp ) ](./Dynamic.md#alterParameterNames)
* [<strong>alterParameterSize(</strong> dnp, offset, location=None, value=0 ) ](./Dynamic.md#alterParameterSize)
* [<strong>alterParameters(</strong> param, location, dnp, offset, value=None ) ](./Dynamic.md#alterParameters)
* [<strong>alterFitindex(</strong> findex, location, dnp, offset ) ](./Dynamic.md#alterFitindex)
