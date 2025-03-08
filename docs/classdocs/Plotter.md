---
---

<a name="plotFit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotFit(</strong> data=None, yfit=None, model=None, fitter=None, show=True,
 residuals=False, xlabel=None, ylabel=None, title=None, figsize=[7,5],
 xlim=None, ylim=None, filename=None, transparent=False ) 
</th></tr></thead></table>
<p>

Plot the data of a fit.

<b>Parameters</b>

* x  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; xdata of the problem<br>
* data  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; ydata of the problem<br>
* yfit  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; fit of the data to the model<br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model the data are fitted to at x<br>
* fitter  :  BaseFitter<br>
&nbsp;&nbsp;&nbsp;&nbsp; the fitter being used<br>
&nbsp;&nbsp;&nbsp;&nbsp; If set it displays a confidence region for the fit<br>
* show  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; display the plot<br>
* residuals  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; plot the residuals in a separate panel<br>
* xlabel  :  None or str<br>
&nbsp;&nbsp;&nbsp;&nbsp; use as xlabel<br>
* ylabel  :  None or str<br>
&nbsp;&nbsp;&nbsp;&nbsp; use as ylabel<br>
* title   :  None or str<br>
&nbsp;&nbsp;&nbsp;&nbsp; use as title<br>
* xlim  :  None or list of 2 floats<br>
&nbsp;&nbsp;&nbsp;&nbsp; limits on x-axis<br>
* ylim  :  None or list of 2 floats<br>
&nbsp;&nbsp;&nbsp;&nbsp; limits on y-axis<br>
* figsize  :  list of 2 floats<br>
&nbsp;&nbsp;&nbsp;&nbsp; size of the figure<br>
* filename   :  None or str<br>
&nbsp;&nbsp;&nbsp;&nbsp; name of png file; otherwise show<br>
* transparent  :  bool<br>
    make the png file transparent

<a name="plotSampleList"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>plotSampleList(</strong> xdata, ydata, errors=None, npt=10000,
 residuals=False, xlabel=None, ylabel=None, title=None, figsize=[7,5],
 xlim=None, ylim=None, filename=None, transparent=False, show=True ) 
</th></tr></thead></table>
<p>

Plot the posterior as npt points from the SampleList.

Parameters
==========
sl : SampleList
&nbsp;&nbsp;&nbsp;&nbsp; the samplelist containing samples from the posterior<br>
xdata : arraylike
&nbsp;&nbsp;&nbsp;&nbsp; the xdata values; plotted for comparison<br>
ydata : arraylike
&nbsp;&nbsp;&nbsp;&nbsp; the ydata values; plotted for comparison<br>
errors : None of arraylike
&nbsp;&nbsp;&nbsp;&nbsp; (No) errors on the ydata are displayed<br>
npt : int
&nbsp;&nbsp;&nbsp;&nbsp; number of points from the sample (10000)<br>
residuals : bool
&nbsp;&nbsp;&nbsp;&nbsp; plot the residuals in a lower panel (False)<br>
xlabel : None or str
&nbsp;&nbsp;&nbsp;&nbsp; use as xlabel<br>
ylabel : None or str
&nbsp;&nbsp;&nbsp;&nbsp; use as ylabel<br>
title  : None or str
&nbsp;&nbsp;&nbsp;&nbsp; use as title<br>
xlim : None or list of 2 floats
&nbsp;&nbsp;&nbsp;&nbsp; limits on x-axis<br>
ylim : None or list of 2 floats
&nbsp;&nbsp;&nbsp;&nbsp; limits on y-axis<br>
figsize : list of 2 floats
&nbsp;&nbsp;&nbsp;&nbsp; size of the figure<br>
filename  : None or str
&nbsp;&nbsp;&nbsp;&nbsp; name of png file; otherwise show<br>
transparent : bool
&nbsp;&nbsp;&nbsp;&nbsp; make the png file transparent<br>


