import numpy as numpy
import warnings

# unconstrained minimization
from scipy.optimize import minimize

from .MaxLikelihoodFitter import MaxLikelihoodFitter
#from ConvergenceError import ConvergenceError

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
__version__ = "2.5.3"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Perpetual Beta"

#  *
#  * This file is part of the BayesicFitting package.
#  *
#  * BayesicFitting is free software: you can redistribute it and/or modify
#  * it under the terms of the GNU Lesser General Public License as
#  * published by the Free Software Foundation, either version 3 of
#  * the License, or ( at your option ) any later version.
#  *
#  * BayesicFitting is distributed in the hope that it will be useful,
#  * but WITHOUT ANY WARRANTY; without even the implied warranty of
#  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  * GNU Lesser General Public License for more details.
#  *
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2007 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2020 Do Kester


class ScipyFitter( MaxLikelihoodFitter ):
    """
    Unified interface to the Scipy minimization module minimize, to fit data to a model.

    For documentation see scipy.org->Docs->Reference Guide->optimization and root finding.
    scipy.optimize.minimize


    Examples
    --------
    # assume x and y are Double1d data arrays.
    >>> x = numpy.arange( 100, dtype=float ) / 10
    >>> y = numpy.arange( 100, dtype=float ) / 122          # make slope
    >>> y += 0.3 * numpy.random.randn( 100 )                # add noise
    >>> y[9:12] += numpy.asarray( [5,10,7], dtype=float )   # make some peak
    >>> gauss = GaussModel( )                               # Gaussian
    >>> gauss += PolynomialModel( 1 )                       # add linear background
    >>> print( gauss.npchain )
    >>> cgfit = ConjugateGradientFitter( x, gauss )
    >>> param = cgfit.fit( y )
    >>> print( len( param ) )
    5
    >>> stdev = cgfit.stdevs
    >>> chisq = cgfit.chisq
    >>> scale = cgfit.scale                                 # noise scale
    >>> yfit  = cgfit.getResult( )                          # fitted values
    >>> yband = cgfit.monteCarloEoor( )                         # 1 sigma confidence region

    Notes
    -----
    1. CGF is <b>not</b> guaranteed to find the global minimum.
    2. CGF does <b>not</b> work with fixed parameters or limits

    Attributes
    ----------
    gradient : callable gradient( par )
        User provided method to calculate the gradient of chisq.
        It can be used to speed up the dotproduct calculation, maybe
        because of the sparseness of the partial.
        default  dotproduct of the partial with the residuals
    tol : float (1.0e-5)
        Stop when the norm of the gradient is less than tol.
    norm : float (inf)
        Order to use for the norm of the gradient (-np.Inf is min, np.Inf is max).
    maxIter : int (200*len(par))
        Maximum number of iterations
    verbose : bool (False)
        if True print status at convergence
    debug : bool (False)
        return the result of each iteration in `vectors`
    yfit : ndarray (read only)
        the result of the model at the optimal parameters
    ntrans : int (read only)
        number of function calls
    ngrad : int (read only)
        number of gradient calls
    vectors : list of ndarray (read only when debug=True)
        list of intermediate vectors

    Hidden Attributes
    -----------------
    _Chisq : class
        to calculate chisq in the method Chisq.func() and Chisq.dfunc()

    Returns
    -------
    pars : array_like
        the parameters at the minimum of the function (chisq).

    """
