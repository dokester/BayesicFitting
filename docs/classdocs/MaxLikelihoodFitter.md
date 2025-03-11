---
---
<br><br>

<a name="MaxLikelihoodFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class MaxLikelihoodFitter(</strong> <a href="./IterativeFitter.html">IterativeFitter</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/MaxLikelihoodFitter.py target=_blank>Source</a></th></tr></thead></table>
<p>

Base class with methods common to fitters handling ErrorDistributions.

Author:      Do Kester.

<b>Attributes</b><br>
* errdis  :  None | "gauss" | "laplace" | "cauchy" | "poisson" |<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "uniform" | "exponential"<br>
&nbsp;&nbsp;&nbsp;&nbsp; None : Use _ChiSq as function to be minimized<br>
&nbsp;&nbsp;&nbsp;&nbsp; name : use -logLikelihood as function to be minimized from the named<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; errordistribution.<br>
* scale  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; the (fixed) noise scale<br>
* power  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; power of errdis (if applicable)<br>

<b>Raises</b><br>
ConvergenceError    Something went wrong during the convergence if the fit.


<a name="MaxLikelihoodFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>MaxLikelihoodFitter(</strong> xdata, model, errdis=None, scale=None, power=2.0,
 **kwargs )
</th></tr></thead></table>
<p>

Create a new iterative fitter, providing xdatas and model.

This is a base class. It collects stuff common to all iterative fitters.
It does not work by itself.

<b>Parameters</b><br>
* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; array of independent input values<br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model function to be fitted<br>

* errdis  :  None | "gauss" | "laplace" | "cauchy" | "poisson" |<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "uniform" | "exponential"<br>
&nbsp;&nbsp;&nbsp;&nbsp; None : Use _ChiSq as function to be minimized<br>
&nbsp;&nbsp;&nbsp;&nbsp; name : use -logLikelihood as function to be minimized from the named<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; errordistribution.<br>
* scale  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; the (fixed) noise scale of errdis (if applicable)<br>
* power  :  float (2.0)<br>
&nbsp;&nbsp;&nbsp;&nbsp; the power of errdis ( if applicable)<br>
* kwargs  :  dict<br>
&nbsp;&nbsp;&nbsp;&nbsp; Possibly includes keywords from<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; IterativeFitter :       maxIter, tolerance, verbose<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; BaseFitter :            map, keep, fixedScale<br>


<a name="makeFuncs"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makeFuncs(</strong> data, weights=None, index=None, ret=3 ) 
</th></tr></thead></table>
<p>

Make connection to the desired func, gradient and hessian.

<b>Parameters</b><br>
* data  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; the data to be fitted<br>
* weights  :  array_like or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights on the data<br>
* index  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; indices of the parameters to be fitted.<br>
* ret  :  1 or 2 or 3<br>
    return (func), (func,dfunc) or (func,dfunc,hess)

<a name="getScale"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getScale(</strong> ) 
</th></tr></thead></table>
<p>

Return the stdev of the noise.

<a name="getLogLikelihood"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLogLikelihood(</strong> autoscale=False, var=1.0 ) 
</th></tr></thead></table>
<p>
<a name="normalize"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>normalize(</strong> normdfdp, normdata, weight=1.0 ) 
</th></tr></thead></table>
<p>

Not Implemented.

<b>Raises</b><br>
NotImplementedError.
the method is not implemented for MaxLikelihoodFitters


<a name="testGradient"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>testGradient(</strong> par, at, data, weights=None )
</th></tr></thead></table>
<p>

returns true if the test fails.


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./IterativeFitter.html">IterativeFitter</a></th></tr></thead></table>


* [<strong>setParameters(</strong> params )](./IterativeFitter.md#setParameters)
* [<strong>doPlot(</strong> param, force=False )](./IterativeFitter.md#doPlot)
* [<strong>fitprolog(</strong> ydata, weights=None, accuracy=None, keep=None ) ](./IterativeFitter.md#fitprolog)
* [<strong>fit(</strong> ydata, weights=None, keep=None, **kwargs )](./IterativeFitter.md#fit)
* [<strong>report(</strong> verbose, param, chi, more=None, force=False ) ](./IterativeFitter.md#report)


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./BaseFitter.html">BaseFitter</a></th></tr></thead></table>


* [<strong>setMinimumScale(</strong> scale=0 ) ](./BaseFitter.md#setMinimumScale)
* [<strong>fitpostscript(</strong> ydata, plot=False ) ](./BaseFitter.md#fitpostscript)
* [<strong>keepFixed(</strong> keep=None ) ](./BaseFitter.md#keepFixed)
* [<strong>insertParameters(</strong> fitpar, index=None, into=None ) ](./BaseFitter.md#insertParameters)
* [<strong>modelFit(</strong> ydata, weights=None, keep=None )](./BaseFitter.md#modelFit)
* [<strong>limitsFit(</strong> ydata, weights=None, keep=None ) ](./BaseFitter.md#limitsFit)
* [<strong>checkNan(</strong> ydata, weights=None, accuracy=None )](./BaseFitter.md#checkNan)
* [<strong>getVector(</strong> ydata, index=None )](./BaseFitter.md#getVector)
* [<strong>getHessian(</strong> params=None, weights=None, index=None )](./BaseFitter.md#getHessian)
* [<strong>getInverseHessian(</strong> params=None, weights=None, index=None )](./BaseFitter.md#getInverseHessian)
* [<strong>getCovarianceMatrix(</strong> )](./BaseFitter.md#getCovarianceMatrix)
* [<strong>makeVariance(</strong> scale=None )](./BaseFitter.md#makeVariance)
* [<strong>getDesign(</strong> params=None, xdata=None, index=None )](./BaseFitter.md#getDesign)
* [<strong>chiSquared(</strong> ydata, params=None, weights=None )](./BaseFitter.md#chiSquared)
* [<strong>getStandardDeviations(</strong> )](./BaseFitter.md#getStandardDeviations)
* [<strong>monteCarloError(</strong> xdata=None, monteCarlo=None)](./BaseFitter.md#monteCarloError)
* [<strong>getEvidence(</strong> limits=None, noiseLimits=None )](./BaseFitter.md#getEvidence)
* [<strong>getLogZ(</strong> limits=None, noiseLimits=None )](./BaseFitter.md#getLogZ)
* [<strong>plotResult(</strong> xdata=None, ydata=None, model=None, residuals=True,](./BaseFitter.md#plotResult)
