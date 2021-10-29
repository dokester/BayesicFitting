import numpy as numpy

from .Problem import Problem
from .Formatter import formatter as fmt

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

class MultipleOutputProblem( Problem ):
    """
    A MultipleOutputProblem is an optimization of parameters where the model
    has multiple outputs. E.g. the orbit of a double star or the outcome of
    a game.

    Problems can be solved by NestedSampler, with appropriate Engines and
    ErrorDistributions.

    The result of the function for certain x and p is given by
    problem.result( p )
    The parameters, p, are to be optimized while the x provide additional
    information.

    Attributes from Problem
    -----------------------
    model, xdata, ydata, weights, partype

    Author :         Do Kester

    """

    #  *************************************************************************
    def __init__( self, model=None, xdata=None, ydata=None, weights=None, copy=None ):
        """
        Problem Constructor.

        Parameters
        ----------
        model : Model
            the model to be solved. One with multiple outputs: model.ndout > 1
        xdata : array_like
            independent variable
        ydata : array_like
            dependent variable. shape = (len(xdata), model.ndout)
        weights : array_like or None
            weights associated with ydata: shape = as xdata or as ydata
        copy : Problem
            to be copied

        """
        if weights is not None :
            if len( weights.shape ) == 1 :
                wgts = numpy.zeros( ( len( weights ), model.ndout ), dtype=float )
                for k in range( model.ndout ) :
                    wgts[:,k] = weights
                weights = wgts
            weights = weights.flatten()

        super( ).__init__( model=model, xdata=xdata, ydata=ydata, weights=weights,
                           copy=copy )


    def copy( self ):
        """
        Copy.

        """
        return MultipleOutputProblem( copy=self )


    #  *****RESULT**************************************************************
    def result( self, param ):
        """
        Returns the result calculated at the xdata.

        Parameters
        ----------
        param : array_like
            values for the parameters + nuisance params.

        """
        return self.model.result( self.xdata, param )

    def partial( self, param ) :
        """
        Returns the partials (df/dp) calculated at the xdata.

        Parameters
        ----------
        param : array_like
            values for the parameters + nuisance params.

        """

        parts = self.model.partial( self.xdata, param )

        partial = parts[0]
        for k in range( 1, self.model.ndout ) :
            partial = numpy.append( partial, parts[k], 1 )

        return partial.reshape( -1, self.npars )


    def derivative( self, param ) :
        """
        Return the derivative of the internal model.

        Parameters
        ----------
        param : array_like
            list of model parameters
        """
        return self.model.derivative( self.xdata, param )

    def residuals( self, param, mockdata=None ) :
        """
        Returns residuals in a flattened array.
        """
        res = super().residuals( param, mockdata=mockdata )
        return res.flatten()

    def myEngines( self ) :
        """
        Return a default list of preferred engines
        """
        return ["galilean", "chord"]

    def myStartEngine( self ) :
        """
        Return the default preferred startengines
        """
        return "start"

    def myDistribution( self ) :
        """
        Return the name of the preferred error distribution
        """
        return "gauss"

    #  *****TOSTRING***********************************************************
    def __str__( self ):
        """ Returns a string representation of the model.  """
        return "MultipleOutputProblem of " + self.model



