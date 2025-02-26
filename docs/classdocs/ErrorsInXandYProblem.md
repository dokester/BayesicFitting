---
---
<br><br><br>

<a name="ErrorsInXandYProblem"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class ErrorsInXandYProblem(</strong> <a href="./Problem.html">Problem</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ErrorsInXandYProblem.py target=_blank>Source</a></th></tr></thead></table>
<p>

A ErrorsInXandYProblem is an optimization of parameters which involves
the fitting of data to a Model, where both the ydata and the xdata
contain errors.

It entails that the xdata are not at the exact locations. They need to
be optimized too. Consequently the parameters of the model are appended
with a set of parameters, the length of xdata. These extra parameters
will contain the target locations of the xdata. The 2-dimensional distance
between data (xdata,ydata) and (target, model(target)) is minimised.
The target are nuisance parameters which are not part of the modeling
solution.

Define
    xd = xdata, yd = ydata, u = target, F(u:P) = model( target )<br>
And the mismathes in both directions.
    X = u - xd <br>
    Y = F(u:p) - yd<br>

Both distances need to be minimized, possibly in the presence of a correlation 
between the mismatches X and Y 

As the targets need to be optimised they need a Prior. In the present
implementation there is the same Prior for all targets, which the centered on
each of the xdata values.
S.Gull (1989) argues to use a GaussPrior with a scale similar to the errors
in both X and Y.

<b>Attributes</b>

* prior  :  Prior<br>
    Priors for the x-axis nuisance parameters.<br>
* varxx  :  float or ndarray of shape (ndata,)<br>
    Variance in the xdata errors<br>
* varyy  :  float or ndarray of shape (ndata,)<br>
    Variance in the ydata errors<br>
* varxy  :  float or ndarray of shape (ndata,)<br>
    Covariance in the xdata and ydata errors<br>



<b>Attributes from Problem</b>

model, xdata, ydata, weights, partype


* Author  :          Do Kester<br>


<a name="ErrorsInXandYProblem"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>ErrorsInXandYProblem(</strong> model=None, xdata=None, ydata=None, weights=None,
 prior=None, covar=None, accuracy=None, copy=None )
</th></tr></thead></table>
<p>

Problem Constructor.

<b>Parameters</b>

* model  :  Model<br>
    the model to be solved<br>
* xdata  :  array_like or None<br>
    independent variable<br>
* ydata  :  array_like or None<br>
    dependent variable<br>
* weights  :  array_like or None<br>
    weights associated with data<br>
* covar  :  ndarray of shape (2,2) or (ndata,2,2)<br>
    covariance matrix of the errors in x and y<br>
    (2,2) : valid for all datapoints<br>
    (ndata,2,2): one for each datpoint<br>
    Default is [[1,0],[0,1]]<br>
* accuracy  :  ndarray of shape (2,) or (3,) or (ndata,2) or (ndata,3)<br>
    accuracy scale for the datapoints<br>
    (2,) scale for resp. y and x, valid for all datapoints<br>
    (3,) scale for y and y, and correlation coefficient between y and x, valid for all<br>
    (ndata,2) or (ndata,3) one set of values for each datapoint<br>
    Alternative for covarince matrix. <br>
    covar = [[ acc[0]^2, 0], [0, acc[1]^2]] no correlation<br>
          = [[ acc[0]^2, r], [r, acc[1]^2]] where r = acc[0] * acc[1] * acc[2]<br>
    accuracy is converted to covar; default is covar.<br>
* prior  :  Prior<br>
    prior for the x-axis nuisance parameters. All centered on each of the xdata<br>
* copy  :  Problem<br>
    to be copied<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>

Copy.


<a name="setAccuracy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setAccuracy(</strong> accuracy=None, covar=None ) 
</th></tr></thead></table>
<p>

Store 3 items from the covar matrix : 

    | var_yy, var_xy |<br>
    | var_xy, var_xx |<br>

When the accuracy is given, convert it to these items by
var_yy = acc[0] * acc[0]
var_xx = acc[1] * acc[1]
var_xy = acc[0] * acc[1] * acc[2]

Store also the determinant of the covariance matrix. 

When both accuracy and covar are None
  var_yy = 0 <br>
  var_xx = 1<br>
  var_xy = 0<br>

<b>Raises</b>

AttributeError. When both accuracy and covar are not None.

<b>Parameters</b>

* accuracy  :  ndarray of shape (2,) or (3,) or (ndata,2) or (ndata,3)<br>
    accuracy scale for the datapoints<br>
    (2,) scale for resp. y and x, valid for all datapoints<br>
    (3,) scale for y and y, and correlation coefficient between y and x, valid for all<br>
    (ndata,2) or (ndata,3) one set of values for each datapoint<br>
    Alternative for covarince matrix. <br>
    vxy = 0 if no correlation else acc[0] * acc[1] * acc[2]<br>
    covar = [[ acc[0]^2, vxy      ],<br>
             [ vxy     , acc[1]^2 ]] <br>
    accuracy is converted to covar; default is covar.<br>
* covar  :  ndarray of shape (2,2) or (ndata,2,2) or None<br>
    covariance matrix of the errors in x and y<br>


<a name="hasWeights"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasWeights(</strong> )
</th></tr></thead></table>
<p>
Return whether it has weights. 

<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> param )
</th></tr></thead></table>
<p>

