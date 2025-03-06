---
---

<a name="formatter_init"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>formatter_init(</strong> indent=None, linelength=None, max=-1 )
</th></tr></thead></table>
<p>

Initialize the formatter with new default values.

<b>Parameters</b>

* format  :  dict {namestring : formatstring }<br>
&nbsp;&nbsp;&nbsp;&nbsp; name : "float64" or "int64"<br>
&nbsp;&nbsp;&nbsp;&nbsp; fmt  : " %fmt"<br>
* indent  :  None or int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of spaces to indent *after* the first line<br>
&nbsp;&nbsp;&nbsp;&nbsp; Default is 0<br>
* linelength  :  None or int<br>
&nbsp;&nbsp;&nbsp;&nbsp; length of the lines produced<br>
&nbsp;&nbsp;&nbsp;&nbsp; Default is 120<br>
* max  :  None or int<br>
&nbsp;&nbsp;&nbsp;&nbsp; maximum number of items displayed followed by ... if there are more<br>
&nbsp;&nbsp;&nbsp;&nbsp; None displays all<br>
    Default is 5

<a name="fma"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fma(</strong> **kwargs ) 
</th></tr></thead></table>
<p>

Syntactic sugar for
    formatter( ..., max=None, ... )

<a name="formatter"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>formatter(</strong> format=None, indent=None, linelength=None, max=-1, tail=0 ) 
</th></tr></thead></table>
<p>

Format a number or an array nicely into a string

Parameters override defaults given earlier with init().

<b>Parameters</b>

* array  :  array_like or number<br>
&nbsp;&nbsp;&nbsp;&nbsp; number or list of numbers or n-dim array of numbers<br>
* format  :  None or string<br>
&nbsp;&nbsp;&nbsp;&nbsp; format applying to one item of array<br>
&nbsp;&nbsp;&nbsp;&nbsp; Default is "8.3f" for float and "8d" for int<br>
* indent  :  None or int<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of spaces to indent *after* the first line<br>
&nbsp;&nbsp;&nbsp;&nbsp; Default is 0<br>
* linelength  :  None or int<br>
&nbsp;&nbsp;&nbsp;&nbsp; length of the lines produced<br>
&nbsp;&nbsp;&nbsp;&nbsp; Default is 120<br>
* max  :  None or int<br>
&nbsp;&nbsp;&nbsp;&nbsp; maximum number of items displayed followed by ... if there are more<br>
&nbsp;&nbsp;&nbsp;&nbsp; None displays all<br>
&nbsp;&nbsp;&nbsp;&nbsp; Default is 5<br>
* tail  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; print the last items in the array, preceeded by ...<br>
&nbsp;&nbsp;&nbsp;&nbsp; Only if the number of items is larger than max.<br>
&nbsp;&nbsp;&nbsp;&nbsp; Default is 0<br>

<b>Returns</b>

* string  :  containing the formatted array<br>


<a name="recursive_format"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>recursive_format(</strong> array, format=None, indent=0, tail=0 ) 
</th></tr></thead></table>
<p>
<a name="spaces"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>spaces(</strong> ) 
</th></tr></thead></table>
<p>

Return ksp spaces.

