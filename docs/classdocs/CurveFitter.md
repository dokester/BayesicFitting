---
---
<br><br>

<a name="CurveFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class CurveFitter(</strong> <a href="./IterativeFitter.html">IterativeFitter</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/CurveFitter.py target=_blank>Source</a></th></tr></thead></table>
<p>

CurveFitter implements scipy.optimize.curve<sub>f</sub>it.

Author:      Do Kester.

<b>Attributes</b>

* method  :  {'lm', 'trf', 'dogbox'}<br>
&nbsp;&nbsp;&nbsp;&nbsp; 'lm'        LevenbergMarquardt (default for no limits)<br>
&nbsp;&nbsp;&nbsp;&nbsp; 'trf'       Trust Region Reflective (default for limits)<br>
&nbsp;&nbsp;&nbsp;&nbsp; 'dogbox'    for small problems with limits<br>

<b>Raises</b>

ConvergenceError    Something went wrong during the convergence if the fit.


<a name="CurveFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>CurveFitter(</strong> xdata, model, method=None, fixedScale=None, map=False, keep=None )
</th></tr></thead></table>
<p>

Create a new class, providing inputs and model.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; array of independent input values<br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model function to be fitted<br>
* method  :  'lm' | 'trf' | 'dogbox'<br>
&nbsp;&nbsp;&nbsp;&nbsp; method to be used<br>
* fixedScale  :  None or float<br>
&nbsp;&nbsp;&nbsp;&nbsp; the fixed noise scale.<br>
* map  :  bool (False)<br>
&nbsp;&nbsp;&nbsp;&nbsp; When true, the xdata should be interpreted as a map.<br>
&nbsp;&nbsp;&nbsp;&nbsp; The fitting is done on the pixel indices of the map,<br>
&nbsp;&nbsp;&nbsp;&nbsp; using ImageAssistant<br>
* keep  :  dict of {int:float}<br>
&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)<br>
&nbsp;&nbsp;&nbsp;&nbsp; The values of keep will be used by the Fitter as long as the Fitter exists.<br>
&nbsp;&nbsp;&nbsp;&nbsp; See also `fit( ..., keep=dict )`<br>


<a name="fit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fit(</strong> ydata, weights=None, inipar=None, keep=None, limits=None,
 accuracy=None, plot=False, **kwargs )
</th></tr></thead></table>
<p>

Return      parameters for the model fitted to the data array.

<b>Parameters</b>

* ydata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted<br>
* weights  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights pertaining to the data<br>
&nbsp;&nbsp;&nbsp;&nbsp; The weights are relative weights unless fixedScale is set.<br>
* accuracy  :  float or array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; accuracy of (individual) data<br>
* inipar  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; inital parameters (default from Model)<br>
* keep  :   dict of {int:float}<br>
&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)<br>
&nbsp;&nbsp;&nbsp;&nbsp; The values of keep are only valid for *this* fit<br>
&nbsp;&nbsp;&nbsp;&nbsp; See also `CurveFitter( ..., keep=dict )`<br>
* limits  :  None or list of 2 floats or list of 2 array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; None :        from Model if Model has limits set else no limits<br>
&nbsp;&nbsp;&nbsp;&nbsp; [-inf,+inf] : no limits applied<br>
&nbsp;&nbsp;&nbsp;&nbsp; [lo,hi] :     low and high limits for all values<br>
&nbsp;&nbsp;&nbsp;&nbsp; [la,ha] :     low array and high array limits for the values<br>
* plot  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; Plot the results.<br>
* kwargs  :  dict<br>
&nbsp;&nbsp;&nbsp;&nbsp; keywords arguments to be passed to :ref:`curve_fit<scipy.optimize.curve_fit>`<br>

<b>Raises</b>

ValueError when ydata or weights contain a NaN

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> xdata, *fitpar ) 
</th></tr></thead></table>
<p>

Result method to make connection to the scipy optimizers

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; input data<br>
* fitpar  :  tuple of float<br>
    parameters for the model

<a name="jacobian"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>jacobian(</strong> xdata, *fitpar ) 
</th></tr></thead></table>
<p>

Method to make connection to the scipy optimizers

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; input data<br>
* fitpar  :  (tuple of) float<br>
    parameters for the model

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
