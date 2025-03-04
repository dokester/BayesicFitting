---
---

<a name="getItem"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getItem(</strong> k ) 
</th></tr></thead></table>
<p>

Return the k-th item of the ilist
    or the last when not enough<br>
    or the ilist itself when it is not a list<br>

<b>Parameters</b>

* ilist  :  an item or a list of items<br>
    List to obtain an item from<br>
* k  :  int<br>
    item to be returned<br>


<a name="firstIndex"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>firstIndex(</strong> condition=lambda x: True ) 
</th></tr></thead></table>
<p>

Returns the index of first item in the `iterable` that
satisfies the `condition`.

If the condition is not given, it returns 0

<b>Parameters</b>

* iterable  :  iterable<br>
    to find the first item in<br>
* condition  :  lambda function<br>
    the condition<br>

<b>Raises</b>

    StopIteration: if no item satysfing the condition is found.<br>

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
<p>

Return the kcol-th column from xdata

<b>Parameters</b>

xdata   2D array_like or Table
    the data array<br>
kcol    int
    column index

<a name="isBetween"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBetween(</strong> x, xe ) 
</th></tr></thead></table>
<p>

Return True when x falls between xs and xe or on xs or xe.
    where the order of xs, xe is unknown.

<a name="getKwargs"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getKwargs(</strong> ) 
</th></tr></thead></table>
<p>

Return kwargs as dictionary

<a name="setAttribute"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setAttribute(</strong> name, value, type=None, islist=False, isnone=False ) 
</th></tr></thead></table>
<p>

Set an attribute to an object.

<b>Parameters</b>

* obj  :  object<br>
    to set the attribute to<br>
* name  :  str<br>
    of the attribute<br>
* value  :  any<br>
    of the attribute<br>
* type  :  class<br>
    check class of the object<br>
* islist  :  boolean<br>
    check if it is a list of type<br>
* isnone  :  boolean<br>
    value could be a None<br>

<b>Raises</b>

TypeError : if any  checks fails

<a name="setNoneAttributes"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setNoneAttributes(</strong> name, value, listNone ) 
</th></tr></thead></table>
<p>

Set attribute contained in dictionary dictList into the attr-list.
A list is a native list or a numpy.ndarray. It also checks the type.
if values is a singular item of the proper type it will be inserted as [value].

<b>Parameters</b>

* obj  :  object<br>
    to place the attribute in<br>
* name  :  str<br>
    of the attribute<br>
* value  :  any<br>
    of the attribute<br>
* listNone  :  list of names<br>
    that could have a None value<br>

<b>Returns</b>

    True on succesful insertion. False otherwise.<br>

<b>Raises</b>

    TypeError   if the type is not as in the dictionary

<a name="setListOfAttributes"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setListOfAttributes(</strong> name, value, dictList ) 
</th></tr></thead></table>
<p>

Set attribute contained in dictionary dictList into the attr-list.
A list is a native list or a numpy.ndarray. It also checks the type.
if values is a singular item of the proper type it will be inserted as [value].

<b>Parameters</b>

* obj  :  object<br>
    to place the attribute in<br>
* name  :  str<br>
    of the attribute<br>
* value  :  any<br>
    of the attribute<br>
* dictList  :  dictionary<br>
    of possible attributes {"name": type}<br>

<b>Returns</b>

    True on succesful insertion. False otherwise.<br>

<b>Raises</b>

    TypeError   if the type is not as in the dictionary<br>


<a name="setSingleAttributes"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setSingleAttributes(</strong> name, value, dictSingle ) 
</th></tr></thead></table>
<p>

Set a singular attribute contained in dictionary dictSingle into the attr-list.
It also checks the type.

<b>Parameters</b>

* obj  :  object<br>
    to place the attribute in<br>
* name  :  str<br>
    of the attribute<br>
* value  :  any<br>
    of the attribute<br>
* dictSingle  :  dictionary<br>
    of possible attributes {"name": type}<br>

<b>Returns</b>

    True on succesful insertion. False otherwise.<br>

<b>Raises</b>

    TypeError   if the type is not as in the dictionary

<a name="makeNext"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makeNext(</strong> k ) 
</th></tr></thead></table>
<p>

Return next item of x, and last item if x is exhausted.
Or x itself if x is singular.

<a name="length"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>length(</strong> ) 
</th></tr></thead></table>
<p>

Return the length of any item. Singletons have length 1; None has length 0..

<a name="toArray"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>toArray(</strong> ndim=1, dtype=None ) 
</th></tr></thead></table>
<p>

Return a array of x when x is a number

<b>Parameters</b>

* x  :  any number, list/array of numbers or []<br>
    to be converted to numpy.ndarray<br>
* ndim  :  int<br>
    minimum number of dimensions present<br>
* dtype  :  type<br>
    conversion to type (None : as is)<br>


<a name="isList"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isList(</strong> cls ) 
</th></tr></thead></table>
<p>

Return (True,False) if item is a instance of cls
       (True,True)  if item is a (list|ndarray) of instances of cls<br>
       (False,False) if not

<a name="isInstance"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isInstance(</strong> cls ) 
</th></tr></thead></table>
<p>

Returns true when one of the following is true
1. when cls is int   : item is an int or item is a numpy.integer.
2. when cls is float : item is an float or item is an int.
3. when cls is cls   : item is a cls.

<a name="ndprint"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>ndprint(</strong> form='{0:.3f}' ) 
</th></tr></thead></table>
<p>

Print a ndarray, formatted.

<a name="decorate"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>decorate(</strong> des, copy=True ) 
</th></tr></thead></table>
<p>

Transfer attributes from src to des.
If copy is True try to copy the attributes, otherwise link it.

<b>Parameters</b>

* src  :  object<br>
    source of the attributes<br>
* des  :  object<br>
    destiny for the attributes<br>
* copy  :  bool<br>
    if True: copy

<a name="subclassof"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>subclassof(</strong> cls ) 
</th></tr></thead></table>
<p>

Determine if sub inherits from the class cls

<b>Parameters</b>

* sub  :  class object<br>
    supposed sub class<br>
* cls  :  class object<br>
    supposed parent class

<a name="printclass"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>printclass(</strong> nitems=8, printId=False ) 
</th></tr></thead></table>
<p>

Print the attributes of a class.

<a name="printlist"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>printlist(</strong> nitems=8 ) 
</th></tr></thead></table>
<p>
<a name="shortName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shortName(</strong> )
</th></tr></thead></table>
<p>

Return a short version the string representation: upto first non-letter.

<a name="nicenumber"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>nicenumber(</strong> ) 
</th></tr></thead></table>
<p>

Return a nice number close to (but below) |x|.

<a name="fix2int"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fix2int(</strong> ) 
</th></tr></thead></table>
<p>

Return integer array with values as in x
<b>Parameters</b>

* x  :  array_like<br>
    array of integer floats

<a name="track"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>track(</strong> ) 
</th></tr></thead></table>
<p>


<b>Parameters</b>

* statement  :  str<br>
    statement to be traced<br>


<a name="average"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>average(</strong> weights=None, circular=None ) 
</th></tr></thead></table>
<p>

Return (weighted) average and standard deviation of input array.

<b>Parameters</b>

* xx  :  array_like<br>
    input to be averaged<br>
* weights  :  array_like<br>
    if present these are the weights<br>
* circular  :  list of 2 floats<br>
    the input is a circular item between [low,high]

