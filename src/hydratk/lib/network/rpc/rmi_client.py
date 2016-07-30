# -*- coding: utf-8 -*-
"""Java RMI client

.. module:: network.rpc.rmi_client
   :platform: Unix
   :synopsis: Java RMI client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
rpc_before_init_proxy
rpc_after_init_proxy
rpc_before_call_method
rpc_after_call_method

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from hydratk.lib.bridge.java import JavaBridge

class RPCClient(object):
    """Class RPCClient
    """
    
    _mh = None
    _bridge = None
    _proxy = None
    
    def __init__(self, jvm_path=None, classpath=None, options=[]):
        """Class constructor
           
        Called when the object is initialized
        Uses Java client program to access JMS provider 
        
        Args:                   
           jvm_path (str): JVM location, default from configuration
           classpath (str): Java classpath, default from configuration
           options (list): JVM options
           
        """         
        
        try:
        
            self._mh = MasterHead.get_head() 
          
            self._bridge = JavaBridge(jvm_path, classpath)
            self._bridge.start(options)  
        
        except RuntimeError as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())       
        
    def close(self):
        """Method stops JVM  
        
        Args:
           none
        
        Returns:
           void
                
        """  
        
        return self._bridge.stop()
        
    @property
    def bridge(self):
        """ Java bridge property getter """
        
        return self._bridge
    
    @property
    def proxy(self):
        """ proxy object property getter """
        
        return self._proxy
        
    def init_proxy(self, url):            
        """Method initializes proxy to remote object
        
        Args:            
           url (str): remote object url
           
        Returns:
           bool: result
           
        Raises:
           event: rpc_before_init_proxy
           event: rpc_after_init_proxy
                
        """        
        
        try:
                  
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_rpc_init_proxy', url), self._mh.fromhere())
            
            ev = event.Event('rpc_before_init_proxy', url)
            if (self._mh.fire_event(ev) > 0):
                url = ev.argv(0)            
            
            if (ev.will_run_default()):      
                self._proxy = self._bridge.get_package('java').rmi.Naming.lookup(url)
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_rpc_proxy_initialized'), self._mh.fromhere())
            ev = event.Event('rpc_after_init_proxy')
            self._mh.fire_event(ev)                 
                
            return True
    
        except (RuntimeError, Exception) as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return False
            
    def call_method(self, name, *args):   
        """Method call remote method
        
        Args:         
           name (str): method name   
           args (args): method parameters
             
        Returns:
           obj: method output
           
        Raises:
           event: rpc_before_call_method
           event: rpc_after_call_method
                
        """         
        
        try:
                    
            args = list(args)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_rpc_call_method', name, args), self._mh.fromhere())
            
            if (self._proxy == None):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_rpc_proxy_not_init'), self._mh.fromhere())
                return None
            
            ev = event.Event('rpc_before_call_method', name, args)
            if (self._mh.fire_event(ev) > 0):
                name = ev.argv(0)
                args = ev.argv(1)                      
                  
            if (ev.will_run_default()):          
                output = getattr(self._proxy, name)(*args)
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_rpc_method_called', output), self._mh.fromhere())
            ev = event.Event('rpc_after_call_method')
            self._mh.fire_event(ev)                 
                
            return output
    
        except (RuntimeError, AttributeError) as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None                          