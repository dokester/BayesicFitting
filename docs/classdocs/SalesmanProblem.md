---
---
<br><br>

<a name="SalesmanProblem"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class SalesmanProblem(</strong> <a href="./OrderProblem.html">OrderProblem</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/SalesmanProblem.py target=_blank>Source</a></th></tr></thead></table>
<p>

Traveling Salesman Problem.

The parameters give the order in which the nodes are visited.

The result is a list of distances.

&nbsp;&nbsp;&nbsp;&nbsp; [dist( x[p[k-1]], x[p[k]] ) for k in range( len( p ) )]<br>

The number of parameters is equal to the length of the xdata array
The parameters are initialized at [k for k in range( npars )]

<b>Examples</b>

     tsm = SalesmanProblem( 100 )
    print( tsm )
TravelingSalesman in 2 dimensions with 100 nodes.
    print( tsm.npars )
100



<a name="SalesmanProblem"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>SalesmanProblem(</strong> xdata=None, weights=None, distance="euclid", scale=None, table=None,
 oneway=False, copy=None )
</th></tr></thead></table>
<p>

Traveling Salesman problem.


<b>Parameters</b>

* xdata  :  array_like of shape [np,ndim]<br>
&nbsp;&nbsp;&nbsp;&nbsp; the nodes to be visited<br>
* weights  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; weights on the arrival nodes<br>
* distance  :  str or callable<br>
&nbsp;&nbsp;&nbsp;&nbsp; to calculate the distance between point1 and point2<br>
&nbsp;&nbsp;&nbsp;&nbsp; "manh"   : Manhattan distance (1 norm) (2 or more dimensions)<br>
&nbsp;&nbsp;&nbsp;&nbsp; "euclid" : Euclidic (2 norm) (2 or more dimensions) <br>
&nbsp;&nbsp;&nbsp;&nbsp; "spher"  : spherical, distance over sphere (2 dimensions only) <br>
&nbsp;&nbsp;&nbsp;&nbsp; "table"  : tabulated distance values<br>
&nbsp;&nbsp;&nbsp;&nbsp; callable of the form callable( xdata, pars )<br>
* scale  :  None or float<br>
&nbsp;&nbsp;&nbsp;&nbsp; scale all distances by this number.<br>
&nbsp;&nbsp;&nbsp;&nbsp; None : take minimum distance as scale<br>
* table  :  arraylike or None<br>
&nbsp;&nbsp;&nbsp;&nbsp; table of all distances, Only when distance is "tabulated"<br>
* oneway  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; Don't close the loop; cut at position 0.<br>
* copy  :  SalesmanProblem<br>
&nbsp;&nbsp;&nbsp;&nbsp; to be copied<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Copy method. 

<a name="acceptWeight"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>acceptWeight(</strong> )
</th></tr></thead></table>
<p>

True if the distribution accepts weights.


<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> params )
</th></tr></thead></table>
<p>

Calculates the distance between the nodes (xdata) in the order
given by the parameters (params), multiplied by the weight at the 
starting node (if present), divided by the scale

Each result is 
&nbsp;&nbsp;&nbsp;&nbsp; res[k] = dis[k] * weight[params[k]] / scale<br>

<b>Parameters</b>

* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; values for the parameters.<br>

<b>Returns</b>

An array of distances


<a name="manhattan"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>manhattan(</strong> xdata, pars, roll=1 ) 
</th></tr></thead></table>
<p>

Use Manhattan distances (1-norm)

Each distance is 
&nbsp;&nbsp;&nbsp;&nbsp; dis[k] = SUM_i ( abs( xdata[pars[k],i] - xdata[pars[k+roll],i] ) )<br>

<b>Parameters</b>

* xdata  :  array-like of shape (ndata,ndim) <br>
&nbsp;&nbsp;&nbsp;&nbsp; positional info in several dimensions<br>
* pars  :  list of indices<br>
&nbsp;&nbsp;&nbsp;&nbsp; designating the order of the nodess<br>
* roll  :  int<br>
    number of positions to roll 

<a name="euclidic"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>euclidic(</strong> xdata, pars, roll=1 ) 
</th></tr></thead></table>
<p>

Use Euclidic distances (2-norm)

