---
---

<div class="button">
  <span style="background-color: DodgerBlue; color: White;  border:5px solid DodgerBlue">
<a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/SampleMovie.py target=_blank>Source</a></span></div>

<a name="SampleMovie"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left">
<strong>class SampleMovie(</strong> object )
</th></tr></thead></table>
<p>

SampleMovie produces a movie (mp4) from a SampleList

This class is provided as an example to vary upon.

===========
MovieWriter
===========

This example uses a MovieWriter directly to grab individual frames and write
them to a file. This avoids any event loop integration, but has the advantage
of working with even the Agg backend. This is not recommended for use in an
interactive setting.


<a name="SampleMovie"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th style="text-align:left">
<strong>SampleMovie(</strong> samplelist, filename="samplemovie.mp4", problem=None, kpar=[0,1] ) 
</th></tr></thead></table>
<p>

Constructor.

The constructor produces the movie.

<b>Parameters</b>

* samplelist  :  SampleList<br>
    to make the movie from<br>
* filename  :  str<br>
    name of the mp4 movie<br>
* problem  :  Problem<br>
    the problem that produced the samplelist<br>
* kpar  :  list of 2 ints<br>
    indices of the parameters to plot

