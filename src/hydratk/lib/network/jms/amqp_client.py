# -*- coding: utf-8 -*-
"""AMQP client

.. module:: network.jms.amqp_client
   :platform: Unix
   :synopsis: AMQP client
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
from proton import Message, ProtonException, Timeout
from proton.utils import BlockingConnection
from proton.reactor import Copy
from logging import basicConfig, getLogger, DEBUG

mapping = {
  'JMSDeliveryMode' : 'header.durable',
  'JMSPriority'     : 'header-priority',
  'JMSExpiration'   : 'header.ttl',
  'JMSType'         : 'message-annotations.x-opt-jms-type',
  'JMSMessageID'    : 'properties.message-id',
  'JMSDestination'  : 'properties.to',
  'JMSReplyTo'      : 'properties.reply-to',
  'JMSCorrelationID': 'properties.correlation-id',
  'JMSTimestamp'    : 'properties.creation-time'
}

class JMSClient:
    """Class JMSClient
    """
    
    _mh = None
    _verbose = None
    _client = None
    _host = None
    _port = None
    _user = None
    _passw = None
    
    def __init__(self, verbose=False):
        """Class constructor
           
        Called when the object is initialized
        
        Args:                   
           verbose (bool): verbose mode
           
        """         
        
        try:
        
            self._mh = MasterHead.get_head() 
            
            self._verbose = verbose
            if (self._verbose):
                basicConfig()
                getLogger().setLevel(DEBUG)            
        
        except ProtonException as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())     
    
    @property
    def verbose(self):
        """ verbose mode property getter """
        
        return self._verbose        
            
    @property
    def client(self):
        """ AMQP client property getter """
        
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
    def user(self):
        """ username property getter """
        
        return self._user
    
    @property
    def passw(self):
        """ user password property getter """
        
        return self._passw         
    
    def connect(self, host, port=5672, user=None, passw=None):
        """Method connects to server
        
        Args:
           host (str): hostname
           port (str): port
           user (str): username
           passw (str): password

        Returns:
           bool: result
           
        Raises:
           event: jms_before_connect
           event: jms_after_connected            
                
        """        
        
        try:
        
            msg = 'host:{0}, port:{1}, user:{2}, passw:{3}'.format(host, port, user, passw)       
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_connecting', msg), self._mh.fromhere()) 
        
            ev = event.Event('jms_before_connect', host, port, user, passw)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv[0]
                port = ev.argv[1]
                user = ev.argv[2]
                passw = ev.argv[3]                 
        
            self._host = host
            self._port = port
            self._user = user
            self._passw = passw
            
            if (ev.will_run_default()):    
                if (self._user == None):         
                    self._client = BlockingConnection('amqp://{0}:{1}'.format(self._host, self._port))
                else:
                    self._client = BlockingConnection('amqp://{0}:{1}@{2}:{3}'.format(self._user, self._passw,
                                                                                      self._host, self._port))
        
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_connected'), self._mh.fromhere()) 
            ev = event.Event('jms_after_connect')
            self._mh.fire_event(ev)               
        
            return True
    
        except ProtonException as ex:
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
                
            self._client.close()           
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_disconnected'), self._mh.fromhere())
                
            return True
        
        except ProtonException as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return False      
        
    def send(self, destination_name, message, destination_type='queue', headers={}):
        """Method sends message
        
        JMS headers - JMSDeliveryMode, JMSPriority, JMSExpiration, JMSType, JMSMessageID,
                      JMSDestination, JMSReplyTo, JMSCorrelationID, JMSTimestamp
        
        Args:
           destination_name (str): queue|topic name
           message (str): message
           destination_type (str): queue|topic
           headers (dict): JMS headers, key - title, value - string

        Returns:
           bool: result
           
        Raises:
           event: jms_before_send
           event: jms_after_send             
                
        """   
        
        try:        
        
            msg = 'destination_name:{0}, message:{1}, destination_type:{2}, headers:{3}'.format(
                   destination_name, message, destination_type, headers)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_sending_msg', msg), self._mh.fromhere())         
        
            ev = event.Event('jms_before_send', destination_name, message, destination_type, headers)
            if (self._mh.fire_event(ev) > 0):        
                destination_name = ev.args[0]
                message = ev.args[1]
                destination_type = ev.args[2]
                headers = ev.args[3]
        
            if (ev.will_run_default()):                 
                sender = self._client.create_sender('{0}://{1}'.format(destination_type, destination_name))
                
                headers_new = {}
                for key, value in headers.items():
                    if (key in mapping):
                        headers_new[mapping[key]] = value
                                
                sender.send(Message(body=message, properties=headers_new))
                sender.close()
        
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_msg_sent'), self._mh.fromhere())  
            ev = event.Event('jms_after_send')
            self._mh.fire_event(ev)    

            return True 
    
        except ProtonException as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return False     
        
    def receive(self, destination_name, cnt=1):
        """Method receives messages
        
        Args:
           destination_name (str): queue name
           cnt (int): count of messages

        Returns:
           list:  messages as dictionary {'message', JMS headers}
           
        Raises:
           event: jms_before_receive
           event: jms_after_receive             
                
        """           
        
        try:
        
            msg = 'destination_name:{0}, count:{1}'.format(destination_name, cnt)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_receiving_msg', msg), self._mh.fromhere())         
        
            ev = event.Event('jms_before_receive', destination_name, cnt)
            if (self._mh.fire_event(ev) > 0):        
                destination_name = ev.args[0]
                cnt = ev.args[1]
        
            if (ev.will_run_default()): 
                receiver = self._client.create_receiver('queue://{0}'.format(destination_name))
                    
                msgs = []
                i = 0
                while (i < cnt):
                    try:
                        msg = receiver.receive(timeout=1)
                        receiver.accept()                           
                        msgs.append(msg)
                        i = i+1
                    except Timeout:
                        break                                     
                    
                messages = []    
                for msg in msgs:
                    
                    message = {}
                    message['message'] = msg.body
                    for key, value in msg.properties.items():
                        message[mapping.keys()[mapping.values().index(key)]] = value
                    
                    messages.append(message)                                                      
                
                receiver.close()
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_msg_received', len(messages)), self._mh.fromhere())  
            ev = event.Event('jms_after_receive')
            self._mh.fire_event(ev)                                                 
       
            return messages  
    
        except ProtonException as ex:
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
        
            ev = event.Event('jms_before_browse', destination_name, cnt)
            if (self._mh.fire_event(ev) > 0):        
                destination_name = ev.args[0]
                cnt = ev.args[1]
                jms_correlation_id = ev.args[2]
                jms_type = ev.args[3]
        
            if (ev.will_run_default()): 
                receiver = self._client.create_receiver('queue://{0}'.format(destination_name), options=Copy())
                    
                msgs = []
                i = 0
                while (i < cnt):
                    try:
                        msg = receiver.receive(timeout=1) 
                        receiver.accept()                       
                        correlation_id = None
                        type = None
                        for key, value in msg.properties.items():
                            if (key == 'properties.correlation-id'):
                                correlation_id = value
                            elif (key == 'message-annotations.x-opt-jms-type'):
                                type = value
                    
                        if ((jms_correlation_id == None or jms_correlation_id == correlation_id) and
                            (jms_type == None or jms_type == type)):
                            msgs.append(msg)  
                            i = i+1                                                                             

                    except Timeout:
                        break                                                                                            
                
                receiver.close()
                    
                messages = []    
                for msg in msgs:
                    
                    message = {}
                    message['message'] = msg.body
                    for key, value in msg.properties.items():
                        message[mapping.keys()[mapping.values().index(key)]] = value
                    
                    messages.append(message)                                                      
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_msg_received', len(messages)), self._mh.fromhere())  
            ev = event.Event('jms_after_browse')
            self._mh.fire_event(ev)                                                 
       
            return messages  
    
        except ProtonException as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None                             