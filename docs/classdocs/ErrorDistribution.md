---
---
<br><br>

<a name="ErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class ErrorDistribution(</strong> object )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source// target=_blank>[source]</a></th></tr></thead></table>
<p>

ErrorDistribution defines general methods for a error distribution.

Error distributions are used to calculate the likelihoods.

Author       Do Kester.

<b>Attributes</b>

* hyperpar  :  HyperParameter
<br>&nbsp;&nbsp;&nbsp;&nbsp; hyperparameter for the error distribution
* deltaP  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; delta for calculating numerical derivatives
* ncalls  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of calls to the logLikelihood
* nparts  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of calls to the partial of the logLikelihood
* sumweight  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; sum over the weights or ndata
* ndata  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of points in data
* hypar  :  [float]
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of values for the hyperparameters
* nphypar  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of hyper parameters in this error distribution
* constrain  :  None or callable
<br>&nbsp;&nbsp;&nbsp;&nbsp; None:     Use logLikelihood as is
<br>&nbsp;&nbsp;&nbsp;&nbsp; callable: logL = func( logL, problem, allpars, lowLhood )
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; returning a (modified) value of the logLikelihood.

<a name="ErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>ErrorDistribution(</strong> fixed=None, constrain=None, copy=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L76-L111 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

<b>Parameters</b>

* fixed  :  dictionary of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; int     list if parameters to fix permanently. Default None.
<br>&nbsp;&nbsp;&nbsp;&nbsp; float   list of values for the fixed parameters.
* constrain  :  None or callable
<br>&nbsp;&nbsp;&nbsp;&nbsp; function as: func( logL, problem, allpars, lowLhood )
<br>&nbsp;&nbsp;&nbsp;&nbsp; returning a (modified) value of the logLikelihood.
* copy  :  ErrorDistribution
<br>&nbsp;&nbsp;&nbsp;&nbsp; distribution to be copied.

<b>Raise</b>

ValueError when constrain is not a callable method.


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L113-L162 target=_blank>[source]</a></th></tr></thead></table>

