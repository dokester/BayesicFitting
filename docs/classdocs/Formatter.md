---
---
<br><br>

<a name="Formatter"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>Module Formatter</strong> </th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source// target=_blank>[source]</a></th></tr></thead></table>
<p>


&nbsp; module contains methods to format numbers, especially in arrays.


<a name="formatter_init"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>formatter_init(</strong> format={}, indent=None, linelength=None, max=-1 )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L45-L77 target=_blank>[source]</a></th></tr></thead></table>

Initialize the formatter with new default values.

<b>Parameters</b>

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
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L79-L84 target=_blank>[source]</a></th></tr></thead></table>
Syntactic sugar for
<br>&nbsp;&nbsp;&nbsp;&nbsp; formatter( ..., max=None, ... )

<a name="gmt"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>gmt(</strong> erray, **kwargs ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L86-L91 target=_blank>[source]</a></th></tr></thead></table>
Syntactic sugar for
<br>&nbsp;&nbsp;&nbsp;&nbsp; formatter( ..., format=" %#10.3g", ... )

<a name="formatter"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>formatter(</strong> erray, format=None, indent=None, linelength=None, max=-1, tail=0 ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L93-L197 target=_blank>[source]</a></th></tr></thead></table>
Format a number or an array nicely into a string

Parameters override defaults given earlier with init().

<b>Parameters</b>

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

<b>Returns</b>

* string  :  containing the formatted array


<a name="spaces"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>spaces(</strong> ksp ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L199-L202 target=_blank>[source]</a></th></tr></thead></table>
Return ksp spaces.

