# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from install.pre_install import run_pre_install
from install.post_install import run_post_install

with open("README.rst", "r") as f:
    readme = f.readlines()
    
requires, data_files = run_pre_install()      
    
classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",   
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",    
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython",    
    "Programming Language :: Python :: Implementation :: PyPy",    
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
      zip_safe=False,
      data_files=data_files
     )        

run_post_install(requires)