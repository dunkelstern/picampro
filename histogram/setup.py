import setuptools
from distutils.core import setup, Extension

module = Extension(
    'rpi_display_histogram',
    sources = ['histogram.c'],
    include_dirs=['/opt/vc/include'],
    library_dirs=['/opt/vc/lib'],
    libraries=['bcm_host'],
)

setup(
    name = 'RPI Display Histogram',
    version = '1.0',
    description = 'Create a histogram from display contents',
    packages=setuptools.find_packages(),
    ext_modules = [module]
)
