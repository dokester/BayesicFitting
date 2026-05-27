---
---
<br><br>

<a name="Huber"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class Huber(</strong> <a href="./Kernel.html">Kernel</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Huber.py target=_blank>[source]</a></th></tr></thead></table>
<p>

Huber is an improper Kernel function

&nbsp; K( x ) = 1.0 if |x| < 1 else 1.0 / |x|

It is improper because the integral equals +inf.

It plays a role in robust fitting, see RobustShell, for medianizing the fit.


<a name="Huber"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Huber(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Huber.py#L41-L52 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

Improper Kernel.

&nbsp; Using
<br>&nbsp; integral = inf
<br>&nbsp; fwhm = 4
<br>&nbsp; range = inf

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Huber.py#L54-L64 target=_blank>[source]</a></th></tr></thead></table>
Return the result for input values.

<b>Parameters</b><br>
* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; input values

<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Huber.py#L66-L76 target=_blank>[source]</a></th></tr></thead></table>
Return the partial derivative wrt the input values.

<b>Parameters</b><br>
* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the input values

<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Huber.py#L78-L80 target=_blank>[source]</a></th></tr></thead></table>

Return False 
<a name="name"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>name(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Huber.py#L82-L84 target=_blank>[source]</a></th></tr></thead></table>

Return the name of the kernel 
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Kernel.html">Kernel</a></th></tr></thead></table>


* [<strong>resultsq(</strong> xsq )](./Kernel.md#resultsq)
