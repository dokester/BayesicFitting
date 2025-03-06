---
---
<br><br>

<a name="Huber"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Huber(</strong> <a href="./Kernel.html">Kernel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Huber.py target=_blank>Source</a></th></tr></thead></table>
<p>

Huber is an improper Kernel function

&nbsp; K( x ) = 1.0 if |x| < 1 else 1.0 / |x|<br>

It is improper because the integral equals +inf.

It plays a role in robust fitting, see RobustShell, for medianizing the fit.


<a name="Huber"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Huber(</strong> ) 
</th></tr></thead></table>
<p>

Constructor.

Improper Kernel.

&nbsp; Using<br>
&nbsp; integral = inf<br>
&nbsp; fwhm = 4<br>
 range = inf

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th></tr></thead></table>
<p>

Return the result for input values.

<b>Parameters</b>

* x  :  array-like<br>
    input values

<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> x )
</th></tr></thead></table>
<p>

Return the partial derivative wrt the input values.

<b>Parameters</b>

* x  :  array-like<br>
    the input values

<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th></tr></thead></table>
<p>
Return False 

<a name="name"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>name(</strong> )
</th></tr></thead></table>
<p>
Return the name of the kernel 

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Kernel.html">Kernel</a></th></tr></thead></table>


* [<strong>resultsq(</strong> xsq )](./Kernel.md#resultsq)
