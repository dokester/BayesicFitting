---
---
<br><br>

<a name="Model"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:20px"><tr><th style="text-align:left">
<strong>class Model(</strong> <a href="./FixedModel.html">FixedModel</a> )</th><th style="text-align:right"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source/Model.py target=_blank>Source</a></th></tr></thead></table>
<p>

Model implements the common parts of (compound) models.
It is the last common anchestor of all Models.

Models can be handled by the Fitter classes.

A model consists of one or more instantiations of (base) models which
are concatenated in a chain of models using various operations
(+-*/). A special operation is the pipe (|). It works like a unix pipe,
i.e. the output of the left-hand process in used as input of the
right-hand process.

Methods defined in BaseModel as eg. baseResult() are recursively called
here as result(). They are the ones used in the fitters.

The Model is the place where model-related items are kept, like parameters,
stdevs.

Model also implements a numerical derivation of partial to be
used when partial is not given in the model definition itself. This same
numerical derivation of partial is used in testPartial to indeed test
whether the partial has been implemented properly.

<b>Example:</b><br>
    x = numpy.arange( 10 )
    poly = PolynomialModel( 2 )             # quadratic model
    poly.parameters = [3,2,1]               # set the parameters for the model
    y = poly( x )                           # evaluate the model at x
    p0 = poly[0]                            # 3: the first parameter
   
    # To make a compound model consisting of a gaussian and a constant background
   
    gauss = GaussModel( )                   # gaussian model
    gauss += PolynomialModel( 0 )           # gaussian on a constant background
    print( gauss.getNumberOfParameters( ) )
    4
   
    # Set limits to this model
   
    lolim = [0,-10,0,-5]                    # lower limits for the parameters
    hilim = [10,10,2, 5]                    # high limits for parameters
    gauss.setLimits( lolim, hilim )         # set limits. Does not work with all Fitters
   
    # Pipe a model; The order of operation matters.
    # m5 = ( m1 | m2 ) + m3
   
    m1 = PolynomialModel( 1 )               # m1( x, p )
    m2 = SineModel()                        # m2( x, q )
    m3 = PolynomialModel( 0 )               # m3( x, r )
    m4 = m1 | m2                            # m2( m1( x, p ), q )
    m5 = m4 + m3                            # m2( m1( x, p ), q ) + m3( x, r )
    print( m5.parameters )                  # [p, q, r]
   
    # Implicit brackets
    # m5 = m1 | ( m2 + m3 )
   
    m1 = PolynomialModel( 1 )               # m1( x, p )
    m2 = SineModel()                        # m2( x, q )
    m3 = PolynomialModel( 0 )               # m3( x, r )
    m4 = m2 + m3                            # m2( x, q ) + m3( x, r )
    m5 = m1 | m4                            # m2( m1( x, p ), q ) + m3( m1( x, p ), r )
    print( m5.parameters )                  # [p, q, r]

