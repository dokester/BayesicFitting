---
---
<br><br>

<a name="GaussErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class GaussErrorDistribution(</strong> <a href="./ScaledErrorDistribution.html">ScaledErrorDistribution</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source// target=_blank>[source]</a></th></tr></thead></table>
<p>

To calculate a Gauss likelihood.

For one residual, x, it holds

&nbsp; L( x ) = 1 / &radic;( 2 &pi; s<sup>2</sup> ) exp( - 0.5 ( x / s )<sup>2</sup> )

where s is the scale.
s is a hyperparameter, which might be estimated from the data.

The scale s is also the square root of the variance of this error distribution.

The function is mostly used to calculate the likelihood L over N residuals,
or easier to use log likelihood, logL.

&nbsp; logL = log( N / ( &radic;( 2 &pi; ) s )  ) - 0.5 &sum;( x / s )<sup>2</sup>

Using weights this becomes

&nbsp; logL = log( &sum;( w ) / ( &radic;( 2 &pi; ) s )  ) - 0.5 &sum;( w ( x / s )<sup>2</sup> )


Author       Do Kester.


<a name="GaussErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>GaussErrorDistribution(</strong> scale=1.0, limits=None, copy=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L65-L83 target=_blank>[source]</a></th></tr></thead></table>

Default Constructor.

<b>Parameters</b>

* scale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; noise scale
* limits  :  None or list of 2 floats [low,high]
<br>&nbsp;&nbsp;&nbsp;&nbsp; None : no limits implying fixed scale
<br>&nbsp;&nbsp;&nbsp;&nbsp; low     low limit on scale (needs to be >0)
<br>&nbsp;&nbsp;&nbsp;&nbsp; high    high limit on scale
<br>&nbsp;&nbsp;&nbsp;&nbsp; when limits are set, the scale is *not* fixed.

* copy  :  GaussErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; distribution to be copied.


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L85-L87 target=_blank>[source]</a></th></tr></thead></table>

Return copy of this. 
<a name="acceptWeight"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>acceptWeight(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L89-L94 target=_blank>[source]</a></th></tr></thead></table>
True if the distribution accepts weights.
Always true for this distribution.

<a name="getScale"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getScale(</strong> problem, allpars=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L96-L109 target=_blank>[source]</a></th></tr></thead></table>
Return the noise scale.

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; None take parameters from problem.model
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem

<a name="logLikelihood_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logLikelihood_alt(</strong> problem, allpars ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L111-L140 target=_blank>[source]</a></th></tr></thead></table>
Return the log( likelihood ) for a Gaussian distribution.

Alternate calculation

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem


<a name="logLdata"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logLdata(</strong> problem, allpars, mockdata=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L142-L171 target=_blank>[source]</a></th></tr></thead></table>
Return the log( likelihood ) for each residual

logL = sum( logLdata )

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem
* mockdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; as calculated by the model


<a name="partialLogL_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialLogL_alt(</strong> problem, allpars, fitIndex ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L173-L215 target=_blank>[source]</a></th></tr></thead></table>
Return the partial derivative of log( likelihood ) to the parameters in fitIndex.

Alternate calculation

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved.
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; (hyper)parameters of the problem
* fitIndex  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters to be fitted


<a name="nextPartialData"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>nextPartialData(</strong> problem, allpars, fitIndex, mockdata=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L217-L252 target=_blank>[source]</a></th></tr></thead></table>
Return the partial derivative all elements of the log( likelihood )
to the parameters in fitIndex.

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; (hyper)parameters of the problem
* fitIndex  :  array_like of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of allpars to fit
* mockdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; as calculated for the problem

<a name="hessianLogL"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hessianLogL(</strong> problem, allpars, fitIndex ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L254-L296 target=_blank>[source]</a></th></tr></thead></table>
Return the hessian of log( likelihood ) to the parameters in fitIndex.

The hessian is a matrix containing the second derivatives to each
of the parameters.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; hessian = d<sup>2</sup> logL / dp<sub>i</sub> dp<sub>k</sub>

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; (hyper)parameters of the problem
* fitIndex  :  array_like of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of allpars to fit

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./ScaledErrorDistribution.html">ScaledErrorDistribution</a></th></tr></thead></table>


* [<strong>setLimits(</strong> limits ) ](./ScaledErrorDistribution.md#setLimits)


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./ErrorDistribution.html">ErrorDistribution</a></th></tr></thead></table>


* [<strong>getGaussianScale(</strong> problem, allpars=None ) ](./ErrorDistribution.md#getGaussianScale)
* [<strong>getResiduals(</strong> problem, allpars=None )](./ErrorDistribution.md#getResiduals)
* [<strong>getChisq(</strong> problem, allpars=None )](./ErrorDistribution.md#getChisq)
* [<strong>toSigma(</strong> scale ) ](./ErrorDistribution.md#toSigma)
* [<strong>isBound(</strong> ) ](./ErrorDistribution.md#isBound)
* [<strong>keepFixed(</strong> fixed=None ) ](./ErrorDistribution.md#keepFixed)
* [<strong>setPriors(</strong> priors ) ](./ErrorDistribution.md#setPriors)
* [<strong>domain2Unit(</strong> dval, ks ) ](./ErrorDistribution.md#domain2Unit)
* [<strong>unit2Domain(</strong> uval, ks ) ](./ErrorDistribution.md#unit2Domain)
* [<strong>logCLhood(</strong> problem, allpars )](./ErrorDistribution.md#logCLhood)
* [<strong>logLhood(</strong> problem, allpars )](./ErrorDistribution.md#logLhood)
* [<strong>partialLogL(</strong> problem, allpars, fitIndex ) ](./ErrorDistribution.md#partialLogL)
* [<strong>numPartialLogL(</strong> problem, allpars, fitIndex ) ](./ErrorDistribution.md#numPartialLogL)
* [<strong>updateLogL(</strong> problem, allpars, parval=None )](./ErrorDistribution.md#updateLogL)
* [<strong>hyparname(</strong> k ) ](./ErrorDistribution.md#hyparname)
