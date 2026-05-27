---
---
<br><br>

<a name="Formatter"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>Module Formatter</strong> </th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Formatter.py target=_blank>[source]</a></th></tr></thead></table>
<p>


This module contains methods to format numbers, especially in arrays.

<b>Examples</b>

    arr = numpy.linspace( 0, 10, 48 ).reshape( (4,12) )
    print( "array ", formatter( arr, indent=7, tail=2, max=5 ) )
    array  [[    0.000    0.213    0.426    0.638    0.851 ...    2.128    2.340]
            [    2.553    2.766    2.979    3.191    3.404 ...    4.681    4.894]
            [    5.106    5.319    5.532    5.745    5.957 ...    7.234    7.447]
            [    7.660    7.872    8.085    8.298    8.511 ...    9.787   10.000]]  


<a name="formatter_init"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>formatter_init(</strong> format={}, indent=None, linelength=None, max=-1 )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Formatter.py#L54-L86 target=_blank>[source]</a></th></tr></thead></table>

Initialize the formatter with new default values.

<b>Parameters</b><br>
* format  :  dict {namestring : formatstring }
<br>&nbsp;&nbsp;&nbsp;&nbsp; name : "float64" or "int64"
<br>&nbsp;&nbsp;&nbsp;&nbsp; fmt  : " %fmt"
* indent  :  None or int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of spaces to indent *after* the first line
<br>&nbsp;&nbsp;&nbsp;&nbsp; Default is 0
* linelength  :  None or int
<br>&nbsp;&nbsp;&nbsp;&nbsp; length of the lines produced
<br>&nbsp;&nbsp;&nbsp;&nbsp; Default is 120
* max  :  None or int
<br>&nbsp;&nbsp;&nbsp;&nbsp; maximum number of items displayed followed by ... if there are more
<br>&nbsp;&nbsp;&nbsp;&nbsp; None displays all
<br>&nbsp;&nbsp;&nbsp;&nbsp; Default is 5

<a name="fma"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fma(</strong> erray, **kwargs ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Formatter.py#L88-L95 target=_blank>[source]</a></th></tr></thead></table>
Syntactic sugar for
<br>&nbsp;&nbsp;&nbsp;&nbsp; formatter( ..., max=None, ... )

It formats ALL numbers in the array

<a name="gmt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>gmt(</strong> erray, **kwargs ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Formatter.py#L97-L104 target=_blank>[source]</a></th></tr></thead></table>
Syntactic sugar for
<br>&nbsp;&nbsp;&nbsp;&nbsp; formatter( ..., format=" %#10.3g", ... )

It formats the array in "%#10.3g" format.

<a name="formatter"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>formatter(</strong> erray, format=None, indent=None, linelength=None, max=-1, tail=0 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Formatter.py#L106-L165 target=_blank>[source]</a></th></tr></thead></table>
Format a number or an array nicely into a string

Parameters override defaults given earlier with init().

<b>Parameters</b><br>
* erray  :  array or number
<br>&nbsp;&nbsp;&nbsp;&nbsp; number or list of numbers or n-dim array of numbers
* format  :  None or string
<br>&nbsp;&nbsp;&nbsp;&nbsp; format applying to one item of array
<br>&nbsp;&nbsp;&nbsp;&nbsp; Default is "8.3f" for float and "8d" for int
* indent  :  None or int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of spaces to indent *after* the first line
<br>&nbsp;&nbsp;&nbsp;&nbsp; Default is 0
* linelength  :  None or int
<br>&nbsp;&nbsp;&nbsp;&nbsp; length of the lines produced
<br>&nbsp;&nbsp;&nbsp;&nbsp; Default is 120
* max  :  None or int
<br>&nbsp;&nbsp;&nbsp;&nbsp; maximum number of items displayed followed by ... if there are more
<br>&nbsp;&nbsp;&nbsp;&nbsp; None displays all
<br>&nbsp;&nbsp;&nbsp;&nbsp; Default is 5
* tail  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; print the last items in the array, preceeded by ...
<br>&nbsp;&nbsp;&nbsp;&nbsp; Only if the number of items is larger than max.
<br>&nbsp;&nbsp;&nbsp;&nbsp; Default is 0

<b>Returns</b><br>
* string  :  containing the formatted array


<a name="spaces"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>spaces(</strong> ksp ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Formatter.py#L212-L215 target=_blank>[source]</a></th></tr></thead></table>
Return ksp spaces.

