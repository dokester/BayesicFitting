import numpy as numpy
from astropy import units
import re
import warnings
from . import Tools
from .Tools import setAttribute as setatt

from .Problem import Problem
from .Formatter import formatter as fmt

__author__ = "Do Kester"
__year__ = 2024
__license__ = "GPL3"
__version__ = "3.2.1"
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

    Define
        xd = xdata, yd = ydata, u = target, F(u:P) = model( target )
    And the mismathes in both directions.
        X = u - xd 
        Y = F(u:p) - yd

    Both distances need to be minimized, possibly in the presence of a correlation 
    between the mismatches X and Y 

    As the targets need to be optimised they need a Prior. In the present
    implementation there is the same Prior for all targets, which the centered on
    each of the xdata values.
    S.Gull (1989) argues to use a GaussPrior with a scale similar to the errors
    in both X and Y.

    Attributes
    ----------
    prior : Prior
        Priors for the x-axis nuisance parameters.
    varxx : float or ndarray of shape (ndata,)
        Variance in the xdata errors
    varyy : float or ndarray of shape (ndata,)
        Variance in the ydata errors
    varxy : float or ndarray of shape (ndata,)
        Covariance in the xdata and ydata errors



    Attributes from Problem
    -----------------------
    model, xdata, ydata, weights, partype


    Author :         Do Kester

    """

    #  *************************************************************************
    def __init__( self, model=None, xdata=None, ydata=None, weights=None,
                    prior=None, covar=None, accuracy=None, copy=None ):
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
            weights associated with data
        covar : ndarray of shape (2,2) or (ndata,2,2)
            covariance matrix of the errors in x and y
            (2,2) : valid for all datapoints
            (ndata,2,2): one for each datpoint
            Default is [[1,0],[0,1]]
        accuracy : ndarray of shape (2,) or (3,) or (ndata,2) or (ndata,3)
            accuracy scale for the datapoints
            (2,) scale for resp. y and x, valid for all datapoints
            (3,) scale for y and y, and correlation coefficient between y and x, valid for all
            (ndata,2) or (ndata,3) one set of values for each datapoint
            Alternative for covarince matrix. 
            covar = [[ acc[0]^2, 0], [0, acc[1]^2]] no correlation
                  = [[ acc[0]^2, r], [r, acc[1]^2]] where r = acc[0] * acc[1] * acc[2]
            accuracy is converted to covar; default is covar.
        prior : Prior
            prior for the x-axis nuisance parameters. All centered on each of the xdata
        copy : Problem
            to be copied

        """
        super( ).__init__( model=model, xdata=xdata, ydata=ydata, weights=weights, copy=copy )
        self.npars += Tools.length( self.xdata )

        if copy is None :
            self.prior = prior
            self.setAccuracy( accuracy=accuracy, covar=covar )
        else :
            self.prior = copy.prior
            self.varxx = copy.varxx
            self.varxy = copy.varxy
            self.varyy = copy.varyy
            
            self.determinant = copy.determinant
            self.sumweight = copy.sumweight

    def copy( self ):
        """
        Copy.

        """
        return ErrorsInXandYProblem( copy=self )

    def __setattr__( self, name, value ):
        """
        Set attributes.

        """
        if name == "accuracy" :
            self.setAccuracy( accuracy=value )
        elif name == "covar" :
            self.setAccuracy( covar=value )
        else :
            super().__setattr__( name, value )


    def setAccuracy( self, accuracy=None, covar=None ) :
        """
        Store 3 items from the covar matrix : 

            | var_yy, var_xy |
            | var_xy, var_xx |

        When the accuracy is given, convert it to these items by
        var_yy = acc[0] * acc[0]
        var_xx = acc[1] * acc[1]
        var_xy = acc[0] * acc[1] * acc[2]

        Store also the determinant of the covariance matrix. 

        When both accuracy and covar are None
          var_yy = 0 
          var_xx = 1
          var_xy = 0

        Raises
        ------
        AttributeError. When both accuracy and covar are not None.

        Parameters
        ----------
        accuracy : ndarray of shape (2,) or (3,) or (ndata,2) or (ndata,3)
            accuracy scale for the datapoints
            (2,) scale for resp. y and x, valid for all datapoints
            (3,) scale for y and y, and correlation coefficient between y and x, valid for all
            (ndata,2) or (ndata,3) one set of values for each datapoint
            Alternative for covarince matrix. 
            vxy = 0 if no correlation else acc[0] * acc[1] * acc[2]
            covar = [[ acc[0]^2, vxy      ],
                     [ vxy     , acc[1]^2 ]] 
            accuracy is converted to covar; default is covar.
        covar : ndarray of shape (2,2) or (ndata,2,2) or None
            covariance matrix of the errors in x and y

        """
        hasAcc = True
        if accuracy is None :
            if  covar is None :
                varyy = 0.0         # scale will fill the value in this case
                varxx = 0.0
                varxy = 0.0
                hasAcc = False
            else :
                covar = numpy.asarray( covar )
                cdim = covar.ndim
                varyy = covar[0,0] if cdim == 2 else covar[:,0,0]
                varxx = covar[1,1] if cdim == 2 else covar[:,1,1]
                varxy = covar[0,1] if cdim == 2 else covar[:,0,1]
        else :
            if covar is None :
                accuracy = numpy.asarray( accuracy )
                adim = accuracy.ndim
#                print( "SetAcc  ", accuracy, adim )
                varxy = 0.0
                if adim == 0 :
                    varyy = accuracy
                    varxx = accuracy
                elif adim == 1 :
                    varyy = accuracy[0] 
                    varxx = accuracy[1]
                    if accuracy.shape[-1] == 3 :
                        varxy = accuracy[2]
                else :
                    varyy = accuracy[:,0]
                    varxx = accuracy[:,1]
                    if accuracy.shape[-1] == 3 :
                        varxy = accuracy[:,2]

                varxy *= varyy * varxx
                varyy *= varyy
                varxx *= varxx
            else :
                raise AttributeError( "Covar and Accuracy are mutually exclusive" )

        setatt( self, "hasAccuracy", hasAcc )
        setatt( self, "accuracy", accuracy if self.hasAccuracy else 0 )
        setatt( self, "varyy", varyy )
        setatt( self, "varxx", varxx )
        setatt( self, "varxy", varxy )

        det = varyy * varxx - varxy * varxy
        setatt( self, "determinant", det )


    def hasWeights( self ):
        """ Return whether it has weights.  """
        return self.weights is not None


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

        Parameters
        ----------
        param : array_like
            values for the parameters + nuisance params.

        Return
        ------
        tuple of ( targets, model parameters )

        """
        np = self.model.npars
        return ( param[np:], param[:np] )


    def partial( self, param ) :
        """
        Return the partials as a matrix [2*nx,np+nx], where nx is the number of
        datapoints and np the number of parameters in the model.

            The upper left submatrix (nx,np) contains dM/dp
            the upper right submatrix (nx,nx) contains dM/dx on the diagonal
            the lower left submatrix (nx,np) contains zeros
            the lower right submatrix (nx,nx) contains the identity matrix

        Parameters
        ----------
        param : array_like
            values for the parameters + nuisance params.

        """
        ( xd, pars ) = self.splitParam( param )
        np = self.model.npars
        nx = len( xd )

        part = numpy.zeros( ( 2*nx, np+nx ), dtype=float )

        idmat = numpy.identity( nx, dtype=float )
        ## upper-left  : model partial
        part[:nx,:np] = self.model.partial( xd, pars )
        ## upper-right : model derivative on diagonal
        part[:nx,np:] = self.model.derivative( xd, pars ) * idmat
        ## lower-left  : zeros
        ## lower-right : identity
        part[nx:,np:] = idmat

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

    def getXYresiduals( self, param ) :
        """
        Return residuals in y-direction and x-direction.

        Parameters
        ----------
        param : array_like
            model parameters and xdata parameters

        Returns
        -------
        tuple of (y residuals, x residuals)
        """
        ( xd, pars ) = self.splitParam( param )
        yres = self.ydata - self.model.result( xd, pars )
        return ( yres, self.xdata - xd )

    def weightedResSq( self, allpars, mockdata=None, extra=False ) :
        """
        Return the (weighted) squared distance between (xdata,ydata) and (xtry,ytry) where xtry are
        the trial values for xdata and ytry = model.result( xtry, param )

        Parameters
        ----------
        allpars : array_like
            model parameters, xdata parameters, and noise scale
        mockdata : array_like
            model fit data model.result( xtry, param )
        extra : bool (False)
            true  : return ( wgt * res^2, wgt * [yres,xres] )
            false : return wgt * res^2
        """
        np = self.npars 
        param = allpars[:np] 
        ( yres, xres ) = self.getXYresiduals( param )

        xres2 = xres * xres
        yres2 = yres * yres

        s2 = allpars[np] * allpars[np]
        det = self.determinant + s2 * ( self.varyy + self.varxx + s2 )

        # values from inverse covar matrix
        myy = ( self.varxx + s2 ) / det
        mxx = ( self.varyy + s2 ) / det
        mxy = -self.varxy / det

        yrot2 = yres2 * myy
        xrot2 = xres2 * mxx
        xyrot = xres * yres * mxy

        res2 = xrot2 + yrot2 + 2 * xyrot            # equiprobable distance squared

        if self.weights is not None : 
            res2 *= self.weights

        if not extra :
            return res2 

        xr = xres * mxx + yres * mxy
        yr = yres * myy + xres * mxy

        xyr2 = xres2 + yres2

        if self.weights is not None : 
            xr *= self.weights
            yr *= self.weights
            xyr2 *= self.weights

        return ( res2, numpy.append( yr, xr ), xyr2 )

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
        Return a default preferred ErrorDistribution: "gauss2d"
        """
        return "gauss2d"

    #  *****TOSTRING***********************************************************
    def baseName( self ):
        """ Returns a string representation of the model.  """
        return "ErrorsInXandYProblem"


