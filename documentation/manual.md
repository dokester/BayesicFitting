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
information are packed into a class. **Model**s can be combined by various
operations (+-*/) into a new compound model. The functional results,
derivatives etc. of the compound model are calculated according to the
operations at hand. This way quite complicated models can be formed
without worrying about internal consistency.

**Model**s come into 2 varieties: those that are linear in its parameters
and those that are not. The former have great advantages as they can be
fitted directly to the data; the latter always need an iterative fitting
approach. Compound models are non-linear unless all its constituents are
linear and its operations are additive.

There are several dozens of simple Models inside this toolbox.

<a name="fitters"></a>
### Fitters 

A fitter tries to find the minimum in the &chi;<sup>2</sup> landscape,
cq. the maximum in the likelihood landscape, as a function of the model
parameters. The values for the parameters where the minimum cq. maximum
in the landscape is found are the least-squares solution resp. the
maximum-likelihood solution. If the likelihood is Gaussian the two are
the same. 

<a name="ns"></a>
### NestedSampler 

**NestedSampler** samples the Posterior while integrating it to calculate
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

    from PolynomialModel import PolynomialModel
    from Fitter import Fitter

    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [1.2, 1.3, 1.5, 1.4, 1.4]
    pars = Fitter( x, PolynomialModel( 1 ) ).fit( y )

`pars` are the parameters of the model. However this is all we can
get from this little script. As we dont have a handle on the fitter, nor
on the model, we cannot request anything else e.g. the standard
deviations, the evidence, or any other interesting property of the fit.

It would be better to write, in stead of the last line:

    model = PolynomialModel( 1 )	# make a first order polynomial
    fitter = Fitter( x, model )	# construct a fitter with this model
    pars = fitter.fit( y )		# fit the data y to the model

This yields the same set of parameters, but now we can also ask:

    yfit = model( x )		# the model values at x
    stdev = fitter.stdevs		# standard deviations of the parameters
    scale = fitter.scale		# stdev of remaining noise (= y - yfit) 
    covar = fitter.covariance	# covariance between the parameters

To calculate the evidence (or better the logEvidence) we need a prior
probability on the parameters and on the noise scale. In the context of
the Fitters, the prior on the parameters is the UniformPrior, and
on the noise scale it is the **JeffreysPrior**. Both these Priors are
improper, i.e. the integral from -inf to +inf is infinite. So we need
limits, on the parameters prior and on the noise scale prior. 

    logE = fitter.getEvidence( limits=[-10,10], noiseLimits=[0.01,1.0] )

The `logE` is calculated using a Gaussian approximation for the
posterior, also known as Laplace's rule.

See [below](#list-fitters) for a list of available fitters with its
purpose line.

<a name="usage-ns"></a>
### Usage of NestedSampler

**NestedSampler** needs more information to run. It needs priors for all 
its parameters and it needs a likelihood function. We start off defining
some data.

    from GaussModel import GaussModel
    from NestedSampler import NestedSampler

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

    yfit = ns.sample()

where `yfit` contains the optimal model fit. We can now ask optimal
parameters, standard deviations, scale and most impotantly the evidence.

    param = ns.parameters
    stdev = ns.standardDeviations
    scale = ns.scale
    evidence = ns.evidence.

The **Sample**s generated are collected in a **SampleList**, from which
numerous items can be extracted.

    slist = ns.samples
    param = slist.parameters
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
itself  has a name, as do all parameters. One or more of its parameters
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
multiplication and division (`-*/`).
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

+ **BaseModel**<br>
    BaseModel implements the common parts of simple Models.
+ **FixedModel**<br>
    FixedModel implements the 'fixing' of parameters for simple Models.
+ **Model**<br>
    Model implements the common parts of (compound) models.
+ **LinearModel**<br>
    Anchestor of all linear models.
+ **NonLinearModel**<br>
    Anchestor of all non-linear models.

+ **BracketModel**<br>
    BracketModel provides brackets to a chain of `Model`s.
+ **CombiModel**<br>
    CombiModel combines a number of copies of the same model.

#### 1 dimensional simple models

+ **ArctanModel**<br>
    Arctangus Model.
+ **BSplinesModel**<br>
    General b-splines model of arbitrary order and with arbitrary knot settings.
+ **ChebyshevPolynomialModel**<br>
    Chebyshev polynomial model of arbitrary degree.
+ **ConstantModel**<br>
    ConstantModel is a Model which does not have any parameters.
+ **EtalonModel**<br>
    Sinusoidal Model with drifting frequency.
+ **ExpModel**<br>
    Exponential Model.
+ **FreeShapeModel**<br>
    Pixelated Model.
+ **GaussModel**<br>
    Gaussian Model.
+ **HarmonicModel**<br>
    Harmonic oscillator Model.
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
+ **PowerLawModel**<br>
    General powerlaw model of arbitrary degree.
+ **PowerModel**<br>
    General power model of arbitrary degree.
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

#### 2 dimensional simple models

+ **EtalonDriftModel**<br>
    Sinusoidal Model with drifting frequency.
+ **FreeShape2dModel**<br>
    Pixelated 2-dim Model.
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

+ **BaseFitter**<br>
    Base class for all Fitters.
+ **IterativeFitter**<br>
    Base class with methods common to all iterative fitters.
+ **MaxLikelihoodFitter**<br>
    Base class with methods common to fitters handling ErrorDistributions.
+ **RobustShell**<br>
    For fitting in the presence of outliers.

+ **ImageAssistant**<br>
    Helper class in case the data are in the form of an image.
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
    The FrogEngine jumps a parameter set towards/over a bunch of others.
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
**Kernel2dModel**. They also find use in the **RobustFitter**.


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
  <td>true</td>
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

<!--
+ **Biweight**<br>
   __( 1-x<sup>2</sup> )<sup>2</sup>__ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bound
+ **CosSquare**<br>
   __cos<sup>2</sup>( 0.5 &pi; x )__ &nbsp;&nbsp; bound
+ **Cosine**<br>
   __cos( 0.5 &pi; x )__ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bound
+ **Gauss**<br>
   __exp( -0.5 x<sup>2</sup> )__ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; unbound
+ **Huber**<br>
   __min( 1, 1/|x| )__ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; unbound and improper because infinite integral
+ **Lorentz**<br>
   __1 / ( 1 + x<sup>2</sup> )__ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; unbound
+ **Parabola**<br>
   __1 - x<sup>2</sup>__ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bound
+ **Sinc**<br>
   __sin(x) / x__ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; unbound
+ **Triangle**<br>
   __1 - |x|__ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bound
+ **Tricube**<br>
   __( 1 - |x|<sup>3</sup> )<sup>3</sup>__ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bound
+ **Triweight**<br>
   __( 1 - x<sup>2</sup> )<sup>3</sup>__ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bound
+ **Uniform**<br>
   __1.0__ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bound
-->

<a name="synops-miscel"></a>
### Miscellaneous

+ **LogFactorial**<br>
    Natural logarithm of n!
+ **Formatter**<br>
    Format a number or array in a nicely into a string.
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

