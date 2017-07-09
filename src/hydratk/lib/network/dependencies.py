# -*- coding: utf-8 -*-
"""Library module dependency definitions
.. module:: lib.network.dependencies
   :platform: Unix
   :synopsis: Library core module dependency definitions
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>
"""

import hydratk.lib.system.config as syscfg
from sys import version_info
from platform import python_implementation
from os import environ

dep_modules = {
    'hydratk': {
        'min-version': '0.5.0',
        'package': 'hydratk'
    },
    'cassandra': {
        'min-version': '3.7.0',
        'package': 'cassandra-driver',
        'optional': True
    },
    'lxml': {
        'min-version': '3.3.3',
        'package': 'lxml'
    },
    'paho.mqtt': {
        'min-version': '1.2',
        'package': 'paho-mqtt',
        'optional': True
    },
    'paramiko': {
        'min-version': '1.16.0',
        'package': 'paramiko'
    },
    'pycurl': {
        'min-version': '7.19.5.1',
        'package': 'pycurl'
    },
    'pyexcel': {
        'min-version': '0.2.0',
        'package': 'pyexcel',
        'optional': True
    },
    'pyexcel_xlsx': {
        'min-version': '0.1.0',
        'package': 'pyexcel-xlsx',
        'optional': True
    },
    'pyexcel_ods3': {
        'min-version': '0.1.1',
        'package': 'pyexcel-ods3',
        'optional': True
    },
    'pymongo': {
        'min-version': '3.3.0',
        'package': 'pymongo',
        'optional': True
    },
    'proton': {
        'min-version': '0.10',
        'package': 'python-qpid-proton',
        'optional': True
    },
    'pytz': {
        'min-version': '2016.6.1',
        'package': 'pytz'
    },
    'redis': {
        'min-version': '2.10.5',
        'package': 'redis',
        'optional': True
    },
    'requests': {
        'min-version': '2.11.1',
        'package': 'requests'
    },
    'requests_ntlm': {
        'min-version': '0.3.0',
        'package': 'requests-ntlm'
    },
    'selenium': {
        'min-version': '2.46.1',
        'package': 'selenium',
        'optional': True
    },
    'simplejson': {
        'min-version': '3.8.2',
        'package': 'simplejson'
    },
    'tftpy': {
        'min-version': '0.6.1',
        'package': 'tftpy'
    }
}


def get_dependencies():
    """Method returns dependent modules

    Args:  
       none        

    Returns:
       dict          

    """

    major, minor = version_info[0], version_info[1]

    if (major == 2):
        dep_modules['jsonrpclib'] = {'min-version': '0.1.7', 'package': 'jsonrpclib'}
        dep_modules['MySQLdb'] = {'min-version': '1.2.3', 'package': 'MySQL-python', 'optional': True}
        dep_modules['ldap'] = {'min-version': '2.4.25', 'package': 'python-ldap'}
        dep_modules['scapy'] = {'min-version': '2.3.1', 'package': 'scapy'}
        if (minor == 6):
            dep_modules['stompest'] = {'min-version': '2.1.6', 'package': 'stompest', 'optional': True}
        else:
            dep_modules['stompest'] = {'min-version': '2.2.5', 'package': 'stompest', 'optional': True}
        dep_modules['suds'] = {'min-version': '0.4',    'package': 'suds'}
    else:
        dep_modules['jsonrpclib'] = {'min-version': '0.2.8', 'package': 'jsonrpclib-pelix'}
        dep_modules['MySQLdb'] = {'min-version': '1.3.7', 'package': 'mysqlclient', 'optional': True}
        dep_modules['ldap'] = {'min-version': '2.4.25', 'package': 'pyldap'}
        dep_modules['scapy'] = {'min-version': '0.18', 'package': 'scapy-python3'}
        dep_modules['stompest'] = {'min-version': '2.2.5', 'package': 'stompest', 'optional': True}
        dep_modules['suds'] = {'min-version': '1.3.2.0', 'package': 'suds-py3'}

    if (python_implementation() != 'PyPy'):
        dep_modules['psycopg2'] = {'min-version': '2.4.5', 'package': 'psycopg2', 'optional': True}
        dep_modules['pymssql'] = {'min-version': '2.1.3', 'package': 'pymssql', 'optional': True}
        if ('ORACLE_HOME' in environ):
            dep_modules['cx_Oracle'] = {'min-version': '5.1.3', 'package': 'cx_Oracle', 'optional': True}
        if ('JAVA_HOME' in environ):
            dep_modules['jpype'] = {'min-version': '0.6.1', 'package': 'JPype1', 'optional': True}
    else:
        dep_modules['psycopg2cffi'] = {'min-version': '2.7.4', 'package': 'psycopg2cffi', 'optional': True}
        dep_modules['pymssql'] = {'min-version': '2.1.2', 'package': 'pymssql', 'optional': True}
        if ('ORACLE_HOME' in environ):
            dep_modules['cx_Oracle'] = {'min-version': '0.1', 'package': 'cx-oracle-on-ctypes', 'optional': True}

    return dep_modules


def _uninstall():
    """Method returns additional uninstall data 

    Args:            
       none

    Returns:
       tuple: list (files), dict (modules)     

    """

    files = [
        '{0}/hydratk/java'.format(syscfg.HTK_VAR_DIR)
    ]
    mods = get_dependencies()

    return files, mods
