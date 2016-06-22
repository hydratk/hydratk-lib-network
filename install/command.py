# -*- coding: utf-8 -*-
"""This code is a part of Hydra toolkit

.. module:: install.command
   :platform: Unix
   :synopsis: Module for common commands used in installation tasks
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from subprocess import call, Popen, PIPE
from os import environ
import cmd

def get_pck_manager():
    """Method detects package managers

    Args:

    Returns:
       list: managers
    
    """    
    
    pck_managers = ['apt-get', 'yum']
    
    pckm = []
    for pck in pck_managers:     
        if (is_installed(pck)):
            pckm.append(pck) 
    
    return pckm

def is_installed(app):
    """Method checks if application is installed

    Args:
       app (str): application

    Returns:
       bool: result
    
    """      
    
    cmd = ['which', app]
    proc = Popen(cmd, stdout=PIPE)
    out = proc.communicate() 
    
    result = True if (len(out[0]) > 0) else False
    return result    

def install_pck(pckm, pck):
    """Method installs package

    Args:
       pckm (str): package manager, apt-get|yum
       pck (str): package name

    Returns:
       void
    
    """     
    
    print('Installing package: {0}'.format(pck))
    
    if (pckm == 'apt-get'):
        cmd = 'apt-get -y install {0}'.format(pck)
    elif (pckm == 'yum'):
        cmd = 'yum -y install {0}'.format(pck)
        
    if (call(cmd, shell=True) != 0):
        print('Failed to install package {0}'.format(pck)) 
        
def getenv(name):
    """Method gets environment variable

    Args:
       name (str): variable name

    Returns:
       str: variable value
    
    """      
    
    value = environ[name] if (name in environ) else None
    return value                                                                    
        
def compile_java_class(dir, file, classpath=None):   
    """Method compiles Java class

    Args:
       dir (str): source directory
       file (str): Java filename
       classpath (str): classpath used in compilation

    Returns:
       void
    
    """      
    
    print('Compiling {0}'.format(file))
    
    if (classpath != None):
        cmd = 'javac -cp {0} {1}'.format(classpath, file)
    else:
        cmd = 'javac {0}'.format(file)
        
    if (call(cmd, cwd=dir, shell=True) != 0):
        print('Failed to compile {0}'.format(file))         