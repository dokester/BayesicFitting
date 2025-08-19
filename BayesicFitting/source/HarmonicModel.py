import numpy as numpy
from astropy import units
import math
from . import Tools
from .Tools import setAttribute as setatt

from .LinearModel import LinearModel

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
#  *    2007 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2025 Do Kester

class HarmonicModel( LinearModel ):
    """
    Harmonic oscillator Model.

    For order = N and period = 1 :
     f( x:p ) = &sum;_j ( p_k * cos( 2*&pi;*j*x ) + p_{k+1} * sin( 2*&pi;*j*x ) )
     for j = 1:N; and k = 0:2N:2.

    Otherwise scale with period :
     x = x / period

    The number of parameters is 2 * order.
    The parameters are initialized at 1.0. It is a linear model.

    Author:      Do Kester

    Examples
    --------
    >>> harm = HarmonicModel( 3 )            # period = 1
    >>> print( harm.npbase )
    >>> 6
    >>> harm = HarmonicModel( 4, 2.7 )        # period = 2.7

    Attributes
    ----------
    order : int
        the order of the harmonic
    period : float
        the length of the period of the fundamental

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
    PARNAMES = ["cosamp_", "sinamp_"]

    def __init__( self, order, period=1.0, copy=None, **kwargs ):
        """
        Harmonic oscillator model.

        Number of parameters is 2 * order.

        Parameters
        ----------
        order : int (>0)
            the number of overtones
        period : float
            length of the period of the fundamental. default 1.0
        copy : HarmonicModel
            model to be copied
        fixed : None or dictionary of {int:float|Model}
            int         index of parameter to fix permanently.
            float|Model values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
            See: @FixedModel

        """
        super( HarmonicModel, self ).__init__( 2 * order, copy=copy, **kwargs )

        self.order = order
        self.period = period

    def copy( self ):
        """ Copy method.  """
        return HarmonicModel( self.order, period=self.period, copy=self )

    def __setattr__( self, name, value ):
        """
        Set attributes: order, period

        """
        if name == 'order' :
            setatt( self, name, value, type=int )
        elif name == 'period' :
            setatt( self, name, value, type=float )
        else :
            super( HarmonicModel, self ).__setattr__( name, value )

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

        Parameters
        ----------
        xdata : array_like
            x values at which to calculate the partials
        params : array_like
            parameters of the model. (ignored in LinearModels)
        parlist : array_like
            list of indices of active parameters

        """
        np = self.npmax if parlist is None else len( parlist )
        ni = Tools.length( xdata )
        partial = numpy.zeros( ( ni, np), dtype=float )

        x = 2 * math.pi * xdata / self.period

        parts = { 0 : ( lambda j : numpy.cos( j * x ) ),
                  1 : ( lambda j : numpy.sin( j * x ) ) }

        if parlist is None :
            parlist = range( self.npmax )

        for k,kp in enumerate( parlist ) :
            j = 1 + kp // 2
            partial[:,k] = parts[kp % 2]( j )

        return partial

    def baseDerivative( self, xdata, params ):
        """
        Returns the partials at the input value.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the partials
        params : array_like
            parameters of the model.

        """
        df = numpy.zeros_like( xdata )
        tp = 2 * math.pi / self.period
        x = tp * xdata
        j = 0
        for k in range( 0, self.npmax, 2 ) :
            j += 1
            df += tp * j * ( params[k+1] * numpy.cos( j * x ) - params[k] * numpy.sin( j * x ) )
        return df

    def baseName( self ):
        """ Returns a string representation of the model.  """
        bn = "Harmonic: f( x:p ) = "
        if self.order == 0 :
            bn += "0"
            return bn

        bn += "p_0 * cos( xx ) + p_1 * sin( xx )"
        j = 2
        for k in range( 2, self.order + 1 ) :
            bn += " + p_%d * cos( %d xx ) + p_%d * sin( %d xx )"%(j,k,j+1,k)
            j += 2
        bn += "; xx = 2 * pi * x / period"
        return bn

    def baseParameterName( self, k ):
        """
        Return the name of the indicated parameter.
        Parameters
        ----------
        k : int
            parameter number.

        """
        return "%s%d"%( self.PARNAMES[k%2], k / 2 )

    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.
        Always : YUnit.
        Parameters
        ----------
        k : int
            parameter number.

        """
        return self.yUnit


