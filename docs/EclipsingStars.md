<!--
run: eqn4html.csh EclipsingStars.md
to convert the embedded latex equations into images.
-->

<p>
<p>

# A model for eclipsing stars. 

<!--
## Still working on this note. DK.
-->

## Prologue.

This is not a scientific paper. It is my take on eclipsing stars using a
simple model with little assumptions. It is about a model with as few
(adjustable) parameters as I can get away with. While still adhering to
elementary physics. 

## 1. Introduction.

Eclipsing binaries are double stars that pass in front of each other
while orbiting. Here we are only concerned with stars that are so close
and far away, that they manifest themselves as one point of light
(star). These stars show periodic behaviour as the light diminishes when
one star is behind the other.

On the face of it, the light curve is simple: add the light when both
stars are seen, otherwise subtract the occluded parts. And indeed such
systems exist. When the stars are really close to each other, of the
order of a few stellar radii, other effects start to emerge. The stars
heat each other, making a hot hemisphere where the stars face each
other. Depending on the time, the hot spots are seen in phases. Think of
the phases of the Moon or Venus. Also at close distances, tidal
attaction will distort the spherical shape of the stars into prolate
spheroids. The spheroids present a surface, larger than the undisturbed
star when looked at sideways, and smaller when looked at head on.

In this not the star at the center of the (calculated) orbit will be
designated as star 1; the orbiting star is star 2. 


## 2. Stellar Orbit in 3 dimensions.

We start with a stellar orbit model in 3 dimensions.  As both stars are
merged into one point, we set the semi-major axis to 1 and the rotation
of the line of nodes to 0.  Those parameters of a stellar orbit model
have no effect in an eclipsing star system. 

When the orbit has grinded down to a completely circular one, 3 more
parameters of the steller orbit model vanish: the eccentricity is 0 by
definition for circles; the phase and the longitude from north disappear
by want of a periastron.  Both are undefined as the periastron does
not exist any more.  We set both values to 0.  This latter model has
only 2 parameters left: the period and the inclination. 

The stellar orbit model yields 3 coordinates (x,y,z).  The +x coordinate
is pointing to the east, -y is pointing north and z is towards the
observer.  We can transform the rectangular coordinates (x,y,z) to
spherical coordinates (&rho;,&phi;,&theta;).  Now &rho; is the spatial
distance between the stars, &phi; is the rotational angle in the
sky-plane, measured from north, and &theta; is the angle measured from
the xy-plane, up (to the observer) is positive and down is negative. 
The apparent distance (in the xy-plane) between the stars is indicated
as d. 

We minimally need 4 more parameters: the radii of both stars and their
luminosities. The radii are given in fractions of the semi-major axis,
i.e. r1,r2 < 1. The luminosities need to be additive, so they cannot be
magnitudes. We need to translate to the magnitude, m, to luminosty, L,
and scale them to some nice number range.

<!--latex
\begin{displaymath}
L = 10 ^ { -m / 2.512 } 
\end{displaymath}
latex-->

| &nbsp; | ![ES-Equation-1](images/es-eq-1.png "Eq 1") | (1) |
|:-:|:-|-------------------------------------------------:|
<p>

In total, these simple eclipsing star models have 6 or 9 adjustable
parameters. 

## 3. Constraints

There are 2 obvious constraints for the parameters. Firstly the stars
should not crash or rupture each other en secondly they should actually
show eclipses.

Constraints are implemented as change in the likelihood, but
theoretically they are extra priors.  It is knowledge we have
beforehand, but it can not be implemented with simple, mutually
independent probability distributions, acting on the parameters.  It is
the relation between the parameters that define the prior. 

The no-crash constraint entails that the sum of the stellar radii must
be smaller than the distance between the stars, or better even the Roche
limits must be smaller.  The distance between the stars depends on the
eccentricity, e, of the system.  The closest approach, the periastron
distance, is (1 - e) times the semi-major axis, that we have defined as
being 1. Here we have a simple prior that is 0 when a crash occurs and 1
otherwise. 

The second constraint, actual eclipses, demands that the inclination
must be near enough to perpendicular to the sky plane. The constraint is a
function of the stellar radii, the eccentricity, the inclination and the
angle between periastron and north (longitude).  From these parameters
we can calculate the nearest approach as projected on the sky plane.
We define an extra prior which accepts the orbit setting when eclipses
are possible (Pr = 1), rejects them when there can not be any eclipses
(Pr = 0) and a linear relation in the in-between zone.

## 4. Overlap.

