---
---
<br><br>

<a name="OrthonormalBasis"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class OrthonormalBasis(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/OrthonormalBasis.py target=_blank>Source</a></th></tr></thead></table>
<p>

Helper class to construct a orthonormal basis from (random) vectors

<b>Attributes</b><br>
* basis  :  2darray<br>
&nbsp;&nbsp;&nbsp;&nbsp; array of orthonormal vectors<br>

Author       Do Kester.


<a name="OrthonormalBasis"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>OrthonormalBasis(</strong> )
</th></tr></thead></table>
<p>

Constructor.

<a name="normalise"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>normalise(</strong> vec, reset=False ) 
</th></tr></thead></table>
<p>

Construct from vec a unit vector orthogonal to self.basis

from http://www.ecs.umass.edu/ece/ece313/Online<sub>help</sub>/gram.pdf

<b>Parameters</b><br>
* vec  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; vector to be orthonomalised to self.basis<br>
* reset  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; start a new basis.<br>

<b>Return</b><br>
* uvec  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; unit vector normal to the basis<br>


