---
---
<br><br><br>

<a name="ExponentialErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class ExponentialErrorDistribution(</strong> <a href="./ScaledErrorDistribution.html">ScaledErrorDistribution</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ExponentialErrorDistribution.py target=_blank>Source</a></th></tr></thead></table>
<p>

Also known as generalized gaussian errordistribution.

To calculate an Exponential likelihood.

For one residual, x, it holds

    f( x ) = p / ( 2 s &Gamma;( 1 / p ) ) exp( - ( |x| / s ) ^ p )<br>

where s is the scale and p is the power.
s and p are hyperparameters, which might be estimated from the data.

The variance of this function is

    &sigma; ^ 2 = s ^ 2 &Gamma;( 3 / p ) / &Gamma;( 1 / p )<br>

See toSigma()

The function is mostly used to calculate the likelihood L over N residuals,
or easier to use log( L )

    logL = log( N p / ( 2 s &Gamma;( 1 / p ) ) ) - &sum;( ( |x| / s ) ^ p )<br>

Using weights this becomes

    logL = log( &sum;( w ) p / ( 2 s &Gamma;( 1 / p ) ) ) - &sum;( w ( |x| / s ) ^ p )<br>

<b>Note</b>

The scale s in Exponential is NOT the same as the scale in Gaussian or in Laplace.

<b>Attributes from ErrorDistibution</b>

hyperpar, deltaP, ncalls, nparts, sumweight, ndata, hypar, nphypar


Author       Do Kester.


<a name="ExponentialErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>ExponentialErrorDistribution(</strong> scale=1.0, power=2.0, limits=None, copy=None )
</th></tr></thead></table>
<p>

Default Constructor.

<b>Parameters</b>

* scale  :  float<br>
    noise scale<br>
* power  :  float<br>
    power of the distribution<br>
* limits  :  None or [low,high] or [[low],[high]]<br>
    None : no limits implying fixed scale<br>
    low     low limit on scale (needs to be >0)<br>
    high    high limit on scale<br>
    [low]   low limit on [scale,power] (need to be >0)<br>
    [high]  high limit on [scale,power]<br>
    when limits are set, the scale cq. power are *not* fixed.<br>
* copy  :  ExponentialErrorDistribution<br>
    distribution to be copied.

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Return copy of this. 

<a name="acceptWeight"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>acceptWeight(</strong> )
</th></tr></thead></table>
<p>

True if the distribution accepts weights.
Always true for this distribution.

<a name="toSigma"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>toSigma(</strong> hypar ) 
</th></tr></thead></table>
<p>

Return sigma, the squareroot of the variance.
<b>Parameter</b>

* hypar  :  array_like (2 floats)<br>
    the [scale,power] of this Exponential distribution.

<a name="logLikelihood_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logLikelihood_alt(</strong> problem, allpars ) 
</th></tr></thead></table>
<p>

Return the log( likelihood ) for a Gaussian distribution.

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    parameters of the problem<br>


<a name="logLdata"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
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


<a name="getChipow"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getChipow(</strong> problem, allpars=None, scale=1 ) 
</th></tr></thead></table>
<p>

Return chisq.

return Sum over the (weighted) powered residuals

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    None take parameters from problem.model<br>
    list of all parameters in the problem<br>
* scale  :  float or array_like<br>
    present scale

<a name="getScale"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getScale(</strong> problem, allpars=None ) 
</th></tr></thead></table>
<p>

Return the noise scale calculated from the residuals.

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    None take parameters from problem.model<br>
    list of all parameters in the problem

<a name="partialLogL_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialLogL_alt(</strong> problem, allpars, fitIndex ) 
</th></tr></thead></table>
<p>

Return the partial derivative of log( likelihood ) to the parameters.

dL/ds is not implemented for problems with accuracy

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    parameters of the problem<br>
* fitIndex  :  array_like<br>
    indices of parameters to be fitted<br>


<a name="nextPartialData"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>nextPartialData(</strong> problem, allpars, fitIndex, mockdata=None ) 
</th></tr></thead></table>
<p>

Return the partial derivative of all elements of the log( likelihood )
to the parameters.

dL/ds is not implemented for problems with accuracy

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    parameters of the problem<br>
* fitIndex  :  array_like<br>
    indices of parameters to be fitted<br>
* mockdata  :  array_like<br>
    as calculated by the model<br>


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./ScaledErrorDistribution.html">ScaledErrorDistribution</a></th></tr></thead></table>


* [<strong>setLimits(</strong> limits ) ](./ScaledErrorDistribution.md#setLimits)


<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./ErrorDistribution.html">ErrorDistribution</a></th></tr></thead></table>


* [<strong>getGaussianScale(</strong> problem, allpars=None ) ](./ErrorDistribution.md#getGaussianScale)
* [<strong>getResiduals(</strong> problem, allpars=None )](./ErrorDistribution.md#getResiduals)
* [<strong>getChisq(</strong> problem, allpars=None )](./ErrorDistribution.md#getChisq)
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
