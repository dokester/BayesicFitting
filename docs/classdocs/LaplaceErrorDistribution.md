---
---
<br><br>

<a name="LaplaceErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class LaplaceErrorDistribution(</strong> <a href="./ScaledErrorDistribution.html">ScaledErrorDistribution</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/LaplaceErrorDistribution.py target=_blank>Source</a></th></tr></thead></table>

To calculate a Laplace likelihood.

For one residual, x, it holds

&nbsp; f( x ) = 1 / ( 2 s ) exp( - |x| / s )

where s is the scale.
s is a hyperparameter, which might be estimated from the data.

The variance of this function is &sigma;<sup>2</sup> = 2 s<sup>2</sup>.
See: toSigma()

The function is mostly used to calculate the likelihood L over N
residuals, or easier using log likelihood, logL.

&nbsp;&nbsp;&nbsp;&nbsp; logL = log( N / ( 2 s ) ) - &sum;( |x| / s  )

Using weights this becomes

&nbsp;&nbsp;&nbsp;&nbsp; logL = log( &sum;( w ) / ( 2 s ) ) - &sum;( w |x| / s  )

Using this error distribution results in median-like solutions.

Author       Do Kester.


<a name="LaplaceErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>LaplaceErrorDistribution(</strong> scale=1.0, limits=None, copy=None ) 
</th></tr></thead></table>

Constructor of Laplace Distribution.

<b>Parameters</b>

* scale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; noise scale
* limits  :  None or list of 2 floats [low,high]
<br>&nbsp;&nbsp;&nbsp;&nbsp; None : no limits implying fixed scale
<br>&nbsp;&nbsp;&nbsp;&nbsp; low     low limit on scale (needs to be >0)
<br>&nbsp;&nbsp;&nbsp;&nbsp; high    high limit on scale
<br>&nbsp;&nbsp;&nbsp;&nbsp; when limits are set, the scale is *not* fixed.

* copy  :  LaplaceErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; distribution to be copied.

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>

Return copy of this. 
<a name="acceptWeight"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>acceptWeight(</strong> )
</th></tr></thead></table>
True if the distribution accepts weights.
Always true for this distribution.

<a name="toSigma"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>toSigma(</strong> scale ) 
</th></tr></thead></table>
Return sigma, the squareroot of the variance.
<b>Parameter</b>

* scale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the scale of this Laplace distribution.

<a name="getScale"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getScale(</strong> problem, allpars=None ) 
</th></tr></thead></table>
Return the noise scale

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; None take parameters from problem.model
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem

<a name="getSumRes"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getSumRes(</strong> problem, allpars=None, scale=1 )
</th></tr></thead></table>
Return the sum of the absolute values of the residuals.

&nbsp;&nbsp;&nbsp;&nbsp; sum ( | res | )

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; None take parameters from problem.model
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem
* scale  :  float or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; scale of residuals (from accuracies or noisescale of errdis)

<a name="logLikelihood_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logLikelihood_alt(</strong> problem, allpars ) 
</th></tr></thead></table>
Return the log( likelihood ) for a Gaussian distribution.

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters of the problem


<a name="logLdata"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logLdata(</strong> problem, allpars, mockdata=None ) 
</th></tr></thead></table>
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
</th></tr></thead></table>
Return the partial derivative of log( likelihood ) to the parameters.

dL/ds is not implemented for problems with accuracy

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem
* fitIndex  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters to be fitted


<a name="nextPartialData"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>nextPartialData(</strong> problem, allpars, fitIndex, mockdata=None ) 
</th></tr></thead></table>
Return the partial derivative of elements of the log( likelihood )
to the parameters.

dL/ds is not implemented for problems with accuracy

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem
* fitIndex  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters to be fitted
* mockdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; as calculated by the model


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./ScaledErrorDistribution.html">ScaledErrorDistribution</a></th></tr></thead></table>


* [<strong>setLimits(</strong> limits ) ](./ScaledErrorDistribution.md#setLimits)


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
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
