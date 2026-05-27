---
---
<br><br>

<a name="PeriodicScout"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class PeriodicScout(</strong> object )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PeriodicScout.py target=_blank>[source]</a></th></tr></thead></table>
<p>

Investigating scout for periodic models


<a name="PeriodicScout"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>PeriodicScout(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PeriodicScout.py#L44-L47 target=_blank>[source]</a></th></tr></thead></table>

<a name="findPeriod"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>findPeriod(</strong> days, flux, pmin=1, pmax=2, grid=1000, clip=2,
 verbose=0 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PeriodicScout.py#L49-L139 target=_blank>[source]</a></th></tr></thead></table>

Find period in  eclipsing star data.

The search periods are defined as a geometric series, from pmin to pmax with
NP points, where NP = int( grid * log10( pmax / pmin ) / math.log10( 2 ) )
That is grid points per octave from pmin to pmax.

Select eclipsing parts and find the minimum distance

<b>Parameters</b><br>
* days  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; Julian days of observation
* flux  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; measured flux
* pmin  :  float (1)
<br>&nbsp;&nbsp;&nbsp;&nbsp; smallest period to be considered
* pmax  :  float (2)
<br>&nbsp;&nbsp;&nbsp;&nbsp; largest period to be considered
* grid  :  int (1000) 
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of points per octave in pmin to pmax
* clip  :  float (2)
<br>&nbsp;&nbsp;&nbsp;&nbsp; select data below median flux minus clip * median abs deviants        
* verbose  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; 0 : silent
<br>&nbsp;&nbsp;&nbsp;&nbsp; 1 : not

<a name="downhill"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>downhill(</strong> days, flux, prs, scl, nrknots=20, tol=0.01, verbose=0 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PeriodicScout.py#L141-L206 target=_blank>[source]</a></th></tr></thead></table>
Search minimum chisq in a range of periods

<b>Parameters</b><br>
* days  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; Julian days of observation
* flux  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; measured flux
* prs  :  array 
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of periods
* scl  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; pertaining scale of fit
* nrknots  :  int (20)
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of knots in BasicSplinesModel
* tol  :  float (0.001)
<br>&nbsp;&nbsp;&nbsp;&nbsp; tolerance, stop criterion

<a name="findParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>findParameters(</strong> days, flux, period, verbose=False, plot=0 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PeriodicScout.py#L208-L321 target=_blank>[source]</a></th></tr></thead></table>
Return a first guess for the parameters
eccentricity, phase, longitude

<b>Parameters</b><br>
* days  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; time of observations
* flux  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; flux of observations
* period  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the period (from findPeriod() )
* verbose  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; print some things
* plot  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; 0   dont plot
<br>&nbsp;&nbsp;&nbsp;&nbsp; 1   plot and show the results
<br>&nbsp;&nbsp;&nbsp;&nbsp; 2   plot but dont show the results

<a name="findRadius"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>findRadius(</strong> time, yfit, kmin, ymed ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PeriodicScout.py#L323-L361 target=_blank>[source]</a></th></tr></thead></table>
Find the radius of a star from the eclips duration

<b>Parameters</b><br>
* time  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; time values of yfit
* yfit  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; splines fit to the clipsing data
* kmin  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index of (local) minimum in yfit
* ymed  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; median value of yfit

