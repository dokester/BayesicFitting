import numpy as numpy
import math
from scipy import special
from .NonLinearModel import NonLinearModel

__author__ = "Do Kester"
__year__ = 2018
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
#  *    2003 - 2011 Do Kester, SRON (JAVA code)
#  *    2016 - 2017 Do Kester

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

    Examples
    --------
    >>> voigt = VoigtModel( )
    >>> voigt.setParameters( [5, 4, 1, 2] )
    >>> print( voigt( numpy.arange(  41 , dtype=float ) / 5 ) )      # from [0,8]

    """

    def __init__( self, copy=None, **kwargs ):
        """
        Voigt model.
        <br>
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
        strictly positive. I.e. they are changed when upon xdata they are negative.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        x = xdata - params[1]
        sigma = params[2] * math.sqrt( 2.0 )
        gamma = params[3]

        return params[0] * ( numpy.real( special.wofz( ( x + 1j * gamma ) / sigma ) ) /
                 ( sigma * math.sqrt( math.pi ) ) )


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


