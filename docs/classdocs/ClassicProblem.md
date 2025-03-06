---
---
<br><br>

<a name="ClassicProblem"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class ClassicProblem(</strong> <a href="./Problem.html">Problem</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ClassicProblem.py target=_blank>Source</a></th></tr></thead></table>
<p>

A ClassicProblem is an optimization of parameters which involves
the fitting of data to a Model at a fixed set of x values.

Problems can be solved by NestedSampler, with appropriate Engines and
ErrorDistributions.

The result of the function for certain x and p is given by
problem.result( x, p )
The parameters, p, are to be optimized while the x provide additional
information.

<b>Attributes from Problem</b>

model, xdata, ydata, weights, accuracy, varyy

* Author  :          Do Kester<br>


<a name="ClassicProblem"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>ClassicProblem(</strong> model=None, xdata=None, ydata=None, weights=None,
 accuracy=None, copy=None )
</th></tr></thead></table>
<p>

Constructor for classic problems.

<b>Parameters</b>

* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model to be solved<br>
* xdata  :  array_like or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; independent variable<br>
* ydata  :  array_like or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; dependent variable<br>
* weights  :  array_like or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights associated with ydata<br>
* accuracy  :  float or array_like<br>
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

The copy points to the same instance of model.

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> param )
</th></tr></thead></table>
<p>

Returns the result calculated at the xdatas.

<b>Parameters</b>

* param  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.<br>


<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> param ) 
</th></tr></thead></table>
<p>

Return the partials of the internal model.

<b>Parameters</b>

* param  :  array_like<br>
    list of model parameters

<a name="derivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>derivative(</strong> param ) 
</th></tr></thead></table>
<p>

Return the derivative of the internal model.

<b>Parameters</b>

* param  :  array_like<br>
    list of model parameters

<a name="myEngines"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>myEngines(</strong> ) 
</th></tr></thead></table>
<p>

Return a default list of preferred engines

<a name="myStartEngine"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>myStartEngine(</strong> ) 
</th></tr></thead></table>
<p>

Return a default preferred start engines: "start"

<a name="myDistribution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>myDistribution(</strong> ) 
</th></tr></thead></table>
<p>

Return a default preferred ErrorDistribution: "gauss"

<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>
<p>
Returns a string representation of the model. 

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Problem.html">Problem</a></th></tr></thead></table>


* [<strong>setAccuracy(</strong> accuracy=None ) ](./Problem.md#setAccuracy)
* [<strong>hasWeights(</strong> )](./Problem.md#hasWeights)
* [<strong>residuals(</strong> param, mockdata=None ) ](./Problem.md#residuals)
* [<strong>cyclicCorrection(</strong> res )](./Problem.md#cyclicCorrection)
* [<strong>cycor1(</strong> res )](./Problem.md#cycor1)
* [<strong>cycor2(</strong> res )](./Problem.md#cycor2)
* [<strong>cyclize(</strong> res, period ) ](./Problem.md#cyclize)
* [<strong>weightedResSq(</strong> allpars, mockdata=None, extra=False ) ](./Problem.md#weightedResSq)
* [<strong>isDynamic(</strong> ) ](./Problem.md#isDynamic)
* [<strong>domain2Unit(</strong> dval, kpar ) ](./Problem.md#domain2Unit)
* [<strong>unit2Domain(</strong> uval, kpar ) ](./Problem.md#unit2Domain)
* [<strong>shortName(</strong> ) ](./Problem.md#shortName)
