.. install_lib_network:

Network
=======

You have 2 options how to install Network library.

Package
^^^^^^^

Install it via Python package managers PIP or easy_install.
Filename after PIP download contains version, adapt sample code.

  .. code-block:: bash
  
     $ sudo pip download hydratk-lib-network
     $ sudo pip install hydratk-lib-network.tar.gz 
     
  .. code-block:: bash
  
     $ sudo easy_install hydratk-lib-network
     
  .. note::
  
     Use PIP to install package from local file for correct installation.
     When installed from remote repository, PIP sometimes doesn't call setup.py.     

Source
^^^^^^

Download the source code from GitHub or PyPi and install it manually.
Full PyPi URL contains MD5 hash, adapt sample code.

  .. code-block:: bash
  
     $ git clone https://github.com/hydratk/hydratk-lib-network.git
     $ cd ./hydratk-lib-network
     $ sudo python setup.py install
     
  .. code-block:: bash
  
     $ wget https://pypi.python.org/pypihydratk-lib-network -O hydratk-lib-network.tar.gz
     $ tar -xf hydratk-lib-network.tar.gz
     $ cd ./hydratk-lib-network
     $ sudo python setup.py install
     
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
     Modules JPype1, pymssql are not supported and not installed.

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
    
Installation
^^^^^^^^^^^^

