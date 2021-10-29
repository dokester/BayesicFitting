import numpy as numpy
from astropy import units
import re
import warnings
from . import Tools

from .ClassicProblem import ClassicProblem
from .Dynamic import Dynamic
from .Modifiable import Modifiable

__author__ = "Do Kester"
__year__ = 2021
__license__ = "GPL3"
__version__ = "2.7.0"
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
#  *    2018 - 2021 Do Kester

class EvidenceProblem( ClassicProblem ):
    """
    An EvidenceProblem is a ClassicProblem containing a Dynamic and/or Modifiable
    model, where the (Gauss-approximated) evidence is used as likelihood

    Problems can be solved by NestedSampler, with appropriate Engines and
    ErrorDistributions.

    The result of the function for certain x and p is given by
    problem.result( x, p )
    The parameters, p, are to be optimized while the x provide additional
    information.

    Attributes from Problem
    -----------------------
    model, xdata, ydata, weights

    Author :         Do Kester

    """

    #  *************************************************************************
    def __init__( self, model=None, xdata=None, ydata=None, weights=None, copy=None ):
        """
        Constructor for classic problems.

        Parameters
        ----------
        model : Model
            the model to be solved
        xdata : array_like or None
            independent variable
        ydata : array_like or None
            dependent variable
        weights : array_like or None
            weights associated with ydata
        copy : Problem
            to be copied

        """
        if not ( model.isDynamic() or model.isModifiable() ) :
            raise ValueError( "Model needs to be dynamic or modifiable" )

        super( ).__init__( model=model, xdata=xdata, ydata=ydata, weights=weights,
                           copy=copy )


    def copy( self ):
        """
        Copy.

        The copy points to the same instance of model.
        """
        return EvidenceProblem( model=self.model, xdata=self.xdata, ydata=self.ydata,
                weights=self.weights, copy=self )


    def myEngines( self ) :
        """
        Return a default list of preferred engines
        """
        engs = []

        if self.model.isDynamic() :
            engs += ["birth", "death"]

        if self.model.isModifiable() :
            engs += ["struct"]

        return engs

    def myDistribution( self ) :
        """
        Return the default preferred ModelDistribution: "model"
        """
        return "model"

    #  *****TOSTRING***********************************************************
    def baseName( self ):
        """ Returns a string representation of the model.  """
        return "EvidenceProblem of " + self.model.__str__()



