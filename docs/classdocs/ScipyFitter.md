---
---
<br><br>

<a name="ScipyFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class ScipyFitter(</strong> <a href="./MaxLikelihoodFitter.html">MaxLikelihoodFitter</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ScipyFitter.py target=_blank>Source</a></th></tr></thead></table>
<p>

Unified interface to the Scipy minimization module minimize, to fit data to a model.

For documentation see scipy.org->Docs->Reference Guide->optimization and root finding.
scipy.optimize.minimize


<b>Examples</b><br>
    # assume x and y are Double1d data arrays.
    x = numpy.arange( 100, dtype=float ) / 10
    y = numpy.arange( 100, dtype=float ) / 122          # make slope
    y += 0.3 * numpy.random.randn( 100 )                # add noise
    y[9:12] += numpy.asarray( [5,10,7], dtype=float )   # make some peak
    gauss = GaussModel( )                               # Gaussian
    gauss += PolynomialModel( 1 )                       # add linear background
    print( gauss.npchain )
    cgfit = ConjugateGradientFitter( x, gauss )
    param = cgfit.fit( y )
    print( len( param ) )
    5
    stdev = cgfit.stdevs
    chisq = cgfit.chisq
    scale = cgfit.scale                                 # noise scale
    yfit  = cgfit.getResult( )                          # fitted values
    yband = cgfit.monteCarloEoor( )                         # 1 sigma confidence region

<b>Notes</b><br>
1. CGF is <b>not</b> guaranteed to find the global minimum.
2. CGF does <b>not</b> work with fixed parameters or limits

