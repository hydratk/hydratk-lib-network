# -*- coding: utf-8 -*-
"""SSH client

.. module:: network.lib.ssh_client
   :platform: Unix
   :synopsis: SSH client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
term_before_connect
term_after_connect
term_before_exec_command
term_after_exec_command

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import SSHException, NoValidConnectionsError
from socket import error
from logging import basicConfig, DEBUG

class TermClient(object):
    """Class TermClient
    """
    
    _mh = None
    _client = None
    _host = None    
    _port = None
    _user = None
    _passw = None
    _verbose = None
    _is_connected = None
    
    def __init__(self, verbose=False):
        """Class constructor
           
        Called when the object is initialized 
        
        Args:      
           verbose (bool): verbose mode
           
        """          
        
        self._mh = MasterHead.get_head()         
        self._client = SSHClient()   
                         
        self._verbose = verbose 
        if (self._verbose):            
            basicConfig(level=DEBUG)
            
    @property
    def client(self):
        """ SSH client property getter """
        
        return self._client
    
    @property
    def host(self):
        """ server host property getter """
        
        return self._host
    
    @property
    def port(self):
        """ Sserver port property getter """
        
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
    def verbose(self):
        """ verbose mode property getter """
        
        return self._verbose   
    
    @property
    def is_connected(self): 
        """ is client connected property getter """
        
        return self._is_connected                
                
    def connect(self, host, port=22, user=None, passw=None, timeout=10):
        """Method connects to server
        
        Args:
           host (str): server host
           port (int): server port, default protocol port
           user (str): username
           passw (str): password
           timeout (int): timeout           
           
        Returns:
           bool: result
           
        Raises:
           event: term_before_connect
           event: term_after_connect          
                
        """                  
        
        try:
            
            message = '{0}/{1}@{2}:{3} timeout:{4}'.format(user, passw, host, port, timeout)                            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_term_connecting', message), self._mh.fromhere())
            
            ev = event.Event('term_before_connect', host, port, user, passw, timeout)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                port = ev.argv(1)
                user = ev.argv(2)
                passw = ev.argv(3)                    
                timeout = ev.argv(4)
            
            self._host = host
            self._port = port
            self._user = user
            self._passw = passw
            
            if (ev.will_run_default()):                  
                self._client.set_missing_host_key_policy(AutoAddPolicy())
                self._client.connect(self._host, self._port, self._user, self._passw, timeout=timeout)                
                self._is_connected = True
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_term_connected'), self._mh.fromhere()) 
            ev = event.Event('term_after_connect')
            self._mh.fire_event(ev)   
                                                   
            return True
        
        except (SSHException, NoValidConnectionsError, error) as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._client.close()            
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
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_term_not_connected'), self._mh.fromhere()) 
                return False
            else:                
                self._client.close()
                self._is_connected = False
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_term_disconnected'), self._mh.fromhere())  
                return True  
    
        except (SSHException, NoValidConnectionsError, error) as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False                    
    
    def exec_command(self, command, input=None):
        """Method executes command
           
        Args:
           command (str): command
           input (str): input for interactive mode         
           
        Returns:
           tuple: result (bool), output (list) (stdout for result True, stderr for result False) 
           
        Raises:
           event: term_before_exec_command
           event: term_after_exec_command   
                
        """         
        
        try:
        
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_term_executing_command', command), self._mh.fromhere())              
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_term_not_connected'), self._mh.fromhere()) 
                return False            
            
            ev = event.Event('term_before_exec_command', command)
            if (self._mh.fire_event(ev) > 0):
                command = ev.argv(0)            
            
            if (ev.will_run_default()): 
                stdin, stdout, stderr = self._client.exec_command(command)
                
                if (input != None):
                    stdin.write(input + '\n')
                    stdin.flush()
                
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_term_command_executed'), self._mh.fromhere())
                ev = event.Event('term_after_exec_command')
                self._mh.fire_event(ev)               
            
                err = stderr.read().splitlines()            
                if (len(err) > 0 and input == None):
                    raise SSHException(err)
                else:
                    out = stdout.read().splitlines()
                    out = out if (len(out) > 0) else None
                    return True, out
            
        except (SSHException, NoValidConnectionsError, error) as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False, [str(ex)]                                