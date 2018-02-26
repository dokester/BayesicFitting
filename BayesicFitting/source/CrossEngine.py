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

class CrossEngine( Engine ):
    """
    Cross over between 2 walkers.

    Select another walker from the ensemble and perform a cross-over of
    their parameter lists. I.e. choose at random from one list or the other.

    The walker is kept when the logLikelihood > lowLhood.

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
            error dstribution to be used
        copy : CrossEngine
            engine to copy
        seed : int
            for rng

        """
        super( CrossEngine, self ).__init__( walkers, errdis, copy=copy, seed=seed )

    def copy( self ):
        """ Return copy of this.  """
        return CrossEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "CrossEngine" )

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
            list if the parameters to be diffused

        Returns
        -------
        int : the number of successfull moves

        """
        if fitIndex is None :
            fitIndex = walker.fitIndex
        nf = len( fitIndex )

        model = walker.model
        param = walker.allpars[:]

        nm = len( self.walkers )
        np = len( param )
        if np <= 2 and nm > 1 :
            self.reportFailed( )
            return 0

        kk = 0
        while True:
            kk += 1
            while True:
                m = self.rng.randint( nm )
                if not ( (m == walker.id or m == walker.parent) ):
                    break

            crospar = self.walkers[m].allpars
            mp = len( crospar )
            if mp == 0:
                continue
            if np < mp:
                mp = np

            # take parameters randomly from param and crospar
#            perm = self.rng.permutation( fitIndex )
#            kp = 1 + self.rng.randint( mp - 2 )         # at least 1 par of each walker
#            perm = perm[:kp]
#            param[perm] = crospar[perm]

            # mix parameters randomly
            f = self.rng.rand( nf )
            param[fitIndex] = f * param[fitIndex] + ( 1 - f ) * crospar[fitIndex]

            Ltry = self.errdis.logLikelihood( model, param )
            if Ltry >= lowLhood:
                self.reportSuccess( )
                self.setSample( walker, model, param, Ltry )
                return nf
            elif kk <= self.maxtrials :
                param = walker.allpars[:]
                self.reportReject( )
            else :
                self.reportFailed()
                return 0

        return 0


