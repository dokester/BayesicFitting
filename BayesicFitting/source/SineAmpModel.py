import numpy as numpy
from astropy import units
import math
from . import Tools
from .Tools import setAttribute as setatt

from .LinearModel import LinearModel

__author__ = "Do Kester"
__year__ = 2021
__license__ = "GPL3"
__version__ = "2.8.0"
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
#  *    2016 - 2021 Do Kester

class SineAmpModel( LinearModel ):
    """
    Sine with fixed frequency.

    Find amplitudes/phases for sinusoidal of a given frequency.

        f( x:p ) = p_0 cos( 2 &pi; &omega; x ) + p_1 sin( 2 &pi; &omega; x )

    where
        p_0 = amplitude of cosine
        p_1 = amplitude of sine
        &omega; is the fixed frequency of the model.

    It is a linear model with 2 parameters.

    Examples
    --------
    >>> sine = SineAmpModel( 150 )        # fixed frequency of 150 Hz

    Attributes
    ----------
    frequency : float
        the (fixed) frequency of the sinusoidal.

    Attributes from Model
    ---------------------
        npchain, parameters, stdevs, xUnit, yUnit

    Attributes from FixedModel
    --------------------------
        npmax, fixed, parlist, mlist

    Attributes from BaseModel
    --------------------------
        npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames

    Alternate
    ---------
    This model is equivalent to
        SineModel( fixed={0:frequency} )

    """
    def __init__( self, frequency, copy=None, **kwargs ):
        """
        Sine model of a fixed frequency.

        Number of parameters is 2.

        Parameters
        ----------
        frequency : float
            the frequency
        copy : SineAmpModel
            model to be copied
        fixed : None or dictionary of {int:float|Model}
            int         index of parameter to fix permanently.
            float|Model values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
            See: @FixedModel

        """
        names = ["cosamp", "sinamp"]
        super( SineAmpModel, self ).__init__( 2, copy=copy, names=names, **kwargs )

        if copy is None :
            self.frequency = frequency
        else :
            self.frequency = copy.frequency

    def copy( self ):
        """ Copy method.  """
        return SineAmpModel( self.frequency, copy=self )

    def __setattr__( self, name, value ) :
        if name == 'frequency' :
            setatt( self, name, value, type=float )
        else :
            super( SineAmpModel, self ).__setattr__( name, value )

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
            list of indices of active parameters

        """
        nxdata = Tools.length( xdata )
        np = self.npmax if parlist is None else len( parlist )
        partial = numpy.zeros( ( nxdata, np ), dtype=float )

        parts = { 0 : ( lambda: numpy.cos( 2 * math.pi * self.frequency * xdata ) ),
                  1 : ( lambda: numpy.sin( 2 * math.pi * self.frequency * xdata ) ) }

        if parlist is None :
            parlist = range( self.npmax )

        for k,kp in enumerate( parlist ) :
            partial[:,k] = parts[kp]()

        return partial

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
        return tpf * ( params[1] * numpy.cos( tpf * xdata ) -
                       params[0] * numpy.sin( tpf * xdata ) )

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return ( "SineAmp: f( x:p ) = p_0 * cos( 2 pi * x * f ) + " +
                 "p_1 * sin( 2 pi * x * f ); f = %f"%self.frequency )

    def baseParameterUnit( self, k ):
        """
        Return the name of a parameter.
        Parameters
        ----------
        k : int
            the kth parameter.

        """
        return self.yUnit


