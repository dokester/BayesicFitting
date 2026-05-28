---
---
<br><br>

<a name="CurveFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class CurveFitter(</strong> <a href="./IterativeFitter.html">IterativeFitter</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/CurveFitter.py target=_blank>[source]</a></th></tr></thead></table>
<p>

CurveFitter implements `scipy.optimize.curve<sub>fit</sub>`.

Author:      Do Kester.

<b>Attributes</b><br>
* method  :  {'lm', 'trf', 'dogbox'}
<br>&nbsp;&nbsp;&nbsp;&nbsp; 'lm'        LevenbergMarquardt (default for no limits)
<br>&nbsp;&nbsp;&nbsp;&nbsp; 'trf'       Trust Region Reflective (default for limits)
<br>&nbsp;&nbsp;&nbsp;&nbsp; 'dogbox'    for small problems with limits

<b>Raises</b><br>
ConvergenceError    Something went wrong during the convergence if the fit.


<a name="CurveFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>CurveFitter(</strong> xdata, model, method=None, fixedScale=None, map=False, keep=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/CurveFitter.py#L49-L77 target=_blank>[source]</a></th></tr></thead></table>

Create a new class, providing inputs and model.

<b>Parameters</b><br>
* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of independent input values
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model function to be fitted
* method  :  'lm' | 'trf' | 'dogbox'
<br>&nbsp;&nbsp;&nbsp;&nbsp; method to be used
* fixedScale  :  None or float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the fixed noise scale.
* map  :  bool (False)
<br>&nbsp;&nbsp;&nbsp;&nbsp; When true, the xdata should be interpreted as a map.
<br>&nbsp;&nbsp;&nbsp;&nbsp; The fitting is done on the pixel indices of the map,
<br>&nbsp;&nbsp;&nbsp;&nbsp; using ImageAssistant
* keep  :  dict of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The values of keep will be used by the Fitter as long as the Fitter exists.
<br>&nbsp;&nbsp;&nbsp;&nbsp; See also `fit( ..., keep=dict )`


<a name="fit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fit(</strong> ydata, weights=None, inipar=None, keep=None, limits=None,
 accuracy=None, plot=False, **kwargs )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/CurveFitter.py#L79-L170 target=_blank>[source]</a></th></tr></thead></table>
Return      parameters for the model fitted to the data array.

<b>Parameters</b><br>
* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted
* weights  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights pertaining to the data
<br>&nbsp;&nbsp;&nbsp;&nbsp; The weights are relative weights unless fixedScale is set.
* accuracy  :  float or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; accuracy of (individual) data
* inipar  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; inital parameters (default from Model)
* keep  :   dict of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The values of keep are only valid for *this* fit
<br>&nbsp;&nbsp;&nbsp;&nbsp; See also `CurveFitter( ..., keep=dict )`
* limits  :  None or list of 2 floats or list of 2 array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; None :        from Model if Model has limits set else no limits
<br>&nbsp;&nbsp;&nbsp;&nbsp; [-inf,+inf] : no limits applied
<br>&nbsp;&nbsp;&nbsp;&nbsp; [lo,hi] :     low and high limits for all values
<br>&nbsp;&nbsp;&nbsp;&nbsp; [la,ha] :     low array and high array limits for the values
* plot  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; Plot the results.
* kwargs  :  dict
<br>&nbsp;&nbsp;&nbsp;&nbsp; keywords arguments to be passed to `curve_fit<scipy.optimize.curve_fit>`

<b>Raises</b><br>
ValueError when ydata or weights contain a NaN

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> xdata, *fitpar ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/CurveFitter.py#L182-L200 target=_blank>[source]</a></th></tr></thead></table>
Result method to make connection to the scipy optimizers

<b>Parameters</b><br>
* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; input data
* fitpar  :  tuple of float
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model

<a name="jacobian"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>jacobian(</strong> xdata, *fitpar ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/CurveFitter.py#L202-L216 target=_blank>[source]</a></th></tr></thead></table>
Method to make connection to the scipy optimizers

<b>Parameters</b><br>
* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; input data
* fitpar  :  (tuple of) float
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./IterativeFitter.html">IterativeFitter</a></th></tr></thead></table>


* [<strong>setParameters(</strong> params )](./IterativeFitter.md#setParameters)
* [<strong>setPlotters(</strong> plot ) ](./IterativeFitter.md#setPlotters)
* [<strong>plotNot(</strong> ydata, param, force=False ) ](./IterativeFitter.md#plotNot)
* [<strong>plotIter(</strong> ydata, param, force=False ) ](./IterativeFitter.md#plotIter)
* [<strong>fitprolog(</strong> ydata, weights=None, accuracy=None, keep=None ) ](./IterativeFitter.md#fitprolog)
* [<strong>report(</strong> verbose, ydata, param, chi, more=None, force=False ) ](./IterativeFitter.md#report)


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
