# -*- coding: utf-8 -*-
"""TFTP client

.. module:: network.ftp.tftp_client
   :platform: Unix
   :synopsis: TFTP client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
ftp_before_connect
ftp_after_connect
ftp_before_download_file
ftp_after_download_file
ftp_before_upload_file
ftp_after_upload_file

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from tftpy import TftpShared, TftpClient
from os import path, remove

class FTPClient(object):
    """Class FTPClient
    """
    
    _mh = None
    _client = None
    _host = None
    _port = None
    _verbose = None
    _is_connected = None
    _timeout = None
    
    def __init__(self, verbose=False):
        """Class constructor
           
        Called when the object is initialized 
        
        Args:        
           verbose (bool): verbose mode
           
        """         
        
        self._mh = MasterHead.get_head()
                         
        self._verbose = verbose 
        if (self._verbose):              
            TftpShared.setLogLevel(2)
            
    @property
    def client(self):  
        """ TFTP client property getter """         
        
        return self._client
    
    @property
    def host(self): 
        """ server host property getter """          
        
        return self._host
    
    @property
    def port(self):  
        """ server port property getter """         
        
        return self._port
    
    @property
    def verbose(self):
        """ verbose mode property getter """  
        
        return self._verbose  
    
    @property
    def is_connected(self):
        """ is_connected property getter """  
        
        return self._verbose                        
        
    def connect(self, host, port=69, timeout=10):
        """Method connects to server
        
        Args:
           host (str): server host
           port (int): server port, default protocol port
           timeout (int): timeout
           
        Returns:
           bool: result
           
        Raises:
           event: ftp_before_connect
           event: ftp_after_connect
                
        """          
        
        try:            
                          
            message = '{0}:{1} timeout:{2}'.format(host, port, timeout)                            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_connecting', message), self._mh.fromhere())
            
            ev = event.Event('ftp_before_connect', host, port, timeout)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                port = ev.argv(1)
                timeout = ev.argv(2)
                
            self._host = host
            self._port = port  
            self._timeout = timeout                    
            
            if (ev.will_run_default()):    
                self._client = TftpClient(self._host, self._port)  
                self._is_connected = True                            
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_connected'), self._mh.fromhere())        
                                            
            ev = event.Event('ftp_after_connect')
            self._mh.fire_event(ev)   
                                    
            return True
        
        except TftpShared.TftpException as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False
        
    def download_file(self, remote_path, local_path=None):
        """Method downloads file from server
        
        Args:
           remote_path (str): remote path
           local_path (str): local path, default ./filename
           
        Returns:
           bool: result         
            
        Raises:
           event: ftp_before_download_file
           event: ftp_after_download_file    
            
        """           
        
        try:
            
            self._mh.dmsg('htk_on_debug_info',self._mh._trn.msg('htk_ftp_downloading_file', remote_path), self._mh.fromhere())
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_ftp_not_connected'), self._mh.fromhere()) 
                return False            
            
            ev = event.Event('ftp_before_download_file', remote_path, local_path)
            if (self._mh.fire_event(ev) > 0):
                remote_path = ev.argv(0)  
                local_path = ev.argv(1)                        
            
            if (local_path != None and not path.exists(local_path)):
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_ftp_unknown_dir', local_path), self._mh.fromhere())  
                return False            
            
            filename = remote_path.split('/')[-1]
            lpath = filename if (local_path == None) else path.join(local_path, filename)
              
            if (ev.will_run_default()):                      
                self._client.download(filename, lpath, timeout=self._timeout)
             
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_file_downloaded'), self._mh.fromhere()) 
            ev = event.Event('ftp_after_download_file')
            self._mh.fire_event(ev)   
              
            return True
 
        except (TftpShared.TftpException, IOError) as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            if (path.exists(lpath)):
                remove(lpath)                     
            return False  
        
    def upload_file(self, local_path, remote_path=None):
        """Method uploads file to server
        
        Args:
           local_path (str): local path
           remote_path (str): remote path, default ./filename
           
        Returns:
           bool: result
           
        Raises:
           event: ftp_before_upload_file
           event: ftp_after_upload_file    
                
        """           
        
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_uploading_file', local_path), self._mh.fromhere())
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_ftp_not_connected'), self._mh.fromhere()) 
                return False            
            
            ev = event.Event('ftp_before_upload_file', local_path, remote_path)
            if (self._mh.fire_event(ev) > 0):
                local_path = ev.argv(0)
                remote_path = ev.argv(1)  
            
            if (not(path.exists(local_path) or path.exists(path.relpath(local_path)))):
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_ftp_unknown_file', local_path), self._mh.fromhere())  
                return False
            
            filename = local_path.split('/')[-1]
            rpath = filename if (remote_path == None) else path.join(remote_path, filename)            
            
            if (ev.will_run_default()):
                self._client.upload(rpath, local_path, timeout=self._timeout)   
 
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_file_uploaded'), self._mh.fromhere()) 
            ev = event.Event('ftp_after_upload_file')   
            self._mh.fire_event(ev) 
            
            return True
 
        except (TftpShared.TftpException, IOError) as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())                    
            return False  
                               