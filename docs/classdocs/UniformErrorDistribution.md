---
---
<br><br>

<a name="UniformErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class UniformErrorDistribution(</strong> <a href="./ScaledErrorDistribution.html">ScaledErrorDistribution</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/UniformErrorDistribution.py target=_blank>Source</a></th></tr></thead></table>
<p>

To calculate a Uniform likelihood, eg. for digitization noise.

For one residual, x, it holds

<br>&nbsp;&nbsp;&nbsp;&nbsp; L( x ) = 1 / ( 2 * s )    if |x| < s<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0                otherwise<br>

where s is the scale.
s is a hyperparameter, which might be estimated from the data.

The variance of this function is &sigma;<sup>2</sup> = s / 6.
See: toSigma()

The function is mostly used to calculate the likelihood L over N residuals,
or easier using log likelihood, logL.

<br>&nbsp;&nbsp;&nbsp;&nbsp; logL = -log( 2 * s ) * N<br>

Note that it is required that <b>all</b> residuals are smaller than s,
otherwise the logL becomes -inf.

Using weights this becomes

<br>&nbsp;&nbsp;&nbsp;&nbsp; logL = -log( 2 * s ) * &sum; w<br>


Author       Do Kester.


<a name="UniformErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>UniformErrorDistribution(</strong> scale=1.0, limits=None, copy=None ) 
</th></tr></thead></table>
<p>

Constructor of Uniform Distribution.

<b>Parameters</b><br>
* scale  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; noise scale<br>
* limits  :  None or list of 2 floats [low,high]<br>
&nbsp;&nbsp;&nbsp;&nbsp; None    no limits implying fixed scale<br>
&nbsp;&nbsp;&nbsp;&nbsp; low     low limit on scale (needs to be >0)<br>
&nbsp;&nbsp;&nbsp;&nbsp; high    high limit on scale<br>
&nbsp;&nbsp;&nbsp;&nbsp; when limits are set, the scale is *not* fixed.<br>
* copy  :  UniformErrorDistribution<br>
&nbsp;&nbsp;&nbsp;&nbsp; distribution to be copied.<br>


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

<b>Parameters</b><br>
* problem  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be solved<br>
* allpars  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; None take parameters from problem.model<br>
    list of all parameters in the problem

<a name="toSigma"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>toSigma(</strong> scale ) 
</th></tr></thead></table>
<p>

Return sigma, the squareroot of the variance.
<b>Parameter</b><br>
* scale  :  float<br>
    the scale of this Uniform distribution.

<a name="logLikelihood_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logLikelihood_alt(</strong> problem, allpars ) 
</th></tr></thead></table>
<p>

Return the log( likelihood ) for a Uniform distribution.

Alternate calculation.

Outside the range the likelihood is zero, so the logL should be -inf.
However for computational reasons the maximum negative value is returned.

<b>Parameters</b><br>
* problem  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be solved<br>
* allpars  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters of the problem<br>


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

Return the partial derivative of log( likelihood ) to the parameters.

dL/ds is not implemented for problems with accuracy

<b>Parameters</b><br>
* problem  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be solved<br>
* allpars  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters of the problem<br>
* fitIndex  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters to be fitted<br>


<a name="nextPartialData"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>nextPartialData(</strong> problem, allpars, fitIndex, mockdata=None ) 
</th></tr></thead></table>
<p>

Return the partial derivative of elements of the log( likelihood )
to the parameters.

dL/ds is not implemented for problems with accuracy

<b>Parameters</b><br>
* problem  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be solved<br>
* allpars  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters of the problem<br>
* fitIndex  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters to be fitted<br>
* mockdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; as calculated by the model<br>


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
