---
---
<br><br>

<a name="Cosine"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class Cosine(</strong> <a href="./Kernel.html">Kernel</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Cosine.py target=_blank>[source]</a></th></tr></thead></table>
<p>

Cosine is a Kernel function between [-1,1]; it is 0 elsewhere.

&nbsp; K( x ) = cos( 0.5 &pi; x )  if |x| < 1 else 0


<a name="Cosine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Cosine(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Cosine.py#L43-L52 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

&nbsp; Using
<br>&nbsp;&nbsp;&nbsp;&nbsp; integral = 4 / &pi;
<br>&nbsp;&nbsp;&nbsp;&nbsp; fwhm = 4.0 / 3.0


<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Cosine.py#L54-L63 target=_blank>[source]</a></th></tr></thead></table>
Calculate the function.

<b>Parameters</b><br>
* x  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; at which to do the calculation

<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Cosine.py#L65-L75 target=_blank>[source]</a></th></tr></thead></table>
Return the partial derivative wrt input values.

<b>Parameters</b><br>
* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the input values

<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Cosine.py#L77-L79 target=_blank>[source]</a></th></tr></thead></table>

Return True 
<a name="name"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>name(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Cosine.py#L81-L83 target=_blank>[source]</a></th></tr></thead></table>

Return the name of the kernel 
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Kernel.html">Kernel</a></th></tr></thead></table>


* [<strong>resultsq(</strong> xsq )](./Kernel.md#resultsq)
