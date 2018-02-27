import numpy as numpy
from astropy import units
import math
from . import Tools

from .PolynomialModel import PolynomialModel
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
    >>> ran = MoreRandom( )
    >>> poly.grow( )                         # starts at degree = 0, npar = 1
    >>> poly.grow( )                         # each grow( ) adds 1
    >>> poly.grow( )
    >>> poly.grow( )
    >>> print poly.npchain
    5
    >>> poly.shrink( )                        # shrink( ) deletes 1 degree
    >>> print poly.npbase
    4

    Category     mathematics/Fitting

    """

    deltaNpar = 1

    def __init__( self, minDegree=0, maxDegree=None, fixed=None,
                  growPrior=None, copy=None, **kwargs ):
        """
        Polynomial of a adaptable degree.

        The model starts as a PolynomialModel of degree = 0.
        Growth of the model is governed by a exponential prior ( scale=1 ).

        Parameters
        ----------
        minDegree : int
            minimum degree of polynomial (def=0)
        maxDegree : None or int
            maximum degree of polynomial (def=None)
        growPrior : None or Prior
            governing the birth and death.
            ExponentialPrior if  maxDegree is None else UniformPrior
        copy : PolynomialDynamicModel
            model to copy
        """
        if fixed is not None :
            raise AttributeError( "DynamicModel cannot have fixed parameters" )

        super( ).__init__( minDegree, copy=copy, **kwargs )

        if copy is None :
            self.minDegree = minDegree
            self.maxDegree = maxDegree
            if growPrior is None :
                self.growPrior = ( ExponentialPrior( scale=10 ) if maxDegree is None
                    else UniformPrior( limits=[minDegree+1, maxDegree+2] ) )
            else :
                selfgrowPrior = growPrior
        else :
            self.minDegree = copy.minDegree
            self.maxDegree = copy.maxDegree
            self.growPrior = copy.growPrior.copy()

    def copy( self ):
        """ Copy method.  """
        return PolynomialDynamicModel( self.degree, copy=self )

    def __setattr__( self, name, value ) :
        lnon = {"maxDegree": int}
#        dind = {"minDegree": int, "maxDegree": int}
        dind = {"degree": int, "minDegree": int, "maxDegree": int,
                "growPrior": Prior}
        if ( Tools.setNoneAttributes( self, name, value, lnon ) or
             Tools.setSingleAttributes( self, name, value, dind ) ) :
            pass
        else :
            super( ).__setattr__( name, value )

#    def getNumberOfComponents( self ):
#        return self.npbase

    def grow( self, pat=0 ):
        """
        Increase the degree by one upto maxDegree ( if present ).

        Return
        ------
        bool :  succes

        """
#        print( "grow  ", self.maxDegree, self.npbase )
        if self.maxDegree is not None and self.npbase >= self.maxDegree:
            return False

#        print( "grow to ", self.npbase, self.deltaNpar, pat )
        self.alterParameterSize( self.deltaNpar, pat )
        self.parNames = ["polycoeff_%d"%k for k in range( self.npbase )]
        self.degree += 1
        return True

    def shrink( self, pat=0 ):
        """
        Decrease the degree by one downto minDegree ( default 1 ).

        Return
        ------
        bool : succes

        """
#        print( "shrink  ", self.minDegree, self.npbase )
        if self.npbase <= self.minDegree + 1:
            return False

#        print( "Shrink to ", self.npbase - 1, pat )
        self.alterParameterSize( -self.deltaNpar, pat )
        self.parNames = ["polycoeff_%d"%k for k in range( self.npbase )]
        self.degree -= 1

        return True


    def baseName( self ):
        """ Return a string representation of the model.  """
        return "Dynamic" + super( PolynomialDynamicModel, self ).baseName( )


