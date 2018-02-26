from .Model import Model
from . import Tools

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

class NonLinearModel( Model ):
    """
    Anchestor of all non-linear models.

    The general non-linear model needs both the function value and the partials.

    It contains provisions for mixed models. (TBC)

    Hidden Attributes:
        _linear     set of indices for the linear parameters (in case of a mixed model)

    @author Do Kester

    """
    def __init__( self, nparams, ndim=1, copy=None, **kwargs ):
        """
        Parent class for all non linear models.

        Parameters
        ----------
        nparams : int
            number of parameters in the model
        ndim : int
            dimensionality of the input. Default 1
        copy : NonLinearModel
            model to be copied.

        """
        super( NonLinearModel, self ).__init__( nparams, ndim=ndim, copy=copy, **kwargs )
        if copy is None : self._linear = set()
        else : self._linear = copy._linear.copy()

    def __setattr__( self, name, value ) :
        """
        Set attributes: _linear

        """
        dic = {'_linear':set}
        if not Tools.setSingleAttributes( self, name, value, dic ) :
            super( NonLinearModel, self ).__setattr__( name, value )

    def setMixedModel( self, lindex ):
        """
        Convert a NonLinear model into a Mixed model with linear and
        non-linear parameters.

        Reset with SetMixedModel( null );

        Parameters
        ----------
        lindex : list of int
            indices of the linear parameters

        """
        if lindex is None:
            self._linear = set()
        else:
            self._linear = set( lindex )

    def isMixed( self ):
        """ Returns true when linear indices have been set  """
        return len( self._linear ) > 0

    def getNonLinearIndex( self ):
        """ Returns the index of the non-linear parameters.  """

        np = self.getNumberOfParameters()
        return set( [x for x in range( np )] ) - self._linear

    def partial( self, xdata, param=None, useNum=False ):
        """
        Return the partial derivatives for the model.

        Parameters
        ----------
        xdata : array_like
            the value at which to calculate the partials
        param : array_like
            the parameters of the model. Default the self.parameters
        useNum : boolean
            if True use numeric partial derivatives. Default False

        """
        if param is None :
            param = self.parameters
        return super().partial( xdata, param, useNum  )