## ******************************************************************************
    def __init__( self, xdata, model, method=None, gradient=True, hessp=None,
                    **kwargs ) :
        """
        Constructor.
        Create a class, providing inputs and model.

        Parameters
        ----------
        xdata : array_like
            array of independent input values
        model : Model
            a model function to be fitted (linear or nonlinear)
        method : None | 'CG' | 'NELDER-MEAD' | 'POWELL' | 'BFGS' | 'NEWTON-CG' | 'L-BFGS-B' |
                  'TNC' | 'COBYLA' | 'SLSQP' | 'DOGLEG' | 'TRUST-NCG'
            the method name is case invariant.
            None            Automatic selection of the method.
                            'SLSQP' when the problem has constraints
                            'L-BFGS-B' when the problem has limits
                            'BFGS' otherwise
            'CG'            Conjugate Gradient Method of Polak and Ribiere
                            :ref:`(see here) <optimize.minimize-cg>`
            'NELDER-MEAD'   Nelder Mead downhill simplex
                            :ref:`(see here) <optimize.minimize-neldermead>`
            'POWELL'        Powell's conjugate direction method
                            :ref:`(see here) <optimize.minimize-powell>`
            'BFGS'          Quasi-Newton method of Broyden, Fletcher, Goldfarb, and Shannon
                            :ref:`(see here) <optimize.minimize-bfgs>`
            'NEWTON-CG'     Truncated Newton method
                            :ref:`(see here) <optimize.minimize-newtoncg>`
            'L-BFGS-B'      Limited Memory Algorithm for Bound Constrained Optimization
                            :ref:`(see here) <optimize.minimize-lbfgsb>`
            'TNC'           Truncated Newton method with limits
                            :ref:`(see here) <optimize.minimize-tnc>`
            'COBYLA'        Constrained Optimization BY Linear Approximation
                            :ref:`(see here) <optimize.minimize-cobyla>`
            'SLSQP'         Sequential Least Squares
                            :ref:`(see here) <optimize.minimize-slsqp>`
            'DOGLEG'        Dog-leg trust-region algorithm
                            :ref:`(see here) <optimize.minimize-dogleg>`
            'TRUST-NCG'     Newton conjugate gradient trust-region algorithm
                            :ref:`(see here) <optimize.minimize-trustncg>`

        gradient : bool or None or callable gradient( par )
            if True use gradient calculated from model. It is the default.
            if False/None dont use gradient (use numeric approximation in stead)
            if callable use the method as gradient
        hessp : callable hessp(x, p, *args) or None
            Function which computes the Hessian times an arbitrary vector, p.
            The hessian itself is always provided.
        kwargs : dict
            Possibly includes keywords from
                MaxLikelihoodFitter :   errdis, scale, power
                IterativeFitter :       maxIter, tolerance, verbose
                BaseFitter :            map, keep, fixedScale

        """
        super( ScipyFitter, self ).__init__( xdata, model, **kwargs )

        self.userGradient = gradient
        self.userHessp = hessp
        self.method = str.upper( method )
        self.norm = numpy.inf
        self.debug = False
        self.ngrad = 0

        numpy.set_printoptions(formatter={'float': '{: 0.3f}'.format})


    #  *************************************************************************
    def fit( self, data, weights=None, par0=None, keep=None, limits=None,
                maxiter=None, tolerance=None, constraints=(), verbose=0,
                plot=False, callback=None, **options ):
        """
        Return      parameters for the model fitted to the data array.

        Parameters
        ----------
        ydata : array_like
            the data vector to be fitted
        weights : array_like
            weights pertaining to the data
        par0 : array_like
            initial values of the function. Default from Model.
        keep : dict of {int:float}
            dictionary of indices (int) to be kept at a fixed value (float)
            The values of keep are only valid for *this* fit
            See also `ScipyFitter( ..., keep=dict )`
        limits : None or list of 2 floats or list of 2 array_like
            None : no limits applied
            [lo,hi] : low and high limits for all values
            [la,ha] : low array and high array limits for the values
        constraints : list of callables
            constraint functions cf. All are subject to cf(par) > 0.

        maxiter : int
            max number of iterations
        tolerance : float
            stops when ( |hi-lo| / (|hi|+|lo|) ) < tolerance
        verbose : int
            0 : silent
            >0 : print output if iter % verbose == 0
        plot : bool
            Plot the results
        callback : callable
            is called each iteration as
            `val = callback( val )`
            where `val` is the minimizable array
        options : dict
            options to be passed to the method

        Raises
        ------
            ConvergenceError if it stops when the tolerance has not yet been reached.

        """
        fitIndex, data, weights = self.fitprolog( data, weights=weights, keep=keep )

        inipar = self.model.parameters[fitIndex]

        # Check for limits in the prior
        if limits is not None and self.model.priors :
            try :
                limits = ( self.model.lowLimits[fitIndex], self.model.highLimits[fitIndex] )
            except :
                limits = ( self.model.lowLimits, self.model.highLimits )

        if self.method is None:
            # Select automatically
            if constraints:
                self.method = 'SLSQP'
            elif limits is not None:
                self.method = 'L-BFGS-B'
            else:
                self.method = 'BFGS'

        (func,gradient,hess) = self.makeFuncs( data, weights=weights, index=fitIndex )

        print( self.method )

        # - hessp
        useHessian = self.method in ('NEWTON-CG', 'DOGLEG', 'TRUST-NCG')
        if ( not useHessian and hasattr( self, "userHessp" ) and self.userHessp is not None ) :
            warnings.warn('Method %s does not use Hessian-vector product '
                    'information (hessp).' % self.method, RuntimeWarning)

        # - constraints or limits
        if (self.method in ['NELDER-MEAD', 'POWELL', 'CG', 'BFGS', 'NEWTON-CG', 'DOGLEG',
                 'TRUST-NCG'] and ( limits is not None or numpy.any( constraints ) ) ):
            warnings.warn('Method %s cannot handle constraints nor limits.' % self.method,
                 RuntimeWarning)
        if self.method in ['L-BFGS-B', 'TNC'] and numpy.any( constraints ):
            warnings.warn('Method %s cannot handle constraints.' % self.method, RuntimeWarning)
        if self.method == 'COBYLA' and limits is not None:
            warnings.warn('Method %s cannot handle limits.' % self.method, RuntimeWarning)

        # - callback
        if (self.method in ['COBYLA'] and callback is not None):
            warnings.warn('Method %s does not support callback.' % self.method, RuntimeWarning)
        elif self.debug :
            self.vectors = numpy.asarray( [inipar] )
            print( self.vectors )
            callback = self.collectVectors

        # - return_all
        if (self.method in ['L-BFGS-B', 'TNC', 'COBYLA', 'SLSQP'] and
                options.get('return_all', False)):
            warnings.warn('Method %s does not support the return_all option.' % self.method,
                 RuntimeWarning)

        if options is None:
            options = {}

        if self.method == 'NELDER-MEAD':
            options.setdefault( 'xatol', self.tolerance )
            options.setdefault( 'fatol', self.tolerance )
            options.setdefault( 'maxiter', self.maxIter )
            res = minimize( func, inipar, method="Nelder-Mead",
                    callback=callback, options=options )
        elif self.method == 'POWELL':
            options.setdefault( 'ftol', self.tolerance )
            options.setdefault( 'xtol', self.tolerance )
            options.setdefault( 'maxiter', self.maxIter )
            res = minimize( func, inipar, method="Powell",
                    callback=callback, options=options )
        elif self.method == 'CG':
            options.setdefault( 'gtol', self.tolerance )
            options.setdefault( 'maxiter', self.maxIter )
            res = minimize( func, inipar, jac=gradient, method="CG",
                    callback=callback, options=options )
        elif self.method == 'BFGS':
            options.setdefault( 'gtol', self.tolerance )
            options.setdefault( 'maxiter', self.maxIter )
            res = minimize( func, inipar, jac=gradient, method="BFGS",
                    callback=callback, options=options )
        elif self.method == 'NEWTON-CG':
            options.setdefault( 'xtol', self.tolerance )
            options.setdefault( 'maxiter', self.maxIter )
            res = minimize( func, inipar, jac=gradient, method="Newton-CG",
                    hess=hess, hessp=self.userHessp, callback=callback, options=options )
        elif self.method == 'L-BFGS-B':
            options.setdefault( 'gtol', self.tolerance )
            options.setdefault( 'ftol', self.tolerance )
            res = minimize( func, inipar, jac=gradient, method="L-BFGS-B",
                    bounds=limits, callback=callback, options=options )
        elif self.method == 'TNC':
            options.setdefault( 'gtol', self.tolerance )
            options.setdefault( 'ftol', self.tolerance )
            options.setdefault( 'xtol', self.tolerance )
            res = minimize( func, inipar, jac=gradient, method="TNC",
                    bounds=limits, callback=callback, options=options )
        elif self.method == 'COBYLA':
            options.setdefault( 'tol', self.tolerance )
            res = minimize( func, inipar, method="COBYLA",
                    constraints=constraints, callback=callback, options=options )
        elif self.method == 'SLSQP':
            options.setdefault( 'ftol', self.tolerance )
            res = minimize( func, inipar, jac=gradient, method="SLSQP",
                    bounds=limits, constraints=constraints, callback=callback, options=options )
        elif self.method == 'DOGLEG':
            options.setdefault( 'gtol', self.tolerance )
            res = minimize( func, inipar, jac=gradient, method="dogleg",
                    hess=hess, callback=callback, options=options )
        elif self.method == 'TRUST-NCG':
            options.setdefault( 'gtol', self.tolerance )
            res = minimize( func, inipar, jac=gradient, method="trust-ncg",
                    hess=hess, hessp=self.userHessp, callback=callback, options=options )
        else:
            raise ValueError('Unknown solver %s' % self.method)

        print( res )

        parameters = self.insertParameters( res["x"], index=fitIndex )
        self.model.parameters = parameters

        if self.errdis is None :
            self.chisq = res["fun"]
        else :
            self.logLikelihood = -res["fun"]


