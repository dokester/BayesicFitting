---
---
<br><br>

<a name="Plotter"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>Module Plotter</strong> </th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source// target=_blank>[source]</a></th></tr></thead></table>
<p>


This module contains several methods to plot the results of some class 

&nbsp; + a fit by a Fitter.
<br>&nbsp; + a fit by a Sampler.
<br>&nbsp; + a fit to a StellarOrbit
<br>&nbsp; + iteration samples from NestedSampler(s)
<br>&nbsp; + 3D plot of a stellar orbit
<br>&nbsp; + Eclipsing stars

The fits are invoked when Fitter.fit() or Sampler.sample() are called with plot=True.


<a name="plotFit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotFit(</strong> x, data=None, yfit=None, model=None, fitter=None, show=True,
 residuals=False, xlabel=None, ylabel=None, title=None, figsize=[7,5],
 xlim=None, ylim=None, filename=None, transparent=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L53-L167 target=_blank>[source]</a></th></tr></thead></table>

Plot the data of a fit.

<b>Parameters</b>

* x  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; xdata of the problem
* data  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; ydata of the problem
* yfit  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; fit of the data to the model
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model the data are fitted to at x
* fitter  :  BaseFitter
<br>&nbsp;&nbsp;&nbsp;&nbsp; the fitter being used
<br>&nbsp;&nbsp;&nbsp;&nbsp; If set it displays a confidence region for the fit
* show  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; display the plot
* residuals  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; plot the residuals in a separate panel
* xlabel  :  None or str
<br>&nbsp;&nbsp;&nbsp;&nbsp; use as xlabel
* ylabel  :  None or str
<br>&nbsp;&nbsp;&nbsp;&nbsp; use as ylabel
* title   :  None or str
<br>&nbsp;&nbsp;&nbsp;&nbsp; use as title
* xlim  :  None or list of 2 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; limits on x-axis
* ylim  :  None or list of 2 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; limits on y-axis
* figsize  :  list of 2 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; size of the figure
* filename   :  None or str
<br>&nbsp;&nbsp;&nbsp;&nbsp; name of png file; otherwise show
* transparent  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; make the png file transparent

