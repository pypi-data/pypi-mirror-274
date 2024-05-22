# setup.py
import os
import numpy as np
from os.path import join
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(name="htrfnwe.HTC_v4",sources=["HTC_v4.pyx"], include_dirs=[np.get_include()]),
    Extension(name="htrfnwe.NWE_v5",sources=["NWE_v5.pyx"], include_dirs=[np.get_include()]),
    Extension(name="htrfnwe.VS_v4",sources=["VS_v4.pyx"], include_dirs=[np.get_include()]),
]

setup(
    include_dirs=[np.get_include()],
    name="htrfnwe",
    version="0.6",
    description="A package with multiple Cython programs for technical analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Litesh",
    author_email="liteshi55@gmail.com",
    url="https://github.com/Liteshi55/htrfnwe",
    packages=["htrfnwe"],
    setup_requires=['numpy','scikit-learn','Cython','setuptools'],
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3", 'boundscheck': False, 'wraparound': False}),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Cython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)