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
#  *    2015 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2017 Do Kester

class EtalonModel( NonLinearModel ):
    """
    Sinusoidal Model with drifting frequency.
    .. math::
        f( x:p ) = p_0 / ( 1.0 + p_1 * sin^2( \pi p_2 x + p_3 ) )

    where :math:`p_0` = amplitude, :math:`p_1` = finesse,
    :math:`p_2` = periods per wavenumber and :math:`p_3` = phase,
    As always x = input; it is in wavenumbers

    The parameters are initialized at {1.0, 1.0, 1.0, 0.0}. It is a non-linear model.

    The finesse should be positive. However, solutions where -1 < p_1 < 0 are equivalent
    to a solution with parameters set as:
        p_0 /= ( 1 + p_1 )
        p_1 /= -( 1 + p_1 )
        p_3 += pi/2             # 90 degree phase shift

    A finesse below -1 causes infinities.

    Examples TBC
    --------
    >>> fpm = EtalonModel( )
    >>> print( fpm.npchain )
    4
    >>> pars = [1.0, 30.0, 1.0, 0.0]
    >>> fpm.parameters = pars
    >>> print( fpm( numpy.arange( 101, dtype=float ) ) )     # etalon with 10 periods

    """

    def __init__( self, copy=None, **kwargs ):
        """
        Etalon model.

        Number of parameters is 4.

        Parameters
        ----------
        copy : EtalonModel
            to be copied
        fixed : dictionary of {int:float}
            int     list if parameters to fix permanently. Default None.
            float   list of values for the fixed parameters.
            Attribute fixed can only be set in the constructor.

        """
        param = [1.0, 1.0, 1.0, 0.0]
        names = ["amplitude", "finesse", "period", "phase"]
        super( EtalonModel, self ).__init__( 4, copy=copy, params=param,
                    names=names, **kwargs )


    def copy( self ):
        """ Copy method.  """
        return EtalonModel( copy=self )

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
        x = math.pi * xdata * params[2] + params[3]
        sx = numpy.sin( x )
        return params[0] / ( 1.0 + params[1] * sx * sx )

    def baseDerivative( self, xdata, params ):
        """
        Returns the derivative of f to x (df/dx) at the input values.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        x = math.pi * xdata * params[2] + params[3]
        sx = numpy.sin( x )
        dd = 1 + params[1] * sx * sx
        dd *= dd
        return - 2 * math.pi * params[0] * params[1] * params[2] * sx * numpy.cos( x ) / dd


    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input values.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        np = self.npbase if parlist is None else len( parlist )
        partial = numpy.ndarray( ( Tools.length( xdata ), np ) )

        x = math.pi * xdata * params[2] + params[3]
        sx = numpy.sin( x )
        s2 = sx * sx
        dd = 1.0 / ( 1 + params[1] * s2 )
        d2 = dd * dd
        p3 = - 2 * params[0] * params[1] * sx * numpy.cos( x ) * d2

        parts = { 0 : ( lambda: dd ),
                  1 : ( lambda: - params[0] * s2 * d2 ),
                  2 : ( lambda: math.pi * xdata * p3 ),
                  3 : ( lambda: p3 ) }

        if parlist is None :
            parlist = range( self.npmax )

        for k,kp in enumerate( parlist ) :
            partial[:,k] = parts[kp]()

        return partial

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return ( "Etalon: f( x:p ) = p_0 / ( 1 + p_1 * sin^2( PI * x * p_2 + p_3 ) )" )

    def baseParameterUnit( self, k ):
        """
        Return the name of a parameter.

        Parameters
        ----------
        k : int
            the kth parameter.

        """
        if k == 0:
            return self.yUnit
        if k == 1:
            return units.Unit( "" )
        if k == 2:
            return units.Unit( units.si.rad ) / self.xUnit
        if k == 3:
            return units.Unit( units.si.rad )
        return self.yUnit


