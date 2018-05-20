import numpy as numpy
from astropy import units
import math
from .import Tools

from .HarmonicModel import HarmonicModel
from .Dynamic import Dynamic
from .Prior import Prior
from .ExponentialPrior import ExponentialPrior
from .UniformPrior import UniformPrior

__author__ = "Do Kester"
__year__ = 2018
__license__ = "GPL"
__version__ = "1.0"
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
#  *    2018        Do Kester


class HarmonicDynamicModel( HarmonicModel, Dynamic ):
    """
    Harmonic oscillator Model of adaptable order.

    f( x:p ) = &sum;_j ( p_k cos( 2 &pi; j x ) + p_k+1 sin( 2 &pi; j x ) )

    j = 1, N; k = 0, 2N, 2

    The parameters are initialized at 1.0. It is a linear model.

    Author       Do Kester

    Examples
    --------
    >>> harm = HarmonicDynamicModel( 3 )     # period = 1
    >>> print harm.getNumberOfParameters( )        # 6
    >>> harm = HarmonicModel( 4, 2.7 )        # period = 2.7

    Category     mathematics/Fitting

    """
    deltaNpar = 2

    def __init__( self, order, minOrder=1, maxOrder=None, period=1.0, fixed=None,
                  growPrior=None, copy=None, **kwargs ):
        """
        Harmonic of a adaptable order.

        The model starts as a HarmonicModel of order = 1
        Growth of the model is governed by a exponential prior ( scale=1 )

        Parameters
        ----------
        order : int
            order to start with. It should be minOrder <= order <= maxOrder
        minOrder : int
            minimum degree of polynomial (def=1)
        maxOrder : None or int
            maximum degree of polynomial (def=None)
        period : float
            period of the oscilation
        growPrior : None or Prior
            governing the birth and death.
            ExponentialPrior (scale=2) if  maxOrder is None else UniformPrior
        copy : HarmonicDynamicModel
            model to copy

        Raises
        ------
        AttributeError when fixed parameters are requested
        ValueError when order is outside [min..max] range

        """
        if fixed is not None :
            raise AttributeError( "DynamicModel cannot have fixed parameters" )
        if order < minOrder or ( maxOrder is not None and order > maxOrder ) :
            raise ValueError( "order outside range of [min..max] range" )

        super( HarmonicDynamicModel, self ).__init__( order, period=period,
            copy=copy, **kwargs )

        if copy is None :
            self.minComp = minOrder
            self.maxComp = maxOrder
            if growPrior is None :
                if maxOrder is None :
                    self.growPrior = ExponentialPrior( scale=2 )
                else :
                    lim = [minOrder, maxOrder+1]        # limits on components
                    self.growPrior = UniformPrior( limits=lim )
            else :
                self.growPrior = growPrior
        else :
            self.minComp = copy.minComp
            self.maxComp = copy.maxComp
            self.growPrior = copy.growPrior.copy()

    def copy( self ):
        """ Copy method.  """
        return HarmonicDynamicModel( self.order, period=self.period, copy=self )

    def changeNComp( self, dn ) :
        self.order += dn

    def __setattr__( self, name, value ) :
        dind = {"minComp": int, "maxComp": int, "growPrior": Prior}
        lnon = ["maxComp"]
        if ( Tools.setNoneAttributes( self, name, value, lnon ) or
             Tools.setSingleAttributes( self, name, value, dind ) ) :
            pass
        else :
            super( HarmonicDynamicModel, self ).__setattr__( name, value )

    def basePrior( self, k ):
        """
        Return the prior for parameter k.

        Parameters
        ----------
        k : int
            the parameter to be selected.
        """
        return super( HarmonicDynamicModel, self ).basePrior( k % self.deltaNpar )


    def baseName( self ):
        """ Return a string representation of the model.  """
        return "Dynamic" + super( HarmonicDynamicModel, self ).baseName( )


