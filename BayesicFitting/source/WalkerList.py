import numpy as numpy
from astropy import units
import math
from . import Tools
from .Walker import Walker

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
__version__ = "2.6.0"
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
#  *    2017 - 2020 Do Kester


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
    def __init__( self, problem, nwalkers, allpars, fitIndex ):
        """
        Constructor.

        Parameters
        ----------
        nwalkers : int
            number of walkerss created.
        problem : Problem
            to be used in the walkerss
        allpars : array_like
            parameters and hyperparams of the problem
        fitIndex : array_like
            indices of allpars to be fitted

        """
        super( WalkerList, self ).__init__( )
        self._count = 0
        self.iteration = 0
        self.logZ = 0.0
        self.info = 0.0
        allpars = numpy.asarray( allpars )
        self.addWalkers( problem, nwalkers, allpars, fitIndex )


    def addWalkers( self, problem, nWalkers, allpars, fitIndex ):
        for i in range( nWalkers ) :
            if problem.model and problem.model.isDynamic() :
                problem = problem.copy()
                fitIndex = fitIndex.copy()
            walker = Walker( self._count, problem, allpars, fitIndex )
            self.append( walker )
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
#        print( "setWalker  ", id( self ), len( self ), walker.id, index )

        if index < len( self ) :
            self[index] = walker

        else :
            walker.id = self._count
            self._count += 1
            self.append( walker )

    def copy( self, src, des ):
        """
        Copy one item of the list onto another.

        Parameters
        ----------
        src : int
            the source item
        des : int
            the destination item

        """
        id = self[des].id
        self[des] = self[src].copy()
        self[des].id = id


    def logPlus( self, x, y ):
        """
        Return the log of sum.
        """
        return numpy.logaddexp( x, y )


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


