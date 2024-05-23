from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'mvlearnPanorama implements MVC algorithms with GPU acceleration and memory optimization for large datasets'
LONG_DESCRIPTION = 'A package for with implementations for several MVC algorithms using PyTorch and minibatching. The package inlcudes implementations for these algorithms: multi-view k-means clustering, multi-view spherical k-means clustering, multi-view k-means with mini-batch, multi-view spherical k-means with mini-batch, multi-view spectral clustering, and multi-view coregularization spectral clustering.'

# Setting up
setup(
    name="mvlearnPanorama",
    version=VERSION,
    author="QCRI (Vrunda Sukhadia)",
    author_email="<sukhadiavrunda@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['torch', 'joblib', 'numpy', 'scikit-learn'],
    keywords=['multi-view', 'clustering', 'mvc', 'mvlearn'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)