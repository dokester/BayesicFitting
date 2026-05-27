---
---
<br><br>

<a name="Tools"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>Module Tools</strong> </th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py target=_blank>[source]</a></th></tr></thead></table>
<p>


This module contains a mixed bag of "usefull" methods.


<a name="getItem"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getItem(</strong> ilist, k ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L38-L54 target=_blank>[source]</a></th></tr></thead></table>

Return the k-th item of the ilist
<br>&nbsp;&nbsp;&nbsp;&nbsp; or the last when not enough
<br>&nbsp;&nbsp;&nbsp;&nbsp; or the ilist itself when it is not a list

<b>Parameters</b><br>
* ilist  :  an item or a list of items
<br>&nbsp;&nbsp;&nbsp;&nbsp; List to obtain an item from
* k  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; item to be returned


<a name="firstIndex"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>firstIndex(</strong> iterable, condition=lambda x: True ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L56-L87 target=_blank>[source]</a></th></tr></thead></table>
Returns the index of first item in the `iterable` that
satisfies the `condition`.

If the condition is not given, it returns 0

<b>Parameters</b><br>
* iterable  :  iterable
<br>&nbsp;&nbsp;&nbsp;&nbsp; to find the first item in
* condition  :  lambda function
<br>&nbsp;&nbsp;&nbsp;&nbsp; the condition

<b>Raises</b><br>
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
<strong>getColumnData(</strong> xdata, kcol ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L89-L105 target=_blank>[source]</a></th></tr></thead></table>
Return the kcol-th column from xdata

<b>Parameters</b><br>
xdata   2D array_like or Table
<br>&nbsp;&nbsp;&nbsp;&nbsp; the data array
kcol    int
<br>&nbsp;&nbsp;&nbsp;&nbsp; column index

<a name="isBetween"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isBetween(</strong> xs, x, xe ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L107-L112 target=_blank>[source]</a></th></tr></thead></table>
Return True when x falls between xs and xe or on xs or xe.
<br>&nbsp;&nbsp;&nbsp;&nbsp; where the order of xs, xe is unknown.

<a name="getKwargs"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getKwargs(</strong> **kwargs ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L114-L118 target=_blank>[source]</a></th></tr></thead></table>
Return kwargs as dictionary

<a name="setAttribute"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setAttribute(</strong> obj, name, value, type=None, islist=False, isnone=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L120-L150 target=_blank>[source]</a></th></tr></thead></table>

<a name="setNoneAttributes"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setNoneAttributes(</strong> obj, name, value, listNone ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L152-L179 target=_blank>[source]</a></th></tr></thead></table>
Set an attribute to an object.

<b>Parameters</b><br>
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

<b>Raises</b><br>
TypeError : if any  checks fails

<a name="setListOfAttributes"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setListOfAttributes(</strong> obj, name, value, dictList ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L181-L220 target=_blank>[source]</a></th></tr></thead></table>
Set attribute contained in dictionary dictList into the attr-list.
A list is a native list or a numpy.ndarray. It also checks the type.
if values is a singular item of the proper type it will be inserted as [value].

<b>Parameters</b><br>
* obj  :  object
<br>&nbsp;&nbsp;&nbsp;&nbsp; to place the attribute in
* name  :  str
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the attribute
* value  :  any
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the attribute
* listNone  :  list of names
<br>&nbsp;&nbsp;&nbsp;&nbsp; that could have a None value

<b>Returns</b><br>
&nbsp; True on succesful insertion. False otherwise.

<b>Raises</b><br>
&nbsp; TypeError   if the type is not as in the dictionary

<a name="setSingleAttributes"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setSingleAttributes(</strong> obj, name, value, dictSingle ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L222-L254 target=_blank>[source]</a></th></tr></thead></table>
<br>&nbsp; """
Set attribute contained in dictionary dictList into the attr-list.
A list is a native list or a numpy.ndarray. It also checks the type.
if values is a singular item of the proper type it will be inserted as [value].

<b>Parameters</b><br>
* obj  :  object
<br>&nbsp;&nbsp;&nbsp;&nbsp; to place the attribute in
* name  :  str
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the attribute
* value  :  any
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the attribute
* dictList  :  dictionary
<br>&nbsp;&nbsp;&nbsp;&nbsp; of possible attributes {"name": type}

<b>Returns</b><br>
&nbsp; True on succesful insertion. False otherwise.

<b>Raises</b><br>
&nbsp; TypeError   if the type is not as in the dictionary


<a name="makeNext"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>makeNext(</strong> x, k ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L256-L291 target=_blank>[source]</a></th></tr></thead></table>
Set a singular attribute contained in dictionary dictSingle into the attr-list.
It also checks the type.

<b>Parameters</b><br>
* obj  :  object
<br>&nbsp;&nbsp;&nbsp;&nbsp; to place the attribute in
* name  :  str
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the attribute
* value  :  any
<br>&nbsp;&nbsp;&nbsp;&nbsp; of the attribute
* dictSingle  :  dictionary
<br>&nbsp;&nbsp;&nbsp;&nbsp; of possible attributes {"name": type}

<b>Returns</b><br>
&nbsp; True on succesful insertion. False otherwise.

<b>Raises</b><br>
&nbsp; TypeError   if the type is not as in the dictionary

<a name="length"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>length(</strong> x ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L293-L303 target=_blank>[source]</a></th></tr></thead></table>
<br>&nbsp; """
Return next item of x, and last item if x is exhausted.
Or x itself if x is singular.

<a name="toArray"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>toArray(</strong> x, ndim=1, dtype=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L305-L311 target=_blank>[source]</a></th></tr></thead></table>
Return the length of any item. Singletons have length 1; None has length 0..

<a name="isList"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isList(</strong> item, cls ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L313-L333 target=_blank>[source]</a></th></tr></thead></table>
Return a array of x when x is a number

<b>Parameters</b><br>
* x  :  any number, list/array of numbers or []
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be converted to numpy.ndarray
* ndim  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; minimum number of dimensions present
* dtype  :  type
<br>&nbsp;&nbsp;&nbsp;&nbsp; conversion to type (None : as is)


<a name="isInstance"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isInstance(</strong> item, cls ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L335-L346 target=_blank>[source]</a></th></tr></thead></table>
Return (True,False) if item is a instance of cls
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (True,True)  if item is a (list|ndarray) of instances of cls
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (False,False) if not

<a name="subclassof"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>subclassof(</strong> sub, cls ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L348-L369 target=_blank>[source]</a></th></tr></thead></table>
Transfer attributes from src to des.
If copy is True try to copy the attributes, otherwise link it.

<b>Parameters</b><br>
* src  :  object
<br>&nbsp;&nbsp;&nbsp;&nbsp; source of the attributes
* des  :  object
<br>&nbsp;&nbsp;&nbsp;&nbsp; destiny for the attributes
* copy  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; if True: copy

<a name="printclass"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>printclass(</strong> cls, nitems=8, printId=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L371-L417 target=_blank>[source]</a></th></tr></thead></table>
Determine if sub inherits from the class cls

<b>Parameters</b><br>
* sub  :  class object
<br>&nbsp;&nbsp;&nbsp;&nbsp; supposed sub class
* cls  :  class object
<br>&nbsp;&nbsp;&nbsp;&nbsp; supposed parent class

<a name="printlist"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>printlist(</strong> val, nitems=8 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L419-L439 target=_blank>[source]</a></th></tr></thead></table>

<a name="shortName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shortName(</strong> val )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L441-L447 target=_blank>[source]</a></th></tr></thead></table>
Print the attributes of a class.

<a name="nicenumber"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>nicenumber(</strong> x ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L449-L469 target=_blank>[source]</a></th></tr></thead></table>
Return a short version the string representation: upto first non-letter.

<a name="average"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>average(</strong> xx, weights=None, circular=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L471-L508 target=_blank>[source]</a></th></tr></thead></table>

<b>Parameters</b><br>
* statement  :  str
<br>&nbsp;&nbsp;&nbsp;&nbsp; statement to be traced


<a name="toRect"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>toRect(</strong> rp, phi=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L510-L545 target=_blank>[source]</a></th></tr></thead></table>
Return (x,y) coordinates from (rho,phi)

Angles are measured counterclockwise from north to east
North is Down (-y) and East is to the Right (+x)

<b>Parameters</b><br>
* rp  :  array of pairs [rho,phi] or tuple of (rhos,phis)
<br>&nbsp;&nbsp;&nbsp;&nbsp; rp[:,0] : separation of the stars
<br>&nbsp;&nbsp;&nbsp;&nbsp; rp[:,1] : angle from north (down) CCW to east (right)
* phi  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; When phi is given, rp is interpeted as rho.

<b>Returns</b><br>
2d-array if the input is a 2d-array  or
tuple of 2 arrays if the input is a tuple of 2 arrays or phi is given


<a name="toRect3D"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>toRect3D(</strong> rho, phi, theta )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L547-L577 target=_blank>[source]</a></th></tr></thead></table>
Return (x,y,z) coordinates from (rho,phi,theta)

The angle phi is measured counterclockwise from north to east
North is Down (-y) and East is to the Right (+x)
The angle theta is measured form the (x,y) plane. 
Up is positive (+) and down is negative (-)

<b>Parameters</b><br>
* rho  :  array of float
<br>&nbsp;&nbsp;&nbsp;&nbsp; Separation between the stars
* phi  :  array of float
<br>&nbsp;&nbsp;&nbsp;&nbsp; angle in (x,y) plane from -y (North,down) to +x (East,right)
* theta  :  array of float 
<br>&nbsp;&nbsp;&nbsp;&nbsp; angle between z and star 2

<b>Returns</b><br>
* (x,y,z)  :  tuple of 3 arrays 


<a name="toSpher3D"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>toSpher3D(</strong> x, y, z ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L579-L604 target=_blank>[source]</a></th></tr></thead></table>
Return (rho,phi,theta) coordinates from (x,y,z)

See toRect3D()

<b>Parameters</b><br>
* x  :  array of float
<br>&nbsp;&nbsp;&nbsp;&nbsp; x position
* y  :  array of float
<br>&nbsp;&nbsp;&nbsp;&nbsp; y position
* z  :  array of float
<br>&nbsp;&nbsp;&nbsp;&nbsp; z position

<b>Returns</b><br>
* (rho,phi,theta)  :  tuple of 3 arrays 


<a name="toSpher"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>toSpher(</strong> xy, y=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L606-L641 target=_blank>[source]</a></th></tr></thead></table>
Return (rho,phi) coordinates from (x,y)

Angles are measured counterclockwise from north to east
North is Down (-y) and East is to the Right (+x)

<b>Parameters</b><br>
* xy  :  array of pairs [x,y] or tuple of (x array,y array)
<br>&nbsp;&nbsp;&nbsp;&nbsp; xy[:,0] : x position
<br>&nbsp;&nbsp;&nbsp;&nbsp; xy[:,1] : y position
* y  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; when given xy is interpreted as x

<b>Returns</b><br>
2d-array if the input is a 2d-array  or
tuple of 2 arrays if the input is a tuple of 2 arrays or when y is given


<a name="arrow"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>arrow(</strong> x, y, z=None, scale=1.0 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L643-L711 target=_blank>[source]</a></th></tr></thead></table>
Return the coordinates of an arrow point from (xyz[0]) to (xyz[1])

The returned 2-d coordinates are at
<br>&nbsp;&nbsp;&nbsp;&nbsp; tail, top, left-head, right-head, top 

the returned 3-d coordinates are at 
<br>&nbsp;&nbsp;&nbsp;&nbsp; tail, top, left-head, right-head, top, read-head, near-head, top

<b>Parameters</b><br>
* x  :  array of length 2 (at least)
<br>&nbsp;&nbsp;&nbsp;&nbsp; x-coordinates
* y  :  array of length 2 (at least)
<br>&nbsp;&nbsp;&nbsp;&nbsp; y-coordinates
* z  :  array of length 2 or None
n None return 2D array else 3D
* scale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; scale factor. End point stays in place

<a name="minmax"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>minmax(</strong> x, range=False, mid=False ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Tools.py#L713-L734 target=_blank>[source]</a></th></tr></thead></table>
Return minimum, maximum, range and midpoint of an array

<b>Parameters</b><br>
* x  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; the array
* range  :  bool (False)
<br>&nbsp;&nbsp;&nbsp;&nbsp; return range (max - min) too
* mid  :  bool (False)
<br>&nbsp;&nbsp;&nbsp;&nbsp; return midpoint (max + min) / 2 too

