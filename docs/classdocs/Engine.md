---
---
<a name="Engine"></a>
<thead style="background-color:red; width:100%"><tr><th>
<strong>class Engine(</strong> object )
</th></tr></thead>


Engine defines common properties of all Engines.

An Engine moves around a walker in a random way such that its likelood
remain above the low-likelihood-limit.

<b>Attributes</b>
    <br>
walkers : WalkerList
    list of walkers to be diffused
errdis : ErrorDistribution
    error distribution to be used
slow : int
    If slow > 0, run this engine every slow-th iteration.
phancol : PhantomCollection
    Collection of valid walker positions collected during engine execution
maxtrials : int
    maximum number of trials for various operations
rng : numpy.random.RandomState
    random number generator
verbose : int
    if verbose > 4 report about the engines. (mostly for debugging)

report : list of int (read only)
    reports number of succes, accepted, rejected, failed calls. Plus the total.
unitRange : array_like (read only)
    present max size of the parameter cloud (in unitspace: [0,1])
unitMin : array_like (read only)
    present minimum values of the parameter cloud (in unitspace: [0,1])

Author       Do Kester.

<a name="Engine"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>Engine(</strong> walkers, errdis, slow=None, phancol=None, copy=None,
 seed=4213, verbose=0 )
</th></tr></thead>


Constructor.

Only one PhantomCollection should be present for all Engines.

<b>Parameters</b>
<br>
walkers : list of Walker
    walkers to be diffused
errdis : ErrorDistribution
    error distribution to be used
slow : None or int > 0
    Run this engine every slow-th iteration. None for all.
phancol : None or PhantomCollection
    Container for all valid walkers, that have been tried. But were not kept.
    To calculate the spread of the parameters vs likelihood.
seed : int
    for random number generator
verbose : int
    report about the engines when verbose > 4
copy : Engine
    engine to be copied 
<a name="copy"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>copy(</strong> )
</th></tr></thead>

Return a copy of this engine. 

<a name="bestBoost"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>bestBoost(</strong> problem, myFitter=None ) 
</th></tr></thead>


When a logL is found better that all the rest, try to update
it using a fitter.

Parameters
problem : Problem
    the problem at hand
myFitter : None or Fitter
    None fetches LevenbergMarquardtFitter
    a (non-linear) fitter
<a name="setWalker"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>setWalker(</strong> kw, problem, allpars, logL, walker=None, fitIndex=None ) 
</th></tr></thead>


Update the walker with problem, allpars, LogL and logW.

<b>Parameters</b>
<br>
walker : Sample
    sample to be updated

kw : int
    index in walkerlist, of the walker to be replaced
problem : Problem
    the problem in the walker
allpars : array_like
    list of all parameters
logL : float
    log Likelihood
walker : Walker or None
    Copy this walker or create new one
fitIndex : array_like
    (new) fitIndex
<a name="noBoost"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>noBoost(</strong> walker ) 
</th></tr></thead>
<a name="doBoost"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>doBoost(</strong> walker ) 
</th></tr></thead>


Check if walker is best in phancol and try to optimize.

<b>Parameters</b>
<br>
walker : Walker
    new walker to be checked
<a name="domain2Unit"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>domain2Unit(</strong> problem, dval, kpar=None ) 
</th></tr></thead>


Return value in [0,1] for the selected parameter.

<b>Parameters</b>
<br>
problem : Problem
    the problem involved
dval : float
    domain value for the selected parameter
kpar : None or array_like
    selected parameter index, where kp is index in [parameters, hyperparams]
    None means all
<a name="unit2Domain"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>unit2Domain(</strong> problem, uval, kpar=None ) 
</th></tr></thead>


Return domain value for the selected parameter.

<b>Parameters</b>
<br>
problem : Problem
    the problem involved
uval : array_like
    unit value for the selected parameter
kpar : None or array_like
    selected parameter indices, where kp is index in [parameters, hyperparams]
    None means all.
<a name="startJourney"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>startJourney(</strong> unitStart ) 
</th></tr></thead>


Calculate the starting position and reset

<b>Parameters</b>
<br>
unitStart : array_like
    start position in npars-dimensions in unit space
<a name="calcJourney"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>calcJourney(</strong> unitDistance ) 
</th></tr></thead>


Calculate the distance travelled since reset

<b>Parameters</b>
<br>
unitDistance : array_like
    step size in npars-dimensions in unit space
<a name="unitTripSquare"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>unitTripSquare(</strong> unitDistance ) 
</th></tr></thead>


Return the squared unit distance 

<b>Parameters</b>
<br>
unitDistance : array_like
    step size in npars-dimensions in unit space
<a name="reportJourney"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>reportJourney(</strong> ) 
</th></tr></thead>
<a name="makeIndex"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>makeIndex(</strong> np, val ) 
</th></tr></thead>
<a name="reportCall"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>reportCall(</strong> )
</th></tr></thead>

Store a call to engine 

<a name="reportSuccess"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>reportSuccess(</strong> )
</th></tr></thead>


Add 1 to the number of succesfull steps: logL < lowLhood.
<a name="reportReject"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>reportReject(</strong> )
</th></tr></thead>


Add 1 to the number of rejected steps: logL > lowLhood.
<a name="reportFailed"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>reportFailed(</strong> )
</th></tr></thead>


Add 1 to the number of failed steps: could not construct a step.
<a name="reportBest"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>reportBest(</strong> )
</th></tr></thead>


Add 1 to the number of best likelihoods found upto now.
<a name="printReport"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>printReport(</strong> best=False ) 
</th></tr></thead>
<a name="successRate"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>successRate(</strong> ) 
</th></tr></thead>


Return percentage of success.
<a name="getUnitMinmax"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>getUnitMinmax(</strong> problem, lowLhood, nap ) 
</th></tr></thead>


Calculate unit minimum and maximum from the Phantoms

<b>Parameters</b>
<br>
problem : Problem
    To extract the unit range for
lowLhood : float
    low likelihood boundary
nap : int
    number of all parameters
<a name="getUnitRange"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>getUnitRange(</strong> problem, lowLhood, nap ) 
</th></tr></thead>


Calculate unit range and minimum from PhantomCollection

<b>Parameters</b>
<br>
problem : Problem
    To extract the unit range for
lowLhood : float
    low likelihood boundary
nap : int
    number of all parameters
<a name="__str__"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>__str__(</strong> ) 
</th></tr></thead>
<a name="execute"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>execute(</strong> kw, lowLhood )
</th></tr></thead>


Execute the engine for difusing the parameters

<b>Parameters</b>
<br>
kw : walker-id
    walker to diffuse
lowLhood : float
    low limit on the loglikelihood

<b>Returns</b>
<br>
int : number of succesfull moves

<a name="DummyPlotter"></a>
<thead style="background-color:red; width:100%"><tr><th>
<strong>class DummyPlotter(</strong> object ) 
</th></tr></thead>
<a name="Engine"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>Engine(</strong> iter=1 ) 
</th></tr></thead>
<a name="start"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>start(</strong> param=None, ulim=None )
</th></tr></thead>

start the plot. 

<a name="point"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>point(</strong> param, col=None, sym=0 )
</th></tr></thead>


Place a point at position param using color col and symbol sym.
<a name="move"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>move(</strong> param, ptry, col=None, sym=None )
</th></tr></thead>


Move parameters at position param to ptry using color col.
<a name="stop"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>stop(</strong> param=None, name=None )
</th></tr></thead>

Stop (show) the plot. 


<thead style="background-color:dodgerblue; width:100%"><tr><th>
<strong>Methods inherited from object</strong></th></tr></thead>

awk -f inherits.awk object.md
