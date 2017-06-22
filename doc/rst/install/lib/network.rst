.. install_lib_network:

Network
=======

You have 2 options how to install Network library.

Package
^^^^^^^

Install it via Python package managers PIP or easy_install.

  .. code-block:: bash
  
     $ sudo pip install --no-binary :all: hydratk-lib-network
     
  .. code-block:: bash
  
     $ sudo easy_install hydratk-lib-network
     
  .. note::
  
     PIP needs option --no-binary to run setup.py install.
     Otherwise it runs setup.py bdist_wheel.   
     
  .. Use PIP option --install-option="--profile=p1,p2" to install only Python dependent modules included
     in requested profiles. Offered profiles are basic, bridge, db, jms. Full profile is installed by default.   
     Not supported for easy_install because it doesn't provide custom options.        

Source
^^^^^^

Download the source code from GitHub or PyPi and install it manually.
Full PyPi URL contains MD5 hash, adapt sample code.

  .. code-block:: bash
  
     $ git clone https://github.com/hydratk/hydratk-lib-network.git
     $ cd ./hydratk-lib-network
     $ sudo python setup.py install
     
  .. code-block:: bash
  
     $ wget https://pypi.python.org/pypi/hydratk-lib-network -O hydratk-lib-network.tar.gz
     $ tar -xf hydratk-lib-network.tar.gz
     $ cd ./hydratk-lib-network
     $ sudo python setup.py install
     
  .. Use option --profile=p1,p2 to install only Python dependent modules included
     in requested profiles. Offered profiles are basic, bridge, db, jms. Full profile is installed by default.      
     
  .. note::
  
     Source is distributed with Sphinx (not installed automatically) documentation in directory doc. 
     Type make html to build local documentation however is it recommended to use up to date online documentation.     
     
Requirements
^^^^^^^^^^^^

Several python modules are used.
These modules will be installed automatically, if not installed yet.

* hydratk
* cassandra-driver
* cx_Oracle
* JPype1
* jsonrpclib
* lxml
* MySQL-python
* mysqlclient
* paho-mqtt
* paramiko
* pymongo
* pymssql
* psycopg2
* pycurl
* pyexcel
* pyexcel-xlsx
* pyexcel-ods3
* python-ldap
* python-ntlm
* python-qpid-proton
* redis
* requests
* requests_ntlm
* scapy
* selenium
* simplejson
* stompest
* suds
* tftpy

Modules cx_Oracle, lxml, MySQL-python, paramiko, pymssql, psycopg2, pycurl, python-ldap, selenium require several 
libraries which will be installed via Linux package managers, if not installed yet.
Module cassandra-driver installation takes longer time (not so fast as other modules).

  .. note ::
     
     Installation for Python2.6 has some differences.
     Module stompest is installed in version 2.1.6 (newer versions has no 2.6 support)

  .. note ::
  
     Installation for Python3 has some differences.
     Module jsonrpclib-pelix is installed instead of jsonrpclib.
     Module mysqlclient is installed instead of MySQL-python.
     Module pyldap is installed instead of python-ldap.
     Module scapy-python3 is installed instead of scapy.
     Module suds-py3 is installed instead of suds.
     Module tftpy is not installed from PyPi but from https://github.com/ZuljinSBK/tftpy.git@master#egg=tftpy
     
  .. note ::
  
     Installation for PyPy has some differences.
     Module cx-oracle-on-ctypes is installed instead of cx_Oracle.
     Module psycopg2cffi is installed instead of psycopg2.
     Module pymssql is not installed from PyPi but from https://github.com/dholth/pymssql.git
     Module JPype1 is not supported and not installed.     

cx_Oracle

* apt-get: libaio1, libaio-dev
* yum: libaio     
    
lxml

* apt-get: python-lxml, libxml2-dev, libxslt1-dev
* yum: python-lxml, libxml2-devel, libxslt-devel

MySQL-python

* apt-get: python-mysqldb, libmysqlclient-dev
* yum: mysql-devel   

paramiko

* apt-get: libffi-dev, libssl-dev
* yum: libffi-devel, openssl-devel

pymssql

* apt-get: freetds-dev
* yum: freetds, freetds-devel

psycopg2

* apt-get: python-psycopg2, libpq-dev
* yum: python-psycopg2, postgresql-devel   

pycurl

* apt-get: python-pycurl, libcurl2-openssl-dev
* yum: python-pycurl, libcurl-devel

