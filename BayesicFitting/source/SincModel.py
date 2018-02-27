from .KernelModel import KernelModel
from .kernels.Sinc import Sinc

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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2017 Do Kester

class SincModel( KernelModel ):
    """
    Sinc Model.
    Also known as Cardinal Sine.
    .. math::
        f( x:p ) = p_0 * sin( ( x - p_1 ) / p_2 ) / ( ( x - p_1 ) / p_2 )

    where :math:`p_0` = amplitude, :math:`p_1` = offset and
    :math:`p_2` = width ( =Distance between first zero-crossings divided by 2 Pi. )
    As always x = input.

    The parameters are initialized at {1.0, 0.0, 1.0}.
    Parameter 2 ( width ) is always kept positive ( >=0 ).

    SincModel() is syntactic sugar for KernelModel( kernel=Sinc() )

    Examples
    --------
    >>> sinc = SincModel( )
    >>> print sinc.npchain
    3
    >>> print( sinc( numpy.arange( 15, dtype=float )-7 ) )        # sinc function between [-7,+7]
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]

    """
    def __init__( self, copy=None, **kwargs ):
        """
        Sinc model.

        Number of parameters is 3.

        Parameters
        ----------
        copy : ArctanModel
            to be copied
        fixed : dictionary of {int:float}
            int     list if parameters to fix permanently. Default None.
            float   list of values for the fixed parameters.
            Attribute fixed can only be set in the constructor.
        """
        super( SincModel, self ).__init__( kernel=Sinc(), copy=copy, **kwargs )

    def copy( self ):
        """ Copy method.  """
        return SincModel( copy=self )


