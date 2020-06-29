import numpy as numpy
import math

from .BaseFitter import BaseFitter

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
__version__ = "2.5.3"
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
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2003 - 2014 Do Kester, SRON (JAVA code)
#  *    2016 - 2020 Do Kester

class QRFitter( BaseFitter ):
    """
    Fitter for linear models, using QR decomposition.
    The QRFitter class is to be used in conjunction with Model classes, linear
    in its parameters.

    For Linear models the matrix equation

        H * p = &beta;

    is solved for p. H is the Hessian matrix ( D * w * D^T )
    and &beta; is the inproduct of the data with the D, design matrix.

        &beta; = y * w * D^T

    The QRFitter class use QR decomposition which effectively is an inversion
    of the hessian matrix such that

        p = &beta; * inverse( H )

    It can be more efficient if
    similar ydata needs to be fitter to the same model and xdata.
    In that case it uses the same decomposition for all fits.

    Examples
    --------
    # assume x and y are numpy.asarray data arrays:
    >>> x = numpy.asarray.range( 100 )
    >>> poly = PolynomialModel( 1 )                             # line
    >>> fitter = QRFitter( x, poly )
    >>> for k in range( 1, 4 ) :
    >>>     y = numpy.arange( 100 ) // k                        # digitization noise
    >>>     param = fitter.fit( y )                             # use same QR decomposition
    >>>     stdev = fitter.stdevs                               # stdevs on the parameters
    >>>     print( k, param )
    >>>     print( " ", stdev )

    Category:    Mathematics/Fitting

    Attributes
    ----------
    needsNewDecomposition : bool
        True when starting. Thereafter False,
            i.e. the previous QR-decomposition is used, unless weights are used.
            Only for linear fitters, setting it to false might improve efficiency.
            It only works properly when the model, the x-data etc are exactly the
            same in the previous run.
            Whenever weights are used, it always needs a new decomposition.

    qrmat : matrix
        matrix formed by q * inverse( r ), where q,r is the QR decomposition
        of the design matrix.
        qrmat is to be multiplied with the data vector to get the solution.

    """

    def __init__( self, xdata, model, map=False, keep=None ):
        """
        Create a new Fitter, providing xdatas and model.

        A Fitter class is defined by its model and the input vector (the
        independent variable). When a fit to another model and/or another
        input vector is needed a new object should be created.

        Parameters
        ----------
        xdata : array_like
            array of independent input values
        model : Model
            the model function to be fitted
        map : bool (False)
            When true, the xdata should be interpreted as a map.
            The fitting is done on the pixel indices of the map,
            using ImageAssistant
        keep : dict of {int:float}
            dictionary of indices (int) to be kept at a fixed value (float)
            The values of keep will be used by the Fitter as long as the Fitter exists.
            See also `fit( ..., keep=dict )`

        """
        super( QRFitter, self ).__init__( xdata, model, map=map, keep=keep )

        self.needsNewDecomposition = True
        self.qrmat = None

    def fit( self, ydata, weights=None, keep=None ):
        """
        Return model parameters fitted to the data, including weights.

        Parameters
        ----------
        ydata : array_like
            the data vector to be fitted
        weights : array_like
            weights pertaining to the data ( = 1.0 / sigma^2 )
        keep : dict of {int:float}
            dictionary of indices (int) to be kept at a fixed value (float)
            The values will override those at initialization.
            They are only used in this call of fit.
        Raises
        ------
        ValueError when ydata or weights contain a NaN

        """
        fi, ydata, weights = self.fitprolog( ydata, weights=weights, keep=keep )

        if self.model.isNullModel() :
            self.chiSquared( ydata, weights )
            return numpy.asarray( 0 )

        ydatacopy = ydata.copy( )
        # subtract influence of fixed parameters on the data
        if fi is not None :
            fxpar = numpy.copy( self.model.parameters )
            fxpar[fi] = 0.0
            ydatacopy = numpy.subtract( ydatacopy, self.model.result( self.xdata, fxpar) )

        wgts = ( numpy.ones_like( ydata, dtype=float ) if weights is None else
                 numpy.sqrt( weights ) )

        if hasattr( self, "normdata" ) :
            normweight = math.sqrt( self.normweight )
            ydatacopy = numpy.append( ydatacopy, self.normdata )
            wgts = numpy.append( wgts, normweight )

        ydatacopy = ydatacopy * wgts

        if self.needsNewDecomposition or weights is not None:
            design = ( self.getDesign( index=fi ).transpose() * wgts ).transpose()

            # The QR decomposition in numpy has a different interface from that in scipy.
            # Here we use numpy. See:
            #   https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.qr.html

            q, r = numpy.linalg.qr( design )
            self.qrmat = numpy.dot( numpy.linalg.inv( r ), q.transpose() )
            self.needsNewDecomposition = False

        params = numpy.dot( self.qrmat, ydatacopy )

        params = self.insertParameters( params, index=fi )
        self.model.parameters = params
        self.chiSquared( ydata, weights=weights )

        return params

#  *************************************************************************
    def __str__( self ):
        """ Return the name of the fitter. """
        return "QRFitter"


