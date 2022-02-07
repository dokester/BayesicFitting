import numpy as numpy
from astropy import units
from astropy.modeling import Model as AstroModel
from astropy.modeling import FittableModel
import math
from . import Tools
from .Tools import setAttribute as setatt
from .Formatter import formatter as fmt

from .Model import Model

__author__ = "Do Kester"
__year__ = 2022
__license__ = "GPL3"
__version__ = "3.0.0"
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
#  *    2021        Do Kester


class AstropyModel( Model ):
    """
    Wrapper for Astropy Models, so they can be used in BayesicFitting.

    Examples
    --------
    >>> from astropy.modelling.models import Gaussian1D
    >>> gm = Gaussian1D( mean=0, stddev=1, amplitude=1 )
    >>>
    >>> gauss = AstropyModel( gm )
    >>> print( gauss )
    AstropyModel( Gauss1D )
    >>> print( gauss.getNumberOfParameters( ) )
    3
    >>> print( gauss( numpy.linspace( -5, 5, 11 ) ) )
    [  3.72665317e-06   3.35462628e-04   1.11089965e-02   1.35335283e-01
       6.06530660e-01   1.00000000e+00   6.06530660e-01   1.35335283e-01
       1.11089965e-02   3.35462628e-04   3.72665317e-06]

    Attributes
    ----------
    astromodel : astropy.modeling.FittableModel
        The astropy model to be wrapped

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
    `GaussModel()` is equivalent to `KernelModel( kernel=Gauss() )`.


    """

    def __init__( self, astromodel, copy=None, **kwargs ):
        """
        Gaussian model.

        Number of parameters is 3.

        Parameters
        ----------
        fitmodel : FittableModel
            FittableModel from astropy.modeling  
        copy : GaussModel
            to be copied
        fixed : None or dictionary of {int:float|Model}
            int         index of parameter to fix permanently.
            float|Model values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
            See: @FixedModel

        """

        setatt( self, "astromodel", astromodel, type=FittableModel )
        
        npars = len( astromodel.parameters )
        ndim = astromodel.n_inputs
        ndout = astromodel.n_outputs
        if ndout > 1 :
            setatt( self, "ndout", ndout )

        super( ).__init__( npars, ndim=ndim, names=astromodel.param_names, 
                           params=astromodel.parameters, copy=copy, **kwargs )


    def copy( self ):
        """ Copy method.  """
        return AstropyModel( self.astromodel.copy(), copy=self )

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
        if self.ndim == 1 :
            return self.astromodel.evaluate( xdata, *tuple( params ) )
        else :
            xd = list( xdata.T )
            return self.astromodel.evaluate( *tuple( xd ), *tuple( params ) )

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            values for the parameters.
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        if self.ndim == 1 :
            ap = self.astromodel.fit_deriv( xdata, *tuple( params ) )
        else :
            xd = list( xdata.T )
            ap = self.astromodel.fit_deriv( *tuple( xd ), *tuple( params ) )
    
        if isinstance( ap, list ) :
            ap = numpy.asarray( ap ).T

        if parlist is None :
            return ap

        partial = numpy.ndarray( ( Tools.length( xdata ), self.npbase ) )
        for k,kp in enumerate( parlist ) :
            partial[:,k] = ap[:,kp]

        return partial

    def baseDerivative( self, xdata, params ) :
        """
        Return the derivative df/dx at each xdata (=x).

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        self.numDerivative( xdata, params )

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        name = str( self.astromodel )
        ke = name.find( "\n" )
        return str( "AstropyModel( %s )" % name[7:ke] )



