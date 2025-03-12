---
---
<br><br>

<a name="FitPlotter"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>Module FitPlotter</strong> </th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Plotter.py target=_blank>Source</a></th></tr></thead></table>

This module contains 2 methods to plot the results of a fit by a Fitter resp. 
a Sampler.

They are invoked when Fitter.fit() or Sampler.sample() is called with plot=True.


<a name="plotFit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotFit(</strong> data=None, yfit=None, model=None, fitter=None, show=True,
 residuals=False, xlabel=None, ylabel=None, title=None, figsize=[7,5],
 xlim=None, ylim=None, filename=None, transparent=False ) 
</th></tr></thead></table>
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
<strong>plotSampleList(</strong> xdata, ydata, errors=None, npt=10000,
 residuals=False, xlabel=None, ylabel=None, title=None, figsize=[7,5],
 xlim=None, ylim=None, filename=None, transparent=False, show=True ) 
</th></tr></thead></table>
Plot the posterior as npt points from the SampleList.

<b>Parameters</b>

* sl  :  SampleList
<br>&nbsp;&nbsp;&nbsp;&nbsp; the samplelist containing samples from the posterior
* xdata  :  arraylike
<br>&nbsp;&nbsp;&nbsp;&nbsp; the xdata values; plotted for comparison
* ydata  :  arraylike
<br>&nbsp;&nbsp;&nbsp;&nbsp; the ydata values; plotted for comparison
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
* figsize  :  list of 2 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; size of the figure
* filename   :  None or str
<br>&nbsp;&nbsp;&nbsp;&nbsp; name of png file; otherwise show
* transparent  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; make the png file transparent


