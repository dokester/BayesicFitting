import numpy as numpy
import math

from .WalkerList import WalkerList

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
#  *           2025 Do Kester

class PhantomCollection( object ):
    """
    Helper class for NestedSamplers Engines to collect all trial walkers
    obtained during the NS run. They are kept ordered according to their logL.  
    They are used to find the minimum and maximum values 
    of the parameter settings as function of the likelihood. 

    There are different methods for static models and for dynamic models. 

    For dynamic models only parameter sets of the proper length are searched.
    The kth item in self.logL belongs to the kth list in self.pars.
    If the model had np parameters then self.logL[np][k] pertain to 
    self.pars[np][k,:] which has np items

    For static models there is only one array of self.logL and one 2-d array 
    od self.pars.

    Attributes
    ----------
    phantoms : WalkerList or dict of { int : WalkerList }
        int         number of parameters in the model
        Wlakerlist  list of (phantom) walkers
    paramMin : array_like or None
        minimum values of the parameters at this stage of lowLhood
        None if too few items of this parameter length is present
    paramMax : array_like or None
        maximum values of the parameters at this stage of lowLhood
        None if too few items of this parameter length is present


    Author       Do Kester.

    """
    #  *********CONSTRUCTORS***************************************************

    MINPARS = 5

    def __init__( self, dynamic=False ):
        """
        Constructor.

        Parameters
        ----------
        dynamic : bool
            whether it is a dynamic model
        """
        self.minpars = self.MINPARS
        self.ncalls = 0
            
        self.phantoms = WalkerList()
        self.lowLhood = -math.inf

        self.npars = -1

    def __str__( self ):
        """ Return the name of this object.  """
        return "PhantomCollection"


    def length( self, np=None ) :
        """
        Return length of internal walkerlist

        Parameters
        ----------
        np : int or None
            None return overall length
            number of parameters (in case of dynamic only)
        """
        if np is None :
            return len( self.phantoms )

        kl = 0
        for w in self.phantoms :
            if w.nap == np :
                kl += 1
        return kl

    def getBest( self, np ) :
        """
        Return the best phantom with np parameters; or -1 if no phantom has
        np parameters

        Parameters
        ----------
        np : int
            number of parameters
        """
        k = len( self.phantoms ) - 1
        while k >= 0 and self.phantoms[k].nap != np :
            k -= 1

        return k
 
    def nextLowPhantom( self, lowLhood ) :
        """
        Generator for phantoms with logL < lowLhood

        Parameters
        ----------
        lowLhood : float
            low border for likelihood
        """
        for ph in self.phantoms :
            if ph.logL <= lowLhood :
                yield ph
            else :
                return

    def storeItems( self, walker ) :
        """
        Store both items as arrays.

        Parameters
        ----------
        walker : Walker
            to be added to the PhantomCollection
        """
        self.ncalls += 1
        self.phantoms = self.phantoms.insertWalker( walker )


    def getParamMinmax( self, lowLhood, np=None ):
        """
        Obtain the min and max values of the present parameter values.

        Parameters
        ----------
        lowLhood : float
            lower boundary of the log Likelihood
        np : int or None
            number of parameters (not used in this implementation)

        """
        if lowLhood > self.lowLhood or self.npars != np :
            self.calculateParamMinmax( lowLhood, np=np )

        return ( self.paramMin, self.paramMax )


    def calculateParamMinmax( self, lowLhood, np=None ):
        """
        Calculate the min and max values of the present parameters of length np.

        Parameters
        ----------
        lowLhood : float
            lower boundary of the log Likelihood
        np : int or None
            None for static models.
            number of parameters

        """
        self.lowLhood = lowLhood
        self.npars = np

        self.phantoms = self.phantoms.cropOnLow( lowLhood )

        if self.length( np ) <= self.minpars :
            self.paramMax = None
            self.paramMin = None
            return

        pars = self.phantoms.allPars( npars=np )

        self.paramMin = numpy.nanmin( pars, axis=0 )
        self.paramMax = numpy.nanmax( pars, axis=0 )

        return





