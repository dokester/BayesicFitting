---
---
<br><br>

<a name="BaseModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class BaseModel(</strong> object )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py target=_blank>[source]</a></th></tr></thead></table>
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

<b>Attributes</b><br>
* npbase  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of params in the base model
* ndim  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of dimensions (parallel streams) of input. (default : 1)
* priors  :  list of Prior
<br>&nbsp;&nbsp;&nbsp;&nbsp; pertaining to each of the parameters of the model.
<br>&nbsp;&nbsp;&nbsp;&nbsp; If the list is shorter than the number of parameters, the last one is repeated.
* posIndex  :  list of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of indices indication positive-definite parameters.
* nonZero  :  list of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of parameters that need a warning when they are equal to zero.
<br>&nbsp;&nbsp;&nbsp;&nbsp; Warnings will only be issued once. Values are replaced by self.tiny
* tiny  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; very small value, replacing zero valued when found on NonZero.
<br>&nbsp;&nbsp;&nbsp;&nbsp; (default : 1e-20)
* deltaP  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; (list of) width(s) for numerical partial calculation. (default : 0.00001)
* parNames  :  list of str
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of parameter names. (default : "parameter_k")

Author          Do Kester


<a name="BaseModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>BaseModel(</strong> nparams=0, ndim=1, ndout=None, copy=None, posIndex=[], nonZero=[], **kwargs )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L91-L136 target=_blank>[source]</a></th></tr></thead></table>

BaseModel Constructor.
<br>
<b>Parameters</b><br>
* nparams  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; Number of parameters in the model (default: 0)
* ndim  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; Number of dimensions of the input (default: 1)
* copy  :  BaseModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be copied
* posIndex  :  list of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters that need to be > 0
* nonZero  :  list of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters that cannot be zero.
<br>&nbsp;&nbsp;&nbsp;&nbsp; they are replaced by self.tiny
kwargs
<br>&nbsp;&nbsp;&nbsp;&nbsp; for internal use.

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> xdata, param )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L185-L199 target=_blank>[source]</a></th></tr></thead></table>
Returns the result calculated at the xdatas.

<b>Parameters</b><br>
* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result
* param  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.


<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> xdata, param, parlist=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L201-L216 target=_blank>[source]</a></th></tr></thead></table>
Returns the partial derivatives calculated at the inputs.

<b>Parameters</b><br>
* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result
* param  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.
* parlist  :  None or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of active parameters


<a name="checkParameter"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>checkParameter(</strong> param ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L218-L230 target=_blank>[source]</a></th></tr></thead></table>
Return parameters corrected for positivity and Non-zero.

<b>Parameters</b><br>
* param  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.


<a name="checkPositive"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>checkPositive(</strong> param ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L232-L243 target=_blank>[source]</a></th></tr></thead></table>
Check parameters for positivity. Silently correct.

<b>Parameters</b><br>
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters


<a name="checkZeroParameter"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>checkZeroParameter(</strong> param )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L245-L260 target=_blank>[source]</a></th></tr></thead></table>
Check parameters for Non-zero. Correct after one warning.

<b>Parameters</b><br>
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters


<a name="isDynamic"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isDynamic(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L262-L266 target=_blank>[source]</a></th></tr></thead></table>
Whether the model implements Dynamic

<a name="isModifiable"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isModifiable(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L268-L274 target=_blank>[source]</a></th></tr></thead></table>
Whether the model implements Modifiable

<a name="shortName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shortName(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L279-L285 target=_blank>[source]</a></th></tr></thead></table>
Return a short version the string representation: upto first non-letter.


<a name="derivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>derivative(</strong> xdata, param ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L287-L302 target=_blank>[source]</a></th></tr></thead></table>
Returns the derivative of the model to xdata.

It is a numeric derivative as the analytic derivative is not present
in the model.

<b>Parameters</b><br>
* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the derivative
* param  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters. (default: model.parameters)


<a name="setPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setPrior(</strong> kpar, prior=None, **kwargs ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L304-L344 target=_blank>[source]</a></th></tr></thead></table>
set the prior and/or limits for the indicated parameter.

The prior (by default UniformPrior) is appended when kpar is equal to np, 
the length of the existing list of priors. 
It replaces the prior when kpar < np and 
it generates an error when kpar > np

<b>Parameters</b><br>
* kpar  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter number.
* prior  :  Prior
<br>&nbsp;&nbsp;&nbsp;&nbsp; prior for the parameter
* kwargs  :  dict
<br>&nbsp;&nbsp;&nbsp;&nbsp; attributes to be passed to the prior

<b>Raises</b><br>
IndexError
<br>&nbsp;&nbsp;&nbsp;&nbsp; when kpar is larger than the length of priors list already present 


<a name="hasPriors"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasPriors(</strong> isBound=True ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L346-L356 target=_blank>[source]</a></th></tr></thead></table>
Return True when the model has priors for all its parameters.

<b>Parameters</b><br>
* isBound  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; Also check if the prior is bound.

<a name="getPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getPrior(</strong> kpar ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L358-L367 target=_blank>[source]</a></th></tr></thead></table>
Return the prior of the indicated parameter.

<b>Parameters</b><br>
* kpar  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter number.

<a name="basePrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePrior(</strong> kpar ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L369-L385 target=_blank>[source]</a></th></tr></thead></table>
Return the prior of the indicated parameter.

<b>Parameters</b><br>
* kpar  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter number.

<a name="getParameterIndex"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParameterIndex(</strong> parname ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L387-L413 target=_blank>[source]</a></th></tr></thead></table>
Return the index of the  parameter.
Uses dictionary self.<sub>parindex</sub>

<b>Parameters</b><br>
* parname  :  str
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter name.

<b>Raise</b><br>
ValueError when parname is not present


<a name="getParameterValue"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParameterValue(</strong> param, name, default=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L415-L440 target=_blank>[source]</a></th></tr></thead></table>
Return the value of the parameter with the given name from the param array.

<b>Parameters</b><br>
* param  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter values
* name  :  str
<br>&nbsp;&nbsp;&nbsp;&nbsp; name of parameter
* default  :  None or not
<br>&nbsp;&nbsp;&nbsp;&nbsp; NOne : raise Error
<br>&nbsp;&nbsp;&nbsp;&nbsp; not  : return the default

<b>Raise</b><br>
ValueError when name cannot be found.


<a name="getParameterName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParameterName(</strong> kpar ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L442-L452 target=_blank>[source]</a></th></tr></thead></table>
Return the name of the indicated parameter.

<b>Parameters</b><br>
* kpar  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter number.

<a name="baseParameterName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseParameterName(</strong> kpar ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L454-L463 target=_blank>[source]</a></th></tr></thead></table>
Return the name of the indicated parameter.

<b>Parameters</b><br>
* kpar  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter number.

<a name="getParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParameterUnit(</strong> kpar ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L465-L474 target=_blank>[source]</a></th></tr></thead></table>
Return the unit of the indicated parameter.

<b>Parameters</b><br>
* kpar  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter number.

<a name="baseParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseParameterUnit(</strong> kpar ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L476-L485 target=_blank>[source]</a></th></tr></thead></table>
Return the name of the indicated parameter.

<b>Parameters</b><br>
* kpar  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter number.

<a name="hasLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasLimits(</strong> fitindex=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseModel.py#L487-L503 target=_blank>[source]</a></th></tr></thead></table>
Return True if the model has limits set.

