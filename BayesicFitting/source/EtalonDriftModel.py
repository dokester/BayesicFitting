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
#  *    2016 - 2020 Do Kester

class EtalonDriftModel( NonLinearModel ):
    """
    Sinusoidal Model with drifting frequency.

        f( x,y:p ) = p_0 / ( 1.0 + p_1^2 * sin^2( &pi; ( p_2 x + p_3 + p_4 y ) ) )

    where p_0 = amplitude
          p_1 = finesse
          p_2 = periods per wavenumber
          p_3 = phase
          p_4 = phase drift
    As always (x,y) = input; it is in (wavenumbers,alpha)

    The parameters are initialized at {1.0, 1.0, 1.0, 0.0, 0.0}. It is a non-linear model.

    This model is specificly made for the MIRI instrumnet aboard JWST.
    Its usefullness elsewhere is doubtfull.

    Attributes from Model
    ---------------------
        npchain, parameters, stdevs, xUnit, yUnit

    Attributes from FixedModel
    --------------------------
        npmax, fixed, parlist, mlist

    Attributes from BaseModel
    --------------------------
        npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames

    Examples
    --------
    >>> fpm = EtalonDriftModel( )
    >>> print( fpm.npchain )
    5
    >>> pars = [1.0, 30.0, 1.0, 0.0, 0.0]
    >>> fpm.parameters = pars

    """

    def __init__( self, copy=None, **kwargs ):
        """
        Etalon model.

        Number of parameters is 5.

        Parameters
        ----------
        copy : EtalonModel
            to be copied
        fixed : None or dictionary of {int:float|Model}
            int         index of parameter to fix permanently.
            float|Model values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
            See: @FixedModel

        """
        param = [1.0, 1.0, 1.0, 0.0, 0.0]
        names = ["amplitude", "finesse", "period", "phase", "drift"]
        super( EtalonDriftModel, self ).__init__( 5, ndim=2, copy=copy,
                params=param, names=names, **kwargs )
        if copy is None :
            self.posIndex = [2]

    def copy( self ):
        """ Copy method.  """
        return EtalonDriftModel( copy=self )

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
        x = math.pi * ( params[2] * xdata[:,0] + params[3] + params[4] * xdata[:,1] )
        sx = params[1] * numpy.sin( x )
        return params[0] / ( 1.0 + sx * sx )

#        sx = numpy.sin( x )
#        return params[0] / ( 1.0 + params[1] * sx * sx )

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
        x = math.pi * ( xdata[:,0] * params[2] + params[3] + params[4] * xdata[:,1] )
        sx = numpy.sin( x )

        p1 = params[1] * params[1]
        dd = 1 + p1 * sx * sx
#        dd = 1 + params[1] * sx * sx

        dd *= dd
        df = - 2 * math.pi * params[0] * p1 * params[2] * sx * numpy.cos( x ) / dd
#        df = - 2 * math.pi * params[0] * params[1] * params[2] * sx * numpy.cos( x ) / dd
        return [df * params[2], df * params[4]]

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

        x = math.pi * ( xdata[:,0] * params[2] + params[3] + params[4] * xdata[:,1] )
        sx = numpy.sin( x )
        s2 = sx * sx

        p1 = params[1] * params[1]
        dd = 1.0 / ( 1 + p1 * s2 )
#        dd = 1.0 / ( 1 + params[1] * s2 )

        d2 = dd * dd
        p3 = - 2 * math.pi * params[0] * p1 * sx * numpy.cos( x ) * d2
#        p3 = - 2 * math.pi * params[0] * params[1] * sx * numpy.cos( x ) * d2

        parts = { 0 : ( lambda: dd ),
                  1 : ( lambda: - 2 * params[0] * params[1] * s2 * d2 ),
#                  1 : ( lambda: - params[0] * s2 * d2 ),
                  3 : ( lambda: p3 ),
                  2 : ( lambda: xdata[:,0] * p3 ),
                  4 : ( lambda: xdata[:,1] * p3 ) }

        if parlist is None :
            parlist = range( self.npmax )

        for k,kp in enumerate( parlist ) :
            partial[:,k] = parts[kp]()

        return partial

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return ( "EtalonDrift: f( x,y:p ) = p_0 / " +
                 "( 1 + p_1 * sin^2( PI * ( x * p_2 + p_3 + y * p_4 ) )" )

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
            return units.Unit( 1.0 )
        if k == 2:
            return units.Unit( units.si.rad ) / self.xUnit[0]
        if k == 3:
            return units.Unit( units.si.rad )
        if k == 4:
            return units.Unit( units.si.rad ) / self.xUnit[1]
        return self.yUnit


