# -*- coding: utf-8 -*-
"""IMAP email client

.. module:: network.email.imap_client
   :platform: Unix
   :synopsis: IMAP email client
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
from imaplib import IMAP4, IMAP4_SSL
from socket import error, setdefaulttimeout
from sys import version_info

if (version_info[0] == 2):
    from string import replace

class EmailClient(object):
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
    _is_connected = None
    
    def __init__(self, secured=False, verbose=False):
        """Class constructor
           
        Called when the object is initialized 
        
        Args:
           secured (bool): secured IMAP  
           verbose (bool): verbose mode     
           
        """         
        
        self._mh = MasterHead.get_head()
        self._secured = secured 
        self._verbose = verbose   
            
    @property
    def client(self):
        """ IMAP client property getter """
        
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
    
    @property
    def is_connected(self):
        """ is_connected property getter """
        
        return self._is_connected                   
                
    def connect(self, host, port=None, user=None, passw=None, timeout=10):
        """Method connects to server
        
        Args:
           host (str): server host
           port (str): server port, default protocol port
           user (str): username
           passw (str): password
           timeout (int): timeout

        Returns:
           bool: result         
             
        Raises:
           event: email_before_connect
           event: email_after_connect     
                
        """                  
        
        try:
            
            if (port == None):
                port = 143 if (not self._secured) else 993
                
            message = '{0}/{1}@{2}:{3} timeout:{4}'.format(user, passw, host, port, timeout)                            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_connecting', message), self._mh.fromhere())
            
            ev = event.Event('email_before_connect', host, port, user, passw, timeout)
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
                
                setdefaulttimeout(timeout)                
                if (not self._secured):
                    self._client = IMAP4(self._host, self._port) 
                else:
                    self._client = IMAP4_SSL(self._host, self._port) 
                           
                if (self._verbose):
                    self._client.debug = 4                                       
                    
                if (self._user != None):
                    self._client.login(self._user, self._passw)  
                    
                self._is_connected = True                     
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_connected'), self._mh.fromhere()) 
            ev = event.Event('email_after_connect')
            self._mh.fire_event(ev)   
                                                   
            return True
        
        except (IMAP4.error, error) as ex:
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
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_email_not_connected'), self._mh.fromhere()) 
                return False
            else:                
                self._client.shutdown() 
                self._is_connected = False              
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_disconnected'), self._mh.fromhere())  
                return True  
    
        except (IMAP4.error, error) as ex:
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
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_email_not_connected'), self._mh.fromhere()) 
                return None
                                    
            count = int(self._client.select()[1][0])        
              
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_count', count), self._mh.fromhere())      
            return count              
            
        except (IMAP4.error, error) as ex: 
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
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_email_not_connected'), self._mh.fromhere()) 
                return None                      
            
            self._client.select()
            msg_list = self._client.search(None, 'ALL')[1][0]
            emails = msg_list.split(' ') if (version_info[0] == 2) else msg_list.split(b' ')
            
            if (version_info[0] == 3):
                for i in range(0, len(emails)):
                    emails[i] = emails[i].decode()                                                                                                  
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_listed'), self._mh.fromhere())         
            return emails
            
        except (IMAP4.error, error) as ex: 
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
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_email_not_connected'), self._mh.fromhere()) 
                return None            
            
            ev = event.Event('email_before_receive_email', msg_id)
            if (self._mh.fire_event(ev) > 0):
                msg_id = ev.argv(0)          
            
            if (ev.will_run_default()):  
                self._client.select()                      
                msg = self._client.fetch(str(msg_id), '(RFC822)')[1][0][1]
                msg = msg.split('\r\n') if (version_info[0] == 2) else msg.split(b'\r\n')                                                                                                                                      
                
            msg_found = False
            sender = None
            recipients = None
            cc = None
            subject = None
            message = ''
            
            for line in msg:
                if (not msg_found):
                    if (version_info[0] == 3):
                        line = line.decode()
                    if ('From: ' in line):
                        sender = replace(line, ('From: '), '') if (version_info[0] == 2) else line.replace('From: ', '')
                    elif ('To: ' in line):
                        recipients = replace(line, ('To: '), '') if (version_info[0] == 2) else line.replace('To: ', '')
                        recipients = recipients.split(',')
                    elif ('CC: ' in line):
                        cc = replace(line, ('CC: '), '') if (version_info[0] == 2) else line.replace('CC: ', '')
                        cc = cc.split(',') 
                    elif ('Subject: ' in line):
                        subject = replace(line, ('Subject: '), '') if (version_info[0] == 2) else line.replace('Subject: ', '')
                    elif ('Inbound message' in line):
                        msg_found = True
                else:
                        message += str(line) + '\r\n'                
               
            ev = event.Event('email_after_receive_email')
            self._mh.fire_event(ev)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_received'), self._mh.fromhere())  

            return (sender, recipients, cc, subject, message)                                                       
            
        except (IMAP4.error, error) as ex: 
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None                                                                            