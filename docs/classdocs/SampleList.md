---
---
<br><br>

<a name="SampleList"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class SampleList(</strong> <a href="./list.html">list</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/SampleList.py target=_blank>Source</a></th></tr></thead></table>

SampleList is a list of Samples, see [Sample](./Sample.md)

SampleList is the main result of the NestedSampler. It contains all
information to calculate averages, medians, modi or maximum likihood solutions
of the parameters, or of any function of the parameters; in particular of the
Model.

To make averages one has to take into account the weights. Each Sample has a weight
and all weights sum to 1.0. So the average of any function, f, of the parameters p is

&nbsp;&nbsp;&nbsp;&nbsp; E( f(p) ) = &sum; w<sub>k</sub> f( p<sub>k</sub> )

where the sum is over all samples k.

A large set of utility functions is provided to extract the information from the
SampleList.


<b>Attributes</b>

* parameters  :  numpy.array (read-only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The average over the parameters. Not for dynamic models.
* stdevs, standardDeviations  :  numpy.array (read-only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The standard deviations for the parameters. Not for dynamic models
* scale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; The average of the noise scale
* stdevScale  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; the standard deviation of the scale.

* logZ  :  float (read-only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; Natural log of evidence
* evidence  :  float (read-only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; log10( Z ). Evidence * 10 is interpretable as dB.
* info  :  float (read-only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The information H. The compression factor ( the ratio of the prior space
<br>&nbsp;&nbsp;&nbsp;&nbsp; available to the model parameters over the posterior space ) is equal to the exp( H ).

* maxLikelihoodIndex  :  int (read-only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The index at which the max likelihood can be found: always the last in the list
* maxLikelihoodParameters  :  numpy.array (read-only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The maximum likelihood parameters at the maxLikelihoodIndex.
* maxLikelihoodScale  :  float (read-only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The maximum likelihood noise scale at the maxLikelihoodIndex.
* medianIndex  :  int (read-only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The index at which the median can be found: the middle of the cumulative weights.
<br>&nbsp;&nbsp;&nbsp;&nbsp; It is calculated once and then kept.
* medianParameters  :  numpy.array (read-only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The median of the parameters at the medianIndex
* medianScale  :  float (read-only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The median of the noise scale at the medianIndex
* modusIndex  :  int (read-only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The index at which the modus can be found: the largest weight
<br>&nbsp;&nbsp;&nbsp;&nbsp; It is calculated once and then kept.
* modusParameters  :  numpy.array (read-only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The modus of the parameters at the modusIndex
* modusScale  :  float (read-only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; The modus of the noise scale at the modusIndex.

* normalized  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; True when the weights are normalized to SUM( weights ) = 1


Author       Do Kester


<a name="SampleList"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>SampleList(</strong> model, nsamples, parameters=None, fitIndex=None, ndata=1 )
</th></tr></thead></table>

Constructor.

<b>Parameters</b>

* nsamples  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of samples created.
* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; to be used in the samples
* parameters  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; list of model parameters
* fitIndex  :  array of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; indicating which parameters need fitting
* ndata  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; length of the data vector; to be used in stdev calculations


<a name="sample"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>sample(</strong> k, sample=None ) 
</th></tr></thead></table>
Set or return the k-th sample from the list.

<b>Parameters</b>

* k  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; the index of the sample
* sample  :  Sample
<br>&nbsp;&nbsp;&nbsp;&nbsp; if present, set the kth sample with sample

<a name="normalize"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>normalize(</strong> )
</th></tr></thead></table>
Normalize the samplelist.
make Sum( weight ) = 1


<a name="add"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>add(</strong> sample )
</th></tr></thead></table>
Add a Sample to the list

<b>Parameters</b>

* sample  :  Sample
<br>&nbsp;&nbsp;&nbsp;&nbsp; the sample to be added


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> src, des )
</th></tr></thead></table>
Copy one item of the list onto another.

<b>Parameters</b>

* src  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; the source item
* des  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; the destination item


<a name="weed"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>weed(</strong> maxsize=None )
</th></tr></thead></table>
Weed superfluous samples.

If MaxSamples has been set, it is checked whether the size of the
SampleList exceeds the maximum. If so the Sample with the smallest
log( Weight ) is removed.
weed( ) is called recursively until the size has the required length.


<a name="logPlus"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>logPlus(</strong> x, y )
</th></tr></thead></table>
Return  log( exp(x) + exp(y) )

<a name="getParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParameters(</strong> )
</th></tr></thead></table>
Calculate the average of the parameters and the standard deviations.

<b>Return</b>

&nbsp;&nbsp;&nbsp;&nbsp; The average values of the parameters.
<b>Raises</b>

&nbsp;&nbsp;&nbsp;&nbsp; ValueError when using Dynamic Models


<a name="getHypars"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getHypars(</strong> ) 
</th></tr></thead></table>
Return the hyper parameters

nhp = len( self[0].hyper )

hypar = numpy.zeros( nhp, dtype=float )
hydev = numpy.zeros( nhp, dtype=float )
sw = 0.0
for sample in self 
<br>&nbsp;&nbsp;&nbsp;&nbsp; wt = math.exp( sample.logW )
<br>&nbsp;&nbsp;&nbsp;&nbsp; sw += wt
<br>&nbsp;&nbsp;&nbsp;&nbsp; ws = wt * sample.hyper
<br>&nbsp;&nbsp;&nbsp;&nbsp; hypar = hypar + ws
<br>&nbsp;&nbsp;&nbsp;&nbsp; hydev = hydev + ws * sample.hyper
self.stdevHypars = numpy.sqrt( hydev - hypar * hypar )
self.hypars = hypar
return self.hypars

<a name="getNuisance"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getNuisance(</strong> ) 
</th></tr></thead></table>
Return the average of the nuisance parameters (if present)

<a name="averstd"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>averstd(</strong> name ) 
</th></tr></thead></table>
Return the average and the stddevs of the named attribute from Sample

<b>Parameters</b>

* name  :  str
<br>&nbsp;&nbsp;&nbsp;&nbsp; name of an attribute from Sample

<a name="getMedianIndex"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getMedianIndex(</strong> ) 
</th></tr></thead></table>
Return the index at which the median can be found.

<a name="getMaximumNumberOfParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getMaximumNumberOfParameters(</strong> )
</th></tr></thead></table>
Return the maximum number of parameters (for Dynamic Models)

<a name="getParameterEvolution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParameterEvolution(</strong> kpar=None )
</th></tr></thead></table>
Return the evolution of one or all parameters.

In case of dynamic models the number of parameters may vary.
They are zero-padded. Use `getNumberOfParametersEvolution`
to get the actual number.

<b>Parameters</b>

* kpar  :  int or tuple of ints
<br>&nbsp;&nbsp;&nbsp;&nbsp; the parameter to be selected. Default: all


<a name="getParAndWgtEvolution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParAndWgtEvolution(</strong> )
</th></tr></thead></table>
Return the evolution of parameters and weights.

In case of dynamic models the number of parameters may vary.
They are zero-padded. Use `getNumberOfParametersEvolution`
to get the actual number.


<a name="getNumberOfParametersEvolution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getNumberOfParametersEvolution(</strong> )
</th></tr></thead></table>

Return the evolution of the number of parameters. 
<a name="getScaleEvolution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getScaleEvolution(</strong> )
</th></tr></thead></table>

Return the evolution of the scale. 
<a name="getLogLikelihoodEvolution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLogLikelihoodEvolution(</strong> )
</th></tr></thead></table>

Return the evolution of the log( Likelihood ). 
<a name="getLogWeightEvolution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLogWeightEvolution(</strong> )
</th></tr></thead></table>
Return the evolution of the log( weight ).

The weights itself sum up to 1.
See #getWeightEvolution( ).


<a name="getWeightEvolution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getWeightEvolution(</strong> )
</th></tr></thead></table>
Return the evolution of the weight.

The weights sum to 1.


<a name="getParentEvolution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParentEvolution(</strong> )
</th></tr></thead></table>

Return the evolution of the parentage. 
<a name="getStartEvolution"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getStartEvolution(</strong> )
</th></tr></thead></table>

Return the evolution of the start generation. 
<a name="getGeneration"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getGeneration(</strong> )
</th></tr></thead></table>

Return the generation number pertaining to the evolution. 
<a name="getLowLogL"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLowLogL(</strong> )
</th></tr></thead></table>
Return the lowest value of logL in the samplelist, plus its index.

<a name="average"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>average(</strong> xdata )
</th></tr></thead></table>
Return the (weighted) average result of the model(s) over the samples.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; the input


<a name="monteCarloError"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>monteCarloError(</strong> xdata )
</th></tr></thead></table>
Calculates 1-sigma-confidence regions on the model given some inputs.

The model is run with the input for the parameters in each of the
samples. Appropiately weighted standard deviations are calculated
and returned at each input value.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp; the input vectors.

<b>Returns</b>

* error  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; standard deviations at each input point


