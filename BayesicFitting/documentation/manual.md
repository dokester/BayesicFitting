# BayesicFitting

Bayes enhanched model fitting and evidence calculation.

It is assumed that the reader is familiar with the Bayesian ways to
perform inference from data. If not there are enough books on the market
that explain what it is about. E.g.
[Sivia][1], [Bishop][2], [von der Linden][3] and [Jaynes][4] 

The BayesicFitting toolbox can be used to fit data to a model *and* to 
find the model that fits the data best. The first goal is achieved by
optimizing the parameters of the model in light of the data present. For
the second goal the evidence is calculated, either as a Gaussian
approximation, or in case of NestedSampler by integrating over the 
posterior.

## Contents
1. [Description](#descript)
    + [Models](#models)
    + [Fitters](#fitters)
    + [NestedSampler](#ns)
2. [Usage](#usage)  
    + [Usage Fitter](#usage-fitter)  
    + [Usage NestedSampler](#usage-ns)  
    + [Usage Model](#usage-model)  
3. [Synopsis](#synopsis)  
    + [Models](#synops-model)  
    + [Fitters](#synops-fitter)  
    + [NestedSampler](#synops-ns)  
    + [Kernels](#synops-kernel)  
    + [Miscellaneous](#synops-miscel)  
4. [References](#refs)  

<a name="descript"></a>  
## 1. Description

The toolbox contains over 100 classes. Each class forms an object that
encapsulates several methods. The name of the class is a good
indication of the functionality of the object it generates. E.g.
**PolynomialModel** generates a **Model** object that yields a polynomial of a
selected order, etc. Similarly there are collections of **Fitter**s,
**ErrorDistribution**s, **Prior**s and **Engine**s. 

Each class and all of its methods are fully documented.

The classes can be divided into 3 broad categories **Model**s, **Fitter**s
and classes pertaining to the **NestedSampler**. 

<a name="models"></a>
### Models 

A model is a function of variables and parameters, which together with
its derivatives, parameter values, and other possibly usefull
information are packed into a class. 
**Model**s come into 2 varieties: those that are linear in its
parameters and those that are not. The former have great advantages as
they can be fitted directly to the data; the latter always need an
iterative fitting approach. 

#### Dimensionality.

Most **Model**s are 1-dimensional i.e. they require a 1-dimensional
input vector. Two- or more-dimensional models need 2 or more numbers for
each result it produces. One could think of fitting  maps or cubes. The
results of any model is always a 1-dimensional vector.

Models of different dimensionality cannot be combined in any way.

#### Compound Models.

**Model**s can be combined by various operations (+-*/) into a new
(compound) model. A special operation that can be applied to two models 
is the pipe, indicated by |. It acts just like the (unix) pipe: the
result of the left-hand model is used as input of the right-hand model.
The functional results, derivatives etc. of the
compound model are calculated according to the operations at hand.
Compound models are **Model**s and can be combined with other (compound)
models into a new model. This way quite complicated models can be formed
without worrying about internal consistency. 
See the [gaussfit example](../examples/gaussfit.ipynb).

#### Fixed Models.

Upon construction  of a model the value(s) of one or more parameters can
be fixed.  Either with a constant value, turning the model into one with
less parameters, or with another **Model**. In the latter case the
parameter is changing as the **Model**. Results and derivatives are
constructed from the interacting models. Again such a fixed model is a
**Model** and can be part of a compound model.  
See the [mrs-fringes example](../examples/mrs-fringes.ipynb).

Compound and fixed models are non-linear
unless all its constituents are linear and its operations are additive.

There are several dozens of simple Models inside this toolbox.

#### Brackets

The models in a chain are process, strictly from left to right. There is
no adherence to operation preferences. However, when a compound model is
appended to a chain, the appended model is considered as a single unit.
It get a set of brackets around it. If m1, m2 and m3 are all models,
then 
    m = m1 * m2
    m += m3
is different from
    m = m1
    m *= m2 + m3
The first is processed as ( m1 * m2 ) + m3 while the second is processed
as m1 * ( m2 + m3 ). The brackets are introduced implicitly. Explicit
placement of brackets can be done with **BracketModel**.


<a name="fitters"></a>
### Fitters 

A fitter tries to find the minimum in the &chi;<sup>2</sup> landscape,
cq. the maximum in the likelihood landscape, as a function of the model
parameters. The values for the parameters where the minimum cq. maximum
in the landscape is found are the least-squares solution resp. the
maximum-likelihood solution. If the likelihood is Gaussian the two are
the same. 

#### data.

Data is a one dimensional vector (array) of measured points that are to
be compared with the model. The misfit is minimized when using
&chi;<sup>2</sup>, or the likelihood of the model parameters, given the
data is maximized.

#### Weights.

Up on fitting, weights can be provided as a vector of the same length as
the data vector. 
The behaviour of the fitter is such
that when a point has a weight of n, this is equivalent to a case where that
particular point is present in the dataset n times. This concept is
extended to non-integral values of the weights.<br>
Weights could be derived from the standard deviations in a previous
calculation. In that case the weights should be set to the inverse
squares of the stdevs. However weights do not need to be inverse
variances; they could be derived in any other way. One specially usefull
feature of the use of weights, is that some weights might be set to zero,
causing those points not to contribute at all to the fit.

#### Linear Fitters.

As with **Model**s there are two kinds of **Fitter**s, linear or
non-linear ones for linear and non-linear **Model**s resp. 

The landscape for linear models is monomodal; it has only
one (global) minimum. The linear fitter has generally no problem finding
this minimum in one direct matrix conversion. It is fast and efficient.
This package has 2 linear fitters: **Fitter** and **QRFitter**.

#### Non-linear Fitters.

For non-linear models the landscape can be multimodal, especially for
periodic models.  It can have many minima of which only one is the
deepest. That is the one the fitter should find. Non linear fitters
search for a gradient in the landscape to descend into the valley.
Wherever a minimum is found, most fitters get stuck. There are several
strategies to search the landscape but all of them are iterative. There
is no single best strategy. It depends on the problem and on knowledge
of the starting values for the parameters. This package has a dozen 
non-linear fitters.

#### Evidence.

When an optimal solution for the parameters has been found, a number of
methods, all inherited from **BaseFitter**, are available to calculate
[standard deviations](./glossary.md/#stdev), 
[noise scale](./glossary.md/#noise), 
[&chi;<sup>2</sup>](./glossary.md/#chisq), 
[confidence regions](./glossary.md/#confidence)
and the [evidence](./glossary.md/#evidence). 
Mostly they are derived from the covariance matrix at
the optimal parameter location. The evidence (or more precisely the log
evidence) is calculated as a Gaussian approximation of the posterior,
also called Laplace's method. 
See [example](../examples/harmonicfit.ipynb). 

#### Keep fixed.

The **Fitter**s have the option to keep one or more parameters fixed
during the fitting proces. Contrary to **FixedModel**s the parameters
are not fixed permanently. In a next run of the fitter they can be taken
along in the fit.
See [example](../examples/fix-parameters.ipynb). 

#### Set limits.

TBC. TBD. TBW. It is one of the areas that need more work.

#### Robust fitting.

A special fitter is **RobustShell**. It is a shell around any other
fitter. **RobustShell** iteratively de-weights outlying points. It makes
the fit more robust in the presence of a minority of outliers i.e.
points that should not partake in the fit. The de-weighting process is
governed by one of the [kernels](../source/kernels).


<a name="ns"></a>
### NestedSampler 

**NestedSampler** is a novel technique to do Bayesian calculations. 
It samples the Posterior while integrating it to calculate
the evidence. From the samples, the optimal values for the model
parameters, its standard deviations etc can be calculated.

It applies an ensemble of walkers, initially evenly distributed over the
prior probability. **Engine**s wander the walkers around randomly over
the **Prior**, provided they stay higher than a certain value that
increases with every iteration.  Thus the walkers slowly ascend the
likelihood to the top. 

**NestedSampler** uses a **Prior** for the initial distribution, an
**ErrorDistribution** to calculate the likelihoods.

Nested sampling is an idea of David McKay and John Skilling.

<a name="usage"></a>
## 2. Usage

We first explain how to use a fitter with a simple model, then the same
with **NestedSampler** also using a simple model. Finally we show how to
make more complicated models.
 
<a name="usage-fitter"></a>
### Usage of Fitter

Assume `x` and `y` are some measurement that might be modelled by a
linear relation. Then the simplest way to get the parameters of the
model is:

    from BayesicFitting import PolynomialModel
    from BayesicFitting import Fitter

    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [1.2, 1.3, 1.5, 1.4, 1.4]
    pars = Fitter( x, PolynomialModel( 1 ) ).fit( y )

The `pars` are the parameters of the model. However this is all we can
get from this little script. As we dont have a handle on the fitter, nor
on the model, we cannot request anything else e.g. the standard
deviations, the evidence, or any other interesting property of the fit.

It would be better to write, in stead of the last line:

    model = PolynomialModel( 1 )	# make a first order polynomial
    fitter = Fitter( x, model )	# construct a fitter with this model
    pars = fitter.fit( y )		# fit the data y to the model

This yields the same set of parameters; these parameters are inserted 
into the model. Now we can also ask:

    yfit = model( x )		# the model values at x
    stdev = fitter.stdevs		# standard deviations of the parameters
    scale = fitter.scale		# stdev of remaining noise (= y - yfit) 
    covar = fitter.covariance	# covariance between the parameters

To calculate the evidence (or better the logEvidence) we need a prior
probability on the parameters and on the noise scale. In the context of
the Fitters, the prior on the parameters is the **UniformPrior**, and
on the noise scale it is the **JeffreysPrior**. Both these **Prior**s are
improper, i.e. the integral from -inf to +inf is infinite. So we need
limits, on the parameters prior and on the noise scale prior. 

    logE = fitter.getEvidence( limits=[-10,10], noiseLimits=[0.01,1.0] )

The `logE` is calculated using a Gaussian approximation for the
posterior, also known as Laplace's method.

See [below](#ref-fitter) for a list of available fitters with its
purpose line.

<a name="usage-ns"></a>
### Usage of NestedSampler

needs more information to run. It needs priors for all 
its parameters and it needs a likelihood function. We start off defining
some data.

    from BayesicFitting import GaussModel
    from BayesicFitting import NestedSampler

    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [0.2, 1.3, 4.5, 1.4, 0.1]

Set up the model with limits on the uniform priors of the parameters.

    model = GaussModel()
    lolim = [-10.0, 0.0, 0.0]		# low limits on the params
    hilim = [+10.0, 5.0, 5.0]		# high limits
    model.setLimits( lolim, hilim )		# use UniformPrior with limits

The likelihood is calculated from the **GaussianErrorDistribution**. By
default it has a fixed scale. However in most real cases it is better
to treat the scale as a hyperparameter, which needs a prior,
**JeffreysPrior**, and limits. 

    limits = [0.01, 10]
    ns = NestedSampler( x, model, y, limits=limits )	

We execute the program as

    logE = ns.sample()

where `logE` is the 10log of the evidence. We can now ask optimal
parameters, standard deviations, scale and the optimal fit of the model. 

    param = ns.parameters
    stdev = ns.standardDeviations
    scale = ns.scale
    yfit  = ns.modelfit

The **Sample**s generated are collected in a **SampleList**, from which
numerous items can be extracted.

    slist = ns.samples
    param = slist.parameters		## same as params above
    mlpar = slist.maxLikelihoodParameters

See below for lists of available [**Prior**s](#list-priors),
[**ErrorDistribution**s](#list-errdis), [**Engine**s](#list-engines).

<a name="usage-model"></a>
### Usage of Model

A **Model** is either a simple model, one of the many classes provided in
this toolbox, or a combination of two or more (simple) models. The simple
models we have seen above: **PolynomialModel** or **GaussModel**. 

All simple models have a method `model.result( x, p )`, which calculated
the model function at points `x`, using parameters `p`. They also have
partial derivatives to p (df/dp) called `model.partial( x, p )` and
derivatives to x (df/dx), called `model.derivative( x, p )`. The model
itself has a name, as do all parameters. One or more of its parameters
can be permanently (ie. for the lifetime of the object) fixed at a
chosen value or replaced by another model. The latter option can produce 
quite sophisticated simple models.

    em1 = EtalonModel( fixed={0:1.0} )

Standardly the **EtalonModel** has 4 parameters: amplitude, finesse, 
period and phase. Here we have fixed the amplitude (parameter 0) at the
value 1.0. The model, em1,  had 3 parameters to be fitted. If we want a slowly
changing finesse too, we define

    pm = PolynomialModel( 1 )
    em2 = EtalonModel( fixed={0:1.0, 1:pm} )

With this definition the model, em2, has 4 parameters, period and phase, 
plus the 2 parameters of pm.

Combining two (simple) models we get a compound model for which all the
same methods are defined too (except fixing of parameters, which need to
be done at the simple model level).

    pm = PolynomialModel( 0 )
    gm = GaussModel()
    gm += pm

The model `gm` is a compound model for a (gaussian) spectral line on a
constant background. The results of the **PolynomialModel** and the
**GaussModel** are added together. Other options are subtraction,
multiplication, division and pipe (`-*/|`). In a pipe the result of the
left-hand model is used as input for the right-hand model.

A compound model can be fitted to data just like before. Or
another model can be added to the chain.

    gm += LorentzModel()

We now have two spectral lines (a gaussian and a lorentzian) on a
constant background.  Every time two models are composed into a new one,
(virtual) brackets are placed around them. So the results of the last
model is `rgm = ( r1 + r2 ) + r3`. This can be used to distinguish
between `rc1 = ( r1 + r2 ) * r3` and `rc2 = r1 + ( r2 * r3 )`.
Explicit brackets can be supplied by **BracketModel**.

Most simple models are 1-dimensional, i.e. the x array is a 1d array, or
list, or even 1 number. Some models are 2-dim or more. Then the x array
needs to be of shape (N,D), where D is the dimension of the model and N
equal the length of the y array. For fitting maps special provisions are
provided. A compound model can only have constituent models of the same
dimensionality.   

<a name="synopsis"></a>
## 3. Synopsis

All classes are listed with a one-line purpose. They are organized by
their functionality into 5 sections, models, fitters, nested sampling,
kernels and miscellaneous.

<a name="synops-model"></a>  
### Models

#### Base models.

+ **BaseModel**<br>
    BaseModel implements the common parts of simple models.
+ **FixedModel**<br>
    FixedModel implements the 'fixing' of parameters for simple models.
+ **Model**<br>
    Model implements the common parts of (compound) models.
+ **LinearModel**<br>
    Anchestor of all linear models.
+ **NonLinearModel**<br>
    Anchestor of all non-linear models.
+ **Dynamic**<br>
    Contains a number of methods common to Dynamic models.

#### Compound models.

+ **BracketModel**<br>
    BracketModel provides brackets to a chain of models.
+ **CombiModel**<br>
    CombiModel combines a number of copies of the same model.

#### 1-dimensional simple models

+ **ArctanModel**<br>
    Arctangus Model.
+ **BSplinesModel**<br>
    General b-splines model of arbitrary order and with arbitrary knot settings.
+ **ChebyshevPolynomialModel**<br>
    Chebyshev polynomial model of arbitrary degree.
+ **ConstantModel**<br>
    ConstantModel is a Model which does not have any parameters.
+ **EtalonModel**<br>
    Fabry-Perot Etalon Model.
+ **ExpModel**<br>
    Exponential Model.
+ **FreeShapeModel**<br>
    Pixelated Model. (TBD)
+ **GaussModel**<br>
    Gaussian Model.
+ **HarmonicModel**<br>
    Harmonic oscillator Model.
+ **HarmonicDynamicModel**<br>
    Harmonic oscillator Model of varaible order.
+ **KernelModel**<br>
    Kernel Model, a Model build around an **Kernel**.
+ **LorentzModel**<br>
    Lorentzian Model.
+ **PadeModel**<br>
    General Pade model of arbitrary degrees in numerator and denominator.
+ **PolySineAmpModel**<br>
    Sine of fixed frequency with polynomials as amplitudes.
+ **PolynomialModel**<br>
    General polynomial model of arbitrary degree.
+ **PolynomialDynamicModel**<br>
    General polynomial model of variable degree.
+ **PowerLawModel**<br>
    General powerlaw model of arbitrary degree.
+ **PowerModel**<br>
    General power model of arbitrary degree.
+ **RepeatingModel**<br>
    Variable repetition the same Model
+ **SincModel**<br>
    Sinc Model.
+ **SineAmpModel**<br>
    Sine with fixed frequency.
+ **SineModel**<br>
    Sinusoidal Model.
+ **SplinesModel**<br>
    General splines model of arbitrary order and with arbitrary knot settings.
+ **VoigtModel**<br>
    Voigt's Gauss Lorentz convoluted model for line profiles.

#### 2-dimensional simple models

+ **EtalonDriftModel**<br>
    Sinusoidal Model with drifting frequency.
+ **FreeShape2dModel**<br>
    Pixelated 2-dim Model. (TBD)
+ **Kernel2dModel**<br>
    Two dimensional **Kernel** Model.
+ **PolySurfaceModel**<br>
    General polynomial surface model of arbitrary degree.
+ **ProductModel**<br>
    Direct product of 2 (or more) models.
+ **SurfaceSplinesModel**<br>
    Surface splines model of arbitrary order and knot settings.

<a name="ref-fitter"></a>  
### Fitters

#### Base fitters.

+ **BaseFitter**<br>
    Base class for all Fitters.
+ **IterativeFitter**<br>
    Base class with methods common to all iterative fitters.
+ **MaxLikelihoodFitter**<br>
    Base class with methods common to fitters handling ErrorDistributions.

#### Helpers.

+ **RobustShell**<br>
    For fitting in the presence of outliers.
+ **ImageAssistant**<br>
    Helper class in case the data are in the form of an image.
+ **AnnealingAmoeba**<br>
    Minimizer using an annealing Nelder-Mead simplex.
+ **MonteCarlo**<br>
    Helper class to calculate the confidence region of a fitted model.
+ **ConvergenceError**<br>
    Thrown when an iterative fitter stops while the minimum has not been found.


#### Linear fitters

+ **Fitter**<br>
    Fitter for linear models.
+ **QRFitter**<br>
    Fitter for linear models, using QR decomposition.

#### Nonlinear fitters

+ **AmoebaFitter**<br>
    Fitter using the simulated annealing simplex minimum finding algorithm,
+ **CurveFitter**<br>
    CurveFitter implements scipy.optimize.curve_fit.
+ **LevenbergMarquardtFitter**<br>
    Non-linear fitter using the Levenberg-Marquardt method.
+ **ScipyFitter**<br>
    Unified interface to the Scipy minimization module `minimize`, to fit 
    data to a model.
    ScipyFitter contains the classes:
    - **NelderMeadFitter**<br>
        Nelder Mead downhill simplex.
    - **PowellFitter**<br>
        Powell's conjugate direction method.
    - **ConjugateGradientFitter**<br>
        Conjugate Gradient Method of Polak and Ribiere.
    - **BfgsFitter**<br>
        Quasi-Newton method of Broyden, Fletcher, Goldfarb, and Shannon.
    - **NewtonCgFitter**<br>
        Truncated Newton method
    - **LbfgsbFitter**<br>
        Limited Memory Algorithm for Bound Constrained Optimization
    - **TncFitter**<br>
        Truncated Newton method with limits.
    - **CobylaFitter**<br>
        Constrained Optimization BY Linear Approximation.
    - **SlsqpFitter**<br>
        Sequential Least Squares
    - **DoglegFitter**<br>
        Dog-leg trust-region algorithm.
    - **TrustNcgFitter**<br>
        Newton conjugate gradient trust-region algorithm.

<a name="ref-ns"></a>
### NestedSampler

+ **NestedSampler**<br>
    A novel technique to do Bayesian calculation.
+ **Explorer**<br>
    Helper class of NestedSampler to run the **Engine**s.
+ **Sample**<br>
    Weighted random draw from a Posterior distribution from **NestedSampler**.
+ **SampleList**<br>
    List of **Sample**s with interpretational methods.

<a name="list-priors"></a>
#### Prior distributions

+ **Prior**<br>
    Base class defining prior distributions.

+ **CauchyPrior**<br>
    Cauchy prior distribution.
+ **ExponentialPrior**<br>
    Exponential prior distribution.
+ **GaussPrior**<br>
    Gauss prior distribution.
+ **JeffreysPrior**<br>
    Jeffreys prior distribution, for scale-like parameters.
+ **LaplacePrior**<br>
    Laplace prior distribution.
+ **UniformPrior**<br>
    Uniform prior distribution, for location parameters.

<a name="list-errdis"></a>
#### Error distributions.

+ **ErrorDistribution**<br>
    Base class that defines general methods for a error distribution.
+ **ScaledErrorDistribution**<br>
    Base class that defines methods common to error distributions with a scale.

+ **CauchyErrorDistribution**<br>
    To calculate a Cauchy or Lorentz likelihood.
+ **GaussErrorDistribution**<br>
    To calculate a Gauss likelihood.
+ **GenGaussErrorDistribution**<br>
    To calculate a generalized Gaussian likelihood.
+ **LaplaceErrorDistribution**<br>
    To calculate a Laplace likelihood.
+ **PoissonErrorDistribution**<br>
    To calculate a Poisson likelihood.

#### Hyper parameters.

+ **HyperParameter**<br>
    Values and priors for the parameter(s) of an ErrorDistribution.
+ **NoiseScale**<br>
    Hyperparameter for the scale of a ScaledErrorDistribution 

<a name="list-engines"></a>
#### Engines.

+ **Engine**<br>
    Base class that defines general properties of a Engine.

+ **CrossEngine**<br>
    Cross over between 2 walkers.
+ **FrogEngine**<br>
    The FrogEngine jumps a parameter set towards/over a bunch of others.(TBD)
+ **GalileanEngine**<br>
    Move all parameters in forward steps, with mirroring on the edge.
+ **GibbsEngine**<br>
    Move a one parameter at a time by a random amount.
+ **StartEngine**<br>
    Generates an initial random sample.
+ **StepEngine**<br>
    Move a a walker in a random direction.

<a name="synops-kernel"></a>
### Kernels

Kernels are even functions that are integrable over (-inf,+inf). 
A kernel is bound when it is zero outside (-1,+1)

They can be encapsulated in a **KernelModel** or in a 2dim
**Kernel2dModel**. They also find use in the **RobustShell**.


<table>
<tr>
  <th>name</th>
  <th>function</th>
  <th>bound</th>
  <th>comment</th>
</tr>
<tr>
  <td><b>Biweight</b></td>
  <td>( 1-x<sup>2</sup> )<sup>2</sup></td> 
  <td>true</td>
</tr>
<tr>
  <td><b>CosSquare</b></td>
  <td>cos<sup>2</sup>( 0.5*&pi;*x )</td>
  <td>true</td>
</tr>
<tr>
  <td><b>Cosine</b></td>
  <td>cos( 0.5 &pi; x )</td> 
  <td>true</td>
</tr>
<tr>
  <td><b>Gauss</b></td>
  <td>exp( -0.5 x<sup>2</sup> )</td> 
  <td>false</td>
</tr>
<tr>
  <td><b>Huber</b></td>
  <td>min( 1, 1/|x| )</td> 
  <td>false</td>
  <td>improper because infinite integral</td>
</tr>
<tr>
  <td><b>Lorentz</b></td>
  <td>1 / ( 1 + x<sup>2</sup> )</td> 
  <td>false</td>
</tr>
<tr>
  <td><b>Parabola</b></td>
  <td>1 - x<sup>2</sup></td> 
  <td>true</td>
</tr>
<tr>
  <td><b>Sinc</b></td>
  <td>sin(x) / x</td> 
  <td>false</td>
  <td>do not use in **RobustShell**</td>
</tr>
<tr>
  <td><b>Triangle</b></td>
  <td>1 - |x|</td> 
  <td>true</td>
</tr>
<tr>
  <td><b>Tricube</b></td>
  <td>( 1 - |x|<sup>3</sup> )<sup>3</sup></td> 
  <td>true</td>
</tr>
<tr>
  <td><b>Triweight</b></td>
  <td>( 1 - x<sup>2</sup> )<sup>3</sup></td>  
 <td>true</td>
</tr>
<tr>
  <td><b>Uniform</b></td>
  <td>1.0</td> 
  <td>true</td>
</tr>
</table>

<a name="synops-miscel"></a>
### Miscellaneous

+ **LogFactorial**<br>
    Natural logarithm of n!
+ **Formatter**<br>
    Format a number or array, nicely into a string.
+ **Plotter**<br>
    Plot a model fitted to data.
+ **Tools**<br>
    Various tools.

<a name="refs"></a>  
## 4. Referenes

[1]: D.S. Sivia and J. Skilling. **Data Analysis, A Bayesian Tutorial.** 
Oxford University Press. 2006.<br>
[2]: C.M. Bishop. **Pattern Recognition and Machine Learning.**
Springer Science. 2006.<br>
[3]: W. von der Linden, V. Dose, U. Toussaint. **Bayesian Probabilty Theory.** 
Cambridge University Press. 2014.<br>
[4]: E.T. Jaynes. **Probability Theory.**
Cambridge University Press. 2003.<br>

