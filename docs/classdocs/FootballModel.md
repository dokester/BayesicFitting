---
---
<br><br>

<a name="FootballModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class FootballModel(</strong> <a href="./NonLinearModel.html">NonLinearModel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/FootballModel.py target=_blank>Source</a></th></tr></thead></table>
<p>

More or less complex model for the outcome of football marches.

The input values are a (nteams,2) list of integers. They represent 
teams that play a match, the first at home the other away.

For each team the complexity lists parameters

| name              |complexity| limits |default| comment                      |
|:------------------|:--------:|:------:|:-----:|:-----------------------------|
| Attack            |    1     |  0<a   |  n/a  | trials on the goal           |
| Defensive strength|    2     |  0<b<1 |   0   | fraction of trials stopped   |
| Midfield strength |    3     |  0<c<2 |   1   | relative strength of the team|
| Home advantage    |    4     |  0<d<2 |   1   | advantage of playing at home |
| Strategy          |    5     |  0<e<2 |   1   | defensive <-> offensive      |


Note: Computational runtime errors/warnings occur when (some of) the parameters are at 
their limits. 

The default values are chosen such that they dont have effect on the results.
I.e. a model with complexity=5 and all parameters at the defaults except for 
"trials", has the same result as a model with complexity 1 with the same "trials"
value.

For information what is calculated at each level of complexity, see info at 
the methods goals1(), goals2(), ... goals5(), below.

Note
This is about the game that most of the world calls football.

<b>Examples</b>

    fm = FootballModel( 18 ) 
    print( fm.npars )
    90

* Author  :  Do Kester<br>

<b>Attributes</b>

* nteams  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of teams<br>
* complexity  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; degree of complexity, default = 5.<br>

<b>Attributes from Model</b>

&nbsp;&nbsp;&nbsp;&nbsp; npchain, parameters, stdevs, xUnit, yUnit<br>

<b>Attributes from FixedModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist<br>

<b>Attributes from BaseModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames<br>



<a name="FootballModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>FootballModel(</strong> nteams, complexity=5, copy=None, **kwargs )
</th></tr></thead></table>
<p>

Calculate the score of football matches

The number of parameters is ( nteams * complexity )

<b>Parameters</b>

* nteams  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of teams<br>
* complexity  :  1 <= int <= 5<br>
&nbsp;&nbsp;&nbsp;&nbsp; of the model<br>
* copy  :  FootballModel<br>
&nbsp;&nbsp;&nbsp;&nbsp; model to copy<br>
* fixed  :  None or dictionary of {int:float|Model}<br>
&nbsp;&nbsp;&nbsp;&nbsp; int         index of parameter to fix permanently.<br>
&nbsp;&nbsp;&nbsp;&nbsp; float|Model values for the fixed parameters.<br>
&nbsp;&nbsp;&nbsp;&nbsp; Attribute fixed can only be set in the constructor.<br>
&nbsp;&nbsp;&nbsp;&nbsp; See: [FixedModel](./FixedModel.md)<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Copy method. 

<a name="getPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getPrior(</strong> k ) 
</th></tr></thead></table>
<p>

Return the prior of the parameter, indicated by k modulo the complexity

<b>Parameters</b>

* k  :  int<br>
    parameter number.

<a name="goals1"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>goals1(</strong> xdata, par ) 
</th></tr></thead></table>
<p>

Consider attack (a) only.

&nbsp; S1 = a1<br>
&nbsp; S2 = a2<br>

<b>Parameters</b>

* xdata  :  array of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of matches team 1 vs team 2<br>
* par  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; attack values<br>


<a name="goals2"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>goals2(</strong> xdata, par ) 
</th></tr></thead></table>
<p>

Consider attack (a) and defense (d).

&nbsp; S1 = a1 * ( 1 - d2 )<br>
&nbsp; S2 = a2 * ( 1 - d1 )<br>

<b>Parameters</b>

* xdata  :  array of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of matches team 1 vs team 2<br>
* par  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; team values<br>


<a name="goals3"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>goals3(</strong> xdata, par ) 
</th></tr></thead></table>
<p>

Consider attack (a), defense (d) and midfield (m).

The ratio of the midfield strength modifies attack and defense

&nbsp; S1 = a1 * &radic;(m1/m2) * ( 1 - d2 ^ (m2/m1) )<br>
&nbsp; S2 = a2 * &radic;(m2/m1) * ( 1 - d1 ^ (m1/m2) )<br>

