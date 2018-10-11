import numpy as numpy
import math

from .ScaledErrorDistribution import ScaledErrorDistribution

__author__ = "Do Kester"
__year__ = 2018
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
#  *    2018        Do Kester


class UniformErrorDistribution( ScaledErrorDistribution ):
    """
    To calculate a Uniform likelihood, eg. for digitization noise.

    For one residual, x, it holds
    .. math::
        f( x ) = 1 / (2*s) if abs( x ) < s else 0

    where s is the scale.
    s is a hyperparameter, which might be estimated from the data.

    The variance of this function is :math:`\sigma^2 = s / 6`.
    See: toSigma()

    The function is mostly used to calculate the likelihood L, or easier
    to use log likelihood, logL.
    .. math::
        logL = -log( 2*s ) if abs( x ) < s else -inf

    Using weights this becomes:
    .. math::
        logL = -w * log( 2*s ) )


    Author       Do Kester.

    """
    SQRT2 = math.sqrt( 2 )
    LGSQ2 = math.log( SQRT2 )
    LOG2 = math.log( 2.0 )


    #  *********CONSTRUCTORS***************************************************
    def __init__( self, xdata, data, weights=None, scale=1.0, limits=None,
                  copy=None ) :
        """
        Constructor of Uniform Distribution.

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
        limits : None or list of 2 floats [low,high]
            None : no limits implying fixed scale
            low     low limit on scale (needs to be >0)
            high    high limit on scale
            when limits are set, the scale is *not* fixed.

        copy : UniformErrorDistribution
            distribution to be copied.
        """
        super( UniformErrorDistribution, self ).__init__( xdata, data,
               weights=weights, scale=scale, limits=limits, copy=copy )

    def copy( self ):
        """ Return copy of this.  """
        return UniformErrorDistribution( self.xdata, self.data, copy=self )

    #  *********DATA & WEIGHT***************************************************
    def acceptWeight( self ):
        """
        True if the distribution accepts weights.
        Always true for this distribution.
        """
        return True

    def toSigma( self, scale ) :
        """
        Return sigma, the squareroot of the variance.
        Parameter
        --------
        scale : float
            the scale of this Uniform distribution.
        """
        return scale * 2 / math.sqrt( 12 )

    #  *********LIKELIHOODS***************************************************
    def logLikelihoodXXX( self, model, allpars ) :
        """
        Return the log( likelihood ) for a Gaussian distribution.

        Outside the range the likelihood is zero, so the logL should be -inf.
        However for computational reasons the maximum negative value is returned.

        Parameters
        ----------
        model : Model
            model to calculate mock data
        allpars : array_like
            parameters of the problem

        """
        self.ncalls += 1
        np = model.npchain
        scale = allpars[-1]
        ares = numpy.abs( self.getResiduals( model, allpars[:np] ) )

        if all( ares < scale ) :
            return - math.log( 2 * scale ) * self.sumweight

        return -math.inf

    def logLdata( self, model, allpars, mockdata=None ) :
        """
        Return the log( likelihood ) for each residual

        logL = sum( logLdata )

        Parameters
        ----------
        model : Model
            to be fitted
        allpars : array_like
            list of all parameters in the problem
        mockdata : array_like
            as calculated by the model

        """
        np = model.npchain
        if mockdata is None :
            mockdata = model.result( self.xdata, allpars[:np] )
        scale = allpars[-1]
        ares = numpy.abs( self.data - mockdata )

        lld = numpy.where( ares < scale, -math.log( 2 * scale ), -math.inf )
        if self.weights is not None :
            lld *= self.weights
        return lld


    def getScale( self, model ) :
        """
        Return the noise scale

        Parameters
        ----------
        model : Model
            the model involved
        """
        return numpy.max( numpy.abs( self.getResiduals( model ) ) )

    def partialLogLXXX( self, model, allpars, fitIndex ) :
        """
        Return the partial derivative of log( likelihood ) to the parameters.

        Parameters
        ----------
        model : Model
            model to calculate mock data
        allpars : array_like
            parameters of the problem
        fitIndex : array_like
            indices of parameters to be fitted

        """
        dL = numpy.zeros( len( fitIndex ), dtype=float )
        if fitIndex[-1] == -1 :
            dL[-1] = -self.sumweight / allpars[-1]
        return dL

    def nextPartialData( self, model, allpars, fitIndex, mockdata=None ) :
        """
        Return the partial derivative of elements of the log( likelihood )
        to the parameters.

        Parameters
        ----------
        model : Model
            model to calculate mock data
        allpars : array_like
            parameters of the problem
        fitIndex : array_like
            indices of parameters to be fitted
        mockdata : array_like
            as calculated by the model

        """
        scale = allpars[-1]
        pll = numpy.zeros_like( self.data )
        if self.weights is not None :
            wgt = self.weights
        else :
            wgt = numpy.ones_like( self.data )

        for k in fitIndex :
            if k >= 0 :
                yield pll
            else :
                yield ( - wgt / scale )

        return

    def __str__( self ) :
        return "Uniform error distribution"

