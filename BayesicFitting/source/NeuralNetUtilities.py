import numpy as numpy
from astropy import units
import math
from . import Tools
from .Tools import setAttribute as setatt
from .Formatter import formatter as fmt


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

##############################################################################
##  This utilities contain a number of classes that can be combined to a    ##
##  Neural Net of arbitrary complexity.                                     ##
##                                                                          ##
##  A Neural Net Model consists of at least one hidden layer of neurons.    ##
##  The inputs are linearly scaled on the first layer.                      ##
##  Optionally a bias can be added to the neurons.                          ##
##  A transfer function is applied to the neurons.                          ##
##  The layer acts as input for the next layer where the same procedure is  ##
##  followed. Until finally it is projected on the output layer.            ##
##                                                                          ##
##############################################################################



class BaseNeuralNetworkUtilities( object ) :


    def pipe( self, dfdr, drdp ) :
        dfdp = numpy.zeros_like( drdp )

        ( ndout, ndata, nip ) = drdp.shape
        for k in range( nip ) :
            for i in range( ndata ) :
                dfdp[:,i,k] = numpy.inner( dfdr[:,i,:], drdp[:,i,k] )

        if ndout == 1 :
            return dfdp[0,:,:]

        return dfdp


class Connect( BaseNeuralNetworkUtilities ):
    """
    Connects one layer to the next.

        0       0       0       0       0       0   K inputs
        |\     /|\     /|\     /|\     /|\     /|

          all inputs connect to all outputs         K*N parameters

           \|/     \|/     \|/     \|/     \|/      N offsets (see ConnectWithBias)
            0       0       0       0       0       N outputs


    Connects layer1 to layer2 via a matrix of [K*N]

    The parameters are initialized at {0.0}.


    Attributes
    ----------
        ndim : int
            number of input parameters
        ndout : int
            number of output parameters
        nraster : int
            ndim * ndout

    """

    def __init__( self, ndim=1, ndout=1 ):

        """
        (Part of) Neural Net.

        Parameters
        ----------
        ndim : int
            number of input columns
        ndout : int
            number of output values, per input row. See also ncat

        """
        self.ndim = ndim
        self.ndout = ndout
        self.nraster = ndim * ndout

        super( ).__init__( )

    def result( self, xdata, params ):
        """
        Returns the result of the model function.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        par = numpy.reshape( params, ( self.ndout, self.ndim ) )
        xd  = numpy.reshape( xdata, ( -1, self.ndim ) )
        return numpy.inner( xd, par )

    def partial( self, xdata, params ) :

        shp = ( self.ndout, Tools.length( xdata ), len( params ) )
        partial = numpy.zeros( shp, dtype=float )

        i2o = numpy.arange( self.ndim, dtype=int )

        for n in range( self.ndout ) :
            partial[n,:,i2o] = xdata.T.copy()
            i2o += self.ndim

        return partial
#        return partial if self.ndout > 1 else partial[0,:,:]
  

    def derivative( self, xdata, params ) :

        nx = Tools.length( xdata )
        dfdx = numpy.zeros( ( self.ndout, nx, self.ndim ), dtype=float )

        par = params.reshape( self.ndout, self.ndim )

        for n in range( self.ndout ) :
            for k in range( self.ndim ) :
               dfdx[n,:,k] = par[n,k]

        return dfdx

class ConnectWithBias( Connect ) :
    """
    Connect as with the previous Connect class and add a bias to layer2
    Using the next N parameters
    """

    def __init__( self, ndim=1, ndout=1 ):
        super( ).__init__( ndim=ndim, ndout=ndout )


    def result( self, xdata, params ):
        return super().result( xdata, params[:self.nraster] ) + params[self.nraster:]

    def partial( self, xdata, params ) :
        pt1 = super().partial( xdata, params[:self.nraster] )
        shp = list( pt1.shape )
        shp[2] += self.ndout
        part = numpy.zeros( shp, dtype=float )
        for k in range( self.ndout ) :
            pt2 = numpy.zeros( ( Tools.length( xdata ), self.ndout ), dtype=float )
            pt2[:,k] = 1
            part[k] = numpy.append( pt1[k], pt2, axis=1 )    

        return part

    def derivative( self, xdata, params ) :
        return super().derivative( xdata, params[:self.nraster] )


######################################################
##                                                  ##
## Hereafter follow a number of transfer functions. ##
##                                                  ##
## Partials are never needed as they dont have      ##
## parameters                                       ##
##                                                  ##
######################################################


class Identity( BaseNeuralNetworkUtilities ) :
    """ 
    Transfer
        f(x) = x 
    """

    def result( self, xdata, params ) :
        return xdata

    def derivative( self, xdata, params ) :
        return numpy.ones_like( xdata )

    def pipe( self, dfdr, drdp ) :
        # dfdr is all 1's
        return drdp


class Arctan( BaseNeuralNetworkUtilities ) :
    """ 
    Transfer
        f(x) = arctan( x ) 
    """

    def result( self, xdata, params ) :
        return numpy.arctan( xdata )

    def derivative( self, xdata, params ) :
        return 1 / ( 1 + xdata * xdata )

    def pipe( self, dfdr, drdp ) :
        dfdp = numpy.zeros_like( drdp )
        dfdrt = dfdr.T
        for k in range( drdp.shape[-1] ) :
            dfdp[:,:,k] = dfdrt * drdp[:,:,k]

        return dfdp


class Logistic( BaseNeuralNetworkUtilities ) :
    """
    To covert outputs to categorical probabilities.
    For 1 choice (category) only: True or False

    Transfer
        f(x) = 1.0 / ( 1.0 + exp( -x ) )

    """
    def result( self, xdata, params ) :
        return 1.0 / ( 1.0 + numpy.exp( -xdata ) )

    def derivative( self, xdata, params ) :
        e = numpy.exp( xdata )
        return e / numpy.square( 1 + e )

    def pipe( self, dfdr, drdp ) :
        dfdp = numpy.zeros_like( drdp )
        dfdrt = dfdr.T
        for k in range( drdp.shape[-1] ) :
            dfdp[:,:,k] = dfdrt * drdp[:,:,k]

        return dfdp

class Heaviside( BaseNeuralNetworkUtilities ) :
    """ 
    Transfer 
        stepfunction at 0 
    """

    def result( self, xdata, params ) :
        return numpy.where( xdata >=0, 1.0, 0.0 )

    def derivative( self, xdata, params ) :
        return numpy.zeros_like( xdata )

    def pipe( self, dfdr, drdp ) :
        return numpy.zeros_like( drdp )

class Softmax( BaseNeuralNetworkUtilities ) :
    """
    To covert outputs to categorical probabilities.
    For more choices (categories): red, green, blue, etc.

    The probabilities are normalized: SUM( f ) = 1

    Transfer 
        f( x_n ) = exp( x_n ) / SUM_i( exp( x_i ) )
    """ 
    def __init__( self, ndout=1 ) :
        self.ndout = ndout

    def result( self, xdata, params ) :
        res = numpy.exp( xdata )
        sum = numpy.sum( res, axis=1 )
        return ( res.T / sum ).T

    def derivative( self, xdata, params ) :
        f = numpy.exp( xdata )
        ndata = xdata.shape[0]

        norm = numpy.sum( f, axis=1 )
        n2 = norm * norm

        shp = ( self.ndout, ndata, self.ndout )
        dfdx = numpy.zeros( shp, dtype=float )

        for n in range( self.ndout ) :
            for k in range( self.ndout ) :
                dfdx[k,:,n] = - ( f[:,k] * f[:,n] / n2 )
            dfdx[n,:,n] = ( ( norm - f[:,n]  ) * f[:,n] / n2 ).T

        return dfdx




