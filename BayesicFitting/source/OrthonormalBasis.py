import numpy as numpy
from . import Tools

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
#  *    2019 - 2020 Do Kester

class OrthonormalBasis( object ):
    """
    Helper class to construct a orthonormal basis from (random) vectors

    Attributes
    ----------
    basis : 2darray
        array of orthonormal vectors

    Author       Do Kester.

    """
    #  *********CONSTRUCTORS***************************************************

    def __init__( self ):
        """
        Constructor.
        """
        pass

    def normalise( self, vec, reset=False ) :
        """
        Construct from vec a unit vector orthogonal to self.basis

        from http://www.ecs.umass.edu/ece/ece313/Online_help/gram.pdf

        Parameters
        ----------
        vec : array_like
            vector to be orthonomalised to self.basis
        reset : bool
            start a new basis.
        """
        nb = 0 if reset or not hasattr( self, "basis" ) else self.basis.shape[0]
        if nb >= len( vec ) :
            nb = 0

        uv = 0.0
        for k in range( nb ) :
            u = self.basis[k,:]
            uv += numpy.inner( u, vec ) * u
        uvec = vec - uv
        uvec /= numpy.linalg.norm( uvec )

        if nb == 0 :
            self.basis = uvec.reshape( (1,-1) )
        else :
            self.basis = numpy.append( self.basis, [uvec], 0 )

#        print( nb, self.basis.shape )
        return uvec


    def __str__( self ) :
        return str( "OrthonormalBasis" )

