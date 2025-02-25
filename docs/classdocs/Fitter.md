---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Fitter.py target=_blank>Source</a></span></div>

<a name="Fitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class Fitter(</strong> <a href="./BaseFitter.html">BaseFitter</a> )
</th></tr></thead></table>
<p>

Fitter for linear models.

The Fitter class is to be used in conjunction with Model classes.

The Fitter class and its descendants fit data to a model. Fitter itself
is the variant for linear models, ie. models linear in its parameters.

<b>Examples</b>

* # assume x and y are numpy.asarray data arrays : <br>
    x = numpy.arange( 100 )<br>
    y = numpy.arange( 100 ) // 4        # digitization noise<br>
    poly = PolynomialModel( 1 )         # line<br>
    fitter = Fitter( x, poly )<br>
    param = fitter.fit( y )<br>
    stdev = fitter.stdevs               # stdevs on the parameters<br>
    chisq = fitter.chisq<br>
    scale = fitter.scale                # noise scale<br>
    yfit  = fitter.getResult( )         # fitted values<br>
    yfit  = poly( x )                   # same as previous<br>
    yband = fitter.monteCarloError( )        # 1 sigma confidence region<br>


<b>Limitations</b>

1. The Fitter does not work with limits.
2. The calculation of the evidence is an Gaussian approximation which is
   only exact for linear models with a fixed scale.<br>

Author  Do Kester


<a name="Fitter"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>Fitter(</strong> xdata, model, map=False, keep=None, fixedScale=None )
</th></tr></thead></table>
<p>

Create a new Fitter, providing xdatas and model.

A Fitter class is defined by its model and the input vector (the
independent variable). When a fit to another model and/or another
input vector is needed a new object should be created.

<b>Parameters</b>

* xdata  :  array_like<br>
    array of independent input values<br>
* model  :  Model<br>
    the model function to be fitted<br>
* map  :  bool (False)<br>
    When true, the xdata should be interpreted as a map.<br>
    The fitting is done on the pixel indices of the map,<br>
    using ImageAssistant<br>
* keep  :  dict of {int:float}<br>
    dictionary of indices (int) to be kept at a fixed value (float)<br>
    The values of keep will be used by the Fitter as long as the Fitter exists.<br>
    See also `fit( ..., keep=dict )`<br>
* fixedScale  :  float<br>
    the fixed noise scale<br>


<a name="fit"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>fit(</strong> ydata, weights=None, accuracy=None, keep=None, plot=False )
</th></tr></thead></table>
<p>

Return model parameters fitted to the data, including weights.

For Linear models the matrix equation

    H * p = &beta;<br>

is solved for p. H is the Hessian matrix ( D * w * D^T )
and &beta; is the inproduct of the data with the D, design matrix.

    &beta; = y * w * D^T<br>

<b>Parameters</b>

* ydata  :  array_like<br>
    the data vector to be fitted<br>
* weights  :  array_like<br>
    weights pertaining to the data ( = 1.0 / sigma^2 )<br>
* accuracy  :  float or array_like<br>
    accuracy of (individual) data<br>
* keep  :  dict of {int:float}<br>
    dictionary of indices (int) to be kept at a fixed value (float)<br>
    The values will override those at initialization.<br>
    They are only used in this call of fit.<br>
* plot  :  bool<br>
    Plot the results<br>

<b>Raises</b>

    ValueError when ydata or weights contain a NaN<br>


<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./BaseFitter.html">BaseFitter</a></th></tr></thead></table>


* [<strong>setMinimumScale(</strong> scale=0 ) ](./BaseFitter.md#setMinimumScale)
* [<strong>fitprolog(</strong> ydata, weights=None, accuracy=None, keep=None ) ](./BaseFitter.md#fitprolog)
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
