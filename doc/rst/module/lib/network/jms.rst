.. _module_lib_network_jms:

JMS
===

This sections contains module documentation of jms module.

client
^^^^^^

Module client provides common way to initialize message queue client of any supported protocol.
It implements factory design pattern, each client provides class JMSClient.
Unit tests available at hydratk/lib/network/jms/client/01_methods_ut.jedi

Following **engines** are supported:

* JMS - module jms_client
* STOMP - module stomp_client
* AMQP - module amqp_client
* MQTT - module mqtt_client

**Methods** :

* JMSClient 

Creates JMSClient instance of given engine (use engine name, case is ignored).
Any constructor parameters can be passed as args, kwargs. When engine is not supported NotImplementedError is raised.

  .. code-block:: python
  
     from hydratk.lib.network.jms.client import JMSClient
     
     c1 = JMSClient('STOMP')
     c2 = JMSClient('JMS', verbose=True, jvm_path='path/to/jvm')
     
jms_client
^^^^^^^^^^

Module provides class JMSClient which implements client for JMS using Java bridge.
Unit tests available at hydratk/lib/network/jms/jms_client/01_methods_ut.jedi
It requires JMS driver for used message queue stored in /var/local/hydratk/java, drivers are not bundled with hydratk.

When PyPy is used method JMSClient raises NotImplementedError. External module JPype1 is not compatible without any alternative.

**Attributes** :

* _mh - MasterHead reference
* _bridge - Java bridge instance
* _client - JMSClient Java class instance
* _verbose - verbose mode, disabled by default
* _connection_factory - JMS connection factory
* _properties - JMS properties
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* bridge - returns _bridge
* client - returns _client
* verbose - returns _verbose
* connection_factory - returns _connection_factory
* properties - returns _properties
* is_connected - returns _is_connected

**Methods** :

* __init__ 

Constructor called by JMSClient method. Provides parameters verbose, jvm_path, classpath, options.
See Java bridge documentation for more details, usually the parameters mustn't be provided, they are determined from default configuration.
Initializes Java bridge, starts JVM and initializes JMSClient object (JMSClient.class in /var/local/hydratk, additional files JMSMessage.class, javaee.jar)
Parameter verbose enables debug messages in JMSClient class (source code in java/JMSClient.java).

* close

Stops JVM.

* connect

Connects to message queue (specified via connection_factory, properties). Parameters are queue specific, check appropriate documentation.
First fires event jms_before_connect where parameters can be rewritten. Calls Java method connect.
After successful connection fires event jms_after_connect and returns bool. Connection timeout can't be specified, it is handled by javax.jms.

  .. code-block:: python
  
     from hydratk.lib.network.jms.client import JMSClient
     
     c = JMSClient('JMS')
     # activemq-all-5.13.0.jar is stored in /val/local/hydratk/java, it is automatically added to classpath
     connection_factory = 'ConnectionFactory'
     properties = {'provider_url': 'tcp://127.0.0.1:61616',
                   'initial_context_factory': 'org.apache.activemq.jndi.ActiveMQInitialContextFactory'}
     res = c.connect(connection_factory, properties)   
     
Method JMSClient.connect initializes InitialContext, looks for ConnectionFactory, connect to message queue (createConnection, createSession) and returns bool.

* disconnect

Disconnects from queue using Java method disconnect and returns bool.
Method JMSClient.disconnect closes connection and returns bool.  

  .. code-block:: python
  
     res = c.disconnect()
     
* send

Sends message to queue. First fires event jms_before_send where parameters (destination_name, message, destination_type, headers) can be rewritten.
Method transforms headers to Java HashMap. Calls Java method send. After successful send fires event jms_after_send and returns bool.

  .. code-block:: python
  
     # queue destination
     queue = 'dynamicQueues/HydraQueue'
     msg = 'test'
     res = c.send(queue, msg, 'queue') 

     # message with headers
     headers = {'JMSCorrelationID': '1234', 'JMSType': 'test_msg'}
     res = c.send(queue, msg, 'queue', headers)      
     
     # topic destination
     topic = 'dynamicTopics/HydraTopic'
     res = c.send(topic, msg, 'topic')       

Method JMSClient.send initializes queue producer (for queue or topic). Prepares message, sets JMS headers using specific methods and send the message.

Supported headers:
JMSCorrelationID, JMSDeliveryMode, JMSDestination, JMSExpiration, JMSMessageID, JMSPriority, JMSRedelivered, JMSReplyTo, JMSTimestamp, JMSType
        
* receive

