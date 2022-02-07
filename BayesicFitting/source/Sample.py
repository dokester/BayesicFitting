import numpy as numpy
import math
from . import Tools
from .Formatter import formatter as fmt

from .Model import Model
from .Tools import setAttribute as setatt

__author__ = "Do Kester"
__year__ = 2020
__license__ = "GPL3"
__version__ = "2.5.3"
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
        log Weights of the log of the weight of the sample.
        The weight is the relative contribution to the evidence integral.
        logW = logL + log( width )
        The logZ, the evidence, equals the log of the sum of the contributions.
        logZ = log( sum( exp( logW ) ) )
    parameters : array_like
        parameters (of the model)
    nuisance : array_like (optional)
        nuisance parameters (of the problem)
    hyper : array_like (optional)
        list of hyper parameters (of the error distribution)
    fitIndex : array_like or None
        list of allpars to be fitted.
    allpars : array_like (read only)
        list of parameters, nuisance parameters and hyperparameters

    Author       Do Kester

    """

    def __init__( self, id, parent, start, model, parameters=None, fitIndex=None, copy=None ):
        """
        Constructor.

        Parameters
        ----------
        id : int
            id of the sample
        parent : int
            id of the parent (-1 for Adam/Eve)
        start : int
            iteration in which the walker was constructed
        model : Model
            the model being used. Parameters are copied from this model.
        parameters : array_like
            list of model parameters
        fitIndex : array_like
            list of indices in allpars that need fitting
        copy : Sample
            the sample to be copied

        """
        self.id = id
        self.parent = parent
        self.start = start

        if copy is None :
            self.model = model
            self.parameters = parameters if parameters is not None else model.parameters
#            self.fitIndex = fitIndex if fitIndex is not None else numpy.arange( model.npars )
            self.fitIndex = fitIndex

            self.logL = 0.0
            self.logW = 0.0
        else :
            self.model = None if copy.model is None else copy.model.copy()
            self.fitIndex = None if copy.fitIndex is None else copy.fitIndex.copy()
#            self.model = copy.model.copy()
#            self.fitIndex = copy.fitIndex.copy()
            self.parameters = copy.parameters.copy()
            if hasattr( copy, "nuisance" ) : self.nuisance = copy.nuisance.copy()
            if hasattr( copy, "hyper" ) : self.hyper = copy.hyper.copy()
            self.logL = copy.logL
            self.logW = copy.logW

    def copy( self ):
        """
        Copy.

        """
        return Sample( self.id, self.parent, self.start, self.model, copy=self )

    def __getattr__( self, name ) :
        """
        Return the value of one of `parameters`, `scale`,

        """
        if name == "weight" :
            return math.exp( self.logW )
        elif name == "allpars" :
            allpars = self.parameters.copy()
            if hasattr( self, "nuisance" ) :
                allpars = numpy.append( allpars, self.nuisance )
            if hasattr( self, "hyper" ) :
                allpars = numpy.append( allpars, self.hyper )
            return allpars
        elif name == "hypars" :
            return self.hyper
        else :
            raise AttributeError( "Unknown attribute " + name )

        return None

    def __setattr__( self, name, value ) :
        """
        Set attributes.
        """
        if name == "parameters" :
            object.__setattr__( self, name, value )
            return

        key0 = [ "model", "fitIndex" ]
        key1 = {"id" : int, "parent" : int, "start" : int, "model": Model,
                "logL" : float, "logW" : float }
        key2 = {"fitIndex" : int, "nuisance" : float, "hyper" : float }
        if ( Tools.setNoneAttributes( self, name, value, key0 ) or
             Tools.setSingleAttributes( self, name, value, key1 ) or
             Tools.setListOfAttributes( self, name, value, key2 ) ) :
            pass
        else :
            raise AttributeError(
                "Object has no attribute " + name + " of type " + str( value.__class__ ) )

    def __str__( self ) :
        return str( "Sample: %3d parent: %3d model: %s logL: %10.2f logW: %10.2f"%
                    ( self.id, self.parent, self.model.shortName(), self.logL, self.logW ) )

    """
    def check( self, nhyp=0 ) :
#        print( len( self.allpars ), self.model.npchain, nhyp )
        if not len( self.allpars ) == ( self.model.npchain + nhyp ) :
            raise ValueError( "Sample inconsistent parameter length : %d is not ( %d + %d )" %
                ( len( self.allpars ), self.model.npchain, nhyp ) )
        if nhyp > 0 and self.allpars[-nhyp] <= 0 :
            raise ValueError( "Sample has non-positive hyperparameter: %f" % self.allpars[-nhyp] )
    """
