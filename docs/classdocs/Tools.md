---
---
<br><br>

<a name="Tools"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>Module Tools</strong> </th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py target=_blank>Source</a></th></tr></thead></table>

This module contains a mixed bag of "usefull" methods.


<a name="getItem"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getItem(</strong> k ) 
</th></tr></thead></table>
Return the k-th item of the ilist
<br>&nbsp;&nbsp;&nbsp;&nbsp; or the last when not enough
<br>&nbsp;&nbsp;&nbsp;&nbsp; or the ilist itself when it is not a list

<b>Parameters</b>

* ilist  :  an item or a list of items
<br>&nbsp;&nbsp;&nbsp;&nbsp; List to obtain an item from
* k  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; item to be returned


<a name="firstIndex"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>firstIndex(</strong> condition=lambda x: True ) 
</th></tr></thead></table>
Returns the index of first item in the `iterable` that
satisfies the `condition`.

If the condition is not given, it returns 0

<b>Parameters</b>

* iterable  :  iterable
<br>&nbsp;&nbsp;&nbsp;&nbsp; to find the first item in
* condition  :  lambda function
<br>&nbsp;&nbsp;&nbsp;&nbsp; the condition

<b>Raises</b>

&nbsp; StopIteration: if no item satysfing the condition is found.

<b>Examples</b>

    firstIndex( (1,2,3), condition=lambda x: x % 2 == 0)
    2
    firstIndex( range( 3, 100 ) )
    3
    firstIndex( () )
    Traceback (most recent call last)
    ...
    StopIteration


<a name="getColumnData"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getColumnData(</strong> kcol ) 
</th></tr></thead></table>
Return the kcol-th column from xdata

<b>Parameters</b>

xdata   2D array_like or Table
<br>&nbsp;&nbsp;&nbsp;&nbsp; the data array
kcol    int
<br>&nbsp;&nbsp;&nbsp;&nbsp; column index

<a name="isBetween"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBetween(</strong> x, xe ) 
</th></tr></thead></table>
Return True when x falls between xs and xe or on xs or xe.
<br>&nbsp;&nbsp;&nbsp;&nbsp; where the order of xs, xe is unknown.

<a name="getKwargs"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getKwargs(</strong> ) 
</th></tr></thead></table>
Return kwargs as dictionary

<a name="setAttribute"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setAttribute(</strong> name, value, type=None, islist=False, isnone=False ) 
</th></tr></thead></table>
Set an attribute to an object.

<b>Parameters</b>

* obj  :  object
<br>&nbsp;&nbsp;&nbsp;&nbsp; to set the attribute to
* name  :  str
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the attribute
* value  :  any
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the attribute
* type  :  class
<br>&nbsp;&nbsp;&nbsp;&nbsp; check class of the object
* islist  :  boolean
<br>&nbsp;&nbsp;&nbsp;&nbsp; check if it is a list of type
* isnone  :  boolean
<br>&nbsp;&nbsp;&nbsp;&nbsp; value could be a None

<b>Raises</b>

TypeError : if any  checks fails

<a name="setNoneAttributes"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setNoneAttributes(</strong> name, value, listNone ) 
</th></tr></thead></table>
Set attribute contained in dictionary dictList into the attr-list.
A list is a native list or a numpy.ndarray. It also checks the type.
if values is a singular item of the proper type it will be inserted as [value].

<b>Parameters</b>

* obj  :  object
<br>&nbsp;&nbsp;&nbsp;&nbsp; to place the attribute in
* name  :  str
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the attribute
* value  :  any
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the attribute
* listNone  :  list of names
<br>&nbsp;&nbsp;&nbsp;&nbsp; that could have a None value

<b>Returns</b>

&nbsp; True on succesful insertion. False otherwise.

<b>Raises</b>

&nbsp; TypeError   if the type is not as in the dictionary

