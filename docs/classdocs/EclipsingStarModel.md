---
---
<br><br>

<a name="EclipsingStarModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class EclipsingStarModel(</strong> <a href="./NonLinearModel.html">NonLinearModel</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source// target=_blank>[source]</a></th></tr></thead></table>
<p>

Model for the light curve of an eclipsing double star, as a function of time, t. 

| par | symbol | name         | description               | limits     | comment      |
|-----|--------|--------------|---------------------------|------------|--------------|
| p<sub>0</sub> |   e    | eccentricity | of the elliptic orbit     | 0<e<1      | 0 is circular |
| p<sub>1</sub> |   P    | period       | of the velocity variation |   P>0      |  |
| p<sub>2</sub> |   T    | phase        | phase until t = 0         | 0<T<2&pi;  |  |
| p<sub>3</sub> |   i    | inclination  | of orbit (close to 90)    | 0<i<&pi;   |  |
| p<sub>4</sub> | &omega;| longitude    | from north to periastron  | 0<&omega;<2&pi; |  |
| p<sub>5</sub> |   r1   | radius<sub>1</sub>     | radius of star 1          | 0<r1<1     |  |
| p<sub>6</sub> |   r2   | radius<sub>2</sub>     | radius of star 2          | 0<r2<1     |  |
| p<sub>7</sub> |   f1   | lumen<sub>1</sub>      | luminosity of star 1      |            |  |
| p<sub>8</sub> |   f2   | lumen<sub>2</sub>      | luminosity of star 2      |            |  |
| p<sub>9</sub> |   fs   | spot         | spot illumination         | fs >= 0    | 0 is no spot |
| p<sub>10</sub>|   m1   | mass<sub>1</sub>       | relative mass of star 1   | 0 < m1 < 1 | m2 = 1 - m1 |

The amplitude (semimajor axis) is set to 1.0. Both stellar radii are given 
as a fraction of the amplitude. The mass of star 2 is ( 1 - m1 ). The mass ratio
is used in calculating the tidal distortion.

When the sum of the radii, p<sub>5</sub> + p<sub>6</sub>, is larger than the periastron distance,
1 - p<sub>0</sub>, the stars clash.

When the model is constructed as circular, the parameter p<sub>0</sub> becomes 0 by 
definition and p<sub>4</sub> looses its meaning. They are removed from the model.

This class uses [StellarOrbitModel](./StellarOrbitModel.md) to find the true orbit

The parameters are initialized at 
<br>&nbsp;&nbsp;&nbsp;&nbsp; [0.0, 1.0, 0.0, pi/2, 0.0, 0.1, 0.1, 1.0, 1.0, 0.0, 0.5].
It is a non-linear model.

For the mathematics of this model and further explanation see [EclipsingStars.html.](EclipsingStars.html.)

(Partial) derivatives were obtained with the help of  
[www.derivative-calculator.net](www.derivative-calculator.net)
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
* occultation  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; True: eclipses stricty enforced
* fixpar  :  lambda function
<br>&nbsp;&nbsp;&nbsp;&nbsp; to provide parameters for StellarOrbitModel

<b>Examples</b>

    esm = EclipsingStarModel( spot=True, tides=True )
    print( esm.npars )
    10



<a name="EclipsingStarModel"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>EclipsingStarModel(</strong> circular=False, spot=False, tides=False, occultation=True,
 copy=None, **kwargs )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L105-L172 target=_blank>[source]</a></th></tr></thead></table>

Radial velocity model.

Number of parameters depends on the settings of ( False or True ) of 
<br>&nbsp; circular       spot        tides
( 9 or 6 ) + ( 0 or 1 ) + ( 0 or 1 )

<b>Parameters</b>

* circular  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; stellar orbit is circular: eccentricity = 0 ==> lonod = 0
* spot  :  bool or number
<br>&nbsp;&nbsp;&nbsp;&nbsp; apply spot illumination; more pronounced when spot > 1
* tides  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; apply tidal distortion
* occultation  :  bool (True)
<br>&nbsp;&nbsp;&nbsp;&nbsp; eclipses are stricty enforced
* copy  :  EclipsingStarModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to copy

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L174-L179 target=_blank>[source]</a></th></tr></thead></table>
Copy method.  

