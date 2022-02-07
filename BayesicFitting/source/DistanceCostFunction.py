import numpy as numpy
import math

from .ErrorDistribution import ErrorDistribution
from .LogFactorial import logFactorial
from .Formatter import formatter as fmt
from .Tools import setAttribute as setatt

__author__ = "Do Kester"
__year__ = 2022
__license__ = "GPL3"
__version__ = "3.0.0"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Alpha"

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
#  *    2019 - 2022 Do Kester


class DistanceCostFunction( ErrorDistribution ):
    """
    To calculate a distance based cost function

    For one observation with n counts it holds

        f( d ) = exp( -SUM( d / s ) )

    where d are the distances and s is the scale

    The function is mostly used to calculate the likelihood L of
    traveling-salesman-like problems

    Author       Do Kester.

    """

    LOG2 = math.log( 2.0 )
    LOG2P1 = math.log( 2.0 ) + 1

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, copy=None ):
        """
        Constructor.

        Parameters
        ----------
        copy : DistanceCostFunction
            distribution to be copied.

        """
        super( ).__init__( copy=copy )

    def copy( self ):
        """ Return copy of this.  """
        return DistanceCostFunction( copy=self )

    def acceptWeight( self ):
        """
        True if the distribution accepts weights.
        Always false for this distribution.
        """
        return True


    #  *********LIKELIHOODS***************************************************
    def logLikelihood_alt( self, problem, allpars ):
        """
        Return the negative sum of the distances.

        Parameters
        ----------
        problem : Problem
            to be solved
        allpars : array_like
            list of all parameters in the problem

        """
        self.ncalls += 1

        return -numpy.sum( problem.result( allpars ) )


    def logLdata( self, problem, allpars ):
        """
        Return the individual distances (multiplied by the weights).

        Parameters
        ----------
        problem : Problem
            to be solved
        allpars : array_like
            list of all parameters in the problem

        """
        return -problem.result( allpars )

    def partialLogL( self, model, param, fitIndex ):
        """
        Does not work for this class

        Parameters
        ----------
        model : Model
            model to calculate mock data
        param : array_like
            parameters of the model
        fitIndex : array_like
            indices of the params to be fitted
        """
        pass

    def __str__( self ) :
        return "Distance Cost Function"

