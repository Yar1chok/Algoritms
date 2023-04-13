from setuptools import setup
from Cython.Build import cythonize


setup(
    name='dynamic_array',
    ext_modules=cythonize("dynamic_array.pyx"),
)
