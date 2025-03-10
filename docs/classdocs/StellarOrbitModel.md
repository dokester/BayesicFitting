---
---
<br><br>

<a name="StellarOrbitModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class StellarOrbitModel(</strong> <a href="./NonLinearModel.html">NonLinearModel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StellarOrbitModel.py target=_blank>Source</a></th></tr></thead></table>
<p>

Model for the radial velocity variations of a star caused by a orbiting planet.

The algorithm was taken from
&nbsp;&nbsp;&nbsp;&nbsp; Cory Boule etal. (2017) J. of Double Star Observations Vol 13 p.189.<br>
&nbsp;&nbsp;&nbsp;&nbsp; http://www.jdso.org/volume13/number2/Harfenist<sub>1</sub>89-199.pdf<br>

p<sub>0</sub> : e     eccentricity of the elliptic orbit (0<e<1; 0 = circular orbit)
p<sub>1</sub> : a     semi major axis (>0)
p<sub>2</sub> : P     period of the orbit (>0)
p<sub>3</sub> : T     phase since periastron passage (0<p<sub>3</sub><2pi)
p<sub>4</sub> : i     inclination of the orbit wrt sky (0<i<pi; 0 = pi = in sky plane)
p<sub>5</sub> : Omega position angle from North to the line of nodes (0<Omega<pi; 0 = north )
p<sub>6</sub> : omega longitude from the node (in p<sub>5</sub>) to the periastron (0<omega<2pi; 0 = periastron in node )

Due to the fact that the orbit can be mirrored in the sky plane, one of p<sub>5</sub> or p<sub>6</sub>
has to be limited to [0,pi] and the other to [0,2pi].

The parameters are initialized at [0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0].
It is a non-linear model.

This class uses [Kepplers](./Kepplers.md)2ndLaw to find the radius and anomaly.

<b>Attributes</b>

* keppler  :  Kepplers2ndLaw()<br>
&nbsp;&nbsp;&nbsp;&nbsp; to calculate the radius and true anomaly<br>
* ndout  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; The number of outputs is 2. Use [MultipleOutputProblem](./MultipleOutputProblem.md).<br>
* spherical  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; if True return the results in spherical coordinates.<br>
* cyclic  :  { 1 : 2*pi }<br>
&nbsp;&nbsp;&nbsp;&nbsp; Only if spherical, indicating that result[:,1] is cyclic.<br>

<b>Attributes from Model</b>

&nbsp;&nbsp;&nbsp;&nbsp; npchain, parameters, stdevs, xUnit, yUnit<br>

<b>Attributes from FixedModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist<br>

<b>Attributes from BaseModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames<br>

<b>Examples</b>

    sm = StellarOrbitModel( )
    print( sm.npars )
7



<a name="StellarOrbitModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>StellarOrbitModel(</strong> copy=None, spherical=True, **kwargs )
</th></tr></thead></table>
<p>

Radial velocity model.

Number of parameters is 5

<b>Parameters</b>

* copy  :  StellarOrbitModel<br>
&nbsp;&nbsp;&nbsp;&nbsp; model to copy<br>
* spherical  :  bool (True)<br>
&nbsp;&nbsp;&nbsp;&nbsp; produce output in sperical coordinates (rho,phi)<br>
&nbsp;&nbsp;&nbsp;&nbsp; otherwise in rectilinear coordinates (x,y)<br>
* fixed  :  dictionary of {int:float}<br>
&nbsp;&nbsp;&nbsp;&nbsp; int     list if parameters to fix permanently. Default None.<br>
&nbsp;&nbsp;&nbsp;&nbsp; float   list of values for the fixed parameters.<br>
&nbsp;&nbsp;&nbsp;&nbsp; Attribute fixed can only be set in the constructor.<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Copy method. 

<a name="baseResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseResult(</strong> xdata, params )
</th></tr></thead></table>
<p>

Returns the result of the model function.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.<br>

* p_0  :  e     eccentricity of the elliptic orbit (0<e<1; 0 = circular orbit)<br>
* p_1  :  a     semi major axis (>0)<br>
* p_2  :  P     period of the orbit (>0)<br>
* p_3  :  p     phase since periastron passage (0<p<2pi)<br>
* p_4  :  i     inclination of the orbit wrt sky (0<i<pi; 0 = orbit in sky plane)<br>
* p_5  :  Omega position angle of the line of nodes<br>
* p_6  :  omega longitude of periastron from lines of nodes<br>


<a name="toRect"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>toRect(</strong> rp )
</th></tr></thead></table>
<p>

Return (x,y) coordinates from (rho,phi)

<b>Parameters</b>

* rp  :  array<br>
&nbsp;&nbsp;&nbsp;&nbsp; rp[:,0] : separation of the stars<br>
    rp[:,1] : angle from north (down) CCW to east (right)

<a name="toSpher"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>toSpher(</strong> xy ) 
</th></tr></thead></table>
<p>

Return (rho,phi) coordinates from (x,y)

<b>Parameters</b>

* xy  :  array<br>
&nbsp;&nbsp;&nbsp;&nbsp; xy[:,0] : x position<br>
    xy[:,1] : y position

<a name="baseDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseDerivative(</strong> xdata, params )
</th></tr></thead></table>
<p>

Returns the derivative (df/dx) of the model function.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.<br>

* p_0  :  e     eccentricity of the elliptic orbit (0<e<1; 0 = circular orbit)<br>
* p_1  :  a     semi major axis (>0)<br>
* p_2  :  P     period of the orbit (>0)<br>
* p_3  :  p     phase since periastron passage (0<p<2pi)<br>
* p_4  :  i     inclination of the orbit wrt sky (0<i<pi; 0 = orbit in sky plane)<br>
* p_5  :  O(mega) position angle of the line of nodes (0<Omega<pi)<br>
* p_6  :  o(mega) longitude of periastron (0<omega<2pi)<br>


<a name="basePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePartial(</strong> xdata, params, parlist=None ) 
</th></tr></thead></table>
<p>

Returns the partials at the xdata value.
<br>
The partials are x ( xdata ) to degree-th power.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters. (not used for linear models)<br>
* parlist  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of indices active parameters (or None for all)<br>

* p_0  :  e     eccentricity of the elliptic orbit (0<e<1; 0 = circular orbit)<br>
* p_1  :  a     semi major axis<br>
* p_2  :  P     period of the orbit (>0)<br>
* p_3  :  p     phase since periastron passage (0<p<2pi)<br>
* p_4  :  i     inclination of the orbit wrt sky (0<i<pi; 0 = orbit in sky plane)<br>
* p_5  :  O     position angle of the line of nodes<br>
* p_6  :  o     longitude of periastron<br>


<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>
<p>

Returns a string representation of the model.


<a name="baseParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseParameterUnit(</strong> k )
</th></tr></thead></table>
<p>

Return the unit of a parameter. (TBC)

<b>Parameters</b>

* k  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; the kth parameter.<br>


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
* [<strong>baseParameterName(</strong> kpar ) ](./BaseModel.md#baseParameterName)
