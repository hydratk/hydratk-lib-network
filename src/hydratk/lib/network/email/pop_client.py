# -*- coding: utf-8 -*-
"""POP email client

.. module:: network.email.pop_client
   :platform: Unix
   :synopsis: POP email client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
email_before_connect
email_after_connect
email_before_receive_email
email_after_receive_email

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from poplib import POP3, POP3_SSL, error_proto
from socket import error
from string import replace

class EmailClient:
    """Class EmailClient
    """
    
    _mh = None
    _client = None
    _secured = None
    _host = None    
    _port = None
    _user = None
    _passw = None
    _verbose = None
    
    def __init__(self, secured=False, verbose=False):
        """Class constructor
           
        Called when the object is initialized 
        
        Args:
           secured (bool): secured POP   
           verbose (bool): verbose mode    
           
        """         
        
        self._mh = MasterHead.get_head()
        self._secured = secured 
        self._verbose = verbose   
            
    @property
    def client(self):
        """ POP client property getter """
        
        return self._client
    
    @property
    def secured(self):
        """ secured property getter """
        
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
    def verbose(self):
        """ verbose mode property getter """
        
        return self._verbose                    
                
    def connect(self, host, port=None, user=None, passw=None):
        """Method connects to server
        
        Args:
           host (str): server host
           port (str): server port, default protocol port
           user (str): username
           passw (str): password

        Returns:
           bool: result         
             
        Raises:
           event: email_before_connect
           event: email_after_connect     
                
        """                  
        
        try:
            
            if (port == None):
                port = 110 if (not self._secured) else 995
                
            message = '{0}/{1}@{2}:{3}'.format(user, passw, host, port)                            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_connecting', message), self._mh.fromhere())
            
            ev = event.Event('email_before_connect', host, port, user, passw)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                port = ev.argv(1)
                user = ev.argv(2)
                passw = ev.argv(3)               
            
            self._host = host
            self._port = port
            self._user = user
            self._passw = passw
            
            if (ev.will_run_default()):  
                                
                if (not self._secured):
                    self._client = POP3(self._host, self._port) 
                else:
                    self._client = POP3_SSL(self._host, self._port) 
                           
                if (self._verbose):
                    self._client.set_debuglevel(2)                                          
                    
                if (self._user != None):
                    self._client.user(self._user)
                    self._client.pass_(self._passw)                        
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_connected'), self._mh.fromhere()) 
            ev = event.Event('email_after_connect')
            self._mh.fire_event(ev)   
                                                   
            return True
        
        except (error_proto, error) as ex:
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
                
            self._client.quit()                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_disconnected'), self._mh.fromhere())  
            return True  
    
        except (error_proto, error) as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False    
        
    def email_count(self):
        """Method gets email count   
        
        Args: 
           none    
           
        Returns: 
           int: count       
                
        """         
                
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_counting'), self._mh.fromhere())              
            count = self._client.stat()[0]        
              
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_count', count), self._mh.fromhere())      
            return count              
            
        except (error_proto, error), ex: 
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None      
        
    def list_emails(self):
        """Method gets email list
        
        Args:
           none
           
        Returns: 
           list: email ids       
                
        """         
                
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_listing'), self._mh.fromhere())          
            
            msg_list = self._client.list()[1]                                 
            emails = []
            for msg in msg_list:
                emails.append(msg.split(' ')[0])                                                                                                   
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_listed'), self._mh.fromhere())         
            return emails
            
        except (error_proto, error) as ex: 
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None  
        
    def receive_email(self, msg_id):  
        """Method receives email
           
        Args:
           msg_id (str) - email id 
           
        Returns: 
           tuple: sender (str), recipients (list), cc (list), subject (str), message (str)     
           
        Raises:
           event: email_before_receive_email
           event: email_after_receive_email   
                
        """         
                
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_receiving', msg_id), self._mh.fromhere())  
            
            ev = event.Event('email_before_receive_email', msg_id)
            if (self._mh.fire_event(ev) > 0):
                msg_id = ev.argv(0)          
            
            if (ev.will_run_default()):                        
                msg = self._client.retr(msg_id)[1]                                                                                                                                      
                
            msg_found = False
            message = ''
            sender = None
            recipients = None
            cc = None
            subject = None
            
            for line in msg:
                if (not msg_found):
                    if ('From: ' in line):
                        sender = replace(line, ('From: '), '')
                    elif ('To: ' in line):
                        recipients = replace(line, ('To: '), '')
                        recipients = recipients.split(',') 
                    elif ('CC: ' in line):
                        cc = replace(line, ('CC: '), '') 
                        cc = cc.split(',') 
                    elif ('Subject: ' in line):
                        subject = replace(line, ('Subject: '), '')
                    elif ('Inbound message' in line):
                        msg_found = True
                else:
                        message += line + '\r\n'            
                
            ev = event.Event('email_after_receive_email')
            self._mh.fire_event(ev)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_received'), self._mh.fromhere())  

            return (sender, recipients, cc, subject, message)                                                       
            
        except (error_proto, error) as ex: 
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None                                                                            