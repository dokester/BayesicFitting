---
---
<br><br>

<a name="Kepplers2ndLaw"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Kepplers2ndLaw(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Kepplers2ndLaw.py target=_blank>Source</a></th></tr></thead></table>

Class for calculating Kepplers second law for planetary motion.

The projection of the orbit on the sky is not included in this class.

The algorithm was taken from [Boule](../references.md#boule).

| param | abbr | name                   | limits    | comment     |
|:-----:|:----:|:-----------------------|:---------:|:------------| 
|   0   |  e   | eccentricity of orbit  | 0<e<1     | 0: circular |
|   1   |  a   | semi major axis        |   a>0     |             |
|   2   |  P   | period of the orbit    |   P>0     |             |
|   3   |  T   | phase since periastron | 0<T<2&pi; |             |

The parameters are initialized at [0.0, 1.0, 1.0, 0.0].


<a name="meanAnomaly"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>meanAnomaly(</strong> xdata, params ) 
</th></tr></thead></table>

Return the mean anomaly.

P = params[2] = period
T = params[3] = periastron passage

M = 2 * pi * xdata / P - T

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; times in the orbit
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters: eccentr, semimajor, period, ppass

<a name="dMdx"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>dMdx(</strong> xdata, params ) 
</th></tr></thead></table>
Return derivatives of M (mean anomaly) to xdata

<b>Returns</b>

* dMdx  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of M to x (xdata)

<a name="dMdpar"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>dMdpar(</strong> xdata, params ) 
</th></tr></thead></table>
Return derivatives of M (mean anomaly) to relevant parameters.

<b>Returns</b>

* dMdP  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of M to P (period)
* dMdp  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of M to p (phase of periastron)

<a name="eccentricAnomaly"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>eccentricAnomaly(</strong> xdata, params, Estart=None ) 
</th></tr></thead></table>
Take the best one : Halleys method

It converges in a few iterations for e <= 0.999999999

<a name="eccentricAnomaly0"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>eccentricAnomaly0(</strong> xdata, params ) 
</th></tr></thead></table>
Return the eccentric anomaly, i.e. the solution for E of

Standard method by Jean Meuss 
<br>&nbsp; Astronomical Algorithms, 2nd ed.,
<br>&nbsp; Willmann-Bell, Inc, Virginia, 193-196, 397-399

e = params[0] = eccentricity
M = mean anomaly

E = M + e * sin( E )

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; times in the orbit
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters: eccentr, semimajor, period, ppass

<a name="eccentricAnomaly1"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>eccentricAnomaly1(</strong> xdata, params ) 
</th></tr></thead></table>
Newtons method.

Return the eccentric anomaly, i.e. the solution for E of

e = params[0] = eccentricity
M = mean anomaly

E = M + e * sin( E )

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; times in the orbit
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters: eccentr, semimajor, period, ppass

<a name="eccentricAnomaly2"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>eccentricAnomaly2(</strong> xdata, params, Estart=None ) 
</th></tr></thead></table>
Halleys method.

Return the eccentric anomaly, i.e. the solution for E of

e = params[0] = eccentricity
M = mean anomaly

E = M + e * sin( E )

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; times in the orbit
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters: eccentr, semimajor, period, phase
* Estart  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; starting values for E

<a name="dEdM"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>dEdM(</strong> xdata, params, cosE ) 
</th></tr></thead></table>
Return derivatives of E (eccentric anomaly) to mean anomaly

<b>Returns</b>

* dEdM  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of E to M (mean anomaly)

<a name="dEdx"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>dEdx(</strong> xdata, params, cosE ) 
</th></tr></thead></table>
Return derivatives of E (eccentric anomaly) to xdata

<b>Returns</b>

* dEdx  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of E to x (xdata)

<a name="dEdpar"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>dEdpar(</strong> xdata, params, cosE, sinE ) 
</th></tr></thead></table>
Return derivatives of E (eccentric anomaly) to relevant parameters.

<b>Returns</b>

* dEde  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of E to e (eccentricity)
* dEdP  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of E to P (period)
* dEdp  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of E to p (phase of periastron)

<a name="radiusAndTrueAnomaly"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>radiusAndTrueAnomaly(</strong> xdata, params ) 
</th></tr></thead></table>
Return the radius and the true anomaly.

e = params[0] = eccentricity
a = params[1] = semimajor axis
E = eccentric anomaly

r = a * ( 1 - e * cos( E ) )

v = 2 * arctan( sqrt( (1+e)/(1-e) ) * tan( E / 2 ) )

from Wikepedia => Trigoniometic Identities 
tan( E / 2 ) = sqrt( ( 1 - cos( E ) ) / ( 1 + cos( E ) ) )
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = sqrt( ( 1 - c ) * ( 1 + c ) / ( 1 + c )<sup>2</sup> )
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = sqrt( s<sup>2</sup> / ( 1 + c )<sup>2</sup> )
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = s / ( 1 + c )
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = sin( E ) / ( 1 + cos( E ) )
Avoid cases where cos( E ) is too close to -1

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; times in the orbit
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters: eccentr, semimajor, inclin, ascpos, asclon, period, ppass

<b>Returns</b>

* r  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; radius
* v  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; true anomaly


<a name="drvdE"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>drvdE(</strong> xdata, params, cosE, sinE ) 
</th></tr></thead></table>
Return derivatives of r (radius) and v (true anomaly) to eccentric anomaly

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; times in the orbit
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters: eccentr, semimajor, period, ppass
* cosE  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; cosine of E
* sinE  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; sine of E

<b>Returns</b>

* drdE  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of r to E (eccentric anomaly)
* dvdE  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of v to E (eccentric anomaly)

<a name="drvdx"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>drvdx(</strong> xdata, params, cosE, sinE ) 
</th></tr></thead></table>
Return derivatives of r (radius) and v (true anomaly) to xdata

<b>Returns</b>

* drdx  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of r to x (xdata)
* dvdx  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of v to x (xdata)

<a name="drvdpar"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>drvdpar(</strong> xdata, params, E, cosE, sinE ) 
</th></tr></thead></table>
Return derivatives of r (radius) and v (true anomaly) to relevant parameters.

<b>Returns</b>

* drde  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of r to e (eccentricity)
* drda  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of r to a (semimajor axis)
* drdP  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of r to P (period)
* drdp  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of r to p (phase of periastron)
* dvde  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of v to e (eccentricity)
* dvdP  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of v to P (period)
* dvdp  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; derivatives of v to p (phase of periastron)

<a name="getMsini"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getMsini(</strong> stellarmass ) 
</th></tr></thead></table>
Return the mass of the exoplanet in Jupiter masses.

<b>Parameters</b>

* stellarmass  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; mass of the host star in solar masses.

