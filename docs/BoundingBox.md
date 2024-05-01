## Bounding Boxes 

We want to investigate how bounding boxes behave in higher dimensions.

Bounding boxes are rectangular N-dimensional boxes encompassing an
ensemble of M (random) points, fullfilling some (likelihood) constraint. 


We will plot 100 random points inside 4 N-balls of radius 1.0, for resp
N = [2,4,6,8], in black, red, green and blue.  And their bounding boxes. 
They are found by rejection sampling. 

Note that for higer dimensions, more and more points need to be
rejected.  For an 8-ball only one in 73 points are OK.  The random
points tend to concentrate to the middle. 



| ndim | nsamples | rejected |
|-:|-:|-:|
| 2 | 100 | 22 |
| 4 | 100 | 233 |
| 6 | 100 | 991 |
| 8 | 100 | 7306 |


![png](images/BB_4_1.png)
    

This will not get us to a 1000-ball.


We try something else to get to a 1000-ball. 

We calculate the distribution of points thrown randomly into an N-ball,
as projected on a line through the center.  It is obvious that this
distribution is proportional to the projected volume. 

For a 2-ball (circle) the distribution is proportional to a half-circle. <br>
&nbsp;&nbsp;&nbsp;&nbsp;d<sub>2</sub>( x ) = SQRT( 1 - x * x )
    
For a 3-ball (cannonball) there is the volume of a circle present at
every x.  It is proportional to<br>
&nbsp;&nbsp;&nbsp;&nbsp;d<sub>3</sub>( x ) ~ ( 1 - x * x ) = d<sub>2</sub>( x ) <sup>2</sup>

For a 4-ball (hyperball) there the projection is a 3-ball, proportional to<br>
&nbsp;&nbsp;&nbsp;&nbsp;d<sub>4</sub>( x ) ~ d<sub>2</sub>( x ) <sup>3</sup>
    
Etc.

    
![png](images/BB_6_0.png)
    

For higher dimensions the projection of the ball gets more concentrated
toward the center.  Which is not so surprising as we need N random
points of which the sum of the squares must to be less than 1.  It is
easiest for all of them to be quite small.  Nontheless points with all
almost 0's, except one that is between -1 and +1 are also part of the
N-ball.  These points are exceedingly rare.  The bulk sits around 0. 

The bounding box, defined as the upper and lower values in each
dimension of an ensemble of points, randomly drawn from the N-ball, also
shrinks to smaller values.  It will miss the extreme possibilities of
the balls, which are getting more and more improbable.  A bounding box
for an ensemble of M points will miss on average 1/M volume area.

N-balls (and other objects) in higher dimensions are quite
couterintuitive. 

Below we do some sanity checks, whether the distributions conform a
random ensemble of M=5000 points

In the figure below, we have M/N points in N (=2,3,4,8,10) dimensions. 
In green we see the calculated distribution scaled to a maximum of 1.0. 
In red we have a histogram of the ensemble projected on each of the
dimensional axes.  M*5000 point in all, scaled to the same volume. 


On the right hand side we plot the moments of the distributions as
projected on each of the dimensional axes. Just to get a feel how much
they can vary when the distribution inside the N-balls is the golden
standard on uniformity. (made by rejection sampling). 

    
![png](images/BB_9_1.png)
    

![png](images/BB_9_3.png)
    

![png](images/BB_9_5.png)
    

![png](images/BB_9_7.png)
    

![png](images/BB_9_9.png)
    

The experiment follows the theory quite well.

Next we check the distribution of random points in 10 N-dim shells of
equal volume and in 8 perpendicular sectors.  We take 10000 points
random in spheres of 2,3,4,6, and 8 dimensions, by rejection sampling. 
We expect 1000 points in each shell and 1250 in each sector. 

The edges of the shells are defined as 
[0,0.1,0.2,...,0.9,1.0] ** ( 1/ndim )

A point belongs to a shell when its 2-norm falls between the edges of
that shell.

The sectors are defined when ndim >= 3 and then dividing dimensions 1,
2, and 3 in its positive and negative values.



    
![png](images/BB_12.png)
    

