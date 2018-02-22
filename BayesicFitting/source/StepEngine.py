import numpy as numpy
from . import Tools

from .Engine import Engine

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

class StepEngine( Engine ):
    """
    Move a a walker in a random direction.

    The StepEngine tries to move a selection of the parameters
    in a random order.

    Author       Do Kester.

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
            error distribution to be used
        copy : StepEngine
            to be copied
        seed : int
            for rng

        """
        super( StepEngine, self ).__init__( walkers, errdis, copy=copy, seed=seed )

    def copy( self ):
        """ Return copy of this.  """
        return StepEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "StepEngine" )


    #  *********EXECUTE***************************************************
    def execute( self, walker, lowLhood, fitIndex=None ):
        """
        Execute the engine by diffusing the parameters.

        Parameters
        ----------
        walker : Sample
            walker to diffuse
        lowLhood : float
            lower limit in logLikelihood
        fitIndex : array_like
            list of the/some parameters indices to be diffused

        Returns
        -------
        int : the number of successfull moves

        """
        if fitIndex is None :
            fitIndex = walker.fitIndex
        np = len( fitIndex )

        model = walker.model
        nm = len( self.walkers )

        urange = self.unitRange[fitIndex]
        dur = urange / nm
        urange += 2 * dur

        param = walker.allpars
        usav = self.domain2Unit( model, param, kpar=fitIndex )

        sz = 1.0
        ptry = param.copy()
        kk = 0
        while True :
            kk += 1

            step = ( 2 * self.rng.rand( np ) - 1 ) * urange
            while True :
                utry = usav + step
                q0 = numpy.where( utry < 0 )[0]
                nq0 = len( q0 )
                q1 = numpy.where( utry > 1 )[0]
                nq1 = len( q1 )

                if nq0 > 0 :
                    step[q0] = ( 2 * self.rng.rand( nq0 ) - 1 ) * urange[q0]
                elif nq1 > 0 :
                    step[q1] = ( 2 * self.rng.rand( nq1 ) - 1 ) * urange[q1]
                else :
                    break

            ptry[fitIndex] = self.unit2Domain( model, utry,  )

            Ltry = self.errdis.logLikelihood( model, ptry )
            if Ltry >= lowLhood:
                self.reportSuccess( )
                self.setSample( walker, model, ptry, Ltry )
                break
            elif kk < self.maxtrials :
                sz *= 0.5
                self.reportReject( )
            else :
                self.reportFailed()
                break

        return np                        # nr of succesfull steps


