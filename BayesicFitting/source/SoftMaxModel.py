import numpy as numpy
from astropy import units
import math
from . import Tools
from .Tools import setAttribute as setatt
from .Formatter import formatter as fmt
from .Formatter import fma

from .NonLinearModel import NonLinearModel

__author__ = "Do Kester"
__year__ = 2021
__license__ = "GPL3"
__version__ = "2.8.0"
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
#  *    2020 - 2021 Do Kester


class SoftMaxModel( NonLinearModel ):
    """
    Softmax Model is a generalization of the LogisticModel over multiple outputs

                       exp( sum_k( x_k * p_kn ) + q_n ) )
        f_n( x:p ) = -------------------------------------------
                     sum_i( exp( sum_k( x_k * p_ki ) + q_i ) ) )




        0       0       0       0       0       0   K inputs
        |\     /|\     /|\     /|\     /|\     /|

          all inputs connect to all outputs        K*N parameters

           \|/     \|/     \|/     \|/     \|/     N offsets (if offset)
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

        setatt( self, "offset", offset )
        setatt( self, "in2out", in2out )
        setatt( self, "ndout", ndout )
        setatt( self, "normed", normed )

        super( ).__init__( np, ndim=ndim, copy=copy, params=param, **kwargs )

    def copy( self ):
        """ Copy method.  """
        return SoftMaxModel( ndim=self.ndim, ndout=self.ndout, normed=self.normed,
                                   offset=self.offset, copy=self )

    def unnormedResult( self, xdata, params ):
        """
        Returns the unnormalized result of the model function: F_n( x_k ) as array of
        shape [nx,ndout], where nx number of data points and ndout is the number of
        outputs.

        Note: This is the same for dfdz

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        ## xdata.shape = [nx,nin]

        par = params[:self.in2out]
        if self.ndim == 1 :
            z = numpy.outer( xdata, par )
        else :
            z = numpy.inner( xdata, par.reshape( self.ndout, self.ndim ) )
        if self.offset :
            z += params[self.in2out:]

        return numpy.exp( z )

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
        res = self.unnormedResult( xdata, params )

        if self.normed :
            norm = numpy.sum( res, axis=1 )
#            print( fma( res ) )
#            print( "NORM  ", fma( norm ) )
            res = ( res.T / norm ).T
#            print( fma( res ) )

#        return res
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
        ## npars = nin * ndout
        ## list: ndout times [nx,npars]

        shp = ( Tools.length( xdata ), self.npbase )

        partial = [numpy.zeros( shp, dtype=float ) for k in range( self.ndout )]

        dudz = self.unnormedResult( xdata, params )     ## shape = [nx,ndout]

        if not self.normed :
            i2o = numpy.arange( self.ndim, dtype=int )
            koff = self.in2out

            print( "MLM1   ", dudz.shape, xdata.shape )
            for n in range( self.ndout ) :
                partial[n][:,i2o] = ( dudz[:,n] * xdata.T ).T
                i2o += self.ndim
                if self.offset :
                    partial[n][:,koff] = dudz[:,n]
                    koff += 1
            return partial if self.ndout > 1 else partial[0]

        ## Normalized case

        f = dudz
        norm = numpy.sum( f, axis=1 )
        n2 = norm * norm    

#        print( "SMM  dudz  ", fmt( dudz ), fmt( norm ) )

        xd = xdata if self.ndim > 1 else xdata.reshape( -1, 1 ) 
        for i in range( self.ndout ) :

            ## k counts inputs; n count outputs.
            k = 0
            n = 0
            for pk in range( self.in2out ) :
                if i == n :
                    partial[i][:,pk] = xd[:,k] * f[:,n] * ( norm - f[:,n] ) / n2
                else :
                    partial[i][:,pk] = - xd[:,k] * f[:,n] * f[:,i] / n2

                k += 1
                if k == self.ndim :
                    k = 0
                    n += 1
            for pk in range( self.in2out, self.npbase ) :
                n = pk - self.in2out
                if i == n :
                    partial[i][:,pk] = f[:,n] * ( norm - f[:,n] ) / n2
                else :
                    partial[i][:,pk] = - f[:,n] * f[:,i] / n2


        return partial if self.ndout > 1 else partial[0]


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
        nx = Tools.length( xdata )
        dfdx = numpy.zeros( (self.ndout, nx, self.ndim ), dtype=float )

        par = params[:self.in2out].reshape( self.ndout, self.ndim )

        dudz = self.unnormedResult( xdata, params )

#        print( "Deriv   ", xdata.shape, par.shape, dudz.shape, dfdx.shape )

        if not self.normed :
            for n in range( self.ndout ) :
                for k in range( self.ndim ) :
                   dfdx[n,:,k] =  dudz[:,n] * par[n,k]
            return dfdx

        ## Normalized case

        dfdz = self.dfdz( dudz )               ## shape = [nx,ndout,ndout]

#        print( "DerivN  ", xdata.shape, par.shape, dfdz.shape, dfdx.shape )

        for n in range( self.ndout ) :
            for k in range( self.ndim ) :
#                print( n, k, o2i )
                dfdx[n,:,k] =  numpy.sum( dfdz[:,:,n] * par[:,k], axis=1 )

        return dfdx


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
        return 1 / self.xUnit


############## TBD ##########################

    def dfdz( self, f ) :
        """
        Returns the derivative of the normalized results of f(z) = exp(z):

           y(z) = f(z) / SUM( f(z) 

        where the sum is over the second index: ndout

        Parameters
        ----------
        f : array_like [nxdata,ndout]
            function

        """
        norm = numpy.sum( f, axis=1 )
        n2 = norm * norm
        shp = ( Tools.length( f ), self.ndout, self.ndout )
        dfdz = numpy.zeros( shp, dtype=float )
        
        for n in range( self.ndout ) :
            for k in range( self.ndout ) :
                dfdz[:,k,n] = - ( f[:,k] * f[:,n] / n2 )
            dfdz[:,n,n] = ( ( norm - f[:,n]  ) * f[:,n] / n2 ).T


#        print( "dfdz   ", dfdz.shape )
#        print( fma( dfdz[0,:,:] ) )

        return dfdz


