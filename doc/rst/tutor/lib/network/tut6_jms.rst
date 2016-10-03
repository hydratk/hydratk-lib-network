.. _tutor_network_tut6_jms:

Tutorial 6: JMS
===============

This sections shows several examples how to use JMS client.

API
^^^

Module hydratk.lib.network.jms.client

Method JMSClient is factory method which requires attribute engine to create 
proper JMSClient object instance. Additional attributes are passed as args, kwargs. 

Supported protocols:

* JMS: module jms_client
* STOMP: module stomp_client
* AMQP: module amqp_client
* MQTT: module mqtt_client

Methods:

* connect: connect to JMS provider 
* disconnect: disconnect from JMS provider 
* send: send message to queue|topic (MQTT supports topic only)
* receive: receive message from queue (from topic for MQTT)
* browse: browse queue, not supported for MQTT
* close: stop JVM, supported for JMS

  .. note::
   
     API uses HydraTK core functionalities so it must be running.

JMS
^^^

Part of JMS client library is implemented in Java as a wrapper application which uses Java JMS API.
Python client library uses Java bridge to create Java object instance.
Specific Java libraries are needed to access JMS providers (WebLogic, HornetQ, OpenMQ, ActiveMQ etc.). 
JMS API has no low level communication protocol specification so there is no universal client library.
These libraries are not bundled with hydratk. 

After installation do following actions:
1. Check that directory /var/local/hydratk/java was created and contains files: JMSClient.java, JMSClient.class, JMSMessage.class, javaee.jar
2. Store specific client jar file to same directory (i.e. activemq-all-5.13.0.jar).

  .. note ::
  
     JMS is not supported for PyPy due to module JPype1.

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.jms.client as jms    
    
     # initialize client
     client = jms.JMSClient('JMS', verbose=True)
     
     # connect to server
     properties = {}
     properties['provider_url'] = 'tcp://localhost:61616'
     properties['initial_context_factory'] = 'org.apache.activemq.jndi.ActiveMQInitialContextFactory'
     
     # returns bool
     client.connect('ConnectionFactory', properties) 
     
     # send message
     headers = {}
     headers['JMSCorrelationID'] = '3141592654-xxx'
     headers['JMSType'] = 'sample'
      
     # returns bool  
     client.send('dynamicQueues/HydraQueue', 'xxx', headers=headers)
     
     # browse queue, search messages of given JMS type
     messages = client.browse('dynamicQueues/HydraQueue', jms_type='sample')
     
     # receive multiple messages
     messages = client.receive('dynamicQueues/HydraQueue', cnt=5) 
     
     # disconnect from server
     # returns bool
     client.disconnect()
     
     # stop JVM
     client.close()
     
STOMP
^^^^^

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.jms.client as jms    
    
     # initialize client
     client = jms.JMSClient('STOMP')
     
     # connect to server     
     # returns bool
     client.connect('localhost', 61613, 'admin', 'password') 
     
     # send message
     headers = {}
     headers['JMSCorrelationID'] = '3141592654-xxx'
     headers['JMSType'] = 'sample'
      
     # returns bool  
     client.send('HydraQueue', 'xxx', headers=headers)
     
     # browse queue, search messages of given JMS type
     messages = client.browse('HydraQueue', cnt=3, jms_type='pokusny')
     
     # receive multiple messages
     messages = client.receive('HydraQueue', cnt=5) 
     
     # disconnect from server
     # returns bool
     client.disconnect()
     
AMQP
^^^^

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.jms.client as jms    
    
     # initialize client
     client = jms.JMSClient('AMQP')
     
     # connect to server     
     # returns bool
     client.connect('localhost', 5672, 'admin', 'password')
     
     # send message
     headers = {}
     headers['JMSCorrelationID'] = '3141592654-xxx'
     headers['JMSType'] = 'sample'
      
     # returns bool  
     client.send('HydraQueue', 'xxx', headers=headers)
     
     # browse queue, search messages of given JMS type
     messages = client.browse('HydraQueue', cnt=3, jms_type='pokusny')
     
     # receive multiple messages
     messages = client.receive('HydraQueue', cnt=5) 
     
     # disconnect from server
     # returns bool
     client.disconnect()
     
MQTT
^^^^

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.jms.client as jms    
    
     # initialize client
     client = jms.JMSClient('MQTT')
     
     # connect to server     
     # returns bool
     client.connect('localhost', 1883, 'admin', 'password')
     
     # send message (only topic is supported)
     # returns bool  
     client.send('HydraTopic', 'xxx')
     
     # receive multiple messages
     # messages are received asynchronously (must be sent to topic during wait timeout) 
     messages = client.receive('HydraTopic', cnt=5) 
     
     # disconnect from server
     # returns bool
     client.disconnect()       