python-ldap

* apt-get: libldap2-dev, libsasl2-dev, libssl-dev
* yum: openldap-devel

selenium

* apt-get: libfontconfig
* yum: fontconfig 

Oracle client is not bundled with library and must be installed individually.
Setup script checks if environment variable ORACLE_HOME is set. If not the module cx_Oracle is excluded.
When you install Oracle, you can update library and cx_Oracle will be installed.

Java virtual machine is not bundled with library and must be installed individually.
Setup script checks if environment variable JAVA_HOME is set. If not the module JPype1 is excluded.
When you install JVM, you can update library and JPype1 including jar files will be installed. 
    
Library offers following profiles.

* basic - hydratk, jsonrpclib, lxml, paramiko, pycurl, python-ldap, python-ntlm, requests, requests_ntlm, scapy, simplejson, suds, tftpy
* bridge - basic profile, JPype1, pyexcel, pyexcel-xlsx, pyexcel-ods3, selenium
* db - basic profile, cassandra-driver, cx_Oracle, MySQL-python, mysqlclient, pymongo, pymssql, psycopg2, redis
* jms - basic profile, paho-mqtt, python-qpid-proton, stompest
* full - everything    
    
Installation
^^^^^^^^^^^^

See installation example for Linux based on Debian distribution, Python 2.7. 

  .. note::
  
     The system is clean therefore external libraries will be also installed (several MBs will be downloaded)
     You can see strange log messages which are out of hydratk control. 
     
  .. code-block:: bash
  
     **************************************
     *     Running pre-install tasks      *
     **************************************
     
     *** Running task: version_update ***
     Oracle has not been detected ($ORACLE_HOME is not set). If you want to use HydraTK Oracle client, install Oracle first.
     Java has not been detected ($JAVA_HOME is not set). If you want to use HydraTK Java bridge, install Java first.
     *** Running task: install_libs ***
     Checking libcurl4-openssl-dev...FAILED
        Unable to locate package libcurl4-openssl-dev
     Checking python-mysqldb...FAILED
        Unable to locate package python-mysqldb
     Checking libmysqlclient-dev...FAILED
        Unable to locate package libmysqlclient-dev
     Checking libssl-dev...FAILED
        Unable to locate package libssl-dev
     Checking libsasl2-dev...FAILED
        Unable to locate package libsasl2-dev
     Checking libfontconfig...OK
     Checking libffi-dev...FAILED
        Unable to locate package libffi-dev
     Checking python-pycurl...FAILED
        Unable to locate package python-pycurl
     Checking freetds-dev...FAILED
        Unable to locate package freetds-dev
     Checking libxslt1-dev...OK
     Checking libpq-dev...FAILED
        Unable to locate package libpq-dev
     Checking python-psycopg2...FAILED
        Unable to locate package python-psycopg2
     Checking libldap2-dev...FAILED
        Unable to locate package libldap2-dev
     Checking python-lxml...OK
     Checking libxml2-dev...OK
     Installing package libcurl4-openssl-dev
     Installing package python-mysqldb
     Installing package libmysqlclient-dev
     Installing package libssl-dev
     Installing package libsasl2-dev
     Installing package libffi-dev
     Installing package python-pycurl
     Installing package freetds-dev
     Installing package libpq-dev
     Installing package python-psycopg2
     Installing package libldap2-dev
     
     *** Running task: install_modules ***
     Module hydratk already installed with version 0.5.0rc1
     Installing module cassandra-driver>=3.7.0
     pip install "cassandra-driver>=3.7.0"
     Module lxml already installed with version 3.4.0
     Installing module paho-mqtt>=1.2
     pip install "paho-mqtt>=1.2"
     Installing module paramiko>=1.16.0
     pip install "paramiko>=1.16.0"
     Upgrading module pycurl to version 7.19.5.1
     Installing module pyexcel>=0.2.0
     pip install "pyexcel>=0.2.0"
     Installing module pyexcel-xlsx>=0.1.0
     pip install "pyexcel-xlsx>=0.1.0"
     Installing module pyexcel-ods3>=0.1.1
     pip install "pyexcel-ods3>=0.1.1"
     Installing module pymongo>=3.3.0
     pip install "pymongo>=3.3.0"
     Installing module python-qpid-proton>=0.10
     pip install "python-qpid-proton>=0.10"
     Module pytz already installed with version 2017.2
     Installing module redis>=2.10.5
     pip install "redis>=2.10.5"
     Installing module requests>=2.11.1
     pip install "requests>=2.11.1"
     Installing module requests-ntlm>=0.3.0
     pip install "requests-ntlm>=0.3.0"
     Installing module selenium>=2.46.1
     pip install "selenium>=2.46.1"
     Installing module jsonrpclib>=0.1.7
     pip install "jsonrpclib>=0.1.7"
     Module MySQL-python already installed with version 1.2.3
     Installing module python-ldap>=2.4.25
     pip install "python-ldap>=2.4.25"
     Installing module scapy>=2.3.1
     pip install "scapy>=2.3.1"
     Module simplejson already installed with version 3.11.1
     Installing module stompest>=2.2.5
     pip install "stompest>=2.2.5"
     Installing module suds>=0.4
     pip install "suds>=0.4"
     Installing module tftpy>=0.6.2
     pip install "tftpy>=0.6.2"
     Module psycopg2 already installed with version 2.5.4
     Installing module pymssql>=2.1.3
     pip install "pymssql>=2.1.3"
     
     running install
     running bdist_egg
     running egg_info
     creating src/hydratk_lib_network.egg-info
     writing src/hydratk_lib_network.egg-info/PKG-INFO
     writing top-level names to src/hydratk_lib_network.egg-info/top_level.txt
     writing dependency_links to src/hydratk_lib_network.egg-info/dependency_links.txt
     writing manifest file 'src/hydratk_lib_network.egg-info/SOURCES.txt'
     reading manifest file 'src/hydratk_lib_network.egg-info/SOURCES.txt'
     reading manifest template 'MANIFEST.in'
     writing manifest file 'src/hydratk_lib_network.egg-info/SOURCES.txt'
     installing library code to build/bdist.linux-x86_64/egg
     running install_lib
     running build_py
     creating build
     creating build/lib.linux-x86_64-2.7
     creating build/lib.linux-x86_64-2.7/hydratk
     ...
     creating build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/PKG-INFO -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/SOURCES.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/dependency_links.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/not-zip-safe -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/top_level.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     creating dist
     creating 'dist/hydratk_lib_network-0.2.1rc1-py2.7.egg' and adding 'build/bdist.linux-x86_64/egg' to it
     removing 'build/bdist.linux-x86_64/egg' (and everything under it)
     Processing hydratk_lib_network-0.2.1rc1-py2.7.egg
     creating /usr/local/lib/python2.7/dist-packages/hydratk_lib_network-0.2.1rc1-py2.7.egg
     Extracting hydratk_lib_network-0.2.1rc1-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding hydratk-lib-network 0.2.1rc1 to easy-install.pth file
     Installed /usr/local/lib/python2.7/dist-packages/hydratk_lib_network-0.2.1rc1-py2.7.egg
     Processing dependencies for hydratk-lib-network==0.2.1rc1
     Finished processing dependencies for hydratk-lib-network==0.2.1rc1
     
     **************************************
     *     Running post-install tasks     *
     **************************************

     *** Running task: copy_files ***

     Creating directory /var/local/hydratk/java
     Copying file src/hydratk/lib/network/dbi/java/DBClient.java to /var/local/hydratk/java
     Copying file src/hydratk/lib/network/jms/java/javaee.jar to /var/local/hydratk/java
     Copying file src/hydratk/lib/network/jms/java/JMSClient.java to /var/local/hydratk/java               
     
     *** Running task: compile_java_classes ***

     Compiling DBClient.java
     Compiling JMSClient.java         
     
Application installs following (paths depend on your OS configuration)

* modules in /usr/local/lib/python2.7/dist-packages/hydratk-lib-network-0.2.1-py2.7egg 
* application folder in /var/local/hydratk/java with files javaee.jar, DBClient.java, DBClient.class, JMSClient.java, JMSClient.class, JMSMessage.class       
     
Run
^^^

When installation is finished you can run the application.

Check hydratk-lib-network module is installed.

  .. code-block:: bash
  
     $ pip list | grep hydratk-lib-network

     hydratk-lib-network (0.2.1)    
     
Upgrade
=======

Use same procedure as for installation. Use command option --upgrade for pip, easy_install, --force for setup.py.

Uninstall
=========    

Run command htkuninstall. Use option -y if you want to uninstall also dependent Python modules (for advanced user).            