When the projected distance, d, is larger than the sum or the radii,
there is no overlap. When the difference between the radii is smaller
than the distance there is complete overlap. In these cases the overlap
area, A<sub>o</sub>, is defined as

<!--latex
\begin{eqnarray*}
\quad A_o =\!&\!0 \quad\ \ & \mbox{if}\ d > r_1 + r_2 \\
           \!&\!A_m    \ \ & \mbox{if}\ d < | r_1 - r_2 |
\end{eqnarray*}
latex-->

| &nbsp; | ![ES-Equation-2](images/es-eq-2.png "Eq 2") | (2) |   
|:-:|:-|-------------------------------------------------:|   
<p>

A<sub>m</sub> is the area of the smaller star (in radius).

The overlap of 2 stars approaching each other is given by the
pink area in figure 1. The area can be calculated as the sum of the two
sectors starting in A and B and subtracting the 2 triangles ACD and BCD.

![Overlap](images/overlap.png "Figure 1")
<table><tr>
<td style="width: 10px;">  </td>
<td style="width: 350px; text-align: left;">
Figure 1. Area of two overlapping circles.
</td></tr>
</table>
<p>

The sector A is found as: 2 &beta; r<sub>1</sub><sup>2</sup>. 
The triangle ACD is equal to  AE * ED = 
r<sub>1</sub><sup>2</sup> cos( &beta; ) sin( &beta; )

For sector B and triangle BCD hold similar equations so that the
combined overlap area, A<sub>o</sub>, equals

<!--latex
\begin{displaymath}
A_o = \beta r_1^2 + \alpha r_2^2 - 0.5 r_2^2 \sin( 2 \alpha ) 
      - 0.5 r_1^2 \sin( 2 \beta )
\end{displaymath}
latex-->

| &nbsp; | ![ES-Equation-3](images/es-eq-3.png "Eq 3") | (3) |
|:-:|:-|-------------------------------------------------:|
<p>
  
The angle &alpha; and &beta; are found using the cosine rule.

from the overlap area, we define 2 visibility functions, one for each
star. The sum of these visibilities, multiplied with the luminosities,
yield the light curve of the double star.

<!--latex
\begin{eqnarray*}
V_1 &=& 1 - ( A_o / A_1 ) \delta( z > 0 ) \\
V_2 &=& 1 - ( A_o / A_2 ) \delta( z < 0 ) 
\end{eqnarray*}
latex-->

The Kronecker &delta; return 1 when the condition is true, 0 otherwise. 

| &nbsp; | ![ES-Equation-4](images/es-eq-4.png "Eq 4") | (4) |
|:-:|:-|-------------------------------------------------:|
<p>

Limb darkening or variations in temperature over the surface of the
stars (like sun spots) are not taken into account. 

![Overlap](images/esm.png "Figure 2")
<table><tr>
<td style="width: 10px;">  </td>
<td style="width: 350px; text-align: left;">
Figure 2. Eclipsing binary star with a variety of additional settings.
</td></tr>
</table>
<p>

The eclipsing of stars can be seen in figure 2, the black line.

## 5. Spot Illumination.

