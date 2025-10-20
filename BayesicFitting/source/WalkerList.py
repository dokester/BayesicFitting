import numpy as numpy
from .Tools import setAttribute as setatt
from .Formatter import formatter as fmt
from .Walker import Walker

__author__ = "Do Kester"
__year__ = 2025
__license__ = "GPL3"
__version__ = "3.2.5"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Perpetual Beta"

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
#  *    2008 - 2014 Do Kester, SRON (Java code)
#  *    2017 - 2025 Do Kester


class WalkerList( list ):
    """
    WalkerList is a list of Walker.

    It is the working ensemble of NestedSampler.


    Attributes
    ----------
    logZ : float (read-only)
        Natural log of evidence
    info : float (read-only)
        The information H. The compression factor ( the ratio of the prior space
        available to the model parameters over the posterior space ) is equal to the exp( H ).
    iteration : int
        Present iteration number.

    Author       Do Kester

    """
    def __init__( self, problem=None, ensemble=0, allpars=None, fitIndex=None, 
                  walker=None,  walkerlist=None ):
        """
        Constructor.

        To be valid it needs either problem/allpars/fitindex or walker or walkerlist

        Parameters
        ----------
        problem : Problem or None
            to construct a walker to be added.
        ensemble : int
            number of walkers
        allpars : array_like
            parameters of the problem
        fitIndex : array of int
            list of parameters to be fitted.
        walker : Walker or None
            walker to be added.
        walkerlist : Walkerlist or None
            walkerlist to be incorporated.
        """
        if walkerlist is not None :
            super( WalkerList, self ).__init__( walkerlist )
            self._count = len( walkerlist )
            return

        super( WalkerList, self ).__init__( )
        self._count = 0

        if problem is not None :
            walker = Walker( 0, problem, allpars, fitIndex )

        self.addWalkers( walker, ensemble )


    def addWalkers( self, walker, ensemble ):
        for i in range( ensemble ) :
            wlkr = walker.copy()
            if wlkr.problem.model and wlkr.problem.model.isDynamic() :
                wlkr.fitIndex = walker.fitIndex.copy()
            wlkr.id = self._count
            self.append( wlkr )
            self._count += 1

    # ===========================================================================
    def setWalker( self, walker, index ):
        """
        replace/append a Walker to this list

        Parameters
        ----------
        walker : Walker
            the list to take to copy from
        index : int
            the index at which to set
        """

        if index < len( self ) :
            self[index] = walker
        else :
            walker.id = self._count
            self._count += 1
            self.append( walker )

    def copy( self, src, des, wlist=None, start=0 ):
        """
        Copy one item of the list onto another.

        Parameters
        ----------
        src : int
            the source item
        des : int
            the destination item
        wlist : WalkerList or None
            Copy from this WalkerList (None == self)
        start : int
            iteration where this walker was created
        """
        if wlist is None :
            wlist = self

        id = self[des].id
        self[des] = wlist[src].copy()
        setatt( self[des], "id", id )
        setatt( self[des], "parent", src )
        setatt( self[des], "start", start )
        setatt( self[des], "step", 0 )


    def logPlus( self, x, y ):
        """
        Return the log of sum.
        """
        return numpy.logaddexp( x, y )

    def firstIndex( self, lowL ) :
        """
        Return  index of the first walker with walker.logL > lowL, 
                None if list is empty
                len  if no item applies 

        Parameters
        ----------
        lowL : float
            low Likelihood
        """
        return next( ( k for k,w in enumerate( self ) if w.logL > lowL ), 
                    None if len( self ) == 0 else len( self)  )


    def insertWalker( self, walker ):
        """
        Insert walker to this list keeping it sorted in logL

        Parameters
        ----------
        walker : Walker
            the list to take to copy from
        """
        klow = self.firstIndex( walker.logL )
        if klow is None :
            self.setWalker( walker, 0 )
            return self

        cnt = self._count

        wl = WalkerList( walkerlist=[walker] )

        if len( self[klow:] ) > 0 :
            wl = wl + WalkerList( walkerlist=self[klow:] )

        if len( self[:klow] ) > 0 :
            self = WalkerList( walkerlist=self[:klow] ) + wl
        else :
            self = wl

        self = WalkerList( walkerlist=self )
        self._count = cnt + 1

        return self

    def printwlogl( self, wlkrs, klow ) :
        print( fmt( klow ), fmt( len( wlkrs ) ) )
        for k,w in enumerate( wlkrs ) :
            print( fmt( w.logL ), end="" )
            if (k % 10 ) == 9 : print()
        print()


    def cropOnLow( self, lowL ) :
        """
        Return WalkerList with all LogL > lowL

        Precondition: self is ordered on logL

        Parameters
        ----------
        lowL : float
            low Likelihood
        """
        cnt = self._count
        self = WalkerList( walkerlist=self[self.firstIndex( lowL ):] )
        self._count = cnt
        return self


    def getLogL( self, walker=None ) :
        """
        Return the logL of the/all walker

        Parameters
        ----------
        walker : None or Walker
            None return value for all walkers
            get the logL from
        """
        if walker is None :
            return self.getLogLikelihoodEvolution()
        return walker.logL


    def allPars( self, npars=None ):
        """
        Return a 2d array of all parameters.

        In case of dynamic models the number of parameters may vary.
        They are zero-padded. Use `getNumberOfParametersEvolution`
        to get the actual number.

        Parameters
        ----------
        kpar : int or tuple of ints
            the parameter to be selected. Default: all

        """
        if npars is None :
            pe = numpy.zeros( ( len( self ), self[0].nap ), dtype=float )
            for k, walker in enumerate( self ) :
                pe[k,:] = walker.allpars
            return pe
        
        indx = [k for k,w in enumerate( self ) if w.nap == npars]
        pe = numpy.zeros( ( len( indx ), npars ), dtype=float )
        for k, i in enumerate( indx ) :
            pe[k,:] = self[i].allpars

        return pe

    def getParameterEvolution( self, kpar=None ):
        """
        Return the evolution of one or all parameters.

        In case of dynamic models the number of parameters may vary.
        They are zero-padded. Use `getNumberOfParametersEvolution`
        to get the actual number.

        Parameters
        ----------
        kpar : int or tuple of ints
            the parameter to be selected. Default: all

        """
        pe = []
        for walker in self :
            pe += [walker.parameters]
        if kpar is None :
            return numpy.asarray( pe )
        else :
            return numpy.asarray( pe )[:,kpar]

    def getScaleEvolution( self ):
        """ Return the evolution of the scale.  """
        pe = [walker.hypars for walker in self]
        return numpy.asarray( pe )

    def getLogLikelihoodEvolution( self ):
        """ Return the evolution of the log( Likelihood ).  """
        pe = [walker.logL for walker in self]
        return numpy.asarray( pe )

    def getLowLogL( self ):
        """
        Return the lowest value of logL in the walkerlist, plus its index.
        """
        low = self[0].logL
        klo = 0
        k = 0
        for walker in self :
            if walker.logL < low :
                klo = k
                low = walker.logL
            k += 1
        return ( low, klo )

    def __str__( self ) :
        return str( "Walkerlist with %3d walkers" % len( self ))