See installation example for Linux based on Debian distribution. 

  .. note::
  
     The system is clean therefore external libraries will be also installed (several MBs will be downloaded)
     You can see strange log messages which are out of hydratk control. 
     
  .. code-block:: bash
  
     **************************************
     *     Running pre-install tasks      *
     **************************************

     *** Running task: install_libs_from_repo ***

     Installing package: python-lxml
     Installing package: libxml2-dev
     Installing package: libxslt1-dev
     Installing package: libfontconfig
     Installing package: libffi-dev
     Installing package: libssl-dev
     Installing package: libaio1
     Installing package: libaio-dev
     Installing package: mysql-devel
     Installing package: python-mysqldb
     Installing package: libmysqlclient-dev
     Installing package: libldap2-dev
     Installing package: libsasl2-dev
     Installing package: libssl-dev
     Installing package: python-pycurl
     Installing package: libcurl4-openssl-dev
     Installing package: python-psycopg2
     Installing package: libpq-dev

     *** Running task: install_java ***

     Java has not been detected. If you want to use HydraTK Java bridge, install Java first.

     *** Running task: install_oracle ***

     Oracle has not been detected. If you want to use HydraTK Oracle client, install Oracle first.
     
     running install
     running bdist_egg
     running egg_info
     writing requirements to src/hydratk_lib_network.egg-info/requires.txt
     writing src/hydratk_lib_network.egg-info/PKG-INFO
     writing top-level names to src/hydratk_lib_network.egg-info/top_level.txt
     writing dependency_links to src/hydratk_lib_network.egg-info/dependency_links.txt
     reading manifest file 'src/hydratk_lib_network.egg-info/SOURCES.txt'
     reading manifest template 'MANIFEST.in'
     writing manifest file 'src/hydratk_lib_network.egg-info/SOURCES.txt'
     installing library code to build/bdist.linux-x86_64/egg
     running install_lib
     running build_py
     creating build
     creating build/lib.linux-x86_64-2.7
     creating build/lib.linux-x86_64-2.7/hydratk
     copying src/hydratk/__init__.py -> build/lib.linux-x86_64-2.7/hydratk
     byte-compiling build/bdist.linux-x86_64/egg/hydratk/__init__.py to __init__.pyc
     byte-compiling build/bdist.linux-x86_64/egg/hydratk/lib/__init__.py to __init__.pyc
     creating build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/PKG-INFO -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/SOURCES.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/dependency_links.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/not-zip-safe -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/requires.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/top_level.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     creating dist
     creating 'dist/hydratk_lib_network-0.1.0a0.dev1-py2.7.egg' and adding 'build/bdist.linux-x86_64/egg' to it
     removing 'build/bdist.linux-x86_64/egg' (and everything under it)
     Processing hydratk_lib_network-0.1.0a0.dev1-py2.7.egg
     creating /usr/local/lib/python2.7/dist-packages/hydratk_lib_network-0.1.0a0.dev1-py2.7.egg
     Extracting hydratk_lib_network-0.1.0a0.dev1-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding hydratk-lib-network 0.1.0a0.dev1 to easy-install.pth file
     Installed /usr/local/lib/python2.7/dist-packages/hydratk_lib_network-0.1.0a0.dev1-py2.7.egg
     Processing dependencies for hydratk-lib-network==0.1.0a0.dev1
     
     Searching for tftpy>=0.6.2
     Reading https://pypi.python.org/simple/tftpy/
     Best match: tftpy 0.6.2
     Downloading https://pypi.python.org/packages/7d/a5/e246b93d0996264f80c54af706bda111b1547cef6def52ecb05183263af7/tftpy-0.6.2.tar.gz#md5=199c48ca8ea8975170596eb5da109514
     Processing tftpy-0.6.2.tar.gz
     Installed /usr/local/lib/python2.7/dist-packages/tftpy-0.6.2-py2.7.egg

     Searching for suds>=0.4
     Reading https://pypi.python.org/simple/suds/
     Best match: suds 0.4
     Downloading https://pypi.python.org/packages/bc/d6/960acce47ee6f096345fe5a7d9be7708135fd1d0713571836f073efc7393/suds-0.4.tar.gz#md5=b7502de662341ed7275b673e6bd73191
     Processing suds-0.4.tar.gz
     Installed /usr/local/lib/python2.7/dist-packages/suds-0.4-py2.7.egg

     Searching for stompest>=2.1.6
     Reading https://pypi.python.org/simple/stompest/
     Best match: stompest 2.1.6
     Downloading https://pypi.python.org/packages/1b/95/54360fd21ec73d411b03034ee8c6f776773dd00b779f8fefa1da34b1569f/stompest-2.1.6.tar.gz#md5=3c7de396491a60d1ff6c56903945b8ec
     Processing stompest-2.1.6.tar.gz
     Installed /usr/local/lib/python2.7/dist-packages/stompest-2.1.6-py2.7.egg

     Searching for selenium>=2.46.1
     Reading https://pypi.python.org/simple/selenium/
     Best match: selenium 2.53.5
     Downloading https://pypi.python.org/packages/41/ff/d77fd45739a2290da74ba314182fcfbe98b4e617e89b973bc5c667444334/selenium-2.53.5.tar.gz#md5=c7e40c360d73e267234e166f252f574c
     Processing selenium-2.53.5.tar.gz
     Installed /usr/local/lib/python2.7/dist-packages/selenium-2.53.5-py2.7.egg

     Searching for scapy>=2.3.1
     Reading https://pypi.python.org/simple/scapy/
     Best match: scapy 2.3.2
     Downloading https://pypi.python.org/packages/6d/72/c055abd32bcd4ee6b36ef8e9ceccc2e242dea9b6c58fdcf2e8fd005f7650/scapy-2.3.2.tar.gz#md5=b8ca06ca3b475bd01ba6cf5cdc5619af
     Processing scapy-2.3.2.tar.gz
     Installed /usr/local/lib/python2.7/dist-packages/scapy-2.3.2-py2.7.egg

     Searching for python-qpid-proton>=0.10
     Reading https://pypi.python.org/simple/python-qpid-proton/
     Best match: python-qpid-proton 0.12.2
     Downloading https://pypi.python.org/packages/6f/2a/822b799025c9b02ff259dc1048f1ce227e85eac7099d851acc68b2a3c0ab/python-qpid-proton-0.12.2.tar.gz#md5=b826a41b2da27cb056cc46fde3aa6182
     Processing python-qpid-proton-0.12.2.tar.gz
     Installed /usr/local/lib/python2.7/dist-packages/python_qpid_proton-0.12.2-py2.7-linux-x86_64.egg

     Searching for python-ntlm>=1.1.0
     Reading https://pypi.python.org/simple/python-ntlm/
     Best match: python-ntlm 1.1.0
     Downloading https://pypi.python.org/packages/10/0e/e7d7e1653852fe440f0f66fa65d14dd21011d894690deafe4091258ea855/python-ntlm-1.1.0.tar.gz#md5=c1b036401a29dd979ee56d48a2267686
     Processing python-ntlm-1.1.0.tar.gz
     Installed /usr/local/lib/python2.7/dist-packages/python_ntlm-1.1.0-py2.7.egg

     Searching for python-ldap>=2.4.25
     Reading https://pypi.python.org/simple/python-ldap/
     Best match: python-ldap 2.4.25
     Downloading https://pypi.python.org/packages/9b/1a/f2bc7ebf2f0b21d78d7cc2b5c283fb265397912cd63c4b53c83223ebcac9/python-ldap-2.4.25.tar.gz#md5=21523bf21dbe566e0259030f66f7a487
     Processing python-ldap-2.4.25.tar.gz
     Installed /usr/local/lib/python2.7/dist-packages/python_ldap-2.4.25-py2.7-linux-x86_64.egg

     Searching for pyexcel-ods3>=0.1.1
     Reading https://pypi.python.org/simple/pyexcel-ods3/
     Best match: pyexcel-ods3 0.2.0
     Downloading https://pypi.python.org/packages/e0/84/8ce15c7b4ea392fb560cd43a6de0cd8b5f4803832eb26e5b141c34e03da5/pyexcel-ods3-0.2.0.zip#md5=1985c2f3ceb9337b1bcc9503660b8d45
     Processing pyexcel-ods3-0.2.0.zip
     Installed /usr/local/lib/python2.7/dist-packages/pyexcel_ods3-0.2.0-py2.7.egg

     Searching for pyexcel-xlsx>=0.1.0
     Reading https://pypi.python.org/simple/pyexcel-xlsx/
     Best match: pyexcel-xlsx 0.2.0
     Downloading https://pypi.python.org/packages/0e/79/14739d317451e8ceed934075c49541336d8c3d0ddad53e946bffdb47ac6d/pyexcel-xlsx-0.2.0.zip#md5=9139b9bdcaf2f185abab31337a40cf05
     Processing pyexcel-xlsx-0.2.0.zip
     Installed /usr/local/lib/python2.7/dist-packages/pyexcel_xlsx-0.2.0-py2.7.egg

     Searching for pyexcel>=0.2.0
     Reading https://pypi.python.org/simple/pyexcel/
     Best match: pyexcel 0.2.2
     Downloading https://pypi.python.org/packages/ae/bb/b4f31f93be6a283816c89fa6fb2608bca58aac7aeeb4df9d46da956389d8/pyexcel-0.2.2.zip#md5=a939ea1841343d533fb31332dcb66ccf
     Processing pyexcel-0.2.2.zip
     Installed /usr/local/lib/python2.7/dist-packages/pyexcel-0.2.2-py2.7.egg

     Searching for pycurl>=7.19.5.1
     Reading https://pypi.python.org/simple/pycurl/
     Best match: pycurl 7.43.0
     Downloading https://pypi.python.org/packages/12/3f/557356b60d8e59a1cce62ffc07ecc03e4f8a202c86adae34d895826281fb/pycurl-7.43.0.tar.gz#md5=c94bdba01da6004fa38325e9bd6b9760
     Processing pycurl-7.43.0.tar.gz
     Installed /usr/local/lib/python2.7/dist-packages/pycurl-7.43.0-py2.7-linux-x86_64.egg

     Searching for paramiko>=1.16.0
     Reading https://pypi.python.org/simple/paramiko/
     Best match: paramiko 2.0.1
     Downloading https://pypi.python.org/packages/b5/dd/cc2b8eb360e3db2e65ad5adf8cb4fd57493184e3ce056fd7625e9c387bfa/paramiko-2.0.1.tar.gz#md5=c00d63b34dcf74649216bdc8875e1ebe
     Processing paramiko-2.0.1.tar.gz
     Installed /usr/local/lib/python2.7/dist-packages/paramiko-2.0.1-py2.7.egg

     Searching for jsonlib2>=1.5.2
     Reading https://pypi.python.org/simple/jsonlib2/
     Best match: jsonlib2 1.5.2
     Downloading https://pypi.python.org/packages/0e/1d/745b4e69ca0710215f7291ebbdfcdc95896dec7e196312b29d5a7c606038/jsonlib2-1.5.2.tar.gz#md5=f650c6979c04ed128e76edaa9ba50323
     Processing jsonlib2-1.5.2.tar.gz
     Installed /usr/local/lib/python2.7/dist-packages/jsonlib2-1.5.2-py2.7-linux-x86_64.egg

     Searching for httplib2>=0.9.1
     Reading https://pypi.python.org/simple/httplib2/
     Best match: httplib2 0.9.2
     Downloading https://pypi.python.org/packages/ff/a9/5751cdf17a70ea89f6dde23ceb1705bfb638fd8cee00f845308bf8d26397/httplib2-0.9.2.tar.gz#md5=bd1b1445b3b2dfa7276b09b1a07b7f0e
     Processing httplib2-0.9.2.tar.gz
     Installed /usr/local/lib/python2.7/dist-packages/ezodf-0.3.2-py2.7.egg

     Searching for pyexcel-io>=0.1.0
     Reading https://pypi.python.org/simple/pyexcel-io/
     Best match: pyexcel-io 0.2.0
     Downloading https://pypi.python.org/packages/43/39/8f2cea9f97ca057da858565347070ee1aa0f748f1232f00d9370c7ab5ff2/pyexcel-io-0.2.0.zip#md5=2f2ea9e662e1ad541dea96f8259fb9f8
     Processing pyexcel-io-0.2.0.zip

     Searching for psycopg2==2.5.4
     Best match: psycopg2 2.5.4
     Adding psycopg2 2.5.4 to easy-install.pth file

     Using /usr/lib/python2.7/dist-packages
     Searching for MySQL-python==1.2.3
     Best match: MySQL-python 1.2.3
     Adding MySQL-python 1.2.3 to easy-install.pth file

     Using /usr/lib/python2.7/dist-packages
     Searching for lxml==3.4.0
     Best match: lxml 3.4.0
     Adding lxml 3.4.0 to easy-install.pth file

     Using /usr/lib/python2.7/dist-packages
     Finished processing dependencies for hydratk-lib-network==0.1.0a0.dev1  
     
     **************************************
     *     Running post-install tasks     *
     **************************************  
     
     only if Java is installed
     *** Running task: copy_files ***

     Creating directory /var/local/hydratk/java
     Copying file src/hydratk/lib/network/jms/java/JMSClient.java to /var/local/hydratk/java  
     Copying file src/hydratk/lib/network/jms/java/javaee.jar to /var/local/hydratk/java 
     Copying file src/hydratk/lib/network/dbi/java/DBClient.java to /var/local/hydratk/java                  
     
     *** Running task: compile_java_classes ***

     Compiling DBClient.java
     Compiling JMSClient.java         
     
Application installs following (paths depend on your OS configuration)

* modules in /usr/local/lib/python2.7/dist-packages/hydratk-lib-network-0.1.0-py2.7egg 
* application folder in /var/local/hydratk/java with files javaee.jar, DBClient.java, DBClient.class, JMSClient.java, JMSClient.class, JMSMessage.class       
     
Run
^^^

When installation is finished you can run the application.

Check hydratk-lib-network module is installed.

  .. code-block:: bash
  
     $ pip list | grep hydratk
     
     hydratk (0.3.0a0.dev1)
     hydratk-lib-network (0.1.0)       