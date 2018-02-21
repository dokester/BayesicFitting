from setuptools import setup, find_packages


__version__ = '0.9'

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
        'future'
#        'bspline>=0.1.1'         # from John Foster and Juha Jeronen at github
    ],
    license='LICENSE.txt',
    description='A Python Toolbox for Bayes-enhanched fitting.',
    keywords = ['Bayesian', 'modeling', 'evidence', 'statistics', 'analysis',
                'optimization','nested sampling'],
#    packages=['BayesicFitting/source', 'BayesicFitting/source/kernels', 'BayesicFitting/test', 'BayesicFitting/examples'],
#    packages = find_packages( exclude=('test',) ),
    packages=['BayesicFitting', 'BayesicFitting/source', 'BayesicFitting/test', 'BayesicFitting/examples'],
    classifiers = [
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research/DataAnalysis",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Scientific/Engineering"
    ],
    include_package_data=True
)