Receives messages from queue (messages are deleted). First fires event jms_before_receive where parameters (destination_name, cnt) can be rewritten.
Methods calls Java method receive. After that fires event jms_after_receive and returns list of dictionary (keys JMSCorrelationID, JMSDeliveryMode, 
JMSDestination, JMSExpiration, JMSMessageID, JMSPriority, JMSRedelivered, JMSReplyTo, JMSTimestamp, JMSType, message).

  .. code-block:: python
  
     # single message
     queue = 'dynamicQueues/HydraQueue'
     res = c.receive(queue, 1) 
     
     # multiple messages
     res = c.receive(queue, 10) 
  
Method JMSClient.receive initializes queue consumer (queue only, topic not supported). Receives messages from queue (up to count or all), extracts
specified JMS headers (JMSCorrelationID, JMSDeliveryMode, JMSDestination, JMSExpiration, JMSMessageID, JMSPriority, JMSRedelivered, JMSReplyTo, 
JMSTimestamp, JMSType) and returns ArrayList.  

* browse

Browses message queue (messages are not deleted). First fires event jms_before_browse where parameters (destination_name, cnt, jms_correlation_id, jms_type) 
can be rewritten. Method calls Java method browse. After that fires event jms_after_browse and returns list of dictionary (same format as in receive).

  .. code-block:: python
  
     # full queue
     queue = 'dynamicQueues/HydraQueue'
     res = c.browse(queue)    
     
     # message filter
     jms_id, jms_type = '1234', 'test_msg'
     res = c.browse(queue, jms_correlation_id=jms_id, jms_type=jms_type)      

Method JMSClient.browse initializes queue browser (queue only, topic not supported). Gets messages from queue (possible filter for JMSCorrelationID, JMSType), 
extracts specified JMS headers (JMSCorrelationID, JMSDeliveryMode, JMSDestination, JMSExpiration, JMSMessageID, JMSPriority, JMSRedelivered, JMSReplyTo, 
JMSTimestamp, JMSType) and returns ArrayList. 

stomp_client
^^^^^^^^^^^^

Module provides class JMSClient which implements client for STOMP protocol using external module
`stompest <https://github.com/nikipore/stompest>`_ in version >= 2.2.5. When Python2.6 is used version 2.1.6 is installed.
Unit tests available at hydratk/lib/network/jms/stomp_client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - stompest client instance
* _host - server hostname (or IP address)
* _port - port name (default 61613)
* _user - username
* _passw - password
* _verbose - verbose mode, disabled by default
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* client - returns _client
* host - returns _host
* port - returns _port
* user - returns _user
* passw - returns _passw
* verbose - returns _verbose
* is_connected - returns _is_connected

**Methods** :

* __init__ 

Constructor called by JMSClient method. Provides parameter verbose. Sets MasterHead instance and turns on verbose mode if enabled.

* connect

Connects to message queue (specified via host, port, user, passw). First fires event jms_before_connect where parameters can be rewritten. 
Sets _client to stompest client instance (constructor Stomp) and connects to message queue using stompest method connect.
After successful connection fires event jms_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.jms.client import JMSClient
     
     c = JMSClient('STOMP')
     res = c.connect(host='127.0.0.1', port=61613, user='admin', passw='password')     
     
* disconnect

Disconnects from queue using stompest methods disconnect, close and returns bool.

  .. code-block:: python
  
     res = c.disconnect()
     
* send

Sends message to queue. First fires event jms_before_send where parameters (destination_name, message, destination_type, headers) can be rewritten.
Method transforms JMS headers (to be common with jms_client) to STOMP specific headers. Sends message using stompest method send.
After successful send fires event jms_after_send and returns bool.

Supported headers:
JMSCorrelationID -> correlation-id, JMSExpiration -> expires, JMSDeliveryMOde -> persistent, JMSPriority -> priority, JMSReplyTo -> reply-to, 
JMSType -> type, JMSMessageID -> message-id, JMSDestination -> destination, JMSTimestamp -> timestamp, JMSRedelivered -> redelivered

  .. code-block:: python
  
     # queue destination
     queue = 'dynamicQueues/HydraQueue'
     msg = 'test'
     res = c.send(queue, msg, 'queue') 

     # message with headers
     headers = {'JMSCorrelationID': '1234', 'JMSType': 'test_msg'}
     res = c.send(queue, msg, 'queue', headers)      
     
     # topic destination
     topic = 'dynamicTopics/HydraTopic'
     res = c.send(topic, msg, 'topic')       

* receive

