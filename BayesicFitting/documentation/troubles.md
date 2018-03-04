
## Restrictions and Trouble Shooting.

**All the math is OK, computation is the nightmare.**


Although the theory of model fitting is quite straightforward, the
implementation can be cumbersome. This is mostly due to the fact that we
have limited precision computers and limited amounts of time. Even
though all the computation is done in 8-byte floats, limited resources
and sometimes the obnoxious shape of the &chi;<sup>2</sup>-landscape can
make life for the fitter difficult. Another common bear on the road is
the (near-)degeneracy in the model with respect to the data.
It sometimes looks more like an art than a craft. 

For diagnostic (and debugging) purposes in the iterative fitters there
is the `verbose` option, which prints increasingly more information for
higher values.

It is also a good idea to visually inspect the results of the fit. All
fitters have a method `fitter.plotResult( xdata, ydata, model )`.

Here are some guidelines that might help to get usefull results.

+ **Constraints on the independent variable(s)**<br>
The independent variable(s) (x) should be nice numbers, ie. roughly of
order 1. Mostly the fitter obtains solutions by manipulating a matrix
consisting of a direct product of the partial derivatives of the model
to each of its parameters. If the elements of this matrix wildly vary in
size, loss of precision is quickly attained. <br>
E.g. a polynomial model of order 3 with an independent variable which
has values from 1 to 100, will have a matrix with values ranging between
1 and 10<sup>12</sup>. Mathematically this is all OK, computation ...<br>
The Fitter software can not and does not scale its inputs in any way. It
takes it all at face value. It is upto the user to present the Fitters
with usable data. 

+ **Constraints on the dependent variable**<br>
The dependent variable (y) has less constraints. Still there is a silent
assumption in the algorithms that the amount of noise in the data is of
the order 1. This is only of importance in the stopping criterion of
iterative fitters. There is no way to do it right in all imaginable
cases. <br>
To redress this condition you can either use weights 
or use the setTolerance() method to adapt the stopping 
criterion to your problem or scale the dependent variable such that 
the noise level attains a more usefull value. <br>
Check whether &chi;<sup>2</sup> is of the order of the
number of datapoints. 

+ **Model Degeneracy**<br>
Sometimes the model is degenerated, meaning that 2 (or more) of its 
parameters are essentially measuring the same thing. 
Trying to fit data using Fitter to such a model results in a singular matrix.
The SingularValueDecompositionFitter has less problems as it evenly 
distributes the value over the degenerated parameters. 
Try hasDegeneracy() to check for this condition.<br>
In general it is better to use models which are not degenerated.   

+ **(Nonlinear)Fitter does not find the minimum.**<br>
When a non-linear fitter searches for a minimum, it migh happen that for
almost all values of the parameters &chi;<sup>2</sup> does not have a
gradient. That is when the parameters move away from the sought minimum,
the &chi;<sup>2</sup> does not or hardly change. Mostly this can be the
case with models of periodic functions or when you are far from the
global minimum. Only at a small  area in the parameters space around the
minimum there is a gradient to  move along.<br>
A similar and sometimes simultaneous condition happens when
the landscape is multimodal, i.e. it has more than one minimum. Of
course only one minimum is the lowest, the global minimum. And that one
is the one we want to find. In general fitters don't have a global view
on the &chi;<sup>2</sup> landscape. They fall for the first minimum they
encounter. <br>
If you can in some other way localise the area where your parameters
should be found, feed them to the system as initial parameters.
Otherwise you have to use the AmoebaFitter in the annealing mode or even
do exhaustive search. Both strategies take a lot more time.

+ **Nonlinear fitters produce warnings.**<br>
Sometimes a nonlinear fitter produces a division-by-zero warning. When 
the fitter just continues and produces sensible results, the warnings
can be ignored. They are caused by a noise scale equal to 0, when 
calculating the loglikelihood. As +inf is larger than any other number 
the fitter cannot have a minimum there. 

+ **Matrix is degenerate**<br>
The model is (almost) degenerate under the data it is presented to. In
general this signals that the model is not the best one for the data at
hand. Use a simpler model.

+ **AmoebaFitter does not start.**<br>
The size of the Simplex in the AmoebaFitter is by default 1.  When your
x-data is  very much larger (or smaller) than 1 and you set your
startValues accordingly,  you might want to adapt the size of the
Simplex too.  In extreme cases the 1 vanishes in the precision of the
startValues and the  simplex is frozen in some dimension(s). Use
setSimplex( startValues, sizeSimplex ).

+ **&chi;<sup>2</sup> is zero.**<br>
This can only happen when the data fit the
model perfectly. And as true perfection is not given to us it often is
the result of something else e.g. digitization of the data: the data is
only perfect after they have been digitized. 
This digitization gives each data point 
a noise of 1/sqrt(12), the standard deviation of a uniform distribution. 
The actual position of each datapoint can be anywhere between two
digitization levels (presumably at distance 1). 
This noise can be added to the internal &chi;<sup>2</sup> with 
setChiSquared( N/12 ).

+ **Standard deviations seem too large.**<br>
When you think that the standard deviations on the parameters are 
ridiculously large, please calculate the confidence region on the model fit 
(use fitter.monteCarloError()). This 1-&sigma; confidence interval is obtained 
directly from the standard deviation and its covariance matrix. Due to strong 
covariance between the parameters, the standard deviations can be large 
while the confidence region is still acceptable. <br>
The confidence region is actually is better indicator for how well the model
performs than the standard deviations on the parameters.  

+ **Parameters at the edge**<br>
The standard deviations of the parameters are calculated as the
square root of chisq multiplied by the diagonal elements of the inverse
Hessian matrix at the chisq minimum, divided by the degrees of freedom.
The chisq landscape at that point is a stationary minimum, curving up in
all directions. The shape of the minimum is approximated by the inverse
Hessian (also known as Covariance Matrix), upto the 2nd power in the
Taylor expansion of the chisq function.<br>
When you have set limits on the parameters and the unconstraint minimum
of chisq would be outside the limits, then the constraint minimum of
chisq is at one of the limits. This constraint minimum is not a
stationary point any more so the assumptions above about a neat valley
in the chisq landscape, curving up to all sides are not met.
What the resulting calculations will give is anyones guess. 