#        self.chisq = res["fun"]
        self.ntrans = res["nfev"]
#        print( self.method, self.method != "COBYLA" )
        if self.method != "COBYLA" :
            self.iter = res["nit"]
        # - gradient
        if self.method in ('CG', 'BFGS', 'NEWTON-CG', 'DOGLEG', 'TRUST-NCG') :
            self.ngrad = res["njev"]

        self.fulloutput = res

        warn = res["status"]
        if warn == 1 :
            warnings.warn( "Maximum number of iterations reached" )
        elif warn == 2 :
            warnings.warn( "Gradient and/or function calls were not changing." )

        self.fitpostscript( data, plot=plot )

        return parameters

    def collectVectors( self, par ) :
        self.vectors = numpy.append( self.vectors, [par], 0 )

    def __str__( self ):
        """
        Return the name of the fitter.
        """
        if not hasattr( self, "errdis" ) or self.errdis is None :
            cost = "chisq"
        else :
            cost = self.errdis
        return "ScipyFitter (%s) using %s"%(self.method, cost)

#####################################################################################
###     Specific Fitters                                                        #####
#####################################################################################


class NelderMeadFitter( ScipyFitter ) :
    """
    Nelder Mead downhill simplex.

    Syntactic sugar for
        ScipyFitter( ..., method='NELDER-MEAD', ... )

    See @ScipyFitter

    """

    def __init__( self, xdata, model, **kwargs ) :
        """
        Constructor.
        Create a class, providing inputs and model.

        Parameters
        ----------
        xdata : array_like
            array of independent input values
        model : Model
            a model function to be fitted (linear or nonlinear)
        kwargs : dict
            Possibly includes keywords from
                ScipyFitter:            gradient, hessp
                MaxLikelihoodFitter :   errdis, scale, power
                IterativeFitter :       maxIter, tolerance, verbose
                BaseFitter :            map, keep, fixedScale

        """
        super( NelderMeadFitter, self ).__init__( xdata, model, method='NELDER-MEAD',
                        **kwargs )

