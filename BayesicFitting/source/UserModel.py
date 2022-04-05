import numpy as numpy
from astropy import units
from astropy.modeling import Model as AstroModel
import math
import warnings
from . import Tools
from .Tools import setAttribute as setatt

from .Model import Model

__author__ = "Do Kester"
__year__ = 2022
__license__ = "GPL3"
__version__ = "3.0.1"
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


class UserModel( Model ):
    """
    Wrapper for a Models where the User provides the method the evaluate
    f( x: p ) as userResult( x, param )

    and optionally the partial derivatives to p and x and a name

    df/dp as  userPartial( x, param )
    df/dx as  userDeriv( x. param )
    name  as  string


    Examples
    --------
    import numpy as np
    >>> def ur( x, p ) :
    >>>     return p[0] * np.sin( p[1] * x + p[2] * np.log( x + p[3] ) ) 
    >>> 
    >>>
    >>> mdl = UserModel( 4, ur, userName="slowchirp" )
    >>> print( mdl )
    UserModel( slowchirp )
    >>> print( mdl.npars )
    4


    Attributes
    ----------
    userResult : callable
        method to evaluate the result of the F(x:p)
        defined as method( x, p )
    userPartial : callable
        method to evaluate the partial derivatives df/dp
        defined as method( x, p ). Default: numeric derivative
    userDerivative : callable
        method to evaluate the derivative df/dx
        defined as method( x, p ). Default: numeric derivative
    userName : str
        name of the class

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

    def __init__( self, npars, userResult, ndim=1, userPartial=None, userDeriv=None, 
                  userName="unknown", copy=None, **kwargs ):
        """
        User provided model.

        Parameters
        ----------
        npars : int
            number of parameters of this model
        userResult : callable
            method of the form userResult( x, p )
            where x is the independent variable; array_like
                  p is the parameter vector; array_like 
        ndim : int
            number of input streams.
        userPartial : callable
            method of the form userPartial( x, p )
            where x is the independent variable; array_like
                  p is the parameter vector; array_like 
        userDeriv : callable
            method of the form userDeriv( x, p )
            where x is the independent variable; array_like
                  p is the parameter vector; array_like 
        userName : str
            Name for this model
        copy : UserModel
            to be copied

        """

        self.setMethod( "userResult", userResult )

        super( ).__init__( npars, ndim=ndim, copy=copy, **kwargs )

        if copy is not None :
            setatt( self, "userPartial", copy.userPartial )
            setatt( self, "userDerivative", copy.userDerivative )
            setatt( self, "userName", copy.userName, type=str )
        else :
            self.setMethod( "userPartial", userPartial, numeric=self.numPartial )
            self.setMethod( "userDerivative", userDeriv, numeric=self.numDerivative )
            setatt( self, "userName", userName, type=str )

    def copy( self ):
        """ Copy method.  """
        return UserModel( self.npars, self.baseResult, ndim=self.ndim, copy=self )

    def setMethod( self, name, userMethod, numeric=None ) :
        if callable( userMethod ) :
            setatt( self, name, userMethod )
        elif callable( numeric ) :
            setatt( self, name, numeric )
            warnings.warn( "Using numeric approximations for %s" % name )
        else :
            raise ValueError( "%s %s is not callable" % ( name, str( userMethod ) ) )

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
        return self.userResult( xdata, params )

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
        if parlist is None :
            return self.userPartial( xdata, params )
        else :
            return self.userPartial( xdata, params )[parlist]

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
        return self.userDerivative( xdata, params )

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return str( "UserModel( %s )" % self.userName )



