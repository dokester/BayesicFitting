---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Parabola.py target=_blank>Source</a></span></div>

<a name="Parabola"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class Parabola(</strong> <a href="./Kernel.html">Kernel</a> )
</th></tr></thead></table>
<p>

Parabola is a Kernel function between [-1,1]; it is 0 elsewhere.

    K( x ) = ( 1-x^2 )      if |x| < 1<br>
             0              elsewhere<br>


<a name="Parabola"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>Parabola(</strong> ) 
</th></tr></thead></table>
<p>

Constructor.

Using
    integral = 4.0/3.0<br>
    fwhm = 2 sqrt( 0.5 )

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>result(</strong> x )
</th></tr></thead></table>
<p>
<a name="resultsq"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>resultsq(</strong> xsq )
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


