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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2017 Do Kester

class SineModel( NonLinearModel ):
    """
    Sinusoidal Model.
    .. math::
        f( x:p ) = p_1 * \cos( 2 * \pi * p_0 * x ) + p_2 * \sin( 2 * \pi * p_0 * x )

    where :math:`p_0` = frequency, :math:`p_1` = amplitude cosine and
    :math:`p_2` = amplitude sine. As always x = input.

    The parameters are initialized at {1.0, 1.0, 1.0}. It is a non-linear model.

    Examples
    --------
    >>> sine = SineModel( )
    >>> print( sine.npchain )
    3
    >>> pars = [0.1, 0.0, 1.0]
    >>> sine.parameters = pars
    >>> print( sine( numpy.arange( 11, dtype=float ) ) )    # One sine period
    >>> pars = [0.1, 1.0, 0.0]
    >>> sine.parameters = pars
    >>> print( sine( numpy.arange( 11, dtype=float ) ) )     # One cosine period


    """
    TWOPI = 2 * math.pi

    def __init__( self, copy=None, **kwargs ):
        """
        Sinusiodal model.

        Number of parameters is 3.

        Parameters
        ----------
        copy : SineModel
            model to copy
        fixed : dictionary of {int:float}
            int     list if parameters to fix permanently. Default None.
            float   list of values for the fixed parameters.
            Attribute fixed can only be set in the constructor.

        """
        param = [1.0, 1.0, 1.0]
        names = ["frequency", "cosamp", "sinamp"]

        super( SineModel, self ).__init__( 3, copy=copy, params=param,
                        names=names, **kwargs )

    def copy( self ):
        """ Copy method.  """
        return SineModel( copy=self )

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
        x = self.TWOPI * xdata * params[0]
        result = params[1] * numpy.cos( x ) + params[2] * numpy.sin( x )
        return result

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

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

        #  disregard count
        x = self.TWOPI * xdata
        xf = x * params[0]
        cxf = numpy.cos( xf )
        sxf = numpy.sin( xf )

        parts = { 0 : ( lambda: x * params[2] * cxf - x * params[1] * sxf ),
                  1 : ( lambda: cxf ),
                  2 : ( lambda: sxf ) }

        if parlist is None :
            parlist = range( self.npmax )

        for k,kp in enumerate( parlist ) :
            partial[:,k] = parts[kp]()

        return partial

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
        x = self.TWOPI * xdata * params[0]
        df = self.TWOPI * params[0] * ( params[2] * numpy.cos( x ) - params[1] * numpy.sin( x ) )
        return df

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return str( "Sine: f( x:p ) = p_1 * cos( 2PI * x * p_0 ) + p_2 * sin( 2PI * x * p_0 )" )

    def baseParameterUnit( self, k ):
        """
        Return the unit of a parameter.

        Parameters
        ----------
        k : int
            the kth parameter.

        """
        if k == 0:
            return units.Unit( units.si.rad ) / self.xUnit
        return self.yUnit


