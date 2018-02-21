<a name="glossary"> </a>
## Glossary 

A list of terms used in this package, with a short explanation. 
The sizes listed at various terms are explained at the end.

<a name="indepvar"></a>
+ **Independent Variable**<br>
The vector(s) of coordinates (locations, times, frequencies or
whatever), at which  the measurements were made. These vector(s) are
known beforehand. Mostly in the ordinary 1 dimensional case this would
be the x-axis when the data were to be plotted. However, more than one
input vector is allowed. Then it becomes a more dimensional
problem.<br>
Size = N if D == 1 else D * N.

<a name="depvar"></a>
+ **Dependent Variable**<br>
The vector of measured datapoints. For the fitterclasses this needs 
to be a 1-dim vector. For fitting maps, cubes or even higher dimensional 
datasets automatic conversion is done to get the dependent and
independent variables in the proper shape.<br>
Size = N.

<a name="weight"></a>
+ **Weight**<br>
A vector of the same shape as the dependent variable representing the weights
of the individual datapoints. Weights by nature are non-negative. <br>
Weights are defined such that a point with weight W is equivalent to having 
W times that same point.<br>
Size = N.

<a name="model"></a>
+ **Model**<br>
The mathematical relationship which is supposed to be present between the 
independent and the dependent variables. The fitting process is a search 
for those model parameters that 
differences between the modelled data and the measured data are minimized.

<a name="param"></a>
+ **Parameter**<br>
The parameters of the model. After fitting they are at the optimal values.<br>
Size = K.

<a name="chisq"></a>
+ **Chisq**<br>
Chisq is the global misfit of the data (D) wrt the model (M): <br>
&chi;<sup>2</sup> = &Sigma; ( D - M )<sup>2</sup> <br>
In least-squares setting, the fitters minimize Chisq to find the optimal 
parameters. 

<a name="lhood"></a>
+ **Likelihood**<br>
The cumulative probability of the data, given the parameters and model.
In practice the log of the likelihood is used as it is a more manageable,
nicer number.<br>
MaxLikelihood fitters search for a (global) maximum in the likelihood 
landscape. At that position, the maximum likelihood solution for the
parameters is found. In case of a Gaussian likelihood, this de ML
solution which is the same as the least squares. 

<a name="stdev"></a>
+ **Standard Deviation**<br>
The standard deviation of the parameters. <br>When the number of data points
increases the standard deviations decrease roughly with a factor sqrt(N).<br>
Size = K.

<a name="noise"></a>
+ **Scale** or **Noise Scale**<br>
The average amount of noise left over when the model with optimized 
parameters has been subtracted. <br>
s = sqrt( &chi;<sup>2</sup> / ( N - K ) ) <br>
Scale will <b>not</b> decrease when the number of datapoints 
increase.

<a name="confidence"></a>
+ **Confidence Region**<br>
The confidence region is the wiggle room of the optiaml solution. 
It is derived via a montecarlo method from the covariance matrix. 

<a name="design"></a>
+ **Design Matrix**<br>
The matrix of the partial derivatives of the model function to each of 
its parameters at every data point. It is also known as the Jacobian 
(matrix).<br>
Size = N * K.

<a name="hessian"></a>
+ **Hessian Matrix**<br>
The inner product of the transpose of the design matrix by itself. <br>
Size = K * K.

<a name="covar"></a>
+ **Covariance Matrix**<br>
The covariance matrix is the inverse of the Hessian matrix multiplied by
the scale squared. The standard deviations are defined as the square
root of the diagonal elements of this matrix.<br>
Size = K * K

<a name="prior"></a>
+ **Prior** or **Prior probability**<br>
The prior is the probability of the parameters (in our case) before 
considering the data.<br>
There is a lot of mumbo-jumbo about priors. They are said to be
subjective and thus (wildly) different, depending on the whim of the
actors. However in real life problems this is not the case. From the 
layout of the problem you are analysing it follows mostly directly 
where parameter can be allowed to go. 
Say if you have data from a spectrometer, then any
frequency derived should be within the measuring domain of the
instrument; fluxes should be above the noise level and below the
saturation etc. My personal rule of thumb is, whenever you start to
frown on the outcome of a parameter it is out of your prior range.

<a name="posterior"></a>
+ **Posterior** or **Posterior probability**<br>
The posterior is the probability of the parameters (in our case) after 
considering the data.<br>
According to Bayes Rule, the joint probability of data and parameters,
given the model:<br>
  joint    = posterior * evidence = likelihood * prior<br>
  P(p,D|M) = P(p|D,M)  * P(D|M)   = P(D|p,M)   * P(p|M)<br>
Where P is probability, p is parameters, D is Data and M is Model.<br>
As the integral of the posterior over the parameter space must be 1.0,
to be a proper probability, the evidence acts as a normalizing constant
of the prior * likelihood.

<a name="evidence"></a>
+ **Evidence**<br>
The integral of the prior * likelihood over the parameter space. It provides
the evidence the data carry for the model. I.e. it tells us how probable
the model is given the data. The number itself does not say anything,
but it can be compared to evidences obtained for other models fitted to 
the same data. If the log evidences of 2 models, a and B, differ by a 
number f, then model P(A/B) = exp( f ).

<a name="information"></a>
+ **Information**<br>
The log of the ratio the space available to the parameters under the prior
probability to the space under the posterior probability. 

The sizes given above are:<br>
D: dimension of the input variable(s).<br>
K: number of parameters in the model.<br>
N: number of data points.<br>


