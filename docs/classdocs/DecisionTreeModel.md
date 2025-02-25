---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/DecisionTreeModel.py target=_blank>Source</a></span></div>

<a name="DecisionTreeModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class DecisionTreeModel(</strong> <a href="./Modifiable.html">Modifiable,</a><a href="./Dynamic.html">Dynamic,</a><a href="./LinearModel.html">LinearModel</a> )
</th></tr></thead></table>
<p>

A DecisionTree Model (DTM) is mostly defined on multiple input dimensions (axes).
It splits the data in 2 parts, according low and high values on a certain input axis.
The splitting can continue along other axes.

The axes can contain float values, categorials (int) or booleans.
The float axes can have Nans when data are unkown.
Each category set one bit in an integer. The unknown category is a category
by itself.
Booleans that contain unknowns should be coded as categorial.

    f( x:p ) = DTM<br>
                 |-> left => DTM (or None)<br>
                 |-> rite => DTM (or None)<br>
                 |-> dimension<br>
                 |-> split or mask<br>

The tree is searched left to right.

The parameters are all initialized at 0.0

<b>Examples</b>

    dtm = DecisionTreeModel( )<br>
    print( dtm )<br>
* DecisionTree :  with 0 components and 1 parameters<br>

<b>Attributes</b>

* left  :  None or DTM<br>
    a None the tree stops otherwise there is a new split.<br>
* rite  :  None or DTM<br>
    a None the tree stops otherwise there is a new split.<br>
* dimension  :  int<br>
    split according to data values on this axes<br>
* itype  :  char. Either 'f' (float), 'i' (integer), or 'b' (boolean)<br>
    characterizes the input dimension as float, integer or boolean<br>
* split  :  float between 0 and 1 (for float dimension)<br>
    to the left normalized values < split; to the rite normvalues > split.<br>
    Unknown values (NaNs to to the smallest faction).<br>
* nsplit  :  int<br>
    number of calls to random.rand() to be averaged. Prior on "split"<br>
* mask  :  float between 0 and 1 (for float dimension)<br>
    to the left normalized values < split; to the rite normvalues > split.<br>
    Unknown values (NaNs to to the smallest faction.<br>

<b>Attributes from Modifiable</b>

    modifiable<br>

<b>Attributes from Dynamic</b>

    dynamic<br>

<b>Attributes from Model</b>

    npchain, parameters, stdevs, xUnit, yUnit<br>

<b>Attributes from FixedModel</b>

    npmax, fixed, parlist, mlist<br>

<b>Attributes from BaseModel</b>

    npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames<br>


<a name="DecisionTreeModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>DecisionTreeModel(</strong> ndim=1, depth=0, split=0.5, kdim=0, itypes=[0], modifiable=True,
 dynamic=True, code=None, growPrior=None, copy=None, **kwargs )
</th></tr></thead></table>
<p>

DecisionTree model.

The DTM standardly has a UniformPrior for all parameters, with limits [0,1]

<b>Parameters</b>

* ndim  :  int<br>
    number of input dimensions<br>
* depth  :  int<br>
    depth of the tree<br>
* kdim  :  None or list of ints<br>
    input channel to be splitted.<br>
* itypes  :  [list of] int<br>
    indicating the type of input: 0 for float, 1 for boolean, >1 for categorial<br>
    The last number is repeated for remaining inputs<br>
* split  :  None or float or list of floats<br>
    fraction (0<s<1) of the input kdim that falls on either side.<br>
* growPrior  :  None or Prior<br>
    Governing the growth<br>
* modifiable  :  bool (True)<br>
    Will the model modify dimension and/or split/mask<br>
* dynamic  :  bool (True)<br>
    Will the model grow/shrink<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Copy method. 

<a name="setSplitOrMask"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>setSplitOrMask(</strong> itype, split ) 
</th></tr></thead></table>
<p>
For internal use only 

<a name="isLeaf"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>isLeaf(</strong> ) 
</th></tr></thead></table>
<p>

