---
---
<br><br>

<a name="Problem"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Problem(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Problem.py target=_blank>Source</a></th></tr></thead></table>
<p>

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

<b>Attributes</b><br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be optimized<br>
* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; independent variable (static)<br>
* ydata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; dependent variable (static)<br>
* weights  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights associated with ydata<br>
* varyy  :  float or ndarry of shape (ndata,)<br>
&nbsp;&nbsp;&nbsp;&nbsp; Variance in the errors of the ydata<br>
* npars  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of parameters in the model of the problem<br>
* partype  :  float | int<br>
&nbsp;&nbsp;&nbsp;&nbsp; type of the parameters<br>


* Author  :          Do Kester<br>


<a name="Problem"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Problem(</strong> model=None, xdata=None, ydata=None, weights=None,
 accuracy=None, copy=None )
</th></tr></thead></table>
<p>

Problem Constructor.

<b>Parameters</b><br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model to be solved<br>
* xdata  :  array_like or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; independent variable<br>
* ydata  :  array_like or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; dependent variable<br>
* weights  :  array_like or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights associated with ydata<br>
* accuracy  :  float or ndarray of shape (ndata,)<br>
&nbsp;&nbsp;&nbsp;&nbsp; accuracy scale for the datapoints<br>
&nbsp;&nbsp;&nbsp;&nbsp; all the same or one for each data point<br>
* copy  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be copied<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>

Copy.


<a name="setAccuracy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setAccuracy(</strong> accuracy=None ) 
</th></tr></thead></table>
<p>

set the value for accuracy.

<b>Paramaters</b><br>
* accuracy  :  float or array of NDATA floats or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; Either one value for all or one for each data point<br>
    When None the value is set to 0 (for easy computational reasons)

<a name="hasWeights"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasWeights(</strong> )
</th></tr></thead></table>
<p>
Return whether it has weights. 

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> param )
</th></tr></thead></table>
<p>

Returns the result using the parameters.

In this (base)class it is a placeholder.

<b>Parameters</b><br>
* param  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.<br>


<a name="residuals"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>residuals(</strong> param, mockdata=None ) 
</th></tr></thead></table>
<p>

Returns the residuals, calculated at the xdata.

<b>Parameters</b><br>
* param  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.<br>
* mockdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; model fit at xdata<br>


<a name="cyclicCorrection"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>cyclicCorrection(</strong> res )
</th></tr></thead></table>
<p>

No correction.

<b>Returns </b><br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; the residuals, unadultered<br>

<b>Parameters</b><br>
* res  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; residuals<br>


<a name="cycor1"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>cycor1(</strong> res )
</th></tr></thead></table>
<p>

Returns the residuals, all corrected for periodicity in residuals

<b>Parameters</b><br>
* res  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; residuals<br>


<a name="cycor2"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>cycor2(</strong> res )
</th></tr></thead></table>
<p>

Returns the residuals corrected for periodicity in residuals, only
the result dimensions listed in the model.cyclic dictionary.

<b>Parameters</b><br>
* res  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; residuals<br>


<a name="cyclize"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>cyclize(</strong> res, period ) 
</th></tr></thead></table>
<p>

Apply correction on residuals which are cyclic in some
phase space.

If the model results in a phase value of +&epsilon;
while the data give that phase value as (p - &epsilon;)
to keep all data in the range [0,p], the naive residual
would be (p - 2 &epsilon;) while the actual distance should
be measured the other way around as (2 &epsilon;).
Here p = period and &epsilon; = small deviation.

<b>Parameters</b><br>
* res  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; original residuals<br>
* period  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; of the phase space<br>

<b>Returns</b><br>
corrected residuals.

<a name="weightedResSq"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>weightedResSq(</strong> allpars, mockdata=None, extra=False ) 
</th></tr></thead></table>
<p>

Returns the (weighted) squared residuals, calculated at the xdata.

Optionally (extra=True) the weighted residuals themselves are returned too.

<b>Parameters</b><br>
* allpars  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.<br>
* mockdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; model fit at xdata<br>
* extra  :  bool (False)<br>
&nbsp;&nbsp;&nbsp;&nbsp; true  : return ( wgt * res^2, wgt * res )<br>
    false : return wgt * res^2

<a name="isDynamic"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isDynamic(</strong> ) 
</th></tr></thead></table>
<p>
<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> dval, kpar ) 
</th></tr></thead></table>
<p>

Return value in [0,1] for the selected parameter.

<b>Parameters</b><br>
* dval  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; domain value for the selected parameter<br>
* kpar  :  array_like<br>
    selected parameter index, where kp is index in [parameters, hyperparams]

<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> uval, kpar ) 
</th></tr></thead></table>
<p>

Return domain value for the selected parameter.

<b>Parameters</b><br>
* uval  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; unit value for the selected parameter<br>
* kpar  :  array_like<br>
    selected parameter indices, where kp is index in [parameters, hyperparams]

<a name="shortName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shortName(</strong> ) 
</th></tr></thead></table>
<p>
<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> ) 
</th></tr></thead></table>
<p>
