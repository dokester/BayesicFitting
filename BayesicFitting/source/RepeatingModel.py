import numpy as numpy
from astropy import units
import math
from . import Tools

from .Model import Model
from .Dynamic import Dynamic
from .ExponentialPrior import ExponentialPrior
from .UniformPrior import UniformPrior
from .Prior import Prior

__author__ = "Do Kester"
__year__ = 2017
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

class RepeatingModel( Model, Dynamic ):
    """
    RepeatingModel implements the the Dynamic interface for a Model.

    It repeatedly calls a  Model, called the basic model,
    zero ( or more ) times, each time with the next set of parameters.


    Author       Do Kester

    """
    #  *****CONSTRUCTOR*********************************************************
    def __init__( self, ncomp, model, minComp=0, maxComp=None, fixed=None,
                  growPrior=None, copy=None, **kwargs ):
        """
        Repeating the same model several times.

        Parameters
        ----------
        ncomp : int
            number of repetitions
        model : Model
            model to be repeated
        minComp : int (0)
            minimum number of repetitions
        maxComp : None or int
            maximum number of repetitions
        growPrior : None or Prior
            governing the birth and death.
            ExponentialPrior (scale=2) if  maxOrder is None else UniformPrior
        copy : HarmonicDynamicModel
            model to copy

        Raises
        ------
        AttributeError when fixed parameters are requested
        ValueError when order is outside [min..max] range

        """
        if fixed is not None :
            raise AttributeError( "DynamicModel cannot have fixed parameters" )
        if ncomp < minComp or ( maxComp is not None and ncomp > maxComp ) :
            raise ValueError( "ncomp outside range of [min..max] range" )

        np = ncomp * model.npchain
        super( RepeatingModel, self ).__init__( np, copy=copy, **kwargs )

        self.ncomp = ncomp
        self.model = model

        if copy is None :
            self.minComp = minComp
            self.maxComp = maxComp
            if growPrior is None :
                if maxComp is None :
                    self.growPrior = ExponentialPrior( scale=2 )
                else :
                    lim = [minComp, maxComp+1]        # limits on components
                    self.growPrior = UniformPrior( limits=lim )
            else :
                self.growPrior = growPrior
        else :
            self.minComp = copy.minComp
            self.maxComp = copy.maxComp
            self.growPrior = copy.growPrior.copy()

    def copy( self ):
        """ Copy method.  """
        return RepeatingModel( self.ncomp, self.model, copy=self )

    def changeNComp( self, dn ) :
        self.ncomp += dn

    #  *************************************************************************
    def __setattr__( self, name, value ) :
        dind = {"minComp": int, "maxComp": int, "growPrior": Prior,
                "model": Model, "ncomp" : int, "deltaNpar" : int}
        lnon = {"maxComp": int}

        if name == "model" :
            self.deltaNpar = value.npchain

        if ( Tools.setNoneAttributes( self, name, value, lnon ) or
             Tools.setSingleAttributes( self, name, value, dind ) ) :
            pass
        else :
            super( RepeatingModel, self ).__setattr__( name, value )

    #  *************************************************************************
    def result( self, xdata, params ):
        """
        Returns the result of the model function.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result
        params : array_like
             values for the parameters

        """
        result = numpy.zeros( Tools.length( xdata ), dtype=float )

        ks = 0
        for k in range( self.ncomp ) :
            ke = ks + self.deltaNpar
            result += self.model.result( xdata, params[ks:ke] )
            ks = ke

        return result

    def partial( self, xdata, params ):
        """
        Returns the partials at the input value.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result
        params : array_like
             values for the parameters


        """
        nxdata = Tools.length( xdata )
        partial = numpy.ndarray( ( nxdata, self.npbase ), dtype=float )

        ks = 0
        for k in range( self.ncomp ) :
            ke = ks + self.deltaNpar
            partial[:,ks:ke] = self.model.partial( xdata, params[ks:ke] )
            ks = ke
        return partial

    def derivative( self, xdata, params ):
        """
        Returns the derivative df/dx at the input value.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result
        params : array_like
             values for the parameters

        """
        nxdata = Tools.length( xdata )
        dfdx = numpy.ndarray( ( nxdata, self.ndim ), dtype=float )

        ks = 0
        for k in range( self.ncomp ) :
            ke = ks + self.deltaNpar
            dfdx += self.model.derivative( xdata, params[ks:ke] )
            ks = ke
        return dfdx

    def getNumberOfComponents( self ):
        """ Return the number of basic models inside this compound model.  """
        return self.ncomp


    def getPrior( self, k ):
        return super( RepeatingModel, self ).getPrior( k % self.deltaNpar )

    def baseName( self ):
        """ Return a string representation of the model.  """
        return ( "Repeat %d times:\n  " % self.ncomp +
                  self.model.baseName( ) )

    def getParName( self, k ):
        """
        Return the name of the indicated parameter.

        Parameters
        ----------
        k : int
            parameter number.

        """
        return ( self._model.getParameterName( k % self.deltaNpar ) + "_" +
                ( k / self.deltaNpar ) )

    def getParUnit( self, k ):
        """
        Return the unit of the indicated parameter.

        Parameters
        ----------
        k : int
            parameter number.

        """
        self._model.setUnits( self.xUnit, self.yUnit )
        return self.model.getParameterUnit( k % self.deltaNpar )
