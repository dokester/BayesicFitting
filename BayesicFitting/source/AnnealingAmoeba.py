import numpy as numpy
import math
from . import Tools

from .Formatter import formatter as fmt
from .ConvergenceError import ConvergenceError

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

class AnnealingAmoeba( object ):
    """
    Simulated annealing simplex finding minimum.

    AnnealingAmoeba can be used in two modes: with simulated annealing on or off.
    The simulated annealing mode is invoked by setting the temperature to
    some value. By default it is off: temperature at zero.

    When the temperature is set at zero (default), AnnealingAmoeba acts as a
    simple Nelder-Mead downhill simplex method. With two advantages and one
    disadvantage. The pro's are that it is reasonably fast and that it does not
    need partial derivatives. The con is that it will fall into the first local
    minimum it encounters. No guarantee that this minimum has anything to do
    with the absolute minimum. This T=0 modus can only be used in mono-modal
    problems.

    In the other modus, when the temperature is set at some value the
    simplex sometimes takes a uphill step, depending on the temperature at
    that moment. Steps downhill are always taken. In that way it is possible
    to climb out of local minima to find better ones. Meanwhile the temperature
    is steadily lowered, concentrating the search on the by now hopefully found
    absolute minimum. Of course this takes much more iterations and still there
    is *no guarantee* that the best value is found. But a better chance.
    The initial temperature which suggests itself is of the order of the
    humps found in the minimizable lanscape.

    At each temperature level a number of moves is made. This number is set by
    the keyword steps=10, by default. After these steps the temperature is lowered
    with a factor set by cooling=0.95, by default.

    Iteration continues until the relative difference between the low and high
    points within the simplex is less than reltol
    ``|yhi - ylo| / ( |yhi| + |ylo| ) < reltol``
    and/or the absolute difference is less than abstol
    ``|yhi - ylo| < abstol``.

    AnnealingAmoeba can be used with limits set to one or more of the input values.

    The original version stems from Numerical Recipes with some additions of my own.

    Author       Do Kester

    Attributes
    ----------
    func : callable
        function to be minimized of form : `y = func( x )`
    lolimits : array_like
        lower limits on `x`. -inf is allowed to indicate no lower limit
    hilimits : array_like
        upper limits on `x`. +inf is allowed to indicate no upper limit
    fopt : float
        the best of the above values
    xopt : ndarray
        copy of the simplex point that has the best value (nx)

    rng : RandomState
        random number generator
    seed : int
        seed of rng

    reltol : float
        Relative tolerance. Program stops when ( |yhi-ylo| / (|yhi|+|ylo|) ) < reltol
    abstol : float
        Absolute tolerance. Program stops when |yhi-ylo| < abstol
    maxiter : int
        maximum number of iterations
    iter : int (read only)
        iteration counter
    ncalls : int (read only)
        numbers of calls to func

    temp : float
        annealing temperature (default: 0)
    cooling : float (non existent when temp=0)
        cooling factor (default: 0.95)
    steps : int (non existent when temp=0)
        number of steps per cooling cycle (default: 10)

    verbose : int
        0  : silent
        1 : print results to output
        2 : print some info every 100 iterations and plot results
        3 : print some info every iteration
    callback : callable
        function to be called every iteration of form :
        xopt = callback( xopt )

    simplex : ndarray
        the simplex has shape = (nx+1, nx); nx is the size of x
    values : ndarray
        the values of the function attained at the simplex points (nx+1).
    sum : ndarray
        sum over the corners of the simplex (nx)

    """
    #  *************************************************************************
    def __init__( self, func, xini, size=1, seed=4567, temp=0, limits=None,
                    maxiter=1000, reltol=0.0001, abstol=0.0001, cooling=0.95, steps=10,
                    verbose=0, callback=None ):
        """
        Create a new AnnealingAmoeba class to minimize the function

        Parameters
        ----------
        func : callable
            the function to be minimized
        xini : array_like
            initial values of the function
        size : float or array_like
            step size of the simplex
        seed : int
            for random number generator
        temp : float
            temperature of annealing (0 is no annealing)
        limits : None or list of 2 floats or list of 2 array_like
            None : no limits applied
            [lo,hi] : low and high limits for all values
            [la,ha] : low array and high array limits for the values
        maxiter : int
            max number of iterations
        reltol : float, None
            Relative tolerance. Program stops when ( |hi-lo| / (|hi|+|lo|) ) < reltol
        abstol : float, None
            Absolute tolerance. Program stops when |hi-lo| < abstol
            when abstol has a (float) value, reltol might be None.
        cooling : float
            cooling factor when annealing
        steps : int
            number of cycles in each cooling step.
        verbose : int
            0 : silent
            1 : print results to output
            2 : print some info every 100 iterations and plot results
            3 : print some info every iteration
        callback : callable
            is called each iteration as
            val = callback( val )
            where val is the minimizable array

        Raises
        ------
        ValueError
            1. When func is not callable
            2. When both tolerances are None
            3. When callback is not callable

        """
        super( AnnealingAmoeba, self ).__init__( )

        if callable( func ) :
            self.func = func
        else :
            raise ValueError( "func needs to be a callable function" )
        self.seed = seed
        self.rng = numpy.random.RandomState( self.seed )
        self.temp = temp
        nfit = Tools.length( xini )
        if Tools.length( size ) == 1 :
            size = [size] * nfit

        if limits is None :
            self.lolimits = None
            self.hilimits = None
        else :
            self.lolimits = limits[0] if Tools.length( limits[0] ) > 1 else [limits[0]]*nfit
            self.hilimits = limits[1] if Tools.length( limits[1] ) > 1 else [limits[1]]*nfit
        self.maxiter = maxiter
        if abstol is None and reltol is None :
            raise ValueError( "Both reltol and abstol are None." )
        self.abstol = abstol
        self.reltol = reltol
        if temp > 0 :
            self.cooling = cooling
            self.steps = steps
        self.verbose = verbose

        self.callback = callback
        if callback is not None and not callable( callback ) :
            raise ValueError( "callback needs to be a callable function (or None)" )

        # counters
        self.iter = 0
        self.ncalls = 0

        # initialize the simplex
        self.makeSimplex( xini, size )


    #  *************************************************************************
    def makeSimplex( self, xini, step ):
        """
        Make a simplex for the given set of parameters.

        Parameters  fitindex    list of parameters to fit

        """
        nfit = len( xini )

        i = 0
        for ir in xini :
            if self.hasLowLimits( i ) and ir <= self.lolimits[i] :
                lo = self.lolimits[i]
                if self.hasHighLimits( i ):
                    hi = self.hilimits[i]
                    xini[i] = 0.5 * ( hi + lo )
                    step[i] = 0.1 * ( hi - lo )
                else:
                    xini[i] = lo + 10
                    step[i] = 1
            if self.hasHighLimits( i ) and ir >= self.hilimits[i] :
                hi = self.hilimits[i]
                if self.hasLowLimits( i ):
                    lo = self.lolimits[i]
                    xini[i] = 0.5 * ( hi + lo )
                    step[i] = 0.1 * ( hi - lo )
                else:
                    xini[i] = hi - 10
                    step[i] = 1
            i += 1

        ndim = nfit + 1
        self.simplex = numpy.zeros( ( ndim, nfit ), dtype=float )
        self.values = numpy.zeros( ndim, dtype=float )
        self.xopt =  numpy.zeros( nfit, dtype=float )
        self.sum = numpy.zeros( nfit, dtype=float )

        for i in range( ndim ) :
            self.simplex[i,:] += xini
            if i < nfit :
                self.simplex[i,i] += step[i]
            trypar = self.stayInLimits( xini, self.simplex[i,:] )
            self.simplex[i,:] = trypar

        self.checkSimplex( self.simplex )
        self.setValues()

    def hasLowLimits( self, k ) :
        return self.lolimits is not None and self.hilimits[k] > -math.inf

    def hasHighLimits( self, k ) :
        return self.hilimits is not None and self.hilimits[k] < math.inf

    def stayInLimits( self, oldpar, trypar ) :
        if self.lolimits is None and self.hilimits is None :
            return trypar

        npar = self.simplex.shape[1]
        for k in range( npar ) :
            if self.lolimits[k] > trypar[k] :
                trypar[k] = ( oldpar[k] + self.lolimits[k] ) / 2
            elif trypar[k] > self.hilimits[k] :
                trypar[k] = ( oldpar[k] + self.hilimits[k] ) / 2
        return trypar

    def checkSimplex( self, simplex ):
        """
        Check for degeneracy: all points on same location.
        """
        dim = simplex.shape
        for i in range( dim[1] ) :
            same = True
            pre = simplex[0,i]
            same = all( sim == pre for sim in simplex[i,:] )

            if same:
                print( simplex[i,:] )
                raise ValueError( "Simplex is degenerate at index %d"%i )

    def setValues( self ):
        """
        Calculate the function values a simplex's corners

        """
        for i in range( self.simplex.shape[0] ):
            corner = self.simplex[i,:]
            cost = self.func( corner )
            if not numpy.isfinite( cost ) :
                corner += 0.01 * numpy.sum( self.simplex, 0 )
                cost = self.func( corner )

            self.values[i] = cost
            if i == 0 or self.values[i] < self.fopt:
                self.fopt = self.values[i]
                self.xopt = corner.copy()
        self.sum = numpy.sum( self.simplex, axis=0 )
        self.ncalls += self.simplex.shape[0]

