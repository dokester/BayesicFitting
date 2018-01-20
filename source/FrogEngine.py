import numpy as numpy
from astropy import units
import math
import Tools

from Engine import Engine

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

class FrogEngine( Engine ):
    """
    The FrogEngine jumps a parameter set towards/over a bunch of others.

    Take a number of walkers, 1 <= N <= maxnumber, and average their parameters.
    Jump the target walker away, towards or over this average.

    The walker is kept when the logLikelihood > lowLhood.

    Usefull engine when the likelihood is a long narrow ridge.

    Author       Do Kester.

    Attributes
    ----------
    maxnumber : int
        the maximum number of averageable walkers.



    """

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, seed=4213 ):
        """
        Constructor.

        Parameters
        ----------
        walkers : SampleList
            walkers to be diffused
        errdis : ErrorDistribution
            error dstribution to be used
        copy : CrossEngine
            engine to copy
        seed : int
            for rng

        """
        super( FrogEngine, self ).__init__( walkers, errdis, copy=copy, seed=seed )
        self.maxnumber = 5

    def copy( self ):
        """ Return copy of this.  """
        return FrogEngine( self.walkers, self.errdis, copy=self )


    def __str__( self ):
        return str( "FrogEngine" )

    #  *********EXECUTE***************************************************
    def execute( self, sample, lowLhood, fitIndex=None ):
        """
        Execute the engine by diffusing the parameters.

        Parameters
        ----------
        sample : Sample
            walker to diffuse
        lowLhood : float
            lower limit in logLikelihood
        fitIndex : array_like
            list if the parameters to be diffused

        Returns
        -------
        int : the number of successfull moves

        """
        if fitIndex is None :
            fitIndex = sample.fitIndex

        model = sample.model                    ### TBC need a copy here ????
        param = sample.allpars[:]

        np = len( param )
        nm = len( self.walkers )

        kk = 1
        while True:

            param = self.frogJump( sample, param )
            if len( param ) == 0 :
                return 0

            Ltry = self.errdis.logLikelihood( model, param )
            if Ltry >= lowLhood:
                self.reportSuccess( )
                self.setSample( walker, model, param, Ltry )
                return np
            elif kk <= self.maxtrials :
                param = walker.getParameters( ).copy( )
                self.reportReject( )
            else :
                self.reportFailed()
                break
            kk += 1
        return 0

    def frogJump( self, sample, param ):
        parent = sample.parent
        model = sample.model
        np = len( param )

        indx = []
        ensemble = getMembers( ).getNumberOfSamples( )
        p = 0
        jumppoint = numpy.asarray( np + 1, dtype=float )
        __trials_1 = trials
        trials += 1
        __p_2 = p
        p += 1
        while True:
            indx = []S
            while i < S:
                while True:
                    if __trials_1 > getMaxTrials( ) * S:
                        reportFailed( )
                        return None
                    m = getRandom( ).nextInt(ensemble )
                    mp = getMembers( ).getNumberOfParameters(m )
                    if not ( (m == walkerId or m == parent or mp != np) ):
                        break
                indx[i] = m
                i += 1
            while k < np and inside:
                while i < S:
                    sum += model.domain2Unit( pp, k )
                    i += 1
                jumppoint.set( k, model.unit2Domain( up + sum / S, k) )
                up += factor * sum / S
                inside = up >= 0 and up <= 1
                if inside:
                    param.set( k, model.unit2Domain( up, k) )
                k += 1
            if inside:
                break
            param = walker.getParameters( ).copy( )
            if not ( (__p_2 < getMaxTrials( )) ):
                break
        return param