When two stars are real close, they heat each other up, on the near
sides only. The heating is proportional to the temperature of the other star
times it surface, and inversely proportional to the true distance
squared. The equation was taken from 
[Dzygunenko and Tvardovskyi](./references.md/#dzygunenko) or 
[PDF](https://oejv.physics.muni.cz/issues/oejv_0258.pdf).
It gives the extra temperture on star 2, caused by star 1

<!--latex
\begin{displaymath}
T_{2,s}^4 \propto T_1^4 \frac{r_1^2}{2 \rho^2} 
\end{displaymath}
latex-->

| &nbsp; | ![ES-Equation-5](images/es-eq-5.png "Eq 5") | (5) |
|:-:|:-|-------------------------------------------------:|
<p>

The hot spot is always facing the other star, so the observer sees
it in phases, with the larger contribution when z < 0, i.e. star 2 
is almost behind star 1. <br>
The phase modulates the spot with 
cos<sup>2</sup>(&nbsp;2&nbsp;(&nbsp;&theta;&nbsp;-&nbsp;90&nbsp;)&nbsp;).

The proportionality in eq.5 defines another adjustable parameter,
f<sub>s</sub>, which combined with the fact that the luminosity is
proportional to T<sup>4</sup>, yields the result, to be added to
L<sub>2</sub>

<!--latex
\begin{displaymath}
L_2\,+\!\!= f_s L_1 \frac{r_1^2}{\rho^2} ( 1 - z / \rho )
\end{displaymath}
latex-->

| &nbsp; | ![ES-Equation-6](images/es-eq-6.png "Eq 6") | (6) |
|:-:|:-|-------------------------------------------------:|
<p>

There is also a heating of star 1 by star 2, which is the same, mutatis
mutandis, as eq.6, except that the phase is reversed, as star 1 needs to
be behind star 2 for visible full illumination: <br>
phase = ( 1 + z / &rho; ). 

Even though the hotter star produces a much larger effect on the other
than reverse, we implemented both as we don't know in advance which star
will be the hotter of the two.

Similar to limb darkening and other temperature variations, we consider
the star surface as uniform when doing the overlap calculations. On the
other hand, when the stars are eclipsing, the rear one is in "full
moon", while the near one is in "new moon". So no terminators in sight. 

The effects of spot illumination can be seen in figure 2, the green line.


## 6. Tidal Distortion.

Another effect present in close binaries is tides due to gravitational
differences on the near and far side of a star. 
The tidal forces follows from Newton's law of gravity:

<!--latex
\begin{displaymath}
\Delta F_1 = 2 r_1 \frac{G m_1 m_2}{\rho^3} 
\end{displaymath}
latex-->

| &nbsp; | ![ES-Equation-7](images/es-eq-7.png "Eq 7") | (7) |
|:-:|:-|-------------------------------------------------:|
<p>

A similar formula holds for star 2. 

The result of this gravitational pull is a distortion of the spherical
star into a prolate (elongated) spheroid. We assume that these effects
act immediately resulting in an elongation directed to the other star.

The ellipticity of a uniform
fluid sphere of radius, r<sub>2</sub>, is given, in first approximation,
by 
[equations 1.468 of teaching site](https://farside.ph.utexas.edu/teaching/355/Surveyhtml/node69.html)
--admittedly not a very good reference, but it is all I could find--

<!--latex
\begin{displaymath}
\epsilon_2 = \frac{15}{4} \frac{ m_1 }{ m_2 } \big( \frac{ r_2 }{ \rho } \big)^3
\end{displaymath}
latex-->

| &nbsp; | ![ES-Equation-8](images/es-eq-8.png "Eq 8") | (8) |
|:-:|:-|-------------------------------------------------:|
<p>

In eq.8 we have the ratio of the masses of the stars, 
m<sub>1</sub>&nbsp;/&nbsp;m<sub2</sub>, which is another
unknown that appears as an extra parameter in the model. In the
analogous equation for the ellipticity of star 1, the same ratio
appears, but now in the inverse. So in total we have one extra
parameters, governing the tidal distortion, which as a bonus,
--for all it's worth--, even represents something physical, the mass
ratio of the stars. 

Assuming that the total volume of the star is preserved, during tidal
distortion, we have that the cube of the (nominal) radius, r, equals the
semimajor axis, a, times the semiminor axis, b, squared. Together with
the ellipticity, &epsilon;, which connectd a and b, via 
a = b ( 1 - &epsilon; ), we find

<!--latex

\begin{eqnarray*}
a_1 &=& r_1 / ( 1 - \epsilon_1 )^{2/3} \\ 
b_1 &=& r_1 * ( 1 - \epsilon_1 )^{1/3}
\end{eqnarray*}
latex-->

| &nbsp; | ![ES-Equation-9](images/es-eq-9.png "Eq 9") | (9) |
|:-:|:-|-------------------------------------------------:|
<p>

Obviously the ellipticity has to be kept strickly within the range
[0,1]. Equation 8, does not automatically guarantee that. We need
another constraint on the combination of parameters that yields the
&epsilon;s.

In figure 3, we display 6 positions of the secundary star in the binary
system. The observer is at the top.  The
variables a<sub>1</sub>, b<sub>1</sub>, and c<sub>1</sub> are defined as
the true semi-major axis, the semi-minor axis and the apparent
semi-major axis of the ellipsoid, respectively.  As the ellipsoid is
rotationally symmetric along the long axis, the apparent semi-minor axis
is the same as the true one. 

![Tides](images/tides.png "Figure 3")
<table><tr>
<td style="width: 10px;">  </td>
<td style="width: 350px; text-align: left;">
Figure 3. Gravitational tides. The shape of star 2 changes considerably
in its elliptic orbit. On star 1, shape changes are hardly noticeable.
</td></tr>
</table>
<p>

Projecting a prolate spheroid, yields an ellipse with the same minor
axis as the spheroid, and an apparent major axis, m<sub>a</sub>,
varying between both axis.  The size of the major axis depends on the
aspect angle &theta;. 

<!--latex
\begin{displaymath}
c_1 = \sqrt{ a_1^2 \sin^2 \theta + b_1^2 \cos^2 \theta  } 
\end{displaymath}
latex-->

| &nbsp; | ![ES-Equation-10](images/es-eq-10.png "Eq 10") | (10) |
|:-:|:-|-------------------------------------------------:|
<p>

Assuming, as we did before, that the surface temperature is the same
everywhere, we see the luminosity increase when looking sideways at the
prolate spheroid and decrease when looking head-on. 
The luminosity changes proportional to the apparent surface area: 
c<sub>1</sub> * b<sub>1</sub> and c<sub>2</sub> * b<sub>2</sub>,
respectively. 

The effects of tidal distortion can be seen in figure 2, the red and
blue lines.


## 7. Symmetry.

As we are seeing only one dot of light which sums the contribution of
both stars, the orbit that fit the light curve, is not unique.  Even
after we fixed the line of nodes to pointing north and the semi-major
axis to 1, there are still several completely identical solutions. 
We can find the other solutions by mirroring of the main axes.

![Tides](images/symmetry.png "Figure 4")
<table><tr>
<td style="width: 10px;">  </td>
<td style="width: 350px; text-align: left;">
Figure 4. Orbital symmetries.
</td></tr>
</table>
<p>

In figure 4 we display 4 panels. The first one, panel a, shows the
starting point, from which we mirror to get to the other panels. In each
panel we see the light curve at the top. The numbered arrows refer to the
positions of star 2 in the insets low-left and low-right. The insets
give two views of the orbit; to the left as eclipsing view and to the
right in a sideways view, with the observer further to the right. The
effects of spot illumination and tidal distortion is only shown in star
2. It would be confusing to show it also for star 1.

Panel b shows the orbit mirrored in the y-z plane, most clearly in the
left inset.  We see star 2 pass on the other side over star 1.  This can
be achieved by changing the inclination into ( 180 - inclination )

Panel c shows the orbit mirrored in the x-z plane, most clearly in the
right inset. The stars are running anti-clockwise. This mirroring comes
about when both the inclination and the longitude of the periastron are 
increased by 180 degrees. The orbit is flipped with respect to
the sky plane and the orbit itself is moved forward by half a period. 

Panel d shows the orbit mirrored in the x-y plane. What was back is now
up front and vice versa. To keep the same light curve we also have to
flip the stars. To achieve this we increase the inclination by 180
degrees and exchange the radii and luminosities of the stars.

The mirrorings are summarized in the table below.

| mirror | panel  |  incl  |  long  |  radius   |  lumen   | 
|:------:|:------:|:------:|:------:|:---------:|:--------:|
|   y z  |   b    | &pi;-i |        |           |          | 
|   x z  |   c    |  +&pi; |  +&pi; |           |          |
|   x y  |   d    |  +&pi; |        |1&lt;=&gt;2 |1&lt;=&gt;2|

<p>
The 3 mirrorings on fundamental planes, can be combined into 8
parameter sets that all produce the same light curve.
 
We could make the choice here to allow all these solutions and see where 
the final ends. However we already have a 10 dimensional parameter space
where the solution must be found in a tiny area, with in some dimensions
almost no gradient leading to it. If e.g. the period is off by a very
small fraction, it is just as bad as when is is off by a large factor.

## 8. Practicalities.

Constricting the parameter search space as much as possible is a must. 
First and foremost we need to know the period. 

There are 2 problems here.  Firstly, we have irregularly spaced data. 
This prohibits everyones favorite method, the FFT.  And secondly, a
light curve does not resemble (co)sines in any way. That makes the 
Lomb-Scargle method much less effective. 

However, inspired by the idea that Lomb-Scargle boils essentially down
to the fitting of (co)sines to a linear series to frequencies, we
replaced the (co)sines for splines. The splines have less of a problem to
follow the intrincacies of a light curve, when it has enough knots.
Assuming that the eclipse time is about 10 % of the total time, we would
need about 20 knots in a periodic configuration. So we at least catch
the eclipses at one knot location. The fitting is more complicated than
with (co)sines, but it is still a linear problem and easily doable in
one (quasi) matrix inversion.

When following this route, we still need to finely search the frequency
space. Generally, the eclipses have steep slopes, prohibiting gradients
along which to slide toward the true minimum. 

 






  



