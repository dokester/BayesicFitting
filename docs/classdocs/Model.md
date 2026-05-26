---
---
<br><br>

<a name="Model"></a>
<table><thead style="background-color:#FFE0E0; width:100%"><tr><th style="text-align:left; font-size:20px">
<strong>class Model(</strong> <a href="./FixedModel.html">FixedModel</a> )</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source// target=_blank>[source]</a></th></tr></thead></table>
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

<b>Example:</b>

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

<b>Attributes</b>

* parameters  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters of the model
* stdevs  :  None or array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; standard deviations after a fit to the data
* xUnit  :  astropy.units or list of
<br>&nbsp;&nbsp;&nbsp;&nbsp; unit of the x-values (list of in case of more dimensions)
* yUnit  :  astropy.units
<br>&nbsp;&nbsp;&nbsp;&nbsp; unit of the y-values
* npars  :  int (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; number of parameters in this model
* npchain  :  int (read only)
<br>&nbsp;&nbsp;&nbsp;&nbsp; identical to npars

<b>Attributes from FixedModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npmax, fixed, parlist, mlist

<b>Attributes from BaseModel</b>

&nbsp;&nbsp;&nbsp;&nbsp; npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames

Author       Do Kester


<a name="Model"></a>
<table><thead style="background-color:#FFE0E0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>Model(</strong> nparams=0, ndim=1, copy=None, params=None, **kwargs )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L141-L200 target=_blank>[source]</a></th></tr></thead></table>

Initializes the Model with all attributes set to None, except for
the parammeters which are all initialized to 0.

<b>Parameters</b>

* nparams  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; the number of parameters in this model
* ndim  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; the dimensionality of the xdatas (default: 1)
* copy  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to be copied (default: None)
* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; initial parameters of the model
* fixed  :  None or dictionary of {int:float|Model}
<br>&nbsp;&nbsp;&nbsp;&nbsp; int         index of parameter to fix permanently.
<br>&nbsp;&nbsp;&nbsp;&nbsp; float|Model values for the fixed parameters.
<br>&nbsp;&nbsp;&nbsp;&nbsp; Attribute fixed can only be set in the constructor.
<br>&nbsp;&nbsp;&nbsp;&nbsp; See: [FixedModel](./FixedModel.md)


<a name="copy"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>copy(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L202-L256 target=_blank>[source]</a></th></tr></thead></table>
Return a copy.  

<a name="chainLength"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>chainLength(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L258-L267 target=_blank>[source]</a></th></tr></thead></table>
Return length of the chain.  

<a name="isNullModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isNullModel(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L269-L273 target=_blank>[source]</a></th></tr></thead></table>
Return True if the model has no parameters (a NullModel).

<a name="isolateModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isolateModel(</strong> k )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L275-L321 target=_blank>[source]</a></th></tr></thead></table>
Return a ( isolated ) copy of the k-th model in the chain.
Fixed parameters and priors which might be present in the compound model
will be lost in the isolated model.

<b>Parameters</b>

* k  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model number ( head = 0 )

<b>Raises</b>

IndexError when the chain is shorter than k.


<a name="addModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>addModel(</strong> model )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L323-L342 target=_blank>[source]</a></th></tr></thead></table>
Make a compound model by concatinating/adding model to this.

The final result is the sum of the individual results.

The compound model is implemented as a chain of Models.
Each of these base models contain the attributes ( parameters, limits etc. )
and when needed these attributes are taken from there, or stored there.

The operation (addition in this case) is always with the total result of the
existing chain. For the use of "brackets" in a chain use BracketModel.

<b>Parameters</b>

* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to be added to


<a name="subtractModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>subtractModel(</strong> model )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L344-L356 target=_blank>[source]</a></th></tr></thead></table>
Make a compound model by concatinating/subtracting a model from this.

The final result is the difference of the models.

<b>Parameters</b>

* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to be subtracted from


<a name="multiplyModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>multiplyModel(</strong> model )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L358-L370 target=_blank>[source]</a></th></tr></thead></table>
Make a compound model by concatinating/multiplying a model with this.

The final result is the product of the models.

<b>Parameters</b>

* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to be multiplied by


<a name="divideModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>divideModel(</strong> model )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L372-L384 target=_blank>[source]</a></th></tr></thead></table>
Make a compound model by concatinating/dividing by a model.

The final result is the division of the models.

<b>Parameters</b>

* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to be divided by


<a name="pipeModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipeModel(</strong> model )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L386-L396 target=_blank>[source]</a></th></tr></thead></table>
Make a compound model by piping the result into the next.

<b>Parameters</b>

* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; model to pipe into


<a name="appendModel"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>appendModel(</strong> model, operation )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L398-L452 target=_blank>[source]</a></th></tr></thead></table>
Append a model to the present chain using a operation.

<b>Parameters</b>

* model  :  Model
<br>&nbsp;&nbsp;&nbsp;&nbsp; the model to be appended
* operation  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; operation index

<b>Raises</b>

ValueError when a model of a different dimensionality is offered.

<a name="correctParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>correctParameters(</strong> params )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L454-L479 target=_blank>[source]</a></th></tr></thead></table>
Check parameters for non-zero and positivity

<b>Parameters</b>

* params  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model.


<a name="result"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>result(</strong> xdata, param=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L481-L514 target=_blank>[source]</a></th></tr></thead></table>
Return the result of the model as applied to an array of input data.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; input data
* param  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model. Default parameters from the Model


<a name="operate"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>operate(</strong> res, pars, next )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L516-L543 target=_blank>[source]</a></th></tr></thead></table>
Apply the operation present in self.

<b>Parameters</b>

* res  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; result of the chain upto now
* pars  :  array
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters for the next result (in case of pipe)
* next  : 
<br>&nbsp;&nbsp;&nbsp;&nbsp; result of next model in chain.

<a name="derivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>derivative(</strong> xdata, param, useNum=False )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L545-L615 target=_blank>[source]</a></th></tr></thead></table>
Return the derivatives (df/dx) of the model at the inputs

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; an input vector or array
* param  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model
* useNum  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; if true, numeric derivatives are used.


<a name="partial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partial(</strong> xdata, param, useNum=False )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L617-L696 target=_blank>[source]</a></th></tr></thead></table>
Return the partial derivatives of the model at the inputs

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; an input vector or array
* param  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model
* useNum  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; if true, numeric partials are used.


<a name="selectPipe"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>selectPipe(</strong> ndim, ninter, ndout ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L698-L771 target=_blank>[source]</a></th></tr></thead></table>
Select one of 9 pipe operations, depending on the dimensionality
of the inputs and outputs of the model G and H

Model G has pars p and model H has pars q.

&nbsp; F(x:pq) ==>  H(G(x:p):q)            G(x:p) | H(*:q)   
<br>&nbsp; dF/dp   ==>  dH/dG * dG/dp          H.derivative(G,p) * G.partial(x,q)
<br>&nbsp; dF/dq   ==>  dH(G(x:p):q) / dq      G.partial(H,q)

&nbsp; G.ndout mustbe H.ndim
<br>&nbsp; partial <== G
<br>&nbsp; dfdx    <== H

<b>Parameters</b>

* ndim  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; input dimensions to G and thus to F
* ninter  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; output dim of G and input dim to H (must be same)
* ndout  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; output dimensions of H and thus of F

<a name="pipe_0"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_0(</strong> dGd, dHdG ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L773-L786 target=_blank>[source]</a></th></tr></thead></table>
ninter == 1 and ndout == 1

Return partial in the form of [N,P]

<b>Parameters</b>

* dGd :   array of form [N,P]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  
* dHdG :  array of form [N]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Derivative of H to G  

<a name="pipe_1"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_1(</strong> dGd, dHdG ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L788-L808 target=_blank>[source]</a></th></tr></thead></table>
ninter > 1 and ndout > 1

Return partial in the form [O][N,P]

<b>Parameters</b>

* dGd :   array of form [K][N,P]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  
* dHdG :  array of form [O][N,K]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Derivative of H to G  

<a name="pipe_2"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_2(</strong> dGd, dHdG ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L810-L829 target=_blank>[source]</a></th></tr></thead></table>
ndim == 1 and ninter > 1 and ndout == 1

Return partial in the form of [N,P]

<b>Parameters</b>

* dGd :   array of form [K][N,P]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  
* dHdG :  array of form [N,K]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Derivative of H to G  

<a name="pipe_3"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_3(</strong> dGd, dHdG ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L831-L848 target=_blank>[source]</a></th></tr></thead></table>
ndim == 1 and ninter = 1 and ndout > 1

Return partial in the form of [O][NP]

<b>Parameters</b>

* dGd :   array of form [N,P]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  
* dHdG :  array of form [N,0]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Derivative of H to G  

<a name="pipe_4"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_4(</strong> dGdx, dHdG ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L850-L863 target=_blank>[source]</a></th></tr></thead></table>
ndim == 0 and ninter == 1 and ndout == 1

Return partial in the form of [N]

<b>Parameters</b>

* dGdx :  array of form [N]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Derivative dGdx  
* dHdG :  array of form [N]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Derivative of H to G  

<a name="pipe_5"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_5(</strong> dGdx, dHdG ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L865-L884 target=_blank>[source]</a></th></tr></thead></table>
ndim == 1 and ninter > 1 and ndout > 1

Return derivative in the form of [N,O]

<b>Parameters</b>

* dGdx :   array of form [N,K]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  
* dHdG :  array of form [O][N,K]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Derivative of H to G  

<a name="pipe_6"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_6(</strong> dGdx, dHdG ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L886-L900 target=_blank>[source]</a></th></tr></thead></table>
ndim == 1 and ninter > 1 and ndout == 1

Return derivative in the form of [N]

<b>Parameters</b>

* dGdx :   array of form [N,K]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  
* dHdG :  array of form [N,K]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Derivative of H to G  

<a name="pipe_7"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_7(</strong> dGdx, dHdG ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L902-L917 target=_blank>[source]</a></th></tr></thead></table>
ndim == 1 and ninter = 1 and ndout > 1

Return derivative in the form of [N,O]

<b>Parameters</b>

* dGdx :   array of form [N,O]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  
* dHdG :  array of form [N]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Derivative of H to G  

<a name="pipe_8"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_8(</strong> dGdx, dHdG ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L919-L938 target=_blank>[source]</a></th></tr></thead></table>
ndim > 1 and ninter > 1 and ndout == 1

Return derivative in the form of [N,I]

<b>Parameters</b>

* dGdx :   array of form [K][N,I]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  
* dHdG :  array of form [N,K]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Derivative of H to G  

<a name="pipe_9"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>pipe_9(</strong> dGdx, dHdG ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L940-L974 target=_blank>[source]</a></th></tr></thead></table>
ndim > 1 and ninter == 1 and ndout > 1

Return derivative in the form of [O][N,I]

<b>Parameters</b>

* dGdx :   array of form [N,I]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Either partial dGdp or derivative dGdx  
* dHdG :  array of form [N,O]
<br>&nbsp;&nbsp;&nbsp;&nbsp; Derivative of H to G  

<a name="shortName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>shortName(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L976-L987 target=_blank>[source]</a></th></tr></thead></table>
Return a short version the string representation: upto first non-letter.

<a name="getNumberOfParameters"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getNumberOfParameters(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L989-L994 target=_blank>[source]</a></th></tr></thead></table>
Returns the number of parameters of the ( compound ) model.  

<a name="numDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>numDerivative(</strong> xdata, param )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L996-L1009 target=_blank>[source]</a></th></tr></thead></table>
Returns numerical derivatives (df/dx) of the model function.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; input data
* param  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; a parameters vector


<a name="numPartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>numPartial(</strong> xdata, param )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1011-L1023 target=_blank>[source]</a></th></tr></thead></table>
Returns numerical partial derivatives of the model function.

<b>Parameters</b>

* xdata  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; input data
* param  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; a parameters vector


<a name="isDynamic"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isDynamic(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1025-L1035 target=_blank>[source]</a></th></tr></thead></table>
Return whether the model can change the number of parameters dynamically.

<a name="hasPriors"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasPriors(</strong> isBound=True ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1037-L1051 target=_blank>[source]</a></th></tr></thead></table>
Return True when the model has priors for all its parameters.

<b>Parameters</b>

* isBound  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; Also check if the prior is bound.

<a name="getPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getPrior(</strong> kpar )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1053-L1074 target=_blank>[source]</a></th></tr></thead></table>
Return the prior of the indicated parameter.

<b>Parameters</b>

* kpar  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter number.

<b>Raises</b>

IndexError when kpar is larger than the number of parameters.


<a name="setPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setPrior(</strong> kpar, prior=None, **kwargs )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1076-L1103 target=_blank>[source]</a></th></tr></thead></table>
Set the prior for the indicated parameter.

<b>Parameters</b>

* kpar  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter number.
* prior  :  Prior
<br>&nbsp;&nbsp;&nbsp;&nbsp; prior for parameter kpar
* kwargs  :  keyword arguments
<br>&nbsp;&nbsp;&nbsp;&nbsp; attributes to be passed to the prior

<b>Raises</b>

IndexError when kpar is larger than the number of parameters.


<a name="getParameterName"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParameterName(</strong> kpar )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1105-L1126 target=_blank>[source]</a></th></tr></thead></table>
Return the name of the indicated parameter.

<b>Parameters</b>

* kpsr  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter number.

<b>Raises</b>

IndexError when kpar is larger than the number of parameters.


<a name="getParameterUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getParameterUnit(</strong> kpar )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1128-L1150 target=_blank>[source]</a></th></tr></thead></table>
Return the unit of the indicated parameter.

<b>Parameters</b>

* kpar  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameter number.

<b>Raise</b>

IndexError when kpar is > number of parameters


<a name="getIntegralUnit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getIntegralUnit(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1152-L1161 target=_blank>[source]</a></th></tr></thead></table>

Return the unit of the integral of the model over x. 
<a name="setLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>setLimits(</strong> lowLimits=None, highLimits=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1163-L1198 target=_blank>[source]</a></th></tr></thead></table>
Sets the limits for the parameters of the compound model.

1. It is valid to insert for either parameter a None value
indicating no lower/upper limits.
2. When a lowerlimit >= upperlimit no limits are enforced.
It only works in *Fitter classes which support it.

<b>Parameters</b>

* lowLimits  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; lower limits on the parameters
* highLimits  :  array_like
<br>&nbsp;&nbsp;&nbsp;&nbsp; upper limits on the parameters


<a name="getLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLimits(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1200-L1228 target=_blank>[source]</a></th></tr></thead></table>
Return the limits stored in the priors

<b>Returns</b>

* limits  :  tuple of 2 array-like or of 2 None (if `self.priors` is None)
<br>&nbsp;&nbsp;&nbsp;&nbsp; (lowlimits, highlimits)

lolim = []
hilim = []
mdl = self
* while mdl is not None  : 
<br>&nbsp;&nbsp;&nbsp;&nbsp; if not super( Model, mdl ).hasLimits( ) 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return [None,None]
<br>&nbsp;&nbsp;&nbsp;&nbsp; lolim += [p.lowLimit for p in mdl.priors]
<br>&nbsp;&nbsp;&nbsp;&nbsp; hilim += [p.highLimit for p in mdl.priors]

&nbsp;&nbsp;&nbsp;&nbsp; mdl = mdl._next
return (lolim, hilim)

<a name="hasLimits"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>hasLimits(</strong> fitindex=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1230-L1251 target=_blank>[source]</a></th></tr></thead></table>
Return true if limits has been set for this model.

<b>Parameters</b>

fitindex    list of indices to be fitted.


<a name="unit2Domain"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>unit2Domain(</strong> uvalue, kpar=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1253-L1276 target=_blank>[source]</a></th></tr></thead></table>
Convert a value in [0,1] to one inside the limits of the parameter.

<b>Parameters</b>

* uvalue  :  (list of) float
<br>&nbsp;&nbsp;&nbsp;&nbsp; value in [0,1]
* kpar  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index of the parameter


<a name="domain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>domain2Unit(</strong> dvalue, kpar=None )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1278-L1299 target=_blank>[source]</a></th></tr></thead></table>
Convert a value within the domain of the parameter to one in [0,1].

<b>Parameters</b>

* dvalue  :  (list of) float
<br>&nbsp;&nbsp;&nbsp;&nbsp; value of parameter
* kpar  :  int
<br>&nbsp;&nbsp;&nbsp;&nbsp; index of the parameter


<a name="partialDomain2Unit"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>partialDomain2Unit(</strong> dvalue )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1301-L1317 target=_blank>[source]</a></th></tr></thead></table>
Return a the derivate of the domain2Unit function to dval.

<b>Parameters</b>

* dvalue  :  (list of) float
<br>&nbsp;&nbsp;&nbsp; parameter array


<a name="nextPrior"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>nextPrior(</strong> ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1319-L1332 target=_blank>[source]</a></th></tr></thead></table>

<a name="isMixed"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>isMixed(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1334-L1336 target=_blank>[source]</a></th></tr></thead></table>

Return false. 
<a name="getLinearIndex"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>getLinearIndex(</strong> )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1338-L1519 target=_blank>[source]</a></th></tr></thead></table>

Return null. 
<a name="testPartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>testPartial(</strong> xdata, params, silent=True )
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1521-L1647 target=_blank>[source]</a></th></tr></thead></table>
A test routine to check the calculation of the partial derivatives.

It is compared to a numerical calculation.

<b>Parameters</b>

* xdata  :  (list of) float
<br>&nbsp;&nbsp;&nbsp;&nbsp; values of the independent variable
* params  :  list of floats
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters for the model
* silent  :  bool
<br>&nbsp;&nbsp;&nbsp;&nbsp; if false print outputs

<b>Return</b>

The number of large deviations.


<a name="strictNumericPartial"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>strictNumericPartial(</strong> xdata, params, parlist=None ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1649-L1692 target=_blank>[source]</a></th></tr></thead></table>
Strictly numeric calculation of partials to params.

For compound models it is different from numPartial and numDerivative.

<b>Parameters</b>

* xdata  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; single xdata point (possibly multidimensional)
* params  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters
* kpar  :  None or int or list of int
<br>&nbsp;&nbsp;&nbsp;&nbsp; int  : return derivative to parameter kpar.

<a name="assignDF1"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>assignDF1(</strong> partial, i, dpi ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1694-L1695 target=_blank>[source]</a></th></tr></thead></table>

<a name="assignDF2"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>assignDF2(</strong> partial, i, dpi ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1697-L1702 target=_blank>[source]</a></th></tr></thead></table>

<a name="strictNumericDerivative"></a>
<table><thead style="background-color:#E0FFE0; width:100%; font-size:15px"><tr><th style="text-align:left">
<strong>strictNumericDerivative(</strong> xdata, param ) 
</th><th style="text-align:right; font-size:12px"><a href=https://github.com/dokester/BayesicFitting/blob/master/BayesicFitting/source//#L1704-L1749 target=_blank>[source]</a></th></tr></thead></table>
Strictly numeric calculation of derivative.

For compound models it is different from numPartial and numDerivative.

&nbsp;&nbsp;&nbsp;&nbsp; ## More dimensions in x

<b>Parameters</b>

* xdata  :  float
<br>&nbsp;&nbsp;&nbsp;&nbsp; single xdata point (possibly multidimensional)
* param  :  array-like
<br>&nbsp;&nbsp;&nbsp;&nbsp; parameters

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
* [<strong>getParameterIndex(</strong> parname ) ](./BaseModel.md#getParameterIndex)
* [<strong>getParameterValue(</strong> param, name, default=None ) ](./BaseModel.md#getParameterValue)
* [<strong>baseParameterName(</strong> kpar ) ](./BaseModel.md#baseParameterName)
* [<strong>baseParameterUnit(</strong> kpar ) ](./BaseModel.md#baseParameterUnit)
