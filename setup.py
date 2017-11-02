# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from sys import argv, version_info
from os import path, environ
from subprocess import call
from time import sleep
from pkgutil import find_loader
from platform import python_implementation
import hydratk.lib.install.task as task

with open("README.rst", "r") as f:
    readme = f.read()
    
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",   
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",    
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython", 
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Utilities"
]     

def version_update(cfg):
    
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
        cfg['modules'].append('git+https://github.com/dholth/pymssql.git')
        
        cfg['libs']['psycopg2cffi>=2.7.4'] = cfg['libs']['psycopg2>=2.4.5']
        cfg['libs']['git+https://github.com/dholth/pymssql.git'] = cfg['libs']['pymssql>=2.1.3']          
        
    if ('ORACLE_HOME' not in environ):
        print ('Oracle has not been detected ($ORACLE_HOME is not set). If you want to use HydraTK Oracle client, install Oracle first.')
        sleep(5)
    else:
        if (python_implementation() != 'PyPy'):
            cfg['modules'].append('cx_Oracle>=5.1.3')
        else:
            cfg['modules'].append('git+https://github.com/lameiro/cx_oracle_on_ctypes.git')
            cfg['libs']['git+https://github.com/lameiro/cx_oracle_on_ctypes.git'] = cfg['libs']['cx_Oracle>=5.1.3']        
      
    if (python_implementation() != 'PyPy'):  
        if ('JAVA_HOME' not in environ):
            print ('Java has not been detected ($JAVA_HOME is not set). If you want to use HydraTK Java bridge, install Java first.')
            sleep(5)
        else: 
            cfg['modules'].append('JPype1>=0.6.1')  

def compile_java_classes(cfg):    
    
    dir = cfg['java']['dir'] 
    if (path.exists(dir)):
        classpath = cfg['java']['classpath']
        for file in cfg['java']['files']:
            print('Compiling {0}'.format(file))  
            if (classpath != None):
                command = 'javac -cp {0} {1}'.format(classpath, file)
            else:
                command = 'javac {0}'.format(file)
            if (call(command, cwd=dir, shell=True) != 0):
                print('Failed to compile {0}'.format(file)) 

config = {
  'pre_tasks' : [
                 version_update,
                 task.install_libs,
                 task.install_modules
                ],

  'post_tasks' : [  
                  task.copy_files,
                  compile_java_classes 
                 ],
          
  'modules' : [   
               'hydratk', 
               'cassandra-driver>=3.7.0', 
               'lxml>=3.3.3',
               'paho-mqtt>=1.2',  
               'paramiko>=1.16.0',                              
               'pycurl>=7.19.5.1',           
               'pyexcel>=0.2.0',
               'pyexcel-xlsx>=0.1.0',
               'pyexcel-ods3>=0.1.1',  
               'pymongo>=3.3.0',                                                                               
               'python-qpid-proton>=0.10',
               'pytz>=2016.6.1',  
               'redis>=2.10.5', 
               'requests>=2.11.1',
               'requests-ntlm>=0.3.0',   
               'selenium>=2.46.1',                         
               'simplejson>=3.8.2'          
              ],
          
  'files' : {
             'data' : {
                       'src/hydratk/lib/network/jms/java/JMSClient.java' : '/var/local/hydratk/java', 
                       'src/hydratk/lib/network/jms/java/javaee.jar'     : '/var/local/hydratk/java',
                       'src/hydratk/lib/network/dbi/java/DBClient.java'  : '/var/local/hydratk/java'
                      } 
            },
          
  'libs' : {
            'cx_Oracle>=5.1.3'    : {
                                     'apt-get' : [
                                                  'libaio1',
                                                  'libaio-dev'
                                                 ],
                                     'yum'     : [
                                                  'libaio'
                                                 ]
                                    },
            'lxml>=3.3.3'         : {
                                     'repo'    : [
                                                  'python-lxml'
                                                 ],
                                     'apt-get' : [
                                                  'libxml2-dev',
                                                  'libxslt1-dev'
                                                 ],
                                     'yum'     : [
                                                  'libxml2-devel',
                                                  'libxslt-devel'
                                                 ]
                                    },
            'MySQL-python>=1.2.3' : {
                                     'apt-get' : [
                                                  'python-mysqldb',
                                                  'libmysqlclient-dev'
                                                 ],
                                     'yum'     : [
                                                  'mysql-devel'
                                                 ]                                     
                                    },
            'paramiko>=1.16.0'    : {
                                     'apt-get' : [
                                                  'libffi-dev',
                                                  'libssl-dev'                                        
                                                 ],
                                     'yum'     : [
                                                  'libffi-devel',
                                                  'openssl-devel'
                                                 ]
                                    },
            'pymssql>=2.1.3'     : {
                                     'apt-get' : [
                                                  'freetds-dev'
                                                 ],
                                     'yum'     : [
                                                  'freetds',
                                                  'freetds-devel'
                                                 ]
                                    },              
            'psycopg2>=2.4.5'     : {
                                     'repo'    : [
                                                  'python-psycopg2'
                                                 ],
                                     'apt-get' : [
                                                  'libpq-dev'
                                                 ],
                                     'yum'     : [
                                                  'postgresql-devel'
                                                 ]
                                    },             
            'pycurl>=7.19.5.1'    : {
                                     'repo'    : [
                                                  'python-pycurl'
                                                 ],
                                     'apt-get' : [
                                                  'libcurl4-openssl-dev'
                                                 ],
                                     'yum'     : [
                                                  'libcurl-devel'
                                                 ]
                                    },
            'python-ldap>=2.4.25' : {
                                     'apt-get' : [
                                                  'libldap2-dev',
                                                  'libsasl2-dev',
                                                  'libssl-dev'
                                                 ],
                                     'yum'     : [
                                                  'openldap-devel'
                                                 ]
                                    },                      
            'selenium>=2.46.1'    : {
                                     'apt-get' : [
                                                  'libfontconfig'
                                                 ],
                                     'yum'     : [
                                                  'fontconfig'
                                                 ]
                                    }                
           },          
          
  'java' : {
            'dir'       : '/var/local/hydratk/java',
            'files'     : [
                           'DBClient.java', 
                           'JMSClient.java'
                          ],
            'classpath' : 'javaee.jar' 
           }                           
}    
    
task.run_pre_install(argv, config)                          
          
setup(
      name='hydratk-lib-network',
      version='0.2.1a.dev4',
      description='Clients/API for many network protocols and technologies',
      long_description=readme,
      author='Petr Rašek, HydraTK team',
      author_email='bowman@hydratk.org, team@hydratk.org',
      url='http://libraries.hydratk.org/network',
      license='BSD',
      packages=find_packages('src'),
      package_dir={'' : 'src'},
      classifiers=classifiers,
      zip_safe=False,
      keywords='hydratk,database,soap,rest,jms,java,gui',
      requires_python='>=2.6,!=3.0.*,!=3.1.*,!=3.2.*',
      platforms='Linux'
     )        

task.run_post_install(argv, config)