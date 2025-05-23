---
---
<br><br>

<a name="Gauss"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Gauss(</strong> <a href="./Kernel.html">Kernel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Gauss.py target=_blank>Source</a></th></tr></thead></table>

Gauss is an unbound Kernel function

&nbsp; f( x ) = exp( -0.5 * x * x ).


<a name="Gauss"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Gauss(</strong> ) 
</th></tr></thead></table>

Constructor.

&nbsp; Using
<br>&nbsp; integral = sqrt( 2 &pi; )
<br>&nbsp; fwhm = sqrt( 2 log( 2 ) )
<br>&nbsp; range = inf

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th></tr></thead></table>
Return the result for input values.

<b>Parameters</b>

* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; input values

<a name="resultsq"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>resultsq(</strong> xsq )
</th></tr></thead></table>
Return the result for squared input values.   

<b>Parameters</b>

* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the squares of the input values                                     

<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> x )
</th></tr></thead></table>
Return the partial derivative wrt the input values.

<b>Parameters</b>

* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the input values

<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th></tr></thead></table>

Return False 
<a name="name"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>name(</strong> )
</th></tr></thead></table>

Return the name of the kernel 
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Kernel.html">Kernel</a></th></tr></thead></table>