Returns the result calculated at the xdatas.

<b>Parameters</b>

* param  :  array_like<br>
    values for the parameters + nuisance params.<br>


<a name="splitParam"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>splitParam(</strong> param ) 
</th></tr></thead></table>
<p>

Split the parameters into Model parameters and targets.

<b>Parameters</b>

* param  :  array_like<br>
    values for the parameters + nuisance params.<br>

<b>Return</b>

tuple of ( targets, model parameters )


<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> param ) 
</th></tr></thead></table>
<p>

Return the partials as a matrix [2*nx,np+nx], where nx is the number of
datapoints and np the number of parameters in the model.

    The upper left submatrix (nx,np) contains dM/dp<br>
    the upper right submatrix (nx,nx) contains dM/dx on the diagonal<br>
    the lower left submatrix (nx,np) contains zeros<br>
    the lower right submatrix (nx,nx) contains the identity matrix<br>

<b>Parameters</b>

* param  :  array_like<br>
    values for the parameters + nuisance params.<br>


<a name="derivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>derivative(</strong> param ) 
</th></tr></thead></table>
<p>

Return the derivative to the Model.

<b>Parameters</b>

* params  :  array_like<br>
    list of problem parameters

<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> dval, kpar ) 
</th></tr></thead></table>
<p>

Return value in [0,1] for the selected parameter.

<b>Parameters</b>

* dval  :  float<br>
    domain value for the selected parameter<br>
* kpar  :  int<br>
    selected parameter index, where kp is index in [parameters, hyperparams]

<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> uval, kpar ) 
</th></tr></thead></table>
<p>

Return domain value for the selected parameter.

<b>Parameters</b>

* uval  :  array_like<br>
    unit value for the selected parameter<br>
* kpar  :  int<br>
    selected parameter indices, where kp is index in [parameters, hyperparams]

<a name="getXYresiduals"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getXYresiduals(</strong> param ) 
</th></tr></thead></table>
<p>

Return residuals in y-direction and x-direction.

<b>Parameters</b>

* param  :  array_like<br>
    model parameters and xdata parameters<br>

<b>Returns</b>

tuple of (y residuals, x residuals)

<a name="weightedResSq"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>weightedResSq(</strong> allpars, mockdata=None, extra=False ) 
</th></tr></thead></table>
<p>

Return the (weighted) squared distance between (xdata,ydata) and (xtry,ytry) where xtry are
the trial values for xdata and ytry = model.result( xtry, param )

<b>Parameters</b>

* allpars  :  array_like<br>
    model parameters, xdata parameters, and noise scale<br>
* mockdata  :  array_like<br>
    model fit data model.result( xtry, param )<br>
* extra  :  bool (False)<br>
    true  : return ( wgt * res^2, wgt * [yres,xres] )<br>
    false : return wgt * res^2

<a name="myEngines"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>myEngines(</strong> ) 
</th></tr></thead></table>
<p>

Return a default list of preferred engines

<a name="myStartEngine"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>myStartEngine(</strong> ) 
</th></tr></thead></table>
<p>

Return a default preferred start engines: "start"

<a name="myDistribution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>myDistribution(</strong> ) 
</th></tr></thead></table>
<p>

Return a default preferred ErrorDistribution: "gauss2d"

<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>
<p>
Returns a string representation of the model. 

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Problem.html">Problem</a></th></tr></thead></table>


* [<strong>residuals(</strong> param, mockdata=None ) ](./Problem.md#residuals)
* [<strong>cyclicCorrection(</strong> res )](./Problem.md#cyclicCorrection)
* [<strong>cycor1(</strong> res )](./Problem.md#cycor1)
* [<strong>cycor2(</strong> res )](./Problem.md#cycor2)
* [<strong>cyclize(</strong> res, period ) ](./Problem.md#cyclize)
* [<strong>XXXweightedResiduals(</strong> param, mockdata=None, extra=False ) ](./Problem.md#XXXweightedResiduals)
* [<strong>isDynamic(</strong> ) ](./Problem.md#isDynamic)
* [<strong>shortName(</strong> ) ](./Problem.md#shortName)
