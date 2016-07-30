# -*- coding: utf-8 -*-
"""JMS client

.. module:: network.jms.jms_client
   :platform: Unix
   :synopsis: JMS client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
jms_before_connect
jms_after_connect
jms_before_send
jms_after_send
jms_before_receive
jms_after_receive
jms_before_browse
jms_after_browse

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from hydratk.lib.bridge.java import JavaBridge

class JMSClient(object):
    """Class JMSClient
    """
    
    _mh = None
    _bridge = None
    _client = None
    _verbose = None
    _connection_factory = None
    _properties = None
    _is_connected = None
    
    def __init__(self, verbose=False, jvm_path=None, classpath=None, options=[]):
        """Class constructor
           
        Called when the object is initialized
        Uses Java client program to access JMS provider 
        
        Args:                   
           verbose (bool): verbose mode
           jvm_path (str): JVM location, default from configuration
           classpath (str): Java classpath, default from configuration
           options (list): JVM options
           
        """         
        
        try:
        
            self._mh = MasterHead.get_head()
            self._verbose = verbose    
          
            self._bridge = JavaBridge(jvm_path, classpath)
            self._bridge.start(options)  
            self._client = self._bridge.get_class('JMSClient', self._verbose) 
        
        except RuntimeError as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())       
        
    def close(self):
        """Method stops JVM  
        
        Args:
           none
        
        Returns:
           bool
                
        """  
        
        return self._bridge.stop()          
         
    @property
    def bridge(self):
        """ Java bridge property getter """
        
        return self._bridge

    @property
    def client(self):
        """ JMS client property getter """
        
        return self._client
    
    @property
    def verbose(self):  
        """ verbose mode property getter """ 
        
        return self._verbose
    
    @property
    def connection_factory(self):
        """ connection factory property getter """
        
        return self._connection_factory
    
    @property
    def properties(self):
        """ connection properties property getter """
        
        return self._properties               
    
    @property
    def is_connected(self):
        """ is_connected property getter """
        
        return self._is_connected         
        
    def connect(self, connection_factory, properties={}):
        """Method connects to server
        
        JMS properties - applet, authoritative, batchsize, dns_url,
                         initial_context_factory, language, object_factories, 
                         provider_url, referral, security_authentication,
                         security_credentials, security_principal, 
                         security_protocol, state_factories, url_pkg_prefixes
        
        Args:
           connection_factory: JMS connection factory
           properties (dict): JMS connection properties 

        Returns:
           bool: result
           
        Raises:
           event: jms_before_connect
           event: jms_after_connect            
                
        """        
        
        try:
        
            msg = 'connection_factory:{0}, properties:{1}'.format(connection_factory, properties)       
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_connecting', msg), self._mh.fromhere()) 
        
            ev = event.Event('jms_before_connect', connection_factory, properties)
            if (self._mh.fire_event(ev) > 0):
                connection_factory = ev.argv(0)
                properties = ev.argv(1)           
        
            self._connection_factory = connection_factory
            self._properties = properties
        
            if (ev.will_run_default()):             
                hashmap = self._bridge.init_hashmap(properties)
                result = bool(self._client.connect(self._connection_factory, hashmap))
        
            if (result):
                self._is_connected = True
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_connected'), self._mh.fromhere()) 
                ev = event.Event('jms_after_connect')
                self._mh.fire_event(ev)         
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_jms_connecting_error'), self._mh.fromhere())        
        
            return result
    
        except RuntimeError as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return False 
        
    def disconnect(self):
        """Method disconnects from server  
        
        Args:  
           none       

        Returns:
           bool: result
                
        """           
        
        try:
        
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_disconnecting'), self._mh.fromhere())
                
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_jms_not_connected'), self._mh.fromhere()) 
                return False                  
                
            result = bool(self._client.disconnect())
            if (result):
                self._is_connected = False
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_disconnected'), self._mh.fromhere())    
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_jms_disconnecting_error'), self._mh.fromhere())   
            
            return result
        
        except RuntimeError as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return False           
        
    def send(self, destination_name, message, destination_type='queue', headers={}):
        """Method sends message
        
        JMS headers - JMSCorrelationID, JMSDeliveryMode PERSISTENT|NON_PERSISTENT,
                      JMSDestination, JMSExpiration, JMSMessageID, JMSPriority, 
                      JMSRedelivered True|False, JMSReplyTo, JMSTimestamp, JMSType
        
        Args:
           destination_name (str): queue|topic name
           message (str): message
           destination_type (str): queue|topic
           headers {dict}: JMS headers, key - title, value - string

        Returns:
           bool: result
           
        Raises:
           event: jms_before_send
           event: jms_after_send             
                
        """   
        
        try:        
        
            msg = 'destination_name:{0}, message:{1}, destination_type:{2}, headers:{3}'.format(destination_name, message,
                  destination_type, headers)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_sending_msg', msg), self._mh.fromhere())         
        
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_jms_not_connected'), self._mh.fromhere()) 
                return False          
        
            ev = event.Event('jms_before_send', destination_name, message, destination_type, headers)
            if (self._mh.fire_event(ev) > 0):        
                destination_name = ev.argv(0)
                message = ev.argv(1)
                destination_type = ev.argv(2)
                headers = ev.argv(3)
        
            if (ev.will_run_default()): 
                hashmap = self._bridge.init_hashmap(headers)
                result = bool(self._client.send(destination_type, destination_name, hashmap, message))
        
            if (result):  
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_msg_sent'), self._mh.fromhere())  
                ev = event.Event('jms_after_send')
                self._mh.fire_event(ev)    
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_jms_sending_error'), self._mh.fromhere())                  
       
            return result 
    
        except RuntimeError as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return False           
    
    def receive(self, destination_name, cnt=1):
        """Method receives messages
        
        Args:
           destination_name (str): queue name
           cnt (int): count of messages

        Returns:
           list: messages as dictionary {'message', JMS headers}
           
        Raises:
           event: jms_before_receive
           event: jms_after_receive             
                
        """           
        
        try:
        
            msg = 'destination_name:{0}, count:{1}'.format(destination_name, cnt)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_receiving_msg', msg), self._mh.fromhere())         
        
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_jms_not_connected'), self._mh.fromhere()) 
                return None          
        
            ev = event.Event('jms_before_receive', destination_name, cnt)
            if (self._mh.fire_event(ev) > 0):        
                destination_name = ev.argv(0)
                cnt = ev.argv(1)
        
            if (ev.will_run_default()): 
                jms_messages = self._client.receive(destination_name, cnt)
        
            messages = []
            if (jms_messages != None):
                
                for msg in jms_messages:
                    messages.append({'JMSCorrelationID': msg.JMSCorrelationID, 'JMSDeliveryMode': msg.JMSDeliveryMode,
                                     'JMSDestination': msg.JMSDestination, 'JMSExpiration': msg.JMSExpiration,
                                     'JMSMessageID': msg.JMSMessageID, 'JMSPriority': msg.JMSPriority,
                                     'JMSRedelivered': msg.JMSRedelivered, 'JMSReplyTo': msg.JMSReplyTo,
                                     'JMSTimestamp': msg.JMSTimestamp, 'JMSType': msg.JMSType, 
                                     'message': msg.message
                                     })
                
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_msg_received', len(messages)), self._mh.fromhere())  
                ev = event.Event('jms_after_receive')
                self._mh.fire_event(ev)                                                 
            else:                   
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_jms_receiving_error'), self._mh.fromhere())
       
            return messages  
    
        except RuntimeError as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None        
        
    def browse(self, destination_name, cnt=100, jms_correlation_id=None, jms_type=None):
        """Method browses queue
        
        Args:
           destination_name (str): queue name
           cnt (int): count of messages
           jms_correlation_id (str): requested JMSCorrelationID
           jms_type (str): requested JMSType

        Returns:
           list: messages as dictionary {'message', JMS headers}
           
        Raises:
           event: jms_before_browse
           event: jms_after_browse       
                
        """           
        
        try:
        
            msg = 'destination_name:{0}, count:{1}, jms_correlation_id:{2}, jms_type:{3}'.format(
                  destination_name, cnt, jms_correlation_id, jms_type)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_browsing', msg), self._mh.fromhere())         
        
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_jms_not_connected'), self._mh.fromhere()) 
                return None          
        
            ev = event.Event('jms_before_browse', destination_name, cnt, jms_correlation_id, jms_type)
            if (self._mh.fire_event(ev) > 0):        
                destination_name = ev.argv(0)
                cnt = ev.argv(1)
                jms_correlation_id = ev.argv(2)
                jms_type = ev.argv(3)
        
            if (ev.will_run_default()): 
                jms_messages = self._client.browse(destination_name, cnt, jms_correlation_id, jms_type)
        
            messages = []
            if (jms_messages != None):
                
                for msg in jms_messages:
                    messages.append({'JMSCorrelationID': msg.JMSCorrelationID, 'JMSDeliveryMode': msg.JMSDeliveryMode,
                                     'JMSDestination': msg.JMSDestination, 'JMSExpiration': msg.JMSExpiration,
                                     'JMSMessageID': msg.JMSMessageID, 'JMSPriority': msg.JMSPriority,
                                     'JMSRedelivered': msg.JMSRedelivered, 'JMSReplyTo': msg.JMSReplyTo,
                                     'JMSTimestamp': msg.JMSTimestamp, 'JMSType': msg.JMSType, 
                                     'message': msg.message
                                     })
                
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_msg_received', len(messages)), self._mh.fromhere())  
                ev = event.Event('jms_after_browse')
                self._mh.fire_event(ev)                                                 
            else:                   
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_jms_browsing_error'), self._mh.fromhere())
       
            return messages  
    
        except RuntimeError as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None             