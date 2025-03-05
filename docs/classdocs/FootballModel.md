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

&nbsp;&nbsp;&nbsp; name                    limits    default    comment<br>
0. Number of trials      0 < a         n/a     trials on the goal of the opponent
1. Defensive strength    0 < b < 1      0      fraction of the trials that is stopped
2. Midfield strength     0 < c < 2      1      relative strength of the team
3. Home advantage        0 < d < 2      1      advantage of playing at home
4. Strategy              0 < e < 2      1      

Note: Computational runtime errors/warnings occur when (some of) the parameters are at 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; their limits. <br>

The default values are chosen such that they dont have effect on the results.
I.e. a model with complexity=5 and all parameters at the defaults except for 
"trials", has the same result as a model with complexity 1 with the same "trials"
value.

Let p1 denote the parameters of the home team and p2 those of the away team,
then the equations for calculating the strengths, S1 and S2, are

&nbsp;&nbsp;&nbsp;&nbsp; S1 = a1 * sqrt( c1 * d1 / c2 ) * ( 1 - b2 ^ ( c1 * d1 / c2 ) )<br>

&nbsp;&nbsp;&nbsp;&nbsp; S2 = a2 * sqrt( c2 / ( c1 * d1 ) ) * ( 1 - b1 ^ ( c2 / ( c1 * d1 ) )<br>


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
attack 

<a name="goals2"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>goals2(</strong> xdata, par ) 
</th></tr></thead></table>
<p>
attack, defense 

<a name="goals3"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>goals3(</strong> xdata, par ) 
</th></tr></thead></table>
<p>
attack, defense, midfield 

<a name="goals4"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>goals4(</strong> xdata, par ) 
</th></tr></thead></table>
<p>
attack, defense, midfield, home 

<a name="goals5"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>goals5(</strong> xdata, par ) 
</th></tr></thead></table>
<p>

attack, defense, midfield, home, strategy 


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
&nbsp;&nbsp;&nbsp;&nbsp; list of indices of active parameters<br>

to a1
(1-b_2^((c_1*d_1)/(c_2*f_2)))*sqrt((c_1*d_1)/c_2)
to b2
-(a_1*c_1*d_1*sqrt((c_1*d_1)/c_2)*b_2^((c_1*d_1)/(c_2*f_2)-1))/(c_2*f_2)
to c1
-(a_1*d_1*(2*b_2^((d_1*c_1)/(c_2*f_2))*log(b_2)*d_1*c_1+(b_2^((d_1*c_1)/(c_2*f_2))-1)
&nbsp;&nbsp;&nbsp;&nbsp; *c_2*f_2))/(2*c_2^2*f_2*sqrt((d_1*c_1)/c_2))<br>
to c2
(a_1*c_1*d_1*((b_2^((c_1*d_1)/(f_2*c_2))-1)*f_2*c_2+2*b_2^((c_1*d_1)/(f_2*c_2))*
&nbsp;&nbsp;&nbsp;&nbsp; log(b_2)*c_1*d_1))/(2*f_2*sqrt((c_1*d_1)/c_2)*c_2^3)<br>
to d1
-(a_1*c_1*(2*b_2^((c_1*d_1)/(c_2*f_2))*log(b_2)*c_1*d_1+(b_2^((c_1*d_1)/(c_2*f_2))-1)*
&nbsp;&nbsp;&nbsp;&nbsp; c_2*f_2))/(2*c_2^2*f_2*sqrt((c_1*d_1)/c_2))<br>
to f2
(a_1*b_2^((c_1*d_1)/(c_2*f_2))*log(b_2)*c_1*d_1*sqrt((c_1*d_1)/c_2))/(c_2*f_2^2)

<a name="part1"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>part1(</strong> xdata, par ) 
</th></tr></thead></table>
<p>
<a name="part2"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>part2(</strong> xdata, par ) 
</th></tr></thead></table>
<p>
<a name="part3"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>part3(</strong> xdata, par ) 
</th></tr></thead></table>
<p>
<a name="part4"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>part4(</strong> xdata, par ) 
</th></tr></thead></table>
<p>
<a name="part5"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>part5(</strong> xdata, par ) 
</th></tr></thead></table>
<p>

Derivatives copies from https://www.derivative-calculator.net

Fh = a0*sqrt((d0*f0*c0)/c1) * (1-b1**((d0*f1*c0)/c1))
Fa = a1*sqrt((c1*f1)/(c0*d0)) * (1-b0**((c1*f0)/(c0*d0)))

dFh/da0 = (1-b1**((d0*f1*c0)/c1))*sqrt((d0*f0*c0)/c1)
dFh/da1 = 0
dFh/db0 = 0
dFh/db1 = -(a0*c0*d0* sqrt((c0*d0*f0)/c1) *f1* b1**((c0*d0*f1)/c1-1)) / c1
dFh/dc0 = -(a0*d0*f0*(2*b1**((d0*f1*c0)/c1)*log(b1)*d0*f1*c0+
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (b1**((d0*f1*c0)/c1)-1)*c1))/(2*c1**2*sqrt((d0*f0*c0)/c1))<br>
dFh/dc1 = (a0*c0*d0*f0*((b1**((c0*d0*f1)/c1)-1)*c1+2*b1**((c0*d0*f1)/c1)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *log(b1)*c0*d0*f1))/(2*sqrt((c0*d0*f0)/c1)*c1**3)<br>
dFh/dd0 = -(a0*c0*f0*(2*b1**((c0*f1*d0)/c1)*log(b1)*c0*f1*d0+
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (b1**((c0*f1*d0)/c1)-1)*c1))/(2*c1**2*sqrt((c0*f0*d0)/c1))<br>
dFh/dd1 = 0
dFh/df0 = (a0*(1-b1**((c0*d0*f1)/c1))*c0*d0)/(2*c1*sqrt((c0*d0*f0)/c1))
dFh/df1 = -(a0*b1**((c0*d0*f1)/c1)*log(b1)*c0*d0*sqrt((c0*d0*f0)/c1))/c1

dFa/da0 = 0
dFa/da1 = (1-b0**((c1*f0)/(c0*d0)))*sqrt((c1*f1)/(c0*d0))
dFa/db0 = -(a1*c1*f0*sqrt((c1*f1)/(c0*d0))*b0**((c1*f0)/
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (c0*d0)-1))/(c0*d0)<br>
dFa/db1 = 0
dFa/dc0 = (a1*c1*f1*((b0**((c1*f0)/(d0*c0))-1)*d0*c0+2*
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; b0**((c1*f0)/(d0*c0))*log(b0)*c1*f0))/(2*d0**2*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; sqrt((c1*f1)/(d0*c0))*c0**3)<br>
dFa/dc1 = -(a1*f1*(2*b0**((f0*c1)/(c0*d0))*log(b0)*f0*c1+
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (b0**((f0*c1)/(c0*d0))-1)*c0*d0))/(2*c0**2*d0**2*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; sqrt((f1*c1)/(c0*d0)))<br>
dFa/dd0 = (a1*c1*f1*((b0**((c1*f0)/(c0*d0))-1)*c0*d0+2*
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; b0**((c1*f0)/(c0*d0))*log(b0)*c1*f0))/(2*c0**2*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; sqrt((c1*f1)/(c0*d0))*d0**3)<br>
dFa/dd1 = 0
dFa/df0 = -(a1*b0**((c1*f0)/(c0*d0))*log(b0)*c1*
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; sqrt((c1*f1)/(c0*d0)))/(c0*d0)<br>
dFa/df1 = (a1*(1-b0**((c1*f0)/(c0*d0)))*c1)/(2*c0*d0*
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; sqrt((c1*f1)/(c0*d0)))<br>


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
