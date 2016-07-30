# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from sys import argv
from install.pre_install import run_pre_install
from install.post_install import run_post_install

with open("README.rst", "r") as f:
    readme = f.read()
    
requires = run_pre_install(argv)       
    
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",   
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",    
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython", 
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Utilities"
]                        
          
setup(
      name='hydratk-lib-network',
      version='0.1.0',
      description='Clients/API for many network protocols and technologies',
      long_description=readme,
      author='Petr Rašek, HydraTK team',
      author_email='team@hydratk.org',
      url='http://libraries.hydratk.org/network',
      license='BSD',
      packages=find_packages('src'),
      install_requires=requires,
      package_dir={'' : 'src'},
      classifiers=classifiers,
      zip_safe=False
     )        

run_post_install(argv, requires)