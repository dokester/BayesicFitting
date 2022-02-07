import numpy as numpy
from astropy import units
import math
from . import Tools
from . import NeuralNetUtilities
from .Tools import setAttribute as setatt
from .Formatter import formatter as fmt
from .Formatter import fma

from .NonLinearModel import NonLinearModel

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
#  *    2020 - 2022 Do Kester


class SoftMaxModel( NonLinearModel ):
    """
    Softmax Model is a Logistic model if the number of outputs is 1.
    Otherwise it is generalization of the LogisticModel over multiple outputs

                       exp( sum_k( x_k * p_kn ) + q_n ) )
        f_n( x:p ) = -------------------------------------------
                     sum_i( exp( sum_k( x_k * p_ki ) + q_i ) ) )


        0       0       0       0       0       0   I inputs
        |\     /|\     /|\     /|\     /|\     /|

          all inputs connect to all outputs        I*N connecting parameters

           \|/     \|/     \|/     \|/     \|/      N offset parameters (if offset)
            0       0       0       0       0       N outputs



    The parameters (p) are initialized at 1.0, except the offset (q).
    They are initialized at 0.0.



    Attributes
    ----------
    offset : bool
        True : the outputs have offsets
    ndout : int
        number of output categories
    in2out : int
        ndim * ndout
    normed : bool
        the results are normalized (def:True)

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

    def __init__( self, ndim=1, ndout=1, copy=None, offset=False, normed=True, **kwargs ):
        """
        Logistic response model.

        Number of parameters is npars (see offset)

        Parameters
        ----------
        ndim : int
            number of inputs
        ndout : int
            number of classifications
        offset : bool
            False : no offsets                  npars = ndim * ndout
            True  : each output has one offset: npars = ndim * ndout + ndout
        normed : bool
            True : output is normalized
            False : not
        copy : SoftMaxModel
            to be copied

        """
        in2out = ndim * ndout
        param = [1.0] * in2out
        np = in2out

        if offset :
            param += [0.0] * ndout
            np += ndout

        if offset :
            raster = NeuralNetUtilities.ConnectWithBias( ndim=ndim, ndout=ndout )
        else :
            raster = NeuralNetUtilities.Connect( ndim=ndim, ndout=ndout )

        if normed :
            if ndout == 1 :
                trans = NeuralNetUtilities.Logistic()
            else :
                trans = NeuralNetUtilities.Softmax( ndout=ndout )
        else : 
            trans = NeuralNetUtilities.Identity()

        setatt( self, "raster", raster )
        setatt( self, "trans", trans )

        setatt( self, "offset", offset )
        setatt( self, "in2out", in2out )
        setatt( self, "ndout", ndout )
        setatt( self, "normed", normed )

        super( ).__init__( np, ndim=ndim, copy=copy, params=param, **kwargs )

    def copy( self ):
        """ Copy method.  """
        return SoftMaxModel( ndim=self.ndim, ndout=self.ndout, normed=self.normed,
                                   offset=self.offset, copy=self )

    def baseResult( self, xdata, params ):
        """
        Returns the result of the model function: F_n( x_k ) as array of
        shape [nx,ndout], where nx number of data points and ndout is the number of
        outputs.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        res = self.trans.result( self.raster.result( xdata, params ), params )

        return res if self.ndout > 1 else res[:,0]

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value as a list (size N) of arrays
        of shape (K,P). N is #outputs; K is #datapoints; P is #parameters.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the partials
        params : array_like
            values for the parameters.
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        dfdr = self.trans.derivative( self.raster.result( xdata, params ), params )
        drdp = self.raster.partial( xdata, params )

        part = self.trans.pipe( dfdr, drdp )

        return part[0,:,:] if self.ndout == 1 else list( part ) 

    def baseDerivative( self, xdata, params ) :
        """
        Return the derivative df_i/dx_n of each output f_i to the data x_n
        at each xdata (=x).
        It is returned as an array of shape (N,I) of an array of length K.
        N is #outputs; I is #inputs (ndim); K is #datapoints.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        dfdr = self.trans.derivative( self.raster.result( xdata, params ), params )
        drdx = self.raster.derivative( xdata, params )

        der = self.trans.pipe( dfdr, drdx )

        if self.ndout == 1 :
            return der[0,:,0] if self.ndim == 1 else der[0,:,:] 
        else :
            return der[:,:,0].T if self.ndim == 1 else list( der )


    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        return str( "SoftMax: f_n( x:p ) = exp( sum_i( x_i * p_in ) + q_n)/ sum_n )" )


    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.

        """
        xu = 1 if k > self.ndim * self.ndout else ( self.xUnit if self.ndim == 1 else self.xUnit[k % self.ndim] )
        return units.Unit( 1 ) / xu

