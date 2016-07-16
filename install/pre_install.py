# -*- coding: utf-8 -*-

from install.config import config as cfg
import install.command as cmd
from sys import version_info
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

def version_update(requires):
    
    major, minor = version_info[0], version_info[1]
    
    if (major == 3):
        del cfg['modules'][cfg['modules'].index('stompest>=2.1.6')]
        cfg['modules'][cfg['modules'].index('MySQL-python>=1.2.3')] = 'mysqlclient>=1.3.7'
        cfg['libs']['mysqlclient>=1.3.7'] = cfg['libs']['MySQL-python>=1.2.3']
        cfg['modules'][cfg['modules'].index('python-ldap>=2.4.25')] = 'pyldap>=2.4.25'
        cfg['libs']['pyldap>=2.4.25'] = cfg['libs']['python-ldap>=2.4.25']
        cfg['modules'][cfg['modules'].index('scapy>=2.3.1')] = 'scapy-python3>=0.18'
        cfg['modules'][cfg['modules'].index('suds>=0.4')] = 'suds-py3>=1.3.2.0'

def install_libs_from_repo(requires):       
    
    pckm = cmd.get_pck_manager()[0]
    
    libs = cfg['libs']
    for key in libs.keys():
        if (key in requires):
            lib_inst = []
            if ('repo' in libs[key]):
                lib_inst += libs[key]['repo']
            if (pckm in libs[key]):
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