<b>Attributes</b><br>
* parameters  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters of the model<br>
* stdevs  :  None or array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; standard deviations after a fit to the data<br>
* xUnit  :  astropy.units or list of<br>
&nbsp;&nbsp;&nbsp;&nbsp; unit of the x-values (list of in case of more dimensions)<br>
* yUnit  :  astropy.units<br>
&nbsp;&nbsp;&nbsp;&nbsp; unit of the y-values<br>
* npars  :  int (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; number of parameters in this model<br>
* npchain  :  int (read only)<br>
&nbsp;&nbsp;&nbsp;&nbsp; identical to npars<br>

<b>Attributes from FixedModel</b><br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist<br>

<b>Attributes from BaseModel</b><br>
<br>&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames<br>

Author       Do Kester


<a name="Model"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Model(</strong> nparams=0, ndim=1, copy=None, params=None, **kwargs )
</th></tr></thead></table>
<p>

Initializes the Model with all attributes set to None, except for
the parammeters which are all initialized to 0.

<b>Parameters</b><br>
* nparams  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; the number of parameters in this model<br>
* ndim  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; the dimensionality of the xdatas (default: 1)<br>
* copy  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; model to be copied (default: None)<br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; initial parameters of the model<br>
* fixed  :  None or dictionary of {int:float|Model}<br>
&nbsp;&nbsp;&nbsp;&nbsp; int         index of parameter to fix permanently.<br>
&nbsp;&nbsp;&nbsp;&nbsp; float|Model values for the fixed parameters.<br>
&nbsp;&nbsp;&nbsp;&nbsp; Attribute fixed can only be set in the constructor.<br>
&nbsp;&nbsp;&nbsp;&nbsp; See: [FixedModel](./FixedModel.md)<br>


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th></tr></thead></table>
<p>
Return a copy. 

<a name="chainLength"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>chainLength(</strong> )
</th></tr></thead></table>
<p>
Return length of the chain. 

<a name="isNullModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isNullModel(</strong> ) 
</th></tr></thead></table>
<p>

Return True if the model has no parameters (a NullModel).

<a name="isolateModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isolateModel(</strong> k )
</th></tr></thead></table>
<p>

Return a ( isolated ) copy of the k-th model in the chain.
Fixed parameters and priors which might be present in the compound model
will be lost in the isolated model.

<b>Parameters</b><br>
* k  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model number ( head = 0 )<br>

<b>Raises</b><br>
IndexError when the chain is shorter than k.


<a name="addModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>addModel(</strong> model )
</th></tr></thead></table>
<p>

Make a compound model by concatinating/adding model to this.

The final result is the sum of the individual results.

The compound model is implemented as a chain of Models.
Each of these base models contain the attributes ( parameters, limits etc. )
and when needed these attributes are taken from there, or stored there.

The operation (addition in this case) is always with the total result of the
existing chain. For the use of "brackets" in a chain use BracketModel.

<b>Parameters</b><br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; model to be added to<br>


<a name="subtractModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>subtractModel(</strong> model )
</th></tr></thead></table>
<p>

Make a compound model by concatinating/subtracting a model from this.

The final result is the difference of the models.

<b>Parameters</b><br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; model to be subtracted from<br>


<a name="multiplyModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>multiplyModel(</strong> model )
</th></tr></thead></table>
<p>

Make a compound model by concatinating/multiplying a model with this.

The final result is the product of the models.

<b>Parameters</b><br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; model to be multiplied by<br>


<a name="divideModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>divideModel(</strong> model )
</th></tr></thead></table>
<p>

Make a compound model by concatinating/dividing by a model.

The final result is the division of the models.

<b>Parameters</b><br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; model to be divided by<br>


<a name="pipeModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipeModel(</strong> model )
</th></tr></thead></table>
<p>

Make a compound model by piping the result into the next.

<b>Parameters</b><br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; model to pipe into<br>


<a name="appendModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>appendModel(</strong> model, operation )
</th></tr></thead></table>
<p>

Append a model to the present chain using a operation.

<b>Parameters</b><br>
* model  :  Model<br>
&nbsp;&nbsp;&nbsp;&nbsp; the model to be appended<br>
* operation  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; operation index<br>

<b>Raises</b><br>
ValueError when a model of a different dimensionality is offered.

<a name="correctParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>correctParameters(</strong> params )
</th></tr></thead></table>
<p>

Check parameters for non-zero and positivity

<b>Parameters</b><br>
* params  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model.<br>


<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> xdata, param=None )
</th></tr></thead></table>
<p>

Return the result of the model as applied to an array of input data.

<b>Parameters</b><br>
* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; input data<br>
* param  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model. Default parameters from the Model<br>


<a name="operate"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>operate(</strong> res, pars, next )
</th></tr></thead></table>
<p>
<a name="derivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>derivative(</strong> xdata, param, useNum=False )
</th></tr></thead></table>
<p>

Return the derivatives (df/dx) of the model at the inputs

<b>Parameters</b><br>
* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; an input vector or array<br>
* param  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model<br>
* useNum  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; if true, numeric derivatives are used.<br>


<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> xdata, param, useNum=False )
</th></tr></thead></table>
<p>

Return the partial derivatives of the model at the inputs

<b>Parameters</b><br>
* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; an input vector or array<br>
* param  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model<br>
* useNum  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; if true, numeric partials are used.<br>


<a name="selectPipe"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>selectPipe(</strong> ndim, ninter, ndout ) 
</th></tr></thead></table>
<p>

Select one of 9 pipe operations, depending on the dimensionality
of the inputs and outputs of the model G and H

Model G has pars p and model H has pars q.

<br>&nbsp; F(x:pq) ==>  H(G(x:p):q)            G(x:p) | H(*:q)   <br>
&nbsp; dF/dp   ==>  dH/dG * dG/dp          H.derivative(G,p) * G.partial(x,q)<br>
&nbsp; dF/dq   ==>  dH(G(x:p):q) / dq      G.partial(H,q)<br>

