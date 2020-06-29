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
#  *    2004 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2020 Do Kester

class PowerLawModel( NonLinearModel ):
    """
    General powerlaw model of arbitrary degree.

        f( x:p ) = p_0 * ( x - p_1 )^p_2

    with
        p_0 = amplitide
        p_1 = x-shift
        p_2 = power

    The parameters are initialized at {1.0, 0.0, 1.0}.

    Note that the term ( x - p_1 ) needs to be divided by a factor 1.0
    in the same units as the x, to get the overall units of f( x:p ) right.
    The factor is omitted as it does not contribute in the calculations.

    Examples
    --------
    >>> pl = PowerLawModel( )
    >>> print( pl.npchain )
    4

    Attributes
    ----------
        no attributes of its own.

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
        Powerlaw of an unknown degree.

        The number of parameters is 3

        Parameters
        ----------
        copy : PowerLawModel
            to be copied
        fixed : None or dictionary of {int:float|Model}
            int         index of parameter to fix permanently.
            float|Model values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
            See: @FixedModel
        """
        param = [1.0, 0.0, 1.0]
        names = ["amplitude", "x-shift", "power"]

        super( PowerLawModel, self ).__init__( 3, copy=copy, params=param,
                    names=names, **kwargs )

    def copy( self ):
        """ Copy method.  """
        return PowerLawModel( copy=self )

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
        return params[0] * numpy.power( xdata - params[1], params[2] )


    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input (xdata) value.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        partial = numpy.ndarray( ( Tools.length( xdata ), self.npbase ) )
        p0 = params[0]
        xs = xdata - params[1]
        p2 = params[2]

        parts = { 0 : ( lambda: numpy.power( xs, p2 ) ),
                  1 : ( lambda: -p0 * p2 * numpy.power( xs, p2 - 1 ) ),
                  2 : ( lambda: p0 * numpy.power( xs, p2 ) * numpy.log( xs ) ) }

        if parlist is None :
            parlist = range( self.npmax )

        for k,kp in enumerate( parlist ) :
            partial[:,k] = parts[kp]()

        return partial


    def baseDerivative( self, xdata, params ):
        """
        Returns the derivative (df/dx) at the input (xdata) value.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        return params[0] * params[2] * numpy.power( xdata - params[1], params[2] - 1 )

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return str( "PowerLaw: f( x:p ) = p_0 * ( x - p_1)^p_2" )

    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.
        Parameters
        ----------
        k : int
            parameter number.

        """
        if k == 0:
            return self.yUnit
        if k == 1:
            return self.xUnit
        return units.Unit( 1.0 )


