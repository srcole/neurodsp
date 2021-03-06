"""NeuroDSP setup script."""

import os
from setuptools import setup, find_packages

# Get the current version number from inside the module
with open(os.path.join('neurodsp', 'version.py')) as vf:
    exec(vf.read())

# Copy in long description.
#  Note: this is a partial copy from the README
#    Only update here in coordination with the README, to keep things consistent.
long_description = \
"""
========
Neurodsp
========

A package for digital signal processing of neural time series.

Neurodsp contains several modules:

- burst : Detect bursting oscillators in neural signals
- filt : Filter data with bandpass, highpass, lowpass, or notch filters
- laggedcoherence : Estimate rhythmicity using the lagged coherence measure
- sim : Simulate bursting or stationary oscillators with brown noise
- spectral : Compute spectral domain features (PSD and 1/f slope, etc)
- swm : Identify recurrent patterns in a signal using sliding window matching
- timefrequency : Estimate instantaneous measures of oscillatory activity
"""

setup(
    name = 'neurodsp',
    version = __version__,
    description = 'Digital Signal Processing for Neural time series',
    long_description = long_description,
    author = 'The Voytek Lab',
    author_email = 'voyteklab@gmail.com',
    url = 'https://github.com/neurodsp-tools/neurodsp',
    packages = find_packages(),
    license = 'MIT',
    download_url = 'https://github.com/neurodsp-tools/neurodsp/releases',
    keywords = ['neuroscience', 'neural oscillations', 'time series analysis', 'spectral analysis', 'LFP'],
    install_requires = ['numpy', 'scipy', 'matplotlib', 'pandas'],
    tests_require = ['pytest'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
        ]
)
