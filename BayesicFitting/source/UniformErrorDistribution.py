import numpy as numpy
import math

from .ScaledErrorDistribution import ScaledErrorDistribution

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
#  * The GPL3 license can be found at <http://www.gnu.org/licenses/>.
#  *
#  *    2018        Do Kester


class UniformErrorDistribution( ScaledErrorDistribution ):
    """
    To calculate a Uniform likelihood, eg. for digitization noise.

    For one residual, x, it holds

        L( x ) = 1 / ( 2 * s )    if |x| < s
                 0                otherwise

    where s is the scale.
    s is a hyperparameter, which might be estimated from the data.

    The variance of this function is &sigma;^2 = s / 6.
    See: toSigma()

    The function is mostly used to calculate the likelihood L over N residuals,
    or easier using log likelihood, logL.

        logL = -log( 2 * s ) * N

    Note that it is required that <b>all</b> residuals are smaller than s,
    otherwise the logL becomes -inf.

    Using weights this becomes:

        logL = -log( 2 * s ) * &sum; w


    Author       Do Kester.

    """
    SQRT2 = math.sqrt( 2 )
    LGSQ2 = math.log( SQRT2 )
    LOG2 = math.log( 2.0 )


    #  *********CONSTRUCTORS***************************************************
    def __init__( self, scale=1.0, limits=None, copy=None ) :
        """
        Constructor of Uniform Distribution.

        Parameters
        ----------
        scale : float
            noise scale
        limits : None or list of 2 floats [low,high]
            None    no limits implying fixed scale
            low     low limit on scale (needs to be >0)
            high    high limit on scale
            when limits are set, the scale is *not* fixed.
        copy : UniformErrorDistribution
            distribution to be copied.

        """
        super( UniformErrorDistribution, self ).__init__( scale=scale,
                limits=limits, copy=copy )

    def copy( self ):
        """ Return copy of this.  """
        return UniformErrorDistribution( copy=self )

    #  *********DATA & WEIGHT***************************************************
    def acceptWeight( self ):
        """
        True if the distribution accepts weights.
        Always true for this distribution.
        """
        return True

    def getScale( self, problem, allpars=None ) :
        """
        Return the noise scale

        Parameters
        ----------
        problem : Problem
            to be solved
        allpars : array_like
            None take parameters from problem.model
            list of all parameters in the problem
        """
        res = self.getResiduals( problem, allpars=allpars )
        return numpy.max( numpy.abs( res ) )

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
    def logLikelihood_alt( self, problem, allpars ) :
        """
        Return the log( likelihood ) for a Uniform distribution.

        Alternate calculation.

        Outside the range the likelihood is zero, so the logL should be -inf.
        However for computational reasons the maximum negative value is returned.

        Parameters
        ----------
        problem : Problem
            to be solved
        allpars : array_like
            parameters of the problem

        """
        self.ncalls += 1

        scale = allpars[-1]

        ares = numpy.abs( problem.residuals( allpars[:-1] ) )

        if all( ares < scale ) :
            return - math.log( 2 * scale ) * problem.sumweight

        return -math.inf

    def logLdata( self, problem, allpars, mockdata=None ) :
        """
        Return the log( likelihood ) for each residual

        logL = sum( logLdata )

        Parameters
        ----------
        problem : Problem
            to be solved
        allpars : array_like
            list of all parameters in the problem
        mockdata : array_like
            as calculated by the model

        """
        if mockdata is None :
            mockdata = problem.result( allpars[:-1] )
        scale = allpars[-1]
        ares = numpy.abs( problem.ydata - mockdata )

        lld = numpy.where( ares < scale, -math.log( 2 * scale ), -math.inf )
        if problem.weights is not None :
            lld *= problem.weights
        return lld


    def partialLogL_alt( self, problem, allpars, fitIndex ) :
        """
        Return the partial derivative of log( likelihood ) to the parameters.

        Parameters
        ----------
        problem : Problem
            to be solved
        allpars : array_like
            parameters of the problem
        fitIndex : array_like
            indices of parameters to be fitted

        """
        dL = numpy.zeros( len( fitIndex ), dtype=float )
        if fitIndex[-1] == -1 :
            dL[-1] = -problem.sumweight / allpars[-1]
        return dL

    def nextPartialData( self, problem, allpars, fitIndex, mockdata=None ) :
        """
        Return the partial derivative of elements of the log( likelihood )
        to the parameters.

        Parameters
        ----------
        problem : Problem
            to be solved
        allpars : array_like
            parameters of the problem
        fitIndex : array_like
            indices of parameters to be fitted
        mockdata : array_like
            as calculated by the model

        """
        scale = allpars[-1]
        pll = numpy.zeros_like( problem.ydata )
        if problem.weights is not None :
            wgt = problem.weights
        else :
            wgt = numpy.ones_like( problem.ydata )

        for k in fitIndex :
            if k >= 0 :
                yield pll
            else :
                yield ( - wgt / scale )

        return

    def __str__( self ) :
        """
        Return a string representation of this class.
        """
        return "Uniform error distribution"