<br>&nbsp; G.ndout mustbe H.ndim<br>
&nbsp; partial <== G<br>
&nbsp; dfdx    <== H<br>

<b>Parameters</b><br>
* ndim  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; input dimensions to G and thus to F<br>
* ninter  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; output dim of G and input dim to H (must be same)<br>
* ndout  :  int<br>
    output dimensions of H and thus of F

<a name="pipe_0"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_0(</strong> dGd, dHdG ) 
</th></tr></thead></table>
<p>

ninter == 1 and ndout == 1

Return partial in the form of [N,P]

<b>Parameters</b><br>
* dGd :   array of form [N,P]<br>
&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  <br>
* dHdG :  array of form [N]<br>
    Derivative of H to G  

<a name="pipe_1"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_1(</strong> dGd, dHdG ) 
</th></tr></thead></table>
<p>

ninter > 1 and ndout > 1

Return partial in the form [O][N,P]

<b>Parameters</b><br>
* dGd :   array of form [K][N,P]<br>
&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  <br>
* dHdG :  array of form [O][N,K]<br>
    Derivative of H to G  

<a name="pipe_2"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_2(</strong> dGd, dHdG ) 
</th></tr></thead></table>
<p>

ndim == 1 and ninter > 1 and ndout == 1

Return partial in the form of [N,P]

<b>Parameters</b><br>
* dGd :   array of form [K][N,P]<br>
&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  <br>
* dHdG :  array of form [N,K]<br>
    Derivative of H to G  

<a name="pipe_3"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_3(</strong> dGd, dHdG ) 
</th></tr></thead></table>
<p>

ndim == 1 and ninter = 1 and ndout > 1

Return partial in the form of [O][NP]

<b>Parameters</b><br>
* dGd :   array of form [N,P]<br>
&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  <br>
* dHdG :  array of form [N,0]<br>
    Derivative of H to G  

<a name="pipe_4"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_4(</strong> dGdx, dHdG ) 
</th></tr></thead></table>
<p>

ndim == 0 and ninter == 1 and ndout == 1

Return partial in the form of [N]

<b>Parameters</b><br>
* dGdx :  array of form [N]<br>
&nbsp;&nbsp;&nbsp;&nbsp; Derivative dGdx  <br>
* dHdG :  array of form [N]<br>
    Derivative of H to G  

<a name="pipe_5"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_5(</strong> dGdx, dHdG ) 
</th></tr></thead></table>
<p>

ndim == 1 and ninter > 1 and ndout > 1

Return derivative in the form of [N,O]

<b>Parameters</b><br>
* dGdx :   array of form [N,K]<br>
&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  <br>
* dHdG :  array of form [O][N,K]<br>
    Derivative of H to G  

<a name="pipe_6"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_6(</strong> dGdx, dHdG ) 
</th></tr></thead></table>
<p>

ndim == 1 and ninter > 1 and ndout == 1

Return derivative in the form of [N]

<b>Parameters</b><br>
* dGdx :   array of form [N,K]<br>
&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  <br>
* dHdG :  array of form [N,K]<br>
    Derivative of H to G  

<a name="pipe_7"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_7(</strong> dGdx, dHdG ) 
</th></tr></thead></table>
<p>

ndim == 1 and ninter = 1 and ndout > 1

Return derivative in the form of [N,O]

<b>Parameters</b><br>
* dGdx :   array of form [N,O]<br>
&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  <br>
* dHdG :  array of form [N]<br>
    Derivative of H to G  

<a name="pipe_8"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_8(</strong> dGdx, dHdG ) 
</th></tr></thead></table>
<p>

ndim > 1 and ninter > 1 and ndout == 1

Return derivative in the form of [N,I]

<b>Parameters</b><br>
* dGdx :   array of form [K][N,I]<br>
&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  <br>
* dHdG :  array of form [N,K]<br>
    Derivative of H to G  

<a name="pipe_9"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_9(</strong> dGdx, dHdG ) 
</th></tr></thead></table>
<p>

ndim > 1 and ninter == 1 and ndout > 1

Return derivative in the form of [O][N,I]

<b>Parameters</b><br>
* dGdx :   array of form [N,I]<br>
&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  <br>
* dHdG :  array of form [N,O]<br>
    Derivative of H to G  

<a name="shortName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shortName(</strong> ) 
</th></tr></thead></table>
<p>

Return a short version the string representation: upto first non-letter.

