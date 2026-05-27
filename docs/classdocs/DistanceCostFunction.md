---
---
<br><br>

<a name="DistanceCostFunction"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class DistanceCostFunction(</strong> <a href="./ErrorDistribution.html">ErrorDistribution</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/DistanceCostFunction.py target=_blank>[source]</a></th></tr></thead></table>
<p>

To calculate a distance based cost function

For one observation with n counts it holds

&nbsp;&nbsp;&nbsp;&nbsp; f( d ) = exp( -SUM( d / s ) )

where d are the distances and s is the scale

The function is mostly used to calculate the likelihood L of
traveling-salesman-like problems

Author       Do Kester.


<a name="DistanceCostFunction"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>DistanceCostFunction(</strong> copy=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/DistanceCostFunction.py#L52-L62 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

<b>Parameters</b><br>
* copy  :  DistanceCostFunction
<br>&nbsp;&nbsp;&nbsp;&nbsp; distribution to be copied.


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/DistanceCostFunction.py#L64-L66 target=_blank>[source]</a></th></tr></thead></table>

Return copy of this. 
<a name="acceptWeight"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>acceptWeight(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/DistanceCostFunction.py#L68-L75 target=_blank>[source]</a></th></tr></thead></table>
True if the distribution accepts weights.
Always false for this distribution.

<a name="logLikelihood_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logLikelihood_alt(</strong> problem, allpars )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/DistanceCostFunction.py#L77-L92 target=_blank>[source]</a></th></tr></thead></table>
Return the negative sum of the distances.

<b>Parameters</b><br>
* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem


<a name="logLdata"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logLdata(</strong> problem, allpars )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/DistanceCostFunction.py#L94-L106 target=_blank>[source]</a></th></tr></thead></table>
Return the individual distances (multiplied by the weights).

<b>Parameters</b><br>
* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem


<a name="partialLogL"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialLogL(</strong> model, param, fitIndex )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/DistanceCostFunction.py#L108-L122 target=_blank>[source]</a></th></tr></thead></table>
Does not work for this class

<b>Parameters</b><br>
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to calculate mock data
* param  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters of the model
* fitIndex  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of the params to be fitted

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./ErrorDistribution.html">ErrorDistribution</a></th></tr></thead></table>


* [<strong>getGaussianScale(</strong> problem, allpars=None ) ](./ErrorDistribution.md#getGaussianScale)
* [<strong>getResiduals(</strong> problem, allpars=None )](./ErrorDistribution.md#getResiduals)
* [<strong>getChisq(</strong> problem, allpars=None )](./ErrorDistribution.md#getChisq)
* [<strong>toSigma(</strong> scale ) ](./ErrorDistribution.md#toSigma)
* [<strong>isBound(</strong> ) ](./ErrorDistribution.md#isBound)
* [<strong>keepFixed(</strong> fixed=None ) ](./ErrorDistribution.md#keepFixed)
* [<strong>setPriors(</strong> priors ) ](./ErrorDistribution.md#setPriors)
* [<strong>setLimits(</strong> limits ) ](./ErrorDistribution.md#setLimits)
* [<strong>domain2Unit(</strong> dval, ks ) ](./ErrorDistribution.md#domain2Unit)
* [<strong>unit2Domain(</strong> uval, ks ) ](./ErrorDistribution.md#unit2Domain)
* [<strong>logCLhood(</strong> problem, allpars )](./ErrorDistribution.md#logCLhood)
* [<strong>logLhood(</strong> problem, allpars )](./ErrorDistribution.md#logLhood)
* [<strong>partialLogL_alt(</strong> problem, allpars, fitIndex ) ](./ErrorDistribution.md#partialLogL_alt)
* [<strong>numPartialLogL(</strong> problem, allpars, fitIndex ) ](./ErrorDistribution.md#numPartialLogL)
* [<strong>updateLogL(</strong> problem, allpars, parval=None )](./ErrorDistribution.md#updateLogL)
* [<strong>hyparname(</strong> k ) ](./ErrorDistribution.md#hyparname)
