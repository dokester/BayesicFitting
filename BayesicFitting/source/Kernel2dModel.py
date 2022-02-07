import numpy as numpy
from astropy import units
import math
from . import Tools
from .Tools import setAttribute as setatt

from .NonLinearModel import NonLinearModel
from .kernels.Kernel import Kernel
from .kernels.Gauss import Gauss

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
#  *    2010 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2022 Do Kester

class Kernel2dModel( NonLinearModel ):
    """
    Two dimensional Kernel Model.

    The Kernel2dModel is defined as

        f( x:p ) = p_0 * K( r )

    where K( r ) is a selectable kernel function and r is the distance to the center.

        r = sqrt( u^2 + v^2 ).

    There are 3 options for u and v

    1. CIRCULAR has 4 parameters
        Circular shape with only one width.
        u = ( x - p_1 ) / p_3
        v = ( x - p_2 ) / p_3
    2. ELLIPTIC has 5 parameters
        Elliptic shape aligned along the axes; 2 widths.
        u = ( x - p_1 ) / p_3
        v = ( x - p_2 ) / p_4
    3. ROTATED has 6 parameters
        Rotated elliptical shape with 2 width and a rotational angle.
        u = ( ( x - p_1 )*cos( p_5 ) - ( y - p_2 )*sin( p_5) ) / p_3
        v = ( ( x - p_1 )*sin( p_5 ) + ( y - p_2 )*cos( p_5) ) / p_4

    The "center" parameters ( 1&2 ) and the "angle" parameter ( 5 ) are initilized as 0.
    The rotational angle is measured counterclockwise from the x-axis.
    The "width" parameters ( 3&4 ) are initialized as 1.0, except for the ROTATED case;
    then they need to be different ( 2.0 and 0.5 resp. ).
    Otherwise the model parameter "angle" is degenerate.
    The "amplitude" parameter is set to 1.0.

    Several kernel functions, K( x ) are defined in the directory fit/kernels.

    Beware: These models are unaware of anything outside their range.

    Author:      Do Kester

    Example
    -------
    >>> model = Kernel2dModel( )                                 # default: circular Gauss
    >>> model.setKernelShape( Lorentz(), 'Elliptic'  )             # elliptic Lorentz model.
    >>> model = Kernel2dModel( shape=3 )                         # rotated Gauss

    Category:    mathematics/Fitting

    """
    SHAPENAMES = ["Circular", "Circular", "Elliptic", "Rotated"]

    CIRCULAR = 1
    ELLIPTIC = 2
    ROTATED = 3
    NPAR = [4,4,5,6]

    def __init__( self, kernel=Gauss(), shape=1, copy=None, **kwargs ):
        """
        Kernel Model.

        Default model: Gauss with Circular shape.

        Parameters
        ----------
        kernel : Kernel
            the kernel to be used
        shape : 1 | 2 | 3 | 'circular' | 'elliptic' | 'rotated'
            int : resp.: circular elliptic, rotated
            str : case insensitive; only the first letter matters.
            shape defaults to 'circular' when misunderstood
        copy : Kernel2dModel
            to be copied
        fixed : None or dictionary of {int:float|Model}
            int         index of parameter to fix permanently.
            float|Model values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
            See: @FixedModel

        """

        shape = self.parseShape( shape )

        super( Kernel2dModel, self ).__init__( self.NPAR[shape], ndim=2, copy=copy, **kwargs )

        if copy is not None :
            self.kernel = copy.kernel
            self.shape = copy.shape
            self.shape2d = copy.shape2d
        else :
            self.setKernelShape( kernel, shape )

    def copy( self ):
        """ Copy method.  """
        return Kernel2dModel( copy=self, shape=self.shape )

    def __setattr__( self, name, value ) :
        if name == "kernel" :
            setatt( self, name, value, type=Kernel )
        elif name == "shape2d" :
            setatt( self, name, value, type=BaseShape2d )
        elif name == "shape" :
            setatt( self, name, value )
        elif name == "npbase" :
            setatt( self, name, value )
        else :
            super( Kernel2dModel, self ).__setattr__( name, value )

    def parseShape( self, shape ) :
        if isinstance( shape, str ) :
            shape = str.find( 'xxcCeErR', shape[0] ) // 2
        if not 1 <= shape <= 3 :
            shape = 1
        return shape


    def setKernelShape( self, kernel, shape ) :
        shape = self.parseShape( shape )
        self.kernel = kernel
        amp = 2.0 / ( self.kernel.integral * math.pi )

        self.shape = shape
        self.npbase = self.NPAR[shape]
        if self.fixed is not None : self.npbase -= len( self.fixed )

        parNames = ["amplitude", "x-center", "y-center"]
        if shape == 1 :
            pars = Tools.toArray( [amp, 0.0, 0.0, 1.0] )
            self.parameters = self.select( pars )
            self.posIndex = [3]
            self.nonZero = [3]
            parNames += ["width"]
            self.shape2d = Circle( self.npbase, self.kernel )
        elif shape == 2 :
            pars = Tools.toArray( [amp, 0.0, 0.0, 1.0, 1.0] )
            self.parameters = self.select( pars )
            self.posIndex = [3,4]
            self.nonZero = [3,4]
            parNames += ["x-width", "y-width"]
            self.shape2d = Ellipse( self.npbase, self.kernel )
        elif shape == 3 :
            pars = Tools.toArray( [amp, 0.0, 0.0, 2.0, 0.5, 0.0] )
            self.parameters = self.select( pars )
            self.posIndex = [3,4]
            self.nonZero = [3,4]
            parNames += ["x-width", "y-width", "angle"]
            self.shape2d = Rotated( self.npbase, self.kernel )
        self.parNames = self.selectNames( parNames )

    def baseName( self ):
        """ Returns a string representation of the model.  """
        return "2-d-" + self.SHAPENAMES[self.shape] + "-" + self.kernel.name( )

    def baseResult( self, xdata, params ):
        """
        Returns the result of the model function.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result
        params : array_like
            values for the parameters

        """
        return self.shape2d.result( xdata, params )

    def baseDerivative( self, xdata, params ):
        """
        Returns df/dx of the model function.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result
        params : array_like
            values for the parameters

        """
        df = self.shape2d.derivative( xdata, params )
        return numpy.asarray( df ).T

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the xdata value.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the partials
        params : array_like
            parameters to the model (ignored in LinearModels)
        parlist : array_like
            list of indices of active parameters

        """
        return self.shape2d.partial( xdata, params, parlist=parlist )


    def baseParameterUnit( self, k ):
        """
        Return the unit of a parameter.
        Parameters
        ----------
        k : int
            the kth parameter.

        """
        if k == 0:
            return self.yUnit
        if k == 5:
            return units.Unit( units.si.rad )
        return self.xUnit[(k-1)%2]

    def isBound( self ):
        return self.kernel.isBound( )

class BaseShape2d( object ):
    def __init__( self, npbase, kernel ) :
        self.npbase = npbase
        self.kernel = kernel

    def reslt( self, xdata, params, kp ):
        x = ( xdata[:,0] - params[1] ) / params[3]
        y = ( xdata[:,1] - params[2] ) / params[kp]
        return params[0] * self.kernel.resultsq( x * x + y * y )

    def deriv( self, xdata, params, kp ) :
        x = ( xdata[:,0] - params[1] ) / params[3]
        y = ( xdata[:,1] - params[2] ) / params[kp]
        r = numpy.sqrt( x * x + y * y )
        drdx = x / r
        drdy = y / r
        df = [params[0] * self.kernel.partial( r ) * drdx / params[3],
              params[0] * self.kernel.partial( r ) * drdy / params[kp]]
        return df


class Circle( BaseShape2d ):
    def __init__( self, npbase, kernel ) :
        super( Circle, self ).__init__( npbase, kernel )

    def result( self, xdata, params ):
        return self.reslt( xdata, params, 3 )

    def derivative( self, xdata, params ):
        return self.deriv( xdata, params, 3 )

    def partial( self, xdata, params, parlist=None ):
        np = self.npbase if parlist is None else len( parlist )
        partial = numpy.ndarray( ( Tools.length( xdata[:,0] ), np ) )
        u = ( xdata[:,0] - params[1] ) / params[3]
        v = ( xdata[:,1] - params[2] ) / params[3]
        r2 = u * u + v * v
        r = numpy.sqrt( r2 )
        p0dkdr = -params[0] * self.kernel.partial( r )
        try :
            drdu = numpy.where( r == 0, 1.0, u / r )
            drdv = numpy.where( r == 0, 1.0, v / r )
        except Warning :
            pass

        parts = { 0 : ( lambda: self.kernel.resultsq( r2 ) ),
                  1 : ( lambda: p0dkdr * drdu / params[3] ),
                  2 : ( lambda: p0dkdr * drdv / params[3] ),
                  3 : ( lambda: p0dkdr * r / params[3] ) }

        if parlist is None :
            parlist = range( np )

        for k,kp in enumerate( parlist ) :
            partial[:,k] = parts[kp]()

        return partial

    def __str__( self ) :
        return "Circle"

class Ellipse( BaseShape2d ):
    def __init__( self, npbase, kernel ) :
        super( Ellipse, self ).__init__( npbase, kernel )

    def result( self, xdata, params ):
        return self.reslt( xdata, params, 4 )

    def derivative( self, xdata, params ):
        return self.deriv( xdata, params, 4 )

    def partial( self, xdata, params, parlist=None ):
        np = self.npbase if parlist is None else len( parlist )
        partial = numpy.ndarray( ( Tools.length( xdata[:,0] ), np ) )
        u = ( xdata[:,0] - params[1] ) / params[3]
        v = ( xdata[:,1] - params[2] ) / params[4]
        r2 = u * u + v * v
        r = numpy.sqrt( r2 )
        p0dkdr = -params[0] * self.kernel.partial( r )
        try :
            drdu = numpy.where( r == 0, 1.0, u / r )
            drdv = numpy.where( r == 0, 1.0, v / r )
        except RuntimeWarning :
            pass

        parts = { 0 : ( lambda: self.kernel.resultsq( r2 ) ),
                  1 : ( lambda: p0dkdr * drdu / params[3] ),
                  2 : ( lambda: p0dkdr * drdv / params[4] ),
                  3 : ( lambda: p0dkdr * u * drdu / params[3] ),
                  4 : ( lambda: p0dkdr * v * drdv / params[4] ) }


        if parlist is None :
            parlist = range( np )

        for k,kp in enumerate( parlist ) :
            partial[:,k] = parts[kp]()

        return partial

    def __str__( self ) :
        return "Ellipse"

class Rotated( BaseShape2d ):
    def __init__( self, npbase, kernel ) :
        super( Rotated, self ).__init__( npbase, kernel )

    def result( self, xdata, params ):
        x = ( xdata[:,0] - params[1] )
        y = ( xdata[:,1] - params[2] )
        c = math.cos( params[5] )
        s = math.sin( params[5] )
        u = ( x * c - y * s ) / params[3]
        v = ( x * s + y * c ) / params[4]
        return params[0] * self.kernel.resultsq( u * u + v * v )

    def derivative( self, xdata, params ) :
        x = ( xdata[:,0] - params[1] )
        y = ( xdata[:,1] - params[2] )
        c = math.cos( params[5] )
        s = math.sin( params[5] )

        u = ( x * c - y * s ) / params[3]
        v = ( x * s + y * c ) / params[4]
        r = numpy.sqrt( u * u + v * v )
        drdu = numpy.where( r == 0, 1.0, u / r )
        drdv = numpy.where( r == 0, 1.0, v / r )
        p0dkdr = params[0] * self.kernel.partial( r )
        df = [ p0dkdr * ( drdu * c / params[3] + drdv * s / params[4] ),
               p0dkdr * ( drdv * c / params[4] - drdu * s / params[3] ) ]

        return df

    def partial( self, xdata, params, parlist=None ):
        np = self.npbase if parlist is None else len( parlist )
        partial = numpy.ndarray( ( Tools.length( xdata[:,0] ), np ) )
        x = ( xdata[:,0] - params[1] )
        y = ( xdata[:,1] - params[2] )
        c = math.cos( params[5] )
        s = math.sin( params[5] )
        u = ( x * c - y * s ) / params[3]
        v = ( x * s + y * c ) / params[4]
        r2 = u * u + v * v
        r = numpy.sqrt( r2 )
        p0dkdr = - params[0] * self.kernel.partial( r )
        try :
            drdu = numpy.where( r == 0, 1.0, u / r )
            drdv = numpy.where( r == 0, 1.0, v / r )
        except RuntimeWarning :
            pass

        parts = { 0 : ( lambda: self.kernel.resultsq( r2 ) ),
                    #  dfdp1 = p0 * dkdr * ( drdu * dudx + drdv * dvdx ) * dxdp1
                  1 : ( lambda: p0dkdr * ( drdu * c / params[3] + drdv * s / params[4] ) ),

                    #  dfdp2 = p0 * dkdr * ( drdu * dudy + drdv * dvdy ) * dydp2
                  2 : ( lambda: p0dkdr * ( -drdu * s / params[3] + drdv * c / params[4] ) ),

                    #  dfdp3 = p0 * dkdr * drdu * dudp3
                  3 : ( lambda: p0dkdr * drdu * u / params[3] ),
                  4 : ( lambda: p0dkdr * drdv * v / params[4] ),

                    #  dfdp5 = p0 * dkdr * ( drdu * ( dudc * dcdp5 + duds * dsdp5 ) +
                    #                        drdv * ( dvdc * dcdp5 + dvds * dsdp5 ) )
                  5 : ( lambda: -p0dkdr * ( drdu * ( -x * s - y * c ) / params[3] +
                                            drdv * ( -y * s + x * c ) / params[4] ) ) }

        if parlist is None :
            parlist = range( np )

        for k,kp in enumerate( parlist ) :
            partial[:,k] = parts[kp]()

        return partial

    def __str__( self ) :
        return "Rotated"


