import numpy as numpy
from astropy import units
import math
from . import Tools

from .Dynamic import Dynamic
from .Engine import Engine

__author__ = "Do Kester"
__year__ = 2018
__license__ = "GPL"
__version__ = "1.0"
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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2018        Do Kester


class DeathEngine( Engine ):
    """
    The DeathEngine deletes a component from the model.

    Only for Models that are Dynamic.
    The death rate is governed by the growth-prior in the dynamic model.

    The member is kept when the logLikelihood > lowLhood.

    Author       Do Kester.

    """
#    _deathrate = 1.0

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, seed=23455 ):
        """
        Constructor.

        Parameters
        ----------
        walkers : SampleList
            walkers to be diffused
        errdis : ErrorDistribution
            error distribution to be used
        copy : GalileanEngine
            to be copied
        seed : int
            for random number generator
        """
        super( DeathEngine, self ).__init__( walkers, errdis, copy=copy,
                    seed=seed )

    def copy( self ):
        """ Return copy of this.  """
        return DeathEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "DeathEngine" )

    #  *********EXECUTE***************************************************
    def execute( self, walker, lowLhood, fitIndex=None ):
        """
        Execute the engine by removins a component.

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
#        print( "Deng  : ", end="" )
        waltry = walker.copy()
        model = waltry.model
        ptry = waltry.allpars

        pat = 0
        while model is not None and not isinstance( model, Dynamic ) :
            pat += model.npbase
            model = model._next

        np = model.npbase

        if not ( np > model.growPrior.unit2Domain( self.rng.rand() ) and
                model.shrink( pat ) ) :
            self.reportFailed()
#            print( "DE  failed" )
            return 0

        dnp = model.deltaNpar        # parameter decrease
        ptry = model.alterParameters( ptry, np, -dnp, pat )
        find = model.alterFitindex( walker.fitIndex, np, -dnp, pat )

        model = waltry.model

        Ltry = self.errdis.logLikelihood( model, ptry )

        if Ltry >= lowLhood:
            self.reportSuccess()
            self.setSample( walker, model, ptry, Ltry, fitindex=find )
            walker.check( nhyp=self.errdis.nphypar )
            return dnp

        self.reportReject( )
        walker.check( nhyp=self.errdis.nphypar )
        return 0