<a name="setListOfAttributes"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setListOfAttributes(</strong> name, value, dictList ) 
</th></tr></thead></table>
<br>&nbsp; """
Set attribute contained in dictionary dictList into the attr-list.
A list is a native list or a numpy.ndarray. It also checks the type.
if values is a singular item of the proper type it will be inserted as [value].

<b>Parameters</b>

* obj  :  object
<br>&nbsp;&nbsp;&nbsp;&nbsp; to place the attribute in
* name  :  str
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the attribute
* value  :  any
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the attribute
* dictList  :  dictionary
<br>&nbsp;&nbsp;&nbsp;&nbsp; of possible attributes {"name": type}

<b>Returns</b>

&nbsp; True on succesful insertion. False otherwise.

<b>Raises</b>

&nbsp; TypeError   if the type is not as in the dictionary


<a name="setSingleAttributes"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setSingleAttributes(</strong> name, value, dictSingle ) 
</th></tr></thead></table>
Set a singular attribute contained in dictionary dictSingle into the attr-list.
It also checks the type.

<b>Parameters</b>

* obj  :  object
<br>&nbsp;&nbsp;&nbsp;&nbsp; to place the attribute in
* name  :  str
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the attribute
* value  :  any
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the attribute
* dictSingle  :  dictionary
<br>&nbsp;&nbsp;&nbsp;&nbsp; of possible attributes {"name": type}

<b>Returns</b>

&nbsp; True on succesful insertion. False otherwise.

<b>Raises</b>

&nbsp; TypeError   if the type is not as in the dictionary

<a name="makeNext"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makeNext(</strong> k ) 
</th></tr></thead></table>
<br>&nbsp; """
Return next item of x, and last item if x is exhausted.
Or x itself if x is singular.

<a name="length"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>length(</strong> ) 
</th></tr></thead></table>
Return the length of any item. Singletons have length 1; None has length 0..

<a name="toArray"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>toArray(</strong> ndim=1, dtype=None ) 
</th></tr></thead></table>
Return a array of x when x is a number

<b>Parameters</b>

* x  :  any number, list/array of numbers or []
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be converted to numpy.ndarray
* ndim  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; minimum number of dimensions present
* dtype  :  type
<br>&nbsp;&nbsp;&nbsp;&nbsp; conversion to type (None : as is)


<a name="isList"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isList(</strong> cls ) 
</th></tr></thead></table>
Return (True,False) if item is a instance of cls
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (True,True)  if item is a (list|ndarray) of instances of cls
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (False,False) if not

<a name="isInstance"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isInstance(</strong> cls ) 
</th></tr></thead></table>
Returns true when one of the following is true
1. when cls is int   : item is an int or item is a numpy.integer.
2. when cls is float : item is an float or item is an int.
3. when cls is cls   : item is a cls.

<a name="ndprint"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>ndprint(</strong> form='{0:.3f}' ) 
</th></tr></thead></table>
Print a ndarray, formatted.

<a name="decorate"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>decorate(</strong> des, copy=True ) 
</th></tr></thead></table>
Transfer attributes from src to des.
If copy is True try to copy the attributes, otherwise link it.

<b>Parameters</b>

* src  :  object
<br>&nbsp;&nbsp;&nbsp;&nbsp; source of the attributes
* des  :  object
<br>&nbsp;&nbsp;&nbsp;&nbsp; destiny for the attributes
* copy  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; if True: copy

<a name="subclassof"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>subclassof(</strong> cls ) 
</th></tr></thead></table>
Determine if sub inherits from the class cls

<b>Parameters</b>

* sub  :  class object
<br>&nbsp;&nbsp;&nbsp;&nbsp; supposed sub class
* cls  :  class object
<br>&nbsp;&nbsp;&nbsp;&nbsp; supposed parent class

<a name="printclass"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>printclass(</strong> nitems=8, printId=False ) 
</th></tr></thead></table>
Print the attributes of a class.

<a name="printlist"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>printlist(</strong> nitems=8 ) 
</th></tr></thead></table>

<a name="shortName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shortName(</strong> )
</th></tr></thead></table>
Return a short version the string representation: upto first non-letter.

<a name="nicenumber"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>nicenumber(</strong> ) 
</th></tr></thead></table>
Return a nice number close to (but below) |x|.

<a name="fix2int"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fix2int(</strong> ) 
</th></tr></thead></table>
Return integer array with values as in x

<b>Parameters</b>

* x  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; array of integer floats

<a name="track"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>track(</strong> ) 
</th></tr></thead></table>

<b>Parameters</b>

* statement  :  str
<br>&nbsp;&nbsp;&nbsp;&nbsp; statement to be traced


<a name="average"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>average(</strong> weights=None, circular=None ) 
</th></tr></thead></table>
Return (weighted) average and standard deviation of input array.

<b>Parameters</b>

* xx  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; input to be averaged
* weights  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; if present these are the weights
* circular  :  list of 2 floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; the input is a circular item between [low,high]

