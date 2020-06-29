import numpy as numpy
import math
from . import Tools
from .Tools import setAttribute as setatt
from .NonLinearModel import NonLinearModel
from .PolynomialModel import PolynomialModel
from .SplinesModel import SplinesModel

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
#  *    2017 - 2020 Do Kester

class SineSplineDriftModel( NonLinearModel ):
    """
    Sine with drifting frequency and splineslike amplitudes/phases.

        nd = degree + 1
        nh = len( knots ) + order - 1
        xx = 2 &pi; x PM( x:p[:nd] )
        A  = SM( x:p[nd:nd+nh] )
        B  = SM( x:p[nd+nh:] )
        f( x:p ) = A cos( xx ) + B sin( xx )

    Where PM is a PolynomialModel and SM a SplinesModel

    It is a linear model with 2 * ( len(knots) + order - 1 ) papameters.

    Examples
    --------
    >>> knots = [3.0*k for k in range( 11 )]
    >>> sine = SineSplineDriftModel( 150, knots )        # fixed frequency of 150 Hz
    >>> print( sine.npbase )                        # number of parameters
    26

    Attributes
    ----------
    degree : int
        degree of the polynomial governing the frequency of the sine
    knots : array_like
        positions of the spline knots
    order : int
        order of the spline. default: 3
    cm : SplinesModel
        amplitude of the cosine
    sm : SplinesModel
        amplitude of the sine

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

    def __init__( self, knots, order=3, degree=1, copy=None, fixed=None, **kwargs ):
        """
        Sine model of a polynomially drifting frequency with a splineslike changing
        amplitude/phase

        Number of parameters is 2 * ( len(knots) + order - 1 ) + degree + 1.

        Parameters
        ----------
        knots : array of float
            the knot positions of the amplitude splines
        order : int
            order of the splines
        degree : int
            degree of the drifting polynomial
        copy : SineSplineDriftModel
            model to be copied
        fixed : dict
            If not None raise AttributeError.

        Raises
        ------
        AttributeError : When fixed is not None

        """
        if fixed is not None :
            raise AttributeError( "SineSplineDriftModel cannot have fixed parameters" )

        np = 2 * ( len( knots ) + order - 1 ) + degree + 1
        super( SineSplineDriftModel, self ).__init__( np, copy=copy, **kwargs )

        self.knots = knots
        self.order = order
        self.degree = degree
        if copy is not None :
            setatt( self, "pm", copy.pm.copy() )
            setatt( self, "cm", copy.cm.copy() )
            setatt( self, "sm", copy.sm.copy() )
        else :
            setatt( self, "pm", PolynomialModel( self.degree ) )
            setatt( self, "cm", SplinesModel( knots, order=order ) )
            setatt( self, "sm", SplinesModel( knots, order=order ) )

    def copy( self ):
        """ Copy method.  """
        return SineSplineDriftModel( self.knots, order=self.order,
                                     degree=self.degree, copy=self )

    def __setattr__( self, name, value ) :
        if name == "degree" :
            setatt( self, name, value, type=int )
        elif name == "knots" :
            setatt( self, name, value, type=float, islist=True )
        elif name == "order" :
            setatt( self, name, value, type=int )
        elif name == "cm" or name == "sm" or name == "pm":
            raise AttributeError( "Attributes cm or sm or pm can not be set" )
        else :
            super( SineSplineDriftModel, self ).__setattr__( name, value )

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
        drift = self.pm.result( xdata, params[:self.degree+1] )
        x = 2 * math.pi * xdata * drift
        amps = self.getAmplitudes( xdata, params )
        return amps[0] * numpy.cos( x ) + amps[1] * numpy.sin( x )

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
        nd = self.degree + 1
        nh = ( self.npbase - nd ) // 2
        drift = 2 * math.pi * xdata * self.pm.result( xdata, params[:nd] )
        amps = self.getAmplitudes( xdata, params )
        cx = numpy.cos( drift )
        sx = numpy.sin( drift )
        dpm = 2 * math.pi * xdata * self.pm.basePartial( xdata, params ).transpose()
        part[:,:nd]      = ( ( amps[1] * cx * dpm ).transpose() -
                             ( amps[0] * sx * dpm ).transpose() )
        part[:,nd:nd+nh] = ( cx * self.cm.basePartial( xdata, params ).transpose() ).transpose()
        part[:,nd+nh:]   = ( sx * self.sm.basePartial( xdata, params ).transpose() ).transpose()
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
        nd = self.degree + 1
        drift = 2 * math.pi * xdata * self.pm.result( xdata, params[:nd] )
        cx = numpy.cos( drift )
        sx = numpy.sin( drift )
        pdx = self.pm.baseDerivative( xdata, params )
        cdx = cx * pdx
        sdx = sx * pdx
        amps = self.getAmplitudes( xdata, params )
        cadx = self.cm.baseDerivative( xdata, params )
        sadx = self.sm.baseDerivative( xdata, params )
        return 2 * math.pi * ( cadx * cx - amps[0] * sdx + sadx * sx + amps[1] * cdx )

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
        nd = self.degree + 1
        nh = ( self.npbase - nd ) // 2
        return ( self.cm.result( xdata, params[nd:nd+nh] ),
                 self.sm.result( xdata, params[nd+nh:] ) )

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return ( "SineSplineDrift: f( x:p ) = spline_0 * cos( poly ) + " +
                 "spline_1 * sin( poly )" )

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



