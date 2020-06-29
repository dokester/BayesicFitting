import numpy as numpy
from . import Tools
from .Tools import setAttribute as setatt
from .SplinesModel import SplinesModel
from .BasicSplinesModel import BasicSplinesModel
from .Dynamic import Dynamic
from .Modifiable import Modifiable

from .Formatter import formatter as fmt

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
#  *    2020 - 2020 Do Kester

class SplinesDynamicModel( Modifiable, Dynamic, BasicSplinesModel ):
    """
    BasicSplinesModel that is modifiable (knot locations) and dynamic (in number
    of knots)


    Examples
    --------
    >>> knots = numpy.arange( 17, dtype=float ) * 10    # make equidistant knots from 0 to 160
    >>> csm = SplinesModel( knots=knots, order=2 )
    >>> print csm.getNumberOfParameters( )
    18
    # or alternatively:
    >>> csm = SplinesModel( nrknots=17, order=2, min=0, max=160 )    # automatic layout of knots
    >>> print csm.getNumberOfParameters( )
    18
    # or alternatively:
    >>> npt = 161                                               # to include both 0 and 160.
    >>> x = numpy.arange( npt, dtype=float )                    # x-values
    >>> csm = SplinesModel( nrknots=17, order=2, xrange=x )     # automatic layout of knots
    >>> print csm.getNumberOfParameters( )
    18

    Attributes
    ----------
    minKnots : int
        minimum number of knots
    maxDegree : int or None
        maximum number of knots

    Attributes from Modifiable
    --------------------------
        modifiable

    Attributes from Dynamic
    -----------------------
        dynamic, ncomp (=degree+1), deltaNpar, minComp (=minDegree+1), maxComp (=maxDegree+1), growPrior

    Attributes from SplinesModel
    ----------------------------
        knots, order

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
    def __init__( self, modifiable=True, dynamic=True, growPrior=None, minKnots=2, maxKnots=None,
                        minDistance=0.01, copy=None, **kwargs ):
        """
        Splines on a given set of knots and a given order.

        The number of parameters is ( length( knots ) + order - 1 )

        Parameters
        ----------
        modifiable : bool
            if True allow changement of the knot locations
        dynamic : bool
            if True allow growth and shrinkage of number of knots
        minKnots : int
            minimum number of knots (def=2)
        maxKnots : None or int
            maximum number of Knots
        minDistance : float
            minimum distance between knots, provided as fraction of average knot distance.
            default is ( 0.01 * ( knots[-1] - knots[0] ) / nrknots )
        growPrior : None or Prior
            governing the birth and death.
            ExponentialPrior (scale=2) if  maxDegree is None else UniformPrior
        copy : PolynomialDynamicModel
            model to copy

        Parameters for SplinesModel
        ---------------------------
        knots, order, nrknots, min, max, xrange

        Raises
        ------
        ValueError if not minKnots <= nrknots <= maxKnots

        """
        Modifiable.__init__( self, modifiable=modifiable )
        Dynamic.__init__( self, dynamic=dynamic )

        BasicSplinesModel.__init__( self, copy=copy, **kwargs )

        nrknots = len( self.knots )
        if nrknots < minKnots or ( maxKnots is not None and nrknots > maxKnots ) :
            raise ValueError( "nrknots outside range of [min..max] range" )

        self.deltaNpar = 1

        if copy is None :
            minDistance *= ( self.knots[-1] - self.knots[0] ) / nrknots
            setatt( self, "minDistance", minDistance )
            self.setGrowPrior( growPrior=growPrior, min=minKnots, max=maxKnots,
                           name="Knots" )
        else :
            setatt( self, "knots", copy.knots.copy() )
            setatt( self, "minKnots", copy.minKnots )
            setatt( self, "maxKnots", copy.maxKnots )
            setatt( self, "minDistance", copy.minDistance )
            setatt( self, "growPrior", copy.growPrior.copy() )


    def copy( self ):
        return SplinesDynamicModel( knots=self.knots, modifiable=self.modifiable,
                                    dynamic=self.dynamic, copy=self )

    def __setattr__( self, name, value ) :
        if self.setDynamicAttribute( name, value ) :
            return
        else :
            super( ).__setattr__( name, value )

    def __getattr__( self, name ) :
        """
        Return value belonging to attribute with name.

        Parameters
        ----------
        name : string
            name of the attribute
        """
        if name == 'ncomp' :
            return len( self.knots )
        if name == 'minComp' :
            return self.minKnots
        if name == 'maxComp' :
            return self.maxKnots

        return super( ).__getattr__( name )

    def baseName( self ):
        """ Returns a string representation of the model. """
        name = "Dyn" if self.dynamic else ""
        name += "Mod" if self.modifiable else ""

        return name + super().baseName()

    def changeNComp( self, dn ) :
        pass                        ## it is the length of knots

    def grow( self, offset=0, rng=None, force=False, **kwargs ):
        """
        Increase the degree by one upto maxComp ( if present ).

        Parameters
        ----------
        offset : int
            index where the params of the Dynamic model start
        rng : random number generator (obligatory)
            to generate a new parameter.
        force : bool
            dont check maxKnots

        Return
        ------
        bool :  succes

        """
        if not force and self.maxKnots is not None and self.knots.size >= self.maxKnots :
            return False

#        print( "SDg p0 ", fmt( self._head.parameters, max=None ) )

        nrknots = len( self.knots )
        npars = self.npbase
        while True :
            newkn = rng.rand() * ( self.knots[-1] - self.knots[0] ) + self.knots[0]
            k = 1
            while self.knots[k] < newkn : k += 1
            if ( newkn - self.knots[k-1] > self.minDistance and
                 self.knots[k] - newkn   > self.minDistance ) :
                break

        self.knots = numpy.insert( self.knots, k, newkn )   ## new set of knots

        location = ( npars - nrknots ) // 2 + k + 1

        dnp = self.deltaNpar
        self.alterParameterSize( dnp, offset, location=location )

        try :
            self.basis = self.makeBasis()
        except :
            print( "Grow: Could not make basis from", fmt( self.knots,max=None ) )
            return False

        head = self._head
        mdlpar = head.parameters
        kl = location + offset

#        print( "SDg p1 ", fmt( mdlpar, max=None ) )

#        print( "grow    ", nrknots, location, offset, k, kl, newkn )

        mdlpar[kl-1] *= 0.7
        value = mdlpar[kl-1]
        mdlpar = self.alterParameters( mdlpar, location, dnp, offset, value=value )

        setatt( self._head, "parameters", mdlpar )

        self.alterParameterNames( 1 )

        self.changeNComp( 1 )

        return True


    def shrink( self, offset=0, rng=None, **kwargs ):
        """
        Decrease the degree by one downto minComp ( default 1 ).

        Parameters
        ----------
        offset : int
            index where the params of the Dynamic model start
        rng : random number generator
            to generate a new parameter (obligatory)

        Return
        ------
        bool : succes

        """
        nrknots = len( self.knots )
        npars = self.npbase
        if nrknots <= self.minKnots :
            return False

#        print( "SDs p0 ", fmt( self._head.parameters, max=None ) )

        k = rng.randint( nrknots - 2 ) + 1              ## avoid endpoints
        dis = self.knots[k+1] - self.knots[k-1]
        r1 = ( self.knots[k] - self.knots[k-1] ) / dis
        r2 = ( self.knots[k+1] - self.knots[k] ) / dis

        self.knots = numpy.delete( self.knots, k )      ## new set of knots

        location = ( npars - nrknots ) // 2 + k + 1
        dnp = - self.deltaNpar
        kl = offset + location - 1
        head = self._head
        mdlpar = head.parameters

        ## new value is the weighted average of the joined parameters
        value = 1.4 * ( mdlpar[kl] * r1 + mdlpar[kl+1] * r2 )

        if self.getPrior( kl ).isOutOfLimits( value ) :
            value = ( self.getPrior( kl ).stayInLimits( value ) + mdlpar[kl] + mdlpar[kl+1] ) / 3

        if self.getPrior( kl ).isOutOfLimits( value ) :
            print( "New shrink value out of limit" )
            print( "Knots ", k, fmt( r1 ), fmt( r2 ), fmt( dis ), fmt( self.knots, max=None ) )
            print( "Pars  ", fmt( mdlpar, max=None ) )
            print( "Old   ", kl, fmt( mdlpar[kl:kl+2] ), "  New  ", fmt( value ) )
            return False

#        print( "SD  p1 ", npars, nrknots, k, location, kl )

        self.alterParameterSize( dnp, offset, location=location )
        try :
            self.basis = self.makeBasis()
        except :
            print( "Shrk: Could not make basis from", fmt( self.knots,max=None ) )
            return False

        mdlpar = self.alterParameters( mdlpar, location, dnp, offset )
        mdlpar[kl] = value

#        print( "SD  p2 ", fmt( mdlpar, max=None ), kl, value )

        setatt( self._head, "parameters", mdlpar )

        self.alterParameterNames( dnp )

        self.changeNComp( -1 )

        return True

    def vary( self, rng=None, location=None ) :

        nrknots = len( self.knots )
        if nrknots <= 2 or location == 0 or location == nrknots :
            return False

        kk = location if location is not None else rng.randint( nrknots - 2 ) + 1

        newkn = self.knots[kk]

        while True :
            rn = ( rng.rand() + rng.rand() ) - 1
            newkn += rn * ( ( newkn - self.knots[kk-1] ) if rn < 0 else
                            ( self.knots[kk+1] - newkn ) )

            ## check minimum distance from neighbouring knots
            if ( newkn - self.knots[kk-1] > self.minDistance and
                 self.knots[kk+1] - newkn > self.minDistance ) :
                break

#        print( "SDM   ", fmt( self.knots, max=None ), kk, newkn )

        self.knots[kk] = newkn
        try :
            self.basis = self.makeBasis()
        except :
            print( "Vary: Could not make basis from", fmt( self.knots,max=None ) )
            raise
            return False

        return True

    def varyAlt( self, offset=0, rng=None, **kwargs ) :
        """
        Vary the structure of a Modifiable Model


        Parameters
        ----------
        offset : int
            index where the params of the Modifiable model start
        rng : RNG
            random number generator
        kwargs : keyword arguments
            for specific implementations
        """
        suc = self.grow( offset=offset, rng=rng, force=True )
        suc = suc and self.shrink( offset=offset, rng=rng )
        return suc


