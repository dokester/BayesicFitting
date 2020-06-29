import numpy as numpy
from astropy import units
import re
import warnings
from . import Tools

from .Problem import Problem
from .Dynamic import Dynamic
from .Modifiable import Modifiable

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
#  *    2018 - 2020 Do Kester

class ClassicProblem( Problem ):
    """
    A ClassicProblem is an optimization of parameters which involves
    the fitting of data to a Model at a fixed set of x values.

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
        """
        Return the partials of the internal model.

        Parameters
        ----------
        param : array_like
            list of model parameters
        """
        return self.model.partial( self.xdata, param )

    def derivative( self, param ) :
        """
        Return the derivative of the internal model.

        Parameters
        ----------
        param : array_like
            list of model parameters
        """
        return self.model.derivative( self.xdata, param )

    def myEngines( self ) :
        """
        Return a default list of preferred engines
        """
        engs = ["galilean", "chord"]

        if self.model.isDynamic() :
            engs += ["birth", "death"]

        if self.model.isModifiable() :
            engs += ["struct"]

        return engs

    def myStartEngine( self ) :
        """
        Return a default preferred start engines: "start"
        """
        return "start"

    def myDistribution( self ) :
        """
        Return a default preferred ErrorDistribution: "gauss"
        """
        return "gauss"

    #  *****TOSTRING***********************************************************
    def baseName( self ):
        """ Returns a string representation of the model.  """
        return "ClassicProblem of " + self.model.__str__()



