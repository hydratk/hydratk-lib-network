.. _module_lib_network_rpc:

RPC
===

This sections contains module documentation of rpc module.

client
^^^^^^

Module client provides common way to initialize message queue client of any supported provider.
It implements factory design pattern, each client provides class RPCClient.
Unit tests available at hydratk/lib/network/rpc/client/01_methods_ut.jedi

Following **providers** are supported:

* RMI - module rmi_client
* XMLRPC - module xmlrpc_client
* JSONRPC - module jsonrpc_client

**Methods** :

* RPCClient 

Creates RPCClient instance of given engine (use provider name, case is ignored). Any constructor parameters can be passed as args, kwargs 
(supported for rmi_client only). When provider is not supported NotImplementedError is raised.

  .. code-block:: python
  
     from hydratk.lib.network.rpc.client import RPCClient
     
     c1 = RPCClient('RMI')
     c2 = RPCClient('RMI', jvm_path='path/to/jvm')
     
rpc_client
^^^^^^^^^^

Module provides class RPCClient which implements client for RMI using Java bridge.
Unit tests available at hydratk/lib/network/rpc/rmi_client/01_methods_ut.jedi

When PyPy is used method JMSClient raises NotImplementedError. External module JPype1 is not compatible without any alternative.

**Attributes** :

* _mh - MasterHead reference
* _bridge - Java bridge instance
* _proxy - proxy to remote object

**Properties (Getters)** :

* bridge - returns _bridge
* proxy - returns _proxy    

**Methods** :

* __init__ 

Constructor called by RPCClient method. Provides parameters jvm_path, classpath, options.
See Java bridge documentation for more details, usually the parameters mustn't be provided, they are determined from default configuration.

* close

Stops JVM.

* init_proxy

Methods initializes proxy to remote object. First fires event rpc_before_init_proxy where parameter url can be rewritten.
The method uses standard Java method java.rmi.Naming.lookup. After successful initialization fires event rpc_after_init_proxy and returns bool.

  .. code-block:: python
  
     from hydratk.lib.network.rpc.client import RPCClient
     
     c = RPCClient('RMI')
     url = 'rmi://127.0.0.1:2004/server'
     res = c.init_proxy(url) 
     
* call_method

Methods call remote method using proxy object. First fires event rpc_before_call_method where parameters (name, args) can be rewritten.
It calls proxy method name and passes parameters as args. When it receives response fires event rpc_after_call_method and returns method output.

  .. code-block:: python
  
     # no parameters
     res = c.call_method('callRemote')  
     
     # output int parameter
     res = c.call_method('out_int')
     # returns 666
     
     # output string parameter
     res = c.call_method('out_string')
     
     # input int, output int parameters
     res = c.call_method('in_int', 2)
     # returns 8
     
     # 2 input int, output string parameters
     res = c.call_method('in2', 3, 5) 
     # returns '35'      
     
xmlrpc_client
^^^^^^^^^^^^^

Module provides class RPCClient which implements client for XML-RPC using standard module
`xmlrpclib <https://docs.python.org/2/library/xmlrpclib.html>`_.
When Python3 is used module xmlrpclib is replaced by `xmlrpc <https://docs.python.org/3/library/xmlrpc.client.html>`
Unit tests available at hydratk/lib/network/rpc/xmlrpc_client/01_methods_ut.jedi.

**Attributes** :

* _mh - MasterHead reference
* _proxy - proxy to remote object

**Properties (Getters)** :

* proxy - returns _proxy    

**Methods** :

* __init__ 

Constructor called by RPCClient method. Sets MasterHead reference.

* init_proxy

Methods initializes proxy to remote object. First fires event rpc_before_init_proxy where parameters (url, timeout) can be rewritten.
The method uses xmlrpclib constructor ServerProxy. After successful initialization fires event rpc_after_init_proxy and returns bool.
Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.rpc.client import RPCClient
     
     c = RPCClient('XMLRPC')
     url = 'http://127.0.0.1:8000'
     res = c.init_proxy(url)  
     
* call_method

Methods call remote method using proxy object. First fires event rpc_before_call_method where parameters (name, args) can be rewritten.
It calls proxy method name and passes parameters as args. When it receives response fires event rpc_after_call_method and returns method output.

  .. code-block:: python
  
     # no parameters
     res = c.call_method('callRemote')  
     
     # output int parameter
     res = c.call_method('out_int')
     # returns 666
     
     # output string parameter
     res = c.call_method('out_string')
     
     # input int, output int parameters
     res = c.call_method('in_int', 2)
     # returns 8
     
     # 2 input int, output string parameters
     res = c.call_method('in2', 3, 5) 
     # returns '35'           
     
jsonrpc_client
^^^^^^^^^^^^^^

Module provides class RPCClient which implements client for JSON-RPC using external module
`jsonrpclib <https://github.com/joshmarshall/jsonrpclib/>`_ in version >= 0.1.7.
When Python3 is used module jsonrpclib is replaced by `jsonrpclib-pelix <https://github.com/tcalmant/jsonrpclib/>`_ in version >= 0.2.8.
Unit tests available at hydratk/lib/network/rpc/jsonrpc_client/01_methods_ut.jedi.

**Attributes** :

* _mh - MasterHead reference
* _proxy - proxy to remote object

**Properties (Getters)** :

* proxy - returns _proxy    

**Methods** :

* __init__ 

Constructor called by RPCClient method. Sets MasterHead reference.

* init_proxy

Methods initializes proxy to remote object. First fires event rpc_before_init_proxy where parameters (url, timeout) can be rewritten.
The method uses jsonrpclib constructor Server. After successful initialization fires event rpc_after_init_proxy and returns bool.
Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.rpc.client import RPCClient
     
     c = RPCClient('JSONRPC')
     url = 'http://127.0.0.1:7999'
     res = c.init_proxy(url)  
     
* call_method

Methods call remote method using proxy object. First fires event rpc_before_call_method where parameters (name, args) can be rewritten.
It calls proxy method name and passes parameters as args. When it receives response fires event rpc_after_call_method and returns method output.

  .. code-block:: python
  
     # no parameters
     res = c.call_method('callRemote')  
     
     # output int parameter
     res = c.call_method('out_int')
     # returns 666
     
     # output string parameter
     res = c.call_method('out_string')
     
     # input int, output int parameters
     res = c.call_method('in_int', 2)
     # returns 8
     
     # 2 input int, output string parameters
     res = c.call_method('in2', 3, 5) 
     # returns '35'         