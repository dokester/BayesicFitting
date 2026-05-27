---
---
<br><br>

<a name="Uniform"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class Uniform(</strong> <a href="./Kernel.html">Kernel</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Uniform.py target=_blank>[source]</a></th></tr></thead></table>
<p>

Uniform is a Kernel function which is constant between [-1,1].

&nbsp;&nbsp;&nbsp;&nbsp; K( x ) = 1.0        if |x| < 1
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0.0        elsewhere


<a name="Uniform"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Uniform(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Uniform.py#L41-L49 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

Using
<br>&nbsp;&nbsp;&nbsp;&nbsp; integral = 2.0
<br>&nbsp;&nbsp;&nbsp;&nbsp; fwhm = 2.0

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Uniform.py#L51-L61 target=_blank>[source]</a></th></tr></thead></table>
Return the result for input values.

<b>Parameters</b><br>
* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; input values

<a name="resultsq"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>resultsq(</strong> xsq )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Uniform.py#L63-L72 target=_blank>[source]</a></th></tr></thead></table>
Return the result for input values. Same as result.

<b>Parameters</b><br>
* xsq  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; input values

<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Uniform.py#L74-L83 target=_blank>[source]</a></th></tr></thead></table>
Return the partial derivative wrt the input values.

<b>Parameters</b><br>
* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the input values

<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Uniform.py#L85-L87 target=_blank>[source]</a></th></tr></thead></table>

Return True 
<a name="name"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>name(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Uniform.py#L89-L91 target=_blank>[source]</a></th></tr></thead></table>

Return the name of the kernel 
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Kernel.html">Kernel</a></th></tr></thead></table>


