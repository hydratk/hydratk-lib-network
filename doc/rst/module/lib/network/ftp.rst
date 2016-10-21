.. _module_lib_network_ftp:

FTP
===

This sections contains module documentation of ftp module.

client
^^^^^^

Module client provides common way to initialize FTP client.
It implements factory design pattern, each client provides class FTPClient.
Unit tests available at hydratk/lib/network/ftp/client/01_methods_ut.jedi

Following **protocols** are supported:

* FTP - module ftp_client
* SFTP - module sftp_client
* TFTP - module tftp_client

**Methods** :

* FTPClient 

Creates FTPClient instance of given protocol (use protocol name, case is ignored).
Any constructor parameters can be passed as args, kwargs. When engine is not supported NotImplementedError is raised.

  .. code-block:: python
  
     from hydratk.lib.network.dbi.client import FTPClient
     
     c1 = EmailClient('FTP')
     c2 = EmailClient('FTP', secured=True, verbose=True)
     
ftp_client
^^^^^^^^^^

Module provides class FTPClient which implements FTP client using Python module 
`ftplib <https://docs.python.org/3.6/library/ftplib.html>`_.
Unit tests available at hydratk/lib/network/ftp/ftp_client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - ftplib client instance
* _secured - bool, secured protocol FTPS
* _host - server hostname (or IP address)
* _port - port number (default 21)
* _user - username
* _passw - password
* _path - server path (default /)
* _verbose - bool, verbose mode
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* client - returns _client
* secured - returns _secured
* host - returns _host
* port - returns _port
* user - returns _user
* passw - returns _passw
* path - returns _path
* verbose - returns _verbose
* is_connected - returns _is_connected

**Methods** :

* __init__

Constructor called by FTPClient method. Sets _client to ftplib client instance (using constructor FTP or FTP_TLS depending on _secured).
Turns verbose mode if enabled (ftplib method set_debuglevel), not secured protocol is used by default.

* connect

Connects to server (specified via parameters host, port, user, passw, path).
First fires event ftp_before_connect where parameters can be rewritten. Connects to server using method ftplib method connect and login.
Sets given working directory. After successful connection fires event ftp_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.ftp.client import FTPClient
     
     c = FTPClient('FTP')
     res = c.connect(host='test.rebex.net', port=21, user='demo', passw='password')     

* disconnect

Disconnects from database using ftplib method quit and returns bool.

  .. code-block:: python
  
     res = c.disconnect()     
     
* list_dir

List working directory using ftplib method nlst. Directories . and .. are omitted. Returns list of directory, file names.

  .. code-block:: python
  
     res = c.list_dir()    
     
* change_dir

Changes working directory using ftplib method cwd and sets _path. Returns bool.

  .. code-block:: python
  
     res = c.change_dir('/pub')   
     
* download_file

Downloads file from server. First fires event ftp_before_download_file where parameters (remote_path, local_path) can be rewritten.
Downloads file content using ftplib method retrbinary and writes it to local file (by default ./filename if local_path not specified).
After successful download fires event ftp_after_download_file and returns bool. 

  .. code-block:: python
  
     # default local path
     res = c.download_file('readme.txt')
     
     # given local path
     res = c.download_file('readme.txt', './')   
     
* upload_file

Uploads file to server. First fires event ftp_before_upload_file where parameters (local_path, remote_path) can be rewritten.
Uploads file content using ftplib method storbinary and writes it to remote file (by default ./filename if remote_path not specified).
After successful download fires event ftp_after_upload_file and returns bool. 

  .. code-block:: python
  
     # default remote path
     res = c.upload_file('readme.txt')
     
     # given remote path
     res = c.upload_file('readme.txt', './')     
     
* delete_file

Deletes file on server. First fires event ftp_before_delete_file where parameter path can be rewritten.
Deletes file using ftplib method delete. After successful download fires event ftp_after_delete_file and returns bool. 

  .. code-block:: python
  
     res = c.delete_file('readme.txt')  
     
* make_dir

Creates directory on server. First fires event ftp_before_make_dir where parameter path can be rewritten.
Creates it ftplib method mkd. After successful download fires event ftp_after_make_dir and returns bool. 

  .. code-block:: python
  
     res = c.make_dir('/lynus.cekuj.net/web/test') 
     
* remove_dir

Deletes directory on server. First fires event ftp_before_remove_dir where parameter path can be rewritten.
Deteles it ftplib method rmd. After successful download fires event ftp_after_remove_dir and returns bool. 

  .. code-block:: python
  
     res = c.remove_dir('/lynus.cekuj.net/web/test')   
     
sftp_client
^^^^^^^^^^^

Module provides class FTPClient which implements SFTP client using external module 
`paramiko <http://www.paramiko.org/>`_ in version >= 1.16.0.
paramiko requires non-Python libraries which are automatically installed by setup script (libffi-dev, libssl-dev for apt-get, libffi-devel, openssl-devel for yum).

Unit tests available at hydratk/lib/network/ftp/sftp_client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - paramiko client instance
* _host - server hostname (or IP address)
* _port - port number (default 22)
* _user - username
* _passw - password
* _cert - path to certificate
* _path - server path (default /)
* _verbose - bool, verbose mode
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* client - returns _client
* host - returns _host
* port - returns _port
* user - returns _user
* passw - returns _passw
* cert - returns _cert
* path - returns _path
* verbose - returns _verbose
* is_connected - returns _is_connected

