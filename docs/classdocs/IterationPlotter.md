---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/IterationPlotter.py target=_blank>Source</a></span></div>

<a name="IterationPlotter"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class IterationPlotter(</strong> object )
</th></tr></thead></table>
<p>

The IterationPlotter plots intermediate results from a iterative fitter.

Author:      Do Kester


<a name="plotData"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>plotData(</strong> x, y, title )
</th></tr></thead></table>
<p>

Plot the data.

<b>Parameters</b>

* x  :  array_like<br>
    x-axis values of the data<br>
* y  :  array_like<br>
    y-axis values of the data<br>
* title  :  string<br>
    the title of the plot

<a name="plotResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>plotResult(</strong> x, r, iter )
</th></tr></thead></table>
<p>

Plot the ( intermediate ) result.

<b>Parameters</b>

* x  :  array_like<br>
    x-axis values of the data<br>
* r  :  array_like<br>
    model result<br>
* iter  :  int<br>
    iteration number

<a name="plotProgress"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>plotProgress(</strong> percent )
</th></tr></thead></table>
<p>

Plot (estimated) progress upto now.


