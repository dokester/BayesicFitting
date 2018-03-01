

In this directory is an enhanced copy of the bspline package of 
John Foster and Juha Jeronen, at http://github.com/johnfoster/bspline.

A bspline is defined on a set of knots. The original bspline gave valid
results when the input x was strictly: knots[0] <= x < knots[-1].
An x values equal to the last knot gives an error.

This version is enhanced in the sense that now x can be 
knots[0] <= x <= knots[-1].

DK.
