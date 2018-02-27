import numpy as numpy
import math

from .ErrorDistribution import ErrorDistribution
from .NoiseScale import NoiseScale
from .JeffreysPrior import JeffreysPrior
from . import Tools

__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2017        Do Kester


class ScaledErrorDistribution( ErrorDistribution ):
    """
    Base class that defines methods common to error distributions with a scale.

    GaussErrorDistribution
    LaplaceErrorDistribution
    CauchyErrorDistribution
    GenGaussErrorDistribution

    Author       Do Kester.

    """
    PARNAMES = ["scale"]

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, xdata, data, weights=None, scale=1.0, limits=None,
                  copy=None ):
        """
        Default Constructor.

        Parameters
        ----------
        xdata : array_like
            input data for the model
        data : array_like
            data to be fitted
        weights : array_like
            weights to be used
        scale : float
            noise scale
        limits : None or list of 2 floats [low,high]
            None : no limits implying fixed scale
            low     low limit on scale (needs to be >0)
            high    high limit on scale
            when limits are set, the scale is *not* fixed.

        copy : ScaledErrorDistribution
            distribution to be copied.

        """
        super( ScaledErrorDistribution, self ).__init__( xdata, data,
                weights=weights, copy=copy )

        if copy is None :
            self.hyperpar = NoiseScale( scale=scale, limits=limits )
        else :
            self.hyperpar = copy.hyperpar                   ## TBC copy ???

        if limits is None :
            self.fixed = self.keepFixed( {0: scale} )

    def copy( self ):
        """ Return copy of this.  """
        return ScaledErrorDistribution( self.xdata, self.data, copy=self )

    def setLimits( self, limits ) :
        """
        Set limits for scale.

        Parameters
        ----------
        limits : [low,high]
            low : float or array_like
                low limits
            high : float or array_like
                high limits
        """
        if self.hyperpar[0].prior is None :
            self.hyperpar[0].prior = JeffreysPrior()

        super( ScaledErrorDistribution, self ).setLimits( limits )



    def __setattr__( self, name, value ):
        """
        Set attributes.

        """
        if name == "scale" and Tools.isInstance( value, float ) :
            self.hyperpar[0].hypar = value
        else :
            super( ScaledErrorDistribution, self ).__setattr__( name, value )

    def __getattr__( self, name ) :
        """
        Return value belonging to attribute with name.

        Parameters
        ----------
        name : string
            name of the attribute
        """
        if name == "scale" :
            return self.hyperpar[0].hypar
        else :
            return super( ScaledErrorDistribution, self ).__getattr__( name )

    def getResiduals( self, model, param=None ):
        """
        Return the residuals.
        For those distributions r=that need them.

        Parameters
        ----------
        model : Model
            model to be fitted
        param : array_like
            parameters of the model

        """
        return self.data - model.result( self.xdata, param )

