---
---
<br><br>

<a name="AnnealingAmoeba"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class AnnealingAmoeba(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/AnnealingAmoeba.py target=_blank>Source</a></th></tr></thead></table>
<p>

Simulated annealing simplex finding minimum.

AnnealingAmoeba can be used in two modes: with simulated annealing on or off.
The simulated annealing mode is invoked by setting the temperature to
some value. By default it is off: temperature at zero.

When the temperature is set at zero (default), AnnealingAmoeba acts as a
simple Nelder-Mead downhill simplex method. With two advantages and one
disadvantage. The pro's are that it is reasonably fast and that it does not
need partial derivatives. The con is that it will fall into the first local
minimum it encounters. No guarantee that this minimum has anything to do
with the absolute minimum. This T=0 modus can only be used in mono-modal
problems.

In the other modus, when the temperature is set at some value the
simplex sometimes takes a uphill step, depending on the temperature at
that moment. Steps downhill are always taken. In that way it is possible
to climb out of local minima to find better ones. Meanwhile the temperature
is steadily lowered, concentrating the search on the by now hopefully found
absolute minimum. Of course this takes much more iterations and still there
is *no guarantee* that the best value is found. But a better chance.
The initial temperature which suggests itself is of the order of the
humps found in the minimizable lanscape.

At each temperature level a number of moves is made. This number is set by
the keyword steps=10, by default. After these steps the temperature is lowered
with a factor set by cooling=0.95, by default.

Iteration continues until the relative difference between the low and high
points within the simplex is less than reltol
&nbsp;&nbsp;&nbsp;&nbsp; |yhi - ylo| / ( |yhi| + |ylo| ) < reltol<br>
and/or the absolute difference is less than abstol
&nbsp;&nbsp;&nbsp;&nbsp; |yhi - ylo| < abstol.<br>

AnnealingAmoeba can be used with limits set to one or more of the input values.

The original version stems from Numerical Recipes with some additions of my own.

Author       Do Kester

<b>Attributes</b>

* func  :  callable<br>
&nbsp;&nbsp;&nbsp;&nbsp; function to be minimized of form : y = func( x )<br>
* lolimits  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; lower limits on x. -inf is allowed to indicate no lower limit<br>
* hilimits  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; upper limits on x. +inf is allowed to indicate no upper limit<br>
* fopt  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; the best of the above values<br>
* xopt  :  ndarray<br>
&nbsp;&nbsp;&nbsp;&nbsp; copy of the simplex point that has the best value (nx)<br>

* rng  :  RandomState<br>
&nbsp;&nbsp;&nbsp;&nbsp; random number generator<br>
* seed  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; seed of rng<br>

* reltol  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; Relative tolerance. Program stops when ( |yhi-ylo| / (|yhi|+|ylo|) ) < reltol<br>
* abstol  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; Absolute tolerance. Program stops when |yhi-ylo| < abstol<br>
* maxiter  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; maximum number of iterations<br>
* iter  :  int (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; iteration counter<br>
* ncalls  :  int (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; numbers of calls to func<br>

* temp  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; annealing temperature (default: 0)<br>
* cooling  :  float (non existent when temp=0)<br>
&nbsp;&nbsp;&nbsp;&nbsp; cooling factor (default: 0.95)<br>
* steps  :  int (non existent when temp=0)<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of steps per cooling cycle (default: 10)<br>

* verbose  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; 0  : silent<br>
&nbsp;&nbsp;&nbsp;&nbsp; 1 : print results to output<br>
&nbsp;&nbsp;&nbsp;&nbsp; 2 : print some info every 100 iterations and plot results<br>
&nbsp;&nbsp;&nbsp;&nbsp; 3 : print some info every iteration<br>
* callback  :  callable<br>
&nbsp;&nbsp;&nbsp;&nbsp; function to be called every iteration of form :<br>
&nbsp;&nbsp;&nbsp;&nbsp; xopt = callback( xopt )<br>

* simplex  :  ndarray<br>
&nbsp;&nbsp;&nbsp;&nbsp; the simplex has shape = (nx+1, nx); nx is the size of x<br>
* values  :  ndarray<br>
&nbsp;&nbsp;&nbsp;&nbsp; the values of the function attained at the simplex points (nx+1).<br>
* sum  :  ndarray<br>
&nbsp;&nbsp;&nbsp;&nbsp; sum over the corners of the simplex (nx)<br>


<a name="AnnealingAmoeba"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>AnnealingAmoeba(</strong> func, xini, size=1, seed=4567, temp=0, limits=None,
 maxiter=1000, reltol=0.0001, abstol=0.0001, cooling=0.95, steps=10,
 verbose=0, callback=None )
</th></tr></thead></table>
<p>

Create a new AnnealingAmoeba class to minimize the function

<b>Parameters</b>

* func  :  callable<br>
&nbsp;&nbsp;&nbsp;&nbsp; the function to be minimized<br>
* xini  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; initial values of the function<br>
* size  :  float or array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; step size of the simplex<br>
* seed  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; for random number generator<br>
* temp  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; temperature of annealing (0 is no annealing)<br>
* limits  :  None or list of 2 floats or list of 2 array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; None : no limits applied<br>
&nbsp;&nbsp;&nbsp;&nbsp; [lo,hi] : low and high limits for all values<br>
&nbsp;&nbsp;&nbsp;&nbsp; [la,ha] : low array and high array limits for the values<br>
* maxiter  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; max number of iterations<br>
* reltol  :  float, None<br>
&nbsp;&nbsp;&nbsp;&nbsp; Relative tolerance. Program stops when ( |hi-lo| / (|hi|+|lo|) ) < reltol<br>
* abstol  :  float, None<br>
&nbsp;&nbsp;&nbsp;&nbsp; Absolute tolerance. Program stops when |hi-lo| < abstol<br>
&nbsp;&nbsp;&nbsp;&nbsp; when abstol has a (float) value, reltol might be None.<br>
* cooling  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; cooling factor when annealing<br>
* steps  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of cycles in each cooling step.<br>
* verbose  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; 0 : silent<br>
&nbsp;&nbsp;&nbsp;&nbsp; 1 : print results to output<br>
&nbsp;&nbsp;&nbsp;&nbsp; 2 : print some info every 100 iterations and plot results<br>
&nbsp;&nbsp;&nbsp;&nbsp; 3 : print some info every iteration<br>
* callback  :  callable<br>
&nbsp;&nbsp;&nbsp;&nbsp; is called each iteration as<br>
&nbsp;&nbsp;&nbsp;&nbsp; val = callback( val )<br>
&nbsp;&nbsp;&nbsp;&nbsp; where val is the minimizable array<br>

<b>Raises</b>

ValueError
&nbsp;&nbsp;&nbsp;&nbsp; 1. When func is not callable<br>
&nbsp;&nbsp;&nbsp;&nbsp; 2. When both tolerances are None<br>
&nbsp;&nbsp;&nbsp;&nbsp; 3. When callback is not callable<br>


<a name="makeSimplex"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makeSimplex(</strong> xini, step )
</th></tr></thead></table>
<p>

Make a simplex for the given set of parameters.

<b>Parameters</b>

* xini  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; initial (parameter) array<br>
* step  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; size of the simplex<br>


<a name="hasLowLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasLowLimits(</strong> k ) 
</th></tr></thead></table>
<p>

Return True if it has low limits > -inf.

<a name="hasHighLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasHighLimits(</strong> k ) 
</th></tr></thead></table>
<p>

Return True if it has high limits < inf.

<a name="stayInLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>stayInLimits(</strong> oldpar, trypar ) 
</th></tr></thead></table>
<p>

Keep the parameters within the limits.

<b>Parameters</b>

* oldpar  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; previous set of parameters (assumed to be within limits)<br>
* trypar  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; new parameters, possibly out of limits<br>

<b>Returns</b>

* newpar  :  array_like<br>
    new parameters, within limits

<a name="checkSimplex"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>checkSimplex(</strong> simplex )
</th></tr></thead></table>
<p>

Check for degeneracy: all points on same location.

<b>Parameters</b>

* simplex  :  matrix<br>
    the simplex of amoeba

<a name="setValues"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setValues(</strong> )
</th></tr></thead></table>
<p>

Calculate the function values a simplex's corners


<a name="minimize"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>minimize(</strong> )
</th></tr></thead></table>
<p>

Converge the simplex.

<b>Returns</b>

* ndarray  :  the optimal x values.<br>

<b>Raises</b>

ConvergenceError when too many iterations are needed.

<a name="temperatureStep"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>temperatureStep(</strong> )
</th></tr></thead></table>
<p>

Perform simplex moves in the right direction.

<b>Returns</b>

* int  :  number of transforms.<br>


<a name="doVerbose"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>doVerbose(</strong> name, chisq, par, verbose=0 ) 
</th></tr></thead></table>
<p>
<a name="randomRange"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>randomRange(</strong> factor )
</th></tr></thead></table>
<p>
<a name="inflateSimplex"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>inflateSimplex(</strong> ilo, factor )
</th></tr></thead></table>
<p>

Inflate/deflate simplex around the (lowest) point (ilo).

inflate if factor > 1
deflate if factor < 1
mirror  if factor < 0

<b>Parameters</b>

* ilo  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; lowest point in the simplex<br>
* factor  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; inflation factor<br>


<a name="trialStep"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>trialStep(</strong> ihi, yhi, factor )
</th></tr></thead></table>
<p>

Do a trial step to improve the worst (highest) point.

<b>Parameters</b>

* ihi  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index of the high point<br>
* yhi  :   int<br>
&nbsp;&nbsp;&nbsp;&nbsp; value at the high point<br>
* factor  :  int<br>
    step size

<a name="logRanTemp"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logRanTemp(</strong> )
</th></tr></thead></table>
<p>
