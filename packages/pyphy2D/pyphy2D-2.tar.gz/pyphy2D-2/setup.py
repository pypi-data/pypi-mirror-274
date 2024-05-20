from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import numpy

# Define Cython extension modules
extensions = [
    Extension("pyphy.collisions_c", ["pyphy/collisions_c.pyx"]),
    Extension("pyphy.resolveCollisions_c", ["pyphy/resolveCollisions_c.pyx"]),
]

setup(
    name='pyphy2D',
    version='2',
    author='Krishiv Goel',
    author_email='KrishivGoelXD@gmail.com',
    description='A 2D Rigid Body Physics Engine.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['pygame'],
    include_dirs=[numpy.get_include()]
)