<a name="plotSampleList"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotSampleList(</strong> sl, xdata, ydata, problem=None, errors=None, npt=10000,
 residuals=False, xlabel=None, ylabel=None, title=None, period=None, figsize=[7,5],
 xlim=None, ylim=None, filename=None, transparent=False, show=True ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L169-L330 target=_blank>[source]</a></th></tr></thead></table>
Plot the posterior as npt points from the SampleList.

<b>Parameters</b>

* sl  :  SampleList
<br>&nbsp;&nbsp;&nbsp;&nbsp; the samplelist containing samples from the posterior
* xdata  :  arraylike
<br>&nbsp;&nbsp;&nbsp;&nbsp; the xdata values; plotted for comparison
* ydata  :  arraylike
<br>&nbsp;&nbsp;&nbsp;&nbsp; the ydata values; plotted for comparison
* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; the problem at hand
* errors  :  None of arraylike
<br>&nbsp;&nbsp;&nbsp;&nbsp; (No) errors on the ydata are displayed
* npt  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of points from the sample (10000)
* residuals  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; plot the residuals in a lower panel (False)
* xlabel  :  None or str
<br>&nbsp;&nbsp;&nbsp;&nbsp; use as xlabel
* ylabel  :  None or str
<br>&nbsp;&nbsp;&nbsp;&nbsp; use as ylabel
* title   :  None or str
<br>&nbsp;&nbsp;&nbsp;&nbsp; use as title
* xlim  :  None or list of 2 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; limits on x-axis
* ylim  :  None or list of 2 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; limits on y-axis
* period  :  float or int
<br>&nbsp;&nbsp;&nbsp;&nbsp; fold over period
<br>&nbsp;&nbsp;&nbsp;&nbsp; if int the period is taken from sl.parameters[period]
* figsize  :  list of 2 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; size of the figure
* filename   :  None or str
<br>&nbsp;&nbsp;&nbsp;&nbsp; name of png file; otherwise show
* transparent  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; make the png file transparent
* show  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; show the plot (or not, for testing)


<a name="plotWalker"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotWalker(</strong> walker, iter, show=False )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L332-L350 target=_blank>[source]</a></th></tr></thead></table>
Plot the results for a walker in an iteration plot.

<b>Parameters</b>

* walker  :  Walker
<br>&nbsp;&nbsp;&nbsp;&nbsp; the walker to plot
* iter  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; iteration number
* show  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; show the plot (or not, for testing)

<a name="plotIter"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotIter(</strong> xdata, ydata, model, param, iter, show=False )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L352-L396 target=_blank>[source]</a></th></tr></thead></table>
Plot the data and the fit-results in an iteration plot.

<b>Parameters</b>

* xdata  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; x data points
* ydata  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; y data points
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model
* param  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; the parameters
* iter  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; iteration number
* show  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; show the plot (or not, for testing)

<a name="plotOrbit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotOrbit(</strong> som, par, npoint=361, xdata=None, ydata=None, show=True,
 plot=None, color='k', ls='-', northEast=True ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L398-L499 target=_blank>[source]</a></th></tr></thead></table>
Plot the orbit of a StellarOrbitModel in N points, a forward 
pointing arrow at T = 0, the line to the periastron and 
an extended line of nodes. 

if ydata is present, plot the datapoints. If also xdata is present, 
plot the connecting lines too.

<b>Parameters</b>

* som  :  StellarOrbitModel with spherical=False
<br>&nbsp;&nbsp;&nbsp;&nbsp; the orbit to plot
* par  :   array
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter of the model
* npoint  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of points in the orbit
* xdata  :  array 
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of times at which the data are measured
* ydata  :  2d array 
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of [x,y] pairs representing the data
* show  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; show the plot (or not, for testing)
* plot  :  None or pyplot
<br>&nbsp;&nbsp;&nbsp;&nbsp; None    make a self standing plot and show it
<br>&nbsp;&nbsp;&nbsp;&nbsp; pyplot  operate within thid plot; do not show
* color, ls  :  color and linestyle
<br>&nbsp;&nbsp;&nbsp;&nbsp; for the plot
* northEast  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; plot North-East pointers 


<a name="lineOfNodes"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>lineOfNodes(</strong> x, y, n2n, scale=1.0, indices=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L501-L542 target=_blank>[source]</a></th></tr></thead></table>
Calculate the line of nodes

<b>Parameters</b>

* x  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; x-values along the orbit
* y  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; y-values along the orbit
* n2n  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; angle from North to Line-of-nodes
* scale  :  float (1.0)
<br>&nbsp;&nbsp;&nbsp;&nbsp; extension beyond the orbit
* indices  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; return indices in (x,y)

<b>Returns</b>

* ( ndx, ndy )  :  tuple to 2 lists 
<br>&nbsp;&nbsp;&nbsp;&nbsp; tuple of x-values and y-values of the nodes


<a name="plotOrbit3D"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotOrbit3D(</strong> som, par, npoint=361, xdata=None, ydata=None, show=True,
 plot=None, color='k', ls='-', northEast=True ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L544-L653 target=_blank>[source]</a></th></tr></thead></table>
Three dimensional plot of the orbit of a StellarOrbitModel in N points, a forward 
pointing arrow at T = 0, the line to the periastron and 
an extended line of nodes. 

if ydata is present, plot the datapoints. If also xdata is present, 
plot the connecting lines too.

<b>Parameters</b>

* som  :  StellarOrbitModel with spherical=False
<br>&nbsp;&nbsp;&nbsp;&nbsp; the orbit to plot
* par  :   array
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter of the model
* npoint  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of points in the orbit
* xdata  :  array 
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of times at which the data are measured
* ydata  :  2d array 
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of [x,y] pairs representing the data
* show  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; show the plot (or not, for testing)
* plot  :  None or pyplot
<br>&nbsp;&nbsp;&nbsp;&nbsp; None    make a self standing plot and show it
<br>&nbsp;&nbsp;&nbsp;&nbsp; pyplot  operate within this plot; do not show
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; needs to have  .add_subplot( projection='3d' )
* color, ls  :  color and linestyle
<br>&nbsp;&nbsp;&nbsp;&nbsp; for the plot
* northEast  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; plot North-East pointers 


<a name="plotEclipsingStar"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotEclipsingStar(</strong> esm, pars, xdata=None, ydata=None, toMags=False, starpos=None,
 figsize=[9,6], grid=None, show=True, filename=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L655-L759 target=_blank>[source]</a></th></tr></thead></table>
plot of eclipsing stars seen from above. The orientation is irrelevant.

<b>Parameters</b>

* esm  :  EclipsingStarModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; containing the stars
* pars  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; for esm
* xdata  :  None or array
<br>&nbsp;&nbsp;&nbsp;&nbsp; of (measured) data points.
* ydata  :  None or array
<br>&nbsp;&nbsp;&nbsp;&nbsp; of (measured) data points.
* toMags  :  bool or float
<br>&nbsp;&nbsp;&nbsp;&nbsp; true    produce plot in magnitudes (ydata is in mags)
<br>&nbsp;&nbsp;&nbsp;&nbsp; float   true and use number to scale the fluxes
* starpos  :  (small) array
<br>&nbsp;&nbsp;&nbsp;&nbsp; times of star positions to display
* figsize  :  list of 2 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; size of the plot
* grid  :  GridSpec
<br>&nbsp;&nbsp;&nbsp;&nbsp; GridSpec where to plot the orbit in
* show  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; to show the plot (or not)
* filename  :  str
<br>&nbsp;&nbsp;&nbsp;&nbsp; write to filename

<a name="plotEsmSideView"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotEsmSideView(</strong> esm, pars, times=None, starpos=None, axin=None, figsize=[9,6],
 show=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L761-L875 target=_blank>[source]</a></th></tr></thead></table>
Plot an EclipsingStarModel in sideways view.

<b>Parameters</b>

* esm  :  EclipsingStarModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; containing the stars
* pars  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; for esm
* times  :  None or array
<br>&nbsp;&nbsp;&nbsp;&nbsp; to plot
* starpos  :  (small) array
<br>&nbsp;&nbsp;&nbsp;&nbsp; times of star positions to display
* axin  :  Axes (None)
<br>&nbsp;&nbsp;&nbsp;&nbsp; to plot in
* figsize  :  list of 2 floats ([9,6])
<br>&nbsp;&nbsp;&nbsp;&nbsp; size of the plot
* show  :  bool (False)
<br>&nbsp;&nbsp;&nbsp;&nbsp; to show the plot

<a name="starColors"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>starColors(</strong> L1, L2, L3 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L877-L905 target=_blank>[source]</a></th></tr></thead></table>
Return colors for star 1, star 2 dark side and star 2 spot.

<b>Parameters</b>

* L1, L2, L3  :  floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; luminosities for star 1, 2 and spot

<a name="plotEsmEclipseView"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotEsmEclipseView(</strong> esm, pars, times=None, starpos=None, axin=None, figsize=[9,6],
 show=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L907-L1066 target=_blank>[source]</a></th></tr></thead></table>
Plot an EclipsingStarModel in eclipsing view.

<b>Parameters</b>

* esm  :  EclipsingStarModel
<br>&nbsp;&nbsp;&nbsp;&nbsp; containing the stars
* pars  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; for esm
* times  :  None or array
<br>&nbsp;&nbsp;&nbsp;&nbsp; to plot
* starpos  :  (small) array
<br>&nbsp;&nbsp;&nbsp;&nbsp; times of star positions to display
* axin  :  Axes (None)
<br>&nbsp;&nbsp;&nbsp;&nbsp; to plot in
* figsize  :  list of 2 floats ([9,6])
<br>&nbsp;&nbsp;&nbsp;&nbsp; size of the plot
* show  :  bool (False)
<br>&nbsp;&nbsp;&nbsp;&nbsp; to show the plot

