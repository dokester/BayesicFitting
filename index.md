---
---

<!--
## Navigation

| Global | Documentation 
|:-|:-|
| [Home](./index.md) | [Manual](./docs/manual.md) |
| [Readme](./README.md) | [Glossary](./docs/glossary.md)  |
| [Notes](./docs/notes.md) | [Design](./docs/design.md) |
| [Examples][exlink] | [Trouble](./docs/troubles.md) |
-->

[![PyPI Downloads](https://static.pepy.tech/badge/bayesicfitting)](https://pepy.tech/projects/bayesicfitting)
![Tests Status](./docs/images/tests-badge.svg)
![Coverage Status](./docs/images/coverage-badge.svg)


[exlink]: https://github.com/dokester/BayesicFitting/tree/master/BayesicFitting/examples

&nbsp;

# Home

BayesicFitting is a PYTHON toolbox for the fitting of models to data 
in a Bayesian way.

Data in this context means a set of (measured) points x and y. 
The model provides some (mathematical) relation between the x and y.
Fitting adapts the model such that certain criteria are optimized, 
making the model as close as possible to the data. 

BayesicFitting has various tools to find the optimal fit of the data to the model.
The toolbox can also answer the question whether one model fits 
the data better than another model. 
Especially this latter aspect elevates Bayesian fitting above other model fitting procedures.

BayesicFitting consists of more than 100 Python classes, of which a third are model
classes. Another third are fitters in one guise or another and miscelleaneous stuff.
The remaining third is needed for Nested Sampling, a novel way to solve 
inference problems in a completely Bayesian way. 
It was developed by John Skilling and David MacKay around 2000.

The package is stored at [github](https://github.com/dokester/BayesicFitting)
and [pypi](https://pypi.org/project/BayesicFitting/).
The easiest way to install it is via

    pip install BayesicFitting

This site is dedicated to documentation. It contains a manual about the 
use of the package and a reference manual with details about each class.
A design document about the structure of the package. A glossary
defining the term used and a help document about restrictions and trouble
shooting. All can be found via the Navigation fold-out table, upper left.
On other pages there is also a Contents table, for the page itself.

The pictures in the side bars are a few examples of what can achieved with the 
toolbox. More examples can be found on [examples][exlink].






