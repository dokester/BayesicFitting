---
---
<br><br>

<a name="EclipsingStarModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class EclipsingStarModel(</strong> <a href="./NonLinearModel.html">NonLinearModel</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py target=_blank>[source]</a></th></tr></thead></table>
<p>

Model for the radial velocity variations of a star caused by a orbiting planet.

| par | symbol | name         | description               | limits     | comment      |
|-----|--------|--------------|---------------------------|------------|--------------|
| p<sub>0</sub> |   e    | eccentricity | of the elliptic orbit     | 0<e<1      | 0 = circular |
| p<sub>1</sub> |   P    | period       | of the velocity variation |   P>0      |  |
| p<sub>2</sub> |   T    | phase        | phase since periastron    | 0<T<2&pi;  |  |
| p<sub>3</sub> |   i    | inclination  | of orbit (close to 90)    | 0<i<&pi;   |  |
| p<sub>4</sub> | &omega;| longitude    | from north to periastron  | 0<&omega;<2&pi; |  |
| p<sub>5</sub> |   r1   | radius<sub>1</sub>     | radius of star 1          | 0<r1<1     |  |
| p<sub>6</sub> |   r2   | radius<sub>2</sub>     | radius of star 2          | 0<r2<1     |  |
| p<sub>7</sub> |   f1   | lumen<sub>1</sub>      | luminosity of star 1      |            |  |
| p<sub>8</sub> |   f2   | lumen<sub>2</sub>      | luminosity of star 2      |            |  |
| p<sub>9</sub> |   fs   | spot         | spot illumination         | fs >= 0    | optional |
| p<sub>10</sub>|   mr   | mass<sub>1</sub>       | relative mass of star 1   | 0 < m1 < 1 | optional |

The amplitude (semimajor axis) is set to 1.0. Both stellar radii are given 
as a fraction of the amplitude. The mass of star 2 is ( 1 - m1 ). The mass ratio
is used in calculating the tidal distortion.

When the sum of the radii (p<sub>5</sub> + p<sub>6</sub>) is larger than the periastron distance 
(1 - p<sub>0</sub>), the stars clash. 

When the model is defined with "circular=True", the parameters p<sub>0</sub> and p<sub>4</sub>
loose their meaning. They are removed from the model.

This class uses [StellarOrbitModel](./StellarOrbitModel.md) to find the true orbit

The parameters are initialized at 
<br>&nbsp;&nbsp;&nbsp;&nbsp; [0.0, 1.0, 0.0, pi/2, 0.0, 0.1, 0.1, 1.0, 1.0, 0.0, 0.5].
It is a non-linear model.

For the mathematics of this model and further explanation see [EclipsingStars](./EclipsingStars.md).html.

(Partial) derivatives were obtained with the help of  
[https](./https.md)://www.derivative-calculator.net
Muchas Gracias


<b>Attributes</b>

* storbit  :  StellarOrbitModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; to calculate the true stellar orbit
* circular  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; whether the orbit is circular (eccentricity == phase == longitude == 0)
* spot  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; apply spot illumination and tidal distortion
* tides  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; apply tidal distortion
* noeclipses  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; no eclipses stricty necessary
* fixpar  :  lambda function
<br>&nbsp;&nbsp;&nbsp;&nbsp; to provide parameters for StellarOrbitModel

<b>Examples</b>

    esm = EclipsingStarModel( spot=True, tides=True )
    print( esm.npars )
    10



<a name="EclipsingStarModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>EclipsingStarModel(</strong> circular=False, spot=False, tides=False, copy=None,
 noeclipses=False, debug=False, **kwargs )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L106-L173 target=_blank>[source]</a></th></tr></thead></table>

Radial velocity model.

Number of parameters depends on the settings of ( False or True ) of 
<br>&nbsp; circular       spot        tides
( 9 or 6 ) + ( 0 or 1 ) + ( 0 or 1 )

<b>Parameters</b>

* circular  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; stellar orbit is circular: eccentricity = 0 ==> phase = lonod = 0
* spot  :  bool or number
<br>&nbsp;&nbsp;&nbsp;&nbsp; apply spot illumination; more pronounced when spot > 1
* tides  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; apply tidal distortion
* noeclipses  :  bool (False)
<br>&nbsp;&nbsp;&nbsp;&nbsp; no eclipses stricty enforced
* copy  :  EclipsingStarModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to copy

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L175-L180 target=_blank>[source]</a></th></tr></thead></table>
Copy method.  