<a name="getNumberOfParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getNumberOfParameters(</strong> )
</th></tr></thead></table>
<p>
Returns the number of parameters of the ( compound ) model. 

<a name="numDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>numDerivative(</strong> xdata, param )
</th></tr></thead></table>
<p>

Returns numerical derivatives (df/dx) of the model function.

<b>Parameters</b><br>
* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; input data<br>
* param  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; a parameters vector<br>


<a name="numPartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>numPartial(</strong> xdata, param )
</th></tr></thead></table>
<p>

Returns numerical partial derivatives of the model function.

<b>Parameters</b><br>
* xdata  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; input data<br>
* param  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; a parameters vector<br>


<a name="isDynamic"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isDynamic(</strong> ) 
</th></tr></thead></table>
<p>

Return whether the model can change the number of parameters dynamically.

<a name="hasPriors"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasPriors(</strong> isBound=True ) 
</th></tr></thead></table>
<p>

Return True when the model has priors for all its parameters.

<b>Parameters</b><br>
* isBound  :  bool<br>
    Also check if the prior is bound.

<a name="getPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getPrior(</strong> kpar )
</th></tr></thead></table>
<p>

Return the prior of the indicated parameter.

<b>Parameters</b><br>
* kpar  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameter number.<br>

<b>Raises</b><br>
IndexError when kpar is larger than the number of parameters.


<a name="setPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setPrior(</strong> kpar, prior=None, **kwargs )
</th></tr></thead></table>
<p>

Set the prior for the indicated parameter.

<b>Parameters</b><br>
* kpar  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameter number.<br>
* prior  :  Prior<br>
&nbsp;&nbsp;&nbsp;&nbsp; prior for parameter kpar<br>
* kwargs  :  keyword arguments<br>
&nbsp;&nbsp;&nbsp;&nbsp; attributes to be passed to the prior<br>

<b>Raises</b><br>
IndexError when kpar is larger than the number of parameters.


<a name="getParameterName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParameterName(</strong> kpar )
</th></tr></thead></table>
<p>

Return the name of the indicated parameter.

<b>Parameters</b><br>
* kpsr  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameter number.<br>

<b>Raises</b><br>
IndexError when kpar is larger than the number of parameters.


<a name="getParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParameterUnit(</strong> kpar )
</th></tr></thead></table>
<p>

Return the unit of the indicated parameter.

<b>Parameters</b><br>
* kpar  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameter number.<br>

<b>Raise</b><br>
IndexError when kpar is > number of parameters


<a name="getIntegralUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getIntegralUnit(</strong> )
</th></tr></thead></table>
<p>
Return the unit of the integral of the model over x. 

<a name="setLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setLimits(</strong> lowLimits=None, highLimits=None )
</th></tr></thead></table>
<p>

Sets the limits for the parameters of the compound model.

1. It is valid to insert for either parameter a None value
indicating no lower/upper limits.
2. When a lowerlimit >= upperlimit no limits are enforced.
It only works in *Fitter classes which support it.

<b>Parameters</b><br>
* lowLimits  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; lower limits on the parameters<br>
* highLimits  :  array_like<br>
&nbsp;&nbsp;&nbsp;&nbsp; upper limits on the parameters<br>


<a name="getLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLimits(</strong> ) 
</th></tr></thead></table>
<p>

Return the limits stored in the priors

<b>Returns</b><br>
* limits  :  tuple of 2 array-like or of 2 None (if `self.priors` is None)<br>
&nbsp;&nbsp;&nbsp;&nbsp; (lowlimits, highlimits)<br>

lolim = []
hilim = []
mdl = self
* while mdl is not None  : <br>
&nbsp;&nbsp;&nbsp;&nbsp; if not super( Model, mdl ).hasLimits( ) :<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return [None,None]<br>
&nbsp;&nbsp;&nbsp;&nbsp; lolim += [p.lowLimit for p in mdl.priors]<br>
&nbsp;&nbsp;&nbsp;&nbsp; hilim += [p.highLimit for p in mdl.priors]<br>

<br>&nbsp;&nbsp;&nbsp;&nbsp; mdl = mdl._next<br>
return (lolim, hilim)

<a name="hasLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasLimits(</strong> fitindex=None )
</th></tr></thead></table>
<p>

Return true if limits has been set for this model.

<b>Parameters</b><br>
fitindex    list of indices to be fitted.


<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> uvalue, kpar=None )
</th></tr></thead></table>
<p>

