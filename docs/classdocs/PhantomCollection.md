---
---
<br><br>

<a name="PhantomCollection"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class PhantomCollection(</strong> object )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PhantomCollection.py target=_blank>[source]</a></th></tr></thead></table>
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

<b>Attributes</b>

* phantoms  :  WalkerList or dict of { int : WalkerList }
<br>&nbsp;&nbsp;&nbsp;&nbsp; int         number of parameters in the model
<br>&nbsp;&nbsp;&nbsp;&nbsp; Wlakerlist  list of (phantom) walkers
* paramMin  :  array_like or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; minimum values of the parameters at this stage of lowLhood
<br>&nbsp;&nbsp;&nbsp;&nbsp; None if too few items of this parameter length is present
* paramMax  :  array_like or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; maximum values of the parameters at this stage of lowLhood
<br>&nbsp;&nbsp;&nbsp;&nbsp; None if too few items of this parameter length is present


Author       Do Kester.


<a name="PhantomCollection"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>PhantomCollection(</strong> dynamic=False )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PhantomCollection.py#L67-L87 target=_blank>[source]</a></th></tr></thead></table>

Constructor.

<b>Parameters</b>

* dynamic  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; whether it is a dynamic model

<a name="length"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>length(</strong> np=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PhantomCollection.py#L89-L106 target=_blank>[source]</a></th></tr></thead></table>
Return length of internal walkerlist

<b>Parameters</b>

* np  :  int or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; None return overall length
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of parameters (in case of dynamic only)

<a name="getBest"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getBest(</strong> np ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PhantomCollection.py#L108-L122 target=_blank>[source]</a></th></tr></thead></table>
Return the best phantom with np parameters; or -1 if no phantom has
np parameters

<b>Parameters</b>

* np  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of parameters

<a name="nextLowPhantom"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>nextLowPhantom(</strong> lowLhood ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PhantomCollection.py#L124-L137 target=_blank>[source]</a></th></tr></thead></table>
Generator for phantoms with logL < lowLhood

<b>Parameters</b>

* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; low border for likelihood

<a name="storeItems"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>storeItems(</strong> walker ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PhantomCollection.py#L139-L150 target=_blank>[source]</a></th></tr></thead></table>
Store both items as arrays.

<b>Parameters</b>

* walker  :  Walker
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be added to the PhantomCollection

<a name="getParamMinmax"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParamMinmax(</strong> lowLhood, np=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PhantomCollection.py#L152-L168 target=_blank>[source]</a></th></tr></thead></table>
Obtain the min and max values of the present parameter values.

<b>Parameters</b>

* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; lower boundary of the log Likelihood
* np  :  int or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of parameters (not used in this implementation)


<a name="calculateParamMinmax"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>calculateParamMinmax(</strong> lowLhood, np=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/PhantomCollection.py#L170-L201 target=_blank>[source]</a></th></tr></thead></table>
Calculate the min and max values of the present parameters of length np.

<b>Parameters</b>

* lowLhood  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; lower boundary of the log Likelihood
* np  :  int or None
<br>&nbsp;&nbsp;&nbsp;&nbsp; None for static models.
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of parameters


Endline #L203
