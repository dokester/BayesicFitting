---
---
<br><br>

<a name="Tricube"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Tricube(</strong> <a href="./Kernel.html">Kernel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Tricube.py target=_blank>Source</a></th></tr></thead></table>
<p>

Tricube is a Kernel function between [-1,1]; it is 0 elsewhere.

 K( x ) = ( 1 - |x|^3 )^3  if |x| < 1 else 0<br>


<a name="Tricube"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Tricube(</strong> ) 
</th></tr></thead></table>
<p>

Constructor.

Using
    integral = 81.0/70.0<br>
    fwhm = 1.18176021

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
Return True 

<a name="name"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>name(</strong> )
</th></tr></thead></table>
<p>
Return the name of the kernel 

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Kernel.html">Kernel</a></th></tr></thead></table>


* [<strong>resultsq(</strong> xsq )](./Kernel.md#resultsq)
