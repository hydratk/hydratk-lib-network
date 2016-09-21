.. _tutor_network_tut5_java:

Tutorial 5: Java bridge
=======================

This sections shows several examples how to use bridge to JVM.

API
^^^

Module hydratk.lib.bridge.java

Methods:

* start: start JVM
* stop: stop JVM
* get_var: create Java variable
* get_class: create Java class instance
* desc_class: describe Java class
* get_package: get reference to Java package
* init_arraylist: initialize Java ArrayList collection (aka Python list)
* init_hashmap: initialize Java HashMap collection (aka Python dict)

  .. note::
   
     API uses HydraTK core functionalities so it must be running.
     
Configuration
^^^^^^^^^^^^^

Common configuration file contains 2 parameters

* jvm_path: path to JVM library (file libjvm.so), JVM is found by bridge in default configuration
* classpath: path with Java files (class, jar) to be added to JVM classpath

  .. code-block:: python

     Libraries:
       hydratk.lib.bridge.java:
         jvm_path: default
         classpath: /var/local/hydratk/java     
         
Examples
^^^^^^^^

  .. code-block:: python
  
     # import library
     from hydratk.lib.bridge.java import JavaBridge
    
     # initialize bridge
     bridge = JavaBridge()
     
     # start JVM
     bridge.start()
     
     # display status, JVM path and classpath 
     # classpath contains all included Java files
     print jbridge.status
     print jbridge.jvm_path  
     print jbridge.classpath  
     
     # create Java object
     # bool variable is passed to constructor
     jms = bridge.get_class('JMSClient', bridge.get_var('bool', True))  
     
     # describe class (aka Python __dict__)
     print jbridge.desc_class('JMSClient') 
     
     # call method
     # str is passed as Java string, None is passed as null
     jms.connect('javax/jms/QueueConnectionFactory', 'weblogic.jndi.WLInitialContextFactory',
                 't3://sxcipppr1.ux.to2cz.cz:8301,sxcipppr2.ux.to2cz.cz:8301', None, None)
     
     # stop JVM
     bridge.stop()           