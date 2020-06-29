import numpy as numpy
from .Tools import setAttribute as setatt

from .PolynomialModel import PolynomialModel
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

class PolynomialDynamicModel( PolynomialModel, Dynamic ):
    """
    General polynomial model of an adaptable degree.

    f( x:p ) = &sum; p_k * x^k

    where the sum is over k running from 0 to degree ( inclusive ).

    It is a linear model.

    Author       Do Kester

    Examples
    --------
    >>> poly = PolynomialDynamicModel( )         # polynomial with unknown degree
    >>> poly.grow( )                         # starts at degree = 0, npar = 1
    >>> poly.grow( )                         # each grow( ) adds 1
    >>> poly.grow( )
    >>> poly.grow( )
    >>> print poly.npchain
    5
    >>> poly.shrink( )                        # shrink( ) deletes 1 degree
    >>> print poly.npbase
    4

    Attributes
    ----------
    minDegree : int
        minimum degree of the polynomial
    maxDegree : int or None
        maximum degree of the polynomial

    Attributes from Dynamic
    -----------------------
        ncomp (=degree+1), deltaNpar, minComp (=minDegree+1), maxComp (=maxDegree+1), growPrior

    Attributes from PolynomialModel
    -------------------------------
        degree

    Attributes from Model
    ---------------------
        npchain, parameters, stdevs, xUnit, yUnit

    Attributes from FixedModel
    --------------------------
        npmax, fixed, parlist, mlist

    Attributes from BaseModel
    --------------------------
        npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames


    Category     mathematics/Fitting

    """

    deltaNpar = 1

    def __init__( self, degree, minDegree=0, maxDegree=None, fixed=None,
                  growPrior=None, copy=None, **kwargs ):
        """
        Polynomial of a adaptable degree.

        The model starts as a PolynomialModel of degree = 0.
        Growth of the model is governed by a exponential prior ( scale=1 ).

        Parameters
        ----------
        degree : int
            degree to start with; it should be minDegree <= degree <= maxDegree
        minDegree : int
            minimum degree of polynomial (def=0)
        maxDegree : None or int
            maximum degree of polynomial (def=None)
        growPrior : None or Prior
            governing the birth and death.
            ExponentialPrior (scale=2) if  maxDegree is None else UniformPrior
        copy : PolynomialDynamicModel
            model to copy

        Raises
        ------
        AttributeError when fixed parameters are requested
        ValueError when degree is outside [min..max] range
        """
        if fixed is not None :
            raise AttributeError( "DynamicModel cannot have fixed parameters" )
        if degree < minDegree or ( maxDegree is not None and degree > maxDegree ):
            raise ValueError( "degree outside range of [min..max] range" )


        super( PolynomialDynamicModel, self ).__init__( degree, copy=copy, **kwargs )

        self.deltaNpar = 1

        if copy is None :
            self.setGrowPrior( growPrior=growPrior, min=minDegree, max=maxDegree,
                           name="Degree" )
        else :
            setatt( self, "minDegree", copy.minDegree )
            setatt( self, "maxDegree", copy.maxDegree )
            setatt( self, "growPrior", copy.growPrior.copy() )

    def copy( self ):
        """ Copy method.  """
        return PolynomialDynamicModel( self.degree, copy=self )

    def isDynamic( self ) :
        return True

    def changeNComp( self, dn ) :
        setatt( self, "degree", self.degree + dn )

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
            return self.degree + 1
        if name == 'minComp' :
            return self.minDegree + 1
        if name == 'maxComp' :
            return self.maxDegree if self.maxDegree is None else ( self.maxDegree + 1 )

        return super( ).__getattr__( name )


    def baseName( self ):
        """ Return a string representation of the model.  """
        return "Dynamic" + super( PolynomialDynamicModel, self ).baseName( )


