import numpy as numpy
import numpy.linalg
from astropy import units
import math

from . import Tools
from .Tools import setAttribute as setatt
from .Formatter import formatter as fmt
from .LinearModel import LinearModel
from .kernels.Kernel import Kernel
from .kernels.Tophat import Tophat

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
__version__ = "2.5.3"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Perpetual Beta"

#  *
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
#  *    2010 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2020 Do Kester

class FreeShapeModel( LinearModel ):
    """
    Pixelated Model.

    f( x:p ) = p( expanded )

    where p is a array of amplitudes of the same size as the input x divided by
    the number of pixels per bin ( ppb ). When ppb > 1, each p has a shape which
    is used to fill the pixels of the bin. Initially the shape is a top-hat,
    which can be autoconvolved.

    By default ppb = 5.

    The parameters are initialized at {0}.

    Although this is a LinearModel it will not work very well with the ( linear )
    Fitter. It will be a very ill-posed problem.

    Using NestedSampler its exponential prior will ensure that all
    parameters are kept positive.

    Attributes
    ----------
    npix : int
        Number of pixels in result. Is also npar.
    xlo : float ( default 0 )
        Lowest value in xdata
    xhi : float ( default npix )
        Highest value in xdata
        xlo and xhi define the valid domain of the model.
        All input data must be: xlo <= xdata <= xhi
    shape : Kernel
        shape of convolving function
    center : float (between 0..1)
        position of the center of shape with respect to the pixels

    Attributes from Model
    ---------------------
        npchain, parameters, stdevs, xUnit, yUnit

    Attributes from FixedModel
    --------------------------
        npmax, fixed, parlist, mlist

    Attributes from BaseModel
    --------------------------
        npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames

    Examples
    --------
    >>> nn = 100
    >>> fsm = FreeShapeModel( nn, nconvolve=4, xlo=-1.0, xhi=4.0 )
    >>> print( fsm.shape )

    Author       Do Kester

    """
    def __init__( self, npix, copy=None, shape=None, nconvolve=0,
                  center=0.5, xlo=0, xhi=None, **kwargs ):
        """
        Free Shape model with npix pixels.

        The number of parameters equals the number of pixels

        Parameters
        ----------
        npix : int
            number of pixels = npar
        copy : FreeShapeModel
            model to be copied
        shape : None or Kernel
            None : Use Tophat(), convolved nconvolve times.
            Kernel : use the kernel as shape; nconvolve does not apply.
        nconvolve : int
            number of (auto)convolutions on Tophat
        center : float (between 0..1)
            positions where the pixels are centered.
            default: 0.5 -> pixels run from k to k+1
        xlo : float ( default 0 )
            lowest value in xdata
        xhi : float ( default np )
            highest value in xdata

        """
        super( FreeShapeModel, self ).__init__( npix, copy=copy )

        if copy is None :
            if shape is None :
                setatt( self, "shape", Tophat( nconv=nconvolve ) )
            else :
                self.shape = shape
            self.xlo = xlo
            self.xhi = xhi
            self.center = center

        else :
            setatt( self, "xlo", copy.xlo )
            setatt( self, "xhi", copy.xhi )
            setatt( self, "shape", copy.shape )
            setatt( self, "center", copy.center )

    def copy( self ):
        """ Copy method.  """
        return FreeShapeModel( self.npbase,  copy=self )

    def __setattr__( self, name, value ) :
        if name == "shape" :
            setatt( self, name, value, type=Kernel )
            return
        if name == "xlo" :
            setatt( self, name, value, type=float )
            return
        if name == "xhi" :
            setatt( self, name, self.npbase if value is None else value, type=float )
            return
        if name == "center" and ( 0 <= value <= 1 ) :
            setatt( self, name, value, type=float )
            return

        super( FreeShapeModel, self ).__setattr__( name, value )


    def checkDomain( self, xdata ) :
        """
        Check for all data inside domain defined by (xlo - range, xhi + range).
        range = self.shape.range

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result

        Raises
        ------
        ValueError when outside domain.
        """
        if numpy.any( numpy.logical_or( xdata < self.xlo - self.shape.range,
                                        xdata > self.xhi + self.shape.range ) ) :
            raise ValueError( "Some values are outside domain (%f,%f)" %
                                (self.xlo, self.xhi) )


    def baseResult( self, xdata, params ):
        """
        Returns the result of the model function.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result
        params : array_like
            values for the parameters

        """
        self.checkDomain( xdata )

        return super( FreeShapeModel, self ).baseResult( xdata, params )

    def basePartial( self, xdata, params, parlist=None ) :
        """
        Returns the partial derivative of the model function to
        each of the parameters.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result
        params : array_like
             values for the parameters

        """
        self.checkDomain( xdata )

        nxdata = Tools.length( xdata )
        xpix = self.npbase * ( xdata - self.xlo ) / ( self.xhi - self.xlo )
        xpix += self.center

        if parlist is None :
            parlist = [k for k in range( self.npbase )]
        np = len( parlist )

        partial = numpy.zeros( ( nxdata, np ), dtype=float )
        p0 = 0
        for k,p in enumerate( parlist ) :
            xpix -= ( p - p0 )
            p0 = p
            partial[:,k] = self.shape.result( xpix )

#        print( fmt( partial ) )
        return partial

    def TBCbaseDerivative( self, xdata, params ):
        """
        Returns the derivative of the model function df/dx.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result
        params : array_like
             values for the parameters

        """
        nxdata = Tools.length( xdata )
        xpix = self.npbase * ( xdata - self.xlo ) / ( self.xhi - self.xlo )
        xpix += self.center

        partial = numpy.zeros( ( nxdata, self.npbase ), dtype=float )
        for k in range( self.npbase ) :
            partial[:,k] = self.shape.partial( xpix )
            xpix -= 1

        return numpy.inner( params, partial )

    def baseName( self ):
        return str( "FreeShape with %d pixels." % self.npbase )

    def baseParameterUnit(  self, k ):
        """
        Return the unit of the indicated parameter.

        Parameters
        ---------
        k : int
            parameter number.

        """
        return self.yUnit
