---
---
<br><br>

<a name="SampleMovie"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class SampleMovie(</strong> object )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/SampleMovie.py target=_blank>Source</a></th></tr></thead></table>

SampleMovie produces a movie (mp4) from a SampleList

This class is provided as an example to vary upon.

This example uses a MovieWriter directly to grab individual frames and write
them to a file. This avoids any event loop integration, but has the advantage
of working with even the Agg backend. This is not recommended for use in an
interactive setting.


<a name="SampleMovie"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>SampleMovie(</strong> samplelist, filename="samplemovie.mp4", problem=None, kpar=[0,1] ) 
</th></tr></thead></table>

Constructor.

The constructor produces the movie.

<b>Parameters</b>

* samplelist  :  SampleList
<br>&nbsp;&nbsp;&nbsp;&nbsp; to make the movie from
* filename  :  str
<br>&nbsp;&nbsp;&nbsp;&nbsp; name of the mp4 movie
* problem  :  Problem
<br>&nbsp;&nbsp;&nbsp;&nbsp; the problem that produced the samplelist
* kpar  :  list of 2 ints
<br>&nbsp;&nbsp;&nbsp;&nbsp; indices of the parameters to plot

