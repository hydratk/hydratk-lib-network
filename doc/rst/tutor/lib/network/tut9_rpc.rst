.. _tutor_network_tut9_rpc:

Tutorial 9: RPC
===============

This sections shows several examples how to use RPC client.

API
^^^

Module hydratk.lib.network.rpc.client

Method RPCClient is factory method which requires attribute engine to create 
proper RPCClient object instance. Additional attributes are passed as args, kwargs. 

Supported providers:

* Java RMI: module rmi_client
* XML-RPC: module xmlrpc_client
* JSON-RPC: module jsonrpc_client

Methods:

* init_proxy: initialize proxy to remote object
* call_method: call method on remote object
* close: stop JVM

  .. note::
   
     API uses HydraTK core functionalities so it must be running.

RMI
^^^

  .. code-block:: python
  
     # import library
     from hydratk.lib.network.rpc.client import RPCClient
     
     # initialize client
     client = RPCClient('rmi')
     
     # initialize proxy
     client.init_proxy('rmi://localhost:2004/server') 
     
     # call remote method
     client.call_method('callRemote', 'xxx')
     
     # stop JVM
     client.close()      
     
XML-RPC
^^^^^^^

  .. code-block:: python     
  
     # import library
     from hydratk.lib.network.rpc.client import RPCClient
     
     # initialize client
     client = RPCClient('xmlrpc')
     
     # initialize proxy
     client.init_proxy('http://127.0.0.1:8000') 
     
     # call remote method
     client.call_method('callRemote', 'xxx')
     
     # stop JVM
     client.close()   
     
JSON-RPC
^^^^^^^^

  .. code-block:: python     
  
     # import library
     from hydratk.lib.network.rpc.client import RPCClient
     
     # initialize client
     client = RPCClient('jsonrpc')
     
     # initialize proxy
     client.init_proxy('http://127.0.0.1:8000') 
     
     # call remote method
     client.call_method('callRemote', 'xxx')
     
     # stop JVM
     client.close()       