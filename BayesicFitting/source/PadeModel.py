import numpy as numpy
from astropy import units
import math
from . import Tools

from .NonLinearModel import NonLinearModel
from .Formatter import formatter as fmt

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
#  *    2016 - 2017 Do Kester

class PadeModel( NonLinearModel ):
    """
    General Pade model of arbitrary degrees in numerator and denominator.
    .. math::
        f( x:p ) = \sum p_n * x^n / ( \sum p_{num+1+k} * x^k )

    where the sum in the numerator is over n running from 0 to num ( inclusive )
    and the sum in the denominator is over k running from 0 to den ( inclusive )

    At least one parameter needs to be fixed, otherwise the model is
    degenerate in its parameters.
    By default the first parameter of the denominator (p_{num+1})
    is fixed to 1.0.

    All parameters are initialized at 0. It is a non-linear model.

    Beware of the poles where the denominator equals zero.

    Author:      Do Kester

    Examples
    --------
    >>> pade = PadeModel( 3, 1 )            # 3rd degree polynomial
    >>> print pade.getNumberOfParameters( )        # 5
    5

    Category:    mathematics/Fitting

    Attributes
    ----------
    num : int
        order of the polynomial in the numerator
    den : int
        order of the polynomial in the denominator

    """
    PARNAMES = ["numer_", "denom_"]

    def __init__( self, num, den, copy=None, fixed=None, **kwargs ):
        """
        Pade of a certain degree in numerator and denominator.

        The number of parameters is ( num + den + 1 )

        Parameters
        ----------
        num : int
            the degree of the polynomial in the numerator.
        den : int
            the degree of the polynomial in the denominator.
        copy : PadeModel
            model to be copied
        fixed : dictionary of {int:float}
            int     list if parameters to fix permanently.
                    Default {num+1 : 1.0}
            float   list of values for the fixed parameters.
            Attribute fixed can only be set in the constructor.

        """
        names  = ["%s%d" % (self.PARNAMES[0], k) for k in range( num + 1 )]
        names += ["%s%d" % (self.PARNAMES[1], k) for k in range( den + 1 )]

        if fixed is None :
            fixed = { num + 1: 1.0 }
        np = num + den + 2
        params = numpy.zeros( np, dtype=float )
        params[num+1] = 1.0
        super( PadeModel, self ).__init__( np, params=params, copy=copy,
                        names=names, fixed=fixed, **kwargs )

        self.num = num
        self.den = den

    def copy( self ):
        """ Copy method.  """
        return PadeModel( self.num, self.den, copy=self )

    def __setattr__( self, name, value ):
        """
        Set attributes: num, den

        """
        dind = {'num': int, 'den': int }
        if not Tools.setSingleAttributes( self, name, value, dind ):
            super( PadeModel, self ).__setattr__( name, value )

    def baseResult( self, xdata, params ):
        """
        Returns the result of the model function.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            parameters for the model.

        """
        nm = numpy.zeros_like( xdata )
        xx = numpy.ones_like( xdata )
        k = 0
        while k <= self.num :
            nm += params[k] * xx
            xx *= xdata
            k += 1

        dn = numpy.zeros_like( xdata )
        xx = numpy.ones_like( xdata )
        while k < self.npmax :
            dn += params[k] * xx
            xx *= xdata
            k += 1

        return nm / dn

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the xdata values.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            parameters for the model.
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        nxdata = Tools.length( xdata )
        partial = numpy.zeros( ( nxdata, self.npmax ), dtype=float )

        xx = numpy.ones( nxdata )
        nm = numpy.zeros_like( xdata )
        k = 0
        while k <= self.num:
            partial[:,k] = xx
            nm += params[k] * xx
            xx *= xdata
            k += 1

        xx = numpy.ones( nxdata )
        dn = numpy.zeros_like( xdata )
        while k < self.npmax :
            partial[:,k] = -xx * nm
            dn += params[k] * xx
            xx *= xdata
            k += 1

        k = 0
        while k <= self.num :
            partial[:,k] /= dn
            k += 1
        while k < self.npmax :
            partial[:,k] /= dn * dn
            k += 1

        if parlist is None :
            return partial

        return partial[:,parlist]

    def baseDerivative( self, xdata, params ):
        """
        Returns the partials at the xdata values.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            parameters for the model.

        """
        nm = numpy.zeros_like( xdata )
        dn = numpy.zeros_like( xdata )
        dnm = numpy.zeros_like( xdata )
        ddn = numpy.zeros_like( xdata )

        xx = numpy.ones_like( xdata )
        nm += params[0] * xx
        k = 1
        while k <= self.num:
            dnm += k * params[k] * xx
            xx *= xdata
            nm += params[k] * xx
            k += 1

        xx = numpy.ones_like( xdata )
        dn += params[k] * xx
        k += 1
        while k < self.npmax :
            ddn += ( k - self.num - 1 ) * params[k] * xx
            xx *= xdata
            dn += params[k] * xx
            k += 1

        return ( dnm * dn - ddn * nm ) / ( dn * dn )

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        bn = "Pade: f( x:p ) = ( p_0"
        if self.num > 0 :
            bn += " + p_1 * x"
        for k in range( 2, self.num + 1 ) :
            bn += " + p_%d * x^%d"%(k,k)
        bn += " ) / ( p_%d" % (self.num+1)
        if self.den > 0 :
            bn += " + p_%d * x"%(self.num+2)
        for k in range( 3, self.den + 2 ) :
            bn += " + p_%d * x^%d"%(self.num+k, k-1)
        bn += " )"
        return bn

    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.
        Parameters
        ----------
        k : int
            parameter number.

        """
        if k <= self.num:
            return self.yUnit / ( self.xUnit ** k )
        k -= ( self.num + 1 )
        return self.xUnit ** (-k)


