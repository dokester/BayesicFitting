---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/GaussErrorDistribution.py target=_blank>Source</a></span></div>

<a name="GaussErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class GaussErrorDistribution(</strong> <a href="./ScaledErrorDistribution.html">ScaledErrorDistribution</a> )
</th></tr></thead></table>
<p>

To calculate a Gauss likelihood.

For one residual, x, it holds

    L( x ) = 1 / &sqrt;( 2 &pi; s^2 ) exp( - 0.5 ( x / s )^2 )<br>

$$
L(x) = \frac{ 1 }{ s \sqrt( 2 \pi ) } \exp\left( -0.5 (\frac{x}{s})^2 \right)
$$


where s is the scale.
s is a hyperparameter, which might be estimated from the data.

The scale s is also the square root of the variance of this error distribution.

The function is mostly used to calculate the likelihood L over N residuals,
or easier to use log likelihood, logL.

    logL = log( N / ( sqrt( 2 &pi; ) s )  ) - 0.5 &sum;( x / s ) ^ 2<br>

$$
\log L = \log( \frac{ N } { s \sqrt( 2 \pi ) } ) - 
          0.5 \sum \left( \frac{ x } { s } \right)^2<br>
$$

Using weights this becomes

    logL = log( &sum;( w ) / ( sqrt( 2 &pi; ) s )  ) - 0.5 &sum;( w ( x / s ) ^ 2 )<br>


Author       Do Kester.


<a name="GaussErrorDistribution"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>GaussErrorDistribution(</strong> scale=1.0, limits=None, copy=None )
</th></tr></thead></table>
<p>

Default Constructor.

<b>Parameters</b>

* scale  :  float<br>
    noise scale<br>
* limits  :  None or list of 2 floats [low,high]<br>
    None : no limits implying fixed scale<br>
    low     low limit on scale (needs to be >0)<br>
    high    high limit on scale<br>
    when limits are set, the scale is *not* fixed.<br>

* copy  :  GaussErrorDistribution<br>
    distribution to be copied.<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Return copy of this. 

<a name="acceptWeight"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>acceptWeight(</strong> )
</th></tr></thead></table>
<p>

True if the distribution accepts weights.
Always true for this distribution.

<a name="getScale"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>getScale(</strong> problem, allpars=None ) 
</th></tr></thead></table>
<p>

Return the noise scale.

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    None take parameters from problem.model<br>
    list of all parameters in the problem

<a name="logLikelihood_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>logLikelihood_alt(</strong> problem, allpars ) 
</th></tr></thead></table>
<p>

Return the log( likelihood ) for a Gaussian distribution.

Alternate calculation

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    list of all parameters in the problem<br>


<a name="logLdata"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>logLdata(</strong> problem, allpars, mockdata=None ) 
</th></tr></thead></table>
<p>

Return the log( likelihood ) for each residual

logL = sum( logLdata )

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    list of all parameters in the problem<br>
* mockdata  :  array_like<br>
    as calculated by the model<br>


<a name="partialLogL_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>partialLogL_alt(</strong> problem, allpars, fitIndex ) 
</th></tr></thead></table>
<p>

Return the partial derivative of log( likelihood ) to the parameters in fitIndex.

Alternate calculation

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved.<br>
* allpars  :  array_like<br>
    (hyper)parameters of the problem<br>
* fitIndex  :  array_like<br>
    indices of parameters to be fitted<br>


<a name="nextPartialData"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>nextPartialData(</strong> problem, allpars, fitIndex, mockdata=None ) 
</th></tr></thead></table>
<p>

Return the partial derivative all elements of the log( likelihood )
to the parameters in fitIndex.

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    (hyper)parameters of the problem<br>
* fitIndex  :  array_like of int<br>
    indices of allpars to fit<br>
* mockdata  :  array_like<br>
    as calculated for the problem

<a name="hessianLogL"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>hessianLogL(</strong> problem, allpars, fitIndex ) 
</th></tr></thead></table>
<p>

Return the hessian of log( likelihood ) to the parameters in fitIndex.

The hessian is a matrix containing the second derivatives to each
of the parameters.

     hessian = d^2 logL / dp_i dp_k<br>

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    (hyper)parameters of the problem<br>
* fitIndex  :  array_like of int<br>
    indices of allpars to fit

<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./ScaledErrorDistribution.html">ScaledErrorDistribution</a></th></tr></thead></table>


* [<strong>setLimits(</strong> limits ) ](./ScaledErrorDistribution.md#setLimits)


<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
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
