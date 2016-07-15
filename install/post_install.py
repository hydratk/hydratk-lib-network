# -*- coding: utf-8 -*-

from install.config import config as cfg
import install.command as cmd
from os import path

def run_post_install(argv, requires):  
    
    if (cmd.is_install_cmd(argv)):           
    
        print('**************************************') 
        print('*     Running post-install tasks     *')    
        print('**************************************')
    
        if ('JPype1>=0.6.1' in requires):
            for task in cfg['post_tasks']:
                print('\n*** Running task: {0} ***\n'.format(task))
                globals()[task]()     

def copy_files():  
    
    for file, dir in cfg['files'].items():        
        cmd.copy_file(file, dir) 

def compile_java_classes():    
    
    dir = cfg['java']['dir'] 
    if (path.exists(dir)):
        classpath = cfg['java']['classpath']
        for file in cfg['java']['files']:
            cmd.compile_java_class(dir, file, classpath)                                 