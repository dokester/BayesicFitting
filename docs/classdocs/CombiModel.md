---
---
<br><br>

<a name="CombiModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class CombiModel(</strong> <a href="./BracketModel.html">BracketModel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/CombiModel.py target=_blank>Source</a></th></tr></thead></table>

CombiModel combines a number of copies of the same model.

Fixed relations can be set between similar parameters.
The relations can be either multiplicative or additive.
When these relations are set, they must be set for all models.

&nbsp; f( x:p ) = &sum; g( x:p )

where g( x:p ) is a model ( e.g. GaussModel )

For consistency reasons it is not possible to change the attributes of a
CombiModel. It is better to make a new one with the required settings.

As we have copies of the same model, each model can have its own priors.

<b>Attributes</b>

* nrepeat  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of Models in this CombiModel
* nmp  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of parameters in each Model
* expandpar  :  array of float
<br>&nbsp;&nbsp;&nbsp;&nbsp; expanded parameters. to be used in the repeated models
* npcmax  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of parameters in expandpar (= nmp * nrepeat)
* expandindex  :  array of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; converts parameter index into expandpar index
* addindex  :  array of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of additively connected parameters
* addvalue  :  array of float
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of values to be added to the parameters in addindex
* mulindex  :  array of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of multiplicatively connected parameters
* mulvalue  :  array of float
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of values to be multiplied to the parameters in mulindex
* select  :  array of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of expandpar to get parameters

<b>Attributes from BracketModel</b>

&nbsp; model, deep

<b>Attributes from Model</b>

&nbsp; npchain, parameters, stdevs, xUnit, yUnit

<b>Attributes from FixedModel</b>

&nbsp; npmax, fixed, parlist, mlist

<b>Attributes from BaseModel</b>

&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames


<b>Examples</b>

    gauss = GaussModel( )
    combi = CombiModel( gauss, 3, addCombi={1:[0,0.1,0.3]}, mulCombi={2,[0]*3} )
    print( combi )
    Combi of 3 times GaussModel
    print( combi.npchain, combi.nrepeat, combi.nmp, combi.nexpand )
    5 3 3 9
    print( combi.select )
    [0 1 2 3 6]
    print( combi.expandindex )
    [0 1 2 3 1 2 4 1 2]
    print( combi.modelindex )
    [0 0 0 1 2]
    print( combi.addindex )
    [1 4 7]
    print( combi.mulindex )
    [2 5 8]

Category     mathematics/Fitting

<b>Notes</b>

1. When all parameters are left free, precise initial parameters are
needed to converge to the global optimum.
2. The model seems to be especially unstable when the basic models
are overlapping. Fixing the widths relative to each other, helps.
3. Using a PolynomialModel ( or similar ones ) as basic model, is not going
to work.


<a name="CombiModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>CombiModel(</strong> model, nrepeat=1, copy=None, oper='add',
 addCombi=None, mulCombi=None, **kwargs )
</th></tr></thead></table>

CombiModel combines several copies of the same model int one.

<b>Parameters</b>

* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to be repeated
* nrepeat  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of repetitions
* oper  :  "add" or "mul"
<br>&nbsp;&nbsp;&nbsp;&nbsp; the repeated models are combined using this operation
* addCombi  :  None or dict
<br>&nbsp;&nbsp;&nbsp;&nbsp; make additive connections between parameters
<br>&nbsp;&nbsp;&nbsp;&nbsp; None : no additive connection
<br>&nbsp;&nbsp;&nbsp;&nbsp; dict : { int : array }
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; key : int
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; index pointing to the key-th parameter in the model
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; value : array of nrepeat floats
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; values added to each of the key-th parameters
* mulCombi  :  None or dict
<br>&nbsp;&nbsp;&nbsp;&nbsp; make multiplicative connections between parameters
<br>&nbsp;&nbsp;&nbsp;&nbsp; None : no multiplicative connection
<br>&nbsp;&nbsp;&nbsp;&nbsp; dict : { int : array }
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; key : int
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; index pointing to the key-th parameter in the model
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; value : array of nrepeat floats
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; values  multiplied to each of the key-th parameters


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>

Copy method. 
<a name="combine"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>combine(</strong> addCombi=None, mulCombi=None ) 
</th></tr></thead></table>
(re)sets the value of attributes "addindex", "addvalue", "mulindex", "mulvalue",
"select" and "expandindex".

<b>Parameters</b>

* addCombi  :  None or dict
<br>&nbsp;&nbsp;&nbsp;&nbsp; make additive connections between parameters
<br>&nbsp;&nbsp;&nbsp;&nbsp; None : no additive connection
<br>&nbsp;&nbsp;&nbsp;&nbsp; dict : { int : array }
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; key : int
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; index pointing to the key-th parameter in the model
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; value : array of nrepeat floats
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; values added to each of the key-th parameters
* mulCombi  :  None or dict
<br>&nbsp;&nbsp;&nbsp;&nbsp; make multiplicative connections between parameters
<br>&nbsp;&nbsp;&nbsp;&nbsp; None : no multiplicative connection
<br>&nbsp;&nbsp;&nbsp;&nbsp; dict : { int : array }
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; key : int
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; index pointing to the key-th parameter in the model
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; value : array of nrepeat floats
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; values  multiplied to each of the key-th parameters


<a name="makeExpandIndex"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makeExpandIndex(</strong> expandindex, amindex ) 
</th></tr></thead></table>
Make an expanded index enumerating the parameters for the full model

<a name="setCombi"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setCombi(</strong> combi ) 
</th></tr></thead></table>

<a name="expandParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>expandParameters(</strong> param ) 
</th></tr></thead></table>

<a name="baseResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseResult(</strong> xdata, params ) 
</th></tr></thead></table>
Returns the result calculated at the xdatas.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.


<a name="basePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePartial(</strong> xdata, params, parlist=None ) 
</th></tr></thead></table>
Returns the partial derivatives calculated at the xdatas.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the partials
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.
* parlist  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; Not in use


<a name="baseDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseDerivative(</strong> xdata, params ) 
</th></tr></thead></table>
Returns the derivative (df/dx) calculated at the xdatas.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the partials
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.


<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>

Returns a string representation of the model. 
<a name="baseParameterName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseParameterName(</strong> kpar )
</th></tr></thead></table>
Return the name of the indicated parameter.

<b>Parameters</b>

* kpar  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter number.


<a name="baseParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseParameterUnit(</strong> k )
</th></tr></thead></table>
Return the unit of the indicated parameter.

<b>Parameters</b>

* k  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter number.


<a name="getPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getPrior(</strong> kpar ) 
</th></tr></thead></table>
Return the prior for parameter kpar.

First try at the kpar location, possibly further in the chain;
Upon failure try at the equivalent position in the head model

<b>Parameters</b>

* kpar  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index of the parameter to be selected.

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./BracketModel.html">BracketModel</a></th></tr></thead></table>




<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Brackets.html">Brackets</a></th></tr></thead></table>


* [<strong>setPrior(</strong> kpar, prior=None, **kwargs )](./Brackets.md#setPrior)
* [<strong>nextPrior(</strong> ) ](./Brackets.md#nextPrior)
* [<strong>basePrior(</strong> k ) ](./Brackets.md#basePrior)
* [<strong>hasPriors(</strong> isBound=True ) ](./Brackets.md#hasPriors)


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