<a name="distanceConstraint"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>distanceConstraint(</strong> logL, problem, allpars, lowLhood ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L181-L198 target=_blank>[source]</a></th></tr></thead></table>
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
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L200-L268 target=_blank>[source]</a></th></tr></thead></table>
Get extra prior for this combination of parameters.

<b>Parameters</b>

* allpars  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; all parameters involved in the problem

<a name="baseResult"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseResult(</strong> xdata, params )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L270-L288 target=_blank>[source]</a></th></tr></thead></table>
Returns the result of the model function.


<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values at which to calculate the result
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.


<a name="lightCurve"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>lightCurve(</strong> xy, z, params, debug=0 )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L290-L342 target=_blank>[source]</a></th></tr></thead></table>
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
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L344-L370 target=_blank>[source]</a></th></tr></thead></table>
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
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L372-L405 target=_blank>[source]</a></th></tr></thead></table>
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
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L407-L456 target=_blank>[source]</a></th></tr></thead></table>
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
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L458-L494 target=_blank>[source]</a></th></tr></thead></table>
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
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L496-L537 target=_blank>[source]</a></th></tr></thead></table>
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
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L539-L598 target=_blank>[source]</a></th></tr></thead></table>
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
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L600-L656 target=_blank>[source]</a></th></tr></thead></table>
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
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L658-L684 target=_blank>[source]</a></th></tr></thead></table>
Returns the derivative of f to t (dfdt) at the input values.

<b>Parameters</b>

* xdata  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; times at which to calculate the result
* params  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.


<a name="OVpartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>OVpartial(</strong> xy, r1, r2 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L686-L738 target=_blank>[source]</a></th></tr></thead></table>
calculate the partials of overlap to r1 and r2.

<b>Parameters</b>

* xy  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; projected distance between stars
* r1  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; radius of star 1
* r2  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; radius of star 2


<a name="SIpartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>SIpartial(</strong> xy, z, params, surface=(1,1) ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L740-L809 target=_blank>[source]</a></th></tr></thead></table>
Returns partials of the SpotIllumination.
Specificly of the modified f1 and f2 to params[-5:] 
(radius<sub>1</sub>, radius<sub>2</sub>, lumen<sub>1</sub>, lumen<sub>2</sub>, spot) 

If no spot illumination is requested, the dF*dfs are returned as zero.

<b>Parameters</b>

* xy  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance between the stars in the sky plane
* z  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance of star 2 to the sky plane
* params  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.
* surface  :  tuple of arrays
<br>&nbsp;&nbsp;&nbsp;&nbsp; normalized surface areas of the stars

<b>Returns</b>

( dF1dr1, dF1dr2, dF1df1, dF1df2, dF1dfs,
<br>&nbsp;&nbsp; dF2dr1, dF2dr2, dF2df1, dF2df2, dF2dfs )


<a name="LCpartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>LCpartial(</strong> xy, z, params ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L811-L920 target=_blank>[source]</a></th></tr></thead></table>
Return partial derivatives of LightCurve to each of the parameters

<b>Parameters</b>

* xy  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance between the stars in the sky plane
* z  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance of star 2 to the sky plane
* params  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters of the model

<a name="TDpartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>TDpartial(</strong> xy, z, params, TDresult=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L922-L1021 target=_blank>[source]</a></th></tr></thead></table>
Calculate partials of the tidal distortion to the distortion parameter

<b>Parameters</b>

* xy  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance between the stars in the sky plane
* z  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; distance of star 2 to the sky plane
* params  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters of the model
* TDresult  :  None or tuple
<br>&nbsp;&nbsp;&nbsp;&nbsp; result of a call to tidalDistortion

<b>Returns</b>

* ( da1dm, db1dm, da2dm, db2dm,  da1dr, db1dr, da2dr, db2dr )  :  8 arrays
<br>&nbsp;&nbsp;&nbsp;&nbsp; Partials of the normalized projected axes to the parameters

<a name="OVderivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>OVderivative(</strong> xy, r1, r2 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1023-L1057 target=_blank>[source]</a></th></tr></thead></table>
calculate the derivative of overlap to xy

<b>Parameters</b>

* xy  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; projected distance between stars
* r1  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; radius of star 1
* r2  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; radius of star 2


<a name="LCderivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>LCderivative(</strong> xy, z, params ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L105-L1729 target=_blank>[source]</a></th></tr></thead></table>
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
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1143-L1214 target=_blank>[source]</a></th></tr></thead></table>
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
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1216-L1308 target=_blank>[source]</a></th></tr></thead></table>
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
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1310-L1329 target=_blank>[source]</a></th></tr></thead></table>
Returns a string representation of the model.


<a name="reportParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>reportParameters(</strong> param, stdevs=None, toMags=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1331-L1581 target=_blank>[source]</a></th></tr></thead></table>
Print parameters and stdevs (if present)

<b>Parameters</b>

* param  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be converted and printed
* stdevs  :  array 
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be converted and printed
* toMags  :  bool or float (False)
<br>&nbsp;&nbsp;&nbsp;&nbsp; true    convert luminosities to magnitudes
<br>&nbsp;&nbsp;&nbsp;&nbsp; float   true and use number as scaling factor

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
* [<strong>getParameterIndex(</strong> parname ) ](./BaseModel.md#getParameterIndex)
* [<strong>getParameterValue(</strong> param, name, default=None ) ](./BaseModel.md#getParameterValue)
* [<strong>baseParameterName(</strong> kpar ) ](./BaseModel.md#baseParameterName)
* [<strong>baseParameterUnit(</strong> kpar ) ](./BaseModel.md#baseParameterUnit)