Each distance is 
&nbsp;&nbsp;&nbsp;&nbsp; dis[k] = sqrt( SUM_i ( ( xdata[pars[k],i] - xdata[pars[k+roll],i] )^2 ) )<br>

<b>Parameters</b>

* xdata  :  array-like of shape (ndata,ndim) <br>
&nbsp;&nbsp;&nbsp;&nbsp; positional info in several dimensions<br>
* pars  :  list of indices<br>
&nbsp;&nbsp;&nbsp;&nbsp; designating the order of the nodes<br>
* roll  :  int<br>
    number of positions to roll 

<a name="spherical"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>spherical(</strong> xdata, pars, roll=1 ) 
</th></tr></thead></table>
<p>

Use distances over a 2-d unit sphere.

Each distance is calculated according to the Haversine formula.

It is assumed that the xdata is in decimal degrees: [longitude, latitude]

The results are in radian.

<b>Parameters</b>

* xdata  :  array-like of shape (ndata,2) <br>
&nbsp;&nbsp;&nbsp;&nbsp; longitude, latitude info<br>
* pars  :  list of indices<br>
&nbsp;&nbsp;&nbsp;&nbsp; designating the order of the nodes<br>
* roll  :  int<br>
    number of positions to roll 

<a name="tabulated"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>tabulated(</strong> xdata, pars, roll=1 ) 
</th></tr></thead></table>
<p>

Use tabulated distances from self.table

Each distance is 
&nbsp;&nbsp;&nbsp;&nbsp; dis[k] = table[ pars[k], pars[k+roll] ]<br>

<b>Parameters</b>

* xdata  :  array-like of shape (ndata,ndim) <br>
&nbsp;&nbsp;&nbsp;&nbsp; positional info in several dimensions<br>
* pars  :  list of indices<br>
&nbsp;&nbsp;&nbsp;&nbsp; designating the order of the nodess<br>
* roll  :  int<br>
    number of positions to roll 

<a name="minimumDistance"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>minimumDistance(</strong> ) 
</th></tr></thead></table>
<p>

Return the smallest distance in the data.



ndata = len( self.xdata[:,0] )
pars = numpy.arange( ndata, dtype=int )
md = self.distance( self.xdata, pars ).min()
for roll in range( 2, ndata ) 
&nbsp;&nbsp;&nbsp;&nbsp; md = self.distance( self.xdata, pars, roll=roll ).min( initial=md )<br>

return md

<a name="baseName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>baseName(</strong> )
</th></tr></thead></table>
<p>
baseName( self )


return str( "TravelingSalesman in %d dimensions with %d nodes. %s distance" %
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ( self.ndim, self.npars, self.disname ) )<br>



<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./OrderProblem.html">OrderProblem</a></th></tr></thead></table>


* [<strong>isDynamic(</strong> ) ](./OrderProblem.md#isDynamic)
* [<strong>myEngines(</strong> ) ](./OrderProblem.md#myEngines)
* [<strong>myStartEngine(</strong> ) ](./OrderProblem.md#myStartEngine)
* [<strong>myDistribution(</strong> ) ](./OrderProblem.md#myDistribution)


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./Problem.html">Problem</a></th></tr></thead></table>


* [<strong>setAccuracy(</strong> accuracy=None ) ](./Problem.md#setAccuracy)
* [<strong>hasWeights(</strong> )](./Problem.md#hasWeights)
* [<strong>residuals(</strong> param, mockdata=None ) ](./Problem.md#residuals)
* [<strong>cyclicCorrection(</strong> res )](./Problem.md#cyclicCorrection)
* [<strong>cycor1(</strong> res )](./Problem.md#cycor1)
* [<strong>cycor2(</strong> res )](./Problem.md#cycor2)
* [<strong>cyclize(</strong> res, period ) ](./Problem.md#cyclize)
* [<strong>weightedResSq(</strong> allpars, mockdata=None, extra=False ) ](./Problem.md#weightedResSq)
* [<strong>domain2Unit(</strong> dval, kpar ) ](./Problem.md#domain2Unit)
* [<strong>unit2Domain(</strong> uval, kpar ) ](./Problem.md#unit2Domain)
* [<strong>shortName(</strong> ) ](./Problem.md#shortName)