class PowellFitter( ScipyFitter ) :
    """
    Powell's conjugate direction method.

    Syntactic sugar for
        ScipyFitter( ..., method='POWELL', ... )

    See @ScipyFitter

    """
    def __init__( self, xdata, model, **kwargs ) :
        """
        Constructor.
        Create a class, providing inputs and model.

        Parameters
        ----------
        xdata : array_like
            array of independent input values
        model : Model
            a model function to be fitted (linear or nonlinear)
        kwargs : dict
            Possibly includes keywords from
                ScipyFitter:            gradient, hessp
                MaxLikelihoodFitter :   errdis, scale, power
                IterativeFitter :       maxIter, tolerance, verbose
                BaseFitter :            map, keep, fixedScale

        """
        super( PowellFitter, self ).__init__( xdata, model, method='POWELL', **kwargs )

class ConjugateGradientFitter( ScipyFitter ) :
    """
    Conjugate Gradient Method of Polak and Ribiere.

    Syntactic sugar for
        ScipyFitter( ..., method='CG', ... )

    See @ScipyFitter

    """
    def __init__( self, xdata, model, gradient=True, **kwargs ) :
        """
        Constructor.
        Create a class, providing inputs and model.

        Parameters
        ----------
        xdata : array_like
            array of independent input values
        model : Model
            a model function to be fitted (linear or nonlinear)
        gradient : bool or None or callable gradient( par )
            if True use gradient calculated from model. It is the default.
            if False/None dont use gradient (use numeric approximation in stead)
            if callable use the method as gradient
        kwargs : dict
            Possibly includes keywords from
                ScipyFitter:            gradient, hessp
                MaxLikelihoodFitter :   errdis, scale, power
                IterativeFitter :       maxIter, tolerance, verbose
                BaseFitter :            map, keep, fixedScale

        """
        super( ConjugateGradientFitter, self ).__init__( xdata, model, method='CG',
                **kwargs )

