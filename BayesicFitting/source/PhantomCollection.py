import numpy as numpy
import math

from .Walker import Walker
from .WalkerList import WalkerList
from . import Tools

__author__ = "Do Kester"
__year__ = 2024
__license__ = "GPL3"
__version__ = "3.2.1"
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
#  *           2024 Do Kester

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
            
        if dynamic :
            self.phantoms = {}
            self.lowLhood = {}
            self.paramMax = {}
            self.paramMin = {}
            self.getList = self.getDynamicList
            self.getParamMinmax = self.getDynamic
            self.storeItems = self.storeDynamic
            self.length = self.lengthDynamic
        else :
            self.phantoms = WalkerList( )
            self.lowLhood = -math.inf

    def __str__( self ):
        """ Return the name of this object.  """
        return "PhantomCollection"

    ##  Methods for static models

    def length( self, np=0 ) :
        """
        Return length of internal walkerlist

        Parameters
        ----------
        np : int
            number of parameters (in case of dynamic only)
        """
        return len( self.phantoms )

    def getList( self, walker ) :
        """
        Return the applicable WalkerList

        Parameters
        ----------
        walker : Walker
            return list pertaining to this walker (not used here)
        """
        return self.phantoms
 
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

    def calculateParamMinmax( self, lowLhood, np=0 ):
        """
        Calculate the min and max values of the present parameter values.

        Parameters
        ----------
        lowLhood : float
            lower boundary of the log Likelihood
        np : int
            number of parameters (not used in this implementation)

        """
        self.lowLhood = lowLhood
        self.phantoms = self.phantoms.cropOnLow( lowLhood )

        if len( self.phantoms ) == 0 :
            self.paramMin = None
            self.paramMax = None
        else :
            pars = self.phantoms.allPars()
            self.paramMin = numpy.nanmin( pars, axis=0 )
            self.paramMax = numpy.nanmax( pars, axis=0 )


    def getParamMinmax( self, lowLhood, np=0 ):
        """
        Obtain the min and max values of the present parameter values.

        Parameters
        ----------
        lowLhood : float
            lower boundary of the log Likelihood
        np : int
            number of parameters (not used in this implementation)

        """
        if lowLhood > self.lowLhood :
            self.calculateParamMinmax( lowLhood, np=np )

        return ( self.paramMin, self.paramMax )

    ##  Dynamic methods

    def lengthDynamic( self, np=None ) :
        """
        Return length of internal walkerlist

        Parameters
        ----------
        np : int
            number of parameters (in case of dynamic only)
        """
        if np is None :
            return numpy.sum( [len( ph ) for ph in self.phantoms.values()] )
        return len( self.phantoms[np] ) if np in self.phantoms else 0

    def getDynamicList( self, walker ) :
        """
        Return the applicable WalkerList or None if not present.

        Parameters
        ----------
        walker : Walker
            return list pertaining to this walker
        """
        np = walker.problem.npars
        return self.phantoms[np] if np in self.phantoms else None

    def storeDynamic( self, walker ) :
        """
        Put both items in the dictionaries with npars as key

        Parameters
        ----------
        logL : float
            log Likelihood 
        pars : 1d array
            parameters
        """
        self.ncalls += 1
        np = walker.problem.npars
        if not np in self.phantoms :
            self.phantoms[np] = WalkerList()

        self.phantoms[np] = self.phantoms[np].insertWalker( walker )

    def calculateDynamic( self, lowLhood, np=0 ):
        """
        Calculate the min and max values of the present parameters of length np.

        Parameters
        ----------
        lowLhood : float
            lower boundary of the log Likelihood
        np : int
            number of parameters

        """
        self.lowLhood[np] = lowLhood
        if np in self.phantoms :
            self.phantoms[np] = self.phantoms[np].cropOnLow( lowLhood )
        else :
            self.phantoms[np] = WalkerList()


        if self.length( np ) <= self.minpars :
            self.paramMax[np] = None
            self.paramMin[np] = None
            return

        pars = self.phantoms[np].allPars()
        self.paramMin[np] = numpy.nanmin( pars, axis=0 )
        self.paramMax[np] = numpy.nanmax( pars, axis=0 )

        return

    def getDynamic( self, lowLhood, np=0 ):
        """
        Return the min and max values of the present parameters of length np.

        Parameters
        ----------
        lowLhood : float
            lower boundary of the log Likelihood
        np : int
            number of parameters

        """
        if not np in self.lowLhood or lowLhood > self.lowLhood[np] or self.paramMin[np] is None :
            self.calculateDynamic( lowLhood, np=np )
        return ( self.paramMin[np], self.paramMax[np] )




