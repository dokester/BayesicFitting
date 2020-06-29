import numpy as numpy
from astropy import units
import math
from . import Tools
from .NonLinearModel import NonLinearModel

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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2015 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2017 Do Kester

class SineDriftModel( NonLinearModel ):
    """
    Sinusoidal Model with drifting frequency.
    .. math::
        f( x:p ) = p_1 * \cos( \phi ) + p_2 * sin( \phi )
        \phi = 2 * \pi * x * ( p_0 + x * p_3 )

    where :math:`p_0` = frequency, :math:`p_3` = is the drift in frequency,
    :math:`p_1` = amplitude cosine and :math:`p_2` = amplitude sine.
    As always x = input.

    The parameters are initialized at {1.0, 1.0, 1.0, 0.0}. It is a non-linear model.

    Examples
    --------
    >>> sine = SineDriftModel( )
    >>> print( sine.npchain )
    >>> pars = [0.1,0,1,0.0]
    >>> sine.parameters = pars
    >>> print( sine( numpy.arange( 101, dtype=float ) ) )     # 10 sine periods, no drift
    >>> pars = [0.1,0,1,0.001]
    >>> sine.parameters = pars
    >>> print( sine( numpy.arange( 101, dtype=float ) ) )     # 10 sine periods, drifting


    Attributes
    ----------
        No attributes of its own.

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
        Sinusiodal model with drifting frequency.

        Number of parameters is 4.

        Parameters
        ----------
        copy : SineDriftModel
            to be copied
        fixed : dictionary of {int:float}
            int     list if parameters to fix permanently. Default None.
            float   list of values for the fixed parameters.
            Attribute fixed can only be set in the constructor.

        """
        param = [1.0, 1.0, 1.0, 0.0]
        names = ["frequency", "cosamp", "sinamp", "freqslope"]

        super( SineDriftModel, self ).__init__( 4, copy=copy, params=param,
                        names=names, **kwargs )

    def copy( self ):
        """ Copy method.  """
        return SineDriftModel( copy=self )

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
        x = 2 * math.pi * xdata * ( params[0] + params[3] * xdata )
        return params[1] * numpy.cos( x ) + params[2] * numpy.sin( x )

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
        x = 2 * math.pi * xdata * ( params[0] + params[3] * xdata )
        return ( 2 * math.pi * ( params[0] + 2 * params[3] * xdata ) *
                ( params[2] * numpy.cos( x ) - params[1] * numpy.sin( x ) ) )

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

        x0 = 2 * math.pi * xdata
        x3 = x0 * xdata
        xf = x0 * params[0] + x3 * params[3]
        cx = numpy.cos( xf )
        sx = numpy.sin( xf )
        parts = { 0 : ( lambda: x0 * params[2] * cx - x0 * params[1] * sx ),
                  1 : ( lambda: cx ),
                  2 : ( lambda: sx ),
                  3 : ( lambda: x3 * params[2] * cx - x3 * params[1] * sx ) }


        if parlist is None :
            parlist = range( self.npmax )

        for k,kp in enumerate( parlist ) :
            partial[:,k] = parts[kp]()

        return partial

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return ( "Sine: f( x:p ) = p_1 * cos( 2PI * x * ( p_0 + p_3 * x ) ) + " +
                                  "p_2 * sin( 2PI * x * ( p_0 + p_3 * x ) )" )

    def baseParameterUnit( self, k ):
        """
        Return the name of a parameter.

        Parameters
        ----------
        k : int
            the kth parameter.

        """
        if k == 0:
            return units.Unit( units.si.rad ) / self.xUnit
        if k == 3:
            return units.Unit( units.si.rad ) / ( self.xUnit * self.xUnit )
        return self.yUnit


