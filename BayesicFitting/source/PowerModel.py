import numpy as numpy
from .LinearModel import LinearModel
from . import Tools

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
#  *    2004 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2017 Do Kester

class PowerModel( LinearModel ):
    """
    General power model of arbitrary degree.
    .. math::
        f( x:p ) = p * x^a

    a is an float ( positive or negative ).

    To get the overall units of f(x:p) right, please note that the x-term
    needs to be divided by a factor 1.0 in the same units as the x.
    Otherwise possibly fractional dimensions are created.
    The factor is omitted as it does not contribute in the calculations.

    Examples
    --------
    >>> pwr = PowerModel( -1 )
    >>> print pwr.getNumberOfParameters( )       # 1
    1

    """
    def __init__( self, exponent=0, copy=None, **kwargs ):
        """
        Power of a certain degree.
        <br>
        The number of parameters is 1

        Parameters
        ----------
        exponent : int
            power to which the xdata is to be raised.

        """
        param = [1.0]
        names = ["coefficient"]
        super( PowerModel, self ).__init__( 1, copy=copy, params=param,
                    names=names, **kwargs )

        if copy is None :
            self.exponent = float( exponent )
        else :
            self.exponent = copy.exponent

    def copy( self ):
        """ Copy method.  """
        return PowerModel( copy=self )

    def __setattr__( self, name, value ) :
        dind = {"exponent": float}
        if not Tools.setSingleAttributes( self, name, value, dind ) :
            super( PowerModel, self ).__setattr__( name, value )


    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the xdata value.
        <br>
        The partials are x ( xdata ) to degree-th power.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters. (not used for linear models)
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        if parlist is None or parlist[0] == 0 :
            inp = numpy.asarray( [xdata] ).transpose()
            return numpy.power( inp, self.exponent )
        else :
            return numpy.asarray( [] )

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
        return params[0] * self.exponent * numpy.power( xdata, self.exponent - 1 )

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return str( "Power: f( x:p ) = p_0 * x^%.1f"%self.exponent )

    def baseParameterUnit( self, k ):
        """
        Return the name of a parameter.
        Not strictly OK. See Class documentation.
        Parameters
        ----------
        k : int
            the kth parameter.

        """
        return self.yUnit


