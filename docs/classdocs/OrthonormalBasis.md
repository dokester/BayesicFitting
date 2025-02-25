---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/OrthonormalBasis.py target=_blank>Source</a></span></div>

<a name="OrthonormalBasis"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class OrthonormalBasis(</strong> object )
</th></tr></thead></table>
<p>

Helper class to construct a orthonormal basis from (random) vectors

<b>Attributes</b>

* basis  :  2darray<br>
    array of orthonormal vectors<br>

Author       Do Kester.


<a name="OrthonormalBasis"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>OrthonormalBasis(</strong> )
</th></tr></thead></table>
<p>

Constructor.

<a name="normalise"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>normalise(</strong> vec, reset=False ) 
</th></tr></thead></table>
<p>

Construct from vec a unit vector orthogonal to self.basis

from http://www.ecs.umass.edu/ece/ece313/Online_help/gram.pdf

<b>Parameters</b>

* vec  :  array_like<br>
    vector to be orthonomalised to self.basis<br>
* reset  :  bool<br>
    start a new basis.

