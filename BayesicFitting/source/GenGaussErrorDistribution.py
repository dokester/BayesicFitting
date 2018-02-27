import numpy as numpy
from scipy import special
import math

from .ScaledErrorDistribution import ScaledErrorDistribution
from .HyperParameter import HyperParameter
from .NoiseScale import NoiseScale

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
#  *    2017        Do Kester


class GenGaussErrorDistribution( ScaledErrorDistribution ):
    """
    To calculate a generalized Gaussian likelihood.

    For one residual, x, it holds
    .. math::
        f( x ) = p / ( 2 s \Gamma( 1 / p ) ) exp( - ( |x| / s ) ^ p )

    where s is the scale and p is the power.
    s and p are hyperparameters, which might be estimated from the data.

    The variance of this function is
    .. math::
        \sigma ^ 2 = s ^ 2 \Gamma( 3 / p ) / \Gamma( 1 / p )
    See toSigma()

    The function is mostly used to calculate the likelihood L, or easier
    to use log( L )
    .. math::
        logL = log( N p / ( 2 s \Gamma( 1 / p ) ) ) - \sum( ( |x| / s ) ^ p )

    Using weights this becomes:
    .. math::
        logL = log( \sum( w ) p / ( 2 s \Gamma( 1 / p ) ) ) - \sum( w ( |x| / s ) ^ p )

    Note: the scale s in Generalized Gaussian is NOT the same as the scale in Gaussian or
        in Laplace.

    Author       Do Kester.

    """
    LOG2PI = math.log( 2 * math.pi )
    PARNAMES = ["scale", "power"]

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, xdata, data, weights=None, scale=1.0, power=2.0,
                  limits=None, copy=None ):
        """
        Default Constructor.

        Parameters
        ----------
        xdata : array_like
            input data for the model
        data : array_like
            data to be fitted
        weights : array_like
            weights to be used
        scale : float
            noise scale
        power : float
            power of the distribution
        limits : None or [low,high] or [[low],[high]]
            None : no limits implying fixed scale
            low     low limit on scale (needs to be >0)
            high    high limit on scale
            [low]   low limit on [scale,power] (need to be >0)
            [high]  high limit on [scale,power]
            when limits are set, the scale cq. power are *not* fixed.
        copy : GenGaussErrorDistribution
            distribution to be copied.
        """
        super( GenGaussErrorDistribution, self ).__init__( xdata, data,
                       weights=weights, limits=None, copy=copy )

        plim = None
        if limits is None :
            slim = None
        else :
            lo = limits[0]
            hi = limits[1]
            try :
                slim = [lo[0],hi[0]]
            except :
                slim = [lo,hi]
            try :
                plim = [lo[1],hi[1]]
            except :
                pass

        if copy is None :
            self.hyperpar = [NoiseScale( scale=scale, limits=slim ),
                             HyperParameter( hypar=power, limits=plim )]
        else :
            self.hyperpar = copy.hyperpar

    def copy( self ):
        """ Return copy of this.  """
        return GenGaussErrorDistribution( self.xdata, self.data,
                copy=self )

    def acceptWeight( self ):
        """
        True if the distribution accepts weights.
        Always true for this distribution.
        """
        return True

    def toSigma( self, hypar ) :
        """
        Return sigma, the squareroot of the variance.
        Parameter
        --------
        hypar : array_like (2 floats)
            the [scale,power] of this GenGauss distribution.
        """
        p = hypar[1]
        return hypar[0] * math.sqrt( special.gamma( 3.0 / p ) / special.gamma( 1.0 / p ) )

    #  *********LIKELIHOODS***************************************************
    def logLikelihood( self, model, allpars ) :
        """
        Return the log( likelihood ) for a Gaussian distribution.

        Parameters
        ----------
        model : Model
            model to calculate mock data
        allpars : array_like
            parameters of the problem

        """
        self.ncalls += 1
        np = model.npchain
        scale = allpars[np]
        power = allpars[np+1]

        res = self.getResiduals( model, allpars[:np] )
        chisq = self.getChisq( res, scale, power )
        norm = math.log( power / ( 2 * scale ) ) - special.gammaln( 1.0 / power )
#        print( "GG  ", chisq, norm, self.sumweight )
        return self.sumweight * norm - chisq

    def getChisq( self, residual, scale, power ):
        """
        Return chisq.

        Sum over the (weighted) squared residuals

        Parameters
        ----------
        residual : array_like
            the residuals
        scale : float
            noise scale
        power : float
            power of distribution
        """
        ares = numpy.power( numpy.abs( residual / scale ), power )
        if self.weights is not None :
            ares = ares * self.weights
        return numpy.sum( ares )

    def getScale( self, model ) :
        """
        Return the noise scale calculated from the residuals.

        Parameters
        ----------
        model : Model
            the model involved.
        """
        power = self.hyperpar[1].hypar
        chi = self.getChisq( self.getResiduals( model ), 1.0, power )
        return math.pow( chi / self.sumweight, 1.0 / power )


    def partialLogL( self, model, allpars, fitIndex ) :
        """
        Return the partial derivative of log( likelihood ) to the parameters.

        Parameters
        ----------
        model : Model
            model to calculate mock data
        allpars : array_like
            parameters of the problem
        fitIndex : array_like
            indices of the parameters to be fitted

        """
        self.ncalls += 1
        np = model.npchain
        scale = allpars[np]
        power = allpars[np+1]
        res = self.getResiduals( model, allpars[:np] )

        ars = numpy.abs( res / scale )
        rsp = numpy.power( ars, power )
        if self.weights is not None :
            rsp = rsp * self.weights

        dLdm = power * rsp / res
        dM = model.partial( self.xdata, allpars[:np] )

        dL = numpy.zeros( len( fitIndex ), dtype=float )
        i = 0
        for  k in fitIndex :
            if k < np :
                dL[i] = numpy.sum( dLdm * dM[:,k] )
            elif k == np :
                dL[i] = - self.sumweight / scale + power * numpy.sum( rsp ) / scale
            else :
                # special.psi( x ) is the same as special.polygamma( 1, x )
                dL[i] = self.sumweight * ( power + special.psi( 1.0 / power ) )
                dL[i] /= ( power * power )
                dL[i] -= ( numpy.sum( rsp * numpy.log( ars ) ) )
            i += 1

        return dL

    def __str__( self ) :
        return "Generalized Gauss error distribution"

