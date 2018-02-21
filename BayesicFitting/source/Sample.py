import numpy as numpy
import math
import Tools
from Model import Model

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
#  *    2008 - 2014 Do Kester, SRON (Java code)
#  *    2017        Do Kester

class Sample( object ):
    """
    Sample is weighted random draw from a Posterior distribution as
    provided by a Sampler

    Each Sample maintains 5 attributes

    Attributes
    ----------
    id : int
        identification number
    parent : int
        id of the parent (-1 for Adam/Eve)
    model : Model
        the model being used
    logL : float
        log Likelihood = log Prob( data | params )
    logW : float
        log Weights of the likelihood.
            SUM( log( W * L ) = logZ (TBC)
            log( SUM( W * L ) = logZ (evidence)
    allpars : array_like
        list of parameters and hyperparameters
    fitIndex : array_like or None
        list of (super)parameters to be fitted.
    parameters : array_like (read only)
        parameters (of the model)
    hyperpars : array_like (read only)
        list of hyper parameters (of the error distribution)


    Author       Do Kester

    """

    def __init__( self, id, parent, model, errdis=None, fitIndex=None, copy=None ):
        """
        Constructor.

        Either errdis or copy is obligatory.

        Parameters
        ----------
        id : int
            id of the sample
        parent : int
            id of the parent (-1 for Adam/Eve)
        model : Model
            the model being used. Parameters are copied from this model.
        errdis : ErrorDistribution
            to get info about super parameters
        fitIndex : array_like
            list of indices in allpars that need fitting
        copy : Sample
            the sample to be copied

        """
        self.id = id
        self.parent = parent
        self.model = model
        if copy is None :
            self.allpars = numpy.append( model.parameters, errdis.hypar )
            if fitIndex is not None :
                self.fitIndex = fitIndex                # no copy.
            else :
                self.fitIndex = numpy.arange( model.npchain )
                indx = model.npchain
                for s in errdis.hyperpar :
                    if not s.isFixed :
                        self.fitIndex = numpy.append( self.fitIndex, [indx] )
                    indx += 1
            self.logL = 0.0
            self.logW = 0.0
        else :
            self.allpars = copy.allpars.copy()
            self.fitIndex = copy.fitIndex             # no copy; read only
            self.logL = copy.logL
            self.logW = copy.logW

    def copy( self ):
        """
        Copy.

        The copy points to the same instance of model.
        """
        return Sample( self.id, self.parent, self.model, copy=self )

    def __getattr__( self, name ) :
        """
        Return the value of one of `parameters`, `scale`,

        """
        if name == "weight" :
            return math.exp( self.logW )
        elif name == "parameters" :
            return self.allpars[:self.model.npchain]
        elif name == "hypars" :
            if len( self.allpars ) > self.model.npchain :
                return self.allpars[self.model.npchain:]
            else :
                return None
        else :
            raise AttributeError( "Unknown attribute " + name )

        return None

    def __setattr__( self, name, value ) :
        """
        Set attributes.
        """

        key1 = {"id" : int, "parent" : int, "model": Model, "logL" : float, "logW" : float }
        key2 = {"allpars" : float, "fitIndex" : int }
        if ( Tools.setSingleAttributes( self, name, value, key1 ) or
             Tools.setListOfAttributes( self, name, value, key2 ) ) :
            pass
        else :
            raise AttributeError(
                "Object has no attribute " + name + " of type " + str( value.__class__ ) )

    def __str__( self ) :
        return str( "Sample: %3d parent: %3d model: %s logL: %10.2f logW: %10.2f"%
                    ( self.id, self.parent, self.model.shortName(), self.logL, self.logW ) )


