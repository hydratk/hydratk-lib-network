# -*- coding: utf-8 -*-

config = {
  'pre_tasks' : [
                 'version_update',
                 'install_libs_from_repo',
                 'install_pip'
                ],

  'post_tasks' : [  
                  'copy_files',
                  'compile_java_classes' 
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
             'src/hydratk/lib/network/jms/java/JMSClient.java' : '/var/local/hydratk/java', 
             'src/hydratk/lib/network/jms/java/javaee.jar'     : '/var/local/hydratk/java',
             'src/hydratk/lib/network/dbi/java/DBClient.java'  : '/var/local/hydratk/java' 
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
           },                           
}