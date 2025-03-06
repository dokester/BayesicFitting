---
---
<br><br>

<a name="EvidenceProblem"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class EvidenceProblem(</strong> <a href="./ClassicProblem.html">ClassicProblem</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EvidenceProblem.py target=_blank>Source</a></th></tr></thead></table>
<p>

An EvidenceProblem is a ClassicProblem containing a Dynamic and/or Modifiable
model, where the (Gauss-approximated) evidence is used as likelihood

Problems can be solved by NestedSampler, with appropriate Engines and
ErrorDistributions.

The result of the function for certain x and p is given by
problem.result( x, p )
The parameters, p, are to be optimized while the x provide additional
information.

<b>Attributes from Problem</b>

model, xdata, ydata, weights

* Author  :          Do Kester<br>


<a name="EvidenceProblem"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>EvidenceProblem(</strong> model=None, xdata=None, ydata=None, weights=None, copy=None )
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
* copy  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be copied<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>

Copy.

The copy points to the same instance of model.

<a name="myEngines"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>myEngines(</strong> ) 
</th></tr></thead></table>
<p>

Return a default list of preferred engines

<a name="myDistribution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>myDistribution(</strong> ) 
</th></tr></thead></table>
<p>

Return the default preferred ModelDistribution: "model"

<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>
<p>
Returns a string representation of the model. 

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./ClassicProblem.html">ClassicProblem</a></th></tr></thead></table>


* [<strong>result(</strong> param )](./ClassicProblem.md#result)
* [<strong>partial(</strong> param ) ](./ClassicProblem.md#partial)
* [<strong>derivative(</strong> param ) ](./ClassicProblem.md#derivative)
* [<strong>myStartEngine(</strong> ) ](./ClassicProblem.md#myStartEngine)


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
