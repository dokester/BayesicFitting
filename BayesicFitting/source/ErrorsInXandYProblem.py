import numpy as numpy
from astropy import units
import re
import warnings
from . import Tools

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
#  *    2018        Do Kester

class ErrorsInXandYProblem( Problem ):
    """
    A ErrorsInXandYProblem is an optimization of parameters which involves
    the fitting of data to a Model, where both the ydata and the xdata
    contain errors.

    It entails that the xdata are not at the exact locations. They need to
    be optimized too. Consequently the parameters of the model are appended
    with a set of parameters, the length of xdata. These extra parameters
    will contain the target locations of the xdata. The 2-dimensional distance
    between data (xdata,ydata) and (target, model(target)) is minimised.
    The target are nuisance parameters which are not part of the modeling
    solution.

    As the targets need to be optimised they need a Prior. In the present
    implementation there is the same Prior for all targets, which the centered on
    each of the xdata values.
    S.Gull (1989) argues to use a GaussPrior with a scale similar to the errors
    in both X and Y.

    Attributes
    ----------
    prior : Prior
        Priors for the x-axis nuisance parameters.


    Attributes from Problem
    -----------------------
    model, xdata, ydata, weights, partype


    Author :         Do Kester

    """

    #  *************************************************************************
    def __init__( self, model=None, xdata=None, ydata=None, weights=None,
                    prior=None, copy=None ):
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
        prior : Prior
            prior for the x-axis nuisance parameters. All centered on each of the xdata
        copy : Problem
            to be copied

        """
        super( ).__init__( model=model, xdata=xdata, ydata=ydata, weights=weights, copy=copy )
        self.npars += Tools.length( self.xdata )

        if copy is None :
            self.prior = prior
        else :
            self.prior = copy.prior


    def copy( self ):
        """
        Copy.

        """
        return ErrorsInXandYProblem( copy=self )

    #  *****RESULT**************************************************************
    def result( self, param ):
        """
        Returns the result calculated at the xdatas.

        Parameters
        ----------
        param : array_like
            values for the parameters + nuisance params.

        """
        ( xd, pars ) = self.splitParam( param )
        return self.model.result( xd, pars )


    def splitParam( self, param ) :
        """
        Split the parameters into Model parameters and targets.
        """
        np = self.model.npars
        return ( param[np:], param[:np] )


    def partial( self, param ) :
        """
        Return the partials as a matrix [2*nx,np+nx], where nx is the number of
        datapoints and np the number of parameters in the model.
        The upper left submatrix [nx,np] contains dM/dp
        the upper right submatrix [nx,nx] contains dM/dx on the diagonal
        the lower left submatrix [nx,np] contains zeros
        the lower right submatrix [nx,nx] contains the identity matrix

        """
        ( xd, pars ) = self.splitParam( param )
        np = self.model.npars
        nx = len( xd )
        part = numpy.zeros( ( 2*nx, np+nx ), dtype=float )
        part[:nx,:np] = self.model.partial( xd, pars )
        dfdx = self.model.derivative( xd, pars )
        for k in range( nx ) :
            part[k,k+np] = dfdx[k]
            part[k+nx,k+np] = 1.0
        return part

    def derivative( self, param ) :
        """
        Return the derivative to the Model.

        Parameters
        ----------
        params : array_like
            list of problem parameters
        """

        ( xd, pars ) = self.splitParam( param )
        return self.model.derivative( xd, pars )

    def domain2Unit( self, dval, kpar ) :
        """
        Return value in [0,1] for the selected parameter.

        Parameters
        ----------
        dval : float
            domain value for the selected parameter
        kpar : int
            selected parameter index, where kp is index in [parameters, hyperparams]
        """
        if kpar < self.model.npars :
            return self.model.domain2Unit( dval, kpar )

        kp = kpar - self.model.npars
        dv = dval - self.xdata[kp]

        return self.prior.domain2Unit( dv )

    def unit2Domain( self, uval, kpar ) :
        """
        Return domain value for the selected parameter.

        Parameters
        ----------
        uval : array_like
            unit value for the selected parameter
        kpar : int
            selected parameter indices, where kp is index in [parameters, hyperparams]
        """
        if kpar < self.model.npars :
            return self.model.unit2Domain( uval, kpar )

        return self.prior.unit2Domain( uval ) + self.xdata[kpar-self.model.npars]

    def residuals( self, param, mockdata=None ) :
        """
        Return the (weighted) true distance between (xdata,ydata) and (xtry,ytry) where xtry are
        the trial values for xdata and ytry = model.result( xtry, param )

        res = hypothenusa( xdata - xtry, ydata - ytry ) * weights

        Parameters
        ----------
        param : array_like
            model parameters and xdata parameters
        mockdata : array_like
            model fit data model.result( xtry, param )
        """
        ( xd, pars ) = self.splitParam( param )
        res = self.ydata - self.result( param )
        return numpy.hypot( res, self.xdata - xd )


    def weightedResiduals( self, param, mockdata=None, extra=False ) :
        """
        Returns the (weighted) residuals, calculated at the xdata.

        Parameters
        ----------
        param : array_like
            values for the parameters.
        mockdata : array_like
            model fit at xdata
        extra : bool (False)
            true  : return ( wgt * dist, wgt * [yres,xres] / dist )
            false : return wgt * dist
        """
        ( xd, pars ) = self.splitParam( param )
        yres = self.ydata - self.result( param )
        xres = self.xdata - xd
        dist = numpy.hypot( xres, yres )

        if extra :
            if self.weights is None :
                exres = numpy.append( yres / dist, xres / dist )
                return ( dist, exres )
            else :
                exres = numpy.append( self.weights * yres / dist, self.weights * xres / dist )
                return ( dist * self.weights, exres )
        else :
            return dist if self.weights is None else dist * self.weights



    def weightedResSq( self, param, mockdata=None, extra=False ) :
        """
        Return the (weighted) squared distance between (xdata,ydata) and (xtry,ytry) where xtry are
        the trial values for xdata and ytry = model.result( xtry, param )

        Parameters
        ----------
        param : array_like
            model parameters and xdata parameters
        mockdata : array_like
            model fit data model.result( xtry, param )
        extra : bool (False)
            true  : return ( wgt * res^2, wgt * [yres,xres] )
            false : return wgt * res^2
        """
        ( xd, pars ) = self.splitParam( param )
        yres = self.ydata - self.result( param )
        xres = self.xdata - xd

        res2 = numpy.square( yres ) + numpy.square( xres )
        if extra :
            if self.weights is not None :
                res2 *= self.weights
                xres *= self.weights
                yres *= self.weights
            return ( res2, numpy.append( yres, xres ) )

        return res2 if self.weights is None else res2 * self.weights

    def myEngines( self ) :
        """
        Return a default list of preferred engines
        """
        return ["galilean", "gibbs", "chord"]

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
    def __str__( self ):
        """ Returns a string representation of the model.  """
        return "ErrorsInXandYProblem of %s" % self.model



