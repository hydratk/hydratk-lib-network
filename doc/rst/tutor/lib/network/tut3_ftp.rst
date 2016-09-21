.. _tutor_network_tut3_ftp:

Tutorial 3: FTP
===============

This sections shows several examples how to use FTP client.

API
^^^

Module hydratk.lib.network.ftp.client.

Method FTPClient is factory method which requires attribute engine to create 
proper FTPClient object instance. Additional attributes are passed as args, kwargs. 

Supported protocols:

* FTP/FTPS: module ftp_client
* SFTP/SFTP: module sftp_client
* TFTP: module tftp_client

  .. note::
  
     FTPS is not supported for version Py2.6.

Methods:

* connect: connect to server
* disconnect: disconnect from server (FTP, SFTP)
* list_dir: get directory content (FTP, SFTP)
* change_dir: change remote directory (FTP, SFTP)
* download_file: download file from server
* upload_file: upload file to server
* delete_file: delete file on server (FTP, SFTP)
* make_dir: make directory on server (FTP, SFTP)
* remove_dir: remove directory from server (FTP, SFTP)

  .. note::
   
     API uses HydraTK core functionalities so it must be running.

FTP
^^^

  .. code-block:: python
  
     # import library
     from hydratk.lib.network.ftp.client import FTPClient as ftp
    
     # initialize client
     client = ftp('ftp')
     
     # connect to FTP server
     # returns bool
     client.connect(host='srv8.endora.cz', user='aaa', passw='bbb')
     
     # change directory
     # returns bool
     client.change_dir('/lynus.cekuj.net/web')
     
     # get directory content
     # returns file and directory names
     names =  client.list_dir()
     
     # download file from server
     # returns bool
     client.download_file('/lynus.cekuj.net/web/index.php') 
     
     # upload file to server
     # returns bool
     client.upload_file('index2.php', '/lynus.cekuj.net/web')
     
     # delete file from server
     # returns bool
     client.delete_file('index2.php')
     
     # make directory on server
     # returns bool
     client.make_dir('pokus2')
     
     # remove directory from server
     # returns bool
     client.remove_dir('pokus2')   
     
     # disconnect from server
     # returns bool
     client.disconnect()
     
  .. note::
   
     FTPS client is initialized using constructor attribute secured=True.     

SFTP
^^^^ 

  .. code-block:: python
  
     # import library
     from hydratk.lib.network.ftp.client import FTPClient as ftp
    
     # initialize client 
     client = ftp.FTPClient('sftp')
  
     # connect to SFTP server using password, certificate
     client.connect(host='127.0.0.1', port=22, user='aaa', passw='bbb')
     client.connect(host='127.0.0.1', port=22, user='aaa', cert='/home/lynus/key.pri')
     
     # change dicrector
     # returns bool
     client.change_dir('/appl/home/x0549396/portal')
     
     # get directory content
     # returns files and directory names
     client.list_dir()

     # download file from server
     # returns bool
     client.download_file('response.xml')

     # upload file to server
     # returns bool
     client.upload_file('index.php', '/appl/home/portal')
     
     # delete file from server
     # returns bool
     client.delete_file('index.php')
     
     # make directory on server
     # returns bool
     client.make_dir('pokus2')
     
     # remove directory from server
     # returns bool
     client.remove_dir('pokus2')   
     
     # disconnect from server
     # returns bool
     client.disconnect()     

TFTP
^^^^

  .. code-block:: python
  
     # import library
     from hydratk.lib.network.ftp.client import FTPClient as ftp
    
     # initialize client 
     client = ftp.FTPClient('tftp')
     
     # connect to TFTP server
     # returns bool
     client.connect(host='0.0.0.0')  
     
     # download file from server
     # returns bool
     client.download_file('/doc/bdd.txt2')  
     
     # upload file to server
     # returns bool
     client.upload_file('pok.txt', '/doc2') 