# -*- coding: utf-8 -*-
"""Simple JMS client for request based processing

.. module:: network.jms.simplejms
   :platform: Unix
   :synopsis: Simple JMS client for request based processing
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from hydratk.lib.network.jms import jms_client
from hydratk.lib.system import fs

class JMSClient(jms_client.JMSClient, object):
    """Class JMSClient
    """
    
    _request   = None    
    _response  = None
    
    @property
    def request(self):
        """ request property getter, setter """
        
        return self._request
    
    @request.setter
    def request(self, req):
        """ request property setter """
        
        self._request = req
    
    @property
    def response(self):
        """ response property getter """
        
        return self._response
    
    def send(self, jms_correlation_id):
        """Methods sends message

        Args:
           jms_correlation_id (str): JMSCorrelationID

        Returns:
           bool: result
    
        """
                
        return jms_client.JMSClient.send(
                               self, 
                               self._request.destination_queue, 
                               self._request.message.content, 
                               headers={'JMSType': self._request.jms_type, 
                                        'JMSCorrelationID': jms_correlation_id}
                             )
               
class JMSRequest(object):
    """Class JMSRequest
    """
    
    _msg                   = None
    _destination_queue     = None
    _jms_type              = None        
    
    def __init__(self, destination_queue, jms_type):  
        """Class constructor
        
        Called when object is initialized

        Args:
           destination_queue (str): queue
           jms_type (str): JMSType
    
        """          
            
        self._destination_queue = destination_queue
        self._jms_type          = jms_type      
        
    @property
    def destination_queue(self):
        """ destination_queue property getter, setter """
        
        return self._destination_queue
    
    @destination_queue.setter
    def destination_queue(self, queue):
        """ destination queue property setter """
        
        self._destination_queue = queue
    
    @property
    def jms_type(self):
        """ jms_type property getter, setter """
        
        return self._jms_type
    
    @jms_type.setter
    def jms_type(self, type):
        """ jms_type property setter """
        
        self._jms_type = type
    
    @property
    def msg(self):
        """ msg property getter, setter """
        
        return self._msg
    
    @msg.setter
    def msg(self, msg):
        """ msg property setter """
        
        self._msg = msg   
                     
    @property
    def message(self):
        """ message property getter, setter """
        
        return self._msg
    
    @message.setter
    def message(self, msg):
        """ message property setter """
        
        self._msg = msg
        
class JMSRequestMessage(object):
    """Class JMSRequestMessage
    """
    
    _bind_lchr = '['
    _bind_rchr = ']'
    _content   = None
    
    def __init__(self, content=None, source='file'):
        """Class constructor
        
        Called when object is initialized

        Args:
           content (str): filename including path if source=file
                          message content if source=str
           source (str): content source, file|str
    
        """
                
        if content is not None:
            if source == 'file':
                self.load_from_file(content)
            if source == 'str':
                self._content = content  
                
    @property
    def content(self):
        """ content property getter, setter """
                
        return self._content
    
    @content.setter
    def content(self, content):
        """ content property setter """
        
        self._content = content
    
    def load_from_file(self, msg_file):
        """Methods loads message content from file

        Args:
           msg_file (str): filename including path

        Returns:
           void
    
        """
                
        self._content = fs.file_get_contents(msg_file)             
        
    def bind_var(self, *args, **kwargs):
        """Methods binds input data to message template

        Args:
           args (arg): arguments
           kwargs (kwargs): key value arguments

        Returns:
           void
    
        """
                
        if self._content is not None:
            content = str(self._content)
            for bdata in args:
                for var,value in bdata.items():
                    bind_var = '{bind_lchr}{var}{bind_rchr}'.format(bind_lchr=self._bind_lchr,var=var,bind_rchr=self._bind_rchr)                
                    content = content.replace(str(bind_var), str(value))
            for var, value in kwargs.items():
                bind_var = '{bind_lchr}{var}{bind_rchr}'.format(bind_lchr=self._bind_lchr,var=var,bind_rchr=self._bind_rchr)                
                content = content.replace(str(bind_var), str(value))                
            self._content = content    
            
class JMSResponse(object):
    pass  