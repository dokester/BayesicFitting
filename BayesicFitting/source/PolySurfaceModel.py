import numpy as numpy
from . import Tools
from .Tools import setAttribute as setatt
from .Formatter import formatter as fmt

from .LinearModel import LinearModel

__author__ = "Do Kester"
__year__ = 2022
__license__ = "GPL3"
__version__ = "3.0.0"
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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2017 - 2022 Do Kester

class PolySurfaceModel( LinearModel ):
    """
    General polynomial surface model of arbitrary degree.

        f( x,y:p ) = &sum;_d &sum;_k p_n * x^{d-k} * y^k )

    where the first sum is over d running from 0 to degree ( inclusive )
    and the second sum is over k running from 0 to d ( inclusive ).
    The index n is just incrementing, making all p's different.

    It is a 2-dimensional linear model.

    Examples
    --------
    poly = PolySurfaceModel( 3 )         # 3rd degree polynomial
    print poly.getNumberOfParameters( )        # 10

    Author      Do Kester

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
        Polynominal surface of a certain degree. Two dimensions.

        degree      polysurface
          0         p_0
          1         p_0 + p_1 * x + p_2 * y
          2         p_0 + p_1 * x + p_2 * y + p_3 * x^2 + p_4 * x * y + p_5 * y^2
          3         p_0 + p_1 * x + p_2 * y + p_3 * x^2 + p_4 * x * y + p_5 * y^2 +
                        p_6 * x^3 + p_7 * x^2 * y + p_8 * x * y^2 + p_9 * y^3
        etc.

        The number of parameters is ( degree+2 ) * ( degree+1 ) / 2

        Parameters
        ----------
        degree : int
            the degree of the polynomial.
        copy : PolySurfaceModel
            model to be copied
        fixed : dictionary of {int:float|Model}
            int             list if parameters to fix permanently. Default None.
            float|Model     list of values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
            See @FixedModel

        """
        super( PolySurfaceModel, self ).__init__( (degree+2)*(degree+1)//2, ndim=2,
                copy=copy, **kwargs )
        self.degree = degree

        if copy is not None and hasattr( copy, "xindex" ) :
            setatt( self, "xindex", copy.xindex )
            setatt( self, "yindex", copy.yindex )
            setatt( self, "xfact", copy.xfact )
            setatt( self, "yfact", copy.yfact )
            

    def copy( self ):
        """ Copy method.  """
        return PolySurfaceModel( self.degree, copy=self )

    def __setattr__( self, name, value ):
        """
        Set attributes: degree
        """
        if name == 'degree' :
            setatt( self, name, value, type=int )
        else :
            super( PolySurfaceModel, self ).__setattr__( name, value )

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input values.

        The partials are the powers of x,y ( xdata ) from 0 to degree.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        nx = Tools.length( xdata[:,0] )
        part = numpy.zeros( ( nx, self.npmax ), dtype=float )
        n = 0
        for d in range( self.degree + 1 ) :
            x = numpy.ones( nx, dtype=float )
            i = 0
            while i <= d :
                part[:,n+i] = x
                x *= xdata[:,1]
                i += 1
            x = numpy.ones( nx, dtype=float )
            i = d
            while i >= 0 :
                part[:,n+i] *= x
                x *= xdata[:,0]
                i -= 1
            n += d + 1
        if parlist is None :
            return part

        return part[:,parlist]

    def baseDerivative( self, xdata, params ) :
        """
        Return the derivative df/dx at each input (=x).

        degree      df/dx
          0         0
          1         p_1
          2         p_1 + 2 * p_3 * x + p_4 * y
          3         p_1 + 2 * p_3 * x + p_4 * y + 3 * p_6 * x^2 + 2 * p_7 * x * y + p_8 * y^2

        degree      df/dy
          0         0
          1         p_2
          2         p_2 + p_4 * x + 2 * p_5 * y
          3         p_2 + p_4 * x + 2 * p_5 * y + p_7 * x^2 + 2 * p_8 * x * y + 3 * p_9 * y^2


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

        if not hasattr( self, "xindex" ) :
            indx = []
            fact = []
            n = 1
            k = 1
            while k < np :
#                print( np, k, n )
                indx += [i for i in range( k, k+n )]
                fact += [n-f for f in range( n )]
                k += n + 1
                n += 1

#                print( "X  ", fmt( indx, max=None ), fmt( fact, max=None ) )

            setatt( self, "xindex", indx )
            setatt( self, "xfact", fact )

            indx = []
            fact = []
            k = 2
            n = 1
            while k < np :
#                print( np, k, n )
                indx += [i for i in range( k, k+n )]
                fact += [f+1 for f in range( n )]
                k += n + 1
                n += 1

#                print( "Y  ", fmt( indx, max=None ), fmt( fact, max=None ) )

            setatt( self, "yindex", indx )
            setatt( self, "yfact", fact )


        p = params[self.xindex] * self.xfact
        deg  = self.degree - 1

        dfdx = PolySurfaceModel( deg ).result( xdata, p )

        p = params[self.yindex] * self.yfact
        dfdy = PolySurfaceModel( deg ).result( xdata, p )

        return numpy.append( dfdx, dfdy ).reshape( 2, -1 ).T


    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        bn = "PolySurface: f( x,y:p ) ="
        n = 0
        plus = ""
        for d in range( self.degree + 1 ) :
            i = d
            k = 0
            while k <= d :
                bn += "%s p_%d"%(plus,n)
                if i > 0 :
                    bn += " * x%s"%( "" if i == 1 else "^%d"%i )
                if k > 0 :
                    bn += " * y%s"%( "" if k == 1 else "^%d"%k )
                n += 1
                k += 1
                i -= 1
            plus = " +"
        return bn

    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.
        Parameters  k    parameter number.

        """
        dk = 0
        while k > dk:
            dk += 1
            k -= dk
        return self.yUnit / ( ( self.xUnit[0]**k ) * ( self.xUnit[1] ** (dk-k) ) )


