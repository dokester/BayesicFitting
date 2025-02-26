---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/AmoebaFitter.py target=_blank>Source</a></span></div>

<a name="AmoebaFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class AmoebaFitter(</strong> <a href="./MaxLikelihoodFitter.html">MaxLikelihoodFitter</a> )
</th></tr></thead></table>
<p>

Fitter using the simulated annealing simplex minimum finding algorithm,

See also: [AnnealingAmoeba](./AnnealingAmoeba.md)

Author       Do Kester

<b>Examples</b>

    # assume x and y are Double1d data arrays.
    x = numpy.arange( 100, dtype=float ) / 10
    y = 3.5 * SIN( x + 0.4 )                    # make sine
    numpy.random.seed( 12345L )                 # Gaussian random number generator
    y += numpy.random.randn( 100 ) * 0.2        # add noise
    sine = SineModel( )                         # sinusiodal model
    lolim = numpy.asarray( [1,-10,-10], dtype=float )
    hilim = numpy.asarray( [100,10,10], dtype=float )
    sine.setLimits( lolim, hilim )              # set limits on the model parameters
    amfit = AmoebaFitter( x, sine )
    param = amfit.fit( y, temp=10 )
    stdev = amfit.getStandardDeviation( )       # stdevs on the parameters
    chisq = amfit.getChiSquared( )
    scale = amfit.getScale( )                 # noise scale
    yfit  = amfit.getResult( )                # fitted values
    yfit  = sine( x )                         # fitted values ( same as previous )
    yband = amfit.monteCarloError( )               # 1 sigma confidence region
    # for diagnostics ( or just for fun )
    amfit = AmoebaFitter( x, sine )
    amfit.setTemperature( 10 )                # set a temperature to escape local minima
    amfit.setVerbose( 10 )                    # report every 10th iteration
    plotter = IterationPlotter( )             # from BayesicFitting
    amfit.setPlotter( plotter, 20 )            # make a plot every 20th iteration
    param = amfit.fit( y )


<b>Notes</b>

1. AmoebaFitter is not guaranteed to find the global minimum.
2. The calculation of the evidence is an Gaussian approximation which is
only exact for linear models with a fixed scale.

* Author  :  Do Kester.<br>


<a name="AmoebaFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>AmoebaFitter(</strong> xdata, model, **kwargs )
</th></tr></thead></table>
<p>

Create a new Amoeba class, providing inputs and model.

<b>Parameters</b>

* xdata  :  array_like<br>
    independent input values
* model  :  Model<br>
    the model function to be fitted
* kwargs  :  dict<br>
    Possibly includes keywords from
        MaxLikelihoodFitter :   errdis, scale, power
        IterativeFitter :       maxIter, tolerance, verbose
        BaseFitter :            map, keep, fixedScale


<a name="fit"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>fit(</strong> data, weights=None, par0=None, keep=None, size=None,
 seed=4567, temp=0, limits=None, maxiter=1000,
 tolerance=0.0001, cooling=0.95, steps=10,
 verbose=0, plot=False, accuracy=None, callback=None )
</th></tr></thead></table>
<p>

Return Model fitted to the data array.

When done, it also calculates the hessian matrix and chisq.

<b>Parameters</b>

* data  :  array_like<br>
     the data vector to be fitted
* weights  :  array_like<br>
    weights pertaining to the data
    The weights are relative weights unless `scale` is set.
* accuracy  :  float or array_like<br>
    accuracy of (individual) data
* par0  :  array_like<br>
    initial values of teh parameters of the model
    default: from model
* keep  :  dict of {int:float}<br>
    dictionary of indices (int) to be kept at a fixed value (float)
    The values of keep are only valid for *this* fit
    See also `AmoebaFitter( ..., keep=dict )`
* size  :  float or array_like<br>
    step size of the simplex
* seed  :  int<br>
    for random number generator
* temp  :  float<br>
    temperature of annealing (0 is no annealing)
* limits  :  None or list of 2 floats or list of 2 array_like<br>
    None : no limits applied
    [lo,hi] : low and high limits for all values
    [la,ha] : low array and high array limits for the values
* maxiter  :  int<br>
    max number of iterations
* tolerance  :  float<br>
    stops when ( |hi-lo| / (|hi|+|lo|) ) < tolerance
* cooling  :  float<br>
    cooling factor when annealing
* steps  :  int<br>
    number of cycles in each cooling step.
* verbose  :  int<br>
    0 : silent
    1 : print results to output
    2 : print some info every 100 iterations
    3 : print some info all iterations
* plot  :  bool<br>
    plot the results.
* callback  :  callable<br>
    is called each iteration as
    `val = callback( val )`
    where `val` is the minimizable array


<table><thead style="background-color:#FFD0D0; width:100%"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./MaxLikelihoodFitter.html">MaxLikelihoodFitter</a></th></tr></thead></table>


* [<strong>makeFuncs(</strong> data, weights=None, index=None, ret=3 ) ](./MaxLikelihoodFitter.md#makeFuncs)
* [<strong>getScale(</strong> ) ](./MaxLikelihoodFitter.md#getScale)
* [<strong>getLogLikelihood(</strong> autoscale=False, var=1.0 ) ](./MaxLikelihoodFitter.md#getLogLikelihood)
* [<strong>normalize(</strong> normdfdp, normdata, weight=1.0 ) ](./MaxLikelihoodFitter.md#normalize)
* [<strong>testGradient(</strong> par, at, data, weights=None )](./MaxLikelihoodFitter.md#testGradient)


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
* [<strong>getDesign(</strong> params=None, xdata=None, index=None )](./BaseFitter.md#getDesign)
* [<strong>chiSquared(</strong> ydata, params=None, weights=None )](./BaseFitter.md#chiSquared)
* [<strong>getStandardDeviations(</strong> )](./BaseFitter.md#getStandardDeviations)
* [<strong>monteCarloError(</strong> xdata=None, monteCarlo=None)](./BaseFitter.md#monteCarloError)
* [<strong>getEvidence(</strong> limits=None, noiseLimits=None )](./BaseFitter.md#getEvidence)
* [<strong>getLogZ(</strong> limits=None, noiseLimits=None )](./BaseFitter.md#getLogZ)
* [<strong>plotResult(</strong> xdata=None, ydata=None, model=None, residuals=True,](./BaseFitter.md#plotResult)
