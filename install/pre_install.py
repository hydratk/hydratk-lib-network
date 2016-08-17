# -*- coding: utf-8 -*-

from install.config import config as cfg
import install.command as cmd
from sys import version_info
from time import sleep
from os import system
from pkgutil import find_loader

def run_pre_install(argv):   
    
    requires = cfg['modules']
    
    if (cmd.is_install_cmd(argv)):        
     
        print('**************************************') 
        print('*     Running pre-install tasks      *')    
        print('**************************************')            
    
        for task in cfg['pre_tasks']:
            print('\n*** Running task: {0} ***\n'.format(task))
            requires = globals()[task](requires)        
    
    return requires  

def version_update(requires):
    
    major, minor = version_info[0], version_info[1]
    
    cfg['modules'].append('lxml>=3.3.3')
    cfg['modules'].append('pyexcel-ods3>=0.1.1')
    cfg['modules'].append('paramiko>=1.16.0')
    cfg['modules'].append('psycopg2>=2.4.5')
    cfg['modules'].append('pycurl>=7.19.5.1')
    cfg['modules'].append('selenium>=2.46.1')    

    if (major == 3):
        cfg['libs']['mysqlclient>=1.3.7'] = cfg['libs']['MySQL-python>=1.2.3']
        cfg['libs']['pyldap>=2.4.25'] = cfg['libs']['python-ldap>=2.4.25']  
        
    return requires                    

def install_libs_from_repo(requires):       
    
    pckm = cmd.get_pck_manager()[0]
    
    if (version_info[0] == 2):
        inst = ['MySQL-python>=1.2.3', 'python-ldap>=2.4.25']
    else:   
        inst = ['mysqlclient>=1.3.7', 'pyldap>=2.4.25'] 
    
    libs = cfg['libs']    
    for key in libs.keys():
        if (key in requires or key in inst):
            lib_inst = []
            if ('repo' in libs[key]):
                lib_inst += libs[key]['repo']
            if (pckm in libs[key]):
                lib_inst += libs[key][pckm]
            for lib in lib_inst:
                cmd.install_pck(pckm, lib)
                
    return requires
                
def install_pip(requires):
    
    major, minor = version_info[0], version_info[1]   
    
    system('pip install lxml>=3.3.3')
    requires.append('lxml>=3.3.3')
    system('pip install pyexcel-ods3>=0.1.1')
    requires.append('pyexcel-ods3>=0.1.1')
    system('pip install paramiko>=1.16.0')
    requires.append('paramiko>=1.16.0')
    system('pip install psycopg2>=2.4.5')
    requires.append('psycopg2>=2.4.5')
    system('pip install pycurl>=7.19.5.1')
    requires.append('pycurl>=7.19.5.1')
    system('pip install selenium>=2.46.1')
    requires.append('selenium>=2.46.1')    
    
    if (major == 2):
        system('pip install httplib2>=0.9.1')
        system('pip install MySQL-python>=1.2.3')
        system('pip install python-ldap>=2.4.25')
        system('pip install scapy>=2.3.1')
        system('pip install stompest>=2.1.6')
        system('pip install suds>=0.4')
        system('pip install tftpy>=0.6.2')       
    else:   
        if (find_loader('httplib2') == None):
            system('pip install git+https://github.com/httplib2/httplib2.git@master#egg=httplib2')
        system('pip install mysqlclient>=1.3.7') 
        system('pip install pyldap>=2.4.25') 
        system('pip install scapy-python3>=0.18') 
        system('pip install suds-py3>=1.3.2.0')                    
        if (find_loader('tftpy') == None):
            system('pip install git+https://github.com/ZuljinSBK/tftpy.git@master#egg=tftpy') 
            
    return requires                      
                
def install_java(requires):       
    
    if (cmd.getenv('JAVA_HOME') == None):
        print ('Java has not been detected. If you want to use HydraTK Java bridge, install Java first.')
        sleep(5)
    else:           
        module = 'JPype1>=0.6.1'
        requires.append(module)
        system('pip install {0}'.format(module))        
        
    return requires

def install_oracle(requires):       
     
    if (cmd.getenv('ORACLE_HOME') == None):
        print ('Oracle has not been detected. If you want to use HydraTK Oracle client, install Oracle first.')
        sleep(5)
    else:
        module = 'cx_Oracle>=5.1.3'
        requires.append(module)
        
        pckm = cmd.get_pck_manager()[0]
        lib_inst = []
        libs = cfg['libs']
        if ('repo' in libs[module]):
            lib_inst += libs[module]['repo']
        if (pckm in libs[module]):
            lib_inst += libs[module][pckm]
        for lib in lib_inst:
            cmd.install_pck(pckm, lib)          
        
        system('pip install {0}'.format(module))                           
     
    return requires  