import numpy as numpy

from .ConvergenceError import ConvergenceError
from .BaseFitter import BaseFitter
from .IterativeFitter import IterativeFitter
from .IterationPlotter import IterationPlotter
from .GaussErrorDistribution import GaussErrorDistribution
from .LaplaceErrorDistribution import LaplaceErrorDistribution
from .CauchyErrorDistribution import CauchyErrorDistribution
from .PoissonErrorDistribution import PoissonErrorDistribution
from .GenGaussErrorDistribution import GenGaussErrorDistribution


__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

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
#  * The GPL3 license can be found at <http://www.gnu.org/licenses/>.
#  *
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2003 - 2014 Do Kester, SRON ( Java code )
#  *    2016 - 2017 Do Kester

class MaxLikelihoodFitter( IterativeFitter ):
    """
    Base class with methods common to fitters handling ErrorDistributions.

    Author:      Do Kester.

    Attributes
    ----------
    errdis : None | "gauss" | "laplace" | "cauchy" | "poisson" | "gengauss"
        None : Use _ChiSq as function to be minimized
        name : use -logLikelihood as function to be minimized from the named
                errordistribution.
    scale : float
        the (fixed) noise scale
    power : float (2)
        power of errdis (if applicable)

    Raises
    ------
    ConvergenceError    Something went wrong during the convergence if the fit.

    """
    def __init__( self, xdata, model, errdis=None, scale=None, power=2.0,
                    **kwargs ):
        """
        Create a new iterative fitter, providing xdatas and model.

        This is a base class. It collects stuff common to all iterative fitters.
        It does not work by itself.

        Parameters
        ----------
        xdata : array_like
            array of independent input values
        model : Model
            the model function to be fitted

        errdis : None | "gauss" | "laplace" | "cauchy" | "poisson" | "gengauss"
            None : Use _ChiSq as function to be minimized
            name : use -logLikelihood as function to be minimized from the named
                    errordistribution.
        scale : float
            the (fixed) noise scale of errdis (if applicable)
        power : float (2.0)
            the power of errdis ( if applicable)
        kwargs : dict
            Possibly includes keywords from
                IterativeFitter :       maxIter, tolerance, verbose
                BaseFitter :            map, keep, fixedScale

        """
        if scale is not None :
            kwargs["fixedScale"] = scale

        super( MaxLikelihoodFitter, self ).__init__( xdata, model, **kwargs )

        self.errdis = errdis
        self.power = power

    def makeFuncs( self, data, weights=None, index=None, ret=3 ) :
        """
        Make connection to the desired func, gradient and hessian.

        Parameters
        ----------
        data : array_like
            the data to be fitted
        weights : array_like or None
            weights on the data
        index : array_like
            indices of the parameters to be fitted.
        ret : 1 or 2 or 3
            return (func), (func,dfunc) or (func,dfunc,hess)
        """
        if not hasattr( self, "errdis" ) or self.errdis is None :
            landscape = _Chisq( self, data, weights, index=index )
            self.isChisq = True
        else :
            scale = 1.0 if self.fixedScale is None else self.fixedScale
            landscape = _LogL( self, data, weights, index=index,
                    errdis=self.errdis, scale=scale, power=self.power )
            self.isChisq = False

#        self.func = landscape.func
#        self.dfunc = landscape.dfunc
#        self.hfunc = landscape.hessian
        self.landscape = landscape

        if ret == 1 :
            return ( landscape.func )

        # Gradient (or fprime or sometimes jacobian ... confusing)
        if not hasattr( self, "userGradient" ) or not self.userGradient :
            dfunc = None                        ## nonexistent, False or None
        elif callable( self.userGradient ) :
            dfunc = landscape.userdfunc         ## callable function
        else :
            dfunc = landscape.dfunc             ## default, True

        if ret == 2 :
            return ( landscape.func, dfunc )

        return ( landscape.func, dfunc, landscape.hessian )


    def getScale( self ) :
        """
        Return the stdev of the noise.
        """
        if isinstance( self.landscape, _LogL ) :
            errdis = self.landscape.errdis
            return errdis.toSigma( errdis.getScale( self.model ) )

        return super( MaxLikelihoodFitter, self ).getScale()


    def getLogLikelihood( self, autoscale=False, var=1.0 ) :
        if self.isChisq :
            return super( MaxLikelihoodFitter, self ).getLogLikelihood(
                        autoscale=autoscale, var=var )

        if autoscale :
            try :
                self.landscape.hypar[0] = self.getScale()
            except IndexError :
                pass
        return - self.landscape.func( self.model.parameters )


    def normalize( self, normdfdp, normdata, weight=1.0 ) :
        """
        Not Implemented.

        Raises
        ------
        NotImplementedError.
        the method is not implemented for MaxLikelihoodFitters

        """
        raise NotImplementedError( "Not implemented for %s." % str( self ) )


    def testGradient( self, par, at, data, weights=None ):
        """
        returns true if the test fails.

        """

        (func,grad) = self.makeFuncs( data, weights=weights, ret=2 )

        df = grad( par )

        dp = 0.001
        pars = par.copy()
        pars[at] -= dp / 2
        r1 = func( pars )
        pars[at] += dp
        r2 = func( pars )
        grat = numpy.subtract( r2, r1 ) / dp

        print( "At %4d  grad : %10.4f  num : %10.4f"%(at, df[at], grat) )

        return ( abs( grat - df[at] ) > 0.001 )

    def __str__( self ):
        return "MaxLikelihoodFitter"


