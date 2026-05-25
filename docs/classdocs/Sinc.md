---
---
<br><br>

<a name="Sinc"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class Sinc(</strong> <a href="./Kernel.html">Kernel</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Sinc.py target=_blank>[source]</a></th></tr></thead></table>
<p>

Sinc is an unbound Kernel function.

&nbsp; K( x ) = sin( &pi; x ) / ( &pi; x )

Sinc is not strictly positive.


<a name="Sinc"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Sinc(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Sinc.py#L45-L55 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

&nbsp; Using
<br>&nbsp; integral = 1.0
<br>&nbsp; fwhm = 2 * 1.8954942670 / &pi;
<br>&nbsp; range = inf

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Sinc.py#L57-L67 target=_blank>[source]</a></th></tr></thead></table>
Return the result for input values.

<b>Parameters</b>

* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; input values

<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Sinc.py#L69-L80 target=_blank>[source]</a></th></tr></thead></table>
Return the partial derivative wrt the input values.

<b>Parameters</b>

* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the input values

<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Sinc.py#L82-L84 target=_blank>[source]</a></th></tr></thead></table>

Return False 
<a name="name"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>name(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Sinc.py#L86-L88 target=_blank>[source]</a></th></tr></thead></table>

Return the name of the kernel 
Endline #L90
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Kernel.html">Kernel</a></th></tr></thead></table>


* [<strong>resultsq(</strong> xsq )](./Kernel.md#resultsq)
