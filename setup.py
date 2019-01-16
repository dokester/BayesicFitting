from setuptools import setup, find_packages

__version__ = '2.1.0'

def readme():
    with open( 'README.md' ) as f:
        return f.read()

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
    description='A Python Toolbox for Bayesian fitting.',
    long_description=readme(),
    long_description_content_type='markdown',
    url="https://github.com/dokester/BayesicFitting",
    keywords = ['Bayesian', 'modeling', 'evidence', 'statistics', 'analysis',
                'optimization','nested sampling', 'fitting'],
    packages=['BayesicFitting', 'BayesicFitting/source', 'BayesicFitting/source/kernels',
              'BayesicFitting/test', 'BayesicFitting/examples'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Scientific/Engineering"
    ],
    include_package_data=True
)
