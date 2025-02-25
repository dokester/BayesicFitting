---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ScipyFitter.py target=_blank>Source</a></span></div>

<a name="ScipyFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class ScipyFitter(</strong> <a href="./MaxLikelihoodFitter.html">MaxLikelihoodFitter</a> )
</th></tr></thead></table>
<p>

Unified interface to the Scipy minimization module minimize, to fit data to a model.

For documentation see scipy.org->Docs->Reference Guide->optimization and root finding.
scipy.optimize.minimize


<b>Examples</b>

# assume x and y are Double1d data arrays.
    x = numpy.arange( 100, dtype=float ) / 10<br>
    y = numpy.arange( 100, dtype=float ) / 122          # make slope<br>
    y += 0.3 * numpy.random.randn( 100 )                # add noise<br>
    y[9:12] += numpy.asarray( [5,10,7], dtype=float )   # make some peak<br>
    gauss = GaussModel( )                               # Gaussian<br>
    gauss += PolynomialModel( 1 )                       # add linear background<br>
    print( gauss.npchain )<br>
    cgfit = ConjugateGradientFitter( x, gauss )<br>
    param = cgfit.fit( y )<br>
    print( len( param ) )<br>
5
    stdev = cgfit.stdevs<br>
    chisq = cgfit.chisq<br>
    scale = cgfit.scale                                 # noise scale<br>
    yfit  = cgfit.getResult( )                          # fitted values<br>
    yband = cgfit.monteCarloEoor( )                         # 1 sigma confidence region<br>

<b>Notes</b>

1. CGF is <b>not</b> guaranteed to find the global minimum.
2. CGF does <b>not</b> work with fixed parameters or limits

<b>Attributes</b>

* gradient  :  callable gradient( par )<br>
    User provided method to calculate the gradient of chisq.<br>
    It can be used to speed up the dotproduct calculation, maybe<br>
    because of the sparseness of the partial.<br>
    default  dotproduct of the partial with the residuals<br>
* tol  :  float (1.0e-5)<br>
    Stop when the norm of the gradient is less than tol.<br>
* norm  :  float (inf)<br>
    Order to use for the norm of the gradient (-np.Inf is min, np.Inf is max).<br>
* maxIter  :  int (200*len(par))<br>
    Maximum number of iterations<br>
* verbose  :  bool (False)<br>
    if True print status at convergence<br>
* debug  :  bool (False)<br>
    return the result of each iteration in `vectors`<br>
* yfit  :  ndarray (read only)<br>
    the result of the model at the optimal parameters<br>
* ntrans  :  int (read only)<br>
    number of function calls<br>
* ngrad  :  int (read only)<br>
    number of gradient calls<br>
* vectors  :  list of ndarray (read only when debug=True)<br>
    list of intermediate vectors<br>

<b>Hidden Attributes</b>

* _Chisq  :  class<br>
    to calculate chisq in the method Chisq.func() and Chisq.dfunc()<br>

<b>Returns</b>

* pars  :  array_like<br>
    the parameters at the minimum of the function (chisq).<br>


<a name="ScipyFitter"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>ScipyFitter(</strong> xdata, model, method=None, gradient=True, hessp=None,
 **kwargs ) 
</th></tr></thead></table>
<p>

Constructor.
Create a class, providing inputs and model.

<b>Parameters</b>

* xdata  :  array_like<br>
    array of independent input values<br>
* model  :  Model<br>
    a model function to be fitted (linear or nonlinear)<br>
