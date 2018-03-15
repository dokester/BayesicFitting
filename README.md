# BayesicFitting

A package for Bayesian model fitting and evidence calculation.

(In case you are wondering what that is about take a 
quick look at [this example.](./examples/sealevel.ipynb))

## Content

1. [History](#history)
2. [Setup](#setup)
3. [Structure](#structure)
4. [Status](#status)

<a name="history"></a>
## 1. History 

The BayesicFitting package is a python version of the the fitter classes
in Herschel Common Science System (HCSS). The HCSS version was written
in JAVA mostly by me. I encoded features and classes that were requested
by my Herschel colleagues or that I remembered having used myself during
my lifelong career as data analysis for earlier satellites as IRAS, ISO
and AKARI. So most of the stuff in here was needed and used at a certain
moment in time. Even now the package is developing in directions that
are needed by my work for JWST. 

The HCSS system is in the public domain under GPL3. It was used by the 3
instrument groups of the Herschel satellite to write calibration and
analysis software. Since the end of the mission HCSS is not being
maintained

I used a customized version of java2python (j2py on github) to translate
the JAVA classes to python. However, the actual code needed serious
pythonization. Every line has been inspected. The documentation got most
profit from the automated conversion. Also the structure into classes,
the inheritance, methods and dependencies are largely the same as in the
original HCSS.

<a name="setup"> </a>
## 2. Setup 

The package is written in python3 although I am not aware of using any
specific python3 features. It uses numpy (>= 1.9) for its array
structure, scipy (>=1.0) for linear algebra and other stuff and astropy
(>=2.0) for units. Matplotlib (>=2.0) is used for plotting.

Download and unpack the BayesicFitting zip file from github. Move into 
the BayesicFitting-master directory and run:

> python setup.py install

where python is python3.


<a name="structure"> </a>
## 3. Structure 

### source

The BayesicFitting package consists of over 100 classes, each class in
its own file. These classes can be divided into 3 broad categories:
models, fitters and nested sampling. About 50 models, 10 fitters and the
remainder is needed to run the nested sampling algorithm. All these
classes are in a directory BayesicFitting/source. A special type of
functions are found in BayesicFitting/source/kernels. They can be used
e.g. to combine into a model.

### examples

In [BayesicFitting/examples](./examples) a number of scripts can be
found to exercise the classes. They are in the form of jupyter
notebooks. Some are using real data; others have synthetic data
specially constructed to make some point. 

All examples can be inspected by clicking on them. They will fold out in
the browser.

To actually exercise the examples and maybe adapt then, start a jupyter
notebook in the examples directory.

    jupyter notebook

The program will open a list in your webbrowser where you can select a
notebook file (.ipynb), which can be run.


### documentation

In the [documenation](./documentation) directory a number of documents
can be found. 


+ [Manual](./documentation/manual.md)<br>
A first draft of a manual. It obviously needs more work.

+ [FAQ](./documentation/troubles.md)<br>
A list of troublesome situations and what to do about it.

+ [Glossary](./documentation/glossary.md)<br>
A list of the terms used throughout this package, with explanations.

+ [Design](./documentation/design.md)<br>
An architectural design document, displaying the relationships between 
the classes. 

### test

Almost all classes have a test harnass. These are located in
BayesicFitting/test. They can be execised as:

    python -m unittest <file>

where python refers to python3 and file refers to one of the files in
BayesicFitting/test.

As most functionality is tested in a test harnass, examples on how to
use the classes can be found there too.

<a name="status"> </a> 
## 4. Status 

A package like this is never finished. Always more classes and/or
functionalities can be added. I present it now as it is in the hope it
will be usefull and it will generate feedback.

More work needs to be done in:

  * Documentation, especially the manual.
  * Examples, more of them and covering more classes.
  * FreeShapeModel needs rethinking.


 +  4 Jan 2018 version 0.9.0 Do Kester.<br>
Initial upload to github.
 + 26 Jan 2018 version <br>
 +  5 Mar 2018 version 1.0.1 <br>
Package on pypi.com. Restructured all import statement to comply with PYPI package.
 + 14 Mar 2018 version 1.1.0 <br>
   * Added Dynamic Models 
   * Added piping of models

