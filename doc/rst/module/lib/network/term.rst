.. _module_lib_network_term:

TERM
====

This sections contains module documentation of term module.

client
^^^^^^

Module client provides common way to initialize terminal client of any supported protocol.
It implements factory design pattern, each client provides class TermClient.
Unit tests available at hydratk/lib/network/term/client/01_methods_ut.jedi

Following **protocols** are supported:

* SSH - module ssh_client
* TELNET - module telnet_client

**Methods** :

* TermClient 

Creates TermClient instance of given protocol (use protocol name, case is ignored). Any constructor parameters can be passed as args, kwargs 
(supported for rmi_client only). When provider is not supported NotImplementedError is raised.

  .. code-block:: python
  
     from hydratk.lib.network.term.client import TermClient
     
     c1 = TermClient('TELNET')
     c2 = TermClient('SSH', verbose=True)
     
ssh_client
^^^^^^^^^^

Module provides class TermClient which implements client for SSH using external module
`paramiko <http://www.paramiko.org/>`_ in version >= 1.16.0.
paramiko requires non-Python libraries which are automatically installed by setup script (libff-dev, libssl-dev for apt-get, libffi-devel, openssl-devel for yum).

Unit tests available at hydratk/lib/network/term/ssh_client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - paramiko client instance
* _host - server hostname (or IP address)
* _port - port number (default 22)
* _user - username
* _passw - password
* _cert - path to certificate file
* _verbose - bool, verbose mode
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* client - returns _client
* host - returns _host
* port - returns _port
* user - returns _user
* passw - returns _passw
* cert - returns _cert
* verbose - returns _verbose
* is_connected - returns _is_connected  

**Methods** :

* __init__ 

Constructor called by TermClient method. Turns verbose mode if enabled.

* connect

Connects to server (specified via parameters host, port, user, passw, cert). First fires event term_before_connect where parameters can be rewritten. 
Sets _client to paramiko client instance (using paramiko method connect). Undefined hosts are automatically allowed using paramiko method set_missing_host_key_policy.
After successful connection fires event term_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

 .. code-block:: python
   
    from hydratk.lib.network.term.client import TermClient
    
    c = TermClient('SSH')
    res = c.connect(host='127.0.0.1', port=22, user='lynus', passw='bowman')
    
    # certificate
    res = c.connect(host, port, user, cert='/home/lynus/hydratk/key.pri')
    
* disconnect

Disconnects from server using paramiko method close and returns bool.

  .. code-block:: python
  
     res = c.disconnect()      
     
* exec_command

Method executes command on server. First fires event term_before_exec_command where parameters (command, input) can be rewritten.
It uses paramiko method exec_command which returns tuples of streams (stdin, stdout, stderr). If input is provided it is written to stdin
(useful for commands which require some reaction i.e. delete confirmation). 

After that method fires event term_after_exec_command. When stderr is not empty the method returns False and stderr content as list of lines.
Otherwise it returns True and stdout content as list of lines.

  .. code-block:: python
   
     # command with output
     res, out = c.exec_command('pwd')
     
     # command with input
     res, out = c.exec_command('rm test.txt', 'y')
     
     # command with error output (without root privileges)
     res, out = c.exec_command('touch /root/test.txt')

telnet_client
^^^^^^^^^^^^^

Module provides class TermClient which implements client for TELNET using standard module
`telnetlib <https://docs.python.org/3.6/library/telnetlib.html>`.
Unit tests available at hydratk/lib/network/term/telnet_client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - telnetlib client instance
* _host - server hostname (or IP address)
* _port - port number (default 23)
* _verbose - bool, verbose mode
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.
* _br - line break character, default \n (LF), it has no getter

**Properties (Getters)** :

* client - returns _client
* host - returns _host
* port - returns _port
* verbose - returns _verbose
* is_connected - returns _is_connected  

**Methods** :

* __init__ 

Constructor called by TermClient method. Sets _client to telnetlib client (using constructor Telnet), turns verbose mode if enabled.   

* connect

Connects to server (specified via parameters host, port). First fires event term_before_connect where parameters can be rewritten. 
Connects to server using telnetlib method open and gets output using method _read.
After successful connection fires event term_after_connect and returns bool and output as list of string. Connection timeout is 10s by default (parameter timeout).

 .. code-block:: python
   
    from hydratk.lib.network.term.client import TermClient
    
    c = TermClient('TELNET')
    res, out = c.connect(host='freechess.org', port=23)
    
* disconnect

Disconnects from server using telnetlib method close and returns bool.

  .. code-block:: python
  
     res = c.disconnect()   
     
* exec_command

Method executes command on server. First fires event term_before_exec_command where parameter command can be rewritten.
It uses telnetlib method write, each command is appended with line break. Gets output using method _read. 
After that method fires event term_after_exec_command and returns bool and output as list of string.

  .. code-block:: python
   
     res, out = c.exec_command('guest')
     
* _read

Auxiliary method. It reads server response using telnetlib method read_until (it ends with line break).
Returns the output as list of string.