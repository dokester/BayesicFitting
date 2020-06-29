import numpy as numpy
import math
from . import Tools
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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2007 - 2014 Do Kester, SRON (JAVA code)
#  *    2016 - 2020 Do Kester

class ArctanModel( NonLinearModel ):
    """
    Arctangus Model.

        f( x:p ) = p_0 * arctan( p_2 * ( x - p_1 ) )
        p_0 = amplitude;  p_1 = center; p_2 = slope.

    As always x = input.

    The parameters are initialized at {2/pi, 0.0, 1.0}. It is a non-linear model.

    Attributes from Model
    --------------------------
        npchain, parameters, stdevs, xUnit, yUnit

    Attributes from FixedModel
    --------------------------
        npmax, fixed, parlist, mlist

    Attributes from BaseModel
    --------------------------
        npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames

    Example
    -------
    >>> arct = ArctanModel( )
    >>> print( arct.getNumberOfParameters( ) )
    3


    Author:      Do Kester

    """

    def __init__( self, copy=None, **kwargs ):
        """
        Arc-tangus model.

        Number of parameters is 3.

        Parameters
        ----------
        copy : ArctanModel
            to be copied
        fixed : None or dictionary of {int:float|Model}
            int         index of parameter to fix permanently.
            float|Model values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
            See: @FixedModel

        """
        params = [2/math.pi, 0.0, 1.0]
        names = ["amplitude","center","slope"]
        super( ArctanModel, self ).__init__( nparams=3, copy=copy, params=params,
                                             names=names, **kwargs )

    def copy( self ):
        """ Copy method.  """
        return ArctanModel( copy=self )

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
        result = params[0] * numpy.arctan( params[2] * ( xdata - params[1] ) )
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
        partial = numpy.zeros( ( Tools.length( xdata ), np ) )

        x = params[2] * ( xdata - params[1] )
        xf = params[0] / ( 1 + x * x )

        parts = { 0 : ( lambda: numpy.arctan( x ) ),
                  1 : ( lambda: -xf * params[2] ),
                  2 : ( lambda: xf * ( xdata - params[1] ) ) }

        if parlist is None :
            parlist = range( self.npmax )

        for k,kp in enumerate( parlist ) :
            partial[:,k] = parts[kp]()

        return partial

    def baseDerivative( self, xdata, params ) :
        """
        Return the derivative df/dx at each input (=x).

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        x = params[2] * ( xdata - params[1] )
        return params[0] * params[2] / ( 1 + x * x )

    def baseName( self ):
        """
        Returns a string representation of the model.


        """
        return str( "Arctan: f( x:p ) = p_0 * arctan( p_2 * ( x - p_1 ) )" )

    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.

        """
        if k == 0:
            return self.yUnit
        if k == 2:
            return self.xUnit ** ( -1 )
        return self.xUnit


