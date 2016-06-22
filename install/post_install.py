# -*- coding: utf-8 -*-
"""This code is a part of Hydra toolkit

.. module:: install.post_install
   :platform: Unix
   :synopsis: Module for post-install tasks
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from config import config as cfg
import command as cmd
from os import path

def run_post_install(requires):
    """Method runs post-install tasks

    Args:
       requires (list): installed required modules

    Returns:
       void
    
    """     
    
    print('**************************************') 
    print('*     Running post-install tasks     *')    
    print('**************************************')
    
    tasks = cfg['post_tasks']
    if ('JPype1>=0.6.1' not in requires):
        del tasks[tasks.index('compile_java_classes')]
    
    for task in tasks:
        print('\n*** Running task: {0} ***\n'.format(task))
        globals()[task]()     

def compile_java_classes():
    """Method compiles Java classes

    Args:

    Returns:
       void
    
    """    
    
    dir = cfg['java']['dir'] 
    if (path.exists(dir)):
        classpath = cfg['java']['classpath']
        for file in cfg['java']['files']:
            cmd.compile_java_class(dir, file, classpath)                                 