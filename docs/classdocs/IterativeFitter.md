---
---
<br><br>

<a name="IterativeFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class IterativeFitter(</strong> <a href="./BaseFitter.html">BaseFitter</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/IterativeFitter.py target=_blank>[source]</a></th></tr></thead></table>
<p>

Base class with methods common to all iterative fitters.

Author:      Do Kester.

<b>Attributes</b>

* tolerance  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; When absolute and relative steps in subsequent chisq steps are less than
<br>&nbsp;&nbsp;&nbsp;&nbsp; tolerance, the fitter stops. Default = 0.0001
* maxIter  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; When the number of iterations gets larger than maxiter the fitter
<br>&nbsp;&nbsp;&nbsp;&nbsp; stops with a ConvergenceError Default = 1000 * nparams
* iter  :  int (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; iteration counter
* ntrans  :  int (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of transforms
* verbose  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; information per iteration.
<br>&nbsp;&nbsp;&nbsp;&nbsp; 0 : silent
<br>&nbsp;&nbsp;&nbsp;&nbsp; 1 : base information (default)
<br>&nbsp;&nbsp;&nbsp;&nbsp; 2 : report about every 100th iteration
<br>&nbsp;&nbsp;&nbsp;&nbsp; 3 : report about every ietration
* tooLarge  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; When the length parameter array is too large to make a Hessian.
<br>&nbsp;&nbsp;&nbsp;&nbsp; To avert OutOfMemory. Default = 100

* plotter  :  Plotter
<br>&nbsp;&nbsp;&nbsp;&nbsp; Iteration plotter class. Default = IterationPlotter
* plotIter  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; Produce a plot for every plotIter-th iteration.
<br>&nbsp;&nbsp;&nbsp;&nbsp; Default = 0 (no plotting)

<b>Raises</b>

ConvergenceError    Something went wrong during the convergence if the fit.


<a name="IterativeFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>IterativeFitter(</strong> xdata, model, maxIter=None, tolerance=0.0001, verbose=1, **kwargs ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/IterativeFitter.py#L75-L116 target=_blank>[source]</a></th></tr></thead></table>

Create a new iterative fitter, providing xdatas and model.

This is a base class. It collects stuff common to all iterative fitters.
It does not work by itself.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of independent input values
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model function to be fitted

* tolerance  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; When absolute and relative steps in subsequent chisq steps are less than
<br>&nbsp;&nbsp;&nbsp;&nbsp; tolerance, the fitter stops. Default = 0.01
* maxIter  :  None or int
<br>&nbsp;&nbsp;&nbsp;&nbsp; When the number of iterations gets larger than maxiter the fitter
<br>&nbsp;&nbsp;&nbsp;&nbsp; stops with a ConvergenceError Default = 1000 * nparams
* verbose  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; 0 : silent
<br>&nbsp;&nbsp;&nbsp;&nbsp; 1 : report result
<br>&nbsp;&nbsp;&nbsp;&nbsp; 2 : report every 100th iteration
<br>&nbsp;&nbsp;&nbsp;&nbsp; 3 : report every iteration
kwargs for [BaseFitter](./BaseFitter.md)
<br>&nbsp;&nbsp;&nbsp;&nbsp; map, keep, fixedScale


<a name="setParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setParameters(</strong> params )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/IterativeFitter.py#L118-L130 target=_blank>[source]</a></th></tr></thead></table>
Initialize the parameters of the model
A little superfluous: see [link](./link.md) Model#setParameters

<b>Parameters</b>

* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; initial parameters


<a name="setPlotters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setPlotters(</strong> plot ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/IterativeFitter.py#L132-L165 target=_blank>[source]</a></th></tr></thead></table>
Set plot methods as requested by plot.

| plot   | doIterPlot |   doLastPlot   |   comment            |
|--------|------------|----------------|----------------------|
| False  |  no plot   |   no plot      | default; dont plot   |
| True   |  no plot   | plotSampleList |                      |
| "last" |  no plot   | plotSampleList |                      |
| "iter" | plotWalker |   no plot      |                      |
| "all"  | plotWalker | plotSampleList |                      |
| "test" | plotWalker | plotSampleList | no show(), for tests |

The plot methods plotWalker and plotSampleList are part of the
module Plotter.py
<br>&nbsp;&nbsp;&nbsp;&nbsp; 
<b>Parameters</b>

* plot  :  str or bool (False)
<br>&nbsp;&nbsp;&nbsp;&nbsp; as in table

<a name="plotNot"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotNot(</strong> ydata, param, force=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/IterativeFitter.py#L167-L169 target=_blank>[source]</a></th></tr></thead></table>

do not plot 
<a name="plotIter"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotIter(</strong> ydata, param, force=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/IterativeFitter.py#L171-L177 target=_blank>[source]</a></th></tr></thead></table>

Plot Iteration results 
<a name="fitprolog"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fitprolog(</strong> ydata, weights=None, accuracy=None, keep=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/IterativeFitter.py#L179-L213 target=_blank>[source]</a></th></tr></thead></table>
Prolog for all iterative Fitters.

1. Sets up plotting (if requested)
2. Sets self.iter and self.ntrans to 0
3. Checks data/weighs for Nans
4. Makes fitIndex.

<b>Parameters</b>

* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted
* weights  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights pertaining to the data
* accuracy  :  float or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; accuracy of (individual) data
* keep  :  dict of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)

<b>Returns</b>

* fitIndex  :  ndarray of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; Indices of the parameters that need fitting


<a name="fit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fit(</strong> ydata, weights=None, keep=None, **kwargs )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/IterativeFitter.py#L215-L237 target=_blank>[source]</a></th></tr></thead></table>
Return model parameters fitted to the data.

It will calculate the hessian matrix and chisq.

<b>Parameters</b>

* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted
* weights  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights pertaining to the data
* keep  :  dict of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)
* kwargs  : 
<br>&nbsp;&nbsp;&nbsp;&nbsp; passed to the fitter

<b>Raises</b>

ConvergenceError if it stops when the tolerance has not yet been reached.


<a name="report"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>report(</strong> verbose, ydata, param, chi, more=None, force=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/IterativeFitter.py#L239-L254 target=_blank>[source]</a></th></tr></thead></table>
Report on intermediate results.

Endline #L256
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./BaseFitter.html">BaseFitter</a></th></tr></thead></table>


* [<strong>setMinimumScale(</strong> scale=0 ) ](./BaseFitter.md#setMinimumScale)
* [<strong>fitpostscript(</strong> ydata, plot=False ) ](./BaseFitter.md#fitpostscript)
* [<strong>keepFixed(</strong> keep=None ) ](./BaseFitter.md#keepFixed)
* [<strong>insertParameters(</strong> fitpar, index=None, into=None ) ](./BaseFitter.md#insertParameters)
* [<strong>modelFit(</strong> ydata, weights=None, keep=None, **kwargs )](./BaseFitter.md#modelFit)
* [<strong>limitsFit(</strong> ydata, weights=None, keep=None, **kwargs ) ](./BaseFitter.md#limitsFit)
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
* [<strong>monteCarloError(</strong> xdata=None, monteCarlo=None, scale=1.0 )](./BaseFitter.md#monteCarloError)
* [<strong>getScale(</strong> )](./BaseFitter.md#getScale)
* [<strong>getEvidence(</strong> limits=None, noiseLimits=None )](./BaseFitter.md#getEvidence)
* [<strong>getLogLikelihood(</strong> autoscale=False, var=1.0 ) ](./BaseFitter.md#getLogLikelihood)
* [<strong>getLogZ(</strong> limits=None, noiseLimits=None )](./BaseFitter.md#getLogZ)
* [<strong>plotResult(</strong> xdata=None, ydata=None, model=None, residuals=True,](./BaseFitter.md#plotResult)
