import numpy as numpy
from .Model import Model

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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2003 - 2014 Do Kester, SRON (JAVA code)
#  *    2016 - 2017 Do Kester

class LinearModel( Model ):
    """
    Anchestor of all linear models.

    LinearModel implements the baseResult method needed in all linear models.

    For Linear models it holds that
    .. math::
        f( x:p ) = \sum( p_i * f^\prime( x ) )

    which means that only the partial derivatives to :math:`p_i`,
    the :math:`f^\prime( x )`, need to be given as ``basePartial``.
    The ``baseResult`` follows from that one.
    It is implemented here.


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
        parlist = numpy.arange( self.npmax )
        part = self.basePartial( xdata, params, parlist=parlist  )

#        print( "LM  ", params )
#        print( "LM  ", part )
#        print( "LM  ", parlist )
#        try :
#            return numpy.inner( params, part )
#        except ValueError :
#            print( "LinearModel: ValueError" )
#            pass

        res = numpy.zeros( part.shape[0], dtype=float )
        for k in parlist :
            res += params[k] * part[:,k]


#        for k,p in enumerate( params ) :
#            res += p * part[:,k]
        return res

