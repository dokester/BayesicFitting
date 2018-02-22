import numpy as numpy
from . import Tools
from .NonLinearModel import NonLinearModel

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
#  *    2007 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2017 Do Kester

class ExpModel( NonLinearModel ):
    """
    Exponential Model.
    .. math::
        f( x:p ) = p_0 * exp( p_1 * x )

    where p_0 = amplitude, p_1 = slope and
    As always x = input.

    The parameters are initialized at {1.0, -1.0}. It is a non-linear model.

    Beware of a positive 2nd parameter; when positive the model is going off
    to Infinity quite quickly.


    Examples
    --------
    >>> em = ExpModel( )
    >>> print( em.getNumberOfParameters( ) )
    2

    Category:    mathematics/Fitting

    """
    def __init__( self, copy=None, **kwargs ):
        """
        Exponential model.
        <br>
        Number of parameters is 2.

        Parameters
        ----------
        copy : ExpModel
            to be copied

        """
        param = [1.0,-1.0]
        names = ["amplitude","slope"]
        super( ExpModel, self ).__init__( 2, copy=copy, params=param,
                names=names, **kwargs )

    def copy( self ):
        """ Copy method.  """
        return ExpModel( copy=self )

    def baseResult( self, xdata, params ):
        """
        Returns the result of the model function.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result
        params : array_like
            values for the parameters

        """
        return numpy.multiply( numpy.exp( numpy.multiply( params[1], xdata ) ), params[0] )

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result
        params : array_like
            values for the parameters
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        np = self.npbase if parlist is None else len( parlist )
        partial = numpy.ndarray( ( Tools.length( xdata ), np ) )

        e = numpy.exp( params[1] * xdata )

        parts = { 0 : ( lambda: e ),
                  1 : ( lambda: params[0] * e * xdata ) }

        if parlist is None :
            parlist = range( self.npmax )

        for k,kp in enumerate( parlist ) :
            partial[:,k] = parts[kp]()

        return partial

    def baseDerivative( self, xdata, params ):
        """
        Returns the derivative df/dx at the input value.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result
        params : array_like
            values for the parameters

        """
        return numpy.multiply( params[1], self.baseResult( xdata, params ) )

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return str( "Exp: f( x:p ) = p_0 * exp( p_1 * x )" )

    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.
        Parameters: k    parameter number.

        """
        if k == 0:
            return self.yUnit
        return self.xUnit ** ( -1 )


