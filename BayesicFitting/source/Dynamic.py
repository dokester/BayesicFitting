import numpy as numpy
import random
from astropy import units
from . import Tools
import warnings
from .Formatter import formatter as fmt

from .Prior import Prior

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
#  *    2016 - 2018 Do Kester


class Dynamic( object ):
    """
    Class adjoint to Model which implements some dynamic behaviour.

    """

    def getNumberOfComponents( self ):
        return self.npbase / self.deltaNpar

    def __setattr__( self, name, value ) :
        dind = {"growPrior" : Prior}
        if ( Tools.setNoneAttributes( self, name, value, lnon ) or
             Tools.setSingleAttributes( self, name, value, dind ) ) :
            pass
        else :
            super( ).__setattr__( name, value )






    def alterParameterSize( self, dnp, pat ) :
        """
        Change the number of parameters and self.parameters.

        Parameters
        ----------
        npnew : int
            number of parameters in the DynamicModel
        pat : int
            starting index of the DynamicModel
        """
        npnew = self.npbase + dnp
#        print( "Dyn  ", pat, self.npbase, dnp )

        if dnp == 0 :
            return

        mdlpar = self._head.parameters
#        print( "mdlpar  ", mdlpar )
        mdlpar = self.alterParameters( mdlpar, self.npbase, dnp, pat )

        self.npmax += dnp
        self.npbase += dnp
        self._head._npchain += dnp

        self._head.parameters = mdlpar

    def alterParameters( self, param, npbase, dnp, pat ) :

        newpar = numpy.zeros( len( param ) + dnp, dtype=float )
        kh = pat + npbase + dnp
        kb = pat + npbase

#        print( param.shape, npbase, pat, dnp, kh, kb )
        if dnp < 0 :
            newpar[:kh] = param[:kh]
            newpar[kh:] = param[kb:]
        else :
            newpar[:kb] = param[:kb]
            newpar[kh:] = param[kb:]

#        print( "nwpar  ", fmt( newpar, max=None ) )
        return newpar

    def alterFitindex( self, findex, npbase, dnp, pat ) :

        newfi = numpy.zeros( len( findex ) + dnp, dtype=int )
        kh = pat + npbase + dnp
        kb = pat + npbase

#        print( param.shape, npbase, pat, dnp, kh, kb )
        if dnp < 0 :
            newfi[:kh] = findex[:kh]
            newfi[kh:] = findex[kb:]
        else :
            newfi[:kb] = findex[:kb]
            newfi[kb:kh] = numpy.arange( dnp ) + findex[kb-1] + 1
            newfi[kh:] = findex[kb:]

#        print( "newfi  ", fmt( newfi, max=None ) )
        return newfi




