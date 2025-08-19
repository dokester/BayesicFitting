import numpy as numpy
from .Model import Model

from .Formatter import formatter as fmt


__author__ = "Do Kester"
__year__ = 2025
__license__ = "GPL3"
__version__ = "3.2.4"
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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2003 - 2014 Do Kester, SRON (JAVA code)
#  *    2016 - 2025 Do Kester

class LinearModel( Model ):
    """
    Anchestor of all linear models.

    LinearModel implements the baseResult method needed in all linear models.

    For Linear models it holds that

     f( x:p ) = &sum;( p_i * df( x )/dp_i )

    which means that only the partial derivatives to p_i need to be given
    as basePartial. The baseResult follows directly from that one.
    It is implemented here.

    Attributes
    ----------
    None of its own

    Attributes from Model
    ---------------------
        parameters, stdevs, npchain, _next, _head, _operation, xUnit, yUnit (relegated to model)

    Attributes from FixedModel
    --------------------------
        npmax, fixed, parlist, mlist

    Attributes from BaseModel
    --------------------------
        npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames

    Author       Do Kester


    """
    def __init__( self, nparams, ndim=1, copy=None, **kwargs ):
        """
        class for all linear models.

        Parameters
        ----------
        nparams : int
            the number of parameters in this model
        ndim : int
            the dimensionality of the inputs (default: 1)
        copy : LinearModel
            model to be copied (default: None)
        kwargs : dict
            Possibly includes keywords from
                @Model :        params
                @FixedModel :   fixed, names
                @BaseModel :    posIndex, nonZero

        """
        super( LinearModel, self ).__init__( nparams, ndim=ndim, copy=copy, **kwargs )

    def baseResult( self, xdata, params ):
        """
        Returns the base result of linear models.

        for linear models the result is the inner product of parameters
        and partial derivatives.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        part = self.basePartial( xdata, params )

        res = numpy.zeros( part.shape[0], dtype=float )

        ## params might be a heterogeneous list of float or [float] from FixedModel
        ## numpy.inner does not work here
        for k in range( self.npmax ) :
            res += params[k] * part[:,k]

        return res
