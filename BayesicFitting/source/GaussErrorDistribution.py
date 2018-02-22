import numpy as numpy
import math

from .ScaledErrorDistribution import ScaledErrorDistribution

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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2017        Do Kester


class GaussErrorDistribution( ScaledErrorDistribution ):
    """
    To calculate a Gauss likelihood.

    For one residual, x, it holds
    .. math::
        f( x ) = 1 / \sqrt( 2 \pi s^2 ) exp( - 0.5 ( x / s )^2 )

    where s is the scale.
    s is a hyperparameter, which might be estimated from the data.

    The scale s is also the sqrt of the variance of this error distribution.

    The function is mostly used to calculate the likelihood L, or easier
    to use log likelihood, logL.
    .. math::
        logL = \log( N / ( \sqrt( 2 \pi ) s )  ) - 0.5 \sum( ( x / s ) ^ 2 )

    Using weights this becomes:
    .. math::
        logL = \log( \sum( w ) / ( \sqrt( 2 \pi ) s )  ) - 0.5 \sum( w ( x / s ) ^ 2 )


    Author       Do Kester.

    """
    LOG2PI = math.log( 2 * math.pi )


    #  *********CONSTRUCTORS***************************************************
    def __init__( self, xdata, data, weights=None, scale=1.0, limits=None,
                  copy=None ):
        """
        Default Constructor.

        Parameters
        ----------
        xdata : array_like
            input data for the model (independent data)
        data : array_like
            data to be fitted (dependent data)
        weights : array_like
            weights to be used
        scale : float
            noise scale
        limits : None or list of 2 floats [low,high]
            None : no limits implying fixed scale
            low     low limit on scale (needs to be >0)
            high    high limit on scale
            when limits are set, the scale is *not* fixed.

        copy : GaussErrorDistribution
            distribution to be copied.

        """
        super( GaussErrorDistribution, self ).__init__( xdata, data, weights=weights,
                    scale=scale, limits=limits, copy=copy )

    def copy( self ):
        """ Return copy of this.  """
        return GaussErrorDistribution( self.xdata, self.data, copy=self )

    def acceptWeight( self ):
        """
        True if the distribution accepts weights.
        Always true for this distribution.
        """
        return True


    #  *********LIKELIHOODS***************************************************
    def logLikelihood( self, model, allpars ) :
        """
        Return the log( likelihood ) for a Gaussian distribution.

        Parameters
        ----------
        model : Model
            to be fitted
        allpars : array_like
            list of all parameters in the problem

        """
        np = model.npchain
        scale = allpars[np]
        res = self.getResiduals( model, allpars[:np] )
        chisq = self.getChisq( res, scale )
        self.ncalls += 1
        return ( - self.sumweight * ( 0.5 * self.LOG2PI + math.log( scale ) ) -
                       0.5 * chisq )

    def getScale( self, model ) :
        """
        Return the noise scale.

        Parameters
        ----------
        mode : Model
            the model involved
        """
        chi = self.getChisq( self.getResiduals( model ), 1.0 )
        return math.sqrt( chi / self.sumweight )

    def getSumRes( self, residual, scale ):
        return self.getChiSq( residual, scale )

    def getChisq( self, residual, scale ):
        """
        Return chisq.

        Sum over the (weighted) squared normalozed residuals

        Parameters
        ----------
        residual : array_like
            the residuals
        scale : float
            hyperparameter of the problem; here it is the noise scale

        """
        res2 = numpy.square( residual )
        if self.weights is not None :
            res2 = res2 * self.weights
        return numpy.sum( res2  ) / ( scale * scale )

    def partialLogL( self, model, allpars, fitIndex ) :
        """
        Return the partial derivative of log( likelihood ) to the parameters in fitIndex.

        Parameters
        ----------
        model : Model
            to be fitted
        allpars : array_like
            parameters of the problem
        fitIndex : array_like
            indices of parameters to be fitted

        """
        self.nparts += 1                    ## counts calls to partialLogL

        np = model.npchain
        param = allpars[:np]
        scale = allpars[np]
        s2 = scale * scale
        res = self.getResiduals( model, param )
        if self.weights is not None :
            resw = res * self.weights
        else :
            resw = res
        dM = model.partial( self.xdata, param )

        dL = numpy.zeros( len( fitIndex ), dtype=float )
        i = 0
        for  k in fitIndex:
            if k < np :
                dL[i] = numpy.sum( resw * dM[:,k] ) / s2
            else :
                dL[i] = ( numpy.sum( res * resw ) / s2 - self.sumweight ) / scale
            i += 1
        return dL

    def hessianLogL( self, model, allpars, fitIndex ) :
        """
        Return the hessian of log( likelihood ) to the parameters in fitIndex.

        ..math::
             hessian = d^2 logL/ dp_i dp_k

        Parameters
        ----------
        model : Model
            to be fitted
        allpars : array_like
            parameters of the problem
        fitIndex : array_like
            indices of parameters to be fitted

        """
        self.nparts += 1                    ## counts calls to partialLogL

        nh = len( fitIndex )
        np = model.npchain
        param = allpars[:np]
        scale = allpars[np]
        s2 = scale * scale

        fi = fitIndex if fitIndex[-1] != np else fitIndex[-1:]

        nf = len( fi )
        design = model.partial( self.xdata, param )[:,fi]
        design = design.transpose()
        deswgt = design
        if self.weights is None :
            deswgt *= self.weights

        hessian = numpy.zeros( ( nh, nh ), dtype=float )
        hessian[:nf,:nf] = numpy.inner( design, deswgt ) / s2

        if fitIndex[-1] == np :
            hessian[nf,nf] = 2 * ( self.ndata - nf ) / s2

        return hessian

    def __str__( self ) :
        return "Gauss error distribution"
