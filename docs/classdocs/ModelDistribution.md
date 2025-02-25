---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ModelDistribution.py target=_blank>Source</a></span></div>

<a name="ModelDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class ModelDistribution(</strong> <a href="./ScaledErrorDistribution.html">ScaledErrorDistribution</a> )
</th></tr></thead></table>
<p>

To calculate the probability of a model M from a set of models S,
given some data D, use Bayes rule

    P( M|DS ) = P( M|S ) * P( D|MS ) / P( D|S )<br>
    posterior = prior   * likelihood / evidence<br>

This class calculates the likelihood P( D|MS ).
On another level where we calculate the probability of the
parameters p, we see this likelhood appear as evidence P( D|M ).

Again using Bayes 

    P( p|DM ) = P( p|M ) * P( D|pM ) / P( D|M )<br>

The evidence here is calculated as the integral over a Gausian
approximation of the posterior.

Author       Do Kester.


<a name="ModelDistribution"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>ModelDistribution(</strong> arbiter=None, scale=1.0, limits=None,
 copy=None, **kwargs )
</th></tr></thead></table>
<p>

Default Constructor.

<b>Parameters</b>

* arbiter  :  None or BaseFitter or str<br>
    to provide the evidence<br>
    None    select fitter automatically<br>
    BaseFiter   Use this fitter<br>
    str     "fitter", "levenberg", "curve", "amoeba", "NestedSampler"<br>

* scale  :  float<br>
    noise scale<br>
* limits  :  None or list of 2 floats [low,high]<br>
    None : no limits implying fixed scale<br>
    low     low limit on scale (needs to be >0)<br>
    high    high limit on scale<br>
    when limits are set, the scale is *not* fixed.<br>

* copy  :  ModelDistribution<br>
    distribution to be copied.<br>

* kwargs  :  dict<br>
    to be applied to arbiter<br>


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
    Return optimal parameters of the fit<br>


<a name="logLdata"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>logLdata(</strong> problem, allpars, mockdata=None ) 
</th></tr></thead></table>
<p>

Return the log( likelihood ) for each residual
   <br>
logL = sum( logLdata )

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    list of all parameters in the problem   <br>
* mockdata  :  array_like<br>
    as calculated by the model<br>


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
* [<strong>partialLogL_alt(</strong> problem, allpars, fitIndex ) ](./ErrorDistribution.md#partialLogL_alt)
* [<strong>numPartialLogL(</strong> problem, allpars, fitIndex ) ](./ErrorDistribution.md#numPartialLogL)
* [<strong>updateLogL(</strong> problem, allpars, parval=None )](./ErrorDistribution.md#updateLogL)
* [<strong>setResult(</strong> )](./ErrorDistribution.md#setResult)
* [<strong>hyparname(</strong> k ) ](./ErrorDistribution.md#hyparname)
