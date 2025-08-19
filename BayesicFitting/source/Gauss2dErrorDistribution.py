import numpy as numpy
import math

from .GaussErrorDistribution import GaussErrorDistribution
from .Formatter import formatter as fmt

__author__ = "Do Kester"
__year__ = 2025
__license__ = "GPL3"
__version__ = "3.2.4"
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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2017 - 2025 Do Kester


class Gauss2dErrorDistribution( GaussErrorDistribution ):
    """
    To calculate a Gauss likelihood in case of errors in X and Y

    For one residual in x and y it holds

     L = 1 / ( 2 &pi; &radic; det ) exp( - 0.5 ( x / s )^2 )

    where s is the scale.
    s is a hyperparameter, which might be estimated from the data.

    The scale s is also the square root of the variance of this error distribution.

    The function is mostly used to calculate the likelihood L over N residuals,
    or easier to use log likelihood, logL.

     logL = log( N / ( &radic;( 2 &pi; ) s )  ) - 0.5 &sum;( x / s )^2

    Using weights this becomes:

     logL = log( &sum;( w ) / ( &radic;( 2 &pi; ) s )  ) - 0.5 &sum;( w ( x / s )^2 )


    Author       Do Kester.

    """
    LOG2PI = math.log( 2 * math.pi )


    #  *********CONSTRUCTORS***************************************************
    def __init__( self, scale=1.0, limits=None, copy=None ):
        """
        Default Constructor.

        Parameters
        ----------
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
        super( Gauss2dErrorDistribution, self ).__init__(  scale=scale, limits=limits, copy=copy )

    def copy( self ):
        """ Return copy of this.  """
        return Gauss2dErrorDistribution( copy=self )

    def TBDgetScale( self, problem, allpars=None ) :
        """
        Return the noise scale.

        Parameters
        ----------
        problem : Problem
            to be solved
        allpars : array_like
            None take parameters from problem.model
            list of all parameters in the problem
        """
        return self.getGaussianScale( problem, allpars=allpars )

    def updateDeterminant( self, problem, scale  ) :
        """
        Update the determinant of the covar matrix with scale

        Parameters
        ----------
        problem : ErrorsInXandYProblem
            problem at hand
        scale : float
            present vale for the cale
        """
        s2 = scale * scale
        return  problem.determinant + s2 * ( problem.varxx + problem.varyy + s2 )


    #  *********LIKELIHOODS***************************************************
    def logLikelihood_alt( self, problem, allpars ) :
        """
        Return the log( likelihood ) for a Gaussian distribution.

        Alternate calculation

        Parameters
        ----------
        problem : Problem
            to be solved
        allpars : array_like
            list of all parameters in the problem

        """
        self.ncalls += 1

        det = self.updateDeterminant( problem, allpars[-1] )

        chisq = numpy.sum( problem.weightedResSq( allpars ) )

        if problem.weights is None :
            if det.size == 1 : 
                norm = problem.ndata * ( self.LOG2PI + math.log( det ) )
            else :
                norm = problem.ndata * self.LOG2PI + numpy.sum( numpy.log( det ) )  
        else :
            norm = numpy.sum( problem.weights * ( self.LOG2PI + numpy.log( det ) ) ) 

        return -0.5 * ( norm + chisq )

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
        det = self.updateDeterminant( problem, allpars[-1] )

        rot2 = problem.weightedResSq( allpars, mockdata=mockdata )

        norm = self.LOG2PI + numpy.log( det )
        if problem.weights is not None :
            norm *= problem.weights

        return -0.5 * ( norm + rot2 )


    def partialLogL_alt( self, problem, allpars, fitIndex ) :
        """
        Return the partial derivative of log( likelihood ) to the parameters in fitIndex.

        Alternate calculation

        Parameters
        ----------
        problem : Problem
            to be solved.
        allpars : array_like
            (hyper)parameters of the problem
        fitIndex : array_like
            indices of parameters to be fitted

        """

        self.nparts += 1                    ## counts calls to partialLogL

        modelscale = allpars[-1]
        det = self.updateDeterminant( problem, modelscale )

        ( rot2, res, res2 ) = problem.weightedResSq( allpars, extra=True )

        dM = problem.partial( allpars[:-1] )

        dL = numpy.zeros( len( fitIndex ), dtype=float )
        print( "G2dED   ", rot2.shape, res.shape, res2.shape, dM.shape, dL.shape ), 
        print( fmt( dM, max=None ) )
        print( "LLD    ", fmt( res, max=None ) )

        i = 0
        for  k in fitIndex :
            if k < 0 :              # model accuracy
                wgt = 1 if problem.weights is None else problem.weights
                dL[-1] = - modelscale / det * numpy.sum( ( problem.varxx + problem.varyy +
                    2 * modelscale * modelscale ) * ( wgt - rot2 ) + res2 ) 
            else :
                dL[i] = numpy.sum( res * dM[:,k] )
                i += 1

        return dL


    def nextPartialData( self, problem, allpars, fitIndex, mockdata=None ) :
        """
        Return the partial derivative all elements of the log( likelihood )
        to the parameters in fitIndex.

        Parameters
        ----------
        problem : Problem
            to be solved
        allpars : array_like
            (hyper)parameters of the problem
        fitIndex : array_like of int
            indices of allpars to fit
        mockdata : array_like
            as calculated for the problem
        """
        ( rot2, res, res2 ) = problem.weightedResSq( allpars, mockdata=mockdata, extra=True )

        dM = problem.partial( allpars[:problem.npars] )

##      TBD import mockdata into partial
#        dM = problem.partial( param, mockdata=mockdata )

        modelscale = allpars[-1]
        det = self.updateDeterminant( problem, modelscale )

        for  k in fitIndex:
            if k >= 0 :                         ## the parameters
                yield ( res * dM[:,k] )
            else :                              ## the scale
                wgt = 1.0 if problem.weights is None else problem.weights
                yield - modelscale / det * ( ( problem.varxx + problem.varyy +
                        2 * modelscale * modelscale ) * ( wgt - rot2 ) + res2 )

        return

    def _TBDhessianLogL( self, problem, allpars, fitIndex ) :
        """
        Return the hessian of log( likelihood ) to the parameters in fitIndex.

        The hessian is a matrix containing the second derivatives to each
        of the parameters.

             hessian = d^2 logL / dp_i dp_k

        Parameters
        ----------
        problem : Problem
            to be solved
        allpars : array_like
            (hyper)parameters of the problem
        fitIndex : array_like of int
            indices of allpars to fit
        """
        self.nparts += 1                    ## counts calls to partialLogL

        nh = len( fitIndex )
        np = problem.npars
        param = allpars[:np]
        scale = allpars[np]
        s2 = scale * scale

        fi = fitIndex if fitIndex[-1] != np else fitIndex[-1:]

        nf = len( fi )
        design = problem.partial( param )[:,fi]
        design = design.transpose()
        deswgt = design
        if problem.hasWeights() :
            deswgt *= problem.weights

        hessian = numpy.zeros( ( nh, nh ), dtype=float )
        hessian[:nf,:nf] = numpy.inner( design, deswgt ) / s2

        if fitIndex[-1] == np :
            hessian[nf,nf] = 2 * ( problem.ndata - nf ) / s2

        return hessian

    def __str__( self ) :
        return "Gauss2d error distribution"
