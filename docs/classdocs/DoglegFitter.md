---
---
<br><br>

<a name="DoglegFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class DoglegFitter(</strong> <a href="./ScipyFitter.html">ScipyFitter</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ScipyFitter.py target=_blank>Source</a></th></tr></thead></table>

Dog-leg trust-region algorithm.

Syntactic sugar for
<br>&nbsp;&nbsp;&nbsp;&nbsp; ScipyFitter( ..., method='DOGLEG', ... )

See [ScipyFitter](./ScipyFitter.md)


<a name="DoglegFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>DoglegFitter(</strong> xdata, model, gradient=True, **kwargs ) 
</th></tr></thead></table>

Constructor.
Create a class, providing inputs and model.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of independent input values
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; a model function to be fitted (linear or nonlinear)
* gradient  :  bool or None or callable gradient( par )
<br>&nbsp;&nbsp;&nbsp;&nbsp; if True use gradient calculated from model. It is the default.
<br>&nbsp;&nbsp;&nbsp;&nbsp; if False/None dont use gradient (use numeric approximation in stead)
<br>&nbsp;&nbsp;&nbsp;&nbsp; if callable use the method as gradient
* kwargs  :  dict
<br>&nbsp;&nbsp;&nbsp;&nbsp; Possibly includes keywords from
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ScipyFitter:            gradient, hessp
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; MaxLikelihoodFitter :   errdis, scale, power
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; IterativeFitter :       maxIter, tolerance, verbose
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; BaseFitter :            map, keep, fixedScale


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./ScipyFitter.html">ScipyFitter</a></th></tr></thead></table>


* [<strong>fit(</strong> data, weights=None, par0=None, keep=None, limits=None,](./ScipyFitter.md#fit)
* [<strong>collectVectors(</strong> par ) ](./ScipyFitter.md#collectVectors)


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./MaxLikelihoodFitter.html">MaxLikelihoodFitter</a></th></tr></thead></table>


* [<strong>makeFuncs(</strong> data, weights=None, index=None, ret=3 ) ](./MaxLikelihoodFitter.md#makeFuncs)
* [<strong>getScale(</strong> ) ](./MaxLikelihoodFitter.md#getScale)
* [<strong>getLogLikelihood(</strong> autoscale=False, var=1.0 ) ](./MaxLikelihoodFitter.md#getLogLikelihood)
* [<strong>normalize(</strong> normdfdp, normdata, weight=1.0 ) ](./MaxLikelihoodFitter.md#normalize)
* [<strong>testGradient(</strong> par, at, data, weights=None )](./MaxLikelihoodFitter.md#testGradient)


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./IterativeFitter.html">IterativeFitter</a></th></tr></thead></table>


* [<strong>setParameters(</strong> params )](./IterativeFitter.md#setParameters)
* [<strong>doPlot(</strong> param, force=False )](./IterativeFitter.md#doPlot)
* [<strong>fitprolog(</strong> ydata, weights=None, accuracy=None, keep=None ) ](./IterativeFitter.md#fitprolog)
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
