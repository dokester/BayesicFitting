import numpy as numpy
import math
from .NonLinearModel import NonLinearModel
from .LorentzModel import LorentzModel

__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

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
#  *    2003 - 2011 Do Kester, SRON (JAVA code)
#  *    2016 - 2017 Do Kester

class VoigtModel( NonLinearModel ):
    """
    Voigt's Gauss Lorentz convoluted model for line profiles.

    The Voigt function is a convolution of a Gauss and a Lorentz function.
    Physicaly it is the result of thermal and pressure broadening of a spectral
    line.

    The models takes 4 parameters: amplitude, center frequency, half-width of
    the Gaussian, and half-width of the Lorentzian.
    These are initialised to [1, 0, 1, 1].
    Parameters 2 & 3 ( widths ) is always kept positive ( >=0 ).

    Examples
    --------
    >>> voigt = VoigtModel( )
    >>> voigt.setParameters( [5, 4, 1, 2] )
    >>> print( voigt( numpy.arange(  41 , dtype=float ) / 5 ) )      # from [0,8]

    """

    R0 = 146.7
    R1 = 14.67
    RRTPI = 0.56418958              #  = 1/sqrt( pi )
    Y0 = 1.5
    Y0PY0 = Y0 + Y0
    Y0Q = Y0 * Y0
    C = [1.0117281, -0.75197147, 0.012557727, 0.010022008, -0.00024206814, 0.00000050084806]
    S = [1.393237, 0.23115241, -0.15535147, 0.0062183662,  0.000091908299, -0.00000062752596]
    T = [0.31424038, 0.94778839, 1.5976826, 2.2795071, 3.0206370, 3.8897249]
    LN2 = math.log( 2.0 )
    SRLN2 = math.sqrt( LN2 )

    def __init__( self, copy=None, **kwargs ):
        """
        Voigt model.
        <br>
        Number of parameters is 4.

        Parameters
        ----------
        copy : VoigtModel
            to be copied

        """
        param = [1.0, 0.0, 1.0, 1.0]
        names = ["amplitude","center","gausswidth","lorentzwidth"]

        super( VoigtModel, self ).__init__( 4, copy=copy, params=param,
                        names=names, **kwargs )
        if copy is None :
            self.posIndex = [2,3]
            self.nonZero  = [3]

    def copy( self ):
        """ Copy method.  """
        return VoigtModel( copy=self )

    def baseResult( self, xdata, params ):
        """
        Returns the result of the model function.

        Note: both width in the parameter array ( items 2 & 3 ) are kept
        strictly positive. I.e. they are changed when upon xdata they are negative.

        Parameters
        ----------
        xdata : array_like
            values at which to calculate the result
        params : array_like
            values for the parameters.

        """
        if params[2] == 0:
            p = params[[0,1,3]]
            return LorentzModel( ).result( xdata, p )

        rtn = numpy.zeros_like( xdata )
        x = ( xdata - params[1] ) * self.SRLN2 / params[2]
        y = self.SRLN2 * params[3] / params[2]
        for k in range( len( xdata ) ) :
            rtn[k] = self.calculate( x[k], y )

        # Avoid multiple calculations of r0 for the same y
        r0 = self.calculate( 0, y )

        return params[0] * rtn / r0

    def baseName( self ):
        """
        Returns a string representation of the model.
        """
        return str( "Voigt:" )

    def calculate( self, xAxis, y ):
        ## This is legacy code, probably from FORTRAN.
        ## Unfortunately, I dont know where it came from.

        realPart = 0
        RG1 = 1
        RG2 = 1
        RG3 = 1
        YQ = y * y
        YRRTPI = y * self.RRTPI
        ABX = 0.0
        XQ = 0.0
        XLIM0 = self.R0 - y
        XLIM1 = self.R1 - y
        XLIM3 = 3.097 * y - 0.45
        XLIM2 = 6.8 - y
        XLIM4 = 18.1 * y + 1.65
        A0 = 0.0
        D0 = 0.0
        D2 = 0.0
        E0 = 0.0
        E2 = 0.0
        E4 = 0.0
        H0 = 0.0
        H2 = 0.0
        H4 = 0.0
        H6 = 0.0
        P0 = 0.0
        P2 = 0.0
        P4 = 0.0
        P6 = 0.0
        P8 = 0.0
        Z0 = 0.0
        Z2 = 0.0
        Z4 = 0.0
        Z6 = 0.0
        Z8 = 0.0
        D = 0.0
        YF = 0.0
        YPY0 = 0.0
        YPY0Q = 0.0
        XP = numpy.zeros( 6 )
        XM = numpy.zeros( 6 )
        YP = numpy.zeros( 6 )
        YM = numpy.zeros( 6 )
        MQ = numpy.zeros( 6 )
        PQ = numpy.zeros( 6 )
        MF = numpy.zeros( 6 )
        PF = numpy.zeros( 6 )
        ABX = abs( xAxis )
        XQ = ABX * ABX
        if ABX > XLIM0:
            realPart = YRRTPI / ( XQ + YQ )
        elif ABX > XLIM1:
            if RG1 != 0:
                RG1 = 0
                A0 = YQ + 0.5
                D0 = A0 * A0
                D2 = YQ + YQ - 1.0
            D = self.RRTPI / ( D0 + XQ * ( D2 + XQ) )
            realPart = D * y * ( A0 + XQ )
        elif ABX > XLIM2:
            if RG2 != 0:
                RG2 = 0
                H0 = 0.5625 + YQ * ( 4.5 + YQ * ( 10.5 + YQ * ( 6.0 + YQ)) )
                H2 = -4.5 + YQ * ( 9.0 + YQ * ( 6.0 + YQ * 4.0) )
                H4 = 10.5 - YQ * ( 6.0 - YQ * 6.0 )
                H6 = -6.0 + YQ * 4.0
                E0 = 1.875 + YQ * ( 8.25 + YQ * ( 5.5 + YQ) )
                E2 = 5.25 + YQ * ( 1.0 + YQ * 3.0 )
                E4 = 0.75 * H6
            D = self.RRTPI / ( H0 + XQ * ( H2 + XQ * ( H4 + XQ * ( H6 + XQ))) )
            realPart = D * y * ( E0 + XQ * ( E2 + XQ * ( E4 + XQ)) )
        elif ABX < XLIM3:
            if RG3 != 0:
                RG3 = 0
                Z0 = 272.1014 + y * ( 1280.829 + y * ( 2802.870 + y * ( 3764.966 + y * ( 3447.629 + y * ( 2256.981 + y * ( 1074.409 + y * ( 369.1989 + y * ( 88.26741 + y * ( 13.39880 + y)))))))) )
                Z2 = 211.678 + y * ( 902.3066 + y * ( 1758.336 + y * ( 2037.310 + y * ( 1549.675 + y * ( 793.4273 + y * ( 266.2987 + y * ( 53.59518 + y * 5.0)))))) )
                Z4 = 78.86585 + y * ( 308.1852 + y * ( 497.3014 + y * ( 479.2576 + y * ( 269.2916 + y * ( 80.39278 + y * 10.0)))) )
                Z6 = 22.03523 + y * ( 55.02933 + y * ( 92.75679 + y * ( 53.59518 + y * 10.0)) )
                Z8 = 1.496460 + y * ( 13.39880 + y * 5.0 )
                P0 = 153.5168 + y * ( 549.3954 + y * ( 919.4955 + y * ( 946.8970 + y * ( 662.8097 + y * ( 328.2151 + y * ( 115.3772 + y * ( 27.93941 + y * ( 4.264678 + y * 0.3183291))))))) )
                P2 = -34.16955 + y * ( -1.322256 + y * ( 124.5975 + y * ( 189.7730 + y * ( 139.4665 + y * ( 56.81652 + y * ( 12.79458 + y * 1.2733163))))) )
                P4 = 2.584042 + y * ( 10.46332 + y * ( 24.01655 + y * ( 29.81482 + y * ( 12.79568 + y * 1.9099744))) )
                P6 = -0.07272979 + y * ( 0.9377051 + y * ( 4.266322 + y * 1.273316) )
                P8 = 0.0005480304 + y * 0.3183291
            D = 1.7724538 / ( Z0 + XQ * ( Z2 + XQ * ( Z4 + XQ * ( Z6 + XQ * ( Z8 + XQ)))) )
            realPart = D * ( P0 + XQ * ( P2 + XQ * ( P4 + XQ * ( P6 + XQ * P8))) )
        else:
            YPY0 = y + self.Y0
            YPY0Q = YPY0 * YPY0
            realPart = 0.0
            for J in range( 6 ) :
                D = xAxis - self.T[J]
                MQ[J] = D * D
                MF[J] = 1.0 / ( MQ[J] + YPY0Q )
                XM[J] = MF[J] * D
                YM[J] = MF[J] * YPY0
                D = xAxis + self.T[J]
                PQ[J] = D * D
                PF[J] = 1.0 / ( PQ[J] + YPY0Q )
                XP[J] = PF[J] * D
                YP[J] = PF[J] * YPY0

            if ABX <= XLIM4:
                for J in range( 6 ) :
                    realPart = realPart + self.C[J] * ( YM[J] + YP[J] ) - self.S[J] * ( XM[J] - XP[J] )
            else:
                YF = y + self.Y0PY0
                for J in range( 6 ) :
                    realPart = realPart + ( self.C[J] * ( MQ[J] * MF[J] - self.Y0 * YM[J] ) + self.S[J] * YF * XM[J] ) / ( MQ[J] + self.Y0Q ) + ( self.C[J] * ( PQ[J] * PF[J] - self.Y0 * YP[J] ) - self.S[J] * YF * XP[J] ) / ( PQ[J] + self.Y0Q )
                realPart = y * realPart + math.exp( -XQ )
        return realPart

    def baseParameterUnit( self, k ):
        """
        Return the name of a parameter.

        Parameters
        ---------
        k : int
            parameter number.

        """
        if k == 0:
            return self.yUnit
        return self.xUnit


