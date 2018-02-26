import numpy as numpy
from . import Tools
from .LinearModel import LinearModel

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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2017        Do Kester

class PolySurfaceModel( LinearModel ):
    """
    General polynomial surface model of arbitrary degree.
    .. math::
        f( x,y:p ) = \sum_d \sum_k p_n * x^{d-k} * y^k )

    where the first sum is over d running from 0 to degree ( inclusive )
    and the second sum is over k running from 0 to d ( inclusive ).
    The index n is just incrementing, making all p's different.

    It is a 2-dimensional linear model.

    Examples
    --------
    poly = PolySurfaceModel( 3 )         # 3rd degree polynomial
    print poly.getNumberOfParameters( )        # 10

    Category     mathematics/Fitting

    Attributes
    ----------
    degree : int
        degree of the polynomial


    """
    def __init__( self, degree, copy=None, **kwargs ):
        """
        Polynominal surface of a certain degree.

        The number of parameters is ( degree+2 ) * ( degree+1 ) / 2

        Parameters
        ----------
        degree : int
            the degree of the polynomial.
        copy : PolySurfaceModel
            model to be copied
        fixed : dictionary of {int:float}
            int     list if parameters to fix permanently. Default None.
            float   list of values for the fixed parameters.
            Attribute fixed can only be set in the constructor.

        """
        super( PolySurfaceModel, self ).__init__( (degree+2)*(degree+1)//2, ndim=2,
                copy=copy, **kwargs )
        self.degree = degree


    def copy( self ):
        """ Copy method.  """
        return PolySurfaceModel( self.degree, copy=self )

    def __setattr__( self, name, value ):
        """
        Set attributes: degree
        """
        dind = {"degree": int}

        if Tools.setSingleAttributes( self, name, value, dind ) :
            pass                                            # success
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


