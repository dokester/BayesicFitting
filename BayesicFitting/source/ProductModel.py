import numpy as numpy
from . import Tools
from .Model import Model
from .NonLinearModel import NonLinearModel
from astropy import units

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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2017        Do Kester

class ProductModel( NonLinearModel ):
    """
    Direct product of 2 (or more) models.
    The dimensionality of this model is equal to the number of constituent models.



    The number of parameters is the sum of the parameters of the models.


    Examples
    --------
    >>> nxk = 17
    >>> nyk = 11
    >>> xknots = numpy.arange(  nxk , dtype=float ) * 10      # make knots from 0 to 160
    >>> yknots = numpy.arange(  nyk , dtype=float ) * 10      # make knots from 0 to 100
    >>> csm = ProductModel( xknots, yknots, 2 )
    >>> print csm.getNumberOfParameters( )      # ( nxk + order - 1 ) + ( nyk + order - 1 )
    30
    # ... fitter etc. see Fitter

    Category     mathematics/Fitting

    Attributes
    ----------

    """

    def __init__( self, models, copy=None, fixed=None, **kwargs ):
        """
        Direct product of 2 (or more) models. It has dimensionality equal to
        the number of constituent models.

        The models are given as input the consecutive colums in xdata.

        The number of parameters is the sum of the parameters of the
        constituent models

        Parameters
        ----------
        models : list of Model
            the constituent models
        copy : ProductModel
            model to be copied
        fixed : dict
            If not None raise AttributeError.

        Raises
        ------
        ValueError
            When one of the models is 2 (ore more) dimensional
        AttributeErrr : When fixed is not None

        """
        if fixed is not None :
            raise AttributeError( "ProductModel cannot have fixed parameters" )

        np = 0
        for m in models :
            if m.ndim > 1 :
                raise ValueError( "Only 1-dim models are allowed in ProductModel" )
            np += m.npchain

        super( ProductModel, self ).__init__( np, ndim=len( models ), copy=copy, **kwargs )
        self.models = models

    def copy( self ):
        """ Copy method.  """
        mdls = [m.copy() for m in self.models]
        return ProductModel( mdls, copy=self )

    def __setattr__( self, name, value ):
        """
        Set attributes: models

        """
        dlst = {'models': Model }
        if Tools.setListOfAttributes( self, name, value, dlst ) :
            pass
        else :
            super( ProductModel, self ).__setattr__( name, value )

    def baseResult( self, xdata, params ):
        """
        Returns the partials at the input value.

        The partials are the powers of x (input) from 0 to degree.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the partials
        params : array_like
            parameters to the model.

        """
        ndata = Tools.length( xdata[:,0] )
        k = 0
        n = 0
        res = numpy.ones( ndata, dtype=float )
        for m in self.models :
            res *= m.result( xdata[:,k], params[n:n+m.npchain] )
            k += 1
            n += m.npchain
        return res


    def basePartial( self, xdata, params, parlist=None ):
        """
        Returns the partials at the input value.

        The partials are the powers of x (input) from 0 to degree.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the partials
        params : array_like
            parameters to the model.
        parlist : array_like
            not used in this model

        """
        ndata = Tools.length( xdata[:,0] )
        partial = numpy.ndarray( ( 0, ndata ), dtype=float )    # transpose of needed shape
        k = 0
        n = 0
        res = numpy.ones( ndata, dtype=float )
        for m in self.models :
            nm = n + m.npchain
            x = m.result( xdata[:,k], params[n:nm] )
            partial *= x
            p = res * m.partial( xdata[:,k], params[n:nm] ).transpose()
            partial = numpy.append( partial, p, axis=0 )
            res *= x
            k += 1
            n = nm
        return partial.transpose()                      # transpose back to proper shape

    def baseName( self ):
        """
        Returns a string representation of the model.

        """
        strm = ""
        ch = "xyzuvw"
        k = 0
        for m in self.models :
            strm += m.shortName() + "(%s) * " % ch[k]
            k += 1
        strm = strm[:-3]

        return str( "%dd-Product: f(%s:p) = %s"%(self.ndim, ch[:k], strm) )

    def baseParameterName( self, k ):
        """
        Return the name of a parameter as "param<dim>_<seq>.
        Parameters
        ----------
        k : int
            the kth parameter.

        """
        strpar = "param"
        m = 0
        for mdl in self.models :
            nx = mdl.npchain
            if k < nx :
                return strpar + "%d_%d"%(m,k)
            k -= nx
            m += 1
        return strpar

    def baseParameterUnit( self, k ):
        """
        Return the unit of a parameter.
        Parameters
        ----------
        k : int
            the kth parameter.

        """
        u = units.Unit( 1.0 )
        n = 0
        for mdl in self.models :
            nx = mdl.npbase
            if k < nx :
                return mdl.getParameterUnit( k ) / u
            n += 1
            k -= nx
            u = self.yUnit
        return u


