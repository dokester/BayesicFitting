---
---
<a name="NestedSolver"></a>
<thead style="background-color:red; width:100%"><tr><th>
<strong>class NestedSolver(</strong> NestedSampler )
</th></tr></thead>


NestedSolver is an extension of NestedSampler. It uses the
likelihood-climbing technique to find a solution in an ordering
problem. The negative value of the costfunction, commonly defined
in ordering problems, is maximised. In this sense the costfunction
is acting as the logLikelihood.

For more information about this technique see NestedSampler.

For the random walk of the parameters 4 so-called engines are written.
By default only he first is switched on.

MoveEngine    : insert a snippet of parameters at another location
ReverseEngine : reverse the order of a snippet of parameters
ShuffleEngine : shuffle part of the parameter list
SwitchEngine  : switch two elements
LoopEngine    : uncross a crossing loop
NearEngine    : find the nearest location and go there first. 

The last 2 engines are not random. They are mostly (?) taking steps 
uphill. Mixing them with other engines maintain detailed balance in 
an overall sense. 


<b>Attributes</b>
    <br>
xdata : array_like
    array of independent input values
model : Model
    the model function to be fitted
ydata : array_like
    array of dependent (to be fitted) data
weights : array_like (None)
    weights pertaining to ydata
distribution : ErrorDistribution
    to calculate the loglikelihood
ensemble : int (100)
    number of walkers
discard : int (1)
    number of walkers to be replaced each generation
rng : RandomState
    random number generator
seed : int (80409)
    seed of rng
rate : float (1.0)
    speed of exploration
maxsize : None or int
    maximum size of the resulting sample list (None : no limit)
end : float (2.0)
    stopping criterion
verbose : int
    level of blabbering

walkers : SampleList
    ensemble of Samples that explore the likelihood space
samples : SampleList
    Samples resulting from the exploration
engines : list of Engine
    Engine that move the walkers around within the given constraint: logL > lowLogL
initialEngine : Engine
    Engine that distributes the walkers over the available space
restart : StopStart (TBW)
    write intermediate results to (optionally) start from.


Author       Do Kester.


<a name="NestedSolver"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>NestedSolver(</strong> problem, distribution=None, keep=None,
 ensemble=100, discard=1, seed=80409, rate=1.0, engines=None,
 maxsize=None, threads=False, verbose=1 ) 
</th></tr></thead>


Create a new class, providing inputs and model.

<b>Parameters</b>
<br>
problem : OrderProblem
    Problem with integer parameters
keep : None or dict of {int:float}
    None : none of the model parameters are kept fixed.
    Dictionary of indices (int) to be kept at a fixed value (float).
    Hyperparameters follow model parameters.
    The values will override those at initialization.
    They are used in this instantiation, unless overwritten at the call to sample()
distribution : None or String or ErrorDistribution
    None   : DistanceCostFunction is chosen.

    "distance" : `DistanceCostFunction`      no hyperpar

    errdis : A class inheriting from ErrorDistribution
             which implements logLikelihood

    When the hyperpar(s) are not to be kept fixed, they need `Prior` and maybe limits.
ensemble : int (100)
    number of walkers
discard : int (1)
    number of walkers to be replaced each generation
seed : int (80409)
    seed of rng
rate : float (1.0)
    speed of exploration
engines : None or (list of) string or (list of) Engine
    to randomly move the walkers around, within the likelihood bound.

    "move"    : insert a snippet of parameters at another location
    "reverse" : reverse the order of a snippet of parameters
    "shuffle" : shuffle part of the parameter list
    "switch"  : switch two elements
    "loop"    : find two paths that cross, then uncross them
    "near"    : find the nearest location and go there first. 

    None    : take default [all of above].

    engine  : a class inheriting from Engine. At least implementing
              execute( walker, lowLhood )
maxsize : None or int
    maximum size of the resulting sample list (None : no limit)
threads : bool (False)
    Use Threads to distribute the diffusion of discarded samples over the available cores.
verbose : int (1)
    0 : silent
    1 : basic information
    2 : more about every 100th iteration
    3 : more about every iteration

<a name="solve"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>solve(</strong> keep=None, plot=False )
</th></tr></thead>


Solve an order problem.

Return the last sample, representing the best solution.

The more sammples (with solutions) can be found in the sample list.

<b>Parameters</b>
<br>
keep : None or dict of {int:float}
    Dictionary of indices (int) to be kept at a fixed value (float)
    Hyperparameters follow model parameters
    The values will override those at initialization.
    They are only used in this call of fit.
plot : bool
    Show a plot of the results

<a name="__str__"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>__str__(</strong> )
</th></tr></thead>

Return the name of this sampler. 

<a name="setErrorDistribution"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>setErrorDistribution(</strong> name=None, scale=1.0, power=2.0 )
</th></tr></thead>


Set the error distribution for calculating the likelihood.

<b>Parameters</b>
<br>
name : string
    name of distribution
scale : float
    fixed scale of distribution
power : float
    fixed power of distribution

<a name="setEngines"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>setEngines(</strong> engines=None, enginedict=None ) 
</th></tr></thead>


initialize the engines.

<b>Parameters</b>
<br>
engines : list of string
    list of engine names
enginedict : dictionary of { str : Engine }
    connecting names to Engines

<a name="initWalkers"></a>
<thead style="background-color:green; width:100%"><tr><th>
<strong>initWalkers(</strong> ensemble, allpars, fitIndex, startdict=None )
</th></tr></thead>


Initialize the walkers at random values of parameters and scale

<b>Parameters</b>
<br>
ensemble : int
    length od the walkers list
allpars : array_like
    array of parameters
fitIndex : array_like
    indices of allpars to be fitted
startdict : dictionary of { str : Engine }
    connecting a name to a StartEngine