**Methods** :

* __init__

Constructor called by FTPClient method. Turns verbose mode if enabled.

* connect

Connects to server (specified via parameters host, port, user, passw, cert, path).Sets _client to ftplib client instance (using constructor FTP or FTP_TLS depending on _secured).
First fires event ftp_before_connect where parameters can be rewritten. Connects to server using method paramiko methods connect, from_transport.
Certificate is read using paramiko method RSAKey.from_private_key_file.

Sets given working directory. After successful connection fires event ftp_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.ftp.client import FTPClient
     
     c = FTPClient('SFTP')
     res = c.connect(host='127.0.0.1', port=22, user='lynus', passw='bowman')
     
     # certificate     
     res = c.connect(host='127.0.0.1', port=22, user='lynus', cert='/home/lynus/hydratk/key.pri')      

* disconnect

Disconnects from database using paramiko method quit and returns bool.

  .. code-block:: python
  
     res = c.disconnect()     
     
* list_dir

List working directory using paramiko method listdir.

  .. code-block:: python
  
     res = c.list_dir()    
     
* change_dir

Changes working directory using paramiko method chdir and sets _path. Returns bool.

  .. code-block:: python
  
     res = c.change_dir('/home/lynus/private')   
     
* download_file

Downloads file from server. First fires event ftp_before_download_file where parameters (remote_path, local_path) can be rewritten.
Downloads file content using paramiko method get and writes it to local file (by default ./filename if local_path not specified).
After successful download fires event ftp_after_download_file and returns bool. 

  .. code-block:: python
  
     # default local path
     res = c.download_file('readme.txt')
     
     # given local path
     res = c.download_file('readme.txt', './')   
     
* upload_file

Uploads file to server. First fires event ftp_before_upload_file where parameters (local_path, remote_path) can be rewritten.
Uploads file content using paramiko method put and writes it to remote file (by default ./filename if remote_path not specified).
After successful download fires event ftp_after_upload_file and returns bool. 

  .. code-block:: python
  
     # default remote path
     res = c.upload_file('readme.txt')
     
     # given remote path
     res = c.upload_file('readme.txt', './')     
     
* delete_file

Deletes file on server. First fires event ftp_before_delete_file where parameter path can be rewritten.
Deletes file using paramiko method remove. After successful download fires event ftp_after_delete_file and returns bool. 

  .. code-block:: python
  
     res = c.delete_file('readme.txt')  
     
* make_dir

Creates directory on server. First fires event ftp_before_make_dir where parameter path can be rewritten.
Creates it paramiko method mkdir. After successful download fires event ftp_after_make_dir and returns bool. 

  .. code-block:: python
  
     res = c.make_dir('/var/local/hydratk/test') 
     
* remove_dir

Deletes directory on server. First fires event ftp_before_remove_dir where parameter path can be rewritten.
Deteles it paramiko method rmdir. After successful download fires event ftp_after_remove_dir and returns bool. 

  .. code-block:: python
  
     res = c.remove_dir('/var/local/hydratk/test')      
     
tftp_client
^^^^^^^^^^^

Module provides class FTPClient which implements TFTP client using external module 
`tftpy <https://github.com/msoulier/tftpy/tree/master>`_ in version >= 0.6.2. 
When Python3 is used module is replaced by different branch `tftpy <https://github.com/ZuljinSBK/tftpy.git@master#egg=tftpy>` 

Unit tests available at hydratk/lib/network/ftp/tftp_client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - tftpy client instance
* _host - server hostname (or IP address)
* _port - port number (default 69)
* _verbose - bool, verbose mode
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.
* _timeout - auxiliary parameter (it has no getter)

**Properties (Getters)** :

* client - returns _client
* host - returns _host
* port - returns _port
* verbose - returns _verbose
* is_connected - returns _is_connected

**Methods** :

* __init__

Constructor called by FTPClient method. Turns verbose mode if enabled (tftpy method setLogLevel).

* connect

Connects to server (specified via parameters host, port).Sets _client to ftplib client instance (using constructor TftpClient).
First fires event ftp_before_connect where parameters can be rewritten. Connects to server using method paramiko methods connect, from_transport.
After successful connection fires event ftp_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.ftp.client import FTPClient
     
     c = FTPClient('TFTP')
     res = c.connect(host='127.0.0.1', port=69)    
     
* download_file

Downloads file from server. First fires event ftp_before_download_file where parameters (remote_path, local_path) can be rewritten.
Downloads file content using tftpy method download and writes it to local file (by default ./filename if local_path not specified).
After successful download fires event ftp_after_download_file and returns bool. 

  .. code-block:: python
  
     # default local path
     res = c.download_file('readme.txt')
     
     # given local path
     res = c.download_file('readme.txt', './')   
     
* upload_file

Uploads file to server. First fires event ftp_before_upload_file where parameters (local_path, remote_path) can be rewritten.
Uploads file content using tftpy method upload and writes it to remote file (by default ./filename if remote_path not specified).
After successful download fires event ftp_after_upload_file and returns bool. 

  .. code-block:: python
  
     # default remote path
     res = c.upload_file('readme.txt')
     
     # given remote path
     res = c.upload_file('readme.txt', './')                           