Return true if self is a leaf

<a name="partitionList"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>partitionList(</strong> xdata, plist ) 
</th></tr></thead></table>
<p>

Partition the xdata in plist over 2 new lists according to the DTM-branch.

<b>Paramaters</b>

* xdata  :  array-like<br>
    the xdata<br>
* plist  :  array of ints<br>
    indices in xdata<br>

<b>Return</b>

* pl1, pl2  :  2 lists<br>
    together containing all indices in plist

<a name="baseResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>baseResult(</strong> xdata, params )
</th></tr></thead></table>
<p>

Returns the result of the model function.

<b>Parameters</b>

* xdata  :  array_like<br>
    values at which to calculate the result<br>
* params  :  array_like<br>
    values for the parameters.<br>


<a name="recursiveResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>recursiveResult(</strong> xdata, params, kpar, plist, res ) 
</th></tr></thead></table>
<p>
For internal use only 

<a name="basePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>basePartial(</strong> xdata, params, parlist=None )
</th></tr></thead></table>
<p>

Returns the partials at the input value.

<b>Parameters</b>

* xdata  :  array_like<br>
    values at which to calculate the partials<br>
* params  :  array_like<br>
    values for the parameters.<br>
* parlist  :  array_like<br>
    list of indices active parameters (or None for all)<br>


<a name="recursivePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>recursivePartial(</strong> xdata, kpar, plist, part ) 
</th></tr></thead></table>
<p>
For internal use only 

<a name="sortXdata"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>sortXdata(</strong> xdata )
</th></tr></thead></table>
<p>

Reorder the xdata according to the parameter ordering

<b>Parameters</b>

* xdata  :  array_like<br>
    values at which to calculate the partials<br>


<a name="recursiveOrder"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>recursiveOrder(</strong> xdata, plist ) 
</th></tr></thead></table>
<p>
For internal use only 

<a name="baseDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>baseDerivative(</strong> xdata, params ) 
</th></tr></thead></table>
<p>

Return the derivative df/dx at each xdata (=x).

<b>Parameters</b>

* xdata  :  array_like<br>
    values at which to calculate the result<br>
* params  :  array_like<br>
    values for the parameters.<br>


<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>
<p>

Returns a string representation of the model.


<a name="fullName"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>fullName(</strong> ids=False )
</th></tr></thead></table>
<p>

Returns a string representation of the model.

<b>Parameters</b>

* ids  :  bool<br>
    if True give the pointers of the links too.<br>


<a name="recursiveName"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>recursiveName(</strong> name, indent, kpar, ids=False ) 
</th></tr></thead></table>
<p>
For internal use only 

<a name="baseParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>baseParameterUnit(</strong> k )
</th></tr></thead></table>
<p>

Return the unit of the indicated parameter.

<b>Parameters</b>

* k  :  int<br>
    parameter number.<br>


<a name="walk"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>walk(</strong> )
</th></tr></thead></table>
<p>

Iterate tree in pre-order depth-first search order

Found this piece of code on the internet. Fairly obscure.

<a name="encode"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>encode(</strong> ) 
</th></tr></thead></table>
<p>

Make a code tuple to be used by the constructor to resurrect the DTM
The tuple consists of
code : list of (list or 1 or 2), encoding the structure of DTM
dims : list of dimensions at the branches
splim : list of split/mask values at the branches


<a name="decode"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>decode(</strong> code, kdim, splim, kbr ) 
</th></tr></thead></table>
<p>

Resurrect the DTM from the code generated by encode().
For internal use in the Constructor.

<b>Parameters</b>

* code  :  list<br>
    of (list or 1 or 2), encoding the structure of DTM<br>
* dims  :  list<br>
    of dimensions at the branches<br>
* splim  :  list<br>
    of split/mask values at the branches<br>
* kbr  :  int<br>
    counter (start at 0)

<a name="findLeaf"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>findLeaf(</strong> kleaf ) 
</th></tr></thead></table>
<p>

