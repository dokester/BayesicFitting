---
---
<p>
  
<p>

<a name="BaseModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class BaseModel(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py target=_blank>Source</a></th></tr></thead></table>
<p>

BaseModel implements the common parts of simple Models.

A simple model is a function in x with parameters p : f(x:p).
The variable x is an array of points in a space of one or more
dimensions; p can have any length, including 0 i.e. the model
has no parameters.

The result of the function for certain x and p is given by
model.result( x, p )

The partial derivatives of f to p (df/dp) is given by
model.partial( x, p )
Some fitters make use of the partials

The derivative of f to x (df/dx) is given by
model.derivative( x, p )

BaseModel checks parameters for positivity and nonzero-ness, if such
is indicated in the model itself.

BaseModel also implements the numerical calculation of the (partial)
derivatives to be used when they are not given in the model definition
itself.

<b>Attributes</b>

* npbase  :  int<br>
    number of params in the base model<br>
* ndim  :  int<br>
    number of dimensions (parallel streams) of input. (default : 1)<br>
* priors  :  list of Prior<br>
    pertaining to each of the parameters of the model.<br>
    If the list is shorter than the number of parameters, the last one is repeated.<br>
* posIndex  :  list of int<br>
    list of indices indication positive-definite parameters.<br>
* nonZero  :  list of int<br>
    list of parameters that need a warning when they are equal to zero.<br>
    Warnings will only be issued once. Values are replaced by self.tiny<br>
* tiny  :  float<br>
    very small value, replacing zero valued when found on NonZero.<br>
    (default : 1e-20)<br>
* deltaP  :  array_like<br>
    (list of) width(s) for numerical partial calculation. (default : 0.00001)<br>
* parNames  :  list of str<br>
    list of parameter names. (default : "parameter_k")<br>

* Author  :          Do Kester<br>


<a name="BaseModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>BaseModel(</strong> nparams=0, ndim=1, copy=None, posIndex=[], nonZero=[], **kwargs )
</th></tr></thead></table>
<p>

BaseModel Constructor.
<br>
<b>Parameters</b>

* nparams  :  int<br>
    Number of parameters in the model (default: 0)<br>
* ndim  :  int<br>
    Number of dimensions of the input (default: 1)<br>
* copy  :  BaseModel<br>
    to be copied<br>
* posIndex  :  list of int<br>
    indices of parameters that need to be > 0<br>
* nonZero  :  list of int<br>
    indices of parameters that cannot be zero.<br>
    they are replaced by self.tiny<br>
kwargs
    for internal use.

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> xdata, param )
</th></tr></thead></table>
<p>

Returns the result calculated at the xdatas.

<b>Parameters</b>

* xdata  :  array_like<br>
    values at which to calculate the result<br>
* param  :  array_like<br>
    values for the parameters.<br>


<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> xdata, param, parlist=None )
</th></tr></thead></table>
<p>

Returns the partial derivatives calculated at the inputs.

<b>Parameters</b>

* xdata  :  array_like<br>
    values at which to calculate the result<br>
* param  :  array_like<br>
    values for the parameters.<br>
* parlist  :  None or array_like<br>
    indices of active parameters<br>


<a name="checkParameter"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>checkParameter(</strong> param ) 
</th></tr></thead></table>
<p>

Return parameters corrected for positivity and Non-zero.

<b>Parameters</b>

* param  :  array_like<br>
    values for the parameters.<br>


<a name="checkPositive"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>checkPositive(</strong> param ) 
</th></tr></thead></table>
<p>

Check parameters for positivity. Silently correct.

<b>Parameters</b>

* params  :  array_like<br>
    values for the parameters<br>


<a name="checkZeroParameter"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>checkZeroParameter(</strong> param )
</th></tr></thead></table>
<p>

Check parameters for Non-zero. Correct after one warning.

<b>Parameters</b>

* params  :  array_like<br>
    values for the parameters<br>


<a name="isDynamic"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isDynamic(</strong> ) 
</th></tr></thead></table>
<p>

Whether the model implements Dynamic

<a name="isModifiable"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isModifiable(</strong> ) 
</th></tr></thead></table>
<p>

Whether the model implements Modifiable

<a name="shortName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shortName(</strong> )
</th></tr></thead></table>
<p>

Return a short version the string representation: upto first non-letter.


<a name="derivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>derivative(</strong> xdata, param ) 
</th></tr></thead></table>
<p>

Returns the derivative of the model to xdata.

It is a numeric derivative as the analytic derivative is not present
in the model.

<b>Parameters</b>

* xdata  :  array_like<br>
    values at which to calculate the derivative<br>
* param  :  array_like<br>
    values for the parameters. (default: model.parameters)<br>


<a name="setPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setPrior(</strong> kpar, prior=None, **kwargs ) 
</th></tr></thead></table>
<p>

set the prior and/or limits for the indicated parameter.

The prior (by default UniformPrior) is appended when kpar is equal to np, 
the length of the existing list of priors. 
It replaces the prior when kpar < np and 
it generates an error when kpar > np

<b>Parameters</b>

* kpar  :  int<br>
    parameter number.<br>
* prior  :  Prior<br>
    prior for the parameter<br>
* kwargs  :  dict<br>
    attributes to be passed to the prior<br>

<b>Raises</b>

IndexError
    when kpar is larger than the length of priors list already present <br>


<a name="hasPriors"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasPriors(</strong> isBound=True ) 
</th></tr></thead></table>
<p>

Return True when the model has priors for all its parameters.

<b>Parameters</b>

* isBound  :  bool<br>
    Also check if the prior is bound.

<a name="getPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getPrior(</strong> kpar ) 
</th></tr></thead></table>
<p>

Return the prior of the indicated parameter.

<b>Parameters</b>

* kpar  :  int<br>
    parameter number.

<a name="basePrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePrior(</strong> kpar ) 
</th></tr></thead></table>
<p>

Return the prior of the indicated parameter.

<b>Parameters</b>

* kpar  :  int<br>
    parameter number.

<a name="getParameterName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParameterName(</strong> kpar ) 
</th></tr></thead></table>
<p>

Return the name of the indicated parameter.

<b>Parameters</b>

* kpar  :  int<br>
    parameter number.

<a name="baseParameterName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseParameterName(</strong> kpar ) 
</th></tr></thead></table>
<p>

Return the name of the indicated parameter.

<b>Parameters</b>

* kpar  :  int<br>
    parameter number.

<a name="getParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParameterUnit(</strong> kpar ) 
</th></tr></thead></table>
<p>

Return the unit of the indicated parameter.

<b>Parameters</b>

* kpar  :  int<br>
    parameter number.

<a name="baseParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseParameterUnit(</strong> kpar ) 
</th></tr></thead></table>
<p>

Return the name of the indicated parameter.

<b>Parameters</b>

* kpar  :  int<br>
    parameter number.

<a name="hasLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasLimits(</strong> fitindex=None ) 
</th></tr></thead></table>
<p>

Return True if the model has limits set.

