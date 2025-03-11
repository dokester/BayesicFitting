---
---
<br><br>

<a name="MixedErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class MixedErrorDistribution(</strong> <a href="./ErrorDistribution.html">ErrorDistribution</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/MixedErrorDistribution.py target=_blank>Source</a></th></tr></thead></table>
<p>

To calculate a mixture of two likelihoods.

For one residual, x, it holds

<br>&nbsp;&nbsp;&nbsp;&nbsp; L( x ) = f * L1( x ) + ( 1 - f ) * L2( x )<br>

where f is the contributing fraction while L, L1 and L2 are likelihoods
f is a hyperparameter between [0..1]

The likelihood over N datapoints is

<br>&nbsp;&nbsp;&nbsp;&nbsp; L = &Pi; L( x )  = &Pi;( f * L1( x ) + ( 1 - f ) * L2( x ) )<br>

And the log of L is

<br>&nbsp;&nbsp;&nbsp;&nbsp; logL = &sum; logL( x ) = &sum;( log( f * L1(x) + ( 1 - f ) * L2(x) ) )<br>

<b>Note</b><br>
The mixture, i.e. the weighted sum of 2 distributions for each residual, is
the raison-d'etre for the methods logLdata and nextPartialData, so individual
contributions can be weighted, added, log-ged and summed.

Author       Do Kester.


<a name="MixedErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>MixedErrorDistribution(</strong> errdis1, errdis2, fraction=0.5, limits=None, copy=None )
</th></tr></thead></table>
<p>

Constructor.

Make a new error distribution as a fraction of errdis1 plus the rest of errdis2.

<b>Parameters</b><br>
* errdis1  :  ErrorDistribution<br>
&nbsp;&nbsp;&nbsp;&nbsp; First error distribution<br>
* errdis2  :  ErrorDistribution<br>
&nbsp;&nbsp;&nbsp;&nbsp; Second error distribution (might be of the same class as errdis1)<br>
&nbsp;&nbsp;&nbsp;&nbsp; It *must* have the same xdata, data, weights as errdis1.<br>
* fraction  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; contributing fraction<br>
* limits  :  None or list of 2 floats [low,high]<br>
&nbsp;&nbsp;&nbsp;&nbsp; None : no limits implying fixed fraction<br>
&nbsp;&nbsp;&nbsp;&nbsp; low     low limit on fraction ( >0)<br>
&nbsp;&nbsp;&nbsp;&nbsp; high    high limit on fraction ( <1)<br>
&nbsp;&nbsp;&nbsp;&nbsp; when limits are set, the scale is *not* fixed.<br>

* copy  :  MixedErrorDistribution<br>
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

<a name="logLdata"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logLdata(</strong> problem, allpars, mockdata=None ) 
</th></tr></thead></table>
<p>

Return the log( likelihood ) for a Mixedian distribution.

<b>Parameters</b><br>
* problem  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be solved<br>
* allpars  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem<br>
* mockdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; as calculated for the problem<br>


<a name="nextPartialData"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>nextPartialData(</strong> problem, allpars, fitIndex, mockdata=None ) 
</th></tr></thead></table>
<p>

Return the partial derivative of log( likelihood ) to the parameters in fitIndex.

<b>Parameters</b><br>
* problem  :  Problem<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be solved<br>
* allpars  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters of the problem<br>
* fitIndex  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters to be fitted<br>
* mockdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; as calculated for the problem<br>


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
* [<strong>partialLogL_alt(</strong> problem, allpars, fitIndex ) ](./ErrorDistribution.md#partialLogL_alt)
* [<strong>numPartialLogL(</strong> problem, allpars, fitIndex ) ](./ErrorDistribution.md#numPartialLogL)
* [<strong>updateLogL(</strong> problem, allpars, parval=None )](./ErrorDistribution.md#updateLogL)
* [<strong>setResult(</strong> )](./ErrorDistribution.md#setResult)
* [<strong>hyparname(</strong> k ) ](./ErrorDistribution.md#hyparname)
