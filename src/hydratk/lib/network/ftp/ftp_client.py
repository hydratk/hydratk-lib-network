# -*- coding: utf-8 -*-
"""FTP client

.. module:: network.ftp.ftp_client
   :platform: Unix
   :synopsis: FTP client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
ftp_before_connect
ftp_after_connect
ftp_before_change_dir
ftp_before_download_file
ftp_after_download_file
ftp_before_upload_file
ftp_after_upload_file
ftp_before_delete_file
ftp_before_make_dir
ftp_before_remove_dir

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from ftplib import FTP, all_errors
from os import path, remove
from sys import version_info

if (not(version_info[0] == 2 and version_info[1] == 6)):
    from ftplib import FTP_TLS

class FTPClient(object):
    """Class FTPClient
    """
    
    _mh = None
    _client = None
    _secured = None
    _host = None
    _port = None
    _user = None
    _passw = None
    _path = None    
    _verbose = None
    _is_connected = None    
    
    def __init__(self, secured=False, verbose=False):
        """Class constructor
           
        Called when the object is initialized 
        
        Args:
           secured (bool): secured FTP           
           verbose (bool): verbose mode
           
        """         
        
        self._mh = MasterHead.get_head()
   
        self._secured = secured
        if (not self._secured):            
            self._client = FTP()
        else: 
            if (not(version_info[0] == 2 and version_info[1] == 6)):
                self._client = FTP_TLS()
            else:
                raise NotImplementedError('Secured mode is not supported for Python 2.6')              
                         
        self._verbose = verbose 
        if (self._verbose): 
            self._client.set_debuglevel(2) 
            
    @property
    def client(self):   
        """ FTP client property getter """      
        
        return self._client
    
    @property
    def secured(self):
        """ secured protocol mode property getter """ 
        
        return self._secured
    
    @property
    def host(self): 
        """ server host property getter """         
        
        return self._host
    
    @property
    def port(self): 
        """ server port property getter """         
        
        return self._port
    
    @property
    def user(self):   
        """ username property getter """       
        
        return self._user
    
    @property
    def passw(self): 
        """ user password property getter """         
        
        return self._passw 
    
    @property
    def path(self):
        """ remote path property getter """ 
        
        return self._path       
    
    @property
    def verbose(self):
        """ verbose mode property getter """ 
        
        return self._verbose   
    
    @property
    def is_connected(self):
        """ is_connected property getter """ 
        
        return self._is_connected                   
        
    def connect(self, host, port=21, user=None, passw=None, path='/', timeout=10):
        """Method connects to server
        
        Args:
           host (str): server host
           port (int): server port, default protocol port
           user (str): username
           passw (str): password
           path (str): server path
           timeout (int): timeout
           
        Returns:
           bool: result
           
        Raises:
           event: ftp_before_connect
           event: ftp_after_connect
                
        """          
        
        try:            
                   
            message = '{0}/{1}@{2}:{3}{4} timeout:{5}'.format(user, passw, host, port, path, timeout)                            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_connecting', message), self._mh.fromhere())
            
            ev = event.Event('ftp_before_connect', host, port, user, passw, path, timeout)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                port = ev.argv(1)
                user = ev.argv(2)
                passw = ev.argv(3)
                path = ev.argv(4)
                timeout = ev.argv(5)
                
            self._host = host
            self._port = port
            self._user = user
            self._passw = passw
            self._path = '/'                        
            
            if (ev.will_run_default()):    
                self._client.connect(self._host, self._port, timeout=timeout)             
            
                if (self._user != None):
                    self._client.login(self._user, self._passw)    
                    
                if (self._secured):
                    self._client.prot_p() 
                    
                self._is_connected = True              
                
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_connected'), self._mh.fromhere())        
                if (path != None):
                    self.change_dir(path)
                                            
            ev = event.Event('ftp_after_connect')
            self._mh.fire_event(ev)   
                                    
            return True
        
        except all_errors as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False
        
    def disconnect(self):
        """Method disconnects from server 
        
        Args:   
           none
           
        Returns:
           bool: result         
                
        """           
         
        try:
                       
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_ftp_not_connected'), self._mh.fromhere()) 
                return False
            else:                                             
                self._client.quit()
                self._is_connected = False            
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_disconnected'), self._mh.fromhere())  
                return True
            
        except all_errors as ex: 
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())       
            return False 
        
    def list_dir(self):
        """Method lists remote working directory   
        
        Args:  
           none   
           
        Returns:
           list: names         
                
        """           
        
        try: 
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_list_dir', self._path), self._mh.fromhere())
        
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_ftp_not_connected'), self._mh.fromhere()) 
                return False        
        
            names = self._client.nlst()
            if ('.' in names): names.remove('.')
            if ('..' in names): names.remove('..')            
                    
            return names  
    
        except all_errors as ex: 
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())       
            return None       
        
    def change_dir(self, path):
        """Method changes remote working directory
        
        Args:
           path (str): new remote path
        
        Returns:
           bool: result         
                
        Raises:
           event: ftp_before_change_dir        
                
        """           
        
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_change_dir', path), self._mh.fromhere())
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_ftp_not_connected'), self._mh.fromhere()) 
                return False            
            
            ev = event.Event('ftp_before_change_dir', path)
            if (self._mh.fire_event(ev) > 0):
                path = ev.argv(0)             
            
            if (ev.will_run_default()):
                self._client.cwd(path)
                self._path = self._client.pwd()             
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_cur_dir', self._path), self._mh.fromhere())  
            return True
         
        except all_errors as ex:
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
                with open(lpath, 'wb') as f:                   
                    self._client.retrbinary('RETR ' + remote_path, f.write) 
             
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_file_downloaded'), self._mh.fromhere()) 
            ev = event.Event('ftp_after_download_file')
            self._mh.fire_event(ev)   
              
            return True
 
        except all_errors as ex:
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
                with open(local_path, 'rb') as f:                   
                    self._client.storbinary('STOR ' + rpath, f)   
 
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_file_uploaded'), self._mh.fromhere()) 
            ev = event.Event('ftp_after_upload_file')   
            self._mh.fire_event(ev) 
            
            return True
 
        except all_errors as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())                    
            return False  
        
    def delete_file(self, path):  
        """Method deletes file from server
        
        Args:
           path (str): remote path
           
        Returns:
           bool: result
           
        Raises:
           event: ftp_before_delete_file         
                
        """             
        
        try:

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_deleting_file', path), self._mh.fromhere())
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_ftp_not_connected'), self._mh.fromhere()) 
                return False            
            
            ev = event.Event('ftp_before_delete_file', path)
            if (self._mh.fire_event(ev) > 0):
                path = ev.argv(0)            
            
            if (ev.will_run_default()):
                self._client.delete(path)            
             
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_file_deleted'), self._mh.fromhere())        
            return True              
            
        except all_errors as ex:     
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())                             
            return False   
        
    def make_dir(self, path): 
        """Method makes directory on server
        
        Args:
           path (str): remote path
           
        Returns:
           bool: result
           
        Raises:
           event: ftp_before_make_dir         
                
        """              
        
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_making_dir', path), self._mh.fromhere())
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_ftp_not_connected'), self._mh.fromhere()) 
                return False            
            
            ev = event.Event('ftp_before_make_dir', path)
            if (self._mh.fire_event(ev) > 0):
                path = ev.argv(0)            
            
            if (ev.will_run_default()):
                self._client.mkd(path)              
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_dir_made'), self._mh.fromhere())    
            return True
                      
        except all_errors as ex:     
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())                             
            return False              
        
    def remove_dir(self, path): 
        """Method removes directory from server
        
        Args:
           path (str): remote path
           
        Returns:
           bool: result
           
        Raises:
           event: ftp_before_remove_dir        
                
        """                 
        
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_removing_dir', path), self._mh.fromhere())  
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_ftp_not_connected'), self._mh.fromhere()) 
                return False            
            
            ev = event.Event('ftp_before_remove_dir', path)
            if (self._mh.fire_event(ev) > 0):
                path = ev.argv(0)                     
            
            if (ev.will_run_default()):
                self._client.rmd(path)             
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_dir_removed'), self._mh.fromhere())     
            return True
                      
        except all_errors as ex:     
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())                             
            return False                                    