<b>Parameters</b>

* xdata  :  array of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of matches team 1 vs team 2<br>
* par  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; team values<br>


<a name="goals4"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>goals4(</strong> xdata, par ) 
</th></tr></thead></table>
<p>

Consider attack (a), defense (d), midfield (m) and home advantage (h).

The strategy modifies the midfield strangth of the home team.

&nbsp; mh = m1 * h1<br>
&nbsp; S1 = a1 * &radic;(mh/m2) * ( 1 - d2 ^ (m2/mh) )<br>
&nbsp; S2 = a2 * &radic;(m2/mh) * ( 1 - d1 ^ (mh/m2) )<br>

<b>Parameters</b>

* xdata  :  array of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of matches team 1 vs team 2<br>
* par  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; team values<br>


<a name="goals5"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>goals5(</strong> xdata, par ) 
</th></tr></thead></table>
<p>

Consider attack (a), defense (d), midfield (m), home advantage (h),
and strategy (s)

&nbsp; A offensive strategy (s>1) strenghtens the attach and weakens the defense. <br>
&nbsp; A defensive strategy (s<1) strenghtens the defense and weakens the attack. <br>

&nbsp; mh = m1 * h1<br>
&nbsp; S1 = a1 * &radic;(s1*mh/m2) * ( 1 - d2 ^ (s2*m2/mh) )<br>
&nbsp; S2 = a2 * &radic;(s2*m2/mh) * ( 1 - d1 ^ (s1*mh/m2) )<br>

<b>Parameters</b>

* xdata  :  array of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of matches team 1 vs team 2<br>
* par  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; team values<br>


<a name="baseResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseResult(</strong> xdata, params )
</th></tr></thead></table>
<p>

Returns the partials at the input value.

The partials are the powers of x ( xdata ) from 0 to degree.

<b>Parameters</b>

* xdata  :  array_like [2:nteams]<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of team ids playing against each other.<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model <br>


<a name="basePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePartial(</strong> xdata, params, parlist=None )
</th></tr></thead></table>
<p>

Returns the partials at the input value.

The partials are the powers of x ( xdata ) from 0 to degree.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the partials<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model (ignored for LinearModels).<br>
* parlist  :  array_like<br>
    list of indices of active parameters

<a name="part1"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>part1(</strong> xdata, par ) 
</th></tr></thead></table>
<p>

Derivatives copies from https://www.derivative-calculator.net

<b>Parameters</b>

* xdata  :  array_like [2:nteams]<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of team ids playing against each other.<br>
* par  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model <br>


<a name="part2"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>part2(</strong> xdata, par ) 
</th></tr></thead></table>
<p>

Derivatives copies from https://www.derivative-calculator.net

<b>Parameters</b>

* xdata  :  array_like [2:nteams]<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of team ids playing against each other.<br>
* par  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model <br>


<a name="part3"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>part3(</strong> xdata, par ) 
</th></tr></thead></table>
<p>

Derivatives copies from https://www.derivative-calculator.net

<b>Parameters</b>

* xdata  :  array_like [2:nteams]<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of team ids playing against each other.<br>
* par  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model <br>


<a name="part4"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>part4(</strong> xdata, par ) 
</th></tr></thead></table>
<p>

Derivatives copies from https://www.derivative-calculator.net

<b>Parameters</b>

* xdata  :  array_like [2:nteams]<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of team ids playing against each other.<br>
* par  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model <br>


<a name="part5"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>part5(</strong> xdata, par ) 
</th></tr></thead></table>
<p>

Derivatives copies from https://www.derivative-calculator.net

<b>Parameters</b>

* xdata  :  array_like [2:nteams]<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of team ids playing against each other.<br>
* par  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model <br>


<a name="baseDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseDerivative(</strong> xdata, params ) 
</th></tr></thead></table>
<p>

Return the derivative df/dx at each input (=x).

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the partials<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model.<br>


<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>
<p>

Returns a string representation of the model.


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


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./NonLinearModel.html">NonLinearModel</a></th></tr></thead></table>


* [<strong>setMixedModel(</strong> lindex )](./NonLinearModel.md#setMixedModel)
* [<strong>isMixed(</strong> )](./NonLinearModel.md#isMixed)
* [<strong>getNonLinearIndex(</strong> )](./NonLinearModel.md#getNonLinearIndex)
* [<strong>partial(</strong> xdata, param=None, useNum=False )](./NonLinearModel.md#partial)


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