class BfgsFitter( ScipyFitter ) :
    """
    Quasi-Newton method of Broyden, Fletcher, Goldfarb, and Shannon.

    Syntactic sugar for
        ScipyFitter( ..., method='BFGS', ... )

    See @ScipyFitter

    """
    def __init__( self, xdata, model, gradient=True, **kwargs ) :
        """
        Constructor.
        Create a class, providing inputs and model.

        Parameters
        ----------
        xdata : array_like
            array of independent input values
        model : Model
            a model function to be fitted (linear or nonlinear)
        gradient : bool or None or callable gradient( par )
            if True use gradient calculated from model. It is the default.
            if False/None dont use gradient (use numeric approximation in stead)
            if callable use the method as gradient
        kwargs : dict
            Possibly includes keywords from
                ScipyFitter:            gradient, hessp
                MaxLikelihoodFitter :   errdis, scale, power
                IterativeFitter :       maxIter, tolerance, verbose
                BaseFitter :            map, keep, fixedScale

        """
        super( BfgsFitter, self ).__init__( xdata, model, method='BFGS', gradient=gradient,
                        **kwargs )


class NewtonCgFitter( ScipyFitter ) :
    """
    Truncated Newton method

    Syntactic sugar for
        ScipyFitter( ..., method='NEWTON-CG', ... )

    See @ScipyFitter

    """
    def __init__( self, xdata, model, gradient=True, **kwargs ) :
        """
        Constructor.
        Create a class, providing inputs and model.

        Parameters
        ----------
        xdata : array_like
            array of independent input values
        model : Model
            a model function to be fitted (linear or nonlinear)
        gradient : bool or None or callable gradient( par )
            if True use gradient calculated from model. It is the default.
            if False/None dont use gradient (use numeric approximation in stead)
            if callable use the method as gradient
        kwargs : dict
            Possibly includes keywords from
                ScipyFitter:            gradient, hessp
                MaxLikelihoodFitter :   errdis, scale, power
                IterativeFitter :       maxIter, tolerance, verbose
                BaseFitter :            map, keep, fixedScale

        """
        super( NewtonCgFitter, self ).__init__( xdata, model, method='NEWTON-CG',
                        gradient=gradient, **kwargs )


class LbfgsbFitter( ScipyFitter ) :
    """
    Limited Memory Algorithm for Bound Constrained Optimization

    Syntactic sugar for
        ScipyFitter( ..., method='L-BFGS-B', ... )

    See @ScipyFitter

    """
    def __init__( self, xdata, model, gradient=True, **kwargs ) :
        """
        Constructor.
        Create a class, providing inputs and model.

        Parameters
        ----------
        xdata : array_like
            array of independent input values
        model : Model
            a model function to be fitted (linear or nonlinear)
        gradient : bool or None or callable gradient( par )
            if True use gradient calculated from model. It is the default.
            if False/None dont use gradient (use numeric approximation in stead)
            if callable use the method as gradient
        kwargs : dict
            Possibly includes keywords from
                ScipyFitter:            gradient, hessp
                MaxLikelihoodFitter :   errdis, scale, power
                IterativeFitter :       maxIter, tolerance, verbose
                BaseFitter :            map, keep, fixedScale

        """
        super( LbfgsbFitter, self ).__init__( xdata, model, method='L-BFGS-B',
                gradient=gradient, **kwargs )


class TncFitter( ScipyFitter ) :
    """
    Truncated Newton method with limits.

    Syntactic sugar for
        ScipyFitter( ..., method='TNC', ... )

    See @ScipyFitter

    """
    def __init__( self, xdata, model, gradient=True, **kwargs ) :
        """
        Constructor.
        Create a class, providing inputs and model.

        Parameters
        ----------
        xdata : array_like
            array of independent input values
        model : Model
            a model function to be fitted (linear or nonlinear)
        gradient : bool or None or callable gradient( par )
            if True use gradient calculated from model. It is the default.
            if False/None dont use gradient (use numeric approximation in stead)
            if callable use the method as gradient
        kwargs : dict
            Possibly includes keywords from
                ScipyFitter:            gradient, hessp
                MaxLikelihoodFitter :   errdis, scale, power
                IterativeFitter :       maxIter, tolerance, verbose
                BaseFitter :            map, keep, fixedScale

        """
        super( TncFitter, self ).__init__( xdata, model, method='TNC', gradient=gradient,
                        **kwargs )


