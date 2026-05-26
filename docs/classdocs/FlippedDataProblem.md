---
---
<br><br>

<a name="FlippedDataProblem"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class FlippedDataProblem(</strong> <a href="./MultipleOutputProblem.html">MultipleOutputProblem</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source// target=_blank>[source]</a></th></tr></thead></table>
<p>

A FlippedDataProblem is a problem for solving double star orbits, 
where there is ambiguity of the stars A and B,  in a (small) number 
of datapoints. 

In some double stars, it is not  always clear which star is the main
star A and which is the secundary B, resulting in ambiguity in the 
angular direction. 

Directions with misidentification in A and B, should be flipped.
In spherical coordinates (rho,phi) should be (rho,-phi). 
In rectangular coordinates (x,y) should be replaced by (-x,-y).

<b>Attributes</b>

* nflip  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; actual number of flipped datapoints
* flipped  :  list of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of flipped datapoints.

<b>Attributes from Problem</b>

model, xdata, ydata, weights, partype

* Author  :          Do Kester


<a name="FlippedDataProblem"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>FlippedDataProblem(</strong> model=None, xdata=None, ydata=None, weights=None,
 accuracy=None, nflip=0, copy=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L59-L85 target=_blank>[source]</a></th></tr></thead></table>

Problem Constructor.

<b>Parameters</b>

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
* nflip  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; Maximum number of datapoints that can be flipped.
* copy  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be copied


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L87-L92 target=_blank>[source]</a></th></tr></thead></table>
Copy.


<a name="residuals"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>residuals(</strong> param, mockdata=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L94-L117 target=_blank>[source]</a></th></tr></thead></table>
Returns residuals in a flattened array.

<a name="getFlippedData"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getFlippedData(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L119-L140 target=_blank>[source]</a></th></tr></thead></table>
Return the corrected datapoints.

<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L142-L147 target=_blank>[source]</a></th></tr></thead></table>
Returns a string representation of the model.

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./MultipleOutputProblem.html">MultipleOutputProblem</a></th></tr></thead></table>


* [<strong>expandFlat(</strong> weights, ndout ) ](./MultipleOutputProblem.md#expandFlat)
* [<strong>result(</strong> param )](./MultipleOutputProblem.md#result)
* [<strong>partial(</strong> param ) ](./MultipleOutputProblem.md#partial)
* [<strong>derivative(</strong> param ) ](./MultipleOutputProblem.md#derivative)
* [<strong>weightedResSq(</strong> allpars, mockdata=None, extra=False ) ](./MultipleOutputProblem.md#weightedResSq)
* [<strong>myEngines(</strong> ) ](./MultipleOutputProblem.md#myEngines)
* [<strong>myStartEngine(</strong> ) ](./MultipleOutputProblem.md#myStartEngine)
* [<strong>myDistribution(</strong> ) ](./MultipleOutputProblem.md#myDistribution)


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
