import numpy as numpy
import re

from .Tools import setAttribute as setatt
from .Dynamic import Dynamic

__author__ = "Do Kester"
__year__ = 2022
__license__ = "GPL3"
__version__ = "3.0.0"
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
#  *    2018 - 2022 Do Kester

class Problem( object ):
    """
    Problem implements the common parts of specialized Problems.

    A Problem is an optimization of parameters which does not involve
    the fitting of data to a Model.

    Problems can be solved by NestedSampler, with appropriate Engines and
    ErrorDistributions.

    The result of the function for certain x and p is given by
    problem.result( x, p )
    The parameters, p, are to be optimized while the x provide additional
    information.

    This class is a base class. Further specializations will define the
    result method.

    Attributes
    ----------
    model : Model
        to be optimized
    xdata : array_like
        independent variable (static)
    ydata : array_like
        dependent variable (static)
    weights : array_like
        weights associated with ydata
    npars : int
        number of parameters in the model of the problem
    partype : float | int
        type of the parameters


    Author :         Do Kester

    """

    #  *************************************************************************
    def __init__( self, model=None, xdata=None, ydata=None, weights=None, copy=None ):
        """
        Problem Constructor.

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
        super( ).__init__( )

        if copy is None :
            self.xdata = None if xdata is None else numpy.asarray( xdata )
            self.ydata = None if ydata is None else numpy.asarray( ydata )
            self.model = model
            self.weights = None if weights is None else numpy.asarray( weights )
            self.partype = float
        else :
            self.xdata = copy.xdata
            self.ydata = copy.ydata
            self.weights = copy.weights
            if copy.model and ( copy.model.isDynamic() or copy.model.isModifiable() ) :
                self.model = copy.model.copy()
            else :
                self.model = copy.model
            self.partype = copy.partype

        if self.model is None or not hasattr( self.model, "cyclic" ) :
            self.cyclicCorrection = self.cycor0
        elif isinstance( self.model.cyclic, dict ) :
            self.cyclicCorrection = self.cycor2
        else :
            self.cyclicCorrection = self.cycor1

    def copy( self ):
        """
        Copy.

        """
        return Problem( copy=self )


    def __setattr__( self, name, value ):
        """
        Set attributes.

        """
        setatt( self, name, value )
        if name == "weights" :
            try :
                delattr( self, "sumweight" )
            except :
                pass

    def __getattr__( self, name ) :
        """
        Return value belonging to attribute with name.

        Parameters
        ----------
        name : string
            name of the attribute
        """
        if name == 'npars' :
            return self.model.npars

        elif name == 'sumweight' :            # Return the sum over weight vector.
            if self.hasWeights() :
                self.sumweight = numpy.sum( self.weights )
                return self.sumweight
            else :
                return self.ndata
        elif name == 'ndata' :
            self.ndata = len( self.ydata )        # number of data points/tuples
            return self.ndata
        else :
            raise AttributeError( "Unknown attribute " + name )

        return None

    def hasWeights( self ):
        """ Return whether it has weights.  """
        return self.weights is not None


    #  *****RESULT**************************************************************
    def result( self, param ):
        """
        Returns the result using the parameters.

        In this (base)class it is a placeholder.

        Parameters
        ----------
        param : array_like
            values for the parameters.

        """
        pass


    def residuals( self, param, mockdata=None ) :
        """
        Returns the residuals, calculated at the xdata.

        Parameters
        ----------
        param : array_like
            values for the parameters.
        mockdata : array_like
            model fit at xdata

        """
        res = self.ydata - ( self.result( param ) if mockdata is None else mockdata )
        return self.cyclicCorrection( res )

    def cycor0( self, res ):
        """
        Returns the residuals, unadultered

        Parameters
        ----------
        res : array_like
            residuals

        """
        return res

    def cycor1( self, res ):
        """
        Returns the residuals, all corrected for periodicity in residuals

        Parameters
        ----------
        res : array_like
            residuals

        """
        return self.cyclize( res, self.model.cyclic )

    def cycor2( self, res ):
        """
        Returns the residuals corrected for periodicity in residuals, only
        the result dimensions listed in the model.cyclic dictionary.

        Parameters
        ----------
        res : array_like
            residuals

        """
        cyclic = self.model.cyclic
        for key in cyclic.keys() :
            res[:,key] = self.cyclize( res[:,key], cyclic[key] )
        return res

    def cyclize( self, res, period ) :
        """
        Apply correction on residuals which are cyclic in some
        phase space.

        If the model results in a phase value of +&epsilon;
        while the data give that phase value as (p - &epsilon;)
        to keep all data in the range [0,p], the naive residual
        would be (p - 2 &epsilon;) while the actual distance should
        be measured the other way around as (2 &epsilon;).
        Here p = period and &epsilon; = small deviation.

        Parameters
        ----------
        res : array_like
            original residuals
        period : float
            of the phase space

        Returns
        -------
        corrected residuals.
        """

        hp = period / 2
        return numpy.where( res < -hp, res + period,
               numpy.where( res >  hp, res - period, res ) )



    def weightedResiduals( self, param, mockdata=None, extra=False ) :
        """
        Returns the (weighted) residuals, calculated at the xdata.

        Optionally (extra=True) the weighted signs of the residuals are returned too.

        Parameters
        ----------
        param : array_like
            values for the parameters.
        mockdata : array_like
            model fit at xdata
        extra : bool (False)
            true  : return ( wgt * res, wgt * sign( res ) )
            false : return wgt * res
        """
        res = self.residuals( param, mockdata=mockdata )

        if extra :
            if self.weights is None :
                wgt = numpy.ones_like( self.ydata )
                return ( res, numpy.copysign( wgt, res ) )
            else :
                return ( res * self.weights, numpy.copysign( self.weights, res ) )
        else :
            return res if self.weights is None else res * self.weights


    def weightedResSq( self, param, mockdata=None, extra=False ) :
        """
        Returns the (weighted) squared residuals, calculated at the xdata.

        Optionally (extra=True) the weighted residuals themselves are returned too.

        Parameters
        ----------
        param : array_like
            values for the parameters.
        mockdata : array_like
            model fit at xdata
        extra : bool (False)
            true  : return ( wgt * res^2, wgt * res )
            false : return wgt * res^2
        """
        res = self.residuals( param, mockdata=mockdata )

        resw = res if self.weights is None else res * self.weights
        return ( resw * res, resw ) if extra else resw * res

    def isDynamic( self ) :
        return self.model.isDynamic()


    def domain2Unit( self, dval, kpar ) :
        """
        Return value in [0,1] for the selected parameter.

        Parameters
        ----------
        dval : float
            domain value for the selected parameter
        kpar : array_like
            selected parameter index, where kp is index in [parameters, hyperparams]
        """
        return self.model.domain2Unit( dval, kpar )


    def unit2Domain( self, uval, kpar ) :
        """
        Return domain value for the selected parameter.

        Parameters
        ----------
        uval : array_like
            unit value for the selected parameter
        kpar : array_like
            selected parameter indices, where kp is index in [parameters, hyperparams]
        """
        return self.model.unit2Domain( uval, kpar )

    #  *****TOSTRING***********************************************************
    def __str__( self ):
        """ Returns a string representation of the model.  """
        return self.baseName( )

    def _toString( self, spaces ) :
        return self.baseName()


    def shortName( self ):
        """
        Return a short version the string representation: upto first non-letter.

        """
        m = re.match( "^[a-zA-Z_]*", self.baseName() )
        return m.group(0)

    def baseName( self ) :
        return "Problem of %s" % self.model.shortName()

