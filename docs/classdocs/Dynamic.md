---
---
<br><br>

<a name="Dynamic"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Dynamic(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Dynamic.py target=_blank>Source</a></th></tr></thead></table>
<p>

Class adjoint to Model which implements some dynamic behaviour.


<b>Attributes</b><br>
* ncomp  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; the number of components in the dynamic model<br>
* deltaNpar  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; the number of parameters in each component<br>
* minComp  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; minimum number of repetitions<br>
* maxComp  :  None or int<br>
&nbsp;&nbsp;&nbsp;&nbsp; maximum number of repetitions<br>
* growPrior  :  None or Prior<br>
&nbsp;&nbsp;&nbsp;&nbsp; governing the birth and death.<br>
&nbsp;&nbsp;&nbsp;&nbsp; ExponentialPrior (scale=2) if  maxOrder is None else UniformPrior<br>


<a name="Dynamic"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Dynamic(</strong> dynamic=True ) 
</th></tr></thead></table>
<p>

Constructor for Dynamic

<b>Parameters</b><br>
* dynamic :  bool<br>
    True if the Model is to be considered dynamic.

<a name="isDynamic"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isDynamic(</strong> ) 
</th></tr></thead></table>
<p>
<a name="setGrowPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setGrowPrior(</strong> growPrior=None, min=1, max=None, name="Comp" ) 
</th></tr></thead></table>
<p>

Set the growth prior.

<b>Parameters</b><br>
* growPrior  :  None or Prior<br>
&nbsp;&nbsp;&nbsp;&nbsp; governing the birth and death.<br>
&nbsp;&nbsp;&nbsp;&nbsp; ExponentialPrior (scale=2) if  maxOrder is None else UniformPrior<br>
* min  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; lower limit on growthprior<br>
* max  :  None or int<br>
&nbsp;&nbsp;&nbsp;&nbsp; upper limit on growthprior<br>
* name  :  str<br>
    name of the component

<a name="setDynamicAttribute"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setDynamicAttribute(</strong> name, value ) 
</th></tr></thead></table>
<p>

Set attribute, if it belongs to a Dynamic Models.

<b>Parameters</b><br>
* name  :  str<br>
&nbsp;&nbsp;&nbsp;&nbsp; name of the attribute<br>
* value  :  anything<br>
&nbsp;&nbsp;&nbsp;&nbsp; value of the attribute<br>

<b>Return</b><br>
* bool  :  True if name was a Dynamic name<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; False if not<br>


<a name="grow"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>grow(</strong> offset=0, rng=None, **kwargs )
</th></tr></thead></table>
<p>

Increase the degree by one upto maxComp ( if present ).

<b>Parameters</b><br>
* offset  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index where the params of the Dynamic model start<br>
* rng  :  random number generator<br>
&nbsp;&nbsp;&nbsp;&nbsp; to generate a new parameter.<br>

<b>Return</b><br>
* bool  :   succes<br>


<a name="shrink"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shrink(</strong> offset=0, rng=None, **kwargs )
</th></tr></thead></table>
<p>

Decrease the degree by one downto minComp ( default 1 ).

<b>Parameters</b><br>
* offset  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index where the params of the Dynamic model start<br>
* rng  :  random number generator<br>
&nbsp;&nbsp;&nbsp;&nbsp; Not used in this implementation<br>

<b>Return</b><br>
* bool  :  succes<br>


<a name="alterParameterNames"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>alterParameterNames(</strong> dnp ) 
</th></tr></thead></table>
<p>

Renumber the parameter names.

<b>Parameters</b><br>
* dnp  :  int<br>
    change in the number of parameters

<a name="alterParameterSize"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>alterParameterSize(</strong> dnp, offset, location=None, value=0 ) 
</th></tr></thead></table>
<p>

Change the number of parameters and self.parameters.

<b>Parameters</b><br>
* dnp  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; change in the number of parameters in the DynamicModel<br>
* offset  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; starting index of the DynamicModel<br>
* location  :  int<br>
    index in param[offset:] at which to insert/delete the new parameters

<a name="alterParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>alterParameters(</strong> param, location, dnp, offset, value=None ) 
</th></tr></thead></table>
<p>

change the parameters to comply with the changed model.

param:      [p0 p1 p2 p3 p4 p5 p6 p7 p8 p9]   # previous set
offset:     2           # parameters of models in preceeding chain
location:   1           # location where to add/delete parameter
value:      [v0 ...]    # values to be given to added parameters

dnp:        +1
==> newpar: [p0 p1 p2 v0 p3 p4 p5 p6 p7 p8 p9]

dnp:        +2
==> newpar: [p0 p1 p2 v0 v1 p3 p4 p5 p6 p7 p8 p9]

dnp:        -1
==> newpar: [p0 p1 p3 p4 p5 p6 p7 p8 p9]

dnp:        -2
==> ERROR: not enough space in param before location

<b>Parameters</b><br>
* param  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters of the parent model (chain)<br>
* location  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index in param[offset:] at which to insert/delete the new parameters<br>
* dnp  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of parameters to insert (dnp>0) or delete (dnp<0)<br>
* offset  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; start index of the parameters of the dynamic model in param<br>
* value  :  float or array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be given to the inserted parameters (only when dnp>0)<br>


<a name="alterFitindex"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>alterFitindex(</strong> findex, location, dnp, offset ) 
</th></tr></thead></table>
<p>

change the fit index to comply with the changed model.

<b>Parameters</b><br>
* findex  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; fit index of the parent model (chain)<br>
* location  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index in param[offset:] at which to insert/delete the new parameters<br>
* dnp  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of parameters to insert (dnp>0) or delete (dnp<0)<br>
* offset  :  int<br>
    start index of the parameters of the dynamic model in param

<a name="shuffle"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shuffle(</strong> param, offset, np, rng ) 
</th></tr></thead></table>
<p>

Shuffle the parameters of the components (if they are equivalent)
Default implementation: does nothing.

<b>Parameters</b><br>
* param  :  array-like<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters<br>
* offset  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index where the dynamic model starts<br>
* np  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; length of the parameters of the dynamic model<br>
* rng  :  RNG<br>
    random number generator

