---
---
<br><br>

<a name="PoissonErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class PoissonErrorDistribution(</strong> <a href="./ErrorDistribution.html">ErrorDistribution</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PoissonErrorDistribution.py target=_blank>[source]</a></th></tr></thead></table>
<p>

To calculate a Poisson likelihood.

For one observation with n counts it holds

&nbsp; f( n,x ) = x<sup>n</sup> / ( e<sup>x</sup> * n! )

where x is the expected counts

The function is mostly used to calculate the likelihood L, or easier
to use log likelihood, logL.

&nbsp;&nbsp;&nbsp;&nbsp; logL = &sum;( n * log( x ) - x - log( n! ) )

Weights are not accepted in this ErrorDistribution; they are silently ignored.


Author       Do Kester.


<a name="PoissonErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>PoissonErrorDistribution(</strong> copy=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PoissonErrorDistribution.py#L62-L72 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

<b>Parameters</b><br>
* copy  :  PoissonErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; distribution to be copied.


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PoissonErrorDistribution.py#L74-L76 target=_blank>[source]</a></th></tr></thead></table>

Return copy of this. 
<a name="acceptWeight"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>acceptWeight(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PoissonErrorDistribution.py#L78-L84 target=_blank>[source]</a></th></tr></thead></table>
True if the distribution accepts weights.
Always false for this distribution.

<a name="getScale"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getScale(</strong> problem, allpars=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PoissonErrorDistribution.py#L86-L101 target=_blank>[source]</a></th></tr></thead></table>
Return the noise scale.

*** Gaussian approximation ***

<b>Parameters</b><br>
* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; None take parameters from problem.model
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem

<a name="logLikelihood_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logLikelihood_alt(</strong> problem, allpars )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PoissonErrorDistribution.py#L103-L128 target=_blank>[source]</a></th></tr></thead></table>
Return the log( likelihood ) for a Poisson distribution.

<b>Parameters</b><br>
* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem


<a name="logLdata"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logLdata(</strong> problem, allpars, mockdata=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PoissonErrorDistribution.py#L130-L161 target=_blank>[source]</a></th></tr></thead></table>
Return the log( likelihood ) for each residual

logL = sum( logLdata )

<b>Parameters</b><br>
* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem
* mockdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; as calculated by the model


<a name="partialLogL_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialLogL_alt(</strong> problem, allpars, fitIndex )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PoissonErrorDistribution.py#L163-L186 target=_blank>[source]</a></th></tr></thead></table>
Return the partial derivative of log( likelihood ) to the parameters.

<b>Parameters</b><br>
* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem
* fitIndex  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters to be fitted

<a name="nextPartialData"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>nextPartialData(</strong> problem, allpars, fitIndex, mockdata=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PoissonErrorDistribution.py#L188-L215 target=_blank>[source]</a></th></tr></thead></table>
Return the partial derivative of log( likelihood ) to the parameters.

<b>Parameters</b><br>
* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem
* fitIndex  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters to be fitted
* mockdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; as calculated by the model

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
* [<strong>partialLogL(</strong> problem, allpars, fitIndex ) ](./ErrorDistribution.md#partialLogL)
* [<strong>numPartialLogL(</strong> problem, allpars, fitIndex ) ](./ErrorDistribution.md#numPartialLogL)
* [<strong>updateLogL(</strong> problem, allpars, parval=None )](./ErrorDistribution.md#updateLogL)
* [<strong>hyparname(</strong> k ) ](./ErrorDistribution.md#hyparname)
