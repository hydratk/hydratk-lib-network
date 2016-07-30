# -*- coding: utf-8 -*-
"""Generic REST client for protocols HTTP, HTTPS

.. module:: network.rest.client
   :platform: Unix
   :synopsis: Generic REST client for protocols HTTP, HTTPS
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
rest_before_request
rest_after_request

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
import httplib2 
from simplejson import loads
from simplejson.scanner import JSONDecodeError
from lxml import objectify
from lxml.etree import XMLSyntaxError
from socket import error

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

mime_types = {
  'form': 'application/x-www-form-urlencoded',
  'html': 'text/html',  
  'json': 'application/json',  
  'text': 'text/plain',
  'xml' : 'application/xml'
}

class RESTClient(object):
    """Class RESTClient
    """
    
    _mh = None
    _client = None
    _res_header = None
    _res_body = None
    _verbose = None
    
    def __init__(self, verbose=False, cache=False, ignore_cert=True, timeout=10):
        """Class constructor
           
        Called when the object is initialized 
        
        Args:                   
           verbose (bool): verbose mode
           cache (bool): use local cache
           ignore_cert (bool): ignore untrusted certificate errors
           timeout (int): timeout
           
        """         
        
        self._mh = MasterHead.get_head() 
        self._mh.find_module('hydratk.lib.network.rest.client', None)  
        
        if (cache):
            self._client = httplib2.Http('.cache', disable_ssl_certificate_validation=ignore_cert, timeout=timeout)
        else:
            self._client = httplib2.Http(disable_ssl_certificate_validation=ignore_cert, timeout=timeout)     
        
        self._verbose = verbose
        if (self._verbose):
            httplib2.debuglevel = 2
            
    @property
    def client(self):
        """ REST client property getter """
        
        return self._client
    
    @property
    def res_header(self):
        """ response header property getter """
        
        return self._res_header
    
    @property
    def res_body(self):
        """ response body property getter """
        
        return self._res_body
    
    @property
    def verbose(self):
        """ verbose mode """
        
        return self._verbose            
        
    def send_request(self, url, user=None, passw=None, method='GET', headers=None, 
                     body=None, params=None, content_type=None):
        """Method sends request to server
        
        Args:
           url (str): URL
           user (str): username
           passw (str): password           
           method (str): HTTP method
           headers (dict): HTTP headers
           body (str): request body, POST method used by default
           params (dict): parameters, sent in URL for GET method, in body for POST|PUT|DELETE method
           content_type (str): type of content, form|html|json|text|xml

        Returns:
           tuple: status (int), body (str) (json object, xml object, otherwise original string)
       
        Raises:
           event: rest_before_request
           event: rest_after_request
                
        """          
        
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_rest_request', url, user, passw,
                          method, headers, body, params), self._mh.fromhere()) 
            
            ev = event.Event('rest_before_request', url, user, passw, method,
                             headers, body, params, content_type)
            if (self._mh.fire_event(ev) > 0):
                url = ev.argv(0)
                user = ev.argv(1)
                passw = ev.argv(2)
                method = ev.argv(3)
                headers = ev.argv(4)
                body = ev.argv(5)
                params = ev.argv(6)
                content_type = ev.argv(7)             
            
            if (ev.will_run_default()): 
                if (user != None):
                    self._client.add_credentials(user, passw)            
            
                if (params != None):                
                    if (method in ('GET', None)):
                        url = '{0}?{1}'.format(url, urlencode(params))  
                    elif (method in ('POST', 'PUT', 'DELETE')):
                        body = urlencode(params)  
                        content_type = 'form'        
                if (body != None and method in ('GET', None)):
                    method = 'POST'                    
                if (content_type != None and content_type in mime_types):
                    if (headers == None):
                        headers = {}
                    headers['Content-Type'] = mime_types[content_type]
  
                header = None
                header, body = self._client.request(url, method, body, headers)
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_rest_response', header, body), self._mh.fromhere()) 
            ev = event.Event('rest_after_request')
            self._mh.fire_event(ev)              
            
            self._res_header = header
            content_type = self.get_header('Content-Type')
            if (content_type != None):
                if ('json' in content_type and len(body) > 0):
                    body = loads(body)
                elif ('xml' in content_type and len(body) > 0):              
                    body = objectify.fromstring(body)       
            
            if (body.__class__.__name__ == 'bytes'):
                body = body.decode('latin-1')                    
            self._res_body = body                                       
                
            return (int(header.status), body)
            
        except (httplib2.HttpLib2Error, error, JSONDecodeError, XMLSyntaxError) as ex:
            if (str(ex) == 'WWW-Authenticate'):
                return (401, None)
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            status = int(header.status) if (header != None and 'status' in header) else None
            return status, self._res_body   
        
    def get_header(self, title):
        """Method gets response header
        
        Args:
           title (str): header title

        Returns:
           str: header
                
        """  
        
        title = title.lower()
        if (title in self._res_header):        
            return self._res_header[title]
        else:
            return None 
    
    def get_body(self): 
        """Method gets response body
        
        Args:
           none

        Returns:
           str: body
                
        """               
        
        return self._res_body                                                                                              

    def reset_debug(self):
        """Method resets debug level
        
        Args:
           none

        Returns:
           void
                
        """    
        
        httplib2.debuglevel = 0        