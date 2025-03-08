---
---
<br><br>

<a name="MonteCarlo"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class MonteCarlo(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/MonteCarlo.py target=_blank>Source</a></th></tr></thead></table>
<p>

Helper class to calculate the confidence region of a fitted model.

MonteCarlo for models.

The MonteCarlo class is to be used in conjunction with Model classes.

Author:      Do Kester

<b>Attributes</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; array of independent input values<br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model function to be fitted<br>
* mcycles  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; Sets number of cycles in the MonteCarlo procedure to estimate<br>
&nbsp;&nbsp;&nbsp;&nbsp; error bars. Default = 25<br>

<b>Hidden Attributes</b>

* _eigenvectors  :  array_like (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; from eigenvalue decomposition of covariance matrix<br>
* _eigenvalues  :  array_like (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; from eigenvalue decomposition of covariance matrix<br>
* _random  :  random<br>
&nbsp;&nbsp;&nbsp;&nbsp; random number generator<br>


<a name="MonteCarlo"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>MonteCarlo(</strong> xdata, model, covariance, index=None, seed=12345, mcycles=25 )
</th></tr></thead></table>
<p>

Create a new MonteCarlo, providing inputs and model.

A MonteCarlo object is defined by its model and the input vector (the
independent variable). When a fit to another model and/or another
input vector is needed a new object should be created.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; array of independent input values<br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model function to be fitted<br>
* covariance  :  matrix<br>
&nbsp;&nbsp;&nbsp;&nbsp; the covariance matrix of the problem. Default from the Model.<br>
* index  :  list of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; indices of parameters to fit<br>
* seed  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; seed for random number generator<br>
* mcycles  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of cycles in the MonteCarlo procedure to estimate error bars.<br>

<b>Raises</b>

ValueError when model and input have different dimensions


<a name="decompose"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>decompose(</strong> covariance )
</th></tr></thead></table>
<p>
<a name="getError"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getError(</strong> xdata=None )
</th></tr></thead></table>
<p>

Calculates 1 &sigma;-confidence regions on the model given some inputs.

From the full covariance matrix ( = inverse of the Hessian ) random
samples are drawn, which are added to the parameters. With this new
set of parameters the model is calculated. This procedure is done
by default, 25 times.
The standard deviation of the models is returned as the error bar.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; input data over which to calculate the error bars. default provided xdata<br>


<a name="randomVariant"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>randomVariant(</strong> xdata )
</th></tr></thead></table>
<p>

Return a random variant of the model result.
Taking into account the stdev of the parameters and their covariance.

<b>Parameters</b>

* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; input data at these indpendent points<br>


