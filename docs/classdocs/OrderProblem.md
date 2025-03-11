---
---
<br><br>

<a name="OrderProblem"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class OrderProblem(</strong> <a href="./Problem.html">Problem</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/OrderProblem.py target=_blank>Source</a></th></tr></thead></table>
<p>

An OrderProblem needs to optimize the order of a set of nodes.
the nodes are given by the x variable; the order by the parameters p.

The result of the function for certain x and p is given by
`problem.result( x, p )`

This class is a base class. Further specializations will define the
result method.

<b>Attributes</b><br>
* parameters  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be optimized in TBD ways<br>
* npbase  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of params in the base model<br>
* ndim  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of dimensions of input. (default : 1)<br>

* Author  :          Do Kester<br>


<a name="OrderProblem"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>OrderProblem(</strong> xdata=None, weights=None, copy=None )
</th></tr></thead></table>
<p>

OrderProblem Constructor.
<br>
<b>Parameters</b><br>
* xdata  :  array_like of shape [np,ndim]<br>
&nbsp;&nbsp;&nbsp;&nbsp; the nodes to be visited<br>
* weights  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights on the arrival nodes<br>
* copy  :  BaseProblem<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be copied<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> ) 
</th></tr></thead></table>
<p>
Return a copy. 

<a name="isDynamic"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isDynamic(</strong> ) 
</th></tr></thead></table>
<p>
<a name="myEngines"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>myEngines(</strong> ) 
</th></tr></thead></table>
<p>
<a name="myStartEngine"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>myStartEngine(</strong> ) 
</th></tr></thead></table>
<p>
<a name="myDistribution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>myDistribution(</strong> ) 
</th></tr></thead></table>
<p>
<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> ) 
</th></tr></thead></table>
<p>
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Problem.html">Problem</a></th></tr></thead></table>


* [<strong>setAccuracy(</strong> accuracy=None ) ](./Problem.md#setAccuracy)
* [<strong>hasWeights(</strong> )](./Problem.md#hasWeights)
* [<strong>result(</strong> param )](./Problem.md#result)
* [<strong>residuals(</strong> param, mockdata=None ) ](./Problem.md#residuals)
* [<strong>cyclicCorrection(</strong> res )](./Problem.md#cyclicCorrection)
* [<strong>cycor1(</strong> res )](./Problem.md#cycor1)
* [<strong>cycor2(</strong> res )](./Problem.md#cycor2)
* [<strong>cyclize(</strong> res, period ) ](./Problem.md#cyclize)
* [<strong>weightedResSq(</strong> allpars, mockdata=None, extra=False ) ](./Problem.md#weightedResSq)
* [<strong>domain2Unit(</strong> dval, kpar ) ](./Problem.md#domain2Unit)
* [<strong>unit2Domain(</strong> uval, kpar ) ](./Problem.md#unit2Domain)
* [<strong>shortName(</strong> ) ](./Problem.md#shortName)
