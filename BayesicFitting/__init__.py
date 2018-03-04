#
#  This file is part of the BayesicFitting package.
#
#  BayesicFitting is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as
#  published by the Free Software Foundation, either version 3 of
#  the License, or (at your option) any later version.
#
#  BayesicFitting is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  The GPL3 license can be found at <http://www.gnu.org/licenses/>.
#
"""
Provides fitter functions.

Import into BayesicFitting itself all classe that are directly usable.
I.e. leave out the base classes and helper classes.

TBC: How much time does this take. Everything is translated ??

"""

from .source.AmoebaFitter import AmoebaFitter
from .source.AnnealingAmoeba import AnnealingAmoeba
from .source.ArctanModel import ArctanModel
from .source.BSplinesModel import BSplinesModel
from .source.BaseFitter import BaseFitter
from .source.BaseModel import BaseModel
from .source.BracketModel import BracketModel
from .source.CauchyErrorDistribution import CauchyErrorDistribution
from .source.CauchyPrior import CauchyPrior
from .source.ChebyshevPolynomialModel import ChebyshevPolynomialModel
from .source.CombiModel import CombiModel
from .source.ConstantModel import ConstantModel
from .source.ConvergenceError import ConvergenceError
from .source.CrossEngine import CrossEngine
from .source.CurveFitter import CurveFitter
from .source.Engine import Engine
from .source.ErrorDistribution import ErrorDistribution
from .source.EtalonDriftModel import EtalonDriftModel
from .source.EtalonModel import EtalonModel
from .source.ExpModel import ExpModel
from .source.Explorer import Explorer
from .source.ExponentialPrior import ExponentialPrior
from .source.Fitter import Fitter
from .source.FixedModel import FixedModel
#from .source.FreeShape2dModel import FreeShape2dModel
#from .source.FreeShapeModel import FreeShapeModel
from .source.GalileanEngine import GalileanEngine
from .source.GaussErrorDistribution import GaussErrorDistribution
from .source.GaussModel import GaussModel
from .source.GaussPrior import GaussPrior
from .source.GenGaussErrorDistribution import GenGaussErrorDistribution
from .source.GibbsEngine import GibbsEngine
from .source.HarmonicModel import HarmonicModel
from .source.HyperParameter import HyperParameter
from .source.ImageAssistant import ImageAssistant
from .source.IterationPlotter import IterationPlotter
from .source.IterativeFitter import IterativeFitter
from .source.JeffreysPrior import JeffreysPrior
from .source.Kernel2dModel import Kernel2dModel
from .source.KernelModel import KernelModel
from .source.LaplaceErrorDistribution import LaplaceErrorDistribution
from .source.LaplacePrior import LaplacePrior
from .source.LevenbergMarquardtFitter import LevenbergMarquardtFitter
from .source.LinearModel import LinearModel
from .source.LogFactorial import logFactorial
from .source.LorentzModel import LorentzModel
from .source.MaxLikelihoodFitter import MaxLikelihoodFitter
from .source.Model import Model
from .source.MonteCarlo import MonteCarlo
from .source.NestedSampler import NestedSampler
from .source.NoiseScale import NoiseScale
from .source.NonLinearModel import NonLinearModel
#from .source.OrderEngine import OrderEngine
from .source.PadeModel import PadeModel
from .source.PoissonErrorDistribution import PoissonErrorDistribution
from .source.PolySineAmpModel import PolySineAmpModel
from .source.PolySurfaceModel import PolySurfaceModel
from .source.PolynomialDynamicModel import PolynomialDynamicModel
from .source.PolynomialModel import PolynomialModel
from .source.PowerLawModel import PowerLawModel
from .source.PowerModel import PowerModel
from .source.Prior import Prior
from .source.ProductModel import ProductModel
from .source.QRFitter import QRFitter
from .source.RandomEngine import RandomEngine
from .source.RobustShell import RobustShell
from .source.Sample import Sample
from .source.SampleList import SampleList
from .source.ScaledErrorDistribution import ScaledErrorDistribution
## import all fitters inside ScipyFitter
from .source.ScipyFitter import *
from .source.SincModel import SincModel
from .source.SineAmpModel import SineAmpModel
from .source.SineDriftModel import SineDriftModel
from .source.SineModel import SineModel
from .source.SineSplineDriftModel import SineSplineDriftModel
from .source.SineSplineModel import SineSplineModel
from .source.SplinesModel import SplinesModel
from .source.StartEngine import StartEngine
from .source.StepEngine import StepEngine
from .source.SurfaceSplinesModel import SurfaceSplinesModel
from .source.UniformPrior import UniformPrior
from .source.VoigtModel import VoigtModel

from .source.Formatter import formatter
from .source.Formatter import formatter_init
from .source.Plotter import plotFit
from .source.Tools import printclass
from .source import Tools
#from .source import bspline
#from .source import splinelab

#from .source.bsplines.bspline import bspline
#from .source.bsplines.splinelab import splinelab

from .source.kernels.Biweight import Biweight
from .source.kernels.CosSquare import CosSquare
from .source.kernels.Cosine import Cosine
from .source.kernels.Gauss import Gauss
from .source.kernels.Huber import Huber
from .source.kernels.Kernel import Kernel
from .source.kernels.Lorentz import Lorentz
from .source.kernels.Parabola import Parabola
from .source.kernels.Sinc import Sinc
from .source.kernels.Triangle import Triangle
from .source.kernels.Tricube import Tricube
from .source.kernels.Triweight import Triweight
from .source.kernels.Uniform import Uniform

