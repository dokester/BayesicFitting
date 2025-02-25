---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Kepplers2ndLaw.py target=_blank>Source</a></span></div>

<a name="Kepplers2ndLaw"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class Kepplers2ndLaw(</strong> object )
</th></tr></thead></table>
<p>

Class for calculating Kepplers second law for planetary motion.

The projection of the orbit on the sky is not included in this class.

The algorithm was taken from
    Cory Boule etal. (2017) J. of Double Star Observations Vol 13 p.189.<br>

    http://www.jdso.org/volume13/number2/Harfenist_189-199.pdf<br>

p_0 : e     eccentricity of the elliptic orbit (0<e<1; 0 = circular orbit)
p_1 : a     semi major axis (>0)
p_2 : P     period of the orbit (>0)
p_3 : T     phase since periastron passage (0<p_3<2 pi)

The parameters are initialized at [0.0, 1.0, 1.0, 0.0].


<a name="meanAnomaly"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>meanAnomaly(</strong> xdata, params ) 
</th></tr></thead></table>
<p>

Return the mean anomaly.

P = params[2] = period
p = params[3] = periastron passage

M = 2 * pi * xdata / P - p

<b>Parameters</b>

* xdata  :  array_like<br>
    times in the orbit<br>
* params  :  array_like<br>
    parameters: eccentr, semimajor, period, ppass

<a name="dMdx"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>dMdx(</strong> xdata, params ) 
</th></tr></thead></table>
<p>

Return derivatives of M (mean anomaly) to xdata

<b>Returns</b>

* dMdx  :  array_like<br>
    derivatives of M to x (xdata)

<a name="dMdpar"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>dMdpar(</strong> xdata, params ) 
</th></tr></thead></table>
<p>

Return derivatives of M (mean anomaly) to relevant parameters.

<b>Returns</b>

* dMdP  :  array_like<br>
    derivatives of M to P (period)<br>
* dMdp  :  array_like<br>
    derivatives of M to p (phase of periastron)

<a name="eccentricAnomaly"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>eccentricAnomaly(</strong> xdata, params, Estart=None ) 
</th></tr></thead></table>
<p>

Take the best one : Halleys method

It converges in a few iterations for e <= 0.999999999

<a name="eccentricAnomaly0"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>eccentricAnomaly0(</strong> xdata, params ) 
</th></tr></thead></table>
<p>

Return the eccentric anomaly, i.e. the solution for E of

Standard method by Jean Meuss 
    Astronomical Algorithms, 2nd ed.,<br>
    Willmann-Bell, Inc, Virginia, 193-196, 397-399<br>

e = params[0] = eccentricity
M = mean anomaly

E = M + e * sin( E )

<b>Parameters</b>

* xdata  :  array_like<br>
    times in the orbit<br>
* params  :  array_like<br>
    parameters: eccentr, semimajor, period, ppass

<a name="eccentricAnomaly1"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>eccentricAnomaly1(</strong> xdata, params ) 
</th></tr></thead></table>
<p>

Newtons method.

Return the eccentric anomaly, i.e. the solution for E of

e = params[0] = eccentricity
M = mean anomaly

E = M + e * sin( E )

<b>Parameters</b>

* xdata  :  array_like<br>
    times in the orbit<br>
* params  :  array_like<br>
    parameters: eccentr, semimajor, period, ppass

<a name="eccentricAnomaly2"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>eccentricAnomaly2(</strong> xdata, params, Estart=None ) 
</th></tr></thead></table>
<p>

Halleys method.

Return the eccentric anomaly, i.e. the solution for E of

e = params[0] = eccentricity
M = mean anomaly

E = M + e * sin( E )

<b>Parameters</b>

* xdata  :  array_like<br>
    times in the orbit<br>
* params  :  array_like<br>
    parameters: eccentr, semimajor, period, phase<br>
* Estart  :  array_like<br>
    starting values for E

<a name="dEdM"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>dEdM(</strong> xdata, params, cosE ) 
</th></tr></thead></table>
<p>

Return derivatives of E (eccentric anomaly) to mean anomaly

<b>Returns</b>

* dEdM  :  array_like<br>
    derivatives of E to M (mean anomaly)