Return copy of this. 
<a name="getGaussianScale"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getGaussianScale(</strong> problem, allpars=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L164-L180 target=_blank>[source]</a></th></tr></thead></table>
Return the noise scale.

*** Gaussian approximation ***

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; None take parameters from problem.model
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem

<a name="getResiduals"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getResiduals(</strong> problem, allpars=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L182-L203 target=_blank>[source]</a></th></tr></thead></table>
Return residuals: ydata - model.result

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; None take parameters from problem.model
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem

<a name="getChisq"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getChisq(</strong> problem, allpars=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L205-L229 target=_blank>[source]</a></th></tr></thead></table>
Return chisq

*** Gaussian approximation ***

Sum over the (weighted) squared residuals

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; None take parameters from problem.model
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of all parameters in the problem

<a name="toSigma"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>toSigma(</strong> scale ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L231-L242 target=_blank>[source]</a></th></tr></thead></table>
Return sigma, the squareroot of the variance.

<b>Parameter</b>

* scale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the scale of this distribution.

Return default value : scale

<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBound(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L244-L255 target=_blank>[source]</a></th></tr></thead></table>
True when all priors of its (hyper)parameters are bound

<a name="acceptWeight"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>acceptWeight(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L257-L259 target=_blank>[source]</a></th></tr></thead></table>

True if the distribution accepts weights. 
<a name="keepFixed"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>keepFixed(</strong> fixed=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L261-L289 target=_blank>[source]</a></th></tr></thead></table>
Keeps (hyper)parameters fixed at the provided values.

1. Repeated calls start from scratch.<br>
2. Reset with keepFixed( fixed=None )

<b>Parameters</b>

* fixed  :  dictionary of {int:float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; int     list if parameters to fix permanently. Default None.
<br>&nbsp;&nbsp;&nbsp;&nbsp; float   list of values for the fixed parameters.

<a name="setPriors"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setPriors(</strong> priors ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L291-L301 target=_blank>[source]</a></th></tr></thead></table>
Set priors on the hyper parameter(s).

<b>Parameters</b>

* priors   :  (list of) Prior
<br>&nbsp;&nbsp;&nbsp;&nbsp; prior distribution for the hyperparameters

<a name="setLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setLimits(</strong> limits ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L303-L321 target=_blank>[source]</a></th></tr></thead></table>
Set limits on the hyper parameter(s).

<b>Parameters</b>

* limits  :  [low,high]
<br>&nbsp;&nbsp;&nbsp;&nbsp; low : float or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; low limits
<br>&nbsp;&nbsp;&nbsp;&nbsp; high : float or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; high limits

<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> dval, ks ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L323-L338 target=_blank>[source]</a></th></tr></thead></table>
Return value in [0,1] for the selected parameter.

<b>Parameters</b>

* dval  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; hyper parameter value in domain
* ks  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; selecting index

<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> uval, ks ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L340-L357 target=_blank>[source]</a></th></tr></thead></table>
Return domain value for the selected parameter.

<b>Parameters</b>

* uval  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; unit value of hyper parameter
* ks  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; selecting index

<a name="logCLhood"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logCLhood(</strong> problem, allpars )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L359-L377 target=_blank>[source]</a></th></tr></thead></table>
Return the constrained log( likelihood ).

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters of the problem

<a name="logLhood"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logLhood(</strong> problem, allpars )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L379-L393 target=_blank>[source]</a></th></tr></thead></table>
Return the log( likelihood ).

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters of the problem

<a name="partialLogL"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialLogL(</strong> problem, allpars, fitIndex ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L395-L441 target=_blank>[source]</a></th></tr></thead></table>
Return the partial derivative of log( likelihood ) to the parameters.

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters of the problem
* fitIndex  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters to be fitted

try 
<br>&nbsp;&nbsp;&nbsp;&nbsp; pg = self.nextPartialData( problem, allpars, fitIndex, mockdata=mock )
<br>&nbsp;&nbsp;&nbsp;&nbsp; np = len( fitIndex )
<br>&nbsp;&nbsp;&nbsp;&nbsp; dL = numpy.zeros( np, dtype=float )
<br>&nbsp;&nbsp;&nbsp;&nbsp; for k in range( np ) 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; dL[k] = numpy.sum( next( pg ) )
<br>&nbsp;&nbsp;&nbsp;&nbsp; try 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; pg.close()
<br>&nbsp;&nbsp;&nbsp;&nbsp; except Exception 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; pass

&nbsp;&nbsp;&nbsp;&nbsp; return dL
except Exception 
<br>&nbsp;&nbsp;&nbsp;&nbsp; warnings.warn( "Using numeric partialLogL.", UserWarning )

&nbsp;&nbsp;&nbsp;&nbsp; return self.numPartialLogL( problem, allpars, fitIndex )

<a name="partialLogL_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialLogL_alt(</strong> problem, allpars, fitIndex ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L443-L459 target=_blank>[source]</a></th></tr></thead></table>
Return the partial derivative of log( likelihood ) to the parameters.

Alternative calculation.

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters of the problem
* fitIndex  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters to be fitted


<a name="numPartialLogL"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>numPartialLogL(</strong> problem, allpars, fitIndex ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L461-L489 target=_blank>[source]</a></th></tr></thead></table>
Return d log( likelihood ) / dp, numerically calculated.

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* allpars  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters of the problem
* fitIndex  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters to be fitted


<a name="updateLogL"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>updateLogL(</strong> problem, allpars, parval=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L491-L515 target=_blank>[source]</a></th></tr></thead></table>
Return a update of the log( likelihood ) given a change in a few parameter.

This method provides the opportunity to optimize the logL calculation.
Providing this one, automatically provides the previous one.
For now it just refers to logLikelihood() itself.

<b>Parameters</b>

* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be solved
* param  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters of the model
* parval  :  dict of {int : float}
<br>&nbsp;&nbsp;&nbsp;&nbsp; int index of a parameter
<br>&nbsp;&nbsp;&nbsp;&nbsp; float (old) value of the parameter

<a name="hyparname"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hyparname(</strong> k ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L517-L527 target=_blank>[source]</a></th></tr></thead></table>
Return name of the hyperparameter

<b>Parameters</b>

* k  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index of the hyperparameter

