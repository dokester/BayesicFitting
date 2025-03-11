---
---
<br><br>

<a name="Fitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Fitter(</strong> <a href="./BaseFitter.html">BaseFitter</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Fitter.py target=_blank>Source</a></th></tr></thead></table>

Fitter for linear models.

The Fitter class is to be used in conjunction with Model classes.

The Fitter class and its descendants fit data to a model. Fitter itself
is the variant for linear models, ie. models linear in its parameters.

<b>Examples</b>

    # assume x and y are numpy.asarray data arrays
    x = numpy.arange( 100 )
    y = numpy.arange( 100 ) // 4        # digitization noise
    poly = PolynomialModel( 1 )         # line
    fitter = Fitter( x, poly )
    param = fitter.fit( y )
    stdev = fitter.stdevs               # stdevs on the parameters
    chisq = fitter.chisq
    scale = fitter.scale                # noise scale
    yfit  = fitter.getResult( )         # fitted values
    yfit  = poly( x )                   # same as previous
    yband = fitter.monteCarloError( )        # 1 sigma confidence region


<b>Limitations</b>

1. The Fitter does not work with limits.
2. The calculation of the evidence is an Gaussian approximation which is
<br>&nbsp;&nbsp;&nbsp; only exact for linear models with a fixed scale.

Author  Do Kester


<a name="Fitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Fitter(</strong> xdata, model, map=False, keep=None, fixedScale=None )
</th></tr></thead></table>

Create a new Fitter, providing xdatas and model.

A Fitter class is defined by its model and the input vector (the
independent variable). When a fit to another model and/or another
input vector is needed a new object should be created.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of independent input values
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model function to be fitted
* map  :  bool (False)
<br>&nbsp;&nbsp;&nbsp;&nbsp; When true, the xdata should be interpreted as a map.
<br>&nbsp;&nbsp;&nbsp;&nbsp; The fitting is done on the pixel indices of the map,
<br>&nbsp;&nbsp;&nbsp;&nbsp; using ImageAssistant
* keep  :  dict of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The values of keep will be used by the Fitter as long as the Fitter exists.
<br>&nbsp;&nbsp;&nbsp;&nbsp; See also `fit( ..., keep=dict )`
* fixedScale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the fixed noise scale


<a name="fit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fit(</strong> ydata, weights=None, accuracy=None, keep=None, plot=False )
</th></tr></thead></table>
Return model parameters fitted to the data, including weights.

For Linear models the matrix equation

&nbsp;&nbsp;&nbsp;&nbsp; H * p = &beta;

is solved for p. H is the Hessian matrix ( D * w * D<sup>T</sup> )
and &beta; is the inproduct of the data with the D, design matrix.

&nbsp;&nbsp;&nbsp;&nbsp; &beta; = y * w * D<sup>T</sup>

<b>Parameters</b>

* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted
* weights  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights pertaining to the data ( = 1.0 / sigma^2 )
* accuracy  :  float or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; accuracy of (individual) data
* keep  :  dict of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The values will override those at initialization.
<br>&nbsp;&nbsp;&nbsp;&nbsp; They are only used in this call of fit.
* plot  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; Plot the results

<b>Raises</b>

&nbsp;&nbsp;&nbsp;&nbsp; ValueError when ydata or weights contain a NaN


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
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
