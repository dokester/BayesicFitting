---
---
<br><br>

<a name="LogFactorial"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>Module LogFactorial</strong> </th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/LogFactorial.py target=_blank>Source</a></th></tr></thead></table>


method that returns the log of the factorial of a number.


<a name="logFactorial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logFactorial(</strong> )
</th></tr></thead></table>

logFactorial.  It provides the natural log of k!

if k is float, it will be truncated to int

<b>Parameters</b>

* k  :  int or array_like of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; the number(s) the factorial is wanted for.

<b>Return</b>

* float  :  the ( natural ) log( k! ).


<b>Example</b>

    print( logFactorial( 0 ) )
    0
    print( logFactorial( [3, 5, 10] ) )
    [1.7917594692280550, 4.7874917427820458, 15.1044125730755159]

<b>Author</b>

Do Kester, shamelessly copied from J.Skilling



