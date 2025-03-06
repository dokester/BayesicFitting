---
---
<br><br>

<a name="WalkerList"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class WalkerList(</strong> <a href="./list.html">list</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/WalkerList.py target=_blank>Source</a></th></tr></thead></table>
<p>

WalkerList is a list of Walker.

It is the working ensemble of NestedSampler.


<b>Attributes</b>

* logZ  :  float (read-only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; Natural log of evidence<br>
* info  :  float (read-only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; The information H. The compression factor ( the ratio of the prior space<br>
&nbsp;&nbsp;&nbsp;&nbsp; available to the model parameters over the posterior space ) is equal to the exp( H ).<br>
* iteration  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; Present iteration number.<br>

Author       Do Kester


<a name="WalkerList"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>WalkerList(</strong> problem=None, ensemble=0, allpars=None, fitIndex=None,
 walker=None, walkerlist=None )
</th></tr></thead></table>
<p>

Constructor.

To be valid it needs either problem/allpars/fitindex or walker or walkerlist

<b>Parameters</b>

* problem  :  Problem or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; to construct a walker to be added.<br>
* ensemble  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of walkers<br>
* allpars  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters of the problem<br>
* fitIndex  :  array of int<br>
&nbsp;&nbsp;&nbsp;&nbsp; list of parameters to be fitted.<br>
* walker  :  Walker or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; walker to be added.<br>
* walkerlist  :  Walkerlist or None<br>
    walkerlist to be incorporated.

<a name="addWalkers"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>addWalkers(</strong> walker, ensemble )
</th></tr></thead></table>
<p>
<a name="setWalker"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setWalker(</strong> walker, index )
</th></tr></thead></table>
<p>

replace/append a Walker to this list

<b>Parameters</b>

* walker  :  Walker<br>
&nbsp;&nbsp;&nbsp;&nbsp; the list to take to copy from<br>
* index  :  int<br>
    the index at which to set

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> src, des, wlist=None, start=0 )
</th></tr></thead></table>
<p>

Copy one item of the list onto another.

<b>Parameters</b>

* src  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; the source item<br>
* des  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; the destination item<br>
* wlist  :  WalkerList or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; Copy from this WalkerList (None == self)<br>
* start  :  int<br>
    iteration where this walker was created

<a name="logPlus"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logPlus(</strong> x, y )
</th></tr></thead></table>
<p>

Return the log of sum.

<a name="firstIndex"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>firstIndex(</strong> lowL ) 
</th></tr></thead></table>
<p>

Return  index of the first walker with walker.logL > lowL, 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; None if list is empty<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; len  if no item applies <br>

<b>Parameters</b>

* lowL  :  float<br>
    low Likelihood

<a name="insertWalker"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>insertWalker(</strong> walker )
</th></tr></thead></table>
<p>

Insert walker to this list keeping it sorted in logL

<b>Parameters</b>

* walker  :  Walker<br>
    the list to take to copy from

<a name="cropOnLow"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>cropOnLow(</strong> lowL ) 
</th></tr></thead></table>
<p>

Return WalkerList with all LogL > lowL

Precondition: self is ordered on logL

<b>Parameters</b>

* lowL  :  float<br>
    low Likelihood

<a name="getLogL"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLogL(</strong> walker=None ) 
</th></tr></thead></table>
<p>

Return the logL of the/all walker

<b>Parameters</b>

* walker  :  None or Walker<br>
&nbsp;&nbsp;&nbsp;&nbsp; None return value for all walkers<br>
    get the logL from

<a name="allPars"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>allPars(</strong> )
</th></tr></thead></table>
<p>

Return a 2d array of all parameters.

In case of dynamic models the number of parameters may vary.
They are zero-padded. Use `getNumberOfParametersEvolution`
to get the actual number.

<b>Parameters</b>

* kpar  :  int or tuple of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp; the parameter to be selected. Default: all<br>


<a name="getParameterEvolution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParameterEvolution(</strong> kpar=None )
</th></tr></thead></table>
<p>

Return the evolution of one or all parameters.

In case of dynamic models the number of parameters may vary.
They are zero-padded. Use `getNumberOfParametersEvolution`
to get the actual number.

<b>Parameters</b>

* kpar  :  int or tuple of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp; the parameter to be selected. Default: all<br>


<a name="getScaleEvolution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getScaleEvolution(</strong> )
</th></tr></thead></table>
<p>
Return the evolution of the scale. 

<a name="getLogLikelihoodEvolution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLogLikelihoodEvolution(</strong> )
</th></tr></thead></table>
<p>
Return the evolution of the log( Likelihood ). 

<a name="getLowLogL"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLowLogL(</strong> )
</th></tr></thead></table>
<p>

Return the lowest value of logL in the walkerlist, plus its index.

