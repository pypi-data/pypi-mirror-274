import pybind11
from distutils.core import setup, Extension
from distutils import ccompiler
from setuptools import find_packages

cpp_args = [ ]
print("Compiler is: ", ccompiler.get_default_compiler())
sfc_module = Extension(
    'ImageObject',
    sources=['ImageObject.cpp','pybind11.cpp'],
  
    include_dirs=[
      pybind11.get_include(False),
      pybind11.get_include(True ),
    ],
    language='c++',
    extra_compile_args=cpp_args)


setup(
    name='ImageObject',
    version='1.14',
    description='Python package for image object operations',
    ext_modules=[sfc_module],
    author='Lei Wang',
    author_email='leiwang@lsu.edu',
    packages=find_packages(),
    headers=['includes/ImageObject.h'],
    classifiers=[
    'Programming Language :: C++',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
