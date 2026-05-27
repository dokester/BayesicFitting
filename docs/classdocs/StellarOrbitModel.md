---
---
<br><br>

<a name="StellarOrbitModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class StellarOrbitModel(</strong> <a href="./NonLinearModel.html">NonLinearModel</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StellarOrbitModel.py target=_blank>[source]</a></th></tr></thead></table>
<p>

Model for the radial velocity variations of a star caused by a orbiting planet.

The algorithm was taken from Cory Boule etal. (2017) 
J. of Double Star Observations Vol 13 p.189. [Boule](../references.md#boule)

| par |symbol | description                        | limits  | comment |
|-----|-------|------------------------------------|---------|---------|
| p<sub>0</sub> |   e   | eccentricity of the elliptic orbit | 0<e<1   | 0 = circular orbit |
| p<sub>1</sub> |   a   | semi major axis                    |   a>0   |                      |
| p<sub>2</sub> |   P   | period of the orbit                |   P>0   |                      |
| p<sub>3</sub> |   T   | phase since periastron passage     |0<T<2&pi;|                      |
| p<sub>4</sub> |   i   | inclination of the orbit wrt sky   |0<i<&pi; | 0 = pi = in sky plane|
| p<sub>5</sub> |&Omega;| position angle from North          |         |                      |
|     |       |     to the line of nodes         |0<&Omega;<&pi;| 0 = north         |
| p<sub>6</sub> |&omega;| longitude from the node (in p<sub>5</sub>) |              |                   |
|     |       |     to the periastron         |0<&omega;<2&pi;| 0 = periastron in node|

Due to the fact that the orbit can be mirrored in the sky plane, one of p<sub>5</sub> or p<sub>6</sub>
has to be limited to [0,pi] and the other to [0,2pi]. However it could be preferred to
keep the inclination between [0,pi] as it keeps the ascending node at the same place.
All parameter from 3 on, are cyclic and would profit from a circular prior. 

The parameters are initialized at [0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0].
It is a non-linear model.

This class uses [Kepplers2ndLaw to find the radius and anomaly.](Kepplers2ndLaw to find the radius and anomaly.)

<b>Attributes</b><br>
* keppler  :  Kepplers2ndLaw()
<br>&nbsp;&nbsp;&nbsp;&nbsp; to calculate the radius and true anomaly
* ndout  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; The number of outputs is 2. Use [MultipleOutputProblem.](MultipleOutputProblem.)
* spherical  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; if True return the results in spherical coordinates, as [rho,phi]
<br>&nbsp;&nbsp;&nbsp;&nbsp; otherwise return euclidian coordinates [x,y]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Angles are measured counterclockwise from north to east
<br>&nbsp;&nbsp;&nbsp;&nbsp; North is Down (-y) and East is to the Right (+x)
* cyclic  :  { 1 : 2*pi }
<br>&nbsp;&nbsp;&nbsp;&nbsp; Only if spherical, indicating that result[:,1] is cyclic.
* toRect  :  Tools.toRect
<br>&nbsp;&nbsp;&nbsp;&nbsp; Return (x,y) coordinates from (rho,phi). See [Tools](./Tools.md#toRect)
* toSpher  :  Tools.toSpher
<br>&nbsp;&nbsp;&nbsp;&nbsp; Return (rho,phi) coordinates from (x,y). See [Tools](./Tools.md#toSpher)

<b>Attributes from Model</b><br>
&nbsp;&nbsp;&nbsp;&nbsp; npchain, parameters, stdevs, xUnit, yUnit

<b>Attributes from FixedModel</b><br>
&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist

<b>Attributes from BaseModel</b><br>
&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames

<b>Examples</b>

    sm = StellarOrbitModel( )
    print( sm.npars )
    7



<a name="StellarOrbitModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>StellarOrbitModel(</strong> copy=None, spherical=True, **kwargs )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StellarOrbitModel.py#L103-L138 target=_blank>[source]</a></th></tr></thead></table>

Radial velocity model.

Number of parameters is 5

<b>Parameters</b><br>
* copy  :  StellarOrbitModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to copy
* spherical  :  bool (True)
<br>&nbsp;&nbsp;&nbsp;&nbsp; produce output in sperical coordinates (rho,phi)
<br>&nbsp;&nbsp;&nbsp;&nbsp; otherwise in rectilinear coordinates (x,y)
* fixed  :  dictionary of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; int     list if parameters to fix permanently. Default None.
<br>&nbsp;&nbsp;&nbsp;&nbsp; float   list of values for the fixed parameters.
<br>&nbsp;&nbsp;&nbsp;&nbsp; Attribute fixed can only be set in the constructor.


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> spherical=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StellarOrbitModel.py#L140-L153 target=_blank>[source]</a></th></tr></thead></table>
Copy method.  

<b>Parameters</b><br>
* spherical  :  None or bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; return spherical (True) or rectangular (False) coordinates


<a name="baseResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseResult(</strong> xdata, params )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StellarOrbitModel.py#L155-L179 target=_blank>[source]</a></th></tr></thead></table>
<b>Returns</b><br>
the result of the model function as a 2-d array containing 
[rho,phi] when spherical is true else [x,y]

<b>Parameters</b><br>
* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.

The parameters are explained in the [#StellarOrbitModel constructor.](#StellarOrbitModel constructor.)


<a name="getOrbit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getOrbit(</strong> xdata, params, d3=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StellarOrbitModel.py#L181-L235 target=_blank>[source]</a></th></tr></thead></table>
Calculate the 2 (or 3)-dim result of the model function as a tuple of arrays 

The pertaining rho, phi, (theta) are available from self.

<b>Parameters</b><br>
* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.
* d3  :  bool (False)
<br>&nbsp;&nbsp;&nbsp;&nbsp; return 3 dim result if true else 2 dim

The parameters are explained in the [#StellarOrbitModel constructor.](#StellarOrbitModel constructor.)

<b>Returns</b><br>
* x, y(, z)  :  tuple of arrays
<br>&nbsp;&nbsp;&nbsp;&nbsp; containing the rectangular coordinates

<a name="baseDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseDerivative(</strong> xdata, params, d3=False )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StellarOrbitModel.py#L237-L323 target=_blank>[source]</a></th></tr></thead></table>
Returns the derivative [df1/dt, df2/dt] of the model function.
Where f1 = rho if spherical else x
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; f2 = phi if spherical else y
and t is time, input data, here aliased to 'xdata' 

<b>Parameters</b><br>
* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.
* d3  :  boolean
<br>&nbsp;&nbsp;&nbsp;&nbsp; when True also return df3/dt in the array
<br>&nbsp;&nbsp;&nbsp;&nbsp; f3 is theta if spherical else z 

The parameters are explained in the [#StellarOrbitModel constructor.](#StellarOrbitModel constructor.)


<a name="basePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePartial(</strong> xdata, params, parlist=None, d3=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StellarOrbitModel.py#L325-L496 target=_blank>[source]</a></th></tr></thead></table>
Returns the partials at the xdata value.

<b>Parameters</b><br>
* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters. (not used for linear models)
* parlist  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of indices active parameters (or None for all)
* d3  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; if True also return derivatives of theta cq z

The parameters are explained in the [#StellarOrbitModel constructor.](#StellarOrbitModel constructor.)


<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StellarOrbitModel.py#L498-L503 target=_blank>[source]</a></th></tr></thead></table>
Returns a string representation of the model.


<a name="baseParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseParameterUnit(</strong> k )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StellarOrbitModel.py#L505-L522 target=_blank>[source]</a></th></tr></thead></table>
Return the unit of a parameter. (TBC)

<b>Parameters</b><br>
* k  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; the kth parameter.


<a name="convertParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>convertParameters(</strong> param, stdevs=None, year=2000 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StellarOrbitModel.py#L524-L564 target=_blank>[source]</a></th></tr></thead></table>
Return time of periastron (p<sub>3</sub>) in years after year and inclination (p<sub>4</sub>), 
<br>&nbsp;&nbsp;&nbsp;&nbsp; the position angle from North to the line of nodes (p<sub>5</sub>) and
<br>&nbsp;&nbsp;&nbsp;&nbsp; the longitude from line of nodes to periastron (p<sub>6</sub>) in degrees

<b>Parameters</b><br>
* param  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters to be converted
* stdevs  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; standard deviations to be converted
* year  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; return the first periastron passage after year

<b>Returns</b><br>
converted parameters if stdevs is None
converted (parameters, stdevs) else 

<a name="plotOrbit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotOrbit(</strong> par, npoint=361, xdata=None, ydata=None,
 plot=None, color='k', ls='-' ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/StellarOrbitModel.py#L566-L593 target=_blank>[source]</a></th></tr></thead></table>
Plot the orbit in N points, a forward pointing arrow at T = 0, 
the line to the periastron and an extended line of nodes. 

if ydata is present, plot the datapoints. If also xdata is present, 
plot the connecting lines too.

<b>Parameters</b><br>
* par  :   array
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter of the model
* npoint  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of points in the orbit
* xdata  :  array 
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of times at which the data are measured
* ydata  :  2d array 
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of [x,y] pairs representing the data
* plot  :  None or pyplot
<br>&nbsp;&nbsp;&nbsp;&nbsp; None    make a self standing plot and show it
<br>&nbsp;&nbsp;&nbsp;&nbsp; pyplot  operate within thid plot; do not show
* color, ls  :  color and linestyle
<br>&nbsp;&nbsp;&nbsp;&nbsp; for the plot


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
* [<strong>getParameterIndex(</strong> parname ) ](./BaseModel.md#getParameterIndex)
* [<strong>getParameterValue(</strong> param, name, default=None ) ](./BaseModel.md#getParameterValue)
* [<strong>baseParameterName(</strong> kpar ) ](./BaseModel.md#baseParameterName)
