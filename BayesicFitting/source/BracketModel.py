import numpy
from .Model import Model
from .Model import Brackets
from . import Tools
from .Tools import setAttribute as setatt

_author__ = "Do Kester"
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
#  *    2017 - 2020 Do Kester

class BracketModel( Brackets ):
    """
    BracketModel provides brackets to a chain of Models.

    Its results are exactly the same as the results of the contained model.

    When the contained model is a compound model (a chain of models), the
    BracketModel make a single unit out of it. It acts as a pair of brackets
    in another chain of models. Since compound models can be joined by operations
    other than addition ( there is also subtract, multiply and divide ) brackets
    are needed to distinguish m1 * ( m2 + m3 ) from m1 * m2 + m3.

    BracketModel is automatically invoked when the Model appended to another model,
    is actually a chain of models.

    Model.Brackets is an internal class inside Model.

    Attributes
    ----------
    model : Model
        to be put inside of brackets
    deep : int
        container depth (only for nice printing).

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
    Explicit use of BrackeModel

    >>> m1 = GaussModel( )
    >>> m1 += PolynomialModel( 0 )              # Gauss on a constant background
    >>> m2 = BracketModel( m1 )
    >>> m3 = SineModel( )
    >>> m3 *= m2                                # sine * ( gauss + const )
    >>> print( m3 )

    Implicit use of BrackeModel, automatically invoked when m2 is a chain

    >>> m1 = GaussModel( )
    >>> m1 += PolynomialModel( 0 )              # m1 is a chain of models
    >>> m3 = SineModel( )
    >>> m3 *= m1                                # sine * ( gauss + const )
    >>> print( m3 )                             # exactly the same


    Warning
    -------
    BracketModel is about rather advanced model building.

    Notes
    -----
    1. You have to complete the BracketModel, including parameter reduction,
       BEFORE you put it into a model chain.
    2. If you change a BracketModel which is part of a model chain, unexpected result
       might happen.


    """
    #  *************************************************************************
    def __init__( self, model, copy=None, fixed=None, **kwargs ):
        """
        BracketModel

        When constructing a BracketModel existing attributes are lost, except
        parameters that were 'fixed' in the constituent Models. They stay fixed.

        Parameters
        ----------
        model : Model
            to be put in the container.
        copy : BracketModel
            model to be copied
        fixed : dict
            if fixed is not None raise AttributeError
            Use fixed on the constituent models.

        Raises
        ------
        AttributeErrr : When fixed is not None

        """
        if fixed is not None :
            raise AttributeError( "BracketModel cannot have fixed parameters" )

        super( BracketModel, self ).__init__( model, copy=copy, **kwargs )

    def copy( self ):
        """
        Copy a Bracket Model.

        """
        return BracketModel( self.model.copy(), copy=self )

