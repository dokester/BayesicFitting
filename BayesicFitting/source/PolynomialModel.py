import numpy as numpy
from .LinearModel import LinearModel
from . import Tools
from .Tools import setAttribute as setatt

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
#  *    2003 - 2014 Do Kester, SRON (JAVA Code)
#  *    2016 - 2020 Do Kester


class PolynomialModel( LinearModel ):
    """
    General polynomial model of arbitrary degree.

        f( x:p ) = &sum; p_k * x^k

    where the sum is over k running from 0 to degree ( inclusive ).

    It is a linear model.
    Examples
    --------
    >>> poly = PolynomialModel( 3 )            # 3rd degree polynomial
    >>> print( poly.getNumberOfParameters() )
    4

    Author : Do Kester

    Attributes
    ----------
    degree : int
        degree of the polynomial

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
    def __init__( self, degree, copy=None, **kwargs ):
        """
        Polynomial of a certain degree.

        The number of parameters is ( degree + 1 )

        Parameters
        ----------
        degree : int
            the degree of the polynomial.
        copy : PolynomialModel
            model to copy
        fixed : None or dictionary of {int:float|Model}
            int         index of parameter to fix permanently.
            float|Model values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
            See: @FixedModel

        """
        super(PolynomialModel,self ).__init__( degree + 1, copy=copy,
                        **kwargs )

        self.degree = degree

    def copy( self ):
        """ Copy method.  """
        return PolynomialModel( self.degree, copy=self )

    def __setattr__( self, name, value ):
        """
        Set attributes: degree
        """
        if name == 'degree' :
            setatt( self, name, value, type=int )
        else :
            super( PolynomialModel, self ).__setattr__( name, value )

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

        The partials are the powers of x ( xdata ) from 0 to degree.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            parameters for the model (ignored for LinearModels).
        parlist : array_like
            list of indices of active parameters

        """
        nxdata = Tools.length( xdata )
        x = numpy.ones( nxdata )

        partial = numpy.zeros( ( nxdata, self.npmax ), dtype=float )
        k = 0
        for i in range( self.npmax ) :
            partial[:,k] = x
            k += 1
            x *= xdata

        if parlist is None :
            return partial

        return partial[:,parlist]

    def baseDerivative( self, xdata, params ) :
        """
        Return the derivative df/dx at each input (=x).

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            parameters for the model.

        """
        if self.npmax <= 1 :
            return numpy.zeros_like( xdata )

        np = self.npmax
        p = params * numpy.arange( np )
        np -= 2
        return PolynomialModel( np ).result( xdata, p[1:] )

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        bn = "Polynomial: f( x:p ) = p_0"
        if self.npmax > 1 :
            bn += " + p_1 * x"
        for k in range( 2, self.npmax ) :
            bn += " + p_%d * x^%d"%(k,k)
        return bn

    def baseParameterName( self, k ):
        """
        Return the name of the indicated parameter.
        Parameters
        ----------
        k : int
            parameter number.

        """
        return "polycoeff_%d" % k

    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.

        Parameters
        ----------
        k : int
            parameter number.

        """
        return self.yUnit / ( self.xUnit ** k )


