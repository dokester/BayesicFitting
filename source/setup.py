from setuptools import setup

__version__ = '0.9'

setup(
    name='BayesicFitting',
    version=__version__,
    author='Do Kester',
    author_email='dokester@home.nl',
    install_requires=[
        'python>=3.5',
        'numpy>=1.9',
        'matplotlib>=2.0.2',
        'scipy>=1.0.0',
        'astropy>=2.0.2',
        'bspline>=0.1.1'         # from John Foster and Juha Jeronen at github
    ],
    license='LICENSE.txt',
    description='A Python Toolbox for Bayes-enhanched fitting.',
    keywords = ['Bayesian', 'modeling', 'evidence', 'statistics', 'analysis',
                'optimization','nested sampling'],
    packages=['BayesicFitting'],
    classifiers = [
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research/DataAnalysis",
        "License :: GPL3"
    ]
)
