import numpy as numpy
from astropy import units
import math
from . import Tools
from .LinearModel import LinearModel
from .SplinesModel import SplinesModel

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
#  *    2017        Do Kester

class SineSplineModel( LinearModel ):
    """
    Sine of fixed frequency with splineslike amplitudes/phases.

    .. math::
        f( x:p ) = s_0 \cos( 2 \pi \omega x ) + s_1 \sin( 2 \pi \omega x )

    Where :math:`s_0` and :math:`s_1` are splines with defined knots and order.
    It is a linear model with 2 * ( len(knots) + order - 1 ) papameters.

    Examples
    --------
    >>> knots = [3.0*k for k in range( 11 )]
    >>> sine = SineSplineModel( 150, knots )        # fixed frequency of 150 Hz
    >>> print( sine.npbase )                        # number of parameters
    26
    """

    def __init__( self, frequency, knots, order=3, copy=None, fixed=None, **kwargs ):
        """
        Sine model of a fixed frequency with a splineslike changing amplitude/phase.

        Number of parameters is 2 * ( len(knots) + order - 1 ).

        Parameters
        ----------
        frequency : float
            the frequency
        copy : SineSplineModel
            model to be copied
        fixed : dict
            If not None raise AttributeError.

        Raises
        ------
        AttributeError
            when fixed is not None

        """
        if fixed is not None :
            raise AttributeError( "SineSplineModel cannot have fixed parameters" )

        np = 2 * ( len( knots ) + order - 1 )
        super( SineSplineModel, self ).__init__( np, copy=copy, **kwargs )

        self.frequency = frequency
        self.knots = knots
        self.order = order
        if copy is not None :
            self.cm = copy.cm.copy()
            self.sm = copy.sm.copy()
        else :
            self.cm = SplinesModel( knots, order=order )
            self.sm = SplinesModel( knots, order=order )

    def copy( self ):
        """ Copy method.  """
        return SineSplineModel( self.frequency, self.knots, order=self.order, copy=self )

    def __setattr__( self, name, value ) :
        dind = {"frequency": float, "order": float, "cm": SplinesModel, "sm": SplinesModel}
        dlst = {"knots": float}
        if not ( Tools.setListOfAttributes( self, name, value, dlst ) or
                 Tools.setSingleAttributes( self, name, value, dind ) ) :
            super( SineSplineModel, self ).__setattr__( name, value )

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            parameters of the model (ignored in LinearModels)
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        nxdata = Tools.length( xdata )
        part = numpy.zeros( ( nxdata, self.npbase ), dtype=float )
        nh = self.npbase // 2
        cx = numpy.cos( 2 * math.pi * self.frequency * xdata )
        sx = numpy.sin( 2 * math.pi * self.frequency * xdata )

        part[:,:nh] = ( cx * self.cm.basePartial( xdata, params ).transpose() ).transpose()
        part[:,nh:] = ( sx * self.sm.basePartial( xdata, params ).transpose() ).transpose()
        return part

    def baseDerivative( self, xdata, params ):
        """
        Returns the derivative of f to x (df/dx) at the input value.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            parameters of the model

        """
        tpf = 2 * math.pi * self.frequency
        tx = tpf * xdata
        cx = numpy.cos( tx )
        sx = numpy.sin( tx )
        amps = self.getAmplitudes( xdata, params )
        cadx = self.cm.baseDerivative( xdata, params )
        sadx = self.sm.baseDerivative( xdata, params )
        return tpf * ( cadx * cx - amps[0] * sx + sadx * sx + amps[1] * cx )

    def getAmplitudes( self, xdata, params ) :
        """
        Return the amplitudes if cosine and sine, resp.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            parameters of the model

        """
        nh = self.npbase // 2
        return ( self.cm.result( xdata, params[:nh] ),
                 self.sm.result( xdata, params[nh:] ) )

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return ( "SineSpline: f( x:p ) = spline_0 * cos( 2 pi * x * f ) + " +
                 "spline_1 * sin( 2 pi * x * f ); f = %f"%self.frequency )

    def baseParameterUnit( self, k ):
        """
        Return the name of a parameter.
        Parameters
        ----------
        k : int
            the kth parameter.

        """
        k = k % ( self.npbase / 2 )
        if k > self.order :
            k = self.order
        return self.yUnit / ( self.xUnit ** k )



