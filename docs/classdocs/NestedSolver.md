---
---


<a name="NestedSolver"></a>
<table><thead background-color=#FFE0E0; width=100%><tr><th text-align=left>
<strong>class NestedSolver(</strong> NestedSampler )
</th></tr></thead></table>

<b></b>

<a name="NestedSolver"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th text-align=left>
<strong>NestedSolver(</strong> problem, distribution=None, keep=None,
 ensemble=100, discard=1, seed=80409, rate=1.0, engines=None,
 maxsize=None, threads=False, verbose=1 ) 
</th></tr></thead></table>

<b></b>

<a name="solve"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th text-align=left>
<strong>solve(</strong> keep=None, plot=False )
</th></tr></thead></table>

<b></b>

<a name="__str__"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th text-align=left>
<strong>__str__(</strong> )
</th></tr></thead></table>

Return the name of this sampler. 

<a name="setErrorDistribution"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th text-align=left>
<strong>setErrorDistribution(</strong> name=None, scale=1.0, power=2.0 )
</th></tr></thead></table>

<b></b>

<a name="setEngines"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th text-align=left>
<strong>setEngines(</strong> engines=None, enginedict=None ) 
</th></tr></thead></table>

<b></b>

<a name="initWalkers"></a>
<table><thead style="background-color:#E0FFE0; width:100%"><tr><th text-align=left>
<strong>initWalkers(</strong> ensemble, allpars, fitIndex, startdict=None )
</th></tr></thead></table>

<b></b>


<thead style="background-color:#FFD0Do; width:100%"><tr><th text-align=left>
<strong>Methods inherited from NestedSampler</strong></th></tr></thead>



* [<strong>sample(</strong> keep=None, plot=False )](./NestedSampler.md#sample)
* [<strong>initSample(</strong> ensemble=None, keep=None ) ](./NestedSampler.md#initSample)
* [<strong>walkerLogL(</strong> w ) ](./NestedSampler.md#walkerLogL)
* [<strong>makeFitlist(</strong> keep=None ) ](./NestedSampler.md#makeFitlist)
* [<strong>doIterPlot(</strong> plot ) ](./NestedSampler.md#doIterPlot)
* [<strong>doLastPlot(</strong> plot ) ](./NestedSampler.md#doLastPlot)
* [<strong>initReport(</strong> keep=None ) ](./NestedSampler.md#initReport)
* [<strong>iterReport(</strong> kw, tail, plot=False ) ](./NestedSampler.md#iterReport)
* [<strong>printIterRep(</strong> kw, parfmt="%s", tail=0, max=None, indent=0, end="\n" ) ](./NestedSampler.md#printIterRep)
* [<strong>lastReport(</strong> kw, plot=False ) ](./NestedSampler.md#lastReport)
* [<strong>plotLast(</strong> ) ](./NestedSampler.md#plotLast)
* [<strong>XXXgetMaxIter(</strong> ) ](./NestedSampler.md#XXXgetMaxIter)
* [<strong>nextIteration(</strong> ) ](./NestedSampler.md#nextIteration)
* [<strong>__str__(</strong> )](./NestedSampler.md#__str__)
* [<strong>optionalRestart(</strong> )](./NestedSampler.md#optionalRestart)
* [<strong>optionalSave(</strong> )](./NestedSampler.md#optionalSave)
* [<strong>updateEvidence(</strong> worst ) ](./NestedSampler.md#updateEvidence)
* [<strong>unitDomain(</strong> ) ](./NestedSampler.md#unitDomain)
* [<strong>copyWalker(</strong> worst )](./NestedSampler.md#copyWalker)
* [<strong>copyWalkerFromPhantoms(</strong> worst )](./NestedSampler.md#copyWalkerFromPhantoms)
* [<strong>updateWalkers(</strong> explorer, worst ) ](./NestedSampler.md#updateWalkers)
* [<strong>__setattr__(</strong> name, value ) ](./NestedSampler.md#__setattr__)
* [<strong>__getattr__(</strong> name ) ](./NestedSampler.md#__getattr__)
* [<strong>setProblem(</strong> name, model=None, xdata=None, ydata=None, weights=None,](./NestedSampler.md#setProblem)
* [<strong>setErrorDistribution(</strong> name=None, limits=None, scale=1.0, power=2.0 )](./NestedSampler.md#setErrorDistribution)
* [<strong>setEngines(</strong> engines=None, enginedict=None ) ](./NestedSampler.md#setEngines)
* [<strong>setInitialEngine(</strong> ensemble, allpars, fitIndex, startdict=None )](./NestedSampler.md#setInitialEngine)
* [<strong>initWalkers(</strong> ensemble, allpars, fitIndex, startdict=None )](./NestedSampler.md#initWalkers)
* [<strong>plotResult(</strong> walker, iter, plot=0 )](./NestedSampler.md#plotResult)
* [<strong>report(</strong> )](./NestedSampler.md#report)

