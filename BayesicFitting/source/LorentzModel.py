import numpy as numpy
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
#  *    2003 - 2011 Do Kester, SRON (JAVA code)
#  *    2016 - 2017 Do Kester

class LorentzModel( NonLinearModel ):
    """
    Lorentzian Model.
    .. math::
        f( x:p ) = p_0 * ( p_2^2 / ( ( x - p_1 )^2 + p_2^2 )

    :math:`p_0` = amplitude
    :math:`p_1` = x-shift
    :math:`p_2` = gamma ( width )

    The parameters are initialized at [1/PI, 0.0, 1.0] where the integral
    over the function equals 1.
    Parameter 2 ( gamma ) is always kept stricktly positive ( >0 ).

    This model is also known as Cauchy or Cauchy-Lorentz.

    Notes
    -----
    There are other possible
    <a href="http://en.wikipedia.org/wiki/Cauchy_distribution#Probability_density_function">
    definitions of this model</a>, where the integral equals 1.0.
    Definitions that integrate to 1.0 are more fit as a distribution function.
    See sample/CauchyErrorDistribution.

    We choose our definition for 2 reasons.
    1. to be in line with the definitions of the GaussModel, SincModel,
        VoigtModel, all KernelModels etc. In all of them the amplitude parameter,
        :math:`p_0`, equals the maximum of the function.
        I.e. :math:`p_0` is indeed the amplitude.
    2. to have maximally independent parameters, meaning that if you change one
        parameter, only that aspect changes. In the present definition this is the case.
        In the alternative definition if you change :math:`p_2`, not only the width
        of the function changes, but also the amplitude.

    Examples
    --------
    >>> lorentz = LorentzModel( )
    >>> lorentz.setParameters( [5, 4, 1] )
    >>> print( lorentz( numpy.arange(  41 , dtype=float ) / 5 ) )

    """
    def __init__( self, copy=None, **kwargs ):
        """
        Lorentzian model.

        Number of parameters is 3.

        Parameters
        ----------
        copy : LorentzModel
            to be copied
        fixed : dictionary of {int:float}
            int     list if parameters to fix permanently. Default None.
            float   list of values for the fixed parameters.
            Attribute fixed can only be set in the constructor.

        """
        param = [1/math.pi, 0.0, 1.0]
        names = ["amplitude", "center", "width"]

        super( LorentzModel, self ).__init__( 3, copy=copy, params=param,
                        names=names, **kwargs )

        if copy is None :
            self.posIndex = [2]
            self.nonZero = [2]


    def copy( self ):
        """ Copy method.  """
        return LorentzModel( copy=self )

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
        s2 = params[2] * params[2]
        x = ( xdata - params[1] )
        result = params[0] * s2 / ( x * x + s2 )
        return result

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the xdata value.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            values for the parameters.
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        partial = numpy.ndarray( (Tools.length( xdata ), self.npbase ) )

        a = params[0]
        s = abs( params[2] )
        s2 = s * s
        x = ( xdata - params[1] )
        e = 1 / ( x * x + s2 )

        parts = { 0 : ( lambda: s2 * e ),
                  1 : ( lambda: a * 2 * s2 * x * e * e ),
                  2 : ( lambda: a * 2 * s * x * x * e * e ) }

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
            values at which to calculate the derivative
        params : array_like
            values for the parameters.

        """
        x = xdata - params[1]
        c2 = params[2] * params[2]

        return -2 * params[0] * c2 * x / numpy.square( x * x + c2 )


    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return str( "Lorentz: f( x:p ) = p_0 * p_2^2 / ( ( x - p_1 )^2 + p_2^2 )" )

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
        return self.xUnit