<a name="dEdx"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>dEdx(</strong> xdata, params, cosE ) 
</th></tr></thead></table>
<p>

Return derivatives of E (eccentric anomaly) to xdata

<b>Returns</b>

* dEdx  :  array_like<br>
    derivatives of E to x (xdata)

<a name="dEdpar"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>dEdpar(</strong> xdata, params, cosE, sinE ) 
</th></tr></thead></table>
<p>

Return derivatives of E (eccentric anomaly) to relevant parameters.

<b>Returns</b>

* dEde  :  array_like<br>
    derivatives of E to e (eccentricity)<br>
* dEdP  :  array_like<br>
    derivatives of E to P (period)<br>
* dEdp  :  array_like<br>
    derivatives of E to p (phase of periastron)

<a name="radiusAndTrueAnomaly"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>radiusAndTrueAnomaly(</strong> xdata, params ) 
</th></tr></thead></table>
<p>

Return the radius and the true anomaly.

e = params[0] = eccentricity
a = params[1] = semimajor axis
E = eccentric anomaly

r = a * ( 1 - e * cos( E ) )

v = 2 * arctan( sqrt( (1+e)/(1-e) ) * tan( E / 2 ) )

from Wikepedia => Trigoniometic Identities 
tan( E / 2 ) = sqrt( ( 1 - cos( E ) ) / ( 1 + cos( E ) ) )
             = sqrt( ( 1 - c ) * ( 1 + c ) / ( 1 + c )^2 )<br>
             = sqrt( s^2 / ( 1 + c )^2 )<br>
             = s / ( 1 + c )<br>
             = sin( E ) / ( 1 + cos( E ) )<br>
Avoid cases where cos( E ) is too close to -1

<b>Parameters</b>

* xdata  :  array_like<br>
    times in the orbit<br>
* params  :  array_like<br>
    parameters: eccentr, semimajor, inclin, ascpos, asclon, period, ppass<br>

<b>Returns</b>

* r  :  array_like<br>
    radius<br>
* v  :  array_like<br>
    true anomaly<br>


<a name="drvdE"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>drvdE(</strong> xdata, params, cosE, sinE ) 
</th></tr></thead></table>
<p>

Return derivatives of r (radius) and v (true anomaly) to eccentric anomaly

<b>Parameters</b>

* xdata  :  array_like<br>
    times in the orbit<br>
* params  :  array_like<br>
    parameters: eccentr, semimajor, period, ppass<br>
* cosE  :  array_like<br>
    cosine of E<br>
* sinE  :  array_like<br>
    sine of E<br>

<b>Returns</b>

* drdE  :  array_like<br>
    derivatives of r to E (eccentric anomaly)<br>
* dvdE  :  array_like<br>
    derivatives of v to E (eccentric anomaly)

<a name="drvdx"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>drvdx(</strong> xdata, params, cosE, sinE ) 
</th></tr></thead></table>
<p>

Return derivatives of r (radius) and v (true anomaly) to xdata

<b>Returns</b>

* drdx  :  array_like<br>
    derivatives of r to x (xdata)<br>
* dvdx  :  array_like<br>
    derivatives of v to x (xdata)

<a name="drvdpar"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>drvdpar(</strong> xdata, params, E, cosE, sinE ) 
</th></tr></thead></table>
<p>

Return derivatives of r (radius) and v (true anomaly) to relevant parameters.

<b>Returns</b>

* drde  :  array_like<br>
    derivatives of r to e (eccentricity)<br>
* drda  :  array_like<br>
    derivatives of r to a (semimajor axis)<br>
* drdP  :  array_like<br>
    derivatives of r to P (period)<br>
* drdp  :  array_like<br>
    derivatives of r to p (phase of periastron)<br>
* dvde  :  array_like<br>
    derivatives of v to e (eccentricity)<br>
* dvdP  :  array_like<br>
    derivatives of v to P (period)<br>
* dvdp  :  array_like<br>
    derivatives of v to p (phase of periastron)

<a name="getMsini"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>getMsini(</strong> stellarmass ) 
</th></tr></thead></table>
<p>

Return the mass of the exoplanet in Jupiter masses.

<b>Parameters</b>

* stellarmass  :  float<br>
    mass of the host star in solar masses.

