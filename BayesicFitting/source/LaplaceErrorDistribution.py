import numpy as numpy
import math

from .ScaledErrorDistribution import ScaledErrorDistribution
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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2010 - 2014 Do Kester, SRON (Java code)
#  *    2017        Do Kester


class LaplaceErrorDistribution( ScaledErrorDistribution ):
    """
    To calculate a Laplace likelihood.

    For one residual, x, it holds
    .. math::
        f( x ) = 1 / ( 2 s ) exp( - |x| / s )

    where s is the scale.
    s is a hyperparameter, which might be estimated from the data.

    The variance of this function is :math:`\sigma^2 = 2 s ^ 2`.
    See: toSigma()

    The function is mostly used to calculate the likelihood L, or easier
    to use log likelihood, logL.
    .. math::
        logL = log( N / ( 2 s ) ) - \sum( |x| / s  )

    Using weights this becomes:
    .. math::
        logL = log( \sum( w ) / ( 2 s ) ) - \sum( w |x| / s  )

    Using this error distribution results in median-like solutions.

    Author       Do Kester.

    """
    SQRT2 = math.sqrt( 2 )
    LGSQ2 = math.log( SQRT2 )
    LOG2 = math.log( 2.0 )


    #  *********CONSTRUCTORS***************************************************
    def __init__( self, xdata, data, weights=None, scale=1.0, limits=None,
                  copy=None ) :
        """
        Constructor of Laplace Distribution.

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

        copy : LaplaceErrorDistribution
            distribution to be copied.
        """
        super( LaplaceErrorDistribution, self ).__init__( xdata, data,
               weights=weights, scale=scale, limits=limits, copy=copy )

    def copy( self ):
        """ Return copy of this.  """
        return LaplaceErrorDistribution( self.xdata, self.data, copy=self )

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
            the scale of this Laplace distribution.
        """
        return scale * math.sqrt( 2.0 )

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
        res = self.getResiduals( model, allpars[:np] )
        sumres = self.getSumRes( res, scale )
        return - self.sumweight * ( self.LOG2 + math.log( scale ) ) - sumres

    def getScale( self, model ) :
        """
        Return the noise scale

        Parameters
        ----------
        model : Model
            the model involved
        """
        sumres = self.getSumRes( self.getResiduals( model ), 1.0 )
        return sumres / self.sumweight


    def getSumRes( self, residual, scale ):
        """
        Return the sum of the absolute values of the normalized residuals.

        ..math ::
            \sum ( | res | / scale )

        Parameters
        ----------
        residual : array_like
            the residuals
        scale : float
            the noise scale

        """
        if self.weights is not None :
            residual = residual * self.weights
        return numpy.sum( numpy.abs( residual ) ) / scale

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
            indices of parameters to be fitted

        """
        self.nparts += 1
        np = model.npchain
        scale = allpars[np]

        dM = model.partial( self.xdata, allpars[:np] )
        dL = numpy.zeros( len( fitIndex ), dtype=float )
        res = self.getResiduals( model, allpars[:np] )
        wgt = numpy.ones_like( res, dtype=float ) if self.weights is None else self.weights
        wgt = numpy.copysign( wgt, res )

        i = 0
        for k in fitIndex :
            if k < np :
                dL[i] = numpy.sum( wgt * dM[:,k] )
            else :
                dL[i] = self.getSumRes( res, scale ) - self.sumweight
            i += 1
        return dL / scale

    def __str__( self ) :
        return "Laplace error distribution"

