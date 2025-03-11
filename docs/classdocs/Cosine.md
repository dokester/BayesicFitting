---
---
<br><br>

<a name="Cosine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Cosine(</strong> <a href="./Kernel.html">Kernel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Cosine.py target=_blank>Source</a></th></tr></thead></table>
<p>

Cosine is a Kernel function between [-1,1]; it is 0 elsewhere.

<br>&nbsp; K( x ) = cos( 0.5 &pi; x )  if |x| < 1 else 0<br>


<a name="Cosine"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Cosine(</strong> ) 
</th></tr></thead></table>
<p>

Constructor.

<br>&nbsp; Using<br>
&nbsp;&nbsp;&nbsp;&nbsp; integral = 4 / &pi;<br>
&nbsp;&nbsp;&nbsp;&nbsp; fwhm = 4.0 / 3.0<br>


<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th></tr></thead></table>
<p>

Calculate the function.

<b>Parameters</b><br>
* x  :  array_like<br>
    at which to do the calculation

<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> x )
</th></tr></thead></table>
<p>

Return the partial derivative wrt input values.

<b>Parameters</b><br>
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