* method  :  None | 'CG' | 'NELDER-MEAD' | 'POWELL' | 'BFGS' | 'NEWTON-CG' | 'L-BFGS-B' |<br>
          'TNC' | 'COBYLA' | 'SLSQP' | 'DOGLEG' | 'TRUST-NCG'<br>
    the method name is case invariant.<br>
    None            Automatic selection of the method.<br>
                    'SLSQP' when the problem has constraints<br>
                    'L-BFGS-B' when the problem has limits<br>
                    'BFGS' otherwise<br>
    'CG'            Conjugate Gradient Method of Polak and Ribiere<br>
                    :ref:`(see here) <optimize.minimize-cg>`<br>
    'NELDER-MEAD'   Nelder Mead downhill simplex<br>
                    :ref:`(see here) <optimize.minimize-neldermead>`<br>
    'POWELL'        Powell's conjugate direction method<br>
                    :ref:`(see here) <optimize.minimize-powell>`<br>
    'BFGS'          Quasi-Newton method of Broyden, Fletcher, Goldfarb, and Shannon<br>
                    :ref:`(see here) <optimize.minimize-bfgs>`<br>
    'NEWTON-CG'     Truncated Newton method<br>
                    :ref:`(see here) <optimize.minimize-newtoncg>`<br>
    'L-BFGS-B'      Limited Memory Algorithm for Bound Constrained Optimization<br>
                    :ref:`(see here) <optimize.minimize-lbfgsb>`<br>
    'TNC'           Truncated Newton method with limits<br>
                    :ref:`(see here) <optimize.minimize-tnc>`<br>
    'COBYLA'        Constrained Optimization BY Linear Approximation<br>
                    :ref:`(see here) <optimize.minimize-cobyla>`<br>
    'SLSQP'         Sequential Least Squares<br>
                    :ref:`(see here) <optimize.minimize-slsqp>`<br>
    'DOGLEG'        Dog-leg trust-region algorithm<br>
                    :ref:`(see here) <optimize.minimize-dogleg>`<br>
    'TRUST-NCG'     Newton conjugate gradient trust-region algorithm<br>
                    :ref:`(see here) <optimize.minimize-trustncg>`<br>

* gradient  :  bool or None or callable gradient( par )<br>
    if True use gradient calculated from model. It is the default.<br>
    if False/None dont use gradient (use numeric approximation in stead)<br>
    if callable use the method as gradient<br>
* hessp  :  callable hessp(x, p, *args) or None<br>
    Function which computes the Hessian times an arbitrary vector, p.<br>
    The hessian itself is always provided.<br>
* kwargs  :  dict<br>
    Possibly includes keywords from<br>
        MaxLikelihoodFitter :   errdis, scale, power<br>
        IterativeFitter :       maxIter, tolerance, verbose<br>
        BaseFitter :            map, keep, fixedScale<br>


<a name="fit"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>fit(</strong> data, weights=None, par0=None, keep=None, limits=None,
 maxiter=None, tolerance=None, constraints=(), verbose=0,
 accuracy=None, plot=False, callback=None, **options )
</th></tr></thead></table>
<p>

Return      parameters for the model fitted to the data array.

<b>Parameters</b>

* ydata  :  array_like<br>
    the data vector to be fitted<br>
* weights  :  array_like<br>
    weights pertaining to the data<br>
* accuracy  :  float or array_like<br>
    accuracy of (individual) data<br>
* par0  :  array_like<br>
    initial values of the function. Default from Model.<br>
* keep  :  dict of {int:float}<br>
    dictionary of indices (int) to be kept at a fixed value (float)<br>
    The values of keep are only valid for *this* fit<br>
    See also `ScipyFitter( ..., keep=dict )`<br>
* limits  :  None or list of 2 floats or list of 2 array_like<br>
    None : no limits applied<br>
    [lo,hi] : low and high limits for all values<br>
    [la,ha] : low array and high array limits for the values<br>
* constraints  :  list of callables<br>
    constraint functions cf. All are subject to cf(par) > 0.<br>

* maxiter  :  int<br>
    max number of iterations<br>
* tolerance  :  float<br>
    stops when ( |hi-lo| / (|hi|+|lo|) ) < tolerance<br>
* verbose  :  int<br>
    0 : silent<br>
    >0 : print output if iter % verbose == 0<br>
* plot  :  bool<br>
    Plot the results<br>
* callback  :  callable<br>
    is called each iteration as<br>
    `val = callback( val )`<br>
    where `val` is the minimizable array<br>
* options  :  dict<br>
    options to be passed to the method<br>

<b>Raises</b>

    ConvergenceError if it stops when the tolerance has not yet been reached.<br>


<a name="collectVectors"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>collectVectors(</strong> par ) 
</th></tr></thead></table>
<p>
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
