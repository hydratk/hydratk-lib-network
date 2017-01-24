# -*- coding: utf-8 -*-
"""Library module dependency definitions
.. module:: lib.network.dependencies
   :platform: Unix
   :synopsis: Library core module dependency definitions
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>
"""

from sys import version_info
from platform import python_implementation
from os import environ

dep_modules = {
  'hydratk'       : {
                     'min-version' : '0.4.0',
                     'package'     : 'hydratk'
                    }, 
  'cassandra'     : {
                     'min-version' : '3.7.0',
                     'package'     : 'cassandra-driver'
                    },                
  'lxml'          : {
                     'min-version' : '3.3.3',
                     'package'     : 'lxml'
                    },
  'paho.mqtt'     : {
                     'min-version' : '1.2',
                     'package'     : 'paho-mqtt'
                    },
  'paramiko'      : {
                     'min-version' : '1.16.0',
                     'package'     : 'paramiko'
                    },    
  'pycurl'        : {
                     'min-version' : '7.19.5.1',
                     'package'     : 'pycurl'
                    },
  'pyexcel'       : {
                     'min-version' : '0.2.0',
                     'package'     : 'pyexcel'
                    },
  'pyexcel_xlsx'  : {
                     'min-version' : '0.1.0',
                     'package'     : 'pyexcel-xlsx'
                    },
  'pyexcel_ods3'  : {
                     'min-version' : '0.1.1',
                     'package'     : 'pyexcel-ods3'
                    },
  'pymongo'       : {
                     'min-version' : '3.3.0',
                     'package'     : 'pymongo'
                    },
  'proton'        : {
                     'min-version' : '0.10',
                     'package'     : 'python-qpid-proton'
                    },                                  
  'pytz'          : {
                     'min-version' : '2016.6.1',
                     'package'     : 'pytz'
                    },
  'redis'         : {
                     'min-version' : '2.10.5',
                     'package'     : 'redis'
                    },     
  'requests'      : {
                     'min-version' : '2.11.1',
                     'package'     : 'requests'
                    },
  'requests_ntlm' : {
                     'min-version' : '0.3.0',
                     'package'     : 'requests-ntlm'
                    },      
  'selenium'      : {
                     'min-version' : '2.46.1',
                     'package'     : 'selenium'
                  },
  'simplejson'    : {
                     'min-version' : '3.8.2',
                     'package'     : 'simplejson'
                    },  
  'tftpy'         : {
                     'min-version' : '0.6.1',
                     'package'     : 'tftpy'
                    }                                                                                                                                                                                                                           
}

def get_dep_modules():
    """Method returns dependent modules
        
    Args:  
       none        
           
    Returns:
       dict          
                
    """  
    
    major, minor = version_info[0], version_info[1] 
    
    if (major == 2):
        dep_modules['jsonrpclib']   = {'min-version' : '0.1.7',  'package' : 'jsonrpclib'}
        dep_modules['MySQLdb']      = {'min-version' : '1.2.3',  'package' : 'MySQL-python'}
        dep_modules['ldap']         = {'min-version' : '2.4.25', 'package' : 'python-ldap'}
        dep_modules['scapy']        = {'min-version' : '2.3.1',  'package' : 'scapy'}
        if (minor == 6):
            dep_modules['stompest'] = {'min-version' : '2.1.6','package' : 'stompest'}
        else:
            dep_modules['stompest'] = {'min-version' : '2.2.5','package' : 'stompest'}
        dep_modules['suds']         = {'min-version' : '0.4',    'package' : 'suds'}
    else:
        dep_modules['jsonrpclib']   = {'min-version' : '0.2.8',  'package' : 'jsonrpclib-pelix'}    
        dep_modules['MySQLdb']      = {'min-version' : '1.3.7',  'package' : 'mysqlclient'} 
        dep_modules['ldap']         = {'min-version' : '2.4.25', 'package' : 'pyldap'}
        dep_modules['scapy']        = {'min-version' : '0.18',   'package' : 'scapy-python3'}
        dep_modules['stompest']     = {'min-version' : '2.2.5',  'package' : 'stompest'}
        dep_modules['suds']         = {'min-version' : '1.3.2.0','package' : 'suds-py3'}
        
    if (python_implementation() != 'PyPy'):
        dep_modules['psycopg2']     = {'min-version' : '2.4.5',  'package' : 'psycopg2'}
        dep_modules['pymssql']      = {'min-version' : '2.1.3',  'package' : 'pymssql'}
        if ('ORACLE_HOME' in environ):
            dep_modules['cx_Oracle']= {'min-version' : '5.1.3',  'package' : 'cx_Oracle'}
        if ('JAVA_HOME' in environ):
            dep_modules['jpype']    = {'min-version' : '0.6.1',  'package' : 'JPype1'}            
    else:
        dep_modules['psycopg2cffi'] = {'min-version' : '2.7.4',  'package' : 'psycopg2cffi'}      
        if ('ORACLE_HOME' in environ):   
            dep_modules['cx_Oracle']= {'min-version' : '0.1',    'package' : 'cx-oracle-on-ctypes'}       
    
    return dep_modules

def _uninstall():
    """Method returns additional uninstall data 
        
    Args:            
       none
           
    Returns:
       list: files to delete    
                
    """            
        
    files = [
             '/var/local/hydratk/java'
            ]
            
    return files     