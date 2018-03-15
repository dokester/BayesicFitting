import numpy as numpy
from astropy import units
import re
import warnings
from . import Tools

from .Dynamic import Dynamic

__author__ = "Do Kester"
__year__ = 2018
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
#  *    2011 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2017 Do Kester

class BaseModel( object ):
    """
    BaseModel implements the common parts of simple Models.

    A simple model is a function in x with parameters p : f(x:p).
    The variable x is an array of points in a space of one or more
    dimensions; p can have any dimension, including 0 i.e. the model
    has no parameters.

    The result of the function for certain x and p is given by
    `model.result( x, p )`

    The partial derivatives of f to p (df/dp) is given by
    `model.partial( x, p )`
    Some fitters make use of the partials

    The derivative of f to x (df/dx) is given by
    `model.derivative( x, p )`

    BaseModel checks parameters for positivity and nonzero-ness, if such
    is indicated in the model itself.

    BaseModel also implements the numerical calculation of the (partial)
    derivatives to be used when they are not given in the model definition
    itself.

    Attributes
    ----------
    npbase : int
        number of params in the base model
    ndim : int
        number of dimensions of input. (default : 1)
    posIndex : list of int
        list of indices indication positive-definite parameters.
        (default : none)
    nonZero : list of int
        list of parameters that need a warning when they are equal to zero.
        (default : none)
        Warnings will only be issued once. Values are replaced by self.tiny
    tiny : float
        very small value, replacing zero valued when found on NonZero.
        (default : 1e-20)
    deltaP : array_like
        (list of) width(s) for numerical partial calculation. (default : 0.00001)
    parNames : list of str
        list of parameter names. (default : ``parameter_k``)

    Author :         Do Kester

    """

    #  *************************************************************************
    def __init__( self, nparams=0, ndim=1, copy=None, fixed=None, names=None,
                        posIndex=[], nonZero=[] ):
        """
        BaseModel Constructor.
        <br>
        Parameters
        ----------
        nparams : int
            Number of parameters in the model (default: 0)
        ndim : int
            Number of dimensions of the input (default: 1)
        copy : BaseModel
            to be copied
        names : list of string
            names for the parameters

        """
        super( BaseModel, self ).__init__( )
        object.__setattr__( self, "npbase", 0 )
        object.__setattr__( self, "ndim", 1 )

        if copy is None :
            self.npbase    = nparams
            self.ndim      = ndim
            self.posIndex  = posIndex
            self.nonZero   = nonZero
            self.deltaP    = [0.00001]
            self.tiny      = 1e-20
            if names is None :
                self.parNames = ["parameter_%d"%k for k in range( self.npbase )]
            else :
                self.parNames = self.selectNames( names )
        else :
            self.npbase   = copy.npbase
            self.ndim     = copy.ndim
            self.posIndex = copy.posIndex.copy()
            self.nonZero  = copy.nonZero.copy()
            self.deltaP   = copy.deltaP.copy()
            self.tiny     = copy.tiny
            self.parNames = copy.parNames[:]

    def __setattr__( self, name, value ):
        """
        Set attributes.

        """
        keys = {"posIndex":int, "nonZero":int, "deltaP":float, "parNames":str}
        key1 = {"npbase":int, "ndim":int, "tiny":float }
        if ( Tools.setListOfAttributes( self, name, value, keys ) or
             Tools.setSingleAttributes( self, name, value, key1 ) ) :
            pass
        else :
            raise AttributeError(
                "Model has no attribute " + name + " of type " + str( value.__class__ ) )

    #  *****RESULT**************************************************************
    def result( self, xdata, param ):
        """
        Returns the result calculated at the xdatas.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        param : array_like
            values for the parameters.

        """
        self.checkParameter( param )
        return self.baseResult( xdata, param )

    #  *****PARTIAL*************************************************************
    def partial( self, xdata, param, parlist=None ):
        """
        Returns the partial derivatives calculated at the inputs.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        param : array_like
            values for the parameters.
        parlist : None or array_like
            indices of active parameters

        """
        self.checkParameter( param )
        return self.basePartial( xdata, param, parlist=parlist )

    def checkParameter( self, param ) :
        """
        Return parameters corrected for positivity and Non-zero.

        Parameters
        ----------
        param : array_like
            values for the parameters.

        """
        self.checkZeroParameter( param )
        self.checkPositive( param )
        return param

    def checkPositive( self, param ) :
        """
        Check parameters for positivity. Silently correct.

        Parameters
        ----------
        params : array_like
            values for the parameters

        """
        for k in self.posIndex :
            param[k] = abs( param[k] )

    def checkZeroParameter( self, param ):
        """
        Check parameters for Non-zero. Correct after one warning.

        Parameters
        ----------
        params : array_like
            values for the parameters

        """
        for k in self.nonZero :
            if param[k] == 0 :
                msg = ( ( self.shortName() + ": " + self.baseParameterName( k ) +
                            " ( =parameter[%d] ) equals zero."%k ) )
                warnings.warn( msg )
                param[k] = self.tiny

    def isDynamic( self ) :
        """
        Whether the model implements Dynamic
        """
        return isinstance( self, Dynamic )

    #  *****TOSTRING***********************************************************
    def __str__( self ):
        """ Returns a string representation of the model.  """
        return self.baseName( )

    def shortName( self ):
        """
        Return a short version the string representation: upto first non-letter.

        """
        m = re.match( "^[a-zA-Z_]*", self.baseName() )
        return m.group(0)

    def derivative( self, xdata, param ) :
        """
        Returns the derivative of the model to xdata.

        It is a numeric derivative as the analytic derivative is not present
        in the model.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the derivative
        param : array_like
            values for the parameters. (default: self.parameters)

        """
        return self.baseDerivative( xdata, params )

    def setPrior( self, k, prior=None, limits=None ) :
        """
        set the prior and/or limits for the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.
        prior : Prior
            prior for the parameter
        limits : [float,float]
            [low,high] limits on the prior.

        """
        np = len( self.priors )
        if prior is None :
            if np == 0 :
                self.priors = [UniformPrior( limits=limits )]
                return
            else :
                prior = self.basePrior( k )

        prior.setLimits( limits )

        if k == np :
            self.priors += [prior]
        elif k > np :
            k = -1
        self.priors[k] = prior
        return


    def getPrior( self, k ) :
        """
        Return the prior of the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.
        """
        return self.basePrior( k )

    def basePrior( self, k ) :
        """
        Return the prior of the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.
        """
        np = len( self.priors )
        if np == 0 :
            raise IndexError( "The model does not have priors." )
        if k < np:
            return self.priors[k]
        else :
            return self.priors[-1]

    def getParameterName( self, k ) :
        """
        Return the name of the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.
        """
        return self.baseParameterName( k )


    def baseParameterName( self, k ) :
        """
        Return the name of the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.
        """
        return self.parNames[k]

    def getParameterUnit( self, k ) :
        """
        Return the unit of the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.
        """
        return self.baseParameterUnit( k )

    def baseParameterUnit( self, k ) :
        """
        Return the name of the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.
        """
        return units.Unit( 1.0 )

