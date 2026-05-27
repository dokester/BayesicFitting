---
---
<br><br>

<a name="Gauss"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class Gauss(</strong> <a href="./Kernel.html">Kernel</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Gauss.py target=_blank>[source]</a></th></tr></thead></table>
<p>

Gauss is an unbound Kernel function

&nbsp; f( x ) = exp( -0.5 * x * x ).


<a name="Gauss"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Gauss(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Gauss.py#L41-L52 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

&nbsp; Using
<br>&nbsp; integral = sqrt( 2 &pi; )
<br>&nbsp; fwhm = sqrt( 2 log( 2 ) )
<br>&nbsp; range = inf

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Gauss.py#L54-L63 target=_blank>[source]</a></th></tr></thead></table>
Return the result for input values.

<b>Parameters</b><br>
* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; input values

<a name="resultsq"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>resultsq(</strong> xsq )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Gauss.py#L65-L74 target=_blank>[source]</a></th></tr></thead></table>
Return the result for squared input values.   

<b>Parameters</b><br>
* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the squares of the input values                                     

<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Gauss.py#L76-L85 target=_blank>[source]</a></th></tr></thead></table>
Return the partial derivative wrt the input values.

<b>Parameters</b><br>
* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the input values

<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Gauss.py#L87-L89 target=_blank>[source]</a></th></tr></thead></table>

Return False 
<a name="name"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>name(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Gauss.py#L91-L93 target=_blank>[source]</a></th></tr></thead></table>

Return the name of the kernel 
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Kernel.html">Kernel</a></th></tr></thead></table>


