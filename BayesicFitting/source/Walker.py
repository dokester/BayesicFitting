import numpy as numpy
import math
from . import Tools
from .Formatter import formatter as fmt

from .Problem import Problem
from .Sample import Sample

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

class Walker( object ):
    """
    Walker is member of the cloud of points used in NestedSampler.

    Attributes
    ----------
    id : int
        identification number
    parent : int
        id of the parent (-1 for Adam/Eve)
    start : int
        iteration in which the walker is constructed
    problem : Problem
        the problem being addressed
    logL : float
        log Likelihood = log Prob( data | params )
    allpars : array_like
        list of parameters and hyperparameters
    fitIndex : array_like
        list of (super)parameters to be fitted.
    parameters : array_like (read only)
        parameters (of the model)
    hypars : array_like (read only)
        list of hyper parameters (of the error distribution)

    Author       Do Kester

    """

    def __init__( self, wid, problem, allpars, fitIndex, parent=-1, start=0, copy=None ):
        """
        Constructor.

        Either errdis or copy is obligatory.

        Parameters
        ----------
        wid : int
            id of the walker
        problem : Problem
            the problem being used. Parameters are copied from its model.
        allpars : array_like
            array of parameters and hyperparameters
        fitIndex : None or array_like
            indices of allpars to be fitted
            None is all
        parent : int
            id of the parent (-1 for Adam/Eve)
        start : int
            iteration in which the walker is constructed
        copy : Walker
            the walker to be copied

        """
        self.id = wid
        self.allpars = allpars.copy()
        self.fitIndex = fitIndex

        if copy is None :
            self.start = start
            self.parent = parent
            self.problem = problem
            self.logL = 0.0
        else :
            self.start = copy.start
            self.parent = copy.parent
            self.problem = problem.copy()
            self.logL = copy.logL

    def copy( self ):
        """
        Copy.

        """
        return Walker( self.id, self.problem, self.allpars, self.fitIndex, copy=self )

    def toSample( self, logW ) :
        """
        Return the contents of the Walker as a Sample.
        """

        np = self.problem.npars
        nm = self.problem.model.npars if self.problem.model else np

        param = self.allpars[:nm]
        sample = Sample( self.id, self.parent, self.start, self.problem.model,
                         parameters=param, fitIndex=self.fitIndex )

        if len( self.allpars ) > np :
            sample.hyper = self.allpars[np:]
        if np > nm :
            sample.nuisance = self.allpars[nm:np]

        sample.logL = self.logL
        sample.logW = logW
        return sample

    def __getattr__( self, name ) :
        """
        Return the value of one of `parameters`, `scale`,

        """
        if name == "parameters" :
            np = self.problem.model.npars
            return self.allpars[:np]
        elif name == "hypars" :
            np = self.problem.model.npars
            if len( self.allpars ) > np :
                return self.allpars[np:]
            else :
                return None
        else :
            raise AttributeError( "Unknown attribute " + name )

        return None

    def __setattr__( self, name, value ) :
        """
        Set attributes.
        """
        if name == "allpars" or name == "fitIndex":
            object.__setattr__( self, name, value )
            return

        key1 = {"id" : int, "parent" : int, "start" : int, "problem": Problem,
                "logL" : float }
        if Tools.setSingleAttributes( self, name, value, key1 ) :
            pass
        else :
            raise AttributeError(
                "Object has no attribute " + name + " of type " + str( value.__class__ ) )

    def __str__( self ) :
        return str( "Walker: %3d" % self.id )


    def check( self, nhyp=0 ) :
        """
        Perform some sanity checks.
        """
        np = self.problem.npars

        if not len( self.allpars ) == ( np + nhyp ) :
            Tools.printclass( self )
            Tools.printclass( self.problem )
            raise ValueError( "Walker %d inconsistent parameter length : %d is not ( %d + %d )" %
                ( self.id, len( self.allpars ), np, nhyp ) )

#        if not len( self.allpars ) == len( self.fitIndex ) :
#            raise ValueError( "Walker parameter length = %d fitIndex ( %d )" %
#                ( len( self.allpars ), len( self.fitIndex ) ) )

        ## Does this (all hypars > 0) always have to be true ???
        if nhyp > 0 and self.allpars[-nhyp] <= 0 :
            raise ValueError( "Sample has non-positive hyperparameter: %f" % self.allpars[-nhyp] )
