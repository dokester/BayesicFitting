import numpy as numpy
from . import Tools
from .Tools import setAttribute as setatt

from astropy import units
from .LinearModel import LinearModel

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
#  *    2010 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2020 Do Kester

class ChebyshevPolynomialModel( LinearModel ):
    """
    Chebyshev polynomial model of arbitrary degree.

        f( x:p ) = &sum; p_k * T_k( x )

    where the sum is over k running from 0 to degree ( inclusive ).

    The T( x ) are Chebyshev polynomials of the first kind which are defined
    recursively as:

        T_0( x ) = 1
        T_1( x ) = x
        T_n( x ) = 2 x T_{n-1}( x ) - T_{n-2}( x ) for n >= 2

    These polynomials are orthogonal, only when x is in [-1,+1].

    It is a linear model.

    Attributes
    ----------
    degree : int
        degree of the polynomial

    Attributes from Model
    --------------------------
        npchain, parameters, stdevs, xUnit, yUnit

    Attributes from FixedModel
    --------------------------
        npmax, fixed, parlist, mlist

    Attributes from BaseModel
    --------------------------
        npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames

    Examples
    --------
    >>> poly = ChebyshevPolynomialModel( 3 )         # 3rd degree polynomial
    >>> print poly.getNumberOfParameters( )
    4

    """
    def __init__( self, degree, copy=None, **kwargs ):
        """
        Chebyshev Polynomial of a certain degree.

        The number of parameters is ( degree + 1 )

        Parameters
        ----------
        degree : int
            the degree of the polynomial.
        copy : ChebyshevPolynomialModel
            to be copied
        fixed : None or dictionary of {int:float|Model}
            int         index of parameter to fix permanently.
            float|Model values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
            See: @FixedModel

        """
        names = ["coeff_%d"%k for k in range( degree + 1 )]
        super( ChebyshevPolynomialModel, self ).__init__( degree + 1, copy=copy,
                    names=names, **kwargs )

        self.degree = degree

    def copy( self ):
        """ Copy method.  """
        return ChebyshevPolynomialModel( self.degree, copy=self )

    def __setattr__( self, name, value ):
        """
        Set attributes: degree
        """
        if name == 'degree' :
            setatt( self, name, value, type=int )
        else :
            super( ChebyshevPolynomialModel, self ).__setattr__( name, value )

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the xdata value.

        The partials are calculated using the recurrence formula

            f_n( x ) = 2 * x * f_{n-1}( x ) - f_{n-2}( x )

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the partials
        params : array_like
            parameters of the model (ignored for linear models)
        parlist : array_like
            list of indices of active parameters

        """
        np = self.npmax
        nxdata = Tools.length( xdata )

        part = numpy.zeros( ( nxdata, np ), dtype=float )

        part[:,0] = 1.0
        if np >= 2:
            part[:,1] = xdata
        for i in range( 2, np ):
            part[:,i] = 2 * xdata * part[:,i-1] - part[:,i-2]
        if parlist is None :
            return part

        return part[:,parlist]

    def baseDerivative( self, xdata, params ):
        """
        Returns the derivative df/dx at the xdata value.

            df_n = n * U_{n-1}

        where
            U_0 = 1
            U_1 = 2x
            U_{n+1} = 2 * x * U_n - U_{n-1}

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the partials
        params : array_like
            parameters of the model

        """
        if self.npmax <= 1 :
            return numpy.zeros_like( xdata )

        np = self.npmax - 1

        um = numpy.ones_like( xdata )
        der = um * params[1]
        if np >= 2:
            uu = 2 * xdata
            der += 2 * uu * params[2]
        for i in range( 2, np ):
            up = 2 * xdata * uu - um
            um = uu
            uu = up
            der += (i+1) * uu * params[i+1]
        return der

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        bn = "ChebyshevPolynomial: f( x:p ) = p_0 * T_0(x)"
        for k in range( 1, self.npmax ):
            bn += " + p_%d * T_%d(x)"%(k,k)
        return bn

    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.
        It is always yUnit, as it cannot be otherwise.
        The xUnit must be dimensionless.

        Parameters
        ----------
        k : int
            parameter number.

        """
        return self.yUnit


