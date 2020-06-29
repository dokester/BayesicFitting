
import numpy as numpy
import math
from . import Tools
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from .Sample import Sample
from .SampleList import SampleList

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


class SampleMovie( object ):
    """
    SampleMovie produces a movie (mp4) from a SampleList

    This class is provided as an example to vary upon.

    ===========
    MovieWriter
    ===========

    This example uses a MovieWriter directly to grab individual frames and write
    them to a file. This avoids any event loop integration, but has the advantage
    of working with even the Agg backend. This is not recommended for use in an
    interactive setting.

    """

    def __init__( self, samplelist, filename="samplemovie.mp4", problem=None, kpar=[0,1] ) :
        """
        Constructor.

        The constructor produces the movie.

        Parameters
        ----------
        samplelist : SampleList
            to make the movie from
        filename : str
            name of the mp4 movie
        problem : Problem
            the problem that produced the samplelist
        kpar : list of 2 ints
            indices of the parameters to plot
        """

        bakend = matplotlib.get_backend()       ## save present backend to restore

        matplotlib.use("Agg")					## need to use this one to make a movie

        FFMpegWriter = animation.writers[ 'ffmpeg' ]
        metadata = dict( title='Sample Movie', artist='BayesicFitting',
                comment='Movie support!' )
        writer = FFMpegWriter( fps=30, metadata=metadata )

        fig = plt.figure()

        if problem is not None :
            ld, lm, l1, l2, l4 = plt.plot( [], [], 'b*', [], [], 'g-',
                                           [], [], 'y.', [], [], 'r.', [], [], 'k+' )
            xd = problem.xdata
            yd = problem.ydata
            xm = numpy.linspace( numpy.min( xd ), numpy.max( xd ), 10 * len( xd ), dtype=float )
            # xd -= 5.0
            yd -= 9.0
            xn = xm # - 5.0
        else :
            l1, l2, l4 = plt.plot( [], [], 'y.', [], [], 'r.', [], [], 'k+' )

        smpl = samplelist[0]
        k0 = kpar[0]
        k1 = kpar[1]
        pr0 = smpl.model.priors[k0]
        plt.xlim( pr0.lowLimit, pr0.highLimit )
        plt.xlabel( smpl.model.getParameterName( k0 ) )
        pr1 = smpl.model.priors[k1]
        plt.ylim( pr1.lowLimit, pr1.highLimit )
        plt.ylabel( smpl.model.getParameterName( k1 ) )

        mx = smpl.logW
        ns = len( samplelist )
        LOG100 = math.log( 100 )
        with writer.saving( fig, filename, 100 ):
            for i in range( ns ):
                s = samplelist[i]
                if problem is not None :
                    ym = s.model.result( xm, s.parameters ) - 9.0
                    ld.set_data( xd, yd )
                    lm.set_data( xn, ym )
                x1 = []
                y1 = []
                x4 = []
                y4 = []
                if samplelist[i].logW > mx :
                    mx = samplelist[i].logW
                if samplelist[i].logW < ( mx - LOG100 ) :
                    return
                for sample in samplelist[:i] :
                    if sample.logW < ( mx - LOG100 ) :
                        x1 = x1 + [sample.allpars[k0]]
                        y1 = y1 + [sample.allpars[k1]]
                    else :
                        x4 = x4 + [sample.allpars[k0]]
                        y4 = y4 + [sample.allpars[k1]]

                l1.set_data( x1, y1 )
                l4.set_data( x4, y4 )

                x2 = []
                y2 = []

                for sample in samplelist[i:] :
                    if sample.start > i : continue
                    x2 = x2 + [sample.allpars[k0]]
                    y2 = y2 + [sample.allpars[k1]]
                l2.set_data( x2, y2 )

#                print( i, s.id, s.parent, s.start, s.logW, mx, len(x1), len(x2), len(x4) )
                writer.grab_frame( )

        matplotlib.use( bakend )            ## reset to what it was

