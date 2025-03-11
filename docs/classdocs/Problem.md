---
---
<br><br>

<a name="Problem"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Problem(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Problem.py target=_blank>Source</a></th></tr></thead></table>

Problem implements the common parts of specialized Problems.

A Problem is an optimization of parameters which does not involve
the fitting of data to a Model.

Problems can be solved by NestedSampler, with appropriate Engines and
ErrorDistributions.

The result of the function for certain x and p is given by
problem.result( x, p )
The parameters, p, are to be optimized while the x provide additional
information.

This class is a base class. Further specializations will define the
result method.

<b>Attributes</b>

* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be optimized
* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; independent variable (static)
* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; dependent variable (static)
* weights  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights associated with ydata
* varyy  :  float or ndarry of shape (ndata,)
<br>&nbsp;&nbsp;&nbsp;&nbsp; Variance in the errors of the ydata
* npars  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of parameters in the model of the problem
* partype  :  float | int
<br>&nbsp;&nbsp;&nbsp;&nbsp; type of the parameters


* Author  :          Do Kester


<a name="Problem"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Problem(</strong> model=None, xdata=None, ydata=None, weights=None,
 accuracy=None, copy=None )
</th></tr></thead></table>

Problem Constructor.

<b>Parameters</b>

* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model to be solved
* xdata  :  array_like or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; independent variable
* ydata  :  array_like or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; dependent variable
* weights  :  array_like or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights associated with ydata
* accuracy  :  float or ndarray of shape (ndata,)
<br>&nbsp;&nbsp;&nbsp;&nbsp; accuracy scale for the datapoints
<br>&nbsp;&nbsp;&nbsp;&nbsp; all the same or one for each data point
* copy  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be copied


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
Copy.


<a name="setAccuracy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setAccuracy(</strong> accuracy=None ) 
</th></tr></thead></table>
set the value for accuracy.

<b>Paramaters</b>

* accuracy  :  float or array of NDATA floats or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; Either one value for all or one for each data point
<br>&nbsp;&nbsp;&nbsp;&nbsp; When None the value is set to 0 (for easy computational reasons)

<a name="hasWeights"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasWeights(</strong> )
</th></tr></thead></table>

Return whether it has weights. 
<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> param )
</th></tr></thead></table>
Returns the result using the parameters.

In this (base)class it is a placeholder.

<b>Parameters</b>

* param  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.


<a name="residuals"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>residuals(</strong> param, mockdata=None ) 
</th></tr></thead></table>
Returns the residuals, calculated at the xdata.

<b>Parameters</b>

* param  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.
* mockdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; model fit at xdata


<a name="cyclicCorrection"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>cyclicCorrection(</strong> res )
</th></tr></thead></table>
No correction.

<b>Returns </b>

&nbsp;&nbsp;&nbsp;&nbsp; the residuals, unadultered

<b>Parameters</b>

* res  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; residuals


<a name="cycor1"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>cycor1(</strong> res )
</th></tr></thead></table>
Returns the residuals, all corrected for periodicity in residuals

<b>Parameters</b>

* res  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; residuals


<a name="cycor2"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>cycor2(</strong> res )
</th></tr></thead></table>
Returns the residuals corrected for periodicity in residuals, only
the result dimensions listed in the model.cyclic dictionary.

<b>Parameters</b>

* res  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; residuals


<a name="cyclize"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>cyclize(</strong> res, period ) 
</th></tr></thead></table>
Apply correction on residuals which are cyclic in some
phase space.

If the model results in a phase value of +&epsilon;
while the data give that phase value as (p - &epsilon;)
to keep all data in the range [0,p], the naive residual
would be (p - 2 &epsilon;) while the actual distance should
be measured the other way around as (2 &epsilon;).
Here p = period and &epsilon; = small deviation.

<b>Parameters</b>

* res  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; original residuals
* period  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the phase space

<b>Returns</b>

corrected residuals.

<a name="weightedResSq"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>weightedResSq(</strong> allpars, mockdata=None, extra=False ) 
</th></tr></thead></table>
Returns the (weighted) squared residuals, calculated at the xdata.

Optionally (extra=True) the weighted residuals themselves are returned too.

<b>Parameters</b>

* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.
* mockdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; model fit at xdata
* extra  :  bool (False)
<br>&nbsp;&nbsp;&nbsp;&nbsp; true  : return ( wgt * res^2, wgt * res )
<br>&nbsp;&nbsp;&nbsp;&nbsp; false : return wgt * res<sup>2</sup>

<a name="isDynamic"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isDynamic(</strong> ) 
</th></tr></thead></table>

<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> dval, kpar ) 
</th></tr></thead></table>
Return value in [0,1] for the selected parameter.

<b>Parameters</b>

* dval  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; domain value for the selected parameter
* kpar  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; selected parameter index, where kp is index in [parameters, hyperparams]

<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> uval, kpar ) 
</th></tr></thead></table>
Return domain value for the selected parameter.

<b>Parameters</b>

* uval  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; unit value for the selected parameter
* kpar  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; selected parameter indices, where kp is index in [parameters, hyperparams]

<a name="shortName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shortName(</strong> ) 
</th></tr></thead></table>

<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> ) 
</th></tr></thead></table>

