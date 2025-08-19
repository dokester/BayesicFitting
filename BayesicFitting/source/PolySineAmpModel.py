import numpy as numpy
import math
from . import Tools
from .Tools import setAttribute as setatt
from .LinearModel import LinearModel
from .PolynomialModel import PolynomialModel

__author__ = "Do Kester"
__year__ = 2025
__license__ = "GPL3"
__version__ = "3.2.4"
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
#  *    2016 - 2025 Do Kester

class PolySineAmpModel( LinearModel ):
    """
    Sine of fixed frequency with polynomials as amplitudes.

    Find amplitudes/phases for sinusoidal of a given frequency.

        f( x,y:p ) = P(y) cos( 2 &pi; &omega; x ) + Q(y) sin( 2 &pi; &omega; x )

    P(y), Q(y) are Polynomials of a certain order, n.

    It is a linear model in 2 dimensions, with 2n+2 papameters.

    Examples
    --------
    >>> sine = PolySineAmpModel( 2, 150.0 )        # fixed frequency of 150 Hz

    Attributes
    ----------
    degree : int
        degree of the polynomials
    frequency : float
        frequency of the sine.
    pm : PolynomialModel
        polynomial to be multiplied with the (co)sine

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
    def __init__( self, degree, frequency, copy=None, fixed=None, **kwargs ):
        """
        Sine model of a fixed frequency and polynomials as coefficients.

        Number of parameters is 2n+2.

        Parameters
        ----------
        degree : int
            degree of the polynomials
        frequency : float
            the frequency, &omega;
        copy : PolySineAmpModel
            model to be copied
        fixed : dict
            If not None raise AttributeError.

        Raises
        ------
        AttributeError : When fixed is not None

        """
        if fixed is not None :
            raise AttributeError( "PolySineAmpModel cannot have fixed parameters" )

        super( PolySineAmpModel, self ).__init__( 2*degree+2, ndim=2, copy=copy, **kwargs )

        if copy is None :
            self.frequency = frequency
            self.degree = degree
        else :
            self.frequency = copy.frequency
            self.degree = copy.degree

        setatt( self, "pm", PolynomialModel( degree ) )


    def copy( self ):
        """ Copy method.  """
        return PolySineAmpModel( self.degree, self.frequency, copy=self )

    def __setattr__( self, name, value ) :
        if name == "frequency" :
            setatt( self, name, value, type=float )
        elif name == "degree" :
            setatt( self, name, value, type=int )
        elif name == "pm" :
            raise AttributeError( "Attribute pm can not be set" )
        else :
            super( PolySineAmpModel, self ).__setattr__( name, value )

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

        Parameters
        ----------
        xdata : array_like [2,ndata]
            values at which to calculate the partials
        params : array_like
            parameters of the model (ignored in LinearModels)
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        nxdata = Tools.length( xdata )
        part = numpy.zeros( ( nxdata, self.npbase ), dtype=float )
        x = xdata[:,0]
        y = xdata[:,1]
        cx = numpy.cos( 2 * math.pi * self.frequency * x )
        sx = numpy.sin( 2 * math.pi * self.frequency * x )
        np = self.degree + 1
        for k in range( np ) :
            part[:,k] = cx
            n = k + np
            part[:,n] = sx
            cx *= y
            sx *= y
        return part

    def baseDerivative( self, xdata, params ):
        """
        Returns the derivative of f to (x,y) (df/dx,df/dy) at the input value.

        Parameters
        ----------
        xdata : array_like [2,ndata]
            values at which to calculate the partials
        params : array_like
            parameters of the model

        """
        nxdata = Tools.length( xdata )
        dfdx = numpy.zeros( ( nxdata, 2 ), dtype=float )
        x = xdata[:,0]
        y = xdata[:,1]
        np = self.degree + 1
        tpf = 2 * math.pi * self.frequency
        cx = numpy.cos( tpf * x )
        sx = numpy.sin( tpf * x )
        dfdx[:,0] = tpf * ( self.pm.result( y, params[np:] ) * cx -
                            self.pm.result( y, params[:np] ) * sx )
        dfdx[:,1] = ( self.pm.derivative( y, params[:np] ) * cx +
                      self.pm.derivative( y, params[np:] ) * sx )
        return dfdx

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        np = self.npbase // 2
        bn1 = "PolySineAmp: f( x,y:p ) = ( p_0"
        bn2 = "                          ( p_%d"%np
        if np > 1 :
            bn1 += " + p_1 * y"
            bn2 += " + p_%d * y"%(np+1)
        for k in range( 2, np ) :
            bn1 += " + p_%d * y^%d"%(k,k)
            bn2 += " + p_%d * y^%d"%(np+k,np+k)
        bn1 += " ) * cos( 2 pi * x * f ) +\n" + bn2
        bn1 += " ) * sin( 2 pi * x * f ); f = %f"%self.frequency
        return bn1

    def baseParameterUnit( self, k ):
        """
        Return the name of a parameter.
        Parameters
        ----------
        k : int
            the kth parameter.

        """
        np = self.npbase // 2
        return self.yUnit / ( self.xUnit[1] ** ( k % np ) )


