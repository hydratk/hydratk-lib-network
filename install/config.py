# -*- coding: utf-8 -*-

config = {
  'pre_tasks' : [
                 'version_update',
                 'install_libs_from_repo',
                 'install_pip',
                 'install_java',
                 'install_oracle'
                ],

  'post_tasks' : [  
                  'copy_files',
                  'compile_java_classes' 
                 ],
          
  'modules' : [   
               'hydratk',             
               'pyexcel>=0.2.0',
               'pyexcel-xlsx>=0.1.0',                                                                  
               'python-ntlm>=1.1.0', 
               'python-qpid-proton>=0.10',
               'pytz>=2016.6.1',                
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