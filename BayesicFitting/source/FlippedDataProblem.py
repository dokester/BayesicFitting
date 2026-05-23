import numpy as numpy

from .MultipleOutputProblem import MultipleOutputProblem

__author__ = "Do Kester"
__year__ = 2026
__license__ = "GPL3"
__version__ = "3.3.0"
__url__ = "https://www.bayesicfitting.nl"
__status__ = "Alpha"

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
#  *    2018 - 2026 Do Kester

class FlippedDataProblem( MultipleOutputProblem ):
    """
    A FlippedDataProblem is a problem for solving double star orbits, 
    where there is ambiguity of the stars A and B,  in a (small) number 
    of datapoints. 

    In some double stars, it is not  always clear which star is the main
    star A and which is the secundary B, resulting in ambiguity in the 
    angular direction. 

    Directions with misidentification in A and B, should be flipped.
    In spherical coordinates (rho,phi) should be (rho,-phi). 
    In rectangular coordinates (x,y) should be replaced by (-x,-y).

    Attributes
    ----------
    nflip : int
        actual number of flipped datapoints
    flipped : list of int
        indices of flipped datapoints.

    Attributes from Problem
    -----------------------
    model, xdata, ydata, weights, partype

    Author :         Do Kester

    """

    #  *************************************************************************
    def __init__( self, model=None, xdata=None, ydata=None, weights=None, 
                  accuracy=None, nflip=0, copy=None ):
        """
        Problem Constructor.

        Parameters
        ----------
        model : Model
            the model to be solved. One with multiple outputs: model.ndout > 1
        xdata : array_like
            independent variable
        ydata : array_like
            dependent variable. shape = (len(xdata), model.ndout)
        weights : array_like or None
            weights associated with ydata: shape = as xdata or as ydata
        accuracy : float or ndarray of shape (ndata,)
            accuracy scale for the datapoints
            all the same or one for each data point
        nflip : int
            Maximum number of datapoints that can be flipped.
        copy : Problem
            to be copied

        """
        super( ).__init__( model=model, xdata=xdata, ydata=ydata, weights=weights,
                           accuracy=accuracy, copy=copy )

        self.maxflip = nflip

    def copy( self ):
        """
        Copy.

        """
        return FlippedDataProblem( copy=self, nflip=self.maxflip )

    def residuals( self, param, mockdata=None ) :
        """
        Returns residuals in a flattened array.
        """
        if self.maxflip == 0 :
            self.flipped = []
            return super().residuals( param, mockdata=mockdata )

        if mockdata is None :
            mockdata = self.result( param )

        res = mockdata - self.ydata
        rsm = numpy.hypot( res[:,0], res[:,1] )
        rep = mockdata + self.ydata
        rsp = numpy.hypot( rep[:,0], rep[:,1] )
        q = numpy.where( rsp < rsm )[0]
        if len( q ) > self.maxflip :
            q = numpy.random.choice( q, self.maxflip, replace=False )
            
        res[q,:] = rep[q,:]

        self.flipped = q
        
        return res

    def getFlippedData( self ) :
        """
        Return the corrected datapoints.
        """
        data = self.ydata.copy()
        data[self.flipped,:] *= -1
        return data

    def __getattr__( self, name ) :
        """
        Return value belonging to attribute with name.

        Parameters
        ----------
        name : string
            name of the attribute
        """
        if name == 'nflip' :
            return len( self.flipped )

        return super( ).__getattr__( name )

    #  *****TOSTRING***********************************************************
    def baseName( self ):
        """ 
        Returns a string representation of the model.
        """
        return "FlippedDataProblem"



