---
---
<p>

<a name="AmoebaFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class AmoebaFitter(</strong> <a href="./MaxLikelihoodFitter.html">MaxLikelihoodFitter</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/AmoebaFitter.py target=_blank>Source</a></th></tr></thead></table>
<p>

Fitter using the simulated annealing simplex minimum finding algorithm,

See also: [AnnealingAmoeba](./AnnealingAmoeba.md)

Author       Do Kester

<b>Examples</b>

    # assume x and y are Double1d data arrays.<br>
    x = numpy.arange( 100, dtype=float ) / 10<br>
    y = 3.5 * SIN( x + 0.4 )                    # make sine<br>
    numpy.random.seed( 12345L )                 # Gaussian random number generator<br>
    y += numpy.random.randn( 100 ) * 0.2        # add noise<br>
    sine = SineModel( )                         # sinusiodal model<br>
    lolim = numpy.asarray( [1,-10,-10], dtype=float )<br>
    hilim = numpy.asarray( [100,10,10], dtype=float )<br>
    sine.setLimits( lolim, hilim )              # set limits on the model parameters<br>
    amfit = AmoebaFitter( x, sine )<br>
    param = amfit.fit( y, temp=10 )<br>
    stdev = amfit.getStandardDeviation( )       # stdevs on the parameters<br>
    chisq = amfit.getChiSquared( )<br>
    scale = amfit.getScale( )                 # noise scale<br>
    yfit  = amfit.getResult( )                # fitted values<br>
    yfit  = sine( x )                         # fitted values ( same as previous )<br>
    yband = amfit.monteCarloError( )               # 1 sigma confidence region<br>
    # for diagnostics ( or just for fun )<br>
    amfit = AmoebaFitter( x, sine )<br>
    amfit.setTemperature( 10 )                # set a temperature to escape local minima<br>
    amfit.setVerbose( 10 )                    # report every 10th iteration<br>
    plotter = IterationPlotter( )             # from BayesicFitting<br>
    amfit.setPlotter( plotter, 20 )            # make a plot every 20th iteration<br>
    param = amfit.fit( y )<br>


<b>Notes</b>

1. AmoebaFitter is not guaranteed to find the global minimum.
2. The calculation of the evidence is an Gaussian approximation which is
only exact for linear models with a fixed scale.

* Author  :  Do Kester.<br>


<a name="AmoebaFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>AmoebaFitter(</strong> xdata, model, **kwargs )
</th></tr></thead></table>
<p>

Create a new Amoeba class, providing inputs and model.

<b>Parameters</b>

* xdata  :  array_like<br>
    independent input values<br>
* model  :  Model<br>
    the model function to be fitted<br>
* kwargs  :  dict<br>
    Possibly includes keywords from<br>
        MaxLikelihoodFitter :   errdis, scale, power<br>
        IterativeFitter :       maxIter, tolerance, verbose<br>
        BaseFitter :            map, keep, fixedScale<br>


<a name="fit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
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
     the data vector to be fitted<br>
* weights  :  array_like<br>
    weights pertaining to the data<br>
    The weights are relative weights unless `scale` is set.<br>
* accuracy  :  float or array_like<br>
    accuracy of (individual) data<br>
* par0  :  array_like<br>
    initial values of teh parameters of the model<br>
    default: from model<br>
* keep  :  dict of {int:float}<br>
    dictionary of indices (int) to be kept at a fixed value (float)<br>
    The values of keep are only valid for *this* fit<br>
    See also `AmoebaFitter( ..., keep=dict )`<br>
* size  :  float or array_like<br>
    step size of the simplex<br>
* seed  :  int<br>
    for random number generator<br>
* temp  :  float<br>
    temperature of annealing (0 is no annealing)<br>
* limits  :  None or list of 2 floats or list of 2 array_like<br>
    None : no limits applied<br>
    [lo,hi] : low and high limits for all values<br>
    [la,ha] : low array and high array limits for the values<br>
* maxiter  :  int<br>
    max number of iterations<br>
* tolerance  :  float<br>
    stops when ( |hi-lo| / (|hi|+|lo|) ) < tolerance<br>
* cooling  :  float<br>
    cooling factor when annealing<br>
* steps  :  int<br>
    number of cycles in each cooling step.<br>
* verbose  :  int<br>
    0 : silent<br>
    1 : print results to output<br>
    2 : print some info every 100 iterations<br>
    3 : print some info all iterations<br>
* plot  :  bool<br>
    plot the results.<br>
* callback  :  callable<br>
    is called each iteration as<br>
    `val = callback( val )`<br>
    where `val` is the minimizable array<br>


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
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
