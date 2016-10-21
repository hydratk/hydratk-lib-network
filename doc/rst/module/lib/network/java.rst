.. _module_lib_bridge_java:

Java
====

This sections contains module documentation of java module.

java
^^^^

Module provides class JavaBridge which implements bridge to JVM using external module
`JPype1 <http://jpype.readthedocs.io/en/latest/>`_ in version >= 0.6.1.
Unit tests available at hydratk/lib/bridge/java/01_methods_ut.jedi

When PyPy is used JPype1 is not installed because the module is not compatible without any alternative.
JPype1 also requires JVM to be installed (not bundled with hydratk). Installation script checks system variable $JAVA_HOME and omits 
JPype1 installation if not set.

Currently the bridge is used for several protocols which can't be implemented with pure Python.

* JDBC - uses DBClient.class, JDBC driver (not bundled)
* JMS - uses JMSClient.class, JMSMessage.class, javaee.jar, JMS driver (not bundled)
* RMI - uses java.rmi.Naming.lookup

**Attributes** :

* mh - MasterHead reference
* _jvm_path - path to JVM
* _classpath - Java classpath
* _status - JVM status, bool, True/False after successful start/stop. Some methods are disabled if JVM not started.

**Properties (Getters)** : 

* jvm_path - returns _jvm_path
* classpath - returns _classpath
* status - returns _status

**Methods** :

* __init__ 

Provides parameters jvm_path, classpath. Sest _jvm_path and _classpath. If jvm_path is not provided it is set according to hydratk
configuration (parameter Libraries/hydratk.lib.bridge.java/jvm_path = default). By default the path is determined by JPype method get_default_jvm_path.
If classpath is not provided it is got from configuration (parameter classpath = /var/local/hydratk/java).

  .. code-block:: python
  
     from hydratk.lib.bridge.java import JavaBridge
     
     # default configuration
     c = JavaBridge() 
     
     # given JVM path
     jvm_path = '/usr/local/app/java/jdk1.8.0_51/jre/lib/amd64/server/libjvm.so'
     c = JavaBridge(jvm_path)     
     
* start

Methods starts JVM. First fires event java_before_start where parameter options can be rewritten. options is list of possible JVM
parameters (check Java documentation for more info). Methods sets classpath option -Djava.class.path by default.  
Method start JVM using JPype1 method startJVM, fires event java_after_start and returns bool.

  .. code-block:: python
  
     res = c.start()   
     
* stop

Methods stops JVM. First fires event java_before_stop. Stops JVM using JPype1 method shutdownJVM, fires event java_after_stop
and returns bool. There is limitation for JVM restart. When you use stop JVM, it is not possible to start it within same process.
Method start uses JPype1 method isJVMStarted to check if JVM was already started and doesn't allow restart.

  .. code-block:: python
  
     res = c.stop()   
     
* get_var

Method returns Java variable of given data type and sets its value.

Supported types:
byte -> JByte, short -> JShort, int -> JInt, long -> JLong, float -> JFloat, double -> JDouble, char -> JChar, string -> JString, bool -> JBoolean  

  .. code-block:: python
  
     # int
     v = c.get_var('int', 2)
     
     # string
     v = c.get_var('string', 'abc')
     
     # bool
     v = c.get_var('bool', True)
     
* get_class

Method creates instance of given Java class and returns reference. Constructor attributes are passed as args.
The class must standard Java class or custom class available on classpath.

  .. code-block:: python
  
     # DBClient.class
     v = c.get_class('DBClient', c.get_var('bool', True))     
     
     # JMSClient.class
     v = c.get_class('JMSClient', c.get_var('bool', True))
     
* desc_class

Method describe given class. Returns tuple of attributes, methods.  
The class must standard Java class or custom class available on classpath.

  .. code-block:: python
  
     # DBClient.class
     attrs, methods = c.desc_class('DBClient')
     # attrs = ['conn', 'host', 'passw', 'port', 'sid', 'user', 'verbose']
     # methods = ['commit', 'connect', 'disconnect', 'exec_query', 'rollback']
     
     # JMSClient.class
     attrs, methods = c.desc_class('JMSClient')
     # attrs = ['connected', 'connection', 'consumer', 'ctx', 'factory', 'producer', 'session', 'verbose']
     # methods = ['browse', 'connect', 'disconnect', 'receive', 'send']
     
* get_package

Methods returns reference to given package. Package classes are accessible via dot notation.
The package must standard Java class or custom package available on classpath.

  .. code-block:: python
  
     v = c.get_package('java.util')
     v = c.get_package('java').rmi.Naming.lookup(url)
     
* init_arraylist

Methods initializes java.util.ArrayList (similar to Python list).

  .. code-block:: python
  
     v = c.init_arraylist(['a', 'b', 'c'])
     
* init_hashmap

Method initializes java.util.concurrent.ConcurrentHashMap (similar to Python dict).

  .. code-block:: python
  
     v = c.init_hashmap({'a': 1, 'b': 2, 'c': 3})
     
* _set_classpath  

Auxiliary method which sets Java classpath. It walks through given directory (/var/local/hydratk/java)
and adds all jar files to classpath. Returns classpath string used when JVM is started.

  .. code-block:: python
  
     # default
     res = c._set_classpath()
     # returns /var/local/hydratk/java/javaee.jar   
     
     # append classpath
     res = c._set_classpath('/usr/local/app/glassfish/glassfish4/javadb/lib')
     # returns /var/local/hydratk/java/javaee.jar:/usr/local/app/glassfish/glassfish4/javadb/lib/derby.jar                          