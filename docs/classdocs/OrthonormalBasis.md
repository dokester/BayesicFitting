---
---
<br><br>

<a name="OrthonormalBasis"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class OrthonormalBasis(</strong> object )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source// target=_blank>[source]</a></th></tr></thead></table>
<p>

Helper class to construct a orthonormal basis from (random) vectors

<b>Attributes</b>

* basis  :  2darray
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of orthonormal vectors

Author       Do Kester.


<a name="OrthonormalBasis"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>OrthonormalBasis(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L41-L45 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

<a name="normalise"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>normalise(</strong> vec, reset=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L47-L86 target=_blank>[source]</a></th></tr></thead></table>
Construct from vec a unit vector orthogonal to self.basis

from http://www.ecs.umass.edu/ece/ece313/Online<sub>help</sub>/gram.pdf

<b>Parameters</b>

* vec  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; vector to be orthonomalised to self.basis
* reset  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; start a new basis.

<b>Return</b>

* uvec  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; unit vector normal to the basis


