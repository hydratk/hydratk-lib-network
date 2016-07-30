# -*- coding: utf-8 -*-
"""TCP/UDP client

.. module:: network.inet.client
   :platform: Unix
   :synopsis: TCP/UDP client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
inet_before_connect
inet_after_connect
inet_before_send
inet_after_send
inet_before_receive
inet_after_receive

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from socket import socket, error, gethostbyaddr, getaddrinfo, setdefaulttimeout
from socket import AF_INET, AF_INET6, SOCK_STREAM, SOCK_DGRAM, SHUT_RDWR

class Client(object):
    """Class Client
    """

    _mh = None
    _lay3_prot = None
    _lay4_prot = None     
    _client = None
    _host = None
    _port = None
    _is_connected = None
    
    _protocols = {
      'IPV4': AF_INET,
      'IPV6': AF_INET6,
      'TCP' : SOCK_STREAM,
      'UDP' : SOCK_DGRAM
    }    
  
    def __init__(self, lay3_prot='IPv4', lay4_prot='TCP'): 
        """Class constructor
           
        Called when the object is initialized    
        
        Args:            
           lay3_prot (str): layer 3 protocol, IPV4|IPV6
           lay4_prot (str): layer 4 protocol, TCP|UDP
           
        Raises:
           error: NotImplementedError
                
        """           
       
        try:
      
            self._mh = MasterHead.get_head()
            self._mh.find_module('hydratk.lib.network.inet.client', None) 
        
            self._lay3_prot = lay3_prot.upper()
            self._lay4_prot = lay4_prot.upper()  
            if (self._lay3_prot not in self._protocols):
                raise NotImplementedError('Unknown protocol:{0}'.format(self._lay3_prot))   
            elif (self._lay3_prot not in self._protocols):
                raise NotImplementedError('Unknown protocol:{0}'.format(self._lay4_prot))       
            else:
                self._client = socket(self._protocols[self._lay3_prot], self._protocols[self._lay4_prot])
                
        except error as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False                  
            
    @property
    def lay3_prot(self):
        """ 3rd layer protocol property getter """
        
        return self._lay3_prot
    
    @property
    def lay4_prot(self):
        """ 4th layer protocol property getter """
        
        return self._lay4_prot
    
    @property
    def client(self):
        """ INET client property getter """
        
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
    def is_connected(self):
        """ is_connecte property getter """
        
        return self._is_connected      
    
    def connect(self, host, port, timeout=10):   
        """Method connects to server 
        
        Method is supported for TCP only
        
        Args:            
           host (str): host, name or IP address
           port (int): port
           timeout (int): connection timeout
           
        Returns:
           bool: result
           
        Raises:
           event: inet_before_connect
           event: inet_after_connect
                
        """                   
        
        try:     
            
            if (self._lay4_prot != 'TCP'):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_inet_unknown_method', self._lay4_prot), self._mh.fromhere())                 
                return False
            
            message = '{0}:{1} timeout:{2}'.format(host, port, timeout)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_inet_connecting', message), self._mh.fromhere())
            
            ev = event.Event('inet_before_connect', host, port)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                port = ev.argv(1) 
                timeout = ev.argv(2)   
                
            if (ev.will_run_default()):
                self._host = host
                self._port = port
                 
                self._client.settimeout(timeout)      
                self._client.connect((host, port))  
                self._is_connected = True    
                      
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_inet_connected'), self._mh.fromhere())
            ev = event.Event('inet_after_connect')
            self._mh.fire_event(ev)              
            
            return True
            
        except error as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False 
        
    def disconnect(self):
        """Method disconnects from server 
        
        Method is supported for TCP only
        
        Args:            
           
        Returns:
           bool: result
                
        """           
        
        try:
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_inet_not_connected'), self._mh.fromhere()) 
                return False                          
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_inet_disconnecting'), self._mh.fromhere())
            if (self._lay4_prot == 'TCP'):
                self._client.shutdown(SHUT_RDWR)
            self._client.close()
            self._is_connected = False
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_inet_disconnected'), self._mh.fromhere())
            
            return True
            
        except error as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False    
        
    def send(self, data, host=None, port=None):
        """Method sends data to server
        
        Args:            
           data (str): data
           host (str): host, name or IP address, for UDP only
           port (int): port, for UDP only
           
        Returns:
           bool: result
           
        Raises:
           event: inet_before_send
           event: inet_after_send
                
        """           
        
        try:  
            
            if (self._lay4_prot == 'TCP'):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_inet_sending_data', data), self._mh.fromhere())
                
                if (not self._is_connected):
                    self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_inet_not_connected'), self._mh.fromhere()) 
                    return False                
                
                ev = event.Event('inet_before_send', data)
                if (self._mh.fire_event(ev) > 0):
                    data = ev.argv(0) 
                    
                if (ev.will_run_default()):
                    self._client.sendall(data.encode('utf-8'))                      
                
            elif (self._lay4_prot == 'UDP'):
                message = '{0}, server: {1}:{2}'.format(data, host, port)                            
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_inet_sending_data', message), self._mh.fromhere())
                
                ev = event.Event('inet_before_send', data, host, port)
                if (self._mh.fire_event(ev) > 0):
                    data = ev.argv(0) 
                    host = ev.args(1)
                    port = ev.args(2)
                    
                if (ev.will_run_default()):
                    self._host = host if (host != None) else self._host
                    self._port = port if (port != None) else self._port
                    
                    self._client.sendto(data.encode('utf-8'), (self._host, self._port))
                    self._is_connected = True              
                 
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_inet_data_sent'), self._mh.fromhere())         
            ev = event.Event('inet_after_send')
            self._mh.fire_event(ev)               
            
            return True
            
        except error as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False       
        
    def receive(self, size=4096, timeout=10):
        """Method receives data from server
        
        Args:            
           size (int): buffer size
           timeout (float): receive timeout
           
        Returns:
           str: data
           
        Raises:
           event: inet_before_receive
           event: inet_after_receive
                
        """          
        
        try:  
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_inet_receiving_data', size), self._mh.fromhere())
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_inet_not_connected'), self._mh.fromhere()) 
                return None            
            
            ev = event.Event('inet_before_receive', size, timeout)
            if (self._mh.fire_event(ev) > 0):           
                size = ev.argv(0) 
                timeout = ev.argv(1)
            
            if (ev.will_run_default()):
                self._client.settimeout(timeout)
                
                if (self._lay4_prot == 'TCP'):
                    data = self._client.recv(size)
                    self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_inet_data_received', data), self._mh.fromhere()) 
                    
                elif (self._lay4_prot == 'UDP'):
                    data, ip = self._client.recvfrom(size)                     
                    message = '{0}, IP:{1}'.format(data, ip)
                    self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_inet_data_received', message), self._mh.fromhere()) 
                    
                self._client.settimeout(None)
                                      
            ev = event.Event('inet_after_receive')
            self._mh.fire_event(ev)            
            
            return data.decode()
            
        except error as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None                           
        
    def ip2name(self, ip):
        """Method translates IP address to name
        
        Args:            
           ip (str): IP address, IPv4|IPv6 format
           
        Returns:
           str: name           
                
        """          
        
        try:
        
            host = gethostbyaddr(ip)
            return (host[0] if (len(host) > 0) else None)
        
        except error as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None          
        
    def name2ip(self, name):  
        """Method translates name to IP address        
        Args:            
           name (str): hostname
           
        Returns:
           str: ip           
                
        """        
        
        try:
            
            addr = getaddrinfo(name, None)
            return (addr[0][4][0] if (len(addr) > 0) else None)
        
        except error as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None                       