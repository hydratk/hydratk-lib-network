# -*- coding: utf-8 -*-

from config import config as cfg
import command as cmd
from time import sleep

def run_pre_install(argv):   
    
    requires = cfg['modules']
    
    if (cmd.is_install_cmd(argv)):        
     
        print('**************************************') 
        print('*     Running pre-install tasks      *')    
        print('**************************************')
    
        for task in cfg['pre_tasks']:
            print('\n*** Running task: {0} ***\n'.format(task))
        
            if (task in ['install_java', 'install_oracle']):
                requires = globals()[task](requires)
            else:
                globals()[task](requires)          
    
    return requires  

def install_libs_from_repo(requires):       
    
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
                
def install_java(requires):       
    
    if (cmd.getenv('JAVA_HOME') == None):
        print ('Java has not been detected. If you want to use HydraTK Java bridge, install Java first.')
        sleep(5)
        del requires[requires.index('JPype1>=0.6.1')]             

    return requires

def install_oracle(requires):       
     
    if (cmd.getenv('ORACLE_HOME') == None):
        print ('Oracle has not been detected. If you want to use HydraTK Oracle client, install Oracle first.')
        sleep(5)
        del requires[requires.index('cx_Oracle>=5.1.3')]                           
     
    return requires  