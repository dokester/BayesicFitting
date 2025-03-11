---
---
<br><br>

<a name="IterationPlotter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class IterationPlotter(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/IterationPlotter.py target=_blank>Source</a></th></tr></thead></table>

The IterationPlotter plots intermediate results from a iterative fitter.

Author:      Do Kester


<a name="plotData"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotData(</strong> x, y, title )
</th></tr></thead></table>

Plot the data.

<b>Parameters</b>

* x  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; x-axis values of the data
* y  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; y-axis values of the data
* title  :  string
<br>&nbsp;&nbsp;&nbsp;&nbsp; the title of the plot

<a name="plotResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotResult(</strong> x, r, iter )
</th></tr></thead></table>
Plot the ( intermediate ) result.

<b>Parameters</b>

* x  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; x-axis values of the data
* r  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; model result
* iter  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; iteration number

<a name="plotProgress"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotProgress(</strong> percent )
</th></tr></thead></table>
Plot (estimated) progress upto now.