# *************************************************************************
    def minimize( self ):
        """
        Converge the simplex.

        Returns
        -------
        ndarray : the optimal x values.

        Raises
        ------
        ConvergenceError when too many iterations are needed.
        """

        if self.verbose > 0 :
            print( "Iteration   step   ", ( "temp" if ( self.temp > 0 ) else "" ),
                   "  minimum    values" )
            numpy.set_printoptions( precision=3, suppress=True )

        maxiter = self.maxiter * ( 1 if self.temp == 0 else self.steps )
        while self.iter < maxiter :
#            print( self.iter, maxiter )
            trans = self.temperatureStep( )
            self.ncalls += trans

            if self.temp > 0 :
                self.temp *= self.cooling
            if trans == 0:
                return self.xopt

        raise ConvergenceError( "AnnealingAmoeba: Too many iterations: %d"%self.iter )

    def temperatureStep( self ):
        """
        Perform simplex moves in the right direction.

        Returns
        -------
        int : number of transforms.

        """
        ALPHA = 1.0
        BETA = 0.5
        GAMMA = 2.0
        DELTA = 10.

        (ndim,nfit) = self.simplex.shape
        maxiter = self.iter + ( self.maxiter if ( self.temp == 0 ) else self.steps * nfit )
        beta = BETA
        trans = 0

        self.sum = numpy.sum( self.simplex, axis=0 )
        move = "start"
        while self.iter < maxiter :
            ilo = 0
            ihi = 1
            ylo = self.values[0] + self.logRanTemp()
            ynhi = ylo
            yhi = self.values[1] + self.logRanTemp()

            if ylo > yhi:
                ihi = 0
                ilo = 1
                ynhi = yhi
                yhi = ylo
                ylo = ynhi
            for i in range( 2, ndim ) :
                yt = self.values[i] + self.logRanTemp()
                if yt <= ylo:
                    ilo = i
                    ylo = yt
                if yt > yhi:
                    ynhi = yhi
                    ihi = i
                    yhi = yt
                elif yt > ynhi:
                    ynhi = yt

