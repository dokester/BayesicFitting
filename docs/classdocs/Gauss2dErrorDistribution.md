---
---
<br><br>

<a name="Gauss2dErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Gauss2dErrorDistribution(</strong> <a href="./GaussErrorDistribution.html">GaussErrorDistribution</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Gauss2dErrorDistribution.py target=_blank>Source</a></th></tr></thead></table>
<p>

To calculate a Gauss likelihood in case of errors in X and Y

For one residual in x and y it holds

<br>&nbsp; L = 1 / ( 2 &pi; &radic; det ) exp( - 0.5 ( x / s )<sup>2</sup> )<br>

where s is the scale.
s is a hyperparameter, which might be estimated from the data.

The scale s is also the square root of the variance of this error distribution.

The function is mostly used to calculate the likelihood L over N residuals,
or easier to use log likelihood, logL.

<br>&nbsp; logL = log( N / ( &radic;( 2 &pi; ) s )  ) - 0.5 &sum;( x / s )<sup>2</sup><br>

Using weights this becomes

<br>&nbsp; logL = log( &sum;( w ) / ( &radic;( 2 &pi; ) s )  ) - 0.5 &sum;( w ( x / s )<sup>2</sup> )<br>


Author       Do Kester.


<a name="Gauss2dErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Gauss2dErrorDistribution(</strong> scale=1.0, limits=None, copy=None )
</th></tr></thead></table>
<p>

Default Constructor.

<b>Parameters</b><br>
* scale  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; noise scale<br>
* limits  :  None or list of 2 floats [low,high]<br>
&nbsp;&nbsp;&nbsp;&nbsp; None : no limits implying fixed scale<br>
&nbsp;&nbsp;&nbsp;&nbsp; low     low limit on scale (needs to be >0)<br>
&nbsp;&nbsp;&nbsp;&nbsp; high    high limit on scale<br>
&nbsp;&nbsp;&nbsp;&nbsp; when limits are set, the scale is *not* fixed.<br>

* copy  :  GaussErrorDistribution<br>
&nbsp;&nbsp;&nbsp;&nbsp; distribution to be copied.<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Return copy of this. 

<a name="TBDgetScale"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>TBDgetScale(</strong> problem, allpars=None ) 
</th></tr></thead></table>
<p>

Return the noise scale.

<b>Parameters</b><br>
* problem  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be solved<br>
* allpars  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; None take parameters from problem.model<br>
    list of all parameters in the problem

<a name="updateDeterminant"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>updateDeterminant(</strong> problem, scale ) 
</th></tr></thead></table>
<p>

Update the determinant of the covar matrix with scale

<b>Parameters</b><br>
* problem  :  ErrorsInXandYProblem<br>
&nbsp;&nbsp;&nbsp;&nbsp; problem at hand<br>
* scale  :  float<br>
    present vale for the cale

<a name="logLikelihood_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logLikelihood_alt(</strong> problem, allpars ) 
</th></tr></thead></table>
<p>

Return the log( likelihood ) for a Gaussian distribution.

Alternate calculation

<b>Parameters</b><br>
* problem  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be solved<br>
* allpars  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem<br>


<a name="logLdata"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logLdata(</strong> problem, allpars, mockdata=None ) 
</th></tr></thead></table>
<p>

Return the log( likelihood ) for each residual

logL = sum( logLdata )

<b>Parameters</b><br>
* problem  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be solved<br>
* allpars  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem<br>
* mockdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; as calculated by the model<br>


<a name="partialLogL_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialLogL_alt(</strong> problem, allpars, fitIndex ) 
</th></tr></thead></table>
<p>

Return the partial derivative of log( likelihood ) to the parameters in fitIndex.

Alternate calculation

<b>Parameters</b><br>
* problem  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be solved.<br>
* allpars  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; (hyper)parameters of the problem<br>
* fitIndex  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters to be fitted<br>


<a name="nextPartialData"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>nextPartialData(</strong> problem, allpars, fitIndex, mockdata=None ) 
</th></tr></thead></table>
<p>

Return the partial derivative all elements of the log( likelihood )
to the parameters in fitIndex.

<b>Parameters</b><br>
* problem  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be solved<br>
* allpars  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; (hyper)parameters of the problem<br>
* fitIndex  :  array_like of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; indices of allpars to fit<br>
* mockdata  :  array_like<br>
    as calculated for the problem

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./GaussErrorDistribution.html">GaussErrorDistribution</a></th></tr></thead></table>


* [<strong>acceptWeight(</strong> )](./GaussErrorDistribution.md#acceptWeight)
* [<strong>getScale(</strong> problem, allpars=None ) ](./GaussErrorDistribution.md#getScale)
* [<strong>hessianLogL(</strong> problem, allpars, fitIndex ) ](./GaussErrorDistribution.md#hessianLogL)


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
* [<strong>setResult(</strong> )](./ErrorDistribution.md#setResult)
* [<strong>hyparname(</strong> k ) ](./ErrorDistribution.md#hyparname)