<b>Attributes</b><br>
* gradient  :  callable gradient( par )<br>
&nbsp;&nbsp;&nbsp;&nbsp; User provided method to calculate the gradient of chisq.<br>
&nbsp;&nbsp;&nbsp;&nbsp; It can be used to speed up the dotproduct calculation, maybe<br>
&nbsp;&nbsp;&nbsp;&nbsp; because of the sparseness of the partial.<br>
&nbsp;&nbsp;&nbsp;&nbsp; default  dotproduct of the partial with the residuals<br>
* tol  :  float (1.0e-5)<br>
&nbsp;&nbsp;&nbsp;&nbsp; Stop when the norm of the gradient is less than tol.<br>
* norm  :  float (inf)<br>
&nbsp;&nbsp;&nbsp;&nbsp; Order to use for the norm of the gradient (-np.Inf is min, np.Inf is max).<br>
* maxIter  :  int (200*len(par))<br>
&nbsp;&nbsp;&nbsp;&nbsp; Maximum number of iterations<br>
* verbose  :  bool (False)<br>
&nbsp;&nbsp;&nbsp;&nbsp; if True print status at convergence<br>
* debug  :  bool (False)<br>
&nbsp;&nbsp;&nbsp;&nbsp; return the result of each iteration in `vectors`<br>
* yfit  :  ndarray (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; the result of the model at the optimal parameters<br>
* ntrans  :  int (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of function calls<br>
* ngrad  :  int (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of gradient calls<br>
* vectors  :  list of ndarray (read only when debug=True)<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of intermediate vectors<br>

<b>Hidden Attributes</b><br>
* _Chisq  :  class<br>
&nbsp;&nbsp;&nbsp;&nbsp; to calculate chisq in the method Chisq.func() and Chisq.dfunc()<br>

<b>Returns</b><br>
* pars  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; the parameters at the minimum of the function (chisq).<br>


<a name="ScipyFitter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>ScipyFitter(</strong> xdata, model, method=None, gradient=True, hessp=None,
 **kwargs ) 
</th></tr></thead></table>
<p>

Constructor.
Create a class, providing inputs and model.

<b>Parameters</b><br>
* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; array of independent input values<br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; a model function to be fitted (linear or nonlinear)<br>
* method  :  None | 'CG' | 'NELDER-MEAD' | 'POWELL' | 'BFGS' | 'NEWTON-CG' | 'L-BFGS-B' |<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'TNC' | 'COBYLA' | 'SLSQP' | 'DOGLEG' | 'TRUST-NCG'<br>
&nbsp;&nbsp;&nbsp;&nbsp; the method name is case invariant.<br>
&nbsp;&nbsp;&nbsp;&nbsp; None            Automatic selection of the method.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'SLSQP' when the problem has constraints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'L-BFGS-B' when the problem has limits<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'BFGS' otherwise<br>
&nbsp;&nbsp;&nbsp;&nbsp; 'CG'            Conjugate Gradient Method of Polak and Ribiere<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; encapsulates `scipy.optimize.minimize-cg`<br>
&nbsp;&nbsp;&nbsp;&nbsp; 'NELDER-MEAD'   Nelder Mead downhill simplex<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; encapsulates `scipy.optimize.minimize-neldermead`<br>
&nbsp;&nbsp;&nbsp;&nbsp; 'POWELL'        Powell's conjugate direction method<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; encapsulates `scipy.optimize.minimize-powell`<br>
&nbsp;&nbsp;&nbsp;&nbsp; 'BFGS'          Quasi-Newton method of Broyden, Fletcher, Goldfarb, and Shannon<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; encapsulates `scipy.optimize.minimize-bfgs`<br>
&nbsp;&nbsp;&nbsp;&nbsp; 'NEWTON-CG'     Truncated Newton method<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; encapsulates `scipy.optimize.minimize-newtoncg`<br>
&nbsp;&nbsp;&nbsp;&nbsp; 'L-BFGS-B'      Limited Memory Algorithm for Bound Constrained Optimization<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; encapsulates `scipy.optimize.minimize-lbfgsb`<br>
&nbsp;&nbsp;&nbsp;&nbsp; 'TNC'           Truncated Newton method with limits<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; encapsulates `scipy.optimize.minimize-tnc`<br>
&nbsp;&nbsp;&nbsp;&nbsp; 'COBYLA'        Constrained Optimization BY Linear Approximation<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; encapsulates `scipy.optimize.minimize-cobyla`<br>
&nbsp;&nbsp;&nbsp;&nbsp; 'SLSQP'         Sequential Least Squares<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; encapsulates `scipy.optimize.minimize-slsqp`<br>
&nbsp;&nbsp;&nbsp;&nbsp; 'DOGLEG'        Dog-leg trust-region algorithm<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; encapsulates `scipy.optimize.minimize-dogleg`<br>
&nbsp;&nbsp;&nbsp;&nbsp; 'TRUST-NCG'     Newton conjugate gradient trust-region algorithm<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; encapsulates `scipy.optimize.minimize-trustncg`<br>

* gradient  :  bool or None or callable gradient( par )<br>
&nbsp;&nbsp;&nbsp;&nbsp; if True use gradient calculated from model. It is the default.<br>
&nbsp;&nbsp;&nbsp;&nbsp; if False/None dont use gradient (use numeric approximation in stead)<br>
&nbsp;&nbsp;&nbsp;&nbsp; if callable use the method as gradient<br>
* hessp  :  callable hessp(x, p, *args) or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; Function which computes the Hessian times an arbitrary vector, p.<br>
&nbsp;&nbsp;&nbsp;&nbsp; The hessian itself is always provided.<br>
* kwargs  :  dict<br>
&nbsp;&nbsp;&nbsp;&nbsp; Possibly includes keywords from<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; MaxLikelihoodFitter :   errdis, scale, power<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; IterativeFitter :       maxIter, tolerance, verbose<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; BaseFitter :            map, keep, fixedScale<br>


<a name="fit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fit(</strong> data, weights=None, par0=None, keep=None, limits=None,
 maxiter=None, tolerance=None, constraints=(), verbose=0,
 accuracy=None, plot=False, callback=None, **options )
</th></tr></thead></table>
<p>

Return      parameters for the model fitted to the data array.

<b>Parameters</b><br>
* ydata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; the data vector to be fitted<br>
* weights  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights pertaining to the data<br>
* accuracy  :  float or array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; accuracy of (individual) data<br>
* par0  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; initial values of the function. Default from Model.<br>
* keep  :  dict of {int:float}<br>
&nbsp;&nbsp;&nbsp;&nbsp; dictionary of indices (int) to be kept at a fixed value (float)<br>
&nbsp;&nbsp;&nbsp;&nbsp; The values of keep are only valid for *this* fit<br>
&nbsp;&nbsp;&nbsp;&nbsp; See also `ScipyFitter( ..., keep=dict )`<br>
* limits  :  None or list of 2 floats or list of 2 array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; None : no limits applied<br>
&nbsp;&nbsp;&nbsp;&nbsp; [lo,hi] : low and high limits for all values<br>
&nbsp;&nbsp;&nbsp;&nbsp; [la,ha] : low array and high array limits for the values<br>
* constraints  :  list of callables<br>
&nbsp;&nbsp;&nbsp;&nbsp; constraint functions cf. All are subject to cf(par) > 0.<br>

* maxiter  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; max number of iterations<br>
* tolerance  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; stops when ( |hi-lo| / (|hi|+|lo|) ) < tolerance<br>
* verbose  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; 0 : silent<br>
&nbsp;&nbsp;&nbsp;&nbsp; >0 : print output if iter % verbose == 0<br>
* plot  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; Plot the results<br>
* callback  :  callable<br>
&nbsp;&nbsp;&nbsp;&nbsp; is called each iteration as<br>
&nbsp;&nbsp;&nbsp;&nbsp; `val = callback( val )`<br>
&nbsp;&nbsp;&nbsp;&nbsp; where `val` is the minimizable array<br>
* options  :  dict<br>
&nbsp;&nbsp;&nbsp;&nbsp; options to be passed to the method<br>

<b>Raises</b><br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; ConvergenceError if it stops when the tolerance has not yet been reached.<br>


<a name="collectVectors"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>collectVectors(</strong> par ) 
</th></tr></thead></table>
<p>
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./MaxLikelihoodFitter.html">MaxLikelihoodFitter</a></th></tr></thead></table>


* [<strong>makeFuncs(</strong> data, weights=None, index=None, ret=3 ) ](./MaxLikelihoodFitter.md#makeFuncs)
* [<strong>getScale(</strong> ) ](./MaxLikelihoodFitter.md#getScale)
* [<strong>getLogLikelihood(</strong> autoscale=False, var=1.0 ) ](./MaxLikelihoodFitter.md#getLogLikelihood)
* [<strong>normalize(</strong> normdfdp, normdata, weight=1.0 ) ](./MaxLikelihoodFitter.md#normalize)
* [<strong>testGradient(</strong> par, at, data, weights=None )](./MaxLikelihoodFitter.md#testGradient)


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
* [<strong>getDesign(</strong> params=None, xdata=None, index=None )](./BaseFitter.md#getDesign)
* [<strong>chiSquared(</strong> ydata, params=None, weights=None )](./BaseFitter.md#chiSquared)
* [<strong>getStandardDeviations(</strong> )](./BaseFitter.md#getStandardDeviations)
* [<strong>monteCarloError(</strong> xdata=None, monteCarlo=None)](./BaseFitter.md#monteCarloError)
* [<strong>getEvidence(</strong> limits=None, noiseLimits=None )](./BaseFitter.md#getEvidence)
* [<strong>getLogZ(</strong> limits=None, noiseLimits=None )](./BaseFitter.md#getLogZ)
* [<strong>plotResult(</strong> xdata=None, ydata=None, model=None, residuals=True,](./BaseFitter.md#plotResult)
