---
---
<br><br>

<a name="BaseFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class BaseFitter(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/BaseFitter.py target=_blank>Source</a></th></tr></thead></table>

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
<br>&nbsp;&nbsp;&nbsp; only exact for linear models with a fixed scale.
2. Attributes labelled as read only should not be set by a user.

* Author :  Do Kester

<b>Attributes</b>

* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model to be fitted
* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; independent variable(s)
* nxdata  :  int (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; length of the xdata vector(s)
* ndim  :  int (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of xdata vectors
* weights  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the weights on the data from the last fit
* imageAssistant  :  ImageAssistant
<br>&nbsp;&nbsp;&nbsp;&nbsp; to convert images to pixels indices, needed for a fit
* keep  :  dict of {int : float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; to keep the indexed (int) parameter at the provided value (float)
* fitIndex  :  list of int (or None)
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of parameter indices to fit (None is all)
* npfit  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; the number of parameters fitted in the last fit.
* fixedScale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the fixed noise scale.
<br>&nbsp;&nbsp;&nbsp;&nbsp; The presence of `fixedScale` has consequences for the definitions of `chisq`,
<br>&nbsp;&nbsp;&nbsp;&nbsp; `(co)variance`, `stdevs` and `evidence`

* minimumScale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; introduce a minimum value for the noise scale
* design  :  matrix (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; the design matrix (partial of model to parameters)
<br>&nbsp;&nbsp;&nbsp;&nbsp; returns self.getDesign()

<b>Attributes (available after a call to fit())</b>

* yfit  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; The model result at the optimal value for the parameters.
<br>&nbsp;&nbsp;&nbsp;&nbsp; If map is true, a map is returned.
* chisq  :  float (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; chisquared of the fit
* parameters  :  ndarray
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters fitted to the model
<br>&nbsp;&nbsp;&nbsp;&nbsp; returns self.model.parameters
* stdevs, standardDeviations  :  array_like (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; the standard deviations on the parameters
<br>&nbsp;&nbsp;&nbsp;&nbsp; returns self.getStandardDeviations()
* hessian  :  matrix (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; the hessian matrix
* covariance  :  matrix (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; the covariance matrix
<br>&nbsp;&nbsp;&nbsp;&nbsp; returns self.getCovarianceMatrix()
* scale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the noise scale
<br>&nbsp;&nbsp;&nbsp;&nbsp; returns self.getScale()
* sumwgt  :  float (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; sum of the weights
* logZ  :  float (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; the e-log of the evidence
<br>&nbsp;&nbsp;&nbsp;&nbsp; returns self.getLogZ()
* evidence  :  float (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; the 10log of the evidence (logZ / log(10))
<br>&nbsp;&nbsp;&nbsp;&nbsp; returns self.getEvidence()

<b>Attributes (available after a call to getLogZ() or getEvidence())</b>

* logOccam  :  float (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; Occam factor
* logLikelihood  :  float (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; log of the likelihood


<a name="BaseFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>BaseFitter(</strong> xdata, model, map=False, keep=None, fixedScale=None )
</th></tr></thead></table>

Create a new Fitter, providing inputs and model.

A Fitter class is defined by its model and the input vectors ( the
independent variable ). When a fit to another model and/or another
input vector is needed a new object should be created.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; independent input variable(s)
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model function to be fitted
* map  :  bool (False)
<br>&nbsp;&nbsp;&nbsp;&nbsp; When true, the xdata should be interpreted as a map.
<br>&nbsp;&nbsp;&nbsp;&nbsp; The fitting is done on the pixel indices of the map,
<br>&nbsp;&nbsp;&nbsp;&nbsp; using ImageAssistant
* keep  :  dict of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The values of keep will be used by the Fitter as long as the Fitter exists.
<br>&nbsp;&nbsp;&nbsp;&nbsp; See also fit( ..., keep=dict )
* fixedScale  :  None or float
<br>&nbsp;&nbsp;&nbsp;&nbsp; None : the noise scale is not fixed
<br>&nbsp;&nbsp;&nbsp;&nbsp; float: value of the fixed noise scale
<br>&nbsp;&nbsp;&nbsp;&nbsp; The value of fixedScale only influences the evidence calculation

<b>Raises</b>

ValueError when one of the following is true
<br>&nbsp;&nbsp;&nbsp;&nbsp; 1. Dimensionality of model and input does not match.
<br>&nbsp;&nbsp;&nbsp;&nbsp; 2. Nans in input stream.
<br>&nbsp;&nbsp;&nbsp;&nbsp; 3. Model is not the head of a compound model chain.


<a name="setMinimumScale"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setMinimumScale(</strong> scale=0 ) 
</th></tr></thead></table>
Introduce a minimum in scale calculation and consequently in chisq.
<br>&nbsp;&nbsp;&nbsp;&nbsp; chi<sup>2</sup> >= sumwgt * scale<sup>2</sup>

<b>Parameters</b>

* scale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; minimum scale

<a name="fitprolog"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fitprolog(</strong> ydata, weights=None, accuracy=None, keep=None ) 
</th></tr></thead></table>
Prolog for all Fitters.

1. Checks data/weighs/accuracy for Nans
2. Makes fitIndex.

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
* ydata  :  ndarray
<br>&nbsp;&nbsp;&nbsp;&nbsp; Only different from input when ydata is a map 
* fitwgts  :  float or ndarray
<br>&nbsp;&nbsp;&nbsp;&nbsp; Combines weights and accuracy into ( weights / accuracy^2 )
<br>&nbsp;&nbsp;&nbsp;&nbsp; 1.0 if both are None

<a name="fitpostscript"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fitpostscript(</strong> ydata, plot=False ) 
</th></tr></thead></table>
Produce a plot of the results.

<a name="keepFixed"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>keepFixed(</strong> keep=None ) 
</th></tr></thead></table>
Keeps parameters fixed at the provided values.

1. The model will act exactly as if it were a model with less
<br>&nbsp;&nbsp;&nbsp; parameters, although slightly less efficient.
2. Repeated calls start from scratch.
3. Reset with keepFixed( None )

<b>Parameters</b>

* keep  :  dict of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)

<b>Returns</b>

* fitIndex  :  list of int (or None)
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of parameter indices to be kept

<a name="insertParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>insertParameters(</strong> fitpar, index=None, into=None ) 
</th></tr></thead></table>
Insert fitparameters into the parameters when fitIndex is present.

<b>Parameters</b>

* fitpar  :  list of float
<br>&nbsp;&nbsp;&nbsp;&nbsp; (fitted) parameters
* index  :  list of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of parameter indices to be kept
* into  :  list of float
<br>&nbsp;&nbsp;&nbsp;&nbsp; array into which the fitpar need to be inserted.


<a name="modelFit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>modelFit(</strong> ydata, weights=None, keep=None )
</th></tr></thead></table>
Return model fitted to the data.

<b>Parameters</b>

* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted.
* weights  :  None or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights to be used
* keep  :  dict of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The values will override those at initialization.
<br>&nbsp;&nbsp;&nbsp;&nbsp; They are only used in this call of fit.


<a name="limitsFit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>limitsFit(</strong> ydata, weights=None, keep=None ) 
</th></tr></thead></table>
Fit the data to the model.
When a parameter(s) transgresses the limits, it set and fixed at that limit
and the fit is done again, excluding the parameter(s)
When the chisq landscape is largely monomodal (no local minima) this is OK.

<b>Parameter</b>

* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; data that the model needs to be fit to
* weights  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights partaining to the data.
* keep  :  dict of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The values will override those at initialization.
<br>&nbsp;&nbsp;&nbsp;&nbsp; They are only used in this call of fit.

<b>Returns</b>

* pars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the parameters of the fit

<b>Raises</b>

Warning when parameters have been reset at the limits.


<a name="fit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fit(</strong> ydata, weights=None, keep=None ) 
</th></tr></thead></table>
Return model parameters fitted to the data.

<b>Parameters</b>

* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted.
* weights  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights to be used
* keep  :  dict of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The values will override those at initialization.
<br>&nbsp;&nbsp;&nbsp;&nbsp; They are only used in this call of fit.

<b>Raises</b>

NotImplementedError. BaseFitter cannot perform fits by itself.


<a name="checkNan"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>checkNan(</strong> ydata, weights=None, accuracy=None )
</th></tr></thead></table>
Check there are no Nans or Infs in ydata or weights or accuracy.
Check also for zeros or negatives in accuracy.

<b>Parameters</b>

* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; data to be fitted.
* weights  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights pertaining to ydata
* accuracy  :  float or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; accuracy of (individual) data

<b>Raises</b>

ValueError.

<a name="getVector"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getVector(</strong> ydata, index=None )
</th></tr></thead></table>
Return the &beta;-vector.

It includes "normalized" data if present. See normalize().

<b>Parameters</b>

* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted. When such is appliccable, it should be
<br>&nbsp;&nbsp;&nbsp;&nbsp; multiplied by weights and/or appended by normdata.
* index  :  list of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index of parameters to be fixed


<a name="getHessian"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getHessian(</strong> params=None, weights=None, index=None )
</th></tr></thead></table>
Calculates the hessian matrix for a given set of model parameters.

It includes "normalized" data if present. See normalize()

<b>Parameters</b>

* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model parameters to be considered
* weights  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights to be used
* index  :  list of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index of parameters to be fixed


<a name="getInverseHessian"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getInverseHessian(</strong> params=None, weights=None, index=None )
</th></tr></thead></table>
Return the inverse of the Hessian Matrix, H.

<b>Parameters</b>

* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted.
* weights  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights to be used
* index  :  list of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index of parameters to be fixed


<a name="getCovarianceMatrix"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getCovarianceMatrix(</strong> )
</th></tr></thead></table>
Returns the inverse hessian matrix over the fitted parameters,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; multiplied by the variance.

Stdevs are found from this as np.sqrt( np.diag( covarianceMatrix ) )


<a name="makeVariance"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makeVariance(</strong> scale=None )
</th></tr></thead></table>
Return the (calculated) variance of the remaining noise. I.e.
<br>&nbsp;&nbsp;&nbsp;&nbsp; var = chisq / dof
when automatic noise scaling is requested or
<br>&nbsp;&nbsp;&nbsp;&nbsp; var = scale<sup>2</sup>
when we have a fixed scale.

<b>Parameters</b>

* scale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; noise scale to be used

<a name="normalize"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>normalize(</strong> normdfdp, normdata, weight=1.0 ) 
</th></tr></thead></table>
If for some reason the model is degenerate, e.g when two parameters measure
essentially the same thing, This method can disambiguate these parameters.

It is like adding a dummy measurement of one (or more) parameter to the data.

<b>Parameters</b>

* normdfdp  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; for each parameter to sum to value (same length as self.parameters)
* normdata  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; simulated data value
* weight  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; weight of this measurement

<a name="getDesign"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getDesign(</strong> params=None, xdata=None, index=None )
</th></tr></thead></table>
Return the design matrix, D.
The design matrix is also known as the Jacobian Matrix.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the independent input data
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters of the model
* index  :  list of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index of parameters to be fixed


<a name="chiSquared"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>chiSquared(</strong> ydata, params=None, weights=None )
</th></tr></thead></table>
Calculates Chi-Squared for data and weights.

It is the (weighted) sum of the squared residuals.

<b>Parameters</b>

* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted.
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model
* weights  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; weights to be used

<b>Raises</b>

ValueError when chisq <= 0.


<a name="getStandardDeviations"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getStandardDeviations(</strong> )
</th></tr></thead></table>
Calculates of standard deviations pertaining to the parameters.

&nbsp;&nbsp;&nbsp;&nbsp; &sigma;<sub>i</sub> = s * sqrt( C[i,i] )

where C is the Covariance matrix, the inverse of the Hessian Matrix and
s is the noiseScale.

Standard deviation are calculated for the fitted parameters only.

Note that the stdev will decrease with sqrt( N ) of the number of
datapoints while the noise scale, s, does not.


<a name="monteCarloError"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>monteCarloError(</strong> xdata=None, monteCarlo=None)
</th></tr></thead></table>
Calculates &sigma;-confidence regions on the model given some inputs.

From the full covariance matrix (inverse of the Hessian) random
samples are drawn, which are added to the parameters. With this new
set of parameters the model is calculated. This procedure is done
by default, 25 times.
The standard deviation of the models is returned as the error bar.

The calculation of the confidence region is delegated to the class
MonteCarlo. For tweaking of that class can be done outside BaseFitter.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; input data over which to calculate the error bars.
* monteCarlo  :  MonteCarlo
<br>&nbsp;&nbsp;&nbsp;&nbsp; a ready-made MonteCarlo class.


<a name="getScale"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getScale(</strong> )
</th></tr></thead></table>
<b>Return</b>

* float  :  the noise scale
<br>&nbsp;&nbsp;&nbsp;&nbsp; scale = sqrt( chisq / DOF )

<b>Raise</b>

RuntimeError when DoF <= 0. The number of (weighted) datapoints is too small.


<a name="getEvidence"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getEvidence(</strong> limits=None, noiseLimits=None )
</th></tr></thead></table>
Calculation of the evidence, log10( Z ), for the model given the data.

&nbsp;&nbsp;&nbsp;&nbsp; E = log10( P( Model | data ) )

The calculation of the evidence uses a Gaussion approximation of the Posterior
probability.
It needs to know the limits of the parameters (and the noise scale if applicable),
either from the priors in the model or from keywords "limits/noiseLimits".


<b>Parameters</b>

* limits  :  list of 2 floats/array_likes
<br>&nbsp;&nbsp;&nbsp;&nbsp; possible range of the parameters. ( [low,high] )
* noiseLimits  :  list of 2 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; possible range on noise scale ( [low,high] )

<b>Raises</b>

ValueError when no Prior is available


<a name="getLogLikelihood"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLogLikelihood(</strong> autoscale=False, var=1.0 ) 
</th></tr></thead></table>
Return the log likelihood.

It is implementing eq 19/20 last parts (Kester 2002) term by term

<b>Parameters</b>

* autoscale  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; whether the noise scale is optimized too
* var  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; variance

<a name="getLogZ"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLogZ(</strong> limits=None, noiseLimits=None )
</th></tr></thead></table>
Calculation of the evidence, log( Z ), for the model given the data.

&nbsp;&nbsp;&nbsp;&nbsp; logZ = log( P( Model | data ) )

The calculation of the evidence uses a Gaussion approximation of the Posterior
probability.
It needs to know the limits of the parameters (and the noise scale if applicable),
either from the priors in the model or from keywords "limits/noiseLimits".


<b>Parameters</b>

* limits  :  list of 2 floats/array_likes
<br>&nbsp;&nbsp;&nbsp;&nbsp; possible range of the parameters. ( [low,high] )
* noiseLimits  :  list of 2 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; possible range on noise scale ( [low,high] )

<b>Raises</b>

ValueError when no Prior is available

RuntimeError when DoF <= 0. The number of (weighted) datapoints is too small.


<a name="plotResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotResult(</strong> xdata=None, ydata=None, model=None, residuals=True,
 confidence=False, show=True ) 
</th></tr></thead></table>
Plot the results of the fit.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; xdata of the problem
* ydata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; ydata of the problem
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model the ydata are fitted to at xdata.
* residuals  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; plot the residuals in a separate panel.
* confidence  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; plot confidence region
* show  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; display the plot.

