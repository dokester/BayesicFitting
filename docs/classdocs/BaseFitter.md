---
---
<br><br>

<a name="BaseFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class BaseFitter(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseFitter.py target=_blank>Source</a></th></tr></thead></table>
<p>

Base class for all Fitters.

The Fitter class is to be used in conjunction with *Model classes.

The Fitter class and its descendants fit data to a model. Fitter itself
is the variant for linear models, ie. models linear in its parameters.

For both linear and nonlinear models it holds that once the optimal
estimate of the parameters is found, a variety of calculations is exactly
the same: standard deviations, noise scale, evidence and model errors.
They all derive more or less from the inverse Hessian matrix ( aka the
covariance matrix ). All these calculations are in this Fitter class.
Other Fitter classes relegate their calculation in these issues to this one.

<b>Examples</b>

It is not possible to use this class. User Fitter, CurveFitter etc. in stead

<b>Note Also</b>

1. The calculation of the evidence is an Gaussian approximation which is
&nbsp;&nbsp;&nbsp; only exact for linear models with a fixed scale.<br>
2. Attributes labelled as read only should not be set by a user.

* Author :  Do Kester<br>

<b>Attributes</b>

* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model to be fitted<br>
* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; independent variable(s)<br>
* nxdata  :  int (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; length of the xdata vector(s)<br>
* ndim  :  int (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of xdata vectors<br>
* weights  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; the weights on the data from the last fit<br>
* imageAssistant  :  ImageAssistant<br>
&nbsp;&nbsp;&nbsp;&nbsp; to convert images to pixels indices, needed for a fit<br>
* keep  :  dict of {int : float}<br>
&nbsp;&nbsp;&nbsp;&nbsp; to keep the indexed (int) parameter at the provided value (float)<br>
* fitIndex  :  list of int (or None)<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of parameter indices to fit (None is all)<br>
* npfit  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; the number of parameters fitted in the last fit.<br>
* fixedScale  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; the fixed noise scale.<br>
&nbsp;&nbsp;&nbsp;&nbsp; The presence of `fixedScale` has consequences for the definitions of `chisq`,<br>
&nbsp;&nbsp;&nbsp;&nbsp; `(co)variance`, `stdevs` and `evidence`<br>

* minimumScale  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; introduce a minimum value for the noise scale<br>
* design  :  matrix (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; the design matrix (partial of model to parameters)<br>
&nbsp;&nbsp;&nbsp;&nbsp; returns self.getDesign()<br>

<b>Attributes (available after a call to fit())</b>

* yfit  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; The model result at the optimal value for the parameters.<br>
&nbsp;&nbsp;&nbsp;&nbsp; If map is true, a map is returned.<br>
* chisq  :  float (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; chisquared of the fit<br>
* parameters  :  ndarray<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters fitted to the model<br>
&nbsp;&nbsp;&nbsp;&nbsp; returns self.model.parameters<br>
* stdevs, standardDeviations  :  array_like (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; the standard deviations on the parameters<br>
&nbsp;&nbsp;&nbsp;&nbsp; returns self.getStandardDeviations()<br>
* hessian  :  matrix (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; the hessian matrix<br>
* covariance  :  matrix (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; the covariance matrix<br>
&nbsp;&nbsp;&nbsp;&nbsp; returns self.getCovarianceMatrix()<br>
* scale  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; the noise scale<br>
&nbsp;&nbsp;&nbsp;&nbsp; returns self.getScale()<br>
* sumwgt  :  float (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; sum of the weights<br>
* logZ  :  float (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; the e-log of the evidence<br>
&nbsp;&nbsp;&nbsp;&nbsp; returns self.getLogZ()<br>
* evidence  :  float (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; the 10log of the evidence (logZ / log(10))<br>
&nbsp;&nbsp;&nbsp;&nbsp; returns self.getEvidence()<br>

<b>Attributes (available after a call to getLogZ() or getEvidence())</b>

* logOccam  :  float (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; Occam factor<br>
* logLikelihood  :  float (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; log of the likelihood<br>


<a name="BaseFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>BaseFitter(</strong> xdata, model, map=False, keep=None, fixedScale=None )
</th></tr></thead></table>
<p>

Create a new Fitter, providing inputs and model.

A Fitter class is defined by its model and the input vectors ( the
independent variable ). When a fit to another model and/or another
input vector is needed a new object should be created.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; independent input variable(s)<br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model function to be fitted<br>
* map  :  bool (False)<br>
&nbsp;&nbsp;&nbsp;&nbsp; When true, the xdata should be interpreted as a map.<br>
&nbsp;&nbsp;&nbsp;&nbsp; The fitting is done on the pixel indices of the map,<br>
&nbsp;&nbsp;&nbsp;&nbsp; using ImageAssistant<br>
* keep  :  dict of {int:float}<br>
&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)<br>
&nbsp;&nbsp;&nbsp;&nbsp; The values of keep will be used by the Fitter as long as the Fitter exists.<br>
&nbsp;&nbsp;&nbsp;&nbsp; See also fit( ..., keep=dict )<br>
* fixedScale  :  None or float<br>
&nbsp;&nbsp;&nbsp;&nbsp; None : the noise scale is not fixed<br>
&nbsp;&nbsp;&nbsp;&nbsp; float: value of the fixed noise scale<br>
&nbsp;&nbsp;&nbsp;&nbsp; The value of fixedScale only influences the evidence calculation<br>

<b>Raises</b>

ValueError when one of the following is true
&nbsp;&nbsp;&nbsp;&nbsp; 1. Dimensionality of model and input does not match.<br>
&nbsp;&nbsp;&nbsp;&nbsp; 2. Nans in input stream.<br>
&nbsp;&nbsp;&nbsp;&nbsp; 3. Model is not the head of a compound model chain.<br>


<a name="setMinimumScale"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setMinimumScale(</strong> scale=0 ) 
</th></tr></thead></table>
<p>

Introduce a minimum in scale calculation and consequently in chisq.
&nbsp;&nbsp;&nbsp;&nbsp; chi<sup>2</sup> >= sumwgt * scale<sup>2</sup><br>

<b>Parameters</b>

* scale  :  float<br>
    minimum scale

<a name="fitprolog"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fitprolog(</strong> ydata, weights=None, accuracy=None, keep=None ) 
</th></tr></thead></table>
<p>

Prolog for all Fitters.

1. Checks data/weighs/accuracy for Nans
2. Makes fitIndex.

<b>Parameters</b>

* ydata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted<br>
* weights  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights pertaining to the data<br>
* accuracy  :  float or array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; accuracy of (individual) data<br>
* keep  :  dict of {int:float}<br>
&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)<br>

<b>Returns</b>

* fitIndex  :  ndarray of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; Indices of the parameters that need fitting<br>
* ydata  :  ndarray<br>
&nbsp;&nbsp;&nbsp;&nbsp; Only different from input when ydata is a map <br>
* fitwgts  :  float or ndarray<br>
&nbsp;&nbsp;&nbsp;&nbsp; Combines weights and accuracy into ( weights / accuracy^2 )<br>
    1.0 if both are None

<a name="fitpostscript"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fitpostscript(</strong> ydata, plot=False ) 
</th></tr></thead></table>
<p>

Produce a plot of the results.

<a name="keepFixed"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>keepFixed(</strong> keep=None ) 
</th></tr></thead></table>
<p>

Keeps parameters fixed at the provided values.

1. The model will act exactly as if it were a model with less
&nbsp;&nbsp;&nbsp; parameters, although slightly less efficient.<br>
2. Repeated calls start from scratch.
3. Reset with keepFixed( None )

<b>Parameters</b>

* keep  :  dict of {int:float}<br>
&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)<br>

<b>Returns</b>

* fitIndex  :  list of int (or None)<br>
    list of parameter indices to be kept

<a name="insertParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>insertParameters(</strong> fitpar, index=None, into=None ) 
</th></tr></thead></table>
<p>

Insert fitparameters into the parameters when fitIndex is present.

<b>Parameters</b>

* fitpar  :  list of float<br>
&nbsp;&nbsp;&nbsp;&nbsp; (fitted) parameters<br>
* index  :  list of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of parameter indices to be kept<br>
* into  :  list of float<br>
&nbsp;&nbsp;&nbsp;&nbsp; array into which the fitpar need to be inserted.<br>


<a name="modelFit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>modelFit(</strong> ydata, weights=None, keep=None )
</th></tr></thead></table>
<p>

Return model fitted to the data.

<b>Parameters</b>

* ydata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted.<br>
* weights  :  None or array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights to be used<br>
* keep  :  dict of {int:float}<br>
&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)<br>
&nbsp;&nbsp;&nbsp;&nbsp; The values will override those at initialization.<br>
&nbsp;&nbsp;&nbsp;&nbsp; They are only used in this call of fit.<br>


<a name="limitsFit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>limitsFit(</strong> ydata, weights=None, keep=None ) 
</th></tr></thead></table>
<p>

Fit the data to the model.
When a parameter(s) transgresses the limits, it set and fixed at that limit
and the fit is done again, excluding the parameter(s)
When the chisq landscape is largely monomodal (no local minima) this is OK.

<b>Parameter</b>

* ydata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; data that the model needs to be fit to<br>
* weights  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights partaining to the data.<br>
* keep  :  dict of {int:float}<br>
&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)<br>
&nbsp;&nbsp;&nbsp;&nbsp; The values will override those at initialization.<br>
&nbsp;&nbsp;&nbsp;&nbsp; They are only used in this call of fit.<br>

<b>Returns</b>

* pars  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; the parameters of the fit<br>

<b>Raises</b>

Warning when parameters have been reset at the limits.


<a name="fit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fit(</strong> ydata, weights=None, keep=None ) 
</th></tr></thead></table>
<p>

Return model parameters fitted to the data.

<b>Parameters</b>

* ydata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted.<br>
* weights  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights to be used<br>
* keep  :  dict of {int:float}<br>
&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)<br>
&nbsp;&nbsp;&nbsp;&nbsp; The values will override those at initialization.<br>
&nbsp;&nbsp;&nbsp;&nbsp; They are only used in this call of fit.<br>

<b>Raises</b>

NotImplementedError. BaseFitter cannot perform fits by itself.


<a name="checkNan"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>checkNan(</strong> ydata, weights=None, accuracy=None )
</th></tr></thead></table>
<p>

Check there are no Nans or Infs in ydata or weights or accuracy.
Check also for zeros or negatives in accuracy.

<b>Parameters</b>

* ydata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; data to be fitted.<br>
* weights  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights pertaining to ydata<br>
* accuracy  :  float or array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; accuracy of (individual) data<br>

<b>Raises</b>

ValueError.

<a name="getVector"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getVector(</strong> ydata, index=None )
</th></tr></thead></table>
<p>

Return the &beta;-vector.

It includes "normalized" data if present. See normalize().

<b>Parameters</b>

* ydata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted. When such is appliccable, it should be<br>
&nbsp;&nbsp;&nbsp;&nbsp; multiplied by weights and/or appended by normdata.<br>
* index  :  list of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index of parameters to be fixed<br>


<a name="getHessian"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getHessian(</strong> params=None, weights=None, index=None )
</th></tr></thead></table>
<p>

Calculates the hessian matrix for a given set of model parameters.

It includes "normalized" data if present. See normalize()

<b>Parameters</b>

* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model parameters to be considered<br>
* weights  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights to be used<br>
* index  :  list of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index of parameters to be fixed<br>


<a name="getInverseHessian"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getInverseHessian(</strong> params=None, weights=None, index=None )
</th></tr></thead></table>
<p>

Return the inverse of the Hessian Matrix, H.

<b>Parameters</b>

* ydata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted.<br>
* weights  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights to be used<br>
* index  :  list of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index of parameters to be fixed<br>


<a name="getCovarianceMatrix"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getCovarianceMatrix(</strong> )
</th></tr></thead></table>
<p>

Returns the inverse hessian matrix over the fitted parameters,
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; multiplied by the variance.<br>

Stdevs are found from this as np.sqrt( np.diag( covarianceMatrix ) )


<a name="makeVariance"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makeVariance(</strong> scale=None )
</th></tr></thead></table>
<p>

Return the (calculated) variance of the remaining noise. I.e.
&nbsp;&nbsp;&nbsp;&nbsp; var = chisq / dof<br>
when automatic noise scaling is requested or
&nbsp;&nbsp;&nbsp;&nbsp; var = scale<sup>2</sup><br>
when we have a fixed scale.

<b>Parameters</b>

* scale  :  float<br>
    noise scale to be used

<a name="normalize"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>normalize(</strong> normdfdp, normdata, weight=1.0 ) 
</th></tr></thead></table>
<p>

If for some reason the model is degenerate, e.g when two parameters measure
essentially the same thing, This method can disambiguate these parameters.

It is like adding a dummy measurement of one (or more) parameter to the data.

<b>Parameters</b>

* normdfdp  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; for each parameter to sum to value (same length as self.parameters)<br>
* normdata  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; simulated data value<br>
* weight  :  float<br>
    weight of this measurement

<a name="getDesign"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getDesign(</strong> params=None, xdata=None, index=None )
</th></tr></thead></table>
<p>

Return the design matrix, D.
The design matrix is also known as the Jacobian Matrix.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; the independent input data<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters of the model<br>
* index  :  list of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index of parameters to be fixed<br>


<a name="chiSquared"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>chiSquared(</strong> ydata, params=None, weights=None )
</th></tr></thead></table>
<p>

Calculates Chi-Squared for data and weights.

It is the (weighted) sum of the squared residuals.

<b>Parameters</b>

* ydata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted.<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model<br>
* weights  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights to be used<br>

<b>Raises</b>

ValueError when chisq <= 0.


<a name="getStandardDeviations"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getStandardDeviations(</strong> )
</th></tr></thead></table>
<p>

Calculates of standard deviations pertaining to the parameters.

&nbsp;&nbsp;&nbsp;&nbsp; &sigma;<sub>i</sub> = s * sqrt( C[i,i] )<br>

where C is the Covariance matrix, the inverse of the Hessian Matrix and
s is the noiseScale.

Standard deviation are calculated for the fitted parameters only.

Note that the stdev will decrease with sqrt( N ) of the number of
datapoints while the noise scale, s, does not.


<a name="monteCarloError"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>monteCarloError(</strong> xdata=None, monteCarlo=None)
</th></tr></thead></table>
<p>

Calculates &sigma;-confidence regions on the model given some inputs.

From the full covariance matrix (inverse of the Hessian) random
samples are drawn, which are added to the parameters. With this new
set of parameters the model is calculated. This procedure is done
by default, 25 times.
The standard deviation of the models is returned as the error bar.

The calculation of the confidence region is delegated to the class
MonteCarlo. For tweaking of that class can be done outside BaseFitter.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; input data over which to calculate the error bars.<br>
* monteCarlo  :  MonteCarlo<br>
&nbsp;&nbsp;&nbsp;&nbsp; a ready-made MonteCarlo class.<br>


<a name="getScale"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getScale(</strong> )
</th></tr></thead></table>
<p>

<b>Return</b>

* float  :  the noise scale<br>
&nbsp;&nbsp;&nbsp;&nbsp; scale = sqrt( chisq / DOF )<br>

<b>Raise</b>

RuntimeError when DoF <= 0. The number of (weighted) datapoints is too small.


<a name="getEvidence"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getEvidence(</strong> limits=None, noiseLimits=None )
</th></tr></thead></table>
<p>

Calculation of the evidence, log10( Z ), for the model given the data.

&nbsp;&nbsp;&nbsp;&nbsp; E = log10( P( Model | data ) )<br>

The calculation of the evidence uses a Gaussion approximation of the Posterior
probability.
It needs to know the limits of the parameters (and the noise scale if applicable),
either from the priors in the model or from keywords "limits/noiseLimits".


<b>Parameters</b>

* limits  :  list of 2 floats/array_likes<br>
&nbsp;&nbsp;&nbsp;&nbsp; possible range of the parameters. ( [low,high] )<br>
* noiseLimits  :  list of 2 floats<br>
&nbsp;&nbsp;&nbsp;&nbsp; possible range on noise scale ( [low,high] )<br>

<b>Raises</b>

ValueError when no Prior is available


<a name="getLogLikelihood"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLogLikelihood(</strong> autoscale=False, var=1.0 ) 
</th></tr></thead></table>
<p>

Return the log likelihood.

It is implementing eq 19/20 last parts (Kester 2002) term by term

<b>Parameters</b>

* autoscale  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; whether the noise scale is optimized too<br>
* var  :  float<br>
    variance

<a name="getLogZ"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLogZ(</strong> limits=None, noiseLimits=None )
</th></tr></thead></table>
<p>

Calculation of the evidence, log( Z ), for the model given the data.

&nbsp;&nbsp;&nbsp;&nbsp; logZ = log( P( Model | data ) )<br>

The calculation of the evidence uses a Gaussion approximation of the Posterior
probability.
It needs to know the limits of the parameters (and the noise scale if applicable),
either from the priors in the model or from keywords "limits/noiseLimits".


<b>Parameters</b>

* limits  :  list of 2 floats/array_likes<br>
&nbsp;&nbsp;&nbsp;&nbsp; possible range of the parameters. ( [low,high] )<br>
* noiseLimits  :  list of 2 floats<br>
&nbsp;&nbsp;&nbsp;&nbsp; possible range on noise scale ( [low,high] )<br>

<b>Raises</b>

ValueError when no Prior is available

RuntimeError when DoF <= 0. The number of (weighted) datapoints is too small.


<a name="plotResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotResult(</strong> xdata=None, ydata=None, model=None, residuals=True,
 confidence=False, show=True ) 
</th></tr></thead></table>
<p>

Plot the results of the fit.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; xdata of the problem<br>
* ydata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; ydata of the problem<br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model the ydata are fitted to at xdata.<br>
* residuals  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; plot the residuals in a separate panel.<br>
* confidence  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; plot confidence region<br>
* show  :  bool<br>
    display the plot.

