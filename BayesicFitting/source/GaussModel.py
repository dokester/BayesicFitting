import numpy as numpy
from astropy import units
import math
from . import Tools
from .NonLinearModel import NonLinearModel

__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"


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
#  *    2003 - 2014 Do Kester, SRON (JAVA code)
#  *    2016 - 2017 Do Kester


class GaussModel( NonLinearModel ):
    """
    Gaussian Model.
    ..math::
        f( x:p ) = p_0 * \exp( -0.5 * ( ( x - p_1 ) / p_2 )^2 )

        p_0 = amplitide; p_1 = center;  p_2 = width

    The parameters are initialized at {1.0, 0.0, 1.0}.
    Parameter 2 ( sigma ) is always kept stricktly positive ( >0 ).

    Examples
    --------
    >>> gauss = GaussModel( )
    >>> print( gauss )
    Gauss: f( x:p ) = p_0 * exp( -0.5 * ( ( x - p_1 ) / p_2 )^2 )
    >>> print( gauss.getNumberOfParameters( ) )
    3
    >>> print( gauss( numpy.arange( 11 ) - 5 ) )
    [  3.72665317e-06   3.35462628e-04   1.11089965e-02   1.35335283e-01
       6.06530660e-01   1.00000000e+00   6.06530660e-01   1.35335283e-01
       1.11089965e-02   3.35462628e-04   3.72665317e-06]


    """

    def __init__( self, copy=None, **kwargs ):
        """
        Gaussian model.

        Number of parameters is 3.

        Parameters
        ----------
        copy : GaussModel
            to be copied
        fixed : dictionary of {int:float}
            int     list if parameters to fix permanently. Default None.
            float   list of values for the fixed parameters.
            Attribute fixed can only be set in the constructor.

        """
        names = ["amplitude", "center", "width"]
        param = [1.0,0.0,1.0]
        super( GaussModel, self ).__init__( 3, copy=copy, params=param,
                    names=names, **kwargs )
        if copy is None :
            self.posIndex = [2]
            self.nonZero = [2]

    def copy( self ):
        """ Copy method.  """
        return GaussModel( copy=self )

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
        s = 1.0 / params[2]
        x = ( xdata - params[1] ) * s
        res = params[0] * numpy.exp( -0.5 * x * x )
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
        s = 1 / params[2]
        x = ( xdata - params[1] ) * s
        e = numpy.exp( -0.5 * x * x )

        parts = { 0 : ( lambda: e ),
                  1 : ( lambda: a * e * x * s ),
                  2 : ( lambda: a * e * x * x * s ) }

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
        dx = ( params[1] - xdata ) / ( params[2] * params[2] )

        return self.baseResult( xdata, params ) * dx

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return str( "Gauss: f( x:p ) = p_0 * exp( -0.5 * ( ( x - p_1 ) / p_2 )^2 )" )

    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.

        """
        return self.yUnit if k == 0 else self.xUnit


