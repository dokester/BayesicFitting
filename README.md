---
---

<div class="dropdown2">
  <span style="background-color: DodgerBlue; color: White; border:5px 
solid DodgerBlue">Contents</span>
  <div class="dropdown-content">

| Contents |
| :-: | 
| 1. [History](#history) |
| 2. [Setup](#setup) | 
| 3. [Structure](#structure) | 
| 4. [Status](#status) | 
| 5. [Versions](#versions) |

  </div>
</div>

[![PyPI Downloads](https://static.pepy.tech/badge/bayesicfitting)](https://pepy.tech/projects/bayesicfitting)
![Tests Status](./docs/images/tests-badge.svg)
![Coverage Status](./docs/images/coverage-badge.svg)

<!--  With link to tests en coverage
[![Tests Status](./reports/junit/tests-badge.svg?dummy=8484744)](./reports/junit/junit.xml)
[![Coverage Status](./reports/coverage/coverage-badge.svg?dummy=8484744)](./reports/coverage/coverage.xml)
-->


[exlink]: https://github.com/dokester/BayesicFitting/tree/master/BayesicFitting/examples
[srclink]: https://github.com/dokester/BayesicFitting/tree/master/BayesicFitting/source
[kllink]: https://github.com/dokester/BayesicFitting/tree/master/BayesicFitting/source/kernels

&nbsp;

# Readme.

BayesicFitting is a package for model fitting and Bayesian evidence calculation.

In case you are wondering what that is about take a quick look at 
the examples in the side bars.

We have a paper out in "Astronomy and Computing" about BayesicFitting.
[Kester and Mueller (2021)](./docs/references.md/#kester8).

Citation index for the BayesicFitting package:
DOI: 10.5281/zenodo.2597200


<a name="whatsnew"></a>
## What's new.

 + 20 Oct 2025 version 3.2.5<br>
   * Removed unused import statements from source and test (pull request #1)

 + 13 Aug 2025 version 3.2.4<br>
   * Lauch new web site https://dokester.github.io/BayesicFitting/
     - Almost all docstrings adapted for the new site.
   * GalileanEngine
     - add a pertubation attribute: wiggle=0.2. See [Dimensions](./docs/Dimensions.md)
     - find edge by repeated quadratic interpolation before mirroring
   * NestedSampler
     - add new attribute avoid=0.1. See [Dimensions](./docs/Dimensions.md)
   * PhantomSampler now uses all phantoms to do the evidence integral
     - Adaptions in Engines, Explorer, WalkerList, NestedSampler.
     - PhantomCollection has one WalkerList also in Dynamic cases.
   * Removed Deprecations, Checks and/or Warnings.
     - Model, ErrorDistributions, Problem
     - Formatter
     - Sample
    
<a name="history"></a>
## 1. History 

The BayesicFitting package is a python version of the the fitter classes
in Herschel Common Science System (HCSS). HCSS was the all encompassing
software system for the operations and analysis of the ESA satelite 
Herschel. The HCSS version of the fitting software was written
in JAVA, mostly by me. I encoded features and classes that were requested
by my Herschel colleagues or that I remembered having used myself during
my lifelong career as data analyst for earlier satellites as IRAS, ISO
and AKARI. So most of the stuff in here was needed and used at a certain
moment in time. Later, the package was developing in directions that
were needed by my work for the James Webb Space Telescope (JWST). 

The HCSS system is in the public domain under GPL3. It was used by the 3
instrument groups of the Herschel satellite to write calibration and
analysis software. Since the end of the mission HCSS is not being
maintained

I used a customized version of java2python (j2py on github) to translate
the JAVA classes to python. However, the actual code needed serious
pythonization. Every line has been inspected. Every construct has been 
revised.

The documentation got most profit from the automated conversion. Also
the structure into classes, the inheritance, methods and dependencies
are largely the same as in the original HCSS.

<a name="setup"> </a>
## 2. Setup 

The package is written in python3 although I am not aware of using any
specific python3 features. It uses numpy (>= 1.9) for its array
structure, scipy (>=1.0) for linear algebra and other stuff and astropy
(>=2.0) for units. Matplotlib (>=2.0) is used for plotting.

Download and unpack the BayesicFitting zip file from github. Move into 
the BayesicFitting-master directory and run:

    python setup.py install

where python is python3. Or install it as :

    pip install BayesicFitting

<a name="structure"> </a>
## 3. Structure 

### source

The BayesicFitting package consists of over 100 classes, each class in
its own file. These classes can be divided into 3 broad categories:
models, fitters and nested sampling. About 50 models, 10 fitters and the
remainder is needed to run the nested sampling algorithm. All these
classes are in a directory [BayesicFitting/source][srclink]. 
A special type of functions are found in [BayesicFitting/source/kernels][kllink]. 
They can be used to construct a model.


### examples

In [BayesicFitting/examples][exlink] a number of scripts can be
found to exercise the classes. They are in the form of jupyter
notebooks. Some are using real data; others have synthetic data
specially constructed to make some point. 

All examples can be inspected by clicking on them. They will fold out in
the browser.

To actually exercise the examples and maybe adapt then, start a jupyter
notebook in your examples directory.

    jupyter notebook

The program will open a list in your webbrowser where you can select a
notebook file (.ipynb), which can be run.


### documentation

In the [documenation](./docs)
directory a number of documents can be found. 

+ [Manual](./docs/manual.md):
The manual for the package.

+ [Classes](./docs/classes.md):
Detailed documentation on all classes and their methods. Taken from the
Python docstrings.

+ [Troubles](./docs/troubles.md):
A list of troublesome situations and what to do about it.

+ [Glossary](./docs/glossary.md):
A list of the terms used throughout this package, with explanations.

+ [Design](./docs/design.md):
An architectural design document, displaying the relationships between 
the classes. 

+ [Style](./docs/convention.md):
A few notes on my style of code and documenation.

+ [References](./docs/references.md):
A list of external references for BayesicFitting.

### test

Almost all classes have a test harness. These are located in
BayesicFitting/test. They can be execised as:

    python -m unittest <file>

where python refers to python3 and file refers to one of the files in
BayesicFitting/test.<br>
As most functionality is tested in a test harness, examples on how to
use the classes can be found there too.

<a name="status"> </a> 
## 4. Status 

A package like this is never finished. Always more classes and/or
functionalities can be added. I present it now as it is in the hope it
will be usefull and it will generate feedback.

According to Wikipedia -> "Software release life cycle" it is called 
"Perpetual Beta". It continues to be in a beta-release because new 
classes and features can be added.

Some of the newer additions will be indicated as having and "Alpha" 
status and keep that until they matured somewhat further. 
These classes are more prone to change in their interfaces, methods etc.

More work needs to be done in:

  * Introduction of more Classes: NeuralNetModel, Evolving Models, Filters (maybe) ...

<a name="versions"></a>
## 5. Versions

 +  4 Jan 2018 version 0.9.0
   * Initial upload to github.

 + 26 Jan 2018 version 1.0.0

 +  5 Mar 2018 version 1.0.1
   * Package on pypi.com. 
   * Restructured all import statement to comply with PYPI package.

 + 14 Mar 2018 version 1.0.2
   * Added Dynamic Models 
   * Added piping of models

 + 23 Mar 2018 version 1.0.3
   * Some issues with ErrorDistributions and map fitting
   * 2-d fitting examples added
   * All examples revisited
   * Links in README.md updated

 + 28 May 2018 version 1.0.4
   * New classes: CircularUniformPrior, PseudoVoigtModel
   * VoigtModel uses scipy.special.wozf() and has partials now,
   * Refactoring Priors to the BaseModel
   * Restructuring Dynamic
   * Threading optional in NestedSampler.
   * New classes: UniformErrorDistribution, FreeShapeModel and kernels/Tophat
   * added to testharnesses and examples

 + 27 June 2018 version 1.0.5
   * New classes: RadialVelocityModel and MixedErrorDistribution
   * testharnesses and examples
   * documentation updates

 + 28 June 2018 version 1.0.6
   * longdescription set to markdown (Still not OK on pypi.org)

 + 28 July 2018 version 1.0.7
   * small compilation error in 1.0.6

 + 11 October 2018 version 1.0.8
   * refactoring the setting of attributes in Models
   * documentation (manual, design, etc.) updated.

 + 28 December 2018 version 2.0.0
   * Introduction of Problem Classes: 
     - Problem. <br>
	Base class for problems to be handled by NestedSampler.
     - ClassicProblem. <br>
	Common class for everything that was possible in version 1.
	ClassicProblem is transparant as all interfaces to NestedSampler have remained 
	the same as they were in version 1.0, even though behind the scenes a 
	ClassicProblem has been invoked.
     - ErrorsInXandYProblem. <br>
	Problem that have errors in the xdata  and in the ydata.
     - ... more to come.
   * Introduction of Walker and WalkerList to represent the internal ensemble
     in NestedSampler. 
   * Adaptations in NestedSampler, ErrorDistributions, Engines, Sample, SampleList.
   * Better separation of responsibilities of ErrorDistribution and Problem. <br>
     Consequently ErrorDistribution has a new initialisation, which is incompatible 
     with previous versions. In most cases this has no effect on the calling 
     sequences of NestedSampler.
   * Rename GenGaussErrorDistribution into ExponentialErrorDistribution.
   * New testharnesses and examples.
   * Adaptations of documentation: manual and design.

 + 16 Jan 2019 version 2.1.0
   * MultipleOutputProblem.
     Problems with more dimensional outputs 
   * StellarOrbitModel. 
     A 2 dim output model to calculate the orbit of a double star
   * Keppler2ndLaw.
     To calculate the radius and true anomaly according to Kepplers 2nd law. 
     (and derivatives)
   * RadialVelocityModel: adapted to Kepplers2ndLaw. A slight change in the 
     order of the parameters.
   * NestedSampler: some improvements in output layout.
   * New tests, examples and updates for documentation.

 + 7 Feb 2019 version 2.2.0
   * ChordEngine. Implementation of the POLYCHORD engine, developed 
     by Handley etal. (2015) MNRAS 
   * OrthogonalBasis. Helper class fot ChordEngine.
   * Tests and examples

 + 19 Feb 2019 version 2.2.1 
   * AmoebaFitter still mentioned GenGaussErrorDistribution; replaced 
     by ExponentialErrorDistribution
   * Some documentation issues repaired.

 + 20 Jun 2019 version 2.3.0 
   * Add LogisticModel and SampleMovie
   * Periodic residuals in Problem
   * Small issues repaired
   * Rerun all examples
   * Pictures moved to documentation/images
   * Some documentation issues repaired.

 + 14 Nov 2019 version 2.4.0 to 2.4.2
   * New Classes:
      - DecisionTreeModel
	A DecisionTree Model (DTM) is mostly defined on multiple input dimensions (axes).
    	It splits the data in 2 parts, according low and high values on a certain input axis.
    	The splitting can continue along other axes.
      - Modifiable
	Interface to define modifiable behaviour of some Models.
      - StructureEngine
	Engine to modify Models that implement Modifiable
   * Introduce Table from astrolib as (multidimensional) xdata
   * Some restructering necessitated by the classes above.
   * Testcases and examples for the classes above

 + 3 Feb 2020 version 2.4.3
   * Clean up and unification of the python doc strings.
   * Reran all examples and test harnasses in python 3.7.
   * Add random seed to several examples to make them more stable.

 + 17 Mar 2020 version 2.4.4
   * Moved BayesicFitting/BayesicFitting/documentation to BayesicFitting/docs
   * Added a references.md file which collects (external) references.
   * Updated the docs files.
   * Handling of weight in accordance with the definition in the Glossary.
   * Add keyword tail= to formatter to display last items of an array.

 + 4 Jun 2020 version 2.5.0
   * Add new models: BasicSplinesModel and SplinesDynamicModel
   * Option for constraints on the likelihood
   * Option for slow engines (working every slow-th iteration in NestedSampler)
   * Restructure growPrior setting
   * Print formatting in NestedSampler
   * Adapt to SplinesDynamicModel
   * Homogenized and improved plotoptions in test harnesses
   * Three more examples added

 + 5 Jun 2020 versions 2.5.1
   * Comment out NeuralNetModel (not yet available) and some typos.

 + 6 Jun 2020 versions 2.5.2
   * Two more bugs smashed (in StartEngine and Prior)

 + 29 Jun 2020 versions 2.5.3
   * Averaging of circular variables
   * Update of static class attributes
   * Attribute and printing issues.

 + 23 Oct 2020 version 2.6.0
   * New class: PhantomSampler; adaptations in Engines, Explorer, WalkerList
   * Restructured NestedSampler to accommodate PhantomSampler
   * Test harnass for PhantomSampler
   * Option: fix parameters in BasicSplinesModel
   * Confusing __str__ method in compound models improved

 + 6 Nov 2020 versions 2.6.1
   * Avoid infinities in unbound Priors
   * mcycles in initialization of MonteCarlo
   * convert xdata, ydata, weights using numpy.asarray

 + 11 Dec 2020 versions 2.6.2
   * Add limits and circular to Priors
   * Finetune Engines

 + 18 Feb 2021 version 2.7.0
   * New class: EvidenceProblem & ModelDistribution; adaptations in NestedSampler and tests.
   * Change in constrain method definition
   * decay in ExpModel
   * some seldom errors, clean-up & new test harnasses. 

 + 19 April 2021 version 2.7.1
   * remove CrossEngine completely

 + 20 April 2021 version 2.7.2
   * put some tests on hold
   * few minor issues/errors

 + 29 Oct 2021 version 2.8.0
   * New class: BernoulliErrorDistribution and SoftMaxModel, tests, examples and data
   * Adaptations To BernoulliED in some other classes
   * Multi-dim input and output issues
   * Updated some other tests and examples
   * Documentation and other small issues.

 + 25 Nov 2021 version 2.8.1
   * Cleanup in Plotter
   * Documentation issues; Replaced style.md by code-style.md
   * Correcting error on Windows systme

 + 07 Feb 2022 version 3.0.0
   * New classes: AstropyModel and UserModel
   * New class: NeuralNetUtilities
   * New classes: NestedSolver, OrderProblem, SalesmanProblem, DistanceCostFunction
   * New classes: OrderEngine, MoveEngine, SwitchEngine, LoopEngine, ShuffleEngine
   * New classes: ReverseEngine, NearEngine, StartOrderEngine
   * Make pipe work for more dimensional output | input
   * Test harnesses for the new classes
   * New examples for AstropyModel, UserModel and SalesmanProblem
   * Update existing examples to improve coverage of pytest
   * update Manual

 + 05 Apr 2022 version 3.0.1
   * Addressing issue #18: UserModel does not work for multiple dimensions.

 + 19 Nov 2022 version 3.1.0
   * Gauss2dErrorDistribution: New Class to handle correlated errors in X and Y
   * ErrorDistribution and GaussErrorDistribution : adaptation for covariant errors.
   * Small updates and corrections and removal of unused methods
   * Added / corrected version information and documentation issues
   * Rerun all examples and added tests

 + 18 Jan 2023 version 3.1.0 (still working on the same update)
   * Implementing accuracy in fitters and samplers
   * Update of documentation
   * More tests

 + 18 Jan 2023 version 3.1.1
   * remove GaussPriorNew from __init__.py

 + 31 Aug 2023 version 3.2.0
   * The new class, PhantomCollection is part of NestedSampler. It contains a sorted 
     WalkerList, in which all valid positions are collected, proper walkers 
     and phantoms. Each iteration the phantoms with log likelihood lower than the 
     low limit for that iteration, are removed. The PhantomCollection is used 
     to get a better estimate on the size of the bounding box for the  walkers and
     to obtain starting positions for new walkers. In general the PhantomCollection 
     contains an order of magnitude more items than the WalkerList itself. 
   * NestedSampler has a new stopping criterion. It also stops when the log of the 
     relative contribution to the logZ (evidence) integral is less than -tolerance (=12). 
   * FootballModel: new class. Model to estimate strengths of football teams in 
     several key parameters. 
   * Address PhantomCollection and add **kwargs in all Engines
   * Quadratic (in stead of linear) interpolation on edge in GalileanEngine
   * Unnormalized Gauss prior changed into a normalized one
   * Some documentation issues
   * More dimensional arrays in LogFactorial
   * __str__() method in NestedSolver and PhantomSampler
   * Avoid numeric instabilities in sqrt in SampleList
   * New tools in Tools
   * More construction options in WalkerList
   * New example: Uefa2022.ipynb
   * New tests: TestPhantomCollection, TestFootballModel
   * Adaptations in existing tests
   * Reran all tests and examples

 + 27 March 2024 version 3.2.1<br>
   A lot of fairly small stuff.
   * \_\_status\_\_ changed to Alpha for some newer additions
   * Priors: 
      - Adapt to input arrays 
      - Made limited and/or circular
      - Proper integral when limited
   * Engines:
      - Add bestCheck and bestBoost
      - Minor restructoring
   * Models:
      - Minor restructoring and renaming
      - setLimits() replaced by setPrior() in RepeatingModel
      - provide for more dimensions of outputs in derivative
   * Problems:
      - toString() method restructured
   * Walker and WalkerList:
      - Add logPrior attribute
      - Change in inheritance reporting
   * PhantomCollection:
      - getList() method
   * NestedSampler:
      - Add repiter attribute: report every repiter when verbose=2
      - Add bestBoost
   * ModelDistribution:
      - put internal sample() method in try-except block
   * Tools:
      - subclassof() method
      - printclass finetuning
   * Test and documentation. Update.

 + 05 Nov 2024 version 3.2.2<br>
   Issue 24: Adapt to numpy-2 and pertaining Scipy, Astropy and MatplotLib

 + 09 Dec 2024 version 3.2.3<br>
   Issue 27: Remove invalid escape sequences from docstrings.

 + 13 Aug 2025 version 3.2.4<br>
   See [What's new](#whatsnew)

<br><br><br><br>

