# BayesicFitting

A package for model fitting and bayesian evidence calculation.

(In case you are wondering what that is about take a 
quick look at [this example.](./BayesicFitting/examples/sealevel.ipynb))

## What's new in version 2.1.
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



## Content

1. [History](#history)
2. [Setup](#setup)
3. [Structure](#structure)
4. [Status](#status)
5. [Versions](#versions)

<a name="history"></a>
## 1. History 

The BayesicFitting package is a python version of the the fitter classes
in Herschel Common Science System (HCSS). The HCSS version was written
in JAVA mostly by me. I encoded features and classes that were requested
by my Herschel colleagues or that I remembered having used myself during
my lifelong career as data analyst for earlier satellites as IRAS, ISO
and AKARI. So most of the stuff in here was needed and used at a certain
moment in time. Even now the package is developing in directions that
are needed by my work for JWST. 

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
classes are in a directory BayesicFitting/source. A special type of
functions are found in BayesicFitting/source/kernels. They can be used
to construct a model.

### examples

In [BayesicFitting/examples](./BayesicFitting/examples) a number of scripts can be
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

In the [documenation](./BayesicFitting/documentation) directory a number of documents
can be found. 


+ [Manual](./BayesicFitting/documentation/manual.md)<br>
A first draft of a manual. It obviously needs more work.

+ [Troubles](./BayesicFitting/documentation/troubles.md)<br>
A list of troublesome situations and what to do about it.

+ [Glossary](./BayesicFitting/documentation/glossary.md)<br>
A list of the terms used throughout this package, with explanations.

+ [Design](./BayesicFitting/documentation/design.md)<br>
An architectural design document, displaying the relationships between 
the classes. 

### test

Almost all classes have a test harness. These are located in
BayesicFitting/test. They can be execised as:

    python -m unittest <file>

where python refers to python3 and file refers to one of the files in
BayesicFitting/test.

As most functionality is tested in a test harness, examples on how to
use the classes can be found there too.

<a name="status"> </a> 
## 4. Status 

A package like this is never finished. Always more classes and/or
functionalities can be added. I present it now as it is in the hope it
will be usefull and it will generate feedback.

More work needs to be done in:

  * Documentation, especially the manual.
  * Examples, more of them and covering more classes.
  * Introduction of more Problems: MultiOutputProblem, OrderProblem, ...

<a name="versions"></a>
## 5. Versions

 +  4 Jan 2018 version 0.9.0.<br>
   * Initial upload to github.
 + 26 Jan 2018 version <br>
 +  5 Mar 2018 version 1.0.1 <br>
   * Package on pypi.com. 
   * Restructured all import statement to comply with PYPI package.
 + 14 Mar 2018 version 1.0.2 <br>
   * Added Dynamic Models 
   * Added piping of models
 + 23 Mar 2018 version 1.0.3 <br>
   * Some issues with ErrorDistributions and map fitting
   * 2-d fitting examples added
   * All examples revisited
   * Links in README.md updated
 + 28 May 2018 version 1.0.4 <br>
   * New classes: CircularUniformPrior, PseudoVoigtModel
   * VoigtModel uses scipy.special.wozf() and has partials now,
   * Refactoring Priors to the BaseModel
   * Restructuring Dynamic
   * Threading optional in NestedSampler.
   * New classes: UniformErrorDistribution, FreeShapeModel and kernels/Tophat
   * added to testharnesses and examples
 + 27 June 2018 version 1.0.5<br>
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
   * see above in Whats new.