Receives messages from queue (messages are deleted). First fires event jms_before_receive where parameters (destination_name, cnt) can be rewritten.
Methods subscribes to queue using stompest method subscriber, receives message using method receiveFrame and deletes it using ack. 
Headers are translated to JMS header names. After that fires event jms_after_receive and returns list of dictionary (keys message, JMS header1, JMS header2, ...).

  .. code-block:: python
  
     # single message
     queue = 'dynamicQueues/HydraQueue'
     res = c.receive(queue, 1) 
     
     # multiple messages
     res = c.receive(queue, 10)  

* browse

Browses message queue (messages are not deleted). First fires event jms_before_browse where parameters (destination_name, cnt, jms_correlation_id, jms_type) 
can be rewritten. Methods subscribes to queue using stompest method subscriber, receives message using method receiveFrame. 
Message filter for headers correlaion-id and type. Headers are translated to JMS header names. 
After that fires event jms_after_receive and returns list of dictionary (keys message, JMS header1, JMS header2, ...).

  .. code-block:: python
  
     # full queue
     queue = 'dynamicQueues/HydraQueue'
     res = c.browse(queue)    
     
     # message filter
     jms_id, jms_type = '1234', 'test_msg'
     res = c.browse(queue, jms_correlation_id=jms_id, jms_type=jms_type)      

amqp_client
^^^^^^^^^^^

Module provides class JMSClient which implements client for AMQP protocol using external module
`python-qpid-proton <http://qpid.apache.org/releases/qpid-proton-0.15.0/proton/python/api/index.html>`_ in version >= 0.10. 
Unit tests available at hydratk/lib/network/jms/amqp_client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - stompest client instance
* _host - server hostname (or IP address)
* _port - port name (default 5672)
* _user - username
* _passw - password
* _verbose - verbose mode, disabled by default
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* client - returns _client
* host - returns _host
* port - returns _port
* user - returns _user
* passw - returns _passw
* verbose - returns _verbose
* is_connected - returns _is_connected

**Methods** :

* __init__ 

Constructor called by JMSClient method. Provides parameter verbose. Sets MasterHead instance and turns on verbose mode if enabled.

* connect

Connects to message queue (specified via host, port, user, passw). First fires event jms_before_connect where parameters can be rewritten. 
Sets _client to proton client instance (constructor BlockingConnection). After successful connection fires event jms_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.jms.client import JMSClient
     
     c = JMSClient('AMQP')
     res = c.connect(host='127.0.0.1', port=5672, user='admin', passw='password')     
     
* disconnect

Disconnects from queue using proton method close, close and returns bool.

  .. code-block:: python
  
     res = c.disconnect()
     
* send

Sends message to queue. First fires event jms_before_send where parameters (destination_name, message, destination_type, headers) can be rewritten.
Method transforms JMS headers (to be common with jms_client) to AMTP specific headers. Sends message using proton methods create_sender, send.
After successful send fires event jms_after_send and returns bool.

Supported headers:
JMSDeliveryMode -> header.durable, JMSPriority -> header.priority, JMSExpiration -> header.ttl, JMSType -> message-annotations.x-opt-jms-type, 
JMSMessageID -> properties.message-id, JMSDestination -> properties.to, JMSReplyTo -> properties.reply-to, JMSCorrealationID -> properties.correlation-id, 
JMSTimestamp -> properties.creation-time

  .. code-block:: python
  
     # queue destination
     queue = 'dynamicQueues/HydraQueue'
     msg = 'test'
     res = c.send(queue, msg, 'queue') 

     # message with headers
     headers = {'JMSCorrelationID': '1234', 'JMSType': 'test_msg'}
     res = c.send(queue, msg, 'queue', headers)      
     
     # topic destination
     topic = 'dynamicTopics/HydraTopic'
     res = c.send(topic, msg, 'topic')       

* receive

Receives messages from queue (messages are deleted). First fires event jms_before_receive where parameters (destination_name, cnt) can be rewritten.
Methods subscribes to queue using proton method create_receiver, receives message using method receive and deletes it using accept. 
Headers are translated to JMS header names. After that fires event jms_after_receive and returns list of dictionary (keys message, JMS header1, JMS header2, ...).

  .. code-block:: python
  
     # single message
     queue = 'dynamicQueues/HydraQueue'
     res = c.receive(queue, 1) 
     
     # multiple messages
     res = c.receive(queue, 10)  

* browse

Browses message queue (messages are not deleted). First fires event jms_before_browse where parameters (destination_name, cnt, jms_correlation_id, jms_type) 
Methods subscribes to queue using proton method create_receiver, receives message using method receive and accepts using accept (copied from queue, not deleted). 
Headers are translated to JMS header names. After that fires event jms_after_receive and returns list of dictionary (keys message, JMS header1, JMS header2, ...).

  .. code-block:: python
  
     # full queue
     queue = 'dynamicQueues/HydraQueue'
     res = c.browse(queue)    
     
     # message filter
     jms_id, jms_type = '1234', 'test_msg'
     res = c.browse(queue, jms_correlation_id=jms_id, jms_type=jms_type)     
     
