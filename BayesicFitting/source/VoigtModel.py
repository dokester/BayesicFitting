import numpy as numpy
import math
from scipy import special

from .NonLinearModel import NonLinearModel
from . import Tools

__author__ = "Do Kester"
__year__ = 2021
__license__ = "GPL3"
__version__ = "2.7.0"
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
#  *    2003 - 2011 Do Kester, SRON (JAVA code)
#  *    2016 - 2021 Do Kester

class VoigtModel( NonLinearModel ):
    """
    Voigt's Gauss Lorentz convoluted model for line profiles.

    The Voigt function is a convolution of a Gauss and a Lorentz function.
    Physicaly it is the result of thermal and pressure broadening of a spectral
    line.

    The models takes 4 parameters: amplitude, center frequency, half-width of
    the Gaussian, and half-width of the Lorentzian.
    These are initialised to [1, 0, 1, 1].
    Parameters 2 & 3 ( widths ) is always kept positive ( >=0 ).

    The implementation uses the Faddeeva function from scipy.special.wofz.

    Examples
    --------
    >>> voigt = VoigtModel( )
    >>> voigt.setParameters( [5, 4, 1, 2] )
    >>> print( voigt( numpy.arange(  41 , dtype=float ) / 5 ) )      # from [0,8]


    Attributes
    ----------
        none of its own

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
        Voigt model.

        Number of parameters is 4.

        Parameters
        ----------
        copy : VoigtModel
            to be copied

        """
        param = [1.0, 0.0, 1.0, 1.0]
        names = ["amplitude","center","gausswidth","lorentzwidth"]

        super( VoigtModel, self ).__init__( 4, copy=copy, params=param,
                        names=names, **kwargs )
        if copy is None :
            self.posIndex = [2,3]

    def copy( self ):
        """ Copy method.  """
        return VoigtModel( copy=self )

    def baseResult( self, xdata, params ):
        """
        Returns the result of the model function.

        Note: both width in the parameter array ( items 2 & 3 ) are kept
        strictly positive. I.e. they are changed when upon input they are negative.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        sigma = params[2] * math.sqrt( 2.0 )
        gamma = params[3]
        z0 = 1j * gamma / sigma
        z = ( xdata - params[1] ) / sigma + z0


        wofz0 = numpy.real( special.wofz( z0 ) )
        return params[0] * numpy.real( special.wofz( z ) ) / wofz0

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

            z = ( x - p1 + 1j * p3 ) / ( p2 * sqrt2 )
            z0 = 1j * p3 / ( p2 * sqrt2 )

            vgt = p0 * R( wofzz ) / R( wofz0 )

            dvdp = dvdz * dzdp

            dvdz = p0 * ( R(dwdz) * R(wofz0) - R(dwd0) * R(wofzz) ) / R(wofz0)^2
            dvdp = p0 * ( R(dwdz * dzdp) * R(wofz0) - R(dwd0 * d0dp) * R(wofzz) ) / R(wofz0)^2

            dwdz = 2j / sqrt(pi) - 2 * z  * wofzz
            dwd0 = 2j / sqrt(pi) - 2 * z0 * wofz0

            ## p0 and p1 have no influence in wofz0
            dzdp0 = 0
            dzdp1 = -1 / ( p2 * sqrt2 )
            d0dp2 = - ( 1j * p3 / ( p2^2 * sqrt2 )              = -z0 / p2
            dzdp2 = - ( ( x - p1 + 1j * p3 ) / ( p2^2 * sqrt2 ) = -z  / p2
            dzdp3 = d0dp3 = 1j / ( p2 * sqrt2 )

            dvdp0 = R(wofzz) / R(wofz0)
            ## The other partial follow from calculating dvdp for the parameters 1..3

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

        sigma = params[2] * math.sqrt( 2.0 )
        gamma = params[3]
        z0 = 1j * gamma / sigma
        z = ( xdata - params[1] ) / sigma + z0

        wofz0 = special.wofz( z0 )
        wofzz = special.wofz( z )
        dwd0 = 2j / math.sqrt( math.pi ) - 2 * z0 * wofz0
        dwdz = 2j / math.sqrt( math.pi ) - 2 * z * wofzz

        rwz = numpy.real( wofzz )
        rw0 = numpy.real( wofz0 )
        a = params[0] / rw0
        a2 = a / rw0

        dzdp1 = -1 / sigma
        d0dp2 = -z0 / params[2]
        dzdp2 = -z / params[2]
        dzdp3 = 1j / sigma

        parts = { 0 : ( lambda: rwz / rw0 ),
                  1 : ( lambda: a * numpy.real( dwdz * dzdp1 ) ),
                  2 : ( lambda: a2 * ( numpy.real( dwdz * dzdp2 ) * rw0 -
                                       numpy.real( dwd0 * d0dp2 ) * rwz ) ),
                  3 : ( lambda: a2 * ( numpy.real( dwdz * dzdp3 ) * rw0 -
                                       numpy.real( dwd0 * dzdp3 ) * rwz ) ) }

        if parlist is None :
            parlist = range( self.npmax )

        for k,kp in enumerate( parlist ) :
            partial[:,k] = parts[kp]()

        return partial

    def baseDerivative( self, xdata, params ) :
        """
        Return the derivative df/dx at each xdata (=x).

            z = ( x - p1 + 1j * p3 ) / ( p2 * sqrt2 )
            z0 = 1j * p3 / ( p2 * sqrt2 )

            vgt = p0 / wofz0 * re( wofzz )
            dvdx = dvdz * dzdx

            dvdz = p0 / wofz0 * dwdz
            dwdz = 2j / sqrt(pi) - 2 * z * wofzz

            dzdx = 1 / ( p2 * sqrt2 )

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        sigma = params[2] * math.sqrt( 2.0 )
        gamma = params[3]
        z0 = 1j * gamma / sigma
        z = ( xdata - params[1] ) / sigma + z0

        wofz0 = numpy.real( special.wofz( z0 ) )
        wofzz = special.wofz( z )
        dwdz = 2j / math.sqrt( math.pi ) - 2 * z * wofzz

        return numpy.real( params[0] * dwdz / ( wofz0 * sigma ) )

    def baseName( self ):
        """
        Returns a string representation of the model.
        """
        return str( "Voigt:" )


    def baseParameterUnit( self, k ):
        """
        Return the name of a parameter.

        Parameters
        ---------
        k : int
            parameter number.

        """
        if k == 0:
            return self.yUnit
        return self.xUnit


