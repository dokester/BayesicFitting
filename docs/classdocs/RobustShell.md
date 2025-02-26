---
---
<br><br><br>

<a name="RobustShell"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class RobustShell(</strong> <a href="./IterativeFitter.html">IterativeFitter</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/RobustShell.py target=_blank>Source</a></th></tr></thead></table>
<p>

RobustShell tries to make a fit more robust in the presence of outliers.

It is a shell around another fitter. Technically it is in itself a
a Fitter, but with limited possiblities.

A RobustShell tries to make a fit more robust in the presence of outliers.
It does it by manipulating the weights: outliers are
downweighted. "Normal" points keep their weights, more or less.

Apart from methods specific to the robustification, RobustShell has a fit method
and little else from the Fitter family. Methods to get chi^2,
the covariance matrix, the evidence, the noise scale etc. should be taken from
the embedded fitter.

The theory behind robust fitting can be found in Wikipedia: Robust Statistics,
and the references therein.

To determine which points are "normal" and which are "outliers" we
need a previous fit. The difference to this earlier fit determines
the normalcy. Its amount is used to adjust the weights.

The fact that we need a previous iteration makes robust estimation a
iterative procedure.
Typically the procedure should stabilize in half a dozen steps maximally.

There are several schemes to adjust the weights. But before we go into that
we need two values in each scheme.
Firstly the amount of noise present in the data. By default the noise
is taken from the previous fit via Fitter.scale.
The second value needed is the size of the influence domain in terms
of the noise scale.

For all schemes the deviant is calculated as the difference
between data and fit divided by noisescale and domainsize

d = ( data - fit ) / ( noisescale * domainsize )

The domainsize is defined such that deviants upto 3 times the noisescale fall
within the fwhm.

A number of weighting schemes are provided.

With bound support and smooth edges
   Kernel       Name        domain      comment<br>
   Biweight     Tukey         5.54      Default kernel<br>
   CosSquare                  6.00<br>
   Tricube                    5.08<br>
   Triweight                  6.60<br>

With bound support and hard edges
   Uniform      Clip          3.00      Ignore all outside 3 sigma<br>
   Cosine                     4.50<br>
   Triangle                   6.00<br>
   Parabola                   4.50<br>

with unbound support
   Huber        Median        1.50      Inside domain mean; outside domain median<br>
   Gauss                      2.12<br>
   Lorentz                    3.00<br>

Other schemes can be written by making another Kernel or writing a function
    wgts = func( d )<br>
where d is the deviant as above.


<b>Notes</b>

Robust fitting is even more dangerous than ordinary fitting.
*Never trust what you get without thorough checking.*

<b>Example</b>

    model = PolynomialModel( 1 )                # some model
    x = numpy.arange( 100, dtype=float ) / 100  # some x values
    y = numpy.arange( 100, dtype=float ) / 4    # digitization noise
    y[1,11,35,67] += 10                         # create outliers
    ftr = Fitter( x, model )                    # a fitter, a model and a x
    rob = RobustShell( ftr, domain=7 )          # robust fitter using someFtr
    par = rob.fit( y )                          # solution
    print( rob )                                #
    print( rob.weights )                        # print final weights
    print( ftr.chisq )                          # get from someFtr

Author       Do Kester.


<a name="RobustShell"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>RobustShell(</strong> fitter, kernel=Biweight, domain=None, onesided=None, **kwargs )
</th></tr></thead></table>
<p>

Create a new class, providing the fitter to be used.

<b>Parameters</b>

* fitter  :  BaseFitter<br>
     to be used<br>
* kernel  :  Kernel or callable<br>
    All Kernels have a method `result( d )` which is applied to the deviants.<br>
    where d = ( data - model ) / ( domain * scale )<br>
    If kernel is a callable method it is assumed to be a similar result mathod.<br>
* domain  :  None or float<br>
    Width of the kernel.<br>
    None : automatic calculation of domain according to table in class doc.<br>
    float : overrides autocalculation.<br>
* onesided  :  None or "positive" or "p" or "negative" or "n"<br>
    None : apply robust weights to positive and negative residuals<br>
    "positive" : apply robust weights to positive residuals only<br>
    "negative" : apply robust weights to negative residuals only<br>


<a name="setKernel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setKernel(</strong> kernel ) 
</th></tr></thead></table>
<p>

Set the robust kernel to be used.

<b>Parameters</b>

* kernel  :  Kernel or callable<br>
    All Kernels have a method `result( d )` which is applied to the deviants.<br>
    where d = ( data - model ) / ( domain * scale )<br>
    If kernel is a callable method it is assumed to be a similar result mathod.<br>

<b>Raises</b>

ValueError when kernel is not recognized.


<a name="setOneSided"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setOneSided(</strong> onesided ) 
</th></tr></thead></table>
<p>

set self.onesided to either 0 or +1 or -1.

<b>Parameters</b>

* onesided  :  None or "positive" or "negative"<br>
    None : apply robust weights to positive and negative residuals<br>
    "positive" : apply robust weights to positive residuals only<br>
    "negative" : apply robust weights to negative residuals only<br>

<b>Raises</b>

ValueError when onesided could not be interpreted.


<a name="fit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>fit(</strong> data, weights=None, kernel=None, domain=None, onesided=None, **kwargs ) 
</th></tr></thead></table>
<p>

Perform a robustification step.

<b>Parameters</b>

* data  :  array_like<br>
    the data as they go into a fitter<br>
* kwargs  :  dict<br>
    keyword args to be passed to fitter.fit()

<a name="getOneSidedWeights"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getOneSidedWeights(</strong> wgt, res, onesided ) 
</th></tr></thead></table>
<p>
<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./IterativeFitter.html">IterativeFitter</a></th></tr></thead></table>


* [<strong>setParameters(</strong> params )](./IterativeFitter.md#setParameters)
* [<strong>doPlot(</strong> param, force=False )](./IterativeFitter.md#doPlot)
* [<strong>fitprolog(</strong> ydata, weights=None, accuracy=None, keep=None ) ](./IterativeFitter.md#fitprolog)
* [<strong>report(</strong> verbose, param, chi, more=None, force=False ) ](./IterativeFitter.md#report)


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./BaseFitter.html">BaseFitter</a></th></tr></thead></table>


* [<strong>setMinimumScale(</strong> scale=0 ) ](./BaseFitter.md#setMinimumScale)
* [<strong>fitpostscript(</strong> ydata, plot=False ) ](./BaseFitter.md#fitpostscript)
* [<strong>keepFixed(</strong> keep=None ) ](./BaseFitter.md#keepFixed)
* [<strong>insertParameters(</strong> fitpar, index=None, into=None ) ](./BaseFitter.md#insertParameters)
* [<strong>modelFit(</strong> ydata, weights=None, keep=None )](./BaseFitter.md#modelFit)
* [<strong>limitsFit(</strong> ydata, weights=None, keep=None ) ](./BaseFitter.md#limitsFit)
* [<strong>checkNan(</strong> ydata, weights=None, accuracy=None )](./BaseFitter.md#checkNan)
* [<strong>getVector(</strong> ydata, index=None )](./BaseFitter.md#getVector)
* [<strong>getHessian(</strong> params=None, weights=None, index=None )](./BaseFitter.md#getHessian)
* [<strong>getInverseHessian(</strong> params=None, weights=None, index=None )](./BaseFitter.md#getInverseHessian)
* [<strong>getCovarianceMatrix(</strong> )](./BaseFitter.md#getCovarianceMatrix)
* [<strong>makeVariance(</strong> scale=None )](./BaseFitter.md#makeVariance)
* [<strong>normalize(</strong> normdfdp, normdata, weight=1.0 ) ](./BaseFitter.md#normalize)
* [<strong>getDesign(</strong> params=None, xdata=None, index=None )](./BaseFitter.md#getDesign)
* [<strong>chiSquared(</strong> ydata, params=None, weights=None )](./BaseFitter.md#chiSquared)
* [<strong>getStandardDeviations(</strong> )](./BaseFitter.md#getStandardDeviations)
* [<strong>monteCarloError(</strong> xdata=None, monteCarlo=None)](./BaseFitter.md#monteCarloError)
* [<strong>getScale(</strong> )](./BaseFitter.md#getScale)
* [<strong>getEvidence(</strong> limits=None, noiseLimits=None )](./BaseFitter.md#getEvidence)
* [<strong>getLogLikelihood(</strong> autoscale=False, var=1.0 ) ](./BaseFitter.md#getLogLikelihood)
* [<strong>getLogZ(</strong> limits=None, noiseLimits=None )](./BaseFitter.md#getLogZ)
* [<strong>plotResult(</strong> xdata=None, ydata=None, model=None, residuals=True,](./BaseFitter.md#plotResult)
