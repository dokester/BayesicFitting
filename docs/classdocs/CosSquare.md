---
---
<br><br>

<a name="CosSquare"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class CosSquare(</strong> <a href="./Kernel.html">Kernel</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/CosSquare.py target=_blank>[source]</a></th></tr></thead></table>
<p>

CosSquare (Cosine Squared) is a Kernel function between [-1,1]; it is 0 elsewhere.

&nbsp;&nbsp;&nbsp;&nbsp; K( x ) = cos<sup>2</sup>( 0.5 &pi; x )  if |x| < 1 else 0



<a name="CosSquare"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>CosSquare(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/CosSquare.py#L38-L47 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

Using
<br>&nbsp;&nbsp;&nbsp;&nbsp; integral = 1.0
<br>&nbsp;&nbsp;&nbsp;&nbsp; fwhm = 1.0


<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/CosSquare.py#L49-L59 target=_blank>[source]</a></th></tr></thead></table>
Return the result for input values.

<b>Parameters</b><br>
* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; input values

<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/CosSquare.py#L61-L70 target=_blank>[source]</a></th></tr></thead></table>
Return the partial derivative wrt the input values.

<b>Parameters</b><br>
* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the input values

<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/CosSquare.py#L72-L74 target=_blank>[source]</a></th></tr></thead></table>

Return True 
<a name="name"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>name(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/CosSquare.py#L76-L78 target=_blank>[source]</a></th></tr></thead></table>

Return the name of the kernel 
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Kernel.html">Kernel</a></th></tr></thead></table>


* [<strong>resultsq(</strong> xsq )](./Kernel.md#resultsq)
