---
---
<br><br>

<a name="LevenbergMarquardtFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class LevenbergMarquardtFitter(</strong> <a href="./IterativeFitter.html">IterativeFitter</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/LevenbergMarquardtFitter.py target=_blank>Source</a></th></tr></thead></table>
<p>

Non-linear fitter using the Levenberg-Marquardt method.

Implementation of the Levenberg-Marquardt algorithm to fit the parameters
of a non-linear model. It is a gradient fitter which uses partial
derivatives to find the downhill gradient. Consequently it ends in the
first minimum it finds.

The original C-version stems from Numerical Recipes with some additions of my own.
This might be the third or fourth transcription of it.

Author       Do Kester.

<b>Examples</b>

    # assume x and y are Double1d data arrays
    x = numpy.arange( 100, dtype=float ) / 10
    y = numpy.arange( 100, dtype=float ) / 122            # make slope
    rg = RandomGauss( seed=12345L )            # Gaussian random number generator
    y += rg( numpy.asarray( 100, dtype=float ) ) * 0.2            # add noise
    y[Range( 9,12 )] += numpy.asarray( [5,10,7], dtype=float )         # make some peak
    # define a model: GaussModel + background polynomial
    gauss = GaussModel( )                            # Gaussian
    gauss += PolynomialModel( 1 )                    # add linear background
    gauss.setParameters( numpy.asarray( [1,1,0.1,0,0], dtype=float ) )    # initial parameter guess
    print gauss.getNumberOfParameters( )                # 5 ( = 3 for Gauss + 2 for line )
    gauss.keepFixed( numpy.asarray( [2] ), numpy.asarray( [0.1], dtype=float ) )    # keep width fixed at 0.1
    lmfit = LevenbergMarquardtFitter( x, gauss )
    param = lmfit.fit( y )
    print param.length( )                             # 4 ( = 5 - 1 fixed )
    stdev = lmfit.getStandardDeviation( )             # stdevs on the parameters
    chisq = lmfit.getChiSquared( )
    scale = lmfit.getScale( )                         # noise scale
    yfit  = lmfit.getResult( )                        # fitted values
    yband = lmfit.monteCarloError( )                       # 1 sigma confidence region
    # for diagnostics ( or just for fun )
    lmfit = LevenbergMarquardtFitter( x, gauss )
    lmfit.setVerbose( 2 )                             # report every 100th iteration
    plotter = IterationPlotter( )                     # from BayesicFitting
    lmfit.setPlotter( plotter, 20 )                   # make a plot every 20th iteration
    param = lmfit.fit( y )

<b>Notes</b>

In case of problems look at the "Troubles" page in the documentation area.


<b>Limitations</b>

1. LMF is <b>not</b> guaranteed to find the global minimum.
2. The calculation of the evidence is an Gaussian approximation which is
only exact for linear models with a fixed scale.

<b>Attributes</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; vector of numbers as input for model<br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model to be fitted<br>
* lamda  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; to balance the curvature matrix (see Numerical Recipes)<br>


<a name="LevenbergMarquardtFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>LevenbergMarquardtFitter(</strong> xdata, model, **kwargs )
</th></tr></thead></table>
<p>

Create a class, providing xdata and model.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; vector of independent input values<br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; a model function to be fitted<br>

* kwargs  :  dict<br>
&nbsp;&nbsp;&nbsp;&nbsp; Possibly includes keywords from<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; IterativeFitter :       maxIter, tolerance, verbose<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; BaseFitter :            map, keep, fixedScale<br>



<a name="fit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fit(</strong> data, weights=None, par0=None, keep=None, limits=None,
 maxiter=None, tolerance=None, verbose=None, plot=False,
 accuracy=None, callback=None )
</th></tr></thead></table>
<p>

Return Model fitted to the data arrays.

It will calculate the hessian matrix and chisq.

<b>Parameters</b>

* data   :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted<br>
* weights  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights pertaining to the data<br>
* accuracy  :  float or array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; accuracy of (individual) data<br>
* par0  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; initial values for the parameters of the model<br>
&nbsp;&nbsp;&nbsp;&nbsp; default: from model<br>
* keep  :  dict of {int : float}<br>
&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) of parameters to be kept at fixed value (float)<br>
&nbsp;&nbsp;&nbsp;&nbsp; The values of `keep` are only valid for *this* fit<br>
&nbsp;&nbsp;&nbsp;&nbsp; see also `LevenbergMarquardtFitter( ..., keep=dict )<br>
* limits  :  None or list of 2 floats or list of 2 array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; None : no limits applied<br>
&nbsp;&nbsp;&nbsp;&nbsp; [lo,hi] : low and high limits for all values of the parameters<br>
&nbsp;&nbsp;&nbsp;&nbsp; [la,ha] :  arrays of low and high limits for all values of the parameters<br>
* maxiter  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; max number of iterations. default=1000,<br>
* tolerance  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; absolute and relative tolrance. default=0.0001,<br>
* verbose  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; 0 : silent<br>
&nbsp;&nbsp;&nbsp;&nbsp; >0 : more output<br>
&nbsp;&nbsp;&nbsp;&nbsp; default=1<br>
* plot  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; plot the results<br>
* callback  :  callable<br>
&nbsp;&nbsp;&nbsp;&nbsp; is called each iteration as<br>
&nbsp;&nbsp;&nbsp;&nbsp; `val = callback( val )`<br>
&nbsp;&nbsp;&nbsp;&nbsp; where val is the parameter list.<br>

<b>Raises</b>

ConvergenceError if it stops when the tolerance has not yet been reached.


<a name="chiSquaredExtra"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>chiSquaredExtra(</strong> data, params, weights=None ) 
</th></tr></thead></table>
<p>

Add normalizing data to chisq.

<a name="trialfit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>trialfit(</strong> params, fi, data, weights, verbose, maxiter )
</th></tr></thead></table>
<p>
<a name="getParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParameters(</strong> )
</th></tr></thead></table>
<p>

Return status of the fitter: parameters ( for debugging ).

Only for debugging; use Model.getParameters( ) otherwise


<a name="checkLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>checkLimits(</strong> fitpar, fitindex )
</th></tr></thead></table>
<p>



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
