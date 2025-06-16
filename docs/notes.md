---
---
<!--
## Navigation

| Notes | Global | Documentation |
|:-|:-|:-|
| [Splines](./splines.md) | [Home](../index.md) | [Manual](./manual.md) |
| [Quality](./dataquality.md) | [Readme](../README.md) | [Glossary](./glossary.md)  |
| [BoundingBox](./BoundingBox.md) | [Notes](./notes.md) | [Design](./design.md) |
|  | [Examples][exlink] | [Trouble](./troubles.md) |
|  | | |
-->

<div class="dropdown2">
  <span style="background-color: DodgerBlue; color: White; border:5px
solid DodgerBlue">Contents</span>  
  <div class="dropdown-content">

| Notes |
|:-:|
| [Splines](./splines.md) |
| [Quality](./dataquality.md) |
| [BoundingBox](./BoundingBox.md) |
| [Sampling](./Sampling.md) |
| [Dimensions](./Dimensions.md) |

</div>
</div>

[exlink]: https://github.com/dokester/BayesicFitting/tree/master/BayesicFitting/examples

&nbsp;

# Notes

Here we present a number of notes related to BayesicFitting.

To quote John Skilling on one of the Maxent conferences:
"All these things are probably known to people who know these things."

Well.. It aint me, babe.

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

A look at [bounding boxes](./BoundingBox.md) in higher dimensions.

## Sampling.

[Sampling](./Sampling.md) from the Prior can lead in some cases to problems.


