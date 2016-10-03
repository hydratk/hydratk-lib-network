# -*- coding: utf-8 -*-

from install.config import config as cfg
import install.command as cmd
from sys import version_info
from time import sleep
from pkgutil import find_loader
from platform import python_implementation

def run_pre_install(argv):   
    
    if (cmd.is_install_cmd(argv)):        
     
        print('**************************************') 
        print('*     Running pre-install tasks      *')    
        print('**************************************')            
    
        for task in cfg['pre_tasks']:
            print('\n*** Running task: {0} ***\n'.format(task))
            globals()[task]()         

def version_update():
    
    major, minor = version_info[0], version_info[1]  

    if (major == 2):
        cfg['modules'].append('jsonrpclib>=0.1.7')
        cfg['modules'].append('MySQL-python>=1.2.3')
        cfg['modules'].append('python-ldap>=2.4.25')
        cfg['modules'].append('scapy>=2.3.1')
        if (minor == 6):
            cfg['modules'].append('stompest==2.1.6')
        else:
            cfg['modules'].append('stompest>=2.2.5')        
        cfg['modules'].append('suds>=0.4')        
        cfg['modules'].append('tftpy>=0.6.2')
    else:
        cfg['modules'].append('jsonrpclib-pelix>=0.2.8')
        cfg['modules'].append('mysqlclient>=1.3.7')
        cfg['modules'].append('pyldap>=2.4.25')
        cfg['modules'].append('scapy-python3>=0.18')
        cfg['modules'].append('stompest>=2.2.5')
        cfg['modules'].append('suds-py3>=1.3.2.0')
        if (find_loader('tftpy') == None):
            cfg['modules'].append('git+https://github.com/ZuljinSBK/tftpy.git@master#egg=tftpy')
            
        cfg['libs']['mysqlclient>=1.3.7'] = cfg['libs']['MySQL-python>=1.2.3']
        cfg['libs']['pyldap>=2.4.25'] = cfg['libs']['python-ldap>=2.4.25'] 
    
    if (python_implementation() != 'PyPy'):
        cfg['modules'].append('psycopg2>=2.4.5')
        cfg['modules'].append('pymssql>=2.1.3')
    else:
        cfg['modules'].append('psycopg2cffi>=2.7.4')           
        
    if (cmd.getenv('ORACLE_HOME') == None):
        print ('Oracle has not been detected ($ORACLE_HOME is not set). If you want to use HydraTK Oracle client, install Oracle first.')
        sleep(5)
    else:
        if (python_implementation() != 'PyPy'):
            cfg['modules'].append('cx_Oracle>=5.1.3')
        else:
            cfg['modules'].append('git+https://github.com/lameiro/cx_oracle_on_ctypes.git')
            cfg['libs']['git+https://github.com/lameiro/cx_oracle_on_ctypes.git'] = cfg['libs']['cx_Oracle>=5.1.3']        
      
    if (python_implementation() != 'PyPy'):  
        if (cmd.getenv('JAVA_HOME') == None):
            print ('Java has not been detected ($JAVA_HOME is not set). If you want to use HydraTK Java bridge, install Java first.')
            sleep(5)
        else: 
            cfg['modules'].append('JPype1>=0.6.1')                       

def install_libs_from_repo():       
    
    pckm = cmd.get_pck_manager()[0]
    
    libs, modules = cfg['libs'], cfg['modules']    
    for key in libs.keys():
        if (key in modules):
            lib_inst = []
            if ('repo' in libs[key]):
                lib_inst += libs[key]['repo']
            if (pckm in libs[key]):
                lib_inst += libs[key][pckm]
            for lib in lib_inst:
                cmd.install_pck(pckm, lib)
                
def install_pip():  
           
    for module in cfg['modules']:
        cmd.install_pip(module)                                             