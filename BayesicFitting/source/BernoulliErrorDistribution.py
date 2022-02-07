import numpy as numpy
import math

from .Formatter import formatter as fmt
from .Formatter import fma
from .ErrorDistribution import ErrorDistribution

__author__ = "Do Kester"
__year__ = 2022
__license__ = "GPL3"
__version__ = "3.0.0"
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
#  *    2018 - 2022 Do Kester


class BernoulliErrorDistribution( ErrorDistribution ):
    """
    To calculate a Bernoulli likelihood for categorical True/False data.

    For one residual, x, it holds

        f( x ) = x          if d is True
                 1 - x      if d is False

    where x needs to be between [0,1]; use the logistic function f(x) = 1/(1+exp(-x)
    if necessary. And d is true if the residual belongs to the intended category.

    The function is mostly used to calculate the likelihood L, or easier
    to use log likelihood, logL.

        logL = log( x ) if d else log( 1 - x )

    Author       Do Kester.

    """
    SQRT2 = math.sqrt( 2 )
    LGSQ2 = math.log( SQRT2 )
    LOG2 = math.log( 2.0 )


    #  *********CONSTRUCTORS***************************************************
    def __init__( self, copy=None ) :
        """
        Constructor of Bernoulli Distribution.

        Parameters
        ----------
        copy : BernoulliErrorDistribution
            distribution to be copied.
        """
        super( BernoulliErrorDistribution, self ).__init__( copy=copy )

    def copy( self ):
        """ Return copy of this.  """
        return BernoulliErrorDistribution( copy=self )

    #  *********DATA & WEIGHT***************************************************
    def acceptWeight( self ):
        """
        True if the distribution accepts weights.
        Always true for this distribution.
        """
        return False

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
            the scale of this Bernoulli distribution.
        """
        return scale * 2 / math.sqrt( 12 )

    #  *********LIKELIHOODS***************************************************
    def logLikelihood_alt( self, problem, allpars ) :
        """
        Return the log( likelihood ) for a Bernoulli distribution.

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

        return numpy.sum( self.logLdata( problem, allpars ) )

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
            mockdata = problem.result( allpars )

        if problem.model.lastndout == 1 :
            return numpy.log( numpy.where( problem.ydata == 0, mockdata, 1 - mockdata ) )

        lld = numpy.zeros( len( problem.ydata ), dtype=float )

        for k in range( problem.model.lastndout ) :
            lld += numpy.where( problem.ydata == k, mockdata[:,k], 0 )

        return numpy.log( lld )

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

        mock = problem.result( allpars )
        dM = problem.partial( allpars )
        dLdM = numpy.zeros_like( mock )

        if problem.model.lastndout == 1 :
            dLdM = 1.0 / numpy.where( problem.ydata == 0, mock, 1 - mock )
            dL = numpy.sum( numpy.multiply( dLdM, dM.T ), axis=1 )
            return dL

        for k in range( problem.model.lastndout ) :
            q = numpy.where( problem.ydata == k )
            dLdM[q,k] = 1.0 / mock[q,k]

        dL = numpy.tensordot( dLdM, numpy.asarray( dM ), axes=([0,1],[1,0]) )

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
        if mockdata is None :
            mock = problem.result( allpars )
        else :
            mock = mockdata

        dM = problem.partial( allpars )
        dLdM = numpy.zeros_like( mock )

        if problem.model.lastndout == 1 :
            dLdM = 1.0 / numpy.where( problem.ydata == 0, mock, mock - 1 )
            dL = numpy.multiply( dLdM, dM.T )

        else :
            for k in range( problem.model.lastndout ) :
                q = numpy.where( problem.ydata == k )
                dLdM[q,k] = 1.0 / mock[q,k]

            dL = numpy.tensordot( dLdM, numpy.asarray( dM ), axes=([0,1],[1,0]) )

#        r0 = numpy.log( numpy.where( problem.ydata == 0, mock - 0.001, 1 - mock + 0.001 ) )
#        r1 = numpy.log( numpy.where( problem.ydata == 0, mock + 0.001, 1 - mock - 0.001 ) )


        for k in fitIndex :
            yield dL[k]

        return

    def __str__( self ) :
        return "Bernoulli error distribution"

