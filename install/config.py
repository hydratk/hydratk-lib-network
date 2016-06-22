# -*- coding: utf-8 -*-
"""This code is a part of Hydra toolkit

.. module:: install.config
   :platform: Unix
   :synopsis: Module with install config
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

config = {
  'pre_tasks' : [
                 'install_libs_from_repo',
                 'install_java',
                 'install_oracle'
                ],

  'post_tasks' : [  
                  'compile_java_classes' 
                 ],
          
  'modules' : [   
               'hydratk',
               'cx_Oracle>=5.1.3',
               'httplib2>=0.9.1',
               'JPype1>=0.6.1',
               'jsonlib2>=1.5.2',
               'lxml>=3.3.3',                
               'MySQL-python>=1.2.3', 
               'paramiko>=1.16.0',
               'psycopg2>=2.4.5',               
               'pycurl>=7.19.5.1',     
               'pyexcel>=0.2.0',
               'pyexcel-xlsx>=0.1.0',
               'pyexcel-ods3>=0.1.1',
               'python-ldap>=2.4.25',                                                     
               'python-ntlm>=1.1.0', 
               'python-qpid-proton>=0.10',              
               'scapy>=2.3.1',
               'selenium>=2.46.1',
               'stompest>=2.1.6', 
               'suds>=0.4', 
               'tftpy>=0.6.2'                       
              ],
          
  'files' : {
             'JPype1>=0.6.1' : [
                                ('/var/local/hydratk/java', ['src/hydratk/lib/network/jms/java/JMSClient.java']), 
                                ('/var/local/hydratk/java', ['src/hydratk/lib/network/jms/java/javaee.jar']),
                                ('/var/local/hydratk/java', ['src/hydratk/lib/network/dbi/java/DBClient.java'])
                               ]  
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
                                     'repo'    : [
                                                  'mysql-devel'
                                                 ],
                                     'apt-get' : [
                                                  'python-mysqldb',
                                                  'libmysqlclient-dev'
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
            'psycopg2>=2.4.5'     : {
                                     'repo'    : [
                                                  'python-psycopg2'
                                                 ],
                                     'apt-get' : [
                                                  'libpq-dev'
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
           },                           
}