---
---
<br><br>

<a name="Triweight"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class Triweight(</strong> <a href="./Kernel.html">Kernel</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Triweight.py target=_blank>[source]</a></th></tr></thead></table>
<p>

Triweight is a Kernel function between [-1,1]; it is 0 elsewhere.

&nbsp; K( x ) = ( 1 - x<sup>2</sup> )<sup>3</sup> if |x| < 1 else 0


<a name="Triweight"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Triweight(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Triweight.py#L40-L48 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

Using
<br>&nbsp;&nbsp;&nbsp;&nbsp; integral = 32.0/35.0
<br>&nbsp;&nbsp;&nbsp;&nbsp; fwhm = 0.908404

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Triweight.py#L50-L59 target=_blank>[source]</a></th></tr></thead></table>
Return the result for input values.

<b>Parameters</b><br>
* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; input values

<a name="resultsq"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>resultsq(</strong> xsq )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Triweight.py#L61-L71 target=_blank>[source]</a></th></tr></thead></table>
Return the result for squared input values.

<b>Parameters</b><br>
* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the squares of the input values

<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Triweight.py#L73-L83 target=_blank>[source]</a></th></tr></thead></table>
Return the partial derivative wrt the input values.

<b>Parameters</b><br>
* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the input values

<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Triweight.py#L85-L87 target=_blank>[source]</a></th></tr></thead></table>

Return True 
<a name="name"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>name(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Triweight.py#L89-L91 target=_blank>[source]</a></th></tr></thead></table>

Return the name of the kernel 
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Kernel.html">Kernel</a></th></tr></thead></table>


