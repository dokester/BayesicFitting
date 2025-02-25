---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/CurveFitter.py target=_blank>Source</a></span></div>

<a name="CurveFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class CurveFitter(</strong> <a href="./IterativeFitter.html">IterativeFitter</a> )
</th></tr></thead></table>
<p>

CurveFitter implements scipy.optimize.curve_fit.

Author:      Do Kester.

<b>Attributes</b>

* method  :  {'lm', 'trf', 'dogbox'}<br>
    'lm'        LevenbergMarquardt (default for no limits)<br>
    'trf'       Trust Region Reflective (default for limits)<br>
    'dogbox'    for small problems with limits<br>

<b>Raises</b>

ConvergenceError    Something went wrong during the convergence if the fit.


<a name="CurveFitter"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>CurveFitter(</strong> xdata, model, method=None, fixedScale=None, map=False, keep=None )
</th></tr></thead></table>
<p>

Create a new class, providing inputs and model.

<b>Parameters</b>

* xdata  :  array_like<br>
    array of independent input values<br>
* model  :  Model<br>
    the model function to be fitted<br>
* method  :  'lm' | 'trf' | 'dogbox'<br>
    method to be used<br>
* fixedScale  :  None or float<br>
    the fixed noise scale.<br>
* map  :  bool (False)<br>
    When true, the xdata should be interpreted as a map.<br>
    The fitting is done on the pixel indices of the map,<br>
    using ImageAssistant<br>
* keep  :  dict of {int:float}<br>
    dictionary of indices (int) to be kept at a fixed value (float)<br>
    The values of keep will be used by the Fitter as long as the Fitter exists.<br>
    See also `fit( ..., keep=dict )`<br>


<a name="fit"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>fit(</strong> ydata, weights=None, inipar=None, keep=None, limits=None,
 accuracy=None, plot=False, **kwargs )
</th></tr></thead></table>
<p>

Return      parameters for the model fitted to the data array.

<b>Parameters</b>

* ydata  :  array_like<br>
    the data vector to be fitted<br>
* weights  :  array_like<br>
    weights pertaining to the data<br>
    The weights are relative weights unless fixedScale is set.<br>
* accuracy  :  float or array_like<br>
    accuracy of (individual) data<br>
* inipar  :  array_like<br>
    inital parameters (default from Model)<br>
* keep  :   dict of {int:float}<br>
    dictionary of indices (int) to be kept at a fixed value (float)<br>
    The values of keep are only valid for *this* fit<br>
    See also `CurveFitter( ..., keep=dict )`<br>
* limits  :  None or list of 2 floats or list of 2 array_like<br>
    None :        from Model if Model has limits set else no limits<br>
    [-inf,+inf] : no limits applied<br>
    [lo,hi] :     low and high limits for all values<br>
    [la,ha] :     low array and high array limits for the values<br>
* plot  :  bool<br>
    Plot the results.<br>
* kwargs  :  dict<br>
    keywords arguments to be passed to :ref:`curve_fit<scipy.optimize.curve_fit>`<br>

<b>Raises</b>

    ValueError when ydata or weights contain a NaN

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>result(</strong> xdata, *fitpar ) 
</th></tr></thead></table>
<p>

Result method to make connection to the scipy optimizers

<b>Parameters</b>

* xdata  :  array_like<br>
    input data<br>
* fitpar  :  tuple of float<br>
    parameters for the model

<a name="jacobian"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>jacobian(</strong> xdata, *fitpar ) 
</th></tr></thead></table>
<p>

Method to make connection to the scipy optimizers

<b>Parameters</b>

* xdata  :  array_like<br>
    input data<br>
* fitpar  :  (tuple of) float<br>
    parameters for the model

<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./IterativeFitter.html">IterativeFitter</a></th></tr></thead></table>


* [<strong>setParameters(</strong> params )](./IterativeFitter.md#setParameters)
* [<strong>doPlot(</strong> param, force=False )](./IterativeFitter.md#doPlot)
* [<strong>fitprolog(</strong> ydata, weights=None, accuracy=None, keep=None ) ](./IterativeFitter.md#fitprolog)
* [<strong>report(</strong> verbose, param, chi, more=None, force=False ) ](./IterativeFitter.md#report)


<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
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