#            for i in range( ndim ) :
#                print( self.simplex[i,:], self.values[i] )
#            print( ilo, ihi, ylo, ynhi, yhi )

            rtol = abs( yhi - ylo ) / max( abs( yhi ) + abs( ylo ), 1e-20 )
            stops = ( ( self.abstol is None or abs( yhi - ylo ) < self.abstol ) and
                      ( self.reltol is None or rtol < self.reltol ) )

#            print( rtol, self.reltol, abs( yhi - ylo ), self.abstol, stops, trans, self.fopt, ylo )

            if stops :
                # put best values and simplex in first position of the simplex
                if ilo > 0 :
                    swap = self.values[0]
                    self.values[0] = self.values[ilo]
                    self.values[ilo] = swap

                    swap = self.simplex[0,:]
                    self.simplex[0,:] = self.simplex[ilo,:]
                    self.simplex[ilo,:] = swap

                # check if best ever value is better than best in simplex;
                #     if so replace best and continue
                tol = self.abstol if self.abstol is not None else self.reltol
                if abs( self.fopt - ylo ) > tol :
                    self.simplex[ilo,:] = self.xopt[:]
                    self.values[ilo] = self.fopt

                    move = "replace"
                    if self.iter < maxiter:
                        continue

                if self.iter == 0 :             ## it does not start. Inflate the simplex
                    move = "expand"
                    ylo = self.inflateSimplex( ilo, DELTA )
                    trans += nfit
                    continue
                break

            trans += 2
            factor = -ALPHA
            while True:
                ytry = self.trialStep( ihi, yhi, factor )
                factor = self.randomRange( -ALPHA )
                if not math.isnan( ytry ) : break
            move = "reflect"					# reflect worst over the others

            if ytry < ylo:                      # when succesfull move further
                factor = GAMMA
                while True:
                    ytry = self.trialStep( ihi, yhi, factor )
                    factor = self.randomRange( GAMMA )
                    if not math.isnan( ytry ) : break
                move = "extrapolate"			# reflect twice as far

            elif ytry >= ynhi:                  # not better than next hi : contract
                ysave = yhi
                factor = beta
                while True:
                    ytry = self.trialStep( ihi, yhi, factor )
                    factor = self.randomRange( beta )
                    if not math.isnan( ytry ) : break
                move = "contract"				# contract in direction of others

                if ytry >= ysave :              # not better that saved one : shrink
                    factor = beta
                    while True:
                        ytry = self.inflateSimplex( ilo, factor )
                        factor = self.randomRange( beta )
                        if not math.isnan( ytry ) : break
                    trans += nfit
                    move = "shrink" 			# shrink simplex on best point
            else:
                trans -= 1

            if self.callback is not None :
                self.simplex[ihi,:] = self.callback( self.simplex[ihi,:] )

            self.iter += 1
            self.doVerbose( move, ytry, self.simplex[ihi,:], force=(self.verbose>=3) )

        self.doVerbose( move, self.values[0], self.simplex[0,:], force=True )
        return trans

    def doVerbose( self, name, chisq, par, force=False ):
        if self.verbose > 1 and ( self.iter % 100 == 0 or force ):
            mx = 5 if self.verbose < 4 else None if self.verbose == 4 else self.verbose
            print( "%6d    %-8.8s "%(self.iter,name),
                    ( "%6.1f"%(self.temp ) if ( self.temp > 0 ) else "" ),
                    " %8.1f  "%chisq, fmt( par, max=mx ) )

    def randomRange( self, factor ):
        return factor * ( 0.9 + 0.2 * self.rng.rand( ) )

    def inflateSimplex( self, ilo, factor ):
        """
        Inflate/deflate simplex around the (lowest) point (ilo).

        inflate if factor > 1
        deflate if factor < 1
        mirror  if factor < 0

        Parameters
        ----------
        ilo : int
            lowest point in the simplex
        factor : float
            inflation factor

        """
        emf = 1 - factor
        (ndim,nfit) = self.simplex.shape
        milo = [k for k in range( ilo )] + [k for k in range( ilo+1, ndim )]
        for i in milo :
            inpar = self.simplex[i,:]
            self.simplex[i,:] = factor * inpar + emf * self.simplex[ilo,:]

            self.simplex[i,:] = self.stayInLimits( inpar, self.simplex[i,:] )

        ylo = self.values[ilo]
        for i in milo :
            p = self.simplex[i,:]
            self.values[i] = self.func( p )
            if self.values[i] < ylo:
                ylo = self.values[i]
                if self.values[i] < self.fopt:
                    self.fopt = ylo
                    self.xopt = p

        self.sum = numpy.sum( self.simplex, axis=0 )

        return ylo

    def trialStep( self, ihi, yhi, factor ):
        """
        Do a trial step to improve the worst (highest) point.

        Parameters
        ----------
        ihi : int
            index of the high point
        yhi :  int
            value at the high point
        factor : int
            step size
        """
        (ndim,nfit) = self.simplex.shape

        fac1 = ( 1 - factor ) / nfit
        fac2 = fac1 - factor
        partry = self.sum * fac1 - self.simplex[ihi,:] * fac2
        inpar = self.simplex[ihi,:]
        partry = self.stayInLimits( inpar, partry )

        ytry = self.func( partry )

        if ytry < self.fopt:
            self.fopt = ytry
            self.xopt = partry.copy()

        yflu = ytry - self.logRanTemp( )

        if yflu < yhi:
            self.values[ihi] = ytry
            self.sum += partry - self.simplex[ihi,:]
            self.simplex[ihi,:] = partry

        return yflu

    def logRanTemp( self ):
        EPSILON = 1.0e-30
        return -self.temp * math.log( self.rng.rand( ) + EPSILON )


    def __str__( self ) :
        return "AnnealingAmoeba with temp = %f"%self.temp


