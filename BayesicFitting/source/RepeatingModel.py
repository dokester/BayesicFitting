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
                  same=None, growPrior=None, isDynamic=True, copy=None, **kwargs ):
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
        same : None or int or list of int
            indices of parameters of model that get identical values

        growPrior : None or Prior
            governing the birth and death.
            ExponentialPrior (scale=2) if  maxOrder is None else UniformPrior
        isDynamic : bool (True)
            Whether this is a Dynamic Model.
        copy : RepeatingModel
            model to copy

        Raises
        ------
        AttributeError when fixed parameters are requested
        ValueError when order is outside [min..max] range

        """
        if fixed is not None :
            raise AttributeError( "DynamicModel cannot have fixed parameters; " +
                                  " put fixed parameter(s0 in model." )
        if ncomp < minComp or ( maxComp is not None and ncomp > maxComp ) :
            raise ValueError( "ncomp outside range of [min..max] range" )

        np = ncomp * model.npchain

        super( RepeatingModel, self ).__init__( np, copy=copy, **kwargs )

        self.ncomp = ncomp
        self.model = model

        if copy is None :
            self.minComp = minComp
            self.maxComp = maxComp
            self.isDyna = isDynamic and ( maxComp is None or minComp < maxComp )
            self.priors = model.priors          ## point to the same
        else :
            self.minComp = copy.minComp
            self.maxComp = copy.maxComp
            growPrior = copy.growPrior.copy()
            self.isDyna = copy.isDyna
            same = copy.same

        self.setSame( same )
        self.deltaNpar = len( self.index )

        if self.isDynamic() :
            if growPrior is None :
                if maxComp is None :
                    self.growPrior = ExponentialPrior( scale=2 )
                else :
                    lim = [minComp, maxComp+1]        # limits on components
                    self.growPrior = UniformPrior( limits=lim )
            else :
                self.growPrior = growPrior

    def copy( self ):
        """ Copy method.  """
        return RepeatingModel( self.ncomp, self.model, copy=self )

    def changeNComp( self, dn ) :
        self.ncomp += dn

    def setSame( self, same ) :
        self.same = same
        if same is None :
            self.index = numpy.arange( self.model.npbase, dtype=int )
            return

        index = []
        for k in range( self.model.npbase ) :
            if not k in same :
                index += [k]
        self.index = numpy.array( index, dtype=int )

    def grow( self, pat=0 ):
        """
        Increase the degree by one upto maxDegree ( if present ).

        Parameters
        ----------
        pat : int
            location where the new params should be inserted

        Return
        ------
        bool :  succes

        """
        if not self.isDynamic() :
            return False

        if self.maxComp is not None and self.ncomp >= self.maxComp:
            return False

        dnp = self.deltaNpar if self.ncomp > 0 else self.model.npbase
        self.alterParameterSize( dnp, pat )

        self.ncomp += 1

        return True

    def shrink( self, pat=0 ):
        """
        Decrease the degree by one downto minDegree ( default 1 ).

        Parameters
        ----------
        pat : int
            location where the new params should be inserted

        Return
        ------
        bool : succes

        """
        if ( not self.isDynamic() ) or self.ncomp <= self.minComp :
            return False

        dnp = self.deltaNpar if self.ncomp > 1 else self.model.npbase
        self.alterParameterSize( -dnp, pat )

        self.ncomp -= 1

        return True


    #  *************************************************************************
    def __setattr__( self, name, value ) :
        dind = {"minComp": int, "maxComp": int, "growPrior": Prior, "isDyna": bool,
                "model": Model, "ncomp" : int, "deltaNpar" : int}
        lnon = ["maxComp", "same"]
        llst = {"same": int, "index": int}

        if name == "model" :
            self.deltaNpar = value.npchain

        if ( Tools.setNoneAttributes( self, name, value, lnon ) or
             Tools.setSingleAttributes( self, name, value, dind ) or
             Tools.setListOfAttributes( self, name, value, llst ) ) :
            pass
        else :
            super( RepeatingModel, self ).__setattr__( name, value )

    def isDynamic( self ) :
        return self.isDyna

    #  *************************************************************************
    def baseResult( self, xdata, params ):
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
        if self.ncomp == 0 :
            return result

        ke = self.model.npbase
        pars = params[:ke].copy()
        k = 1
        while True :
            result += self.model.result( xdata, pars )
            if k == self.ncomp :
                return result
            k += 1
            ks = ke
            ke += self.deltaNpar
            pars[self.index] = params[ks:ke]

        return result

    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result
        params : array_like
            values for the parameters
        parlist : array_like
            list of indices of active parameter

        """
        nxdata = Tools.length( xdata )
        partial = numpy.zeros( ( nxdata, self.npbase ), dtype=float )
        if self.ncomp == 0 :
            return partial

        ke = self.model.npbase
        pars = params[:ke].copy()
        full = numpy.arange( self.model.npbase, dtype=int )
        k = 1
        while True :
            partial[:,full] += self.model.partial( xdata, pars )
            if k == self.ncomp :
                break
            k += 1
            ks = ke
            ke += self.deltaNpar

            full[self.index] = [k for k in range( ks, ke )]
            pars[self.index] = params[ks:ke]

        if parlist is None :
            return partial

        return partial[:,parlist]

    def baseDerivative( self, xdata, params ):
        """
        Returns the derivative df/dx at the input value.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the result
        params : array_like
             values for the parameters

        """
        dfdx = numpy.zeros( Tools.length( xdata ), dtype=float )
        if self.ncomp == 0 :
            return dfdx

        ke = self.model.npbase
        pars = params[:ke].copy()
        k = 1
        while True :
            dfdx += self.model.derivative( xdata, pars )
            if k == self.ncomp :
                return dfdx
            k += 1
            ks = ke
            ke += self.deltaNpar
            pars[self.index] = params[ks:ke]

        return dfdx

    def getNumberOfComponents( self ):
        """ Return the number of basic models inside this compound model.  """
        return self.ncomp


    def getPrior( self, k ):
        """
        Return the prior for parameter k.

        Parameters
        ----------
        k : int
            the parameter to be selected.
        """
        return super( RepeatingModel, self ).getPrior( k % self.deltaNpar )

    def baseName( self ):
        """ Return a string representation of the model.  """
        return ( "Repeat  Model" )
#        return ( "Repeat %d times:\n  " % self.ncomp + self.model.baseName( ) )

    def baseParameterName( self, k ):
        """
        Return the name of the indicated parameter.

        Parameters
        ----------
        k : int
            parameter number.

        """
        if k < self.model.npchain :
            return self.model.getParameterName( k ) + "_0"

        k -= self.model.npchain
        i = self.index[ k % self.deltaNpar ]
        return ( self.model.getParameterName( i ) + "_%d" %
                ( 1 + k / self.deltaNpar ) )

    def baseParameterUnit( self, k ):
        """
        Return the unit of the indicated parameter.

        Parameters
        ----------
        k : int
            parameter number.

        """
        self.model.xUnit = self.xUnit
        self.model.yUnit = self.yUnit

        if k >= self.model.npchain :
            k -= self.model.npchain
            k = self.index[ k % self.deltaNpar ]

        return self.model.getParameterUnit( k )
