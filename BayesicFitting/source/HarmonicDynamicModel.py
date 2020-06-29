import numpy as numpy
from astropy import units
import math
from .import Tools
from .Tools import setAttribute as setatt

from .HarmonicModel import HarmonicModel
from .Dynamic import Dynamic

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL"
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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2018 - 2020 Do Kester


class HarmonicDynamicModel( HarmonicModel, Dynamic ):
    """
    Harmonic oscillator Model of adaptable order.

    f( x:p ) = &sum;_j ( p_k cos( 2 &pi; j x ) + p_k+1 sin( 2 &pi; j x ) )

    j = 1, N; k = 0, 2N

    The parameters are initialized at 1.0. It is a linear model.

    Author       Do Kester

    Attributes
    ----------
    minOrder : int
        minimum degree of polynomial (def=1)
        Can also be read as minComp
    maxOrder : None or int
        maximum degree of polynomial (def=None)
        Can also be read as maxComp

    Attributes from Dynamic
    ----------------------
        ncomp (= order), deltaNpar, minComp (= minOrder), maxComp (= maxComp), growPrior

    Attributes from HarmonicModel
    -----------------------------
        order, period

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
    >>> harm = HarmonicDynamicModel( 3 )            # period = 1
    >>> print harm.getNumberOfParameters( )         # 6
    >>> harm = HarmonicModel( 4, period=2.7 )       # period = 2.7

    Category     mathematics/Fitting

    """
    deltaNpar = 2

    def __init__( self, order, minOrder=1, maxOrder=None, period=1.0, fixed=None,
                  growPrior=None, copy=None, **kwargs ):
        """
        Harmonic of a adaptable order.

        The model starts as a HarmonicModel of order = 1
        Growth of the model is governed by a prior.

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
        fixed : None
            If fixed is not None an AttributeError is raised
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

        self.deltaNpar = 2

        if copy is None :
            self.setGrowPrior( growPrior=growPrior, min=minOrder, max=maxOrder,
                           name="Order" )
        else :
            setatt( self, "minOrder", copy.minOrder )
            setatt( self, "maxOrder", copy.maxOrder )
            setatt( self, "growPrior", copy.growPrior.copy() )

    def copy( self ):
        """ Copy method.  """
        return HarmonicDynamicModel( self.order, period=self.period, copy=self )

    def isDynamic( self ) :
        return True

    def changeNComp( self, dn ) :
        setatt( self, "order", self.order + dn )

    def __setattr__( self, name, value ) :
        if self.setDynamicAttribute( name, value ) :
            return
        else :
            super( ).__setattr__( name, value )

    def __getattr__( self, name ) :
        """
        Return value belonging to attribute with name.

        Parameters
        ----------
        name : string
            name of the attribute
        """
        if name == 'ncomp' :
            return self.order
        if name == 'minComp' :
            return self.minOrder
        if name == 'maxComp' :
            return self.maxOrder

        return super( ).__getattr__( name )

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


