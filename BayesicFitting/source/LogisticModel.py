import numpy as numpy
from astropy import units
import math
from . import Tools
from .Tools import setAttribute as setatt

from .NonLinearModel import NonLinearModel

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
__version__ = "2.5.3"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Perpetual Beta"


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
#  *    2018 - 2020 Do Kester


class LogisticModel( NonLinearModel ):
    """
    Logistic Model.

        f( x:p ) = p_0 / ( 1 + exp( ( x - p_1 ) / p_2 ) )

    where

        p_0 : amplitude
        p_1 : center
        p_2 : slope

    The parameters are initialized at {1.0, 0.0, 1.0}.

    Examples
    --------
    >>> lm = LogisticModel( )
    >>> print( lm )
    Logistic: f( x:p ) = p_0 / ( 1 + exp( ( p_1 - x ) / p_2 ) )
    >>> print( lm.npars )
    3
    >>> print( lm( numpy.arange( 11 ) - 5 ) )
    [  3.72665317e-06   3.35462628e-04   1.11089965e-02   1.35335283e-01
       6.06530660e-01   1.00000000e+00   6.06530660e-01   1.35335283e-01
       1.11089965e-02   3.35462628e-04   3.72665317e-06]

    Attributes from Model
    ---------------------
        npchain, parameters, stdevs, xUnit, yUnit

    Attributes from FixedModel
    --------------------------
        npmax, fixed, parlist, mlist

    Attributes from BaseModel
    --------------------------
        npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames

    """

    def __init__( self, copy=None, **kwargs ):
        """
        Logistic response model.

        Number of parameters is 3.

        Parameters
        ----------
        copy : LogisticModel
            to be copied
        fixed : None or dictionary of {int:float|Model}
            int         index of parameter to fix permanently.
            float|Model values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
            See: @FixedModel

        """
        names = ["amplitude", "center", "slope"]
        param = [1.0,0.0,1.0]
        super( LogisticModel, self ).__init__( 3, copy=copy, params=param,
                    names=names, **kwargs )

    def copy( self ):
        """ Copy method.  """
        return LogisticModel( copy=self )

    def baseResult( self, xdata, params ):
        """
        Returns the result of the model function.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        x = ( params[1] - xdata ) / params[2]
        res = params[0] / ( 1 + numpy.exp( x ) )
        return res

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            values for the parameters.
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        partial = numpy.ndarray( ( Tools.length( xdata ), self.npbase ) )
        a = params[0]
        s = params[2]
        x = ( params[1] - xdata )
        e = numpy.exp( x / s )
        f = 1 / ( 1 + e )
        f2 = f * f

        parts = { 0 : ( lambda: f ),
                  1 : ( lambda: -a / s * f2 * e ),
                  2 : ( lambda: a * x / ( s * s ) * f2 * e ) }

        if parlist is None :
            parlist = range( self.npmax )

        for k,kp in enumerate( parlist ) :
            partial[:,k] = parts[kp]()

        return partial

    def baseDerivative( self, xdata, params ) :
        """
        Return the derivative df/dx at each xdata (=x).

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        x = ( params[1] - xdata ) / params[2]
        e = numpy.exp( x )

        return ( params[0] / params[2] ) * e / numpy.square( 1 + e )

#        return - ( params[0] / params[2] ) * e / numpy.square( 1 + e )

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return str( "Logistic: f( x:p ) = p_0 / ( 1 + exp( ( p_1 - x ) / p_2 ) )" )

    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.

        """
        return self.yUnit if k == 0 else self.xUnit