class _Chisq( object ):
    """
    Internal class to provide a chisq landscape.

    It defines
    func (chisq), dfunc (dchisq/dp) and hess (hessian matrix).

    """

    def __init__( self, outer, data, weights, index=None ):
        """
        Parameters
        ----------
        outer : IterativeFitter
            the outer class of this inner class
        data : array_like
            the data
        weights : array_like
            the weights
        index : array_like
            fit index
        """
        self._outer = outer
        self._data = data
        self._weights = weights
        self._index = index

    def func( self, par ):
        """
        Return the function to be minimized.
        In this case
        .. math::
            \chi^2 = \sum( D_i - F(x_i:p) )^2

        """
        param = self._outer.insertParameters( par, index=self._index )
        return self._outer.chiSquared( self._data, params=param,
                    weights=self._weights )

    def userdfunc( self, par ):
        """
        Return an efficient calculation of the gradient.
        """
        return self._outer.userGradient( self._outer.xdata, par, self._data,
                                  weights=self._weights, index=self._index )

    def dfunc( self, par ):
        """
        Return the gradient of func to the parameters p.
        .. math::
            d\chi^2/dp = -2 \sum( D_i - F_i ) dF_i/dp
        """
        param = self._outer.insertParameters( par, index=self._index )
        res = numpy.subtract( self._outer.model.result( self._outer.xdata, param ), self._data )
        if self._weights is not None:
            res = numpy.multiply( res, self._weights )
        desmat = self._outer.getDesign( params=param, index=self._index )

        return 2 * numpy.inner( desmat.transpose(), res )

    def hessian( self, par ):
        """
        Return the Hessian matrix.
        """
        return self._outer.getHessian( params=par, weights=self._weights, index=self._index )

class _LogL( _Chisq ) :
    """
    Internal class to provide a log Likelihood landscape.

    It defines
    func (-logL), dfunc (dlogL/dp) and hess (hessian matrix).

    """
    def __init__( self, outer, data, weights, index=None, errdis='gauss',
                    scale=1.0, power=2.0 ):
        """
        Parameters
        ----------
        outer : IterativeFitter
            the outer class of this inner class
        data : array_like
            the data
        weights : array_like
            the weights
        index : array_like
            fit index
        errdis : "gauss" | "laplace" | "cauchy" | "poisson" | "gengauss"
            errordistribution to be used to calculate logLikelihood
        scale : float (1.0)
            scale if applicable in errdis
        power : float (2.0)
            power if applicable in errdis
        """

        super( _LogL, self ).__init__( outer, data, weights, index=None )

        if errdis == 'gauss' :
            self.errdis = GaussErrorDistribution( outer.xdata, data,
                    weights=weights, scale=scale )
            self.hypar = [scale]
        elif errdis == 'laplace' :
            self.errdis = LaplaceErrorDistribution( outer.xdata, data,
                    weights=weights, scale=scale )
            self.hypar = [scale]
        elif errdis == 'cauchy' :
            self.errdis = CauchyErrorDistribution( outer.xdata, data, scale=scale )
            self.hypar = [scale]
        elif errdis == 'poisson' :
            self.errdis = PoissonErrorDistribution( outer.xdata, data )
            self.hypar = []
        elif errdis == 'gengauss' :
            self.errdis = GenGaussErrorDistribution( outer.xdata, data,
                    weights=weights, scale=scale, power=power )
            self.hypar = [scale, power]
        else :
            raise ValueError( "Unknown errordistribution %s."%errdis )

    def func( self, par ) :
        param = self._outer.insertParameters( par, index=self._index )
        param = numpy.append( param, self.hypar )
        return - self.errdis.logLikelihood( self._outer.model, param )


    def dfunc( self, par ) :
        param = self._outer.insertParameters( par, index=self._index )
        param = numpy.append( param, self.hypar )

        return - self.errdis.partialLogL( self._outer.model, param, self._index )

    def hessian( self, par ) :
        param = self._outer.insertParameters( par, index=self._index )
        param = numpy.append( param, self.hypar )

        return - self.errdis.hessianLogL( self._outer.model, param, self._index )