Convert a value in [0,1] to one inside the limits of the parameter.

<b>Parameters</b><br>
* uvalue  :  (list of) float<br>
&nbsp;&nbsp;&nbsp;&nbsp; value in [0,1]<br>
* kpar  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index of the parameter<br>


<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> dvalue, kpar=None )
</th></tr></thead></table>
<p>

Convert a value within the domain of the parameter to one in [0,1].

<b>Parameters</b><br>
* dvalue  :  (list of) float<br>
&nbsp;&nbsp;&nbsp;&nbsp; value of parameter<br>
* kpar  :  int<br>
&nbsp;&nbsp;&nbsp;&nbsp; index of the parameter<br>


<a name="partialDomain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialDomain2Unit(</strong> dvalue )
</th></tr></thead></table>
<p>

Return a the derivate of the domain2Unit function to dval.

<b>Parameters</b><br>
* dvalue  :  (list of) float<br>
&nbsp;&nbsp;&nbsp; parameter array<br>


<a name="nextPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>nextPrior(</strong> ) 
</th></tr></thead></table>
<p>
<a name="isMixed"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isMixed(</strong> )
</th></tr></thead></table>
<p>
Return false. 

<a name="getLinearIndex"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLinearIndex(</strong> )
</th></tr></thead></table>
<p>
Return null. 

<a name="testPartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>testPartial(</strong> xdata, params, silent=True )
</th></tr></thead></table>
<p>

A test routine to check the calculation of the partial derivatives.

It is compared to a numerical calculation.

<b>Parameters</b><br>
* xdata  :  (list of) float<br>
&nbsp;&nbsp;&nbsp;&nbsp; values of the independent variable<br>
* params  :  list of floats<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model<br>
* silent  :  bool<br>
&nbsp;&nbsp;&nbsp;&nbsp; if false print outputs<br>

<b>Return</b><br>
The number of large deviations.


<a name="strictNumericPartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>strictNumericPartial(</strong> xdata, params, parlist=None ) 
</th></tr></thead></table>
<p>

Strictly numeric calculation of partials to params.

For compound models it is different from numPartial and numDerivative.

<b>Parameters</b><br>
* xdata  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; single xdata point (possibly multidimensional)<br>
* params  :  array-like<br>
&nbsp;&nbsp;&nbsp;&nbsp; parameters<br>
* kpar  :  None or int or list of int<br>
    int  : return derivative to parameter kpar.

<a name="assignDF1"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>assignDF1(</strong> partial, i, dpi ) 
</th></tr></thead></table>
<p>
<a name="assignDF2"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>assignDF2(</strong> partial, i, dpi ) 
</th></tr></thead></table>
<p>
<a name="strictNumericDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>strictNumericDerivative(</strong> xdata, param ) 
</th></tr></thead></table>
<p>

Strictly numeric calculation of derivative.

For compound models it is different from numPartial and numDerivative.

<br>&nbsp;&nbsp;&nbsp;&nbsp; ## More dimensions in x<br>

<b>Parameters</b><br>
* xdata  :  float<br>
&nbsp;&nbsp;&nbsp;&nbsp; single xdata point (possibly multidimensional)<br>
* param  :  array-like<br>
    parameters

<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./FixedModel.html">FixedModel</a></th></tr></thead></table>


* [<strong>select(</strong> params ) ](./FixedModel.md#select)
* [<strong>selectNames(</strong> names ) ](./FixedModel.md#selectNames)
* [<strong>expand(</strong> xdata, param ) ](./FixedModel.md#expand)
* [<strong>basePartial(</strong> xdata, param, parlist=None ) ](./FixedModel.md#basePartial)


<table><thead style="background-color:#FFD0D0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Methods inherited from</strong> <a href="./BaseModel.html">BaseModel</a></th></tr></thead></table>


* [<strong>checkParameter(</strong> param ) ](./BaseModel.md#checkParameter)
* [<strong>checkPositive(</strong> param ) ](./BaseModel.md#checkPositive)
* [<strong>checkZeroParameter(</strong> param )](./BaseModel.md#checkZeroParameter)
* [<strong>isModifiable(</strong> ) ](./BaseModel.md#isModifiable)
* [<strong>basePrior(</strong> kpar ) ](./BaseModel.md#basePrior)
* [<strong>baseParameterName(</strong> kpar ) ](./BaseModel.md#baseParameterName)
* [<strong>baseParameterUnit(</strong> kpar ) ](./BaseModel.md#baseParameterUnit)
