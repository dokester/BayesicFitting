---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Triangle.py target=_blank>Source</a></span></div>

<a name="Triangle"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class Triangle(</strong> <a href="./Kernel.html">Kernel</a> )
</th></tr></thead></table>
<p>

Triangle is a Kernel function between [-1,1]; it is 0 elsewhere.

    K( x ) = ( 1 - |x| )        if |x| < 1<br>
             0                  elsewhere<br>


<a name="Triangle"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>Triangle(</strong> ) 
</th></tr></thead></table>
<p>

Constructor.

Using
    integral = 1.0K6.0/15.0<br>
    fwhm = 1.0

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th></tr></thead></table>
<p>
<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>partial(</strong> x )
</th></tr></thead></table>
<p>
<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>isBound(</strong> )
</th></tr></thead></table>
<p>
<a name="name"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>name(</strong> )
</th></tr></thead></table>
<p>
<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Kernel.html">Kernel</a></th></tr></thead></table>


* [<strong>resultsq(</strong> xsq )](./Kernel.md#resultsq)
