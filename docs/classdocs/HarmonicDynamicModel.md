---
---
<br><br>

<a name="HarmonicDynamicModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class HarmonicDynamicModel(</strong> <a href="./HarmonicModel.html">HarmonicModel,</a><a href="./Dynamic.html">Dynamic</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/HarmonicDynamicModel.py target=_blank>Source</a></th></tr></thead></table>
<p>

Harmonic oscillator Model of adaptable order.

f( x:p ) = &sum;_j ( p_k cos( 2 &pi; j x ) + p_k+1 sin( 2 &pi; j x ) )

j = 1, N; k = 0, 2N

The parameters are initialized at 1.0. It is a linear model.

Author       Do Kester

<b>Attributes</b>

* minOrder  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; minimum degree of polynomial (def=1)<br>
&nbsp;&nbsp;&nbsp;&nbsp; Can also be read as minComp<br>
* maxOrder  :  None or int<br>
&nbsp;&nbsp;&nbsp;&nbsp; maximum degree of polynomial (def=None)<br>
&nbsp;&nbsp;&nbsp;&nbsp; Can also be read as maxComp<br>

<b>Attributes from Dynamic</b>

&nbsp;&nbsp;&nbsp;&nbsp; ncomp (= order), deltaNpar, minComp (= minOrder), maxComp (= maxComp), growPrior<br>

<b>Attributes from HarmonicModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; order, period<br>

<b>Attributes from Model</b>

&nbsp;&nbsp;&nbsp;&nbsp; npchain, parameters, stdevs, xUnit, yUnit<br>

<b>Attributes from FixedModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist<br>

<b>Attributes from BaseModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames<br>


<b>Examples</b>

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

<b>Parameters</b>

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

<b>Raises</b>

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

<b>Parameters</b>

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
