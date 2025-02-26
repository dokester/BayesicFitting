---
---
<br><br><br>

<a name="BernoulliErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class BernoulliErrorDistribution(</strong> <a href="./ErrorDistribution.html">ErrorDistribution</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BernoulliErrorDistribution.py target=_blank>Source</a></th></tr></thead></table>
<p>

To calculate a Bernoulli likelihood for categorical True/False data.

For one residual, x, it holds

 f( x ) = x          if d is True<br>
          1 - x      if d is False<br>

where x needs to be between [0,1]; use the logistic function f(x) = 1/(1+exp(-x)
if necessary. And d is true if the residual belongs to the intended category.

The function is mostly used to calculate the likelihood L, or easier
to use log likelihood, logL.

 logL = log( x ) if d else log( 1 - x )<br>

Author       Do Kester.


<a name="BernoulliErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>BernoulliErrorDistribution(</strong> copy=None ) 
</th></tr></thead></table>
<p>

Constructor of Bernoulli Distribution.

<b>Parameters</b>

* copy  :  BernoulliErrorDistribution<br>
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

<a name="getScale"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getScale(</strong> problem, allpars=None ) 
</th></tr></thead></table>
<p>

Return the noise scale

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    None take parameters from problem.model<br>
    list of all parameters in the problem

<a name="toSigma"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>toSigma(</strong> scale ) 
</th></tr></thead></table>
<p>

Return sigma, the squareroot of the variance.

<b>Parameter</b>

* scale  :  float<br>
    the scale of this Bernoulli distribution.

<a name="logLikelihood_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logLikelihood_alt(</strong> problem, allpars ) 
</th></tr></thead></table>
<p>

Return the log( likelihood ) for a Bernoulli distribution.

Alternate calculation.

Outside the range the likelihood is zero, so the logL should be -inf.
However for computational reasons the maximum negative value is returned.

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


<a name="partialLogL_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialLogL_alt(</strong> problem, allpars, fitIndex ) 
</th></tr></thead></table>
<p>

Return the partial derivative of log( likelihood ) to the parameters.

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

Return the partial derivative of elements of the log( likelihood )
to the parameters.

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
<strong>Methods inherited from</strong> <a href="./ErrorDistribution.html">ErrorDistribution</a></th></tr></thead></table>


* [<strong>getGaussianScale(</strong> problem, allpars=None ) ](./ErrorDistribution.md#getGaussianScale)
* [<strong>getResiduals(</strong> problem, allpars=None )](./ErrorDistribution.md#getResiduals)
* [<strong>getChisq(</strong> problem, allpars=None )](./ErrorDistribution.md#getChisq)
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
* [<strong>setResult(</strong> )](./ErrorDistribution.md#setResult)
* [<strong>hyparname(</strong> k ) ](./ErrorDistribution.md#hyparname)