mqtt_client
^^^^^^^^^^^

Module provides class JMSClient which implements client for MQTT protocol using external module
`paho-mqtt <https://github.com/eclipse/paho.mqtt.python>`_ in version >= 1.2. 
Unit tests available at hydratk/lib/network/jms/mqtt_client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - stompest client instance
* _host - server hostname (or IP address)
* _port - port name (default 1883)
* _user - username
* _passw - password
* _verbose - verbose mode, disabled by default
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.
* _messages - auxiliary storage (it has no getter)

**Properties (Getters)** :

* client - returns _client
* host - returns _host
* port - returns _port
* user - returns _user
* passw - returns _passw
* verbose - returns _verbose
* is_connected - returns _is_connected

**Methods** :

* __init__ 

Constructor called by JMSClient method. Provides parameter verbose. Sets _client to paho client instance (constructor Client) 
and turns on verbose mode if enabled.

* connect

Connects to message queue (specified via host, port, user, passw). First fires event jms_before_connect where parameters can be rewritten. 
Connects to queue using paho method connect (authentication using username_pw_set). 
After successful connection fires event jms_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.jms.client import JMSClient
     
     c = JMSClient('MQTT')
     res = c.connect(host='127.0.0.1', port=1883, user='admin', passw='password')     
     
* disconnect

Disconnects from queue using proton method disconnect, close and returns bool.

  .. code-block:: python
  
     res = c.disconnect()
     
* send

Sends message to topic. First fires event jms_before_send where parameters (destination_name, message) can be rewritten.
Method sends message using paho method publish. After successful send fires event jms_after_send and returns bool.

  .. code-block:: python
  
     res = c.send('HydraTopic', 'test')      

* receive

Receives messages from topic. First fires event jms_before_receive where parameters (destination_name, cnt, timeout) can be rewritten.
Methods subscribes to topic using paho method subscribe, methods checks topic for incoming messages (up to count or timeout, asynchronous).
After that fires event jms_after_receive and returns list of string.

  .. code-block:: python
  
     # single message
     res = c.receive('HydraTopic')  
     
     # multiple messages
     res = c.receive('HydraTopic', 2)   
  
* _on_message

Auxiliary method with asynchronous message receiver.  

simplejms
^^^^^^^^^

Modules provides simplified wrapper to jms_client with with possibility to send messages from template.
Unit tests available at hydratk/lib/network/jms/simplejms/01_methods_ut.jedi

**Classes** :

* JMSClient

**Attributes** :
_request, _response

**Properties (Getters)** :
request, response

**Properties (Setters** :
request

**Methods** :
send - uses method jms_client.send, parameter jms_correlation_id

  .. code-block:: python
  
     from hydratk.lib.network.jms.simplejms import JMSClient, JMSRequest, JMSRequestMessage
     
     c = JMSClient()
     msg = '<readCustomer><id>0</id></readCustomer>'
     rqm = JMSRequestMessage(msg, 'str')
     rq = JMSRequest('dynamicQueues/HydraQueue', 'test')
     rq.message = rqm
     c.request = rq
     properties = {'provider_url': 'tcp://127.0.0.1:61616',
                   'initial_context_factory': 'org.apache.activemq.jndi.ActiveMQInitialContextFactory'}
     c.connect('ConnectionFactory', properties) 
     res = c.send('1234')     

* JMSRequest

**Attributes** :
_bind_lchr, _bind_rchr, _content

**Properties (Getters)** :
content

**Properties (Setters)** :
content

**Methods** :
__init__ - sets _destination_queue, _jms_type

* JMSRequestMessage

**Attributes** :
_msg, _destination_queue, _jms_type

**Properties (Getters)** :
destination_queue, jms_type, msg, message

**Properties (Setters)** :
destination_queue, jms_type, msg, message

**Methods** :
__init__ - sets _content, it is possible to load message from file
load_from_file - sets _content with file content
bind_var - fills message template with given data passed as args, kwargs

  .. code-block:: python
  
     msg = '<readCustomer><id>[id]</id><name>[name]</name></readCustomer>'
 
     # bind args
     c = JMSRequestMessage(msg, 'str')
     id, name = '1', 'Charlie Bowman'
     c.bind_var({'id': id}, {'name': name}) 
     
     # bind kwargs
     c.bind_var({'id': id, 'name': name})     