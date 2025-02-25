---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ErrorDistribution.py target=_blank>Source</a></span></div>

<a name="ErrorDistribution"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class ErrorDistribution(</strong> object )
</th></tr></thead></table>
<p>

ErrorDistribution defines general methods for a error distribution.

Error distributions are used to calculate the likelihoods.

Author       Do Kester.

<b>Attributes</b>

* hyperpar  :  HyperParameter<br>
    hyperparameter for the error distribution<br>
* deltaP  :  float<br>
    delta for calculating numerical derivatives<br>
* ncalls  :  int<br>
    number of calls to the logLikelihood<br>
* nparts  :  int<br>
    number of calls to the partial of the logLikelihood<br>
* sumweight  :  float<br>
    sum over the weights or ndata<br>
* ndata  :  int<br>
    number of points in data<br>
* hypar  :  [float]<br>
    list of values for the hyperparameters<br>
* nphypar  :  int<br>
    number of hyper parameters in this error distribution<br>
* constrain  :  None or callable<br>
    None:     Use logLikelihood as is<br>
    callable: logL = func( logL, problem, allpars, lowLhood )<br>
              returning a (modified) value of the logLikelihood.

<a name="ErrorDistribution"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>ErrorDistribution(</strong> fixed=None, constrain=None, copy=None )
</th></tr></thead></table>
<p>

Constructor.

<b>Parameters</b>

* fixed  :  dictionary of {int:float}<br>
    int     list if parameters to fix permanently. Default None.<br>
    float   list of values for the fixed parameters.<br>
* constrain  :  None or callable<br>
    function as: func( logL, problem, allpars )<br>
    returning a (modified) value of the logLikelihood.<br>
* copy  :  ErrorDistribution<br>
    distribution to be copied.<br>

<b>Raise</b>

ValueError when constrain is not a callable method.


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Return copy of this. 

<a name="getGaussianScale"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>getGaussianScale(</strong> problem, allpars=None ) 
</th></tr></thead></table>
<p>

Return the noise scale.

*** Gaussian approximation ***

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    None take parameters from problem.model<br>
    list of all parameters in the problem

<a name="getResiduals"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>getResiduals(</strong> problem, allpars=None )
</th></tr></thead></table>
<p>

Return residuals: ydata - model.result

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    None take parameters from problem.model<br>
    list of all parameters in the problem

<a name="getChisq"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>getChisq(</strong> problem, allpars=None )
</th></tr></thead></table>
<p>

Return chisq

*** Gaussian approximation ***

Sum over the (weighted) squared residuals

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    None take parameters from problem.model<br>
    list of all parameters in the problem

<a name="toSigma"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>toSigma(</strong> scale ) 
</th></tr></thead></table>
<p>

Return sigma, the squareroot of the variance.

<b>Parameter</b>

* scale  :  float<br>
    the scale of this distribution.<br>

Return default value : scale

<a name="isBound"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>isBound(</strong> ) 
</th></tr></thead></table>
<p>

True when all priors of its (hyper)parameters are bound

<a name="acceptWeight"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>acceptWeight(</strong> )
</th></tr></thead></table>
<p>
True if the distribution accepts weights. 

<a name="keepFixed"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>keepFixed(</strong> fixed=None ) 
</th></tr></thead></table>
<p>

Keeps (hyper)parameters fixed at the provided values.

1. Repeated calls start from scratch.<br>
2. Reset with keepFixed( fixed=None )

<b>Parameters</b>

* fixed  :  dictionary of {int:float}<br>
    int     list if parameters to fix permanently. Default None.<br>
    float   list of values for the fixed parameters.

<a name="setPriors"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>setPriors(</strong> priors ) 
</th></tr></thead></table>
<p>

Set priors on the hyper parameter(s).

<b>Parameters</b>

* priors   :  (list of) Prior<br>
    prior distribution for the hyperparameters

<a name="setLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>setLimits(</strong> limits ) 
</th></tr></thead></table>
<p>

Set limits on the hyper parameter(s).

<b>Parameters</b>

* limits  :  [low,high]<br>
    low : float or array_like<br>
        low limits<br>
    high : float or array_like<br>
        high limits

<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> dval, ks ) 
</th></tr></thead></table>
<p>

Return value in [0,1] for the selected parameter.
<b>Parameters</b>

* dval  :  float<br>
    hyper parameter value in domain<br>
* ks  :  int<br>
    selecting index

<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> uval, ks ) 
</th></tr></thead></table>
<p>

Return domain value for the selected parameter.
<b>Parameters</b>

* uval  :  float<br>
    unit value of hyper parameter<br>
* ks  :  int<br>
    selecting index

<a name="logCLhood"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>logCLhood(</strong> problem, allpars )
</th></tr></thead></table>
<p>

Return the constrained log( likelihood ).

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    parameters of the problem

<a name="logLhood"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>logLhood(</strong> problem, allpars )
</th></tr></thead></table>
<p>

Return the log( likelihood ).

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    parameters of the problem

<a name="partialLogL"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>partialLogL(</strong> problem, allpars, fitIndex ) 
</th></tr></thead></table>
<p>

Return the partial derivative of log( likelihood ) to the parameters.

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    parameters of the problem<br>
* fitIndex  :  array_like<br>
    indices of parameters to be fitted<br>


<a name="partialLogL_alt"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>partialLogL_alt(</strong> problem, allpars, fitIndex ) 
</th></tr></thead></table>
<p>

Return the partial derivative of log( likelihood ) to the parameters.

Alternative calculation.

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    parameters of the problem<br>
* fitIndex  :  array_like<br>
    indices of parameters to be fitted<br>


<a name="numPartialLogL"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>numPartialLogL(</strong> problem, allpars, fitIndex ) 
</th></tr></thead></table>
<p>

Return d log( likelihood ) / dp, numerically calculated.

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* allpars  :  array_like<br>
    parameters of the problem<br>
* fitIndex  :  array_like<br>
    indices of parameters to be fitted<br>


<a name="updateLogL"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>updateLogL(</strong> problem, allpars, parval=None )
</th></tr></thead></table>
<p>

Return a update of the log( likelihood ) given a change in a few parameter.

This method provides the opportunity to optimize the logL calculation.
Providing this one, automatically provides the previous one.
For now it just refers to logLikelihood() itself.

<b>Parameters</b>

* problem  :  Problem<br>
    to be solved<br>
* param  :  array_like<br>
    parameters of the model<br>
* parval  :  dict of {int : float}<br>
    int index of a parameter<br>
    float (old) value of the parameter

<a name="setResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>setResult(</strong> )
</th></tr></thead></table>
<p>
<a name="hyparname"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>hyparname(</strong> k ) 
</th></tr></thead></table>
<p>

Return name of the hyperparameter

<b>Parameters</b>

* k  :  int<br>
    index of the hyperparameter

