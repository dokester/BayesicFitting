---
---
<br><br>

<a name="QRFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class QRFitter(</strong> <a href="./BaseFitter.html">BaseFitter</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/QRFitter.py target=_blank>Source</a></th></tr></thead></table>
<p>

Fitter for linear models, using QR decomposition.
The QRFitter class is to be used in conjunction with Model classes, linear
in its parameters.

For Linear models the matrix equation

<br>&nbsp;&nbsp;&nbsp;&nbsp; H * p = &beta;<br>

is solved for p. H is the Hessian matrix ( D * w * D<sup>T</sup> )
and &beta; is the inproduct of the data with the D, design matrix.

<br>&nbsp;&nbsp;&nbsp;&nbsp; &beta; = y * w * D<sup>T</sup><br>

The QRFitter class use QR decomposition which effectively is an inversion
of the hessian matrix such that

<br>&nbsp;&nbsp;&nbsp;&nbsp; p = &beta; * inverse( H )<br>

It can be more efficient if
similar ydata needs to be fitter to the same model and xdata.
In that case it uses the same decomposition for all fits.

<b>Examples</b><br>
    # assume x and y are numpy.asarray data arrays
    x = numpy.asarray.range( 100 )
    poly = PolynomialModel( 1 )                             # line
    fitter = QRFitter( x, poly )
    for k in range( 1, 4 ) 
        y = numpy.arange( 100 ) // k                        # digitization noise
        param = fitter.fit( y )                             # use same QR decomposition
        stdev = fitter.stdevs                               # stdevs on the parameters
        print( k, param )
        print( " ", stdev )

* Category :     Mathematics/Fitting<br>

<b>Attributes</b><br>
* needsNewDecomposition  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; True when starting. Thereafter False,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; i.e. the previous QR-decomposition is used, unless weights are used.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Only for linear fitters, setting it to false might improve efficiency.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; It only works properly when the model, the x-data etc are exactly the<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; same in the previous run.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Whenever weights are used, it always needs a new decomposition.<br>

* qrmat  :  matrix<br>
&nbsp;&nbsp;&nbsp;&nbsp; matrix formed by q * inverse( r ), where q,r is the QR decomposition<br>
&nbsp;&nbsp;&nbsp;&nbsp; of the design matrix.<br>
&nbsp;&nbsp;&nbsp;&nbsp; qrmat is to be multiplied with the data vector to get the solution.<br>


<a name="QRFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>QRFitter(</strong> xdata, model, map=False, keep=None )
</th></tr></thead></table>
<p>

Create a new Fitter, providing xdatas and model.

A Fitter class is defined by its model and the input vector (the
independent variable). When a fit to another model and/or another
input vector is needed a new object should be created.

<b>Parameters</b><br>
* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; array of independent input values<br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model function to be fitted<br>
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
<strong>fit(</strong> ydata, weights=None, accuracy=None, keep=None )
</th></tr></thead></table>
<p>

Return model parameters fitted to the data, including weights.

<b>Parameters</b><br>
* ydata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted<br>
* weights  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights pertaining to the data ( = 1.0 / sigma^2 )<br>
* accuracy  :  float or array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; accuracy of (individual) data<br>
* keep  :  dict of {int:float}<br>
&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)<br>
&nbsp;&nbsp;&nbsp;&nbsp; The values will override those at initialization.<br>
&nbsp;&nbsp;&nbsp;&nbsp; They are only used in this call of fit.<br>
<b>Raises</b><br>
ValueError when ydata or weights contain a NaN


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
