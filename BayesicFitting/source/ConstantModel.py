import numpy as numpy
from . import Tools
from .Tools import setAttribute as setatt

from .Model import Model
from .PolynomialModel import PolynomialModel
from .PolySurfaceModel import PolySurfaceModel

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
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
#  *    2011 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2020 Do Kester

class ConstantModel( Model ):
    """
    ConstantModel is a Model which does not have any parameters.

        f( x:p ) = f( x )

    As such it is irrelevant whether it is linear or not.
    It has 0 params and returns a 0 for its partials.

    ConstantModel, by default, returns a constant ( = 0 ) for its result.
    It can however return any fixed form that a Model can provide.

    This might all seem quite irrelevant for fitting. And indeed no parameters
    can be fitted to these models, no standard deviations can be calculated, but
    it is possible to calculate the evidence for these models and compare them
    with more complicated models to decide whether there is any evidence for
    some structure at all.

    It can also be used when some constant is needed in a compound model,
    or a family of similar shapes.

    Attributes
    ----------
    fixedModel : Model
        a model which is calculated. (default: 0, everywhere)
    table : array_like
        array of tabulated results

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
    To make a model that decays to 1.0

    >>> model = ConstantModel( values=1.0 )
    >>> model.addModel( ExpModel( ) )

    To make a model that returns a fixed cosine of frequency 5

    >>> model = ConstantModel( fixedModel=SineModel(), values=[1.0,0.0,5.0] )

    """
    def __init__( self, ndim=1, copy=None, fixedModel=None, values=None,
                    table=None ):
        """
        The ConstantModel implementation.

        Number of parameters = 0.

        Parameters
        ----------
        ndim : int
            number of dimensions for the model. (default: 1)
        copy : ConstantModel
            model to be copied. (default: None)
        fixedModel : Model
            a fixed model to be returned. (default: 0 everywhere)
        values : array_like
            parameters to be used in the fixedModel. (default: None)
        table : array_like
            array of tabulated results

        Notes
        -----
        A table provided to the constructor has only values at the xdata.
        At other vales than xdata, the model does not work.

        """
        super( ConstantModel, self ).__init__( 0, ndim=ndim, copy=copy )

        if copy is not None :                  # copy from model
            setatt( self, "fixedModel", copy.fixedModel )
            setatt( self, "table", copy.table )
        elif table is not None :                # store tabular results
            setatt( self, "table", table, islist=True, type=float )
            setatt( self, "fixedModel", None )
        else :                                  # make a fixedModel
            setatt( self, "table", None )
            if fixedModel is not None :
                setatt( self, "fixedModel", fixedModel, type=Model )
            else :
                setatt( self, "fixedModel", PolynomialModel( 0 ) if ndim == 1 else PolySurfaceModel( 0 ) )
            if values is not None :
                setatt( self.fixedModel, "parameters", values, type=float, islist=True )

    def copy( self ):
        """ Copy method.  """
        return ConstantModel( ndim=self.ndim, copy=self )

    def __setattr__( self, name, value ):
        """
        Set attributes: fixedModel, table, values
        """
        if name == "fixedModel" :
            setatt( self, name, value, type=Model, isnone=True )
            return
        if name == "table" :
            setatt( self, name, value, type=float, islist=True, isnone=True )
            setatt( self, "fixedModel", None )
            return
        if name == "values" or name == "value":
            setatt( self.fixedModel, "parameters", value, type=float, islist=True )
            return

        super( ConstantModel, self ).__setattr__( name, value )

    def baseResult( self, xdata, params ):
        """
        Returns a constant form.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters. (irrelevant)

        """
        if self.table is not None :
            return self.table

        return self.fixedModel.result( xdata )

    def basePartial( self, xdata, params ) :
        """
        Returns the partials at the xdata value. (=empty array)

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters. (irrelevant)

        """
        return numpy.zeros( ( Tools.length( xdata ), self.npbase ), dtype=float )

    def baseDerivative( self, xdata, params ) :
        """
        Return the derivative df/dx at each point x (== 0).

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters. (irrelevant)

        """
        return numpy.zeros_like( xdata )

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        content = "tabular result" if self.table is not None else self.fixedModel.__str__()
        return str( "ConstantModel: f( x ) = " + content )


