import numpy as numpy
from astropy import units
import math
import Tools

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
#  *    2010 - 2014 Do Kester, SRON (Java code)
#  *    2017        Do Kester

class Engine( object ):
    """
    Engine defines general properties of a Engine.

    An Engine moves around a sample in a random way such that its likelood
    remain above the low-likelihood-limit.

    Attributes
    ----------
    walkers : SampleList
        walkers to be diffused
    errdis : ErrorDistribution
        error distribution to be used
    maxtrials : int
        maximum number of trials for various operations
    rng : numpy.random.RandomState
        random number generator

    report : list of int (read only)
        reports number of succes, accepted, rejected, failed calls. Plus the total.
    unitRange : array_like (read only)
        present max size of the parameter cloud (in [0,1])
    unitMin : array_like (read only)
        present minimum values of the parameter cloud (in [0,1])

    Author       Do Kester.

    """
    SUCCESS = 0             #  succesfull move
    REJECT = 1              #  rejected move
    FAILED = 2              #  failed to move
    NCALLS = 3              #  number of calls


    #  *********CONSTRUCTORS***************************************************

    def __init__( self, walkers, errdis, copy=None, seed=4213 ):
        """
        Copy Constructor.
        Parameters
        ----------
        walkers : SampleList
            walkers to be diffused
        errdis : ErrorDistribution
            error distribution to be used
        copy : Engine
            engine to be copied

        """
        self.walkers = walkers
        self.errdis = errdis
        self.report = [0]*4

        if copy is None :
            self.maxtrials = 5
            self.rng = numpy.random.RandomState( seed )
        else :
            self.maxtrials = copy.maxtrials
            self.rng = copy.rng

    def copy( self ):
        """ Return a copy of ths engine.  """
        return Engine( self.walkers, self.errdis, copy=self )

    def __getattr__( self, name ) :
        if name == "unitRange" :
            return self.calculateUnitRange()
        elif name == "unitMin" :
            self.calculateUnitRange()
            return self.unitMin
        else :
             raise AttributeError( str( self ) + ": Unknown attribute " + name )


    #  *********SET & GET***************************************************
    def setSample( self, walker, model, parlist, logL, logW=None ):
        """
        Update the sample with model, parlist, LogL and logW.

        Parameters
        ----------
        walker : Sample
            sample to be updated
        model : Model
            the model in the sample
        parlist : array_like
            list of all parameters
        logL : float
            log Likelihood
        logW : float
            log of the weight of the likelihood
        """
        walker.logL = logL
        walker.parlist = parlist
        walker.model = model
        if logW is not None :
            walker.logW = logW
        self.walkers[walker.id] = walker

###### TBD:
##  Has dval the length kpar ???

    def domain2Unit( self, model, dval, kpar=None ) :
        """
        Return value in [0,1] for the selected parameter.

        Parameters
        ----------
        model : Model
            the model involved
        dval : float
            domain value for the selected parameter
        kpar : None or array_like
            selected parameter index, where kp is index in [parameters, hyperparams]
            None means all
        """
        np = model.npchain
        if kpar is None :
            kpar = range( len( dval ) )
        elif Tools.isInstance( kpar, int ) :
            return ( model.domain2Unit( dval, kpar ) if kpar < np else
                     self.errdis.domain2Unit( dval, kpar - np ) )

        uval = numpy.ndarray( len( kpar ), dtype=float )
        for i,kp in enumerate( kpar ) :
            if kp < np :
                uval[i] = model.domain2Unit( dval[kp], kp )
            else :
                uval[i] = self.errdis.domain2Unit( dval[kp], kp - np )
        return uval

    def unit2Domain( self, model, uval, kpar=None ) :
        """
        Return domain value for the selected parameter.

        Parameters
        ----------
        model : Model
            the model involved
        uval : array_like
            unit value for the selected parameter
        kpar : None or array_like
            selected parameter indices, where kp is index in [parameters, hyperparams]
            None means all.
        """
        np = model.npchain
        if kpar is None :
            kpar = range( len( uval ) )
        elif Tools.isInstance( kpar, int ) :
            return ( model.unit2Domain( uval, kpar ) if kpar < np else
                     self.errdis.unit2Domain( uval, kpar - np ) )

        dval = numpy.ndarray( len( kpar ), dtype=float )
        for i,kp in enumerate( kpar ) :
            if kp < np :
                dval[i] = model.unit2Domain( uval[kp], kp )
            else :
                dval[i] = self.errdis.unit2Domain( uval[kp], kp - np )
        return dval

    def reportCall( self ):
        """ Store a call to engine  """
        self.report[self.NCALLS] += 1

    def reportSuccess( self ):
        self.report[self.SUCCESS] += 1

    def reportReject( self ):
        self.report[self.REJECT] += 1

    def reportFailed( self ):
        self.report[self.FAILED] += 1

    def printReport( self ) :
        print( " %10d %10d %10d %10d" % (self.report[0], self.report[1],
                                         self.report[2], self.report[3] ) )

    def calculateUnitRange( self ):
        """
        Calculate the range of the present parameter values in unit values.

        For Dynamic models the range is calculated for those parameters present in all models;
        it is 1.0 for other parameters.

        """
        npmax = self.walkers.getMaximumNumberOfParameters( )

        kmx = 0
        for walker in self.walkers :
            if walker.model.npchain == npmax :
                minv = walker.parlist.copy()
                maxv = minv.copy()
                break
            kmx += 1

        nval = numpy.zeros_like( self.walkers[kmx].parlist, dtype=float )

        for walker in self.walkers :
            np = walker.parlist.size
            minv[:np] = numpy.fmin( minv[:np], walker.parlist )
            maxv[:np] = numpy.fmax( maxv[:np], walker.parlist )
            nval[:np] += 1

        model = self.walkers[kmx].model

        maxv = self.domain2Unit( model, maxv )
        minv = self.domain2Unit( model, minv )

        q = numpy.where( numpy.logical_or( maxv == minv, nval < len( self.walkers ) ) )
        maxv[q] = 1.0
        minv[q] = 0.0

        self.unitRange = numpy.abs( maxv - minv )
        self.unitMin = numpy.fmin( minv, maxv )

        return self.unitRange

    def __str__( self ) :
        return str( "Engine" )

    def execute( self, walker, lowLhood, fitIndex=None ):
        """
        Execute the engine for diffusing the parameters

        Parameters
        ----------
        walker : Sample
            walker to diffuse
        lowLhood : float
            low limit on the loglikelihood
        fitIndex : array_like
            list of parameter indices to diffuse

        Returns
        -------
        int : number of succesfull moves

        """
        pass


class DummyPlotter( object ) :

    def __init__( self, iter=0 ) :
        self.iter = iter

    def start( self ):
        """ start the plot. """
        pass

    def move( self, param, ptry, col=None ):
        """
        Move parameters at position param to ptry using color col.
        """
        pass

    def stop( self ):
        """ Stop (show) the plot. """
        pass

