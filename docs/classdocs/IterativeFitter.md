---
---
<br><br><br>

<a name="IterativeFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class IterativeFitter(</strong> <a href="./BaseFitter.html">BaseFitter</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/IterativeFitter.py target=_blank>Source</a></th></tr></thead></table>
<p>

Base class with methods common to all iterative fitters.

Author:      Do Kester.

<b>Attributes</b>

* tolerance  :  float<br>
    When absolute and relative steps in subsequent chisq steps are less than<br>
    tolerance, the fitter stops. Default = 0.0001<br>
* maxIter  :  int<br>
    When the number of iterations gets larger than maxiter the fitter<br>
    stops with a ConvergenceError Default = 1000 * nparams<br>
* iter  :  int (read only)<br>
    iteration counter<br>
* ntrans  :  int (read only)<br>
    number of transforms<br>
* verbose  :  int<br>
    information per iteration.<br>
    0 : silent<br>
    1 : base information (default)<br>
    2 : report about every 100th iteration<br>
    3 : report about every ietration<br>
* tooLarge  :  int<br>
    When the length parameter array is too large to make a Hessian.<br>
    To avert OutOfMemory. Default = 100<br>

* plotter  :  Plotter<br>
    Iteration plotter class. Default = IterationPlotter<br>
* plotIter  :  int<br>
    Produce a plot for every plotIter-th iteration.<br>
    Default = 0 (no plotting)<br>

<b>Raises</b>

ConvergenceError    Something went wrong during the convergence if the fit.


<a name="IterativeFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>IterativeFitter(</strong> xdata, model, maxIter=None, tolerance=0.0001, verbose=1, **kwargs ) 
</th></tr></thead></table>
<p>

Create a new iterative fitter, providing xdatas and model.

This is a base class. It collects stuff common to all iterative fitters.
It does not work by itself.

<b>Parameters</b>

* xdata  :  array_like<br>
    array of independent input values<br>
* model  :  Model<br>
    the model function to be fitted<br>

* tolerance  :  float<br>
    When absolute and relative steps in subsequent chisq steps are less than<br>
    tolerance, the fitter stops. Default = 0.01<br>
* maxIter  :  None or int<br>
    When the number of iterations gets larger than maxiter the fitter<br>
    stops with a ConvergenceError Default = 1000 * nparams<br>
* verbose  :  int<br>
    0 : silent<br>
    1 : report result<br>
    2 : report every 100th iteration<br>
    3 : report every iteration<br>
kwargs for [BaseFitter](./BaseFitter.md)
    map, keep, fixedScale<br>


<a name="setParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setParameters(</strong> params )
</th></tr></thead></table>
<p>

Initialize the parameters of the model
A little superfluous: see {[link](./link.md) Model#setParameters}

<b>Parameters</b>

* params  :  array_like<br>
    initial parameters<br>


<a name="doPlot"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>doPlot(</strong> param, force=False )
</th></tr></thead></table>
<p>

Plot intermediate result.

<b>Parameters</b>

* param  :  array_like<br>
    of the model<br>
* force  :  bool<br>
    do the plot<br>


<a name="fitprolog"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fitprolog(</strong> ydata, weights=None, accuracy=None, keep=None ) 
</th></tr></thead></table>
<p>

Prolog for all iterative Fitters.

1. Sets up plotting (if requested)
2. Sets self.iter and self.ntrans to 0
3. Checks data/weighs for Nans
4. Makes fitIndex.

<b>Parameters</b>

* ydata  :  array_like<br>
    the data vector to be fitted<br>
* weights  :  array_like<br>
    weights pertaining to the data<br>
* accuracy  :  float or array_like<br>
    accuracy of (individual) data<br>
* keep  :  dict of {int:float}<br>
    dictionary of indices (int) to be kept at a fixed value (float)<br>

<b>Returns</b>

* fitIndex  :  ndarray of int<br>
    Indices of the parameters that need fitting<br>


<a name="fit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fit(</strong> ydata, weights=None, keep=None, **kwargs )
</th></tr></thead></table>
<p>

Return model parameters fitted to the data.

It will calculate the hessian matrix and chisq.

<b>Parameters</b>

* ydata  :  array_like<br>
    the data vector to be fitted<br>
* weights  :  array_like<br>
    weights pertaining to the data<br>
* keep  :  dict of {int:float}<br>
    dictionary of indices (int) to be kept at a fixed value (float)<br>
* kwargs  : <br>
    passed to the fitter<br>

<b>Raises</b>

ConvergenceError if it stops when the tolerance has not yet been reached.


<a name="report"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>report(</strong> verbose, param, chi, more=None, force=False ) 
</th></tr></thead></table>
<p>

Report on intermediate results.

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
* [<strong>normalize(</strong> normdfdp, normdata, weight=1.0 ) ](./BaseFitter.md#normalize)
* [<strong>getDesign(</strong> params=None, xdata=None, index=None )](./BaseFitter.md#getDesign)
* [<strong>chiSquared(</strong> ydata, params=None, weights=None )](./BaseFitter.md#chiSquared)
* [<strong>getStandardDeviations(</strong> )](./BaseFitter.md#getStandardDeviations)
* [<strong>monteCarloError(</strong> xdata=None, monteCarlo=None)](./BaseFitter.md#monteCarloError)
* [<strong>getScale(</strong> )](./BaseFitter.md#getScale)
* [<strong>getEvidence(</strong> limits=None, noiseLimits=None )](./BaseFitter.md#getEvidence)
* [<strong>getLogLikelihood(</strong> autoscale=False, var=1.0 ) ](./BaseFitter.md#getLogLikelihood)
* [<strong>getLogZ(</strong> limits=None, noiseLimits=None )](./BaseFitter.md#getLogZ)
* [<strong>plotResult(</strong> xdata=None, ydata=None, model=None, residuals=True,](./BaseFitter.md#plotResult)