Find a leaf in the tree, returning the leaf.

<b>Parameter</b>

* kleaf  :  int<br>
    index of the leaf to be found

<a name="findBranch"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>findBranch(</strong> kbranch ) 
</th></tr></thead></table>
<p>

Find a branch in the tree, returning the branch.

<b>Parameter</b>

* kbranch  :  int<br>
    index of the branch to be found

<a name="check"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>check(</strong> ) 
</th></tr></thead></table>
<p>

Find a branch in the tree, returning the branch.

<b>Parameter</b>

* kbranch  :  int<br>
    index of the branch to be found

<a name="findRoot"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>findRoot(</strong> ) 
</th></tr></thead></table>
<p>

Return the root of the tree.


<a name="count"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>count(</strong> ) 
</th></tr></thead></table>
<p>

Return number of leafs and branches.

<a name="countLeaf"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>countLeaf(</strong> ) 
</th></tr></thead></table>
<p>

Return number of leafs.

<a name="countBranch"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>countBranch(</strong> ) 
</th></tr></thead></table>
<p>

Return number of leafs.

<a name="grow"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>grow(</strong> offset=0, rng=None, location=0, split=0.5, kdim=0 )
</th></tr></thead></table>
<p>

Increase the the number of components by 1 (if allowed by maxComp)

<b>Parameters</b>

* offset  :  int<br>
    offset in the parameter list (pertaining to earlier models in the chain)<br>
* rng  :  Random Number Generator<br>
    to obtain random values for items below.<br>
* location  :  int<br>
    location where the new dtm-leaf should be inserted<br>
* kdim  :  int (<self.ndim)<br>
    dimension to split<br>
* split  :  float (0<split<1)<br>
    relative cut on this dimension<br>

<b>Return</b>

* bool  :   succes<br>


<a name="shrink"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>shrink(</strong> offset=0, rng=None, location=0 )
</th></tr></thead></table>
<p>

Decrease the the number of componenets by 1 (if allowed by minComp)
Remove an arbitrary item.

<b>Parameters</b>

* offset  :  int<br>
    location where the new params should be inserted<br>

<b>Return</b>

* bool  :  succes<br>


<a name="vary"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>vary(</strong> rng=None, location=0, split=0.5, kdim=0 )
</th></tr></thead></table>
<p>

Vary the model structure by changing kdim and/or split at location

<b>Parameters</b>

* rng  :  Random Number Generator<br>
    to obtain random values for items below.<br>
* location  :  int<br>
    location where the dtm-branch should be changed<br>
* kdim  :  int (<self.ndim)<br>
    dimension to split<br>
* split  :  float (0<split<1)<br>
    relative cut on this dimension<br>

<b>Return</b>

* bool  :   succes<br>


<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Modifiable.html">Modifiable,</a></th></tr></thead></table>


* [<strong>isModifiable(</strong> ) ](./Modifiable.md#isModifiable)
<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Dynamic.html">Dynamic,</a></th></tr></thead></table>


* [<strong>isDynamic(</strong> ) ](./Dynamic.md#isDynamic)
* [<strong>setGrowPrior(</strong> growPrior=None, min=1, max=None, name="Comp" ) ](./Dynamic.md#setGrowPrior)
* [<strong>setDynamicAttribute(</strong> name, value ) ](./Dynamic.md#setDynamicAttribute)
* [<strong>alterParameterNames(</strong> dnp ) ](./Dynamic.md#alterParameterNames)
* [<strong>alterParameterSize(</strong> dnp, offset, location=None, value=0 ) ](./Dynamic.md#alterParameterSize)
* [<strong>alterParameters(</strong> param, location, dnp, offset, value=None ) ](./Dynamic.md#alterParameters)
* [<strong>alterFitindex(</strong> findex, location, dnp, offset ) ](./Dynamic.md#alterFitindex)
* [<strong>shuffle(</strong> param, offset, np, rng ) ](./Dynamic.md#shuffle)
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
