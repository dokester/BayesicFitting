import numpy as numpy
from astropy import units
import re
import warnings
from .Problem import Problem
from .Dynamic import Dynamic
from . import Tools

__author__ = "Do Kester"
__year__ = 2022
__license__ = "GPL3"
__version__ = "3.0.0"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Alpha"


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
#  *    2018 - 2022  Do Kester

class OrderProblem( Problem ):
    """
    An OrderProblem needs to optimize the order of a set of nodes.
    the nodes are given by the x variable; the order by the parameters p.

    The result of the function for certain x and p is given by
    `problem.result( x, p )`

    This class is a base class. Further specializations will define the
    result method.

    Attributes
    ----------
    parameters : array_like
        to be optimized in TBD ways
    npbase : int
        number of params in the base model
    ndim : int
        number of dimensions of input. (default : 1)

    Author :         Do Kester

    """

    #  *************************************************************************
    def __init__( self, xdata=None, weights=None, copy=None ):
        """
        OrderProblem Constructor.
        <br>
        Parameters
        ----------
        xdata : array_like of shape [np,ndim]
            the nodes to be visited
        weights : array_like
            weights on the arrival nodes
        copy : BaseProblem
            to be copied

        """

        super( ).__init__( xdata=xdata, weights=weights, copy=copy )

        self.npars, self.ndim = self.xdata.shape
        self.ndata = self.npars

        self.partype = int

        if copy is None :
            self.parameters = numpy.arange( self.npars, dtype=int )
        else :
            self.parameters = copy.parameters


    def copy( self ) :
        """ Return a copy. """
        return OrderProblem( copy=self )

    def isDynamic( self ) :
        return isinstance( self, Dynamic )


    def myEngines( self ) :
        myeng = ["move", "reverse", "switch", "loop"]

        if self.isDynamic() :
            return myeng + ["birth", "death"]
        else :
            return myeng

    def myStartEngine( self ) :
        return "startorder"

    def myDistribution( self ) :
        return "distance"

    def baseName( self ) :
        return "OrderProblem"

