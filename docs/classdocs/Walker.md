---
---
<br><br><br>

<a name="Walker"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Walker(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Walker.py target=_blank>Source</a></th></tr></thead></table>
<p>

Walker is member of the cloud of points used in NestedSampler.

<b>Attributes</b>

* id  :  int<br>
    identification number<br>
* parent  :  int<br>
    id of the parent (-1 for Adam/Eve)<br>
* start  :  int<br>
    iteration in which the walker is constructed<br>
* step  :  int<br>
    number of randomization steps since copy<br>
* problem  :  Problem<br>
    the problem being addressed<br>
* logL  :  float<br>
    log Likelihood = log Prob( data | params )<br>
* logPrior  :  float<br>
    log Prior for the model<br>
* allpars  :  array_like<br>
    list of parameters and hyperparameters<br>
* fitIndex  :  array_like<br>
    list of (super)parameters to be fitted.<br>
* parameters  :  array_like (read only)<br>
    parameters (of the model)<br>
* hypars  :  array_like (read only)<br>
    list of hyper parameters (of the error distribution)<br>

Author       Do Kester


<a name="Walker"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Walker(</strong> wid, problem, allpars, fitIndex, logL=0, parent=-1, start=0, copy=None )
</th></tr></thead></table>
<p>

Constructor.

Either errdis or copy is obligatory.

<b>Parameters</b>

* wid  :  int<br>
    id of the walker<br>
* problem  :  Problem<br>
    the problem being used. Parameters are copied from its model.<br>
* allpars  :  array_like<br>
    array of parameters and hyperparameters<br>
* fitIndex  :  None or array_like<br>
    indices of allpars to be fitted<br>
    None is all<br>
* logL  :  float<br>
    log Likelihood<br>
* parent  :  int<br>
    id of the parent (-1 for Adam/Eve)<br>
* start  :  int<br>
    iteration in which the walker is constructed<br>
* copy  :  Walker<br>
    the walker to be copied<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>

Copy.


<a name="toSample"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>toSample(</strong> logW ) 
</th></tr></thead></table>
<p>

Return the contents of the Walker as a Sample.

<a name="check"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>check(</strong> nhyp=0, nuisance=0 ) 
</th></tr></thead></table>
<p>

Perform some sanity checks.

