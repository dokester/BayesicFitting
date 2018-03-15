from setuptools import setup, find_packages


__version__ = '1.0.2'

setup(
    name='BayesicFitting',
    version=__version__,
    author='Do Kester',
    author_email='dokester@home.nl',
    install_requires=[
        'numpy >= 1.9',
        'matplotlib >= 2.0',
        'scipy >= 1.0',
        'astropy >= 2.0',
# A modified version of bspline is added to BayesicFitting
#        'bspline>=0.1.1',         # from John Foster and Juha Jeronen at github
        'future'
    ],
    license='LICENSE.txt',
    description='A Python Toolbox for Bayes-enhanched fitting.',
    keywords = ['Bayesian', 'modeling', 'evidence', 'statistics', 'analysis',
                'optimization','nested sampling', 'fitting'],
    packages=['BayesicFitting', 'BayesicFitting/source', 'BayesicFitting/source/kernels',
              'BayesicFitting/test', 'BayesicFitting/examples'],
    classifiers = [
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Scientific/Engineering"
    ],
    include_package_data=True
)
