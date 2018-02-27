import numpy as numpy
import scipy
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


class CauchyErrorDistribution( ScaledErrorDistribution ):
    """
    To calculate a Cauchy or Lorentz likelihood.
    ..math ::
        f( x ) = s / ( \pi * ( s^2 + x^2 ) )

    where x = residual and s = scale

    The function is mostly used to calculate the likelihood L, or easier
    to use log likelihood, logL.
    .. math::
        logL = N ( \log( s ) - \log( \pi ) ) - \sum( \log( x^2 + s^2 ) )

    The use of weights is not possible in this error distribution.

    s is a hyperparameter, which might be estimated from the data.

    Author       Do Kester.

    """

    LOGPI = math.log( math.pi )

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, xdata, data, weights=None, scale=1.0, limits=None,
                  copy=None ):
        """
        Default Constructor.

        Parameters
        ----------
        xdata : array_like
            input data fro the model (independent data)
        data : array_like
            data to be fitted (dependent data)
        weights : array_like
            weights to be used (no weights are possible in Cauchy)
        scale : float
            noise scale
        limits : None or list of 2 floats [low,high]
            None : no limits implying fixed scale
            low     low limit on scale (needs to be >0)
            high    high limit on scale
            when limits are set, the scale is *not* fixed.
         copy : CauchyErrorDistribution
            distribution to be copied.

        """
        if weights is not None:
            raise ValueError( "Weights are not possible in Cauchy distributions" )

        super( CauchyErrorDistribution, self ).__init__( xdata, data,
                scale=scale, limits=limits, copy=copy )

    def copy( self ):
        """ Return copy of this.  """
        return CauchyErrorDistribution( self.xdata, self.data, copy=self )

    def __setattr__( self, name, value ):
        """
        Set attributes.

        """
        if name == "res2" :
            object.__setattr__( self, name, value )
        else :
            super( CauchyErrorDistribution, self ).__setattr__( name, value )

    def acceptWeight( self ):
        """
        True if the distribution accepts weights.
        False for this distribution.
        """
        return False

    def getScale( self, model ) :
        """
        Return the noise scale as calculated from the residuals.

        Parameters
        ----------
        model : Model
            the model involved
        """
        res = self.getResiduals( model )
        self.res2 = res * res

        scale = scipy.optimize.bisect( self.funct, 0.001, 100.0 )
        return scale

    def funct( self, scale ) :
        return ( numpy.sum( numpy.log( self.res2 + scale * scale ) ) -
                self.sumweight * ( 2 * math.log( scale ) + math.sqrt( 2.0 ) ) )

    #  *********LIKELIHOODS***************************************************
    def logLikelihood( self, model, allpars ):
        """
        Return the log( likelihood ) for a Cauchy distribution.
        Cauchy distr : f( x ) = s / ( pi * ( s^2 + x^2 ) )

        where x = residual and s = scale

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
        res2 = numpy.square( self.getResiduals( model, allpars[:np] ) )
        return ( self.ndata * ( math.log( scale ) - self.LOGPI ) -
                 numpy.sum( numpy.log( res2 + scale * scale ) ) )

    def partialLogL( self, model, allpars, fitIndex ) :
        """
        Return the partial derivative of log( likelihood ) to the parameters
        in fitIndex.

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
        res = self.getResiduals( model, allpars[:np] )
        r2s = res * res + scale * scale
        dM = model.partial( self.xdata, allpars[:np] )

        dL = numpy.zeros( len( fitIndex ), dtype=float )
        i = 0
        for k in fitIndex :
            if k < np :
                dL[i] = 2 * numpy.sum( res * dM[:,k] / r2s )
            else :
                dL[i] = self.ndata / scale - numpy.sum( 2 * scale / r2s )
            i += 1
        return dL

    def __str__( self ) :
        return "Cauchy error distribution"

