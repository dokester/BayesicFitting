import numpy as numpy
from astropy import units
import re
import warnings
from . import Tools

from .Problem import Problem
from .Dynamic import Dynamic

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
#  *    2018        Do Kester

class ClassicProblem( Problem ):
    """
    A ClassicProblem is an optimization of parameters which involves
    the fitting of data to a Model.

    Problems can be solved by NestedSampler, with appropriate Engines and
    ErrorDistributions (==CostFunctions)

    The result of the function for certain x and p is given by
    `problem.result( x, p )`
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
        <br>
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
        super( ).__init__( model=model, xdata=xdata, ydata=ydata, weights=weights,
                           copy=copy )


    def copy( self ):
        """
        Copy.

        The copy points to the same instance of model.
        """
        return ClassicProblem( copy=self )

    #  *****RESULT**************************************************************
    def result( self, param ):
        """
        Returns the result calculated at the xdatas.

        Parameters
        ----------
        param : array_like
            values for the parameters.

        """
        return self.model.result( self.xdata, param )


    def partial( self, param ) :
        return self.model.partial( self.xdata, param )

    def derivative( self, param ) :
        return self.model.derivative( self.xdata, param )

    def myEngines( self ) :
        if self.model.isDynamic() :
            return ["galilean", "birth", "death"]
        else :
            return ["galilean"]

    def myStartEngine( self ) :
        return "start"

    def myDistribution( self ) :
        return "gauss"

    #  *****TOSTRING***********************************************************
    def baseName( self ):
        """ Returns a string representation of the model.  """
        return "ClassicProblem of " + self.model.__str__()



