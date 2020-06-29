import numpy as numpy
import math
from . import Tools
from .Tools import setAttribute as setatt
from .NonLinearModel import NonLinearModel
from .LorentzModel import LorentzModel
from .GaussModel import GaussModel

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
#  *    2016 - 2020 Do Kester

class PseudoVoigtModel( NonLinearModel ):
    """
    Approximation of VoigtModel as the sum of a GaussModel and a LorentzModel

        F(x:p) = p_3 * L(x:p) + ( 1 - p_3 ) * G(x:p)

    where L() and G() are the LorentzModel and the GaussModel, resp. and p_3
    is the fractional contribution of them. 0 < p_3 < 1.

    The models takes 4 parameters: amplitude, center frequency, half-width and
    the balance between the models
.
    These are initialised to [1, 0, 1, 0.5].
    Parameter 2 (width) is always kept positive ( >=0 ).

    Examples
    --------
    >>> voigt = PseudoVoigtModel( )
    >>> voigt.setParameters( [5, 4, 1, 0.7] )
    >>> print( voigt( numpy.arange(  41 , dtype=float ) / 5 ) )      # from [0,8]

    Attributes
    ----------
    gauss : GaussModel
        to construct the gauss parts
    lorentz : LorentzModel
        to construct the lorentz parts

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

    def __init__( self, copy=None, **kwargs ):
        """
        PseudoVoigt model.
        <br>
        Number of parameters is 4.

        Parameters
        ----------
        copy : PseudoVoigtModel
            to be copied
        fixed : None or dictionary of {int:float|Model}
            int         index of parameter to fix permanently.
            float|Model values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
            See: @FixedModel

        """
        param = [1.0, 0.0, 1.0, 0.5]
        names = ["amplitude","center","width","balance"]

        super( PseudoVoigtModel, self ).__init__( 4, copy=copy, params=param,
                        names=names, **kwargs )

        setatt( self, "gauss", GaussModel() )
        setatt( self, "lorentz", LorentzModel() )
        if copy is None :
            self.posIndex = [2]

    def copy( self ):
        """ Copy method.  """
        return PseudoVoigtModel( copy=self )

    def __setattr__( self, name, value ):
        """
        Set attributes.

        Parameters
        ----------
        name :  string
            name of the attribute
        value :
            value of the attribute

        """
        if name == "gauss" :
            setatt( self, name, value, type=GaussModel )
        elif name == "lorentz" :
            setatt( self, name, value, type=LorentzModel )
        else :
            super( PseudoVoigtModel, self ).__setattr__( name, value )


    def baseResult( self, xdata, params ):
        """
        Returns the result of the model function.

        Note:
        1. The "balance" parameter (item 3) should be kept between [0..1]
        2. The "width" parameter (item 2)
        the width in the parameter array ( items 2 & 3 ) are kept
        strictly positive. I.e. they are changed when upon xdata they are negative.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        return ( params[3] * self.lorentz.baseResult( xdata, params[:3] ) +
                 ( 1 - params[3] ) * self.gauss.baseResult( xdata, params[:3] ) )

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the xdata value.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            values for the parameters.
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        pl = parlist
        if parlist is not None and 3 in pl :
            pl = parlist.copy()
            pl.remove( 3 )

        pars = params[:3]
        partial = ( params[3] * self.lorentz.basePartial( xdata, pars, parlist=pl ) +
                 ( 1 - params[3] ) * self.gauss.basePartial( xdata, pars, parlist=pl ) )

        if parlist is None or 3 in parlist :
            part3 = self.lorentz.baseResult( xdata, pars ) - self.gauss.baseResult( xdata, pars )
            (n0,n1) = partial.shape
            shp = ( n0, n1+1 )
            pp = numpy.zeros( shp, dtype=float )
            pp[:,:n1] = partial
            pp[:,n1] = part3
            partial = pp

        return partial

    def baseDerivative( self, xdata, params ) :
        """
        Return the derivative df/dx at each xdata (=x).

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the derivative
        params : array_like
            values for the parameters.

        """
        return ( params[3] * self.lorentz.baseDerivative( xdata, params[:3] ) +
                 ( 1 - params[3] ) * self.gauss.baseDerivative( xdata, params[:3] ) )


    def baseName( self ):
        """
        Returns a string representation of the model.
        """
        return str( "PseudoVoigt: p_3 * Lorentz + ( 1 - p_3 ) * Gauss" )

    def baseParameterUnit( self, k ):
        """
        Return the name of a parameter.

        Parameters
        ---------
        k : int
            parameter number.

        """
        if k == 0:
            return self.yUnit
        return self.xUnit


