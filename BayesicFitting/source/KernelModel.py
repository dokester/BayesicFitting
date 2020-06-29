import numpy as numpy
from astropy import units
import math
from . import Tools
from .Tools import setAttribute as setatt

from .NonLinearModel import NonLinearModel
from .kernels.Kernel import Kernel
from .kernels.Biweight import Biweight

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

class KernelModel( NonLinearModel ):
    """
    Kernel Model, a Model build around an @Kernel.

    The KernelModel is defined as

        f( x:p ) = p_0 * K( ( x - p_1 ) / p_2 )

    where K( u ) is a selectable kernel function on the rescaled input u
        u = ( x - p_1 ) / p_2.

        p_0 is the amplitude
        p_1 is the center
        p_2 is the range.

    The parameters are initialized at {amp,0,1}. the amplitude is such that the
    function integrates to 1.0. They are listed in the table.

    Several kernel functions predefined.

    Beware: The "bound" models are unaware of anything outside their range.

    Author:      Do Kester

    Examples
    --------
    >>> model = KernelModel( )
    >>> model.kernel = Triweight()

    Attributes
    ----------
    kernel : Kernel
        the kernel of this model

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
    def __init__( self, copy=None, kernel=Biweight(), **kwargs ):
        """
        Kernel Model.

        Parameters
        ----------
        copy : KernelModel
            model to be copied
        kernel : Kernel
            kernel class (default = Biweight)
        fixed : None or dictionary of {int:float|Model}
            int         index of parameter to fix permanently.
            float|Model values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
            See: @FixedModel

        """
        amp = 1.0 / kernel.integral
        param = [amp, 0.0, 1.0]
        names = ["amplitude", "center", "width"]

        super( KernelModel, self ).__init__( 3, copy=copy, params=param,
                    names=names, **kwargs )

        self.kernel = kernel
        if copy is None :
            self.posIndex = [2]
            self.nonZero = [2]

    def copy( self ):
        """
        Copy method.
        """
        return KernelModel( copy=self, kernel=self.kernel )

    def __setattr__( self, name, value ) :
        if name == "kernel" and isinstance( value, Kernel ) :
            setatt( self, name, value )
        else :
            super( KernelModel, self ).__setattr__( name, value )


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
        x = ( xdata - params[1] ) / params[2]
        return params[0] * self.kernel.result( x )

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the xdata value.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        partial = numpy.ndarray( ( Tools.length( xdata ), self.npbase ) )
        x = ( xdata - params[1] ) / params[2]
        dfdx = self.kernel.partial( x )

        parts = { 0 : ( lambda: self.kernel.result( x ) ),
                  1 : ( lambda: -params[0] * dfdx / params[2] ),
                  2 : ( lambda: -params[0] * dfdx * x / params[2] ) }

        if parlist is None :
            parlist = range( self.npmax )

        for k,kp in enumerate( parlist ) :
            partial[:,k] = parts[kp]()

        return partial


    def baseDerivative( self, xdata, params ):
        """
        Returns the derivative at the xdata value.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        x = ( xdata - params[1] ) / params[2]
        return params[0] * self.kernel.partial( x ) / params[2]

    def baseName( self ):
        """ Returns a string representation of the model.  """
        return self.kernel.name( )

    def isBound( self ):
        """
        Return true when the kernel is bound.
        All non-zero values are between -1 and +1

        """
        return self.kernel.isBound( )

    def baseParameterUnit( self, k ):
        """
        Return the name of a parameter.
        Parameters
        ----------
        k : int
            the kth parameter.

        """
        if k == 0:
            return self.yUnit
        return self.xUnit


