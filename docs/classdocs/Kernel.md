---
---
<br><br>

<a name="Kernel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Kernel(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/kernels/Kernel.py target=_blank>Source</a></th></tr></thead></table>

A kernel is an even real-valued integrable function.

It is satisfying the following two requirements

1. The integral over [-Inf,+Inf] exists ( < Inf ).
2. It is an even function: K( x ) = K( -x ).

A kernel is called bound when it is 0 everywhere
except when |x| < range < inf.

All kernels are scaled such that its value at x=0 is 1.0.

Several kernel functions, K( x ) are defined in this package

| Name      | Definition        | Integral  | FWHM | range | comment     |
|-----------|-------------------|:---------:|:----:|:-----:|-------------|
| Biweight  | ( 1-x<sup>2</sup> )<sup>2</sup>       |     16/15 | 1.08 |  1.0  | aka Tukey   |
| CosSquare | cos<sup>2</sup>(0.5*&pi;*x) |       1.0 | 1.00 |  1.0  |             |
| Cosine    | cos( 0.5*&pi;*x ) |    4/&pi; | 1.33 |  1.0  |             |
| Gauss     | exp( -0.5*x<sup>2</sup> ) |&radic;(2*&pi;)|1.22|  inf  |             |
| Huber     | min( 1, 1/\|x\| ) |       inf | 4.00 |  inf  | improper    |
|           |                   |           |      |       | aka Median  |
| Lorentz   | 1 / ( 1 + x<sup>2</sup> )   |      &pi; | 2.00 |  inf  |             |
| Parabola  | 1 - x<sup>2</sup>           |       4/3 | 1.41 |  1.0  |             |
| Sinc      | sin(&pi;*x)/(&pi;*x)|     1.0 | 1.21 |  inf  |             |
| Triangle  | 1 - \|x\|         |       1.0 | 1.00 |  1.0  |             |
| Tricube   | ( 1 - \|x\|<sup>3</sup> )<sup>3</sup> |     81/70 | 1.18 |  1.0  |             |
| Triweight | ( 1 - x<sup>2</sup> )<sup>3</sup>     |     32/35 | 0.91 |  1.0  |             |
| Uniform   | 1.0               |       2.0 | 2.00 |  1.0  | aka Clip    |
| Tophat 0  | 1.0               |       1.0 | 1.00 |  0.5  | like Uniform|
| Tophat 1  | 1 - \|x\|         |       1.0 | 1.00 |  1.0  | aka Triangle|
| Tophat 2  | 2nd order polynome|       1.0 | 1.26 |  1.5  |             |
| Tophat 3  | 3rd order polynome|       1.0 | 1.44 |  2.0  |             |
| Tophat 4  | 4th order polynome|       1.0 | 1.60 |  2.5  |             |
| Tophat 5  | 5th order polynome|       1.0 | 1.73 |  3.0  |             |
| Tophat 6  | 6th order polynome|       1.0 | 1.86 |  3.5  |             |

For all bound Kernels the definition in the table is true for |x| < range;
elsewhere it is 0.

Huber is not a proper Kernel as the integral is inf. However it is important
in robust fitting (RobustShell) to get a madian-like solution for the outliers.

<b>Attributes</b>

* integral  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the integral over the valid range
* fwhm  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the full width at half maximum
* range  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the region [-range..+range] where the kernel is non-zero.

Author      Do Kester

Category    mathematics/Fitting


<a name="Kernel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Kernel(</strong> integral=1.0, fwhm=1.0, range=1.0 ) 
</th></tr></thead></table>

Constructor

<b>Parameters</b>

* integral  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; over [-inf, +inf]
* fwhm  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; full width at half maximum
* range  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the region [-range,+range] where the kernel is nonzero

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
Return true when the kernel is bound, i.e.
all non-zero values are between -1 and +1

<a name="name"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>name(</strong> )
</th></tr></thead></table>
Return the name of the kernel.

