# -*- coding: utf-8 -*-
"""SMTP email client

.. module:: network.email.smtp_client
   :platform: Unix
   :synopsis: SMTP email client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
email_before_connect
email_after_connect
email_before_send_email
email_after_send_email

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from smtplib import SMTP, SMTP_SSL, SMTPException
from socket import error

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
           secured (bool): secured SMTP        
           verbose (bool): verbose mode
           
        """         
        
        self._mh = MasterHead.get_head() 
         
        self._secured = secured     
        if (not self._secured):            
            self._client = SMTP()
        else:
            self._client = SMTP_SSL()   
                         
        self._verbose = verbose 
        if (self.verbose):              
            self._client.set_debuglevel(2)
            
    @property
    def client(self):
        """ SMTP client property getter """
        
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
                port = 25 if (not self._secured) else 465
                
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
                self._client.timeout = timeout              
                self._client.connect(self.host, self.port)                      
                    
                if (self._user != None):
                    self._client.login(self.user, self.passw)  
                    
                self._is_connected = True                       
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_connected'), self._mh.fromhere()) 
            ev = event.Event('email_after_connect')
            self._mh.fire_event(ev)   
                                                   
            return True
        
        except (SMTPException, error) as ex:
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
                self._client.quit()
                self._is_connected = False                
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_disconnected'), self._mh.fromhere())  
                return True  
    
        except (SMTPException, error) as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False  
        
    def send_email(self, subject, message, sender='hydra@hydratk.org', recipients=['hydra@hydratk.org'],
                   cc=[], bcc=[]):   
        """Method sends email
        
        Args:
           subject (str): email subject
           message (str): email content, string, mandatory
           sender (str): from email address 
           recipients (list): to email addresses   
           cc (list): carbon copy email addresses
           bcc (list): blind carbon copy email addresses  
           
        Returns:
           bool: result       
           
        Raises:
           event: email_before_send_email
           event: email_after_send_email
                
        """  
        
        try:
            
            msg = 'From:{0}, To:{1}, CC:{2}, BCC:{3}, Subject:{4}'.format(sender, recipients, cc, bcc, subject)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_sending', msg), self._mh.fromhere())
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_email_not_connected'), self._mh.fromhere()) 
                return False              
            
            ev = event.Event('email_before_send_email', subject, message, sender, recipients, cc, bcc)
            if (self._mh.fire_event(ev) > 0):
                subject = ev.argv(0)
                message = ev.argv(1)
                sender = ev.argv(2)
                recipients = ev.argv(3)
                cc = ev.argv(4)
                bcc = ev.argv(5)
                
            if (ev.will_run_default()):
                msg = 'From: {0}\r\n'.format(sender) + \
                      'To: {0}\r\n'.format(','.join(recipients)) + \
                      'CC: {0}\r\n'.format(','.join(cc)) + \
                      'Subject: {0}\r\n'.format(subject) + \
                      '\r\n{0}'.format(message)
                self._client.sendmail(sender, recipients+cc+bcc, msg)
                
            ev = event.Event('email_after_send_email')
            self._mh.fire_event(ev)                   
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_sent'), self._mh.fromhere())
            
            return True
            
        except (SMTPException, error) as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False 
                                                              