---
---


<a name="Engine"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class Engine(</strong> object )
</th></tr></thead></table>

<b></b>

<a name="Engine"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>Engine(</strong> walkers, errdis, slow=None, phancol=None, copy=None,
 seed=4213, verbose=0 )
</th></tr></thead></table>

<b></b>

<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>

Return a copy of this engine. 

<a name="bestBoost"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>bestBoost(</strong> problem, myFitter=None ) 
</th></tr></thead></table>


<a name="setWalker"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>setWalker(</strong> kw, problem, allpars, logL, walker=None, fitIndex=None ) 
</th></tr></thead></table>

<b></b>

<a name="noBoost"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>noBoost(</strong> walker ) 
</th></tr></thead></table>
<a name="doBoost"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>doBoost(</strong> walker ) 
</th></tr></thead></table>

<b></b>

<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> problem, dval, kpar=None ) 
</th></tr></thead></table>

<b></b>

<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> problem, uval, kpar=None ) 
</th></tr></thead></table>

<b></b>

<a name="startJourney"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>startJourney(</strong> unitStart ) 
</th></tr></thead></table>

<b></b>

<a name="calcJourney"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>calcJourney(</strong> unitDistance ) 
</th></tr></thead></table>

<b></b>

<a name="unitTripSquare"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>unitTripSquare(</strong> unitDistance ) 
</th></tr></thead></table>

<b></b>

<a name="reportJourney"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>reportJourney(</strong> ) 
</th></tr></thead></table>
<a name="makeIndex"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>makeIndex(</strong> np, val ) 
</th></tr></thead></table>
<a name="reportCall"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>reportCall(</strong> )
</th></tr></thead></table>

Store a call to engine 

<a name="reportSuccess"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>reportSuccess(</strong> )
</th></tr></thead></table>


<a name="reportReject"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>reportReject(</strong> )
</th></tr></thead></table>


<a name="reportFailed"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>reportFailed(</strong> )
</th></tr></thead></table>


<a name="reportBest"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>reportBest(</strong> )
</th></tr></thead></table>


<a name="printReport"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>printReport(</strong> best=False ) 
</th></tr></thead></table>
<a name="successRate"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>successRate(</strong> ) 
</th></tr></thead></table>


<a name="getUnitMinmax"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>getUnitMinmax(</strong> problem, lowLhood, nap ) 
</th></tr></thead></table>

<b></b>

<a name="getUnitRange"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>getUnitRange(</strong> problem, lowLhood, nap ) 
</th></tr></thead></table>

<b></b>

<a name="__str__"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>__str__(</strong> ) 
</th></tr></thead></table>
<a name="execute"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>execute(</strong> kw, lowLhood )
</th></tr></thead></table>

<b></b>
<b></b>



<a name="DummyPlotter"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class DummyPlotter(</strong> object ) 
</th></tr></thead></table>
<a name="Engine"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>Engine(</strong> iter=1 ) 
</th></tr></thead></table>
<a name="start"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>start(</strong> param=None, ulim=None )
</th></tr></thead></table>

start the plot. 

<a name="point"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>point(</strong> param, col=None, sym=0 )
</th></tr></thead></table>


<a name="move"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>move(</strong> param, ptry, col=None, sym=None )
</th></tr></thead></table>


<a name="stop"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>stop(</strong> param=None, name=None )
</th></tr></thead></table>

Stop (show) the plot. 


