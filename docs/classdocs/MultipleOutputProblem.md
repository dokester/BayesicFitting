---
---
<br><br>

<a name="MultipleOutputProblem"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class MultipleOutputProblem(</strong> <a href="./Problem.html">Problem</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/MultipleOutputProblem.py target=_blank>[source]</a></th></tr></thead></table>
<p>

A MultipleOutputProblem is an optimization of parameters where the model
has multiple outputs. E.g. the orbit of a double star or the outcome of
a game.

Problems can be solved by NestedSampler, with appropriate Engines and
ErrorDistributions.

The result of the function for certain x and p is given by
problem.result( p )
The parameters, p, are to be optimized while the x provide additional
information.

<b>Attributes from Problem</b><br>
model, xdata, ydata, weights, partype

* Author  :          Do Kester


<a name="MultipleOutputProblem"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>MultipleOutputProblem(</strong> model=None, xdata=None, ydata=None, weights=None,
 accuracy=None, copy=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/MultipleOutputProblem.py#L52-L79 target=_blank>[source]</a></th></tr></thead></table>

Problem Constructor.

<b>Parameters</b><br>
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model to be solved. One with multiple outputs: model.ndout > 1
* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; independent variable
* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; dependent variable. shape = (len(xdata), model.ndout)
* weights  :  array_like or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights associated with ydata: shape = as xdata or as ydata
* accuracy  :  float or ndarray of shape (ndata,)
<br>&nbsp;&nbsp;&nbsp;&nbsp; accuracy scale for the datapoints
<br>&nbsp;&nbsp;&nbsp;&nbsp; all the same or one for each data point
* copy  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be copied


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/MultipleOutputProblem.py#L81-L87 target=_blank>[source]</a></th></tr></thead></table>
Copy.


<a name="expandFlat"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>expandFlat(</strong> weights, ndout ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/MultipleOutputProblem.py#L89-L102 target=_blank>[source]</a></th></tr></thead></table>
Expand and flatten the arrays.


<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> param )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/MultipleOutputProblem.py#L104-L114 target=_blank>[source]</a></th></tr></thead></table>
Returns the result calculated at the xdata.

<b>Parameters</b><br>
* param  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters + nuisance params.


<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> param ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/MultipleOutputProblem.py#L116-L138 target=_blank>[source]</a></th></tr></thead></table>
Returns the partials (df/dp) calculated at the xdata.

<b>Parameters</b><br>
* param  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters + nuisance params.


<a name="derivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>derivative(</strong> param ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/MultipleOutputProblem.py#L140-L149 target=_blank>[source]</a></th></tr></thead></table>
Return the derivative of the internal model.

<b>Parameters</b><br>
* param  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of model parameters

<a name="residuals"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>residuals(</strong> param, mockdata=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/MultipleOutputProblem.py#L151-L156 target=_blank>[source]</a></th></tr></thead></table>
Returns residuals in a flattened array.

<a name="weightedResSq"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>weightedResSq(</strong> allpars, mockdata=None, extra=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/MultipleOutputProblem.py#L158-L177 target=_blank>[source]</a></th></tr></thead></table>
Returns the (weighted) squared residuals, calculated at the xdata.

Optionally (extra=True) the weighted residuals themselves are returned too.

<b>Parameters</b><br>
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.
* mockdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; model fit at xdata
* extra  :  bool (False)
<br>&nbsp;&nbsp;&nbsp;&nbsp; true  : return ( wgt * res^2, wgt * res )
<br>&nbsp;&nbsp;&nbsp;&nbsp; false : return wgt * res<sup>2</sup>

<a name="myEngines"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>myEngines(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/MultipleOutputProblem.py#L179-L183 target=_blank>[source]</a></th></tr></thead></table>
Return a default list of preferred engines

<a name="myStartEngine"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>myStartEngine(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/MultipleOutputProblem.py#L185-L189 target=_blank>[source]</a></th></tr></thead></table>
Return the default preferred startengines

<a name="myDistribution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>myDistribution(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/MultipleOutputProblem.py#L191-L196 target=_blank>[source]</a></th></tr></thead></table>
Return the name of the preferred error distribution

<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/MultipleOutputProblem.py#L198-L201 target=_blank>[source]</a></th></tr></thead></table>

Returns a string representation of the model. 
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Problem.html">Problem</a></th></tr></thead></table>


* [<strong>setAccuracy(</strong> accuracy=None ) ](./Problem.md#setAccuracy)
* [<strong>hasWeights(</strong> )](./Problem.md#hasWeights)
* [<strong>cyclicCorrection(</strong> res )](./Problem.md#cyclicCorrection)
* [<strong>cycor1(</strong> res )](./Problem.md#cycor1)
* [<strong>cycor2(</strong> res )](./Problem.md#cycor2)
* [<strong>cyclize(</strong> res, period ) ](./Problem.md#cyclize)
* [<strong>isDynamic(</strong> ) ](./Problem.md#isDynamic)
* [<strong>domain2Unit(</strong> dval, kpar ) ](./Problem.md#domain2Unit)
* [<strong>unit2Domain(</strong> uval, kpar ) ](./Problem.md#unit2Domain)
* [<strong>shortName(</strong> ) ](./Problem.md#shortName)
