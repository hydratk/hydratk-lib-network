# -*- coding: utf-8 -*-
"""This code is a part of Hydra toolkit

.. module:: install.pre_install
   :platform: Unix
   :synopsis: Module for pre-install tasks
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from config import config as cfg
import command as cmd
from time import sleep

def run_pre_install():
    """Method runs pre-install tasks

    Args:

    Returns:
       tuple: requires (list), data_files (list)
    
    """    
    
    print('**************************************')
    print('*    HydraTK Network installation    *')
    print('**************************************')    

    requires = cfg['modules']
    data_files = []
     
    print('**************************************') 
    print('*     Running pre-install tasks      *')    
    print('**************************************')
    
    for task in cfg['pre_tasks']:
        print('\n*** Running task: {0} ***\n'.format(task))
        
        if (task == 'install_java'):
            requires, data_files = globals()[task](requires, data_files)
        elif (task == 'install_oracle'):
            requires = globals()[task](requires)
        else:
            globals()[task](requires)          
    
    return (requires, data_files)  

def install_libs_from_repo(requires):
    """Method installs libraries from repositories

    Args:
       requires (list): required libraries

    Returns:
       void
    
    """        
    
    pckm = cmd.get_pck_manager()[0]
    
    libs = cfg['libs']
    for key in libs.keys():
        if (key in requires):
            lib_inst = []
            if (libs[key].has_key('repo')):
                lib_inst += libs[key]['repo']
            if (libs[key].has_key(pckm)):
                lib_inst += libs[key][pckm]
            for lib in lib_inst:
                cmd.install_pck(pckm, lib)  
                
def install_java(requires, data_files):
    """Method handles Java installation
    
    Currently JPype1 is excluded from installation if Java is missing

    Args:
       requries (list): required libraries
       data_files (list): data files

    Returns:
       tuple: requires (list), data_files (list), exclude (list)
    
    """        
    
    module = 'JPype1>=0.6.1'
    if (cmd.getenv('JAVA_HOME') != None):
        for file in cfg['files'][module]:
            data_files.append(file)      
    else:
        print ('Java has not been detected. If you want to use HydraTK Java bridge, install Java first.')
        sleep(5)
        del requires[requires.index(module)]             

    return (requires, data_files)

def install_oracle(requires):
    """Method handles Oracle installation
    
    Currently cx_Oracle is excluded from installation if Oracle is missing

    Args:
       requires (list): required libraries

    Returns:
       tuple: requires (list)
    
    """        
    
    module = 'cx_Oracle>=5.1.3'   
    if (cmd.getenv('ORACLE_HOME') == None):
        print ('Oracle has not been detected. If you want to use HydraTK Oracle client, install Oracle first.')
        sleep(5)
        del requires[requires.index(module)]                           
     
    return requires  