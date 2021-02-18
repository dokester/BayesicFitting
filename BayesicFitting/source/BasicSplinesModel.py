import numpy as numpy
from . import Tools
from .Tools import setAttribute as setatt
from .Formatter import formatter as fmt
import matplotlib.pyplot as plt

from .SplinesModel import SplinesModel
from .PolynomialModel import PolynomialModel


from .kernels.Kernel import Kernel
from .kernels.Tophat import Tophat

__author__ = "Do Kester"
__year__ = 2021
__license__ = "GPL3"
__version__ = "2.7.0"
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
#  *    2020 - 2021 Do Kester

class BasicSplinesModel( SplinesModel ):
    """
    Splines model consisting of a basis of spline blobs.

    The blobs have limited support. Each blob is a segment of polynomial order,
    between 2 knots. At the knots they are continuous (differentiable) upto order - 1.
    Similarly the edges of the blobs are smoothly connected to 0.

    order   support behaviour between knots     continuity at knots
      0        1    piecewise constant          not continuous at all
      1        2    piecewise linear            lines are continuous (connected)
      2        3    parabolic pieces            1st derivatives are also continuous
      3        4    cubic pieces                2nd derivatives are also continuous
     n>3      n+1   n-th order polynomials      (n-1)-th derivatives are also continuous

    The function result is the sum over all spline blobs, multiplied with
    the parameters, the amplitudes of the spline blobs.

    The support of the knots defined the domain where the function is defined. They are
    hard edges. Consequently the function is not continuous or differentiable at the edges.
    The spline blobs at the edges may be different from the ones in the middle.


    From SplinesModel
    -----------------
    The user lays out a number ( << datapoints ) of knots on the x-axis at
    arbitrary position, generally more knots where the curvature is higher.
    The knots need to be monotonuously increasing in x.
    Alternatively one can ask this class to do the lay-out which is then
    equidistant in x over the user-provided range.
    Through these knots a splines function is obtained which best
    fits the datapoints. One needs at least 2 knots, one smaller and one
    larger than the x-values in the dataset.

    This model is NOT for (cubic) spline interpolation.

    Examples
    --------
    >>> knots = numpy.arange( 17, dtype=float ) * 10    # make equidistant knots from 0 to 160
    >>> csm = BasicSplinesModel( knots=knots, order=2 )
    >>> print csm.getNumberOfParameters( )
    18
    # or alternatively:
    >>> csm = SplinesModel( nrknots=17, order=2, min=0, max=160 )    # automatic layout of knots
    >>> print csm.getNumberOfParameters( )
    18
    # or alternatively:
    >>> npt = 161                                               # to include both 0 and 160.
    >>> x = numpy.arange( npt, dtype=float )                    # x-values
    >>> csm = BasicSplinesModel( nrknots=17, order=2, xrange=x )     # automatic layout of knots
    >>> print csm.getNumberOfParameters( )
    18

    Attributes
    ----------
    knots : array_like
        positions of the spline knots
    order : int
        order of the spline. default: 3

    Attributes from Model
    ---------------------
        npchain, parameters, stdevs, xUnit, yUnit

    Attributes from FixedModel
    --------------------------
        npmax, fixed, parlist, mlist

    Attributes from BaseModel
    --------------------------
        npbase, ndim, priors, posIndex, nonZero, tiny, deltaP, parNames


    Limitations
    -----------
    Dont construct the knots so closely spaced, that there are no datapoints in between.

    """
    def __init__( self, knots=None, order=3, nrknots=None, min=None, max=None, xrange=None,
                        border=0, copy=None, **kwargs ):
        """
        Splines on a given set of knots and a given order.

        The number of parameters is ( length( knots ) + order - 1 )

        Parameters
        ----------
        knots : array_like
            a array of arbitrarily positioned knots
        order : int
            order of the spline. Default 3 (cubic splines)
        nrknots : int
            number of knots, equidistantly posited over xrange or [min,max]
        border : [0, 1, 2]
            defines what happens at the borders of the knot range.
            0 : Just like de Boors b-splines.
                the model is NOT defined outside the knot range.
            1 : periodic, make knot[0] the same as knot[-1]
            2 : easy borders. the model is slightly extensable.
        min : float
            minimum of the knot range
        max : float
            maximum of the knot range
        xrange : array_like
            range of the xdata
        copy : BasicSplinesModel
            model to be copied.
        fixed : None or dictionary of {int:float|Model}
            int         index of parameter to fix permanently.
            float|Model values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
            See: @FixedModel

        Raises
        ------
        ValueError : At least either (`knots`) or (`nrknots`, `min`, `max`) or
                (`nrknots`, `xrange`) must be provided to define a valid model.

        Notes
        -----
        The SplinesModel is only strictly valid inside the domain defined by the
        minmax of knots. It deteriorates fastly going outside the domain.

        """
        if knots is None and nrknots is None :
            raise ValueError( "Need either knots or (nrknots,min,max) or (nrknots,xrange)" )

        npar = nrknots if knots is None else len( knots )
        npar += order - 1 if border == 0 else -1

        super( ).__init__( nparams=npar, knots=knots, order=order, nrknots=nrknots,
                           min=min, max=max, xrange=xrange, copy=copy, **kwargs )

        self.border = border
        self.makeBasis = self.makeBaseBasis if border == 0 else self.makePeriodicBasis

        if copy is None :
            self.poly = PolynomialModel( self.order )
            self.basis = self.makeBasis()
        else :
            self.poly = copy.poly
            self.basis = copy.basis.copy()



    def copy( self ):
        return BasicSplinesModel( knots=self.knots, border=self.border, copy=self )

    def __setattr__( self, name, value ):
        """
        Set attributes: knots, order

        """
        if name == "basis" :
            setatt( self, name, value )
        elif name == "border" :
            setatt( self, name, value, type=int )
        elif name == "poly" :
            setatt( self, name, value, type=PolynomialModel )
        elif name == "makeBasis" :
            setatt( self, name, value )
        else :
            super( ).__setattr__( name, value )

    def makeBaseBasis( self ) :
        """
        Make a sets of polynomial bases for each of the parameters

        Return
        ------
        basis : 3-d array-like
            parameters to the polynomials that make up the spline blobs

        """
        np = self.order + 1
        nk = len( self.knots )
        hi = 1
        lo = 0

        basis = numpy.zeros( (nk-1,np,self.npmax), dtype=float )
        for k in range( self.npmax ) :

            if hi < nk : hi += 1
            if k >= np : lo += 1

            knotix = numpy.arange( lo, hi, dtype=int )
            dist = self.makeDist( knotix )

            bpar = self.findParameters( knotix, dist, kpar=k )
            bpar = numpy.reshape( bpar, ( -1, np ) )

            basis[knotix[:-1],:,k] =  bpar

        basis = self.normalizeBasis( basis )

        return basis

    def makeDist( self, knotix ) :
        return self.knots[knotix[:-1]+1] - self.knots[knotix[:-1]]


    def makePeriodicBasis( self ) :
        """
        Make a sets of polynomial bases for each of the parameters

        Return
        ------
        basis : 3-d array-like
            parameters to the polynomials that make up the spline blobs

        """
        if self.order == 0 :
            return self.makeBaseBasis()

        np = self.order + 1
        nk = len( self.knots )
        nh = ( np + 1 ) // 2

        basis = numpy.zeros( (nk-1,np,self.npmax), dtype=float )

        knotix = numpy.zeros( np + 1, dtype=int )
        knotix[:np] = numpy.arange( np, dtype=int ) - np - 1

        for k in range( self.npmax ) :
            dist = self.knots[knotix+1] - self.knots[knotix]

            bpar = self.findParameters( knotix, dist )
            bpar = numpy.reshape( bpar, ( -1, np ) )


            km = knotix[:-1] % nk
            basis[km,:,k] =  bpar

            knotix = numpy.where( knotix == -2, 0, knotix + 1 )

        basis = self.normalizeBasis( basis )
        return basis

    def normalizeBasis( self, basis ) :
        """
        Normalize the base splines such that a constant value of 1.0
        is returned when all model parameters are 1.

        Parameters
        ----------
        basis : array_like
            parameters to the polynomials that make up the spline blobs
        """

        ## normalize the blobs to 1
        np = self.npmax
        nk = len( self.knots )
        mat = numpy.zeros( (np,np), dtype=float )

        if self.order % 2 == 0 :
            xmid = ( self.knots[1:] + self.knots[:-1] ) / 2
        else :
            k = 1 - self.border             ## only for border 0 and 1
            xmid = self.knots[k:-1]

        if self.border == 1 or self.order == 0 :
            xx = xmid
        elif nk == 2 :
            xx = numpy.linspace( self.knots[0], self.knots[-1], np, dtype=float )
        else :
            xx = numpy.zeros( np, dtype=float )
            xx[0] = self.knots[0]
            xx[-1] = self.knots[-1]

            ne = np - nk
            ds = ( self.knots[1]  - self.knots[0]  ) / ne
            de = ( self.knots[-1] - self.knots[-2] ) / ne
            ks = self.knots[0] + ds
            ke = self.knots[-1] - de
            ne = ne // 2
            for k in range( ne ) :
                xx[ 1+k] = ks
                xx[-2-k] = ke
                ks += ds
                ke -= de

            xx[1+ne:-1-ne] = xmid

        x2k = self.makeKnotIndices( xx )

        for k in range( np ) :
            mat[:,k] = self.basicBlob( xx, basis[:,:,k], x2k, self.poly )

        beta = numpy.ones( np, dtype=float )
        bpar = numpy.linalg.solve( mat, beta )

        return basis * bpar


    def findParameters( self, knotix, dist, kpar=0 ) :
        """
        Find the parameters by assuming (order-1) continuous differentials.
        At the edges it is less. Normalized to 1.0


        Parameters
        ----------
        knotix : int array
            knot indices involved in this spline blob
        dist : array_like
            distances between knots
        kpar : int
            index of parameter for which the spline-blob is constructed

        Returns
        -------
        par : 2-d array
            sets of poly parameters.
        """
        lo = knotix[0]
        hi = knotix[-1] + 1

        knots = self.knots
        order = self.order
        k0 = order + 1
        np = ( len( knotix ) - 1 ) * k0
        nk = len( knots )

        mat = numpy.zeros( ( np, np ), dtype=float )
        kdf = numpy.arange( k0, dtype=int )

        i = 0
        n = 0
        ks = 0

        ## handling of the left side (edge)
        ## values and diffs all zero
        ff = numpy.ones( k0, dtype=float )
        x0 = numpy.power( 0.0, kdf )                ## center (== 0 ) is at each left knot

        ne1 = min( order, kpar ) if self.border == 0 else order
        while n < ne1 :
            mat[n, kdf] = x0 * ff
            x0 = numpy.roll( x0, 1 )
            ff *= numpy.roll( kdf, n )
            n += 1

        ## for normalization
        if n == 0 :
            mat[-1,i+kdf] = x0

        ## non-edge knots : both poly pieces (and diffs) are same
        ne = min( ks + k0, hi - 1 )
        ne = ks + len( knotix ) - 2

        while ks < ne :
            x0 = numpy.power( 0.0, kdf )    ## value of the left side knot
            kc = dist[ks]
            xx = numpy.power( kc, kdf )     ## value of the right side knot

            # normalization
            if 0 <= i < np : mat[-1,i+kdf] = xx

            ## values at xx (left side params) are equal to values at x0 (right side params)
            ff = numpy.ones( k0, dtype=float )
            idf1 = i + kdf
            idf2 = idf1 + k0
            for k in range( order ) :
                mat[n, idf1] = +xx * ff
                mat[n, idf2] = -x0 * ff
                xx = numpy.roll( xx, 1 )
                x0 = numpy.roll( x0, 1 )
                ff *= numpy.roll( kdf, k )
                n += 1

            i += k0
            ks += 1

        ## right side edge
        ff = numpy.ones( k0, dtype=float )
        xx = numpy.power( dist[ks], kdf )

        k = 0
        while n < np - 1 :
            mat[n, i+kdf] = xx * ff
            xx = numpy.roll( xx, 1 )
            ff *= numpy.roll( kdf, k )
            n += 1
            k += 1

        """
        ## more normalization
        if kpar > 0 :
            mat[-1,-1] = 1.0             ## at right normalize to 1.0

        """
        if kpar > 0 :
            if len( knotix ) == 2 :
                cc = ( ( np - kpar ) * knots[0] + kpar * knots[1] ) / np
                mat[-1,i+kdf] = numpy.power( cc, kdf )
            else :
                mat[-1,i] = 1.0             ## at center normalize to 1.0

        ## beta vector: all zero except last one, is 1 (normalization)
        beta = numpy.zeros( np, dtype=float )
        beta[-1] = 1.0

#        print( fmt( mat, max=None ) )

        try :
            ## solve linear set of equations
            bspar = numpy.linalg.solve( mat, beta )
        except numpy.linalg.LinAlgError :
            mat[-1,-1] = 1.0
            bspar = numpy.linalg.solve( mat, beta )

        return bspar


    def baseResult( self, xdata, params ):
        """
        Returns the functional result at the input value.

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the partials
        params : array_like
            parameters to the model (ignored in LinearModels)

        """
        np = self.npmax
        na = self.order + 1

        x2k = self.makeKnotIndices( xdata )

        pa = numpy.inner( self.basis, params )
        res = numpy.zeros_like( xdata )
        for k, kn in enumerate( self.knots[:-1] ) :
            q = numpy.where( x2k == k )
            xc = xdata[q] - kn
            res[q] = self.poly.result( xc, pa[k,:] )

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
            parameters to the model (ignored in LinearModels)
        parlist : array_like
            list of indices active parameters (or None for all)

        """
        np = self.npbase
        ni = Tools.length( xdata )
        partial = numpy.zeros( ( ni, np), dtype=float )

        if parlist is None :
            parlist = range( self.npmax )

        x2k = self.makeKnotIndices( xdata )
        for k,kb in enumerate( parlist ) :
            bss = self.basis[:,:,kb]
            partial[:,k] = self.basicBlob( xdata, bss, x2k, self.poly )

        return partial

        """
        for kb in range( np ) :
            bss = self.basis[:,:,kb]
            partial[:,kb] = self.basicBlob( xdata, bss, x2k, self.poly )

        return partial
        """

    def makeKnotIndices( self, xdata ) :
        """
        Return a list of indices of the knots immediately preceeding the xdata.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the indices
        """
        ix = numpy.zeros( len( xdata ), dtype=int )
        for kn in self.knots[1:-1] :
            ix = numpy.where( xdata >= kn, ix + 1, ix )

        return ix


    def basicBlob( self, xdata, basis, x2k, poly ) :
        """
        Calculates a spline blob for all of xdata

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the spline
        basis : array_like
            splineParameters
        x2k : int_array
            pointing to the knot preceeding each xdata point
        poly : PolynomialModel
            model to calculate the splines
        """
        blob = numpy.zeros_like( xdata )

        kn = self.knots[:-1]
        for k, kn in enumerate( self.knots[:-1] ) :
            if all( basis[k,:] == 0 ) : continue
            q = numpy.where( x2k == k )
            xc = xdata[q] - kn
            blob[q] = poly.result( xc, basis[k,:] )

        return blob

    def baseDerivative( self, xdata, params ) :
        """
        Return the derivative df/dx at each xdata (=x).

        Parameters
        ----------
        xdata : array_like
            value at which to calculate the partials
        params : array_like
            parameters to the model

        """
        dfdx = numpy.zeros_like( xdata )
        if self.order == 0 :
            return dfdx

        polym1 = PolynomialModel( self.order - 1 )
        x2k = self.makeKnotIndices( xdata )

        fp = numpy.arange( self.order + 1 )
        for n in range( self.npmax ) :
            dbs = self.basis[:,:,n] * fp
            dbs = dbs[:,1:]
            dfdx += self.basicBlob( xdata, dbs, x2k, polym1 ) * params[n]

        return dfdx

    def baseName( self ):
        """ Returns a string representation of the model. """
        return "BasicSplines of order %d with %d knots."%( self.order, len( self.knots) )

    def baseParameterUnit( self, k ):
        """
        Return the name of the parameter.

        Parameters
        ----------
        k : int
            index of the parameter.
        """
        return self.yUnit