<a name="distanceConstraint"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>distanceConstraint(</strong> logL, problem, allpars, lowLhood ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L182-L199 target=_blank>[source]</a></th></tr></thead></table>
Constrain the sizes of the stars for use in NestedSampling to avoid collapse.
and the inclination to ensure eclipses

<b>Parameters</b>

* logL  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; log Likelihood obtained with allpars
* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; to solve
* allpars  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; all parameters involved in the problem
* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; present value of the likelihood constraint

<a name="logCombiPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logCombiPrior(</strong> allpars ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L201-L269 target=_blank>[source]</a></th></tr></thead></table>
Get extra prior for this combination of parameters.

<b>Parameters</b>

* allpars  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; all parameters involved in the problem

<a name="baseResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseResult(</strong> xdata, params )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L271-L289 target=_blank>[source]</a></th></tr></thead></table>
Returns the result of the model function.


<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.


<a name="lightCurve"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>lightCurve(</strong> xy, z, params, debug=0 )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L291-L343 target=_blank>[source]</a></th></tr></thead></table>
Return the visible area of two eclipsing stars, multiplied by their luminicities.

Adapted from 
<br>&nbsp;&nbsp;&nbsp;&nbsp; https://scipython.com/books/book2/chapter-8-scipy/problems/overlapping-circles/

<b>Parameters</b>

* xy  :  arrey
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance between the stars in the sky plane
* z  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance of star 2 to the sky plane
* params  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the model
* debug  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; debug partial derivativesin stages


<a name="visibleFraction"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>visibleFraction(</strong> xy, z, r1, r2 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L345-L371 target=_blank>[source]</a></th></tr></thead></table>
Calculate the fraction of visibility for both stars.

If z is positive, star 2 is in front of star 1    
If z is negative, star 2 is behind star 1    

<b>Parameters</b>

* xy  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance between overlapping circles
* z  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance of star 2 to the sky plane
* r1  :  float or array
<br>&nbsp;&nbsp;&nbsp;&nbsp; radius of star 1
* r2  :  float or array
<br>&nbsp;&nbsp;&nbsp;&nbsp; radius of star 2

<a name="VFderivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>VFderivative(</strong> xy, z, r1, r2 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L373-L406 target=_blank>[source]</a></th></tr></thead></table>
Calculate the derivatives for the visible fraction to xy and z

<b>Parameters</b>

* xy  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance between overlapping circles
* z  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance of star 2 to the sky plane
* r1  :  float or array
<br>&nbsp;&nbsp;&nbsp;&nbsp; radius of star 1
* r2  :  float or array
<br>&nbsp;&nbsp;&nbsp;&nbsp; radius of star 2

<b>Returns</b>

( dV1dx, dV2dx, dV1dz, dV2dz )
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of the visibility to xy and z


<a name="VFpartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>VFpartial(</strong> xy, z, r1, r2 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L408-L457 target=_blank>[source]</a></th></tr></thead></table>
Calculate the partial derivatives for the visible fraction to r1 and r2.

<b>Parameters</b>

* xy  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance between overlapping circles
* z  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance of star 2 to the sky plane
* r1  :  float or array
<br>&nbsp;&nbsp;&nbsp;&nbsp; radius of star 1
* r2  :  float or array
<br>&nbsp;&nbsp;&nbsp;&nbsp; radius of star 2

<b>Returns</b>

( dV1dr1, dV2dr1, dV1dr2, dV2dr2 )
<br>&nbsp;&nbsp;&nbsp;&nbsp; partials of the visibility to r1 and r2


<a name="overlap"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>overlap(</strong> xy, r1, r2 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L459-L495 target=_blank>[source]</a></th></tr></thead></table>
Calculate the overlap area between two partially overlapping circles

From: https://scipython.com/books/book2/chapter-8-scipy/problems/overlapping-circles/

<b>Parameters</b>

* xy  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance between overlapping circles
* r1  :  float or array
<br>&nbsp;&nbsp;&nbsp;&nbsp; radius of circle 1
* r2  :  float or array
<br>&nbsp;&nbsp;&nbsp;&nbsp; radius of circle 2

<a name="spotIllumination"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>spotIllumination(</strong> xy, z, params ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L497-L538 target=_blank>[source]</a></th></tr></thead></table>
Illumination of the stars on each other.
Depending on distance between stars and aspect angle

The algoritm is taken from DOI: 10.5817/OEJV2025-0258

<b>Parameters</b>

* xy  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance between the stars in the sky plane
* z  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance of star 2 to the sky plane
* params  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters of the model


<a name="tidalDistortion"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>tidalDistortion(</strong> xy, z, params ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L540-L599 target=_blank>[source]</a></th></tr></thead></table>
Calculate the tidal distortion of the stars in a binary system
as elongated, prolate spheroids (cigars).

from: https://farside.ph.utexas.edu/teaching/355/Surveyhtml/node69.html
Equation. (1.468) (for as long as it lasts)

<b>Parameters</b>

* xy  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance between the stars in the sky plane
* z  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance of star 2 to the sky plane
* params  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters of the model

<b>Returns</b>

( a1, b1, a2, b2 )
<br>&nbsp;&nbsp;&nbsp;&nbsp; apparent stretch and squeeze of both stars

<a name="basePartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>basePartial(</strong> xdata, params, parlist=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L601-L657 target=_blank>[source]</a></th></tr></thead></table>
Returns the partials at the input value.

x,y,z = SOM(t:p1)

r = S(x,y,z) = ( SQRT( x*x + y*y ), z )

F(t:p,q) = SOM(t:p) | R(x,y,z:) | LC(r,z:q)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = LC( R( SOM( t:p ) ):q )
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; H(G(x:p):q)

dF/dq = dLC( R( SOM(t:p)))/dq

dF/dp = dLC/drz * dRZ/dxyz * dSOM/dp

<b>Parameters</b>

* xdata  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result
* params  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.
* parlist  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of indices active parameters (or None for all)


<a name="baseDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseDerivative(</strong> xdata, params )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L659-L685 target=_blank>[source]</a></th></tr></thead></table>
Returns the derivative of f to t (dfdt) at the input values.

<b>Parameters</b>

* xdata  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; times at which to calculate the result
* params  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.


<a name="OVpartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>OVpartial(</strong> xy, r1, r2 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L687-L738 target=_blank>[source]</a></th></tr></thead></table>
calculate the partials of overlap to r1 and r2.

<b>Parameters</b>

* xy  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; projected distance between stars
* r1  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; radius of star 1
* r2  :  array

<br>&nbsp;&nbsp;&nbsp;&nbsp; radius of star 2
dOdr1 = numpy.where( r1 > r2, 0.0,  
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; numpy.where( xy < r1 + r2, 2 * math.pi * r1, 0.0 ) )
dOdr2 = numpy.where( r1 < r2, 0.0,  
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; numpy.where( xy < r1 + r2, 2 * math.pi * r2, 0.0 ) )

q = numpy.where( ( xy > abs( r1 - r2 ) ) & ( xy < r1 + r2 ) )[0]

xyq = xy[q]
r1 = r1[q]
r2 = r2[q]

d2 = xyq * xyq
rr1 = r1 * r1
rr2 = r2 * r2

r2d = xyq * numpy.sqrt( 1 - ( d2 - rr1 + rr2 )**2 / ( 4 * rr2 * d2 ) )
dAdr1 = r1 / ( r2 * r2d )
dAdr2 = ( d2 - rr1 - rr2 ) / ( 2 * rr2 * r2d )

r1d = xyq * numpy.sqrt( 1 - ( d2 - rr2 + rr1 )**2 / ( 4 * rr1 * d2 ) )
dBdr1 = ( d2 - rr1 - rr2 ) / ( 2 * rr1 * r1d )
dBdr2 = r2 / ( r1 * r1d )

alfa = numpy.arccos( ( d2 + rr2 - rr1 ) / ( 2 * xyq * r2 ) )
beta = numpy.arccos( ( d2 + rr1 - rr2 ) / ( 2 * xyq * r1 ) )

dOdA = rr2 * ( 1 - numpy.cos( 2 * alfa ) )
dOdB = rr1 * ( 1 - numpy.cos( 2 * beta ) )

dr1 = ( 2 * beta - numpy.sin( 2 * beta ) ) * r1
dr2 = ( 2 * alfa - numpy.sin( 2 * alfa ) ) * r2

dr1 += dOdA * dAdr1 + dOdB * dBdr1
dr2 += dOdA * dAdr2 + dOdB * dBdr2

dOdr1[q] = dr1
dOdr2[q] = dr2

return ( dOdr1, dOdr2 )

<a name="SIpartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>SIpartial(</strong> xy, z, params, surface=(1,1) ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L740-L809 target=_blank>[source]</a></th></tr></thead></table>

SIpartial( self, xy, z, params, surface=(1,1) ) 
ones = numpy.ones<sub>like</sub>( z )
zero = numpy.zeros<sub>like</sub>( z )

if not self.spot 
<br>&nbsp;&nbsp;&nbsp;&nbsp; return ( zero, zero, ones*surface[0], zero, zero,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; zero, zero, zero, ones*surface[1], zero )

spot = self.spot

r1 = self.getParameterValue( params, "radius<sub>1</sub>" )
r2 = self.getParameterValue( params, "radius<sub>2</sub>" )
f1 = self.getParameterValue( params, "lumen<sub>1</sub>" )
f2 = self.getParameterValue( params, "lumen<sub>2</sub>" )
fs = self.getParameterValue( params, "spot" )

rr1 = r1 * r1
rr2 = r2 * r2

d2 = xy * xy + z * z
d = numpy.sqrt( d2 )

## F2 = f2 + fs * f1 * ( 1 - z / d ) * ( rr1 / d2 ) ** spot
## F1 = f1 + fs * f2 * ( 1 + z / d ) * ( rr2 / d2 ) ** spot

sifrac = surface[1] * ( 1 - z / d ) / ( d2 ** spot )

dF2dr1 = fs * f1 * sifrac * 2 * spot * r1 ** (2 * spot - 1)
dF2dr2 = zero
sifrac *= rr1 ** spot
dF2df1 = fs * sifrac
dF2df2 = ones * surface[1]
dF2dfs = f1 * sifrac

sifrac = surface[0] * ( 1 + z / d ) / ( d2 ** spot )

dF1dr1 = zero
dF1dr2 = fs * f2 * sifrac * 2 * spot * r2 ** ( 2 * spot - 1 ) 
dF1df1 = ones * surface[0]
sifrac *= rr2 ** spot
dF1df2 = fs * sifrac
dF1dfs = f2 * sifrac

return ( dF1dr1, dF1dr2, dF1df1, dF1df2, dF1dfs, 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; dF2dr1, dF2dr2, dF2df1, dF2df2, dF2dfs )


<a name="LCpartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>LCpartial(</strong> xy, z, params ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L811-L920 target=_blank>[source]</a></th></tr></thead></table>

LCpartial( self, xy, z, params ) 
## radii and luminosities of both stars
r1 = self.getParameterValue( params, "radius<sub>1</sub>" )
r2 = self.getParameterValue( params, "radius<sub>2</sub>" )

## tidalDistortion : partials
tdresult = self.tidalDistortion( xy, z, params )
tdpart = self.TDpartial( xy, z, params, TDresult=tdresult )

self.assertParts( xy, z, params, tdpart, debug=1 )

a1, b1, a2, b2 = tdresult
da1dm, db1dm, da2dm, db2dm, da1dr, db1dr, da2dr, db2dr = tdpart

ra1 = a1 * r1
ra2 = a2 * r2

V1, V2 = self.visibleFraction( xy, z, ra1, ra2 )
dV1dra1, dV2dra1, dV1dra2, dV2dra2 = self.VFpartial( xy, z, ra1, ra2 )


## partials to mass<sub>1</sub>
dV1dm1 = dV1dra1 * r1 * da1dm + dV1dra2 * r2 * da2dm
dV2dm1 = dV2dra1 * r1 * da1dm + dV2dra2 * r2 * da2dm

## convert from partials to ra1,ra2 to partials to r1,r2
dra1dr1 = a1 + r1 * da1dr
dra2dr2 = a2 + r2 * da2dr

dV1dr1 = dV1dra1 * dra1dr1 
dV1dr2 = dV1dra2 * dra2dr2 
dV2dr1 = dV2dra1 * dra1dr1 
dV2dr2 = dV2dra2 * dra2dr2 

self.assertParts( xy, z, params, 
<br>&nbsp;&nbsp;&nbsp;&nbsp; ( dV1dr1, dV2dr1, dV1dr2, dV2dr2, dV1dm1, dV2dm1 ), debug=2 )


## spotIllumination : partials with effects of tidalDistortion
F1, F2 = self.spotIllumination( xy, z, params )
surface1 = a1 * b1                            ## normalized star surface
surface2 = a2 * b2                            ## normalized star surface

sipart = self.SIpartial( xy, z, params )

self.assertParts( xy, z, params, sipart, debug=3 )

sipart = tuple( [df * surface1 for df in sipart[:5]] + 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [df * surface2 for df in sipart[5:]] )

( dF1dr1, dF1dr2, dF1df1, dF1df2, dF1dfs, 
<br>&nbsp;&nbsp; dF2dr1, dF2dr2, dF2df1, dF2df2, dF2dfs ) = sipart

dS1dr1 = a1 * db1dr + b1 * da1dr
dS2dr2 = a2 * db2dr + b2 * da2dr

dF1dr1 += F1 * dS1dr1
dF2dr2 += F2 * dS2dr2

dF1dm1 = F1 * ( a1 * db1dm + b1 * da1dm )
dF2dm1 = F2 * ( a2 * db2dm + b2 * da2dm )

self.assertParts( xy, z, params, 
<br>&nbsp;&nbsp;&nbsp;&nbsp; ( dF1dr1, dF1dr2, dF1df1, dF1df2, dF1dfs, dF1dm1, 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; dF2dr1, dF2dr2, dF2df1, dF2df2, dF2dfs, dF2dm1 ), debug=4 )

F1 *= surface1
F2 *= surface2

## lightCurve : partials
## LC = V1 * F1 + V2 * F2
## dLCdp = dV1dp * F1 + V1 * dF1dp + dV2dp * F2 + V2 * dF2dp
dLCdr1 = dV1dr1 * F1 + V1 * dF1dr1 + dV2dr1 * F2 + V2 * dF2dr1
dLCdr2 = dV1dr2 * F1 + V1 * dF1dr2 + dV2dr2 * F2 + V2 * dF2dr2
dLCdf1 = V1 * dF1df1 + V2 * dF2df1
dLCdf2 = V1 * dF1df2 + V2 * dF2df2

dLCdp = numpy.append( dLCdr1, dLCdr2 )
dLCdp = numpy.append( dLCdp, dLCdf1 )
dLCdp = numpy.append( dLCdp, dLCdf2 )
ksh = 4

if self.spot 
<br>&nbsp;&nbsp;&nbsp;&nbsp; dLCdfs = V1 * dF1dfs + V2 * dF2dfs
<br>&nbsp;&nbsp;&nbsp;&nbsp; dLCdp = numpy.append( dLCdp, dLCdfs )
<br>&nbsp;&nbsp;&nbsp;&nbsp; ksh += 1

if self.tides 
<br>&nbsp;&nbsp;&nbsp;&nbsp; dLCdm1 = dV1dm1 * F1 + V1 * dF1dm1 + dV2dm1 * F2 + V2 * dF2dm1
<br>&nbsp;&nbsp;&nbsp;&nbsp; dLCdp = numpy.append( dLCdp, dLCdm1 )
<br>&nbsp;&nbsp;&nbsp;&nbsp; ksh += 1

dLCdp = dLCdp.reshape( ( ksh, -1 ) ).T

self.assertParts( xy, z, params, dLCdp, debug=5, doprint=False )

return dLCdp


<a name="TDpartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>TDpartial(</strong> xy, z, params, TDresult=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L922-L1021 target=_blank>[source]</a></th></tr></thead></table>

TDpartial( self, xy, z, params, TDresult=None ) 
if not self.tides 
<br>&nbsp;&nbsp;&nbsp;&nbsp; zr = numpy.zeros<sub>like</sub>( z )
<br>&nbsp;&nbsp;&nbsp;&nbsp; return ( zr, zr, zr, zr, zr, zr, zr, zr )

if TDresult is None 
<br>&nbsp;&nbsp;&nbsp;&nbsp; a1, b1, a2, b2 = self.tidalDistortion( xy, z, params )
else 
<br>&nbsp;&nbsp;&nbsp;&nbsp; a1, b1, a2, b2 = TDresult
t1, t2 = self.truemajor

r1 = self.getParameterValue( params, "radius<sub>1</sub>" )
r2 = self.getParameterValue( params, "radius<sub>2</sub>" )
m1 = self.getParameterValue( params, "mass<sub>1</sub>" )

mr = ( 1 - m1 ) / m1
dmrdm = - 1 / ( m1 * m1 )

r1c = r1 * r1 * r1
r2c = r2 * r2 * r2

xy2 = xy * xy
z2  = z * z
rho2 = xy2 + z2
rho = numpy.sqrt( rho2 )
rho3 = rho * rho2

## eps : flattening of the sphere
eps1 = 3.75 * mr * r1c / rho3
eps2 = 3.75 / mr * r2c / rho3

de1dr = 11.25 * mr * r1 * r1 / rho3 
de2dr = 11.25 / mr * r2 * r2 / rho3
de1dm =  3.75 * r1c * dmrdm / rho3
de2dm = -3.75 * r2c * dmrdm / ( rho3 * mr * mr )

## use approximation that cannot go negative when eps > 1
# b1 = ( 1 + eps1 ) ** ( -1 / 3 )
# b2 = ( 1 + eps2 ) ** ( -1 / 3 )

# db1de = -( 1 / 3 ) * ( 1 + eps1 ) ** ( -4/3 )
# db2de = -( 1 / 3 ) * ( 1 + eps2 ) ** ( -4/3 )

## use flattening as b = a ( 1 - eps )
## and a * b * b = r**3
# b1 = ( 1 - eps1 ) ** ( 1 / 3 )
# b2 = ( 1 - eps2 ) ** ( 1 / 3 )

db1de = -( 1 / 3 ) * ( 1 - eps1 ) ** ( -2/3 )
db2de = -( 1 / 3 ) * ( 1 - eps2 ) ** ( -2/3 )
db1dr = db1de * de1dr 
db1dm = db1de * de1dm
db2dr = db2de * de2dr
db2dm = db2de * de2dm

# t1 = 1 / (b1*b1)                    ## true major factor for star 1
# t2 = 1 / (b2*b2)                    ## true major factor for star 2

dt1db = -2 / b1**3
dt2db = -2 / b2**3

dt1dr = dt1db * db1dr
dt1dm = dt1db * db1dm
dt2dr = dt2db * db2dr
dt2dm = dt2db * db2dm

## Apparent major axis is the projection along theta
## a1 = numpy.hypot( t1 * xy, b1 * z ) / rho
## a1 = sqrt( t1**2 * xy**2 + b1**2 * z**2 ) / rho
## dadp = ( xy**2 * t * dtdp + z**2 * b * dbdp ) / ( rho * sqrt() )

rsr1 = rho * numpy.hypot( t1 * xy, b1 * z )
rsr2 = rho * numpy.hypot( t2 * xy, b2 * z )

da1dm = ( xy2 * t1 * dt1dm + z2 * b1 * db1dm ) / rsr1
da1dr = ( xy2 * t1 * dt1dr + z2 * b1 * db1dr ) / rsr1
da2dm = ( xy2 * t2 * dt2dm + z2 * b2 * db2dm ) / rsr2
da2dr = ( xy2 * t2 * dt2dr + z2 * b2 * db2dr ) / rsr2

return ( da1dm, db1dm, da2dm, db2dm, 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; da1dr, db1dr, da2dr, db2dr )

<a name="OVderivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>OVderivative(</strong> xy, r1, r2 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L1023-L1056 target=_blank>[source]</a></th></tr></thead></table>

OVderivative( self, xy, r1, r2 ) 


<a name="LCderivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>LCderivative(</strong> xy, z, params ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L1058-L1139 target=_blank>[source]</a></th></tr></thead></table>
Return derivative of LightCurve to xy and z, as 

<b>Parameters</b>

* xy  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance between the stars in the sky plane
* z  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance of star 2 to the sky plane
* params  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters of the model

<a name="SIderivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>SIderivative(</strong> xy, z, params, surface=(1,1) ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L1141-L1212 target=_blank>[source]</a></th></tr></thead></table>
Returns derivatives of the SpotIllimunation.
Specificly of the modified f1 and f2 to xy and z 

<b>Parameters</b>

* xy  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance between the stars in the sky plane
* z  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance of star 2 to the sky plane
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.
* surface  :  tuple of 2 array
<br>&nbsp;&nbsp;&nbsp;&nbsp; normalized surface areas of the stars

<b>Returns</b>

( dF1dx, dF2dx, dF1dz, dF2dz )


<a name="TDderivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>TDderivative(</strong> xy, z, params, TDresult=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L1214-L1306 target=_blank>[source]</a></th></tr></thead></table>
Calculate the derivative of the tidal distortion to xy and z

<b>Parameters</b>

* xy  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance between the stars in the sky plane
* z  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance of star 2 to the sky plane
* params  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters of the model
* TDresult  :  tuple
<br>&nbsp;&nbsp;&nbsp;&nbsp; result of call tp tidalDostortion

<b>Returns</b>

( da1dx, db1dx, da2dx, db2dx, da1dz, db1dz, da2dz, db2dz )
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of apparent major and minor axes to xy and z

<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L1308-L1327 target=_blank>[source]</a></th></tr></thead></table>
Returns a string representation of the model.


<a name="reportParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportParameters(</strong> param, stdevs=None, toMags=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L1329-L1521 target=_blank>[source]</a></th></tr></thead></table>
Print parameters and stdevs (if present)

<b>Parameters</b>

* param  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be converted and printed
* stdevs  :  array 
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be converted and printed
* toMags  :  bool or float (False)
<br>&nbsp;&nbsp;&nbsp;&nbsp; true    convert luminosities to magnitudes
<br>&nbsp;&nbsp;&nbsp;&nbsp; float   true and use number as scaling factor
m1 = param[k]
m2 = param[k+1]
if toMags 
<br>&nbsp;&nbsp;&nbsp;&nbsp; fm = float( toMags )
<br>&nbsp;&nbsp;&nbsp;&nbsp; m1 = -2.512 * math.log10( m1 * fm )
<br>&nbsp;&nbsp;&nbsp;&nbsp; m2 = -2.512 * math.log10( m2 * fm )
<br>&nbsp;&nbsp;&nbsp;&nbsp; print( fm, m1, m2 )

print( "%-12.12s : %10.3f" % ( self.getParameterName( k ), m1 ) )
print( "%-12.12s : %10.3f" % ( self.getParameterName( k+1 ), m2 ) )

k += 2

<a name="assertPrint"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>assertPrint(</strong> df, nm, tol, msg, doprint=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/EclipsingStarModel.py#L1523-L1592 target=_blank>[source]</a></th></tr></thead></table>

Endline #L1594
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./NonLinearModel.html">NonLinearModel</a></th></tr></thead></table>


* [<strong>setMixedModel(</strong> lindex )](./NonLinearModel.md#setMixedModel)
* [<strong>isMixed(</strong> )](./NonLinearModel.md#isMixed)
* [<strong>getNonLinearIndex(</strong> )](./NonLinearModel.md#getNonLinearIndex)
* [<strong>partial(</strong> xdata, param=None, useNum=False )](./NonLinearModel.md#partial)


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Model.html">Model</a></th></tr></thead></table>


* [<strong>chainLength(</strong> )](./Model.md#chainLength)
* [<strong>isNullModel(</strong> ) ](./Model.md#isNullModel)
* [<strong>isolateModel(</strong> k )](./Model.md#isolateModel)
* [<strong>addModel(</strong> model )](./Model.md#addModel)
* [<strong>subtractModel(</strong> model )](./Model.md#subtractModel)
* [<strong>multiplyModel(</strong> model )](./Model.md#multiplyModel)
* [<strong>divideModel(</strong> model )](./Model.md#divideModel)
* [<strong>pipeModel(</strong> model )](./Model.md#pipeModel)
* [<strong>appendModel(</strong> model, operation )](./Model.md#appendModel)
* [<strong>correctParameters(</strong> params )](./Model.md#correctParameters)
* [<strong>result(</strong> xdata, param=None )](./Model.md#result)
* [<strong>operate(</strong> res, pars, next )](./Model.md#operate)
* [<strong>derivative(</strong> xdata, param, useNum=False )](./Model.md#derivative)
* [<strong>selectPipe(</strong> ndim, ninter, ndout ) ](./Model.md#selectPipe)
* [<strong>pipe_0(</strong> dGd, dHdG ) ](./Model.md#pipe_0)
* [<strong>pipe_1(</strong> dGd, dHdG ) ](./Model.md#pipe_1)
* [<strong>pipe_2(</strong> dGd, dHdG ) ](./Model.md#pipe_2)
* [<strong>pipe_3(</strong> dGd, dHdG ) ](./Model.md#pipe_3)
* [<strong>pipe_4(</strong> dGdx, dHdG ) ](./Model.md#pipe_4)
* [<strong>pipe_5(</strong> dGdx, dHdG ) ](./Model.md#pipe_5)
* [<strong>pipe_6(</strong> dGdx, dHdG ) ](./Model.md#pipe_6)
* [<strong>pipe_7(</strong> dGdx, dHdG ) ](./Model.md#pipe_7)
* [<strong>pipe_8(</strong> dGdx, dHdG ) ](./Model.md#pipe_8)
* [<strong>pipe_9(</strong> dGdx, dHdG ) ](./Model.md#pipe_9)
* [<strong>shortName(</strong> ) ](./Model.md#shortName)
* [<strong>getNumberOfParameters(</strong> )](./Model.md#getNumberOfParameters)
* [<strong>numDerivative(</strong> xdata, param )](./Model.md#numDerivative)
* [<strong>numPartial(</strong> xdata, param )](./Model.md#numPartial)
* [<strong>isDynamic(</strong> ) ](./Model.md#isDynamic)
* [<strong>hasPriors(</strong> isBound=True ) ](./Model.md#hasPriors)
* [<strong>getPrior(</strong> kpar )](./Model.md#getPrior)
* [<strong>setPrior(</strong> kpar, prior=None, **kwargs )](./Model.md#setPrior)
* [<strong>getParameterName(</strong> kpar )](./Model.md#getParameterName)
* [<strong>getParameterUnit(</strong> kpar )](./Model.md#getParameterUnit)
* [<strong>getIntegralUnit(</strong> )](./Model.md#getIntegralUnit)
* [<strong>setLimits(</strong> lowLimits=None, highLimits=None )](./Model.md#setLimits)
* [<strong>getLimits(</strong> ) ](./Model.md#getLimits)
* [<strong>hasLimits(</strong> fitindex=None )](./Model.md#hasLimits)
* [<strong>unit2Domain(</strong> uvalue, kpar=None )](./Model.md#unit2Domain)
* [<strong>domain2Unit(</strong> dvalue, kpar=None )](./Model.md#domain2Unit)
* [<strong>partialDomain2Unit(</strong> dvalue )](./Model.md#partialDomain2Unit)
* [<strong>nextPrior(</strong> ) ](./Model.md#nextPrior)
* [<strong>getLinearIndex(</strong> )](./Model.md#getLinearIndex)
* [<strong>testPartial(</strong> xdata, params, silent=True )](./Model.md#testPartial)
* [<strong>strictNumericPartial(</strong> xdata, params, parlist=None ) ](./Model.md#strictNumericPartial)
* [<strong>assignDF1(</strong> partial, i, dpi ) ](./Model.md#assignDF1)
* [<strong>assignDF2(</strong> partial, i, dpi ) ](./Model.md#assignDF2)
* [<strong>strictNumericDerivative(</strong> xdata, param ) ](./Model.md#strictNumericDerivative)


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./FixedModel.html">FixedModel</a></th></tr></thead></table>


* [<strong>select(</strong> params ) ](./FixedModel.md#select)
* [<strong>selectNames(</strong> names ) ](./FixedModel.md#selectNames)
* [<strong>expand(</strong> xdata, param ) ](./FixedModel.md#expand)


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./BaseModel.html">BaseModel</a></th></tr></thead></table>


* [<strong>checkParameter(</strong> param ) ](./BaseModel.md#checkParameter)
* [<strong>checkPositive(</strong> param ) ](./BaseModel.md#checkPositive)
* [<strong>checkZeroParameter(</strong> param )](./BaseModel.md#checkZeroParameter)
* [<strong>isModifiable(</strong> ) ](./BaseModel.md#isModifiable)
* [<strong>basePrior(</strong> kpar ) ](./BaseModel.md#basePrior)
* [<strong>baseParameterName(</strong> kpar ) ](./BaseModel.md#baseParameterName)
* [<strong>baseParameterUnit(</strong> kpar ) ](./BaseModel.md#baseParameterUnit)
