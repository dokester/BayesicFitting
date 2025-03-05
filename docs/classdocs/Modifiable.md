---
---
<br><br>

<a name="Modifiable"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Modifiable(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Modifiable.py target=_blank>Source</a></th></tr></thead></table>
<p>

Class adjoint to Model which implements the modifiable behaviour of some Models.

In the inhertance list is should be *before* Model as it changes the behaviour of Model.


<a name="Modifiable"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Modifiable(</strong> modifiable=True ) 
</th></tr></thead></table>
<p>

Constructor for Modifiable

<b>Parameters</b>

* modifiable :  bool<br>
    True if the Model is to be considered modifiable.

<a name="isModifiable"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isModifiable(</strong> ) 
</th></tr></thead></table>
<p>
<a name="vary"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>vary(</strong> location=None, rng=None, **kwargs ) 
</th></tr></thead></table>
<p>

Vary the structure of a Modifiable Model
Default implementation: does nothing.

<b>Parameters</b>

* location  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index of the item to be modified; otherwise random<br>
* rng  :  RNG<br>
&nbsp;&nbsp;&nbsp;&nbsp; random number generator<br>
* kwargs  :  keyword arguments<br>
    for specific implementations

