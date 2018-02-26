import numpy as numpy
from . import Tools

from .Model import Model
from .PolynomialModel import PolynomialModel
from .PolySurfaceModel import PolySurfaceModel

__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
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
#  *    2011 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2017 Do Kester

class ConstantModel( Model ):
    """
    ConstantModel is a Model which does not have any parameters.

    .. math::
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

    It can also be used when some constant is needed in a compound model.

    Examples
    --------
    To make a model that decays to 1.0

    >>> model = ConstantModel( values=1.0 )
    >>> model.addModel( ExpModel( ) )

    To make a model that returns a fixed cosine of frequency 5

    >>> model = ConstantModel( fixedModel=SineModel(), values=[1.0,0.0,5.0] )

    Attributes
    ----------
    fixedModel : Model
        a model which is calculated. (default: 0, everywhere)
    table : array_like
        array of tabulated results

    """
    def __init__( self, ndim=1, copy=None, fixedModel=None, values=None,
                    table=None, **kwargs ):
        """
        The ConstantModel implementation.
        <br>
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

        """
        super( ConstantModel, self ).__init__( 0, ndim=ndim, copy=copy, **kwargs )
        if copy is not None :                  # copy from model
            self.fixedModel = copy.fixedModel
            self.table = copy.table
        elif table is not None :                # store tabular results
            self.table = table
            self.fixedModel = None
        else :                                  # make a fixedModel
            self.table = None
            if fixedModel is not None :
                self.fixedModel = fixedModel
            else :
                self.fixedModel = PolynomialModel( 0 ) if ndim == 1 else PolySurfaceModel( 0 )
            if values is not None :
                self.fixedModel.parameters = values

    def copy( self ):
        """ Copy method.  """
        return ConstantModel( ndim=self.ndim, copy=self )

    def __setattr__( self, name, value ):
        """
        Set attributes: fixedModel
        """
        lnon = ["fixedModel", "table"]
        dlst = {"table": float}
        dind = {"fixedModel":Model}

        if ( Tools.setNoneAttributes( self, name, value, lnon ) or
             Tools.setListOfAttributes( self, name, value, dlst ) or
             Tools.setSingleAttributes( self, name, value, dind ) ) :
            pass                                            # success
        else :
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


