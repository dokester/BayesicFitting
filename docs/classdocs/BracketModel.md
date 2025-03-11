---
---
<br><br>

<a name="BracketModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class BracketModel(</strong> <a href="./Brackets.html">Brackets</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BracketModel.py target=_blank>Source</a></th></tr></thead></table>
<p>

BracketModel provides brackets to a chain of Models.

Its results are exactly the same as the results of the contained model.

When the contained model is a compound model (a chain of models), the
BracketModel make a single unit out of it. It acts as a pair of brackets
in another chain of models. Since compound models can be joined by operations
other than addition ( there is also subtract, multiply and divide ) brackets
are needed to distinguish m1 * ( m2 + m3 ) from m1 * m2 + m3.

BracketModel is automatically invoked when the Model appended to another model,
is actually a chain of models.

Model.Brackets is an internal class inside Model.

<b>Attributes</b><br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be put inside of brackets<br>
* deep  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; container depth (only for nice printing).<br>

<b>Attributes from Model</b><br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; npchain, parameters, stdevs, xUnit, yUnit<br>

<b>Attributes from FixedModel</b><br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist<br>

<b>Attributes from BaseModel</b><br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames<br>


<b>Examples</b><br>
Explicit use of BrackeModel

    m1 = GaussModel( )
    m1 += PolynomialModel( 0 )              # Gauss on a constant background
    m2 = BracketModel( m1 )
    m3 = SineModel( )
    m3 *= m2                                # sine * ( gauss + const )
    print( m3 )

Implicit use of BrackeModel, automatically invoked when m2 is a chain

    m1 = GaussModel( )
    m1 += PolynomialModel( 0 )              # m1 is a chain of models
    m3 = SineModel( )
    m3 *= m1                                # sine * ( gauss + const )
    print( m3 )                             # exactly the same


<b>Warning</b><br>
BracketModel is about rather advanced model building.

<b>Notes</b><br>
1. You have to complete the BracketModel, including parameter reduction,
<br>&nbsp;&nbsp;&nbsp; BEFORE you put it into a model chain.<br>
2. If you change a BracketModel which is part of a model chain, unexpected result
<br>&nbsp;&nbsp;&nbsp; might happen.<br>



<a name="BracketModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>BracketModel(</strong> model, copy=None, fixed=None, **kwargs )
</th></tr></thead></table>
<p>

BracketModel

When constructing a BracketModel existing attributes are lost, except
parameters that were 'fixed' in the constituent Models. They stay fixed.

<b>Parameters</b><br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be put in the container.<br>
* copy  :  BracketModel<br>
&nbsp;&nbsp;&nbsp;&nbsp; model to be copied<br>
* fixed  :  dict<br>
&nbsp;&nbsp;&nbsp;&nbsp; if fixed is not None raise AttributeError<br>
&nbsp;&nbsp;&nbsp;&nbsp; Use fixed on the constituent models.<br>

<b>Raises</b><br>
* AttributeErrr  :  When fixed is not None<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>

Copy a Bracket Model.


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Brackets.html">Brackets</a></th></tr></thead></table>


* [<strong>baseResult(</strong> xdata, param )](./Brackets.md#baseResult)
* [<strong>basePartial(</strong> xdata, param, parlist=None )](./Brackets.md#basePartial)
* [<strong>baseDerivative(</strong> xdata, param )](./Brackets.md#baseDerivative)
* [<strong>setPrior(</strong> kpar, prior=None, **kwargs )](./Brackets.md#setPrior)
* [<strong>getPrior(</strong> kpar ) ](./Brackets.md#getPrior)
* [<strong>nextPrior(</strong> ) ](./Brackets.md#nextPrior)
* [<strong>basePrior(</strong> k ) ](./Brackets.md#basePrior)
* [<strong>hasPriors(</strong> isBound=True ) ](./Brackets.md#hasPriors)
* [<strong>baseParameterName(</strong> k )](./Brackets.md#baseParameterName)
* [<strong>baseParameterUnit(</strong> k )](./Brackets.md#baseParameterUnit)


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
* [<strong>getParameterName(</strong> kpar )](./Model.md#getParameterName)
* [<strong>getParameterUnit(</strong> kpar )](./Model.md#getParameterUnit)
* [<strong>getIntegralUnit(</strong> )](./Model.md#getIntegralUnit)
* [<strong>setLimits(</strong> lowLimits=None, highLimits=None )](./Model.md#setLimits)
* [<strong>getLimits(</strong> ) ](./Model.md#getLimits)
* [<strong>hasLimits(</strong> fitindex=None )](./Model.md#hasLimits)
* [<strong>unit2Domain(</strong> uvalue, kpar=None )](./Model.md#unit2Domain)
* [<strong>domain2Unit(</strong> dvalue, kpar=None )](./Model.md#domain2Unit)
* [<strong>partialDomain2Unit(</strong> dvalue )](./Model.md#partialDomain2Unit)
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
