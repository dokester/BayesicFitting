---
---
<br><br>

<a name="Tophat"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class Tophat(</strong> <a href="./Kernel.html">Kernel</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source// target=_blank>[source]</a></th></tr></thead></table>
<p>

Tophat (without convolutions) is a Kernel function which is 1.0 
between [-0.5,0.5]; it is 0 elsewhere.

| Name      | Definition          | Integral  | FWHM | range | comment     |
|:----------|:--------------------|----------:|:----:|:-----:|:------------|
| Tophat 0  | 1.0                 |      1.0  | 1.00 |  0.5  | like Uniform|
| Tophat 1  | 1 - \|x\|           |      1.0  | 1.00 |  1.0  | aka Triangle|
| Tophat 2  | 2nd order polynomial|      1.0  | 1.26 |  1.5  |             |
| Tophat 3  | 3rd order polynomial|      1.0  | 1.44 |  2.0  |             |
| Tophat 4  | 4th order polynomial|      1.0  | 1.60 |  2.5  |             |
| Tophat 5  | 5th order polynomial|      1.0  | 1.73 |  3.0  |             |
| Tophat 6  | 6th order polynomial|      1.0  | 1.86 |  3.5  |             |

<b>Attributes</b>

* nconv  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; successive autoconvolutions of the tophat. max=6.

Thanks to Romke Bontekoe and Mathematica for providing the analytic expressions.


<a name="Tophat"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Tophat(</strong> nconv=0 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L58-L90 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

Integral, fwhm and range are dependent on the number of convolutions.
See table above.

<b>Parameters</b>

* nconv  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of auto-convolutions


<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L92-L101 target=_blank>[source]</a></th></tr></thead></table>
Return the result for input values.

<b>Parameters</b>

* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; input values

<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> x )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L103-L112 target=_blank>[source]</a></th></tr></thead></table>
Return the partial derivative wrt the input values.

<b>Parameters</b>

* x  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the input values

<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L114-L116 target=_blank>[source]</a></th></tr></thead></table>

Return True 
<a name="name"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>name(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L118-L120 target=_blank>[source]</a></th></tr></thead></table>

Return the name of the kernel 
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Kernel.html">Kernel</a></th></tr></thead></table>


* [<strong>resultsq(</strong> xsq )](./Kernel.md#resultsq)
