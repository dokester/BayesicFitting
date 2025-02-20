---
---

<div class="dropdown2">
  <span style="background-color: DodgerBlue; color: White; border:5px
solid DodgerBlue">Contents</span>  
  <div class="dropdown-content">

| classes |
|:-:|
| [ArctanModel](./classdocs/ChordEngine.md) |
| [ErrorDistribution](./classdocs/Engine.md) |
| [NestedSolver](./classdocs/NestedSolver.md) |

</div>
</div>

[exlink]: https://github.com/dokester/BayesicFitting/tree/master/BayesicFitting/examples

&nbsp;

# Reference Manual

The reference manual for BayesicFitting contains documentation on all classes 
and on the methods pertaining to the clases. Almost all software of BayesicFitting 
is in the form of classes, Models, Fitters etc. 

All classes are listed in the navigation bar on the left. 

Each reference page contains a pink part where the class is documented. Thereafter is a 
white section where all methods and the constructor are documented.

In a Python session they are called as:

    ## import some class
    from BayesicFitting import SomeClass
    ## construct an instantiation of SomeClass
    sc = SomeClass( some, arguments )
    ## assign an attribute of the class
    a = sc.someAttribute
    ## run a method of the class
    r = sc.someMethod( more, arguments )


Documentation on classes, methods, arguments and attributes are found in this 
reference manual. 







# Notes

Here we present a number of notes related to BayesicFitting.

## Splines.

The [splines](./splines.md) note presents details on the construction and 
algorithm of splines in 

 + **SplinesModel**  simple, fast and dense
 + **BSplinesModel** recursive de Boor algoritme, slow
 + **BasicSplineModel** non-recursive de Boor, faster
 + **SplinesDynamicModel** a **BasicSplinesModel** which is 
   - **Dynamic** in the number of knots
   - **Modifiable** in the position of the knots

## Data Quality.   

The [quality](./dataquality.md) note discusses the merits of defining 
data quality in terms of accuracy versus weights.

## BoundingBox

A look at bounding boxes in higher dimensions.


