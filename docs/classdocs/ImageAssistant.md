---
---
<br><br><br>

<a name="ImageAssistant"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class ImageAssistant(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/ImageAssistant.py target=_blank>Source</a></th></tr></thead></table>
<p>

ImageAssistant contains 2 methods to assist with more dimensional
fitting.

1. getIndices Generates indices for data arrays of any dimension.
   To be used as input in the Fitter classes.<br>
2. resizeData Resizes the data arrays into a 1-dimensional array.
   To be used as data in the Fitter.<br>




<b>Example</b>

    ymap = numpy.arange( 6, dtype=float ).reshape( 2, 3 )
    ias = ImageAssistant()
    ky = ias.getIndices( ymap )
    print( ky.shape )
    (6,2)<br>
    print( ky[4,0], ky[4,1], ymap[ ky[4,0], ky[4,1] ] )
    1 0 4<br>
    ias = ImageAssistant( order='F')
    ky = ias.getIndices( ymap )
    print( ky.shape )
    (6,2)<br>
    print( ky[4,0], ky[4,1], ymap[ ky[4,1], ky[4,0] ] )
    0 1 4<br>

## Suppose y is a 2-dimensional map of something
    aass = ImageAssistant( )
    input = aass.getIndices( y )
    fitter = Fitter( input, some2dModel )
    pars = fitter.fit( aass.resizeData( y ) )
    yfit = some2dModel.result( input )                  # Double1d
    yfit2d = aass.resizeData( yfit, shape=y.shape )     # Double2d


Author       Do Kester


<a name="ImageAssistant"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>ImageAssistant(</strong> order='C' )
</th></tr></thead></table>
<p>

Helper class to construct from an image, the input arrays
needed for the Fitters.

<b>Parameters</b>

* order  :  'C' or 'F'<br>
    set index view according to character<br>
    'C' orders from slow to fast<br>
    'F' orders from fast to slow

<a name="getIndices"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getIndices(</strong> ya, order='C' )
</th></tr></thead></table>
<p>

Generates indices for data arrays of any dimension.

To be used as input in the Fitter classes.

<b>Parameters</b>

* ya  :  map<br>
    array of y ( data ) values for which an indexed array<br>
* order  :  'C' or 'F'<br>
    set index view according to character<br>

<b>Returns</b>

* numpy.array of ints  :  the indices of the pixels<br>


<a name="getPositions"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getPositions(</strong> ymap, order='C', center=True, deproject=None ) 
</th></tr></thead></table>
<p>

Return the (x,y) positions of the pixels in the map.

<b>Parameters</b>

* ya  :  map<br>
    array of y ( data ) values for which an indexed array<br>
* order  :  'C' or 'F'<br>
    set index view according to character<br>
* center  :  bool<br>
    if True, return the positions of the center of the pixels.<br>
    otherwise the (left,lower) corner<br>
* deproject  :  callable<br>
    Deprojection method: from projected map to sky position,<br>
    returning (x,y,...) position given the map indices (ix,iy,...)<br>
    Default: returning the indices as floats (+0.5 if center)<br>

<b>Returns</b>

numpy.array of floats : the positions of the pixels

<a name="getydata"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getydata(</strong> ya )
</th></tr></thead></table>
<p>

Return a copy of ya as a 1 dim array.

<b>Parameters</b>

* ya  :  array_like<br>
    map to be reshaped

<a name="resizeData"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>resizeData(</strong> res, shape=None )
</th></tr></thead></table>
<p>

Reshape the data (res) into the same shape as the map (ya)

<b>Parameters</b>

* res  :  array_like<br>
    result of the fit as a 1-dim array<br>
* shape  :  tuple of int<br>
    dimensional lengths of the reconstructable map<br>
    default remembered from a call to getIndices