class CobylaFitter( ScipyFitter ) :
    """
    Constrained Optimization BY Linear Approximation.

    Syntactic sugar for
        ScipyFitter( ..., method='COBYLA', ... )

    See @ScipyFitter

    """
    def __init__( self, xdata, model, **kwargs ) :
        """
        Constructor.
        Create a class, providing inputs and model.

        Parameters
        ----------
        xdata : array_like
            array of independent input values
        model : Model
            a model function to be fitted (linear or nonlinear)
        kwargs : dict
            Possibly includes keywords from
                ScipyFitter:            gradient, hessp
                MaxLikelihoodFitter :   errdis, scale, power
                IterativeFitter :       maxIter, tolerance, verbose
                BaseFitter :            map, keep, fixedScale

        """
        super( CobylaFitter, self ).__init__( xdata, model, method='COBYLA',
                        **kwargs )


class SlsqpFitter( ScipyFitter ) :
    """
    Sequential Least Squares

    Syntactic sugar for
        ScipyFitter( ..., method='SLSQP', ... )

    See @ScipyFitter

    """
    def __init__( self, xdata, model, gradient=True, **kwargs ) :
        """
        Constructor.
        Create a class, providing inputs and model.

        Parameters
        ----------
        xdata : array_like
            array of independent input values
        model : Model
            a model function to be fitted (linear or nonlinear)
        gradient : bool or None or callable gradient( par )
            if True use gradient calculated from model. It is the default.
            if False/None dont use gradient (use numeric approximation in stead)
            if callable use the method as gradient
        kwargs : dict
            Possibly includes keywords from
                ScipyFitter:            gradient, hessp
                MaxLikelihoodFitter :   errdis, scale, power
                IterativeFitter :       maxIter, tolerance, verbose
                BaseFitter :            map, keep, fixedScale

        """
        super( SlsqpFitter, self ).__init__( xdata, model, method='SLSQP',
               gradient=gradient, **kwargs )


class DoglegFitter( ScipyFitter ) :
    """
    Dog-leg trust-region algorithm.

    Syntactic sugar for
        ScipyFitter( ..., method='DOGLEG', ... )

    See @ScipyFitter

    """
    def __init__( self, xdata, model, gradient=True, **kwargs ) :
        """
        Constructor.
        Create a class, providing inputs and model.

        Parameters
        ----------
        xdata : array_like
            array of independent input values
        model : Model
            a model function to be fitted (linear or nonlinear)
        gradient : bool or None or callable gradient( par )
            if True use gradient calculated from model. It is the default.
            if False/None dont use gradient (use numeric approximation in stead)
            if callable use the method as gradient
        kwargs : dict
            Possibly includes keywords from
                ScipyFitter:            gradient, hessp
                MaxLikelihoodFitter :   errdis, scale, power
                IterativeFitter :       maxIter, tolerance, verbose
                BaseFitter :            map, keep, fixedScale

        """
        super( DoglegFitter, self ).__init__( xdata, model, method='DOGLEG',
            gradient=gradient, **kwargs )

class TrustNcgFitter( ScipyFitter ) :
    """
    Newton conjugate gradient trust-region algorithm.

    Syntactic sugar for
        ScipyFitter( ..., method='TRUST-NCG', ... )

    See @ScipyFitter

    """
    def __init__( self, xdata, model, gradient=True, **kwargs ) :
        """
        Constructor.
        Create a class, providing inputs and model.

        Parameters
        ----------
        xdata : array_like
            array of independent input values
        model : Model
            a model function to be fitted (linear or nonlinear)
        gradient : bool or None or callable gradient( par )
            if True use gradient calculated from model. It is the default.
            if False/None dont use gradient (use numeric approximation in stead)
            if callable use the method as gradient
        kwargs : dict
            Possibly includes keywords from
                ScipyFitter:            gradient, hessp
                MaxLikelihoodFitter :   errdis, scale, power
                IterativeFitter :       maxIter, tolerance, verbose
                BaseFitter :            map, keep, fixedScale

        """
        super( TrustNcgFitter, self ).__init__( xdata, model, method='TRUST-NCG',
                        gradient=gradient, **kwargs )


