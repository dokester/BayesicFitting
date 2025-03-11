---
---
<br><br>

<a name="PhantomCollection"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class PhantomCollection(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PhantomCollection.py target=_blank>Source</a></th></tr></thead></table>
<p>

Helper class for NestedSamplers Engines to collect all trial walkers
obtained during the NS run. They are kept ordered according to their logL.  
They are used to find the minimum and maximum values 
of the parameter settings as function of the likelihood. 

There are different methods for static models and for dynamic models. 

For dynamic models only parameter sets of the proper length are searched.
The kth item in self.logL belongs to the kth list in self.pars.
If the model had np parameters then self.logL[np][k] pertain to 
self.pars[np][k,:] which has np items

For static models there is only one array of self.logL and one 2-d array 
od self.pars.

<b>Attributes</b><br>
* phantoms  :  WalkerList or dict of { int : WalkerList }<br>
&nbsp;&nbsp;&nbsp;&nbsp; int         number of parameters in the model<br>
&nbsp;&nbsp;&nbsp;&nbsp; Wlakerlist  list of (phantom) walkers<br>
* paramMin  :  array_like or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; minimum values of the parameters at this stage of lowLhood<br>
&nbsp;&nbsp;&nbsp;&nbsp; None if too few items of this parameter length is present<br>
* paramMax  :  array_like or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; maximum values of the parameters at this stage of lowLhood<br>
&nbsp;&nbsp;&nbsp;&nbsp; None if too few items of this parameter length is present<br>


Author       Do Kester.


<a name="PhantomCollection"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>PhantomCollection(</strong> dynamic=False )
</th></tr></thead></table>
<p>

Constructor.

<b>Parameters</b><br>
* dynamic  :  bool<br>
    whether it is a dynamic model

<a name="length"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>length(</strong> np=0 ) 
</th></tr></thead></table>
<p>

Return length of internal walkerlist

<b>Parameters</b><br>
* np  :  int<br>
    number of parameters (in case of dynamic only)

<a name="getList"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getList(</strong> walker ) 
</th></tr></thead></table>
<p>

Return the applicable WalkerList

<b>Parameters</b><br>
* walker  :  Walker<br>
    return list pertaining to this walker (not used here)

<a name="storeItems"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>storeItems(</strong> walker ) 
</th></tr></thead></table>
<p>

Store both items as arrays.

<b>Parameters</b><br>
* walker  :  Walker<br>
    to be added to the PhantomCollection

<a name="calculateParamMinmax"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>calculateParamMinmax(</strong> lowLhood, np=0 )
</th></tr></thead></table>
<p>

Calculate the min and max values of the present parameter values.

<b>Parameters</b><br>
* lowLhood  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; lower boundary of the log Likelihood<br>
* np  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of parameters (not used in this implementation)<br>


<a name="getParamMinmax"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParamMinmax(</strong> lowLhood, np=0 )
</th></tr></thead></table>
<p>

Obtain the min and max values of the present parameter values.

<b>Parameters</b><br>
* lowLhood  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; lower boundary of the log Likelihood<br>
* np  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of parameters (not used in this implementation)<br>


<a name="lengthDynamic"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>lengthDynamic(</strong> np=None ) 
</th></tr></thead></table>
<p>

Return length of internal walkerlist

<b>Parameters</b><br>
* np  :  int<br>
    number of parameters (in case of dynamic only)

<a name="getDynamicList"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getDynamicList(</strong> walker ) 
</th></tr></thead></table>
<p>

Return the applicable WalkerList or None if not present.

<b>Parameters</b><br>
* walker  :  Walker<br>
    return list pertaining to this walker

<a name="storeDynamic"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>storeDynamic(</strong> walker ) 
</th></tr></thead></table>
<p>

Put both items in the dictionaries with npars as key

<b>Parameters</b><br>
* logL  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; log Likelihood <br>
* pars  :  1d array<br>
    parameters

<a name="calculateDynamic"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>calculateDynamic(</strong> lowLhood, np=0 )
</th></tr></thead></table>
<p>

Calculate the min and max values of the present parameters of length np.

<b>Parameters</b><br>
* lowLhood  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; lower boundary of the log Likelihood<br>
* np  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of parameters<br>


<a name="getDynamic"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getDynamic(</strong> lowLhood, np=0 )
</th></tr></thead></table>
<p>

Return the min and max values of the present parameters of length np.

<b>Parameters</b><br>
* lowLhood  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; lower boundary of the log Likelihood<br>
* np  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of parameters<br>


