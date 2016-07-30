# -*- coding: utf-8 -*-
"""Generic SOAP client

.. module:: network.soap.client
   :platform: Unix
   :synopsis: Generic SOAP client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
soap_before_load_wsdl
soap_after_load_wsdl
soap_before_request
soap_after_request

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from suds import client, WebFault, MethodNotFound
from suds.transport import TransportError
from suds.cache import NoCache
from lxml.etree import Element, SubElement, fromstring, tostring, XMLSyntaxError
from logging import getLogger, StreamHandler, CRITICAL, DEBUG
from sys import stderr

try:
    from urllib2 import URLError
except ImportError:
    from urllib.error import URLError    

getLogger('suds.client').setLevel(CRITICAL)

class SOAPClient(object):
    """Class SOAPClient
    """
    
    _mh = None
    _client = None
    _wsdl = None
    _url = None
    _location = None
    _user = None
    _passw = None
    _endpoint = None
    _headers = None
    _verbose = None
    
    def __init__(self, verbose=False):
        """Class constructor
           
        Called when the object is initialized 
        
        Args:       
           verbose (bool): verbose mode
           
        """          
        
        self._mh = MasterHead.get_head()  
        self._mh.find_module('hydratk.lib.network.soap.client', None)          
        
        self._verbose = verbose
        if (self._verbose):
            handler = StreamHandler(stderr)
            logger = getLogger('suds.transport.http')
            logger.setLevel(DEBUG), handler.setLevel(DEBUG)
            logger.addHandler(handler)
            
    @property
    def client(self):
        """ SOAP client property getter """
        
        return self._client
    
    @property
    def wsdl(self):
        """ WSDL property getter """
        
        return self._wsdl
    
    @property
    def url(self):
        """ URL property getter """
        
        return self._url     
    
    @property
    def location(self):
        """ WSDL location property getter """
        
        return self._location
    
    @property
    def user(self):
        """ username property getter """
        
        return self._user
    
    @property
    def passw(self):
        """ user password property getter """
        
        return self._passw     
    
    @property
    def endpoint(self):
        """ service endpoint property getter """
        
        return self._endpoint
    
    @property
    def headers(self):
        """ HTTP headers property getter """
        
        return self._headers
    
    @property
    def verbose(self):
        """ verbose mode property getter """
        
        return self._verbose                      
            
    def load_wsdl(self, url, location='remote', user=None, passw=None, endpoint=None, headers=None,
                  transport=None, use_cache=True, timeout=10): 
        """Method loads wsdl
        
        Args:
           url (str): WSDL URL, URL for remote, file path for local
           location (str): WSDL location, remote|local
           user (str): username
           passw (str): password
           endpoint (str): service endpoint, default endpoint from WSDL 
           headers (dict): HTTP headers
           transport (obj): HTTP transport
           use_cache (bool): load WSDL from cache
           timeout (int): timeout

        Returns:
           bool: result
           
        Raises:
           event: soap_before_load_wsdl
           event: soap_after_load_wsdl      
                
        """          
        
        try:
                        
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_soap_loading_wsdl', url,
                          user, passw, endpoint, headers), self._mh.fromhere())
            
            ev = event.Event('soap_before_load_wsdl', url, location, user, passw, endpoint, headers, transport)
            if (self._mh.fire_event(ev) > 0):
                url = ev.argv(0)
                location = ev.argv(1)
                user = ev.argv(2)
                passw = ev.argv(3)
                endpoint = ev.argv(4)
                headers = ev.argv(5)
                transport = ev.argv(6)         
        
            self._url = url
            self._location = location
            self._user = user
            self._passw = passw
            self._endpoint = endpoint  
            self._headers = headers
        
            if (ev.will_run_default()): 
                
                options = {}
                if (self._location == 'local'):
                    self._url = 'file://' + self._url
                if (self._user != None):
                    options['username'] = self._user
                    options['password'] = self._passw
                if (self._endpoint != None):
                    options['location'] = self._endpoint
                if (self._headers != None):
                    options['headers'] = self._headers
                if (transport != None):
                    options['transport'] = transport
                if (timeout != None):
                    options['timeout'] = timeout
    
                self._client = client.Client(self._url, **options) if (use_cache) else client.Client(self._url, cache=NoCache(), **options) 
                self._wsdl = self._client.wsdl
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_soap_wsdl_loaded'), self._mh.fromhere())
            ev = event.Event('soap_after_load_wsdl')
            self._mh.fire_event(ev)                   
                
            return True
            
        except (WebFault, TransportError, URLError, ValueError) as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False 
        
    def get_operations(self):
        """Method returns service operations
        
        Args:  
           none         

        Returns:
           list: operations
                
        """           
                               
        if (self._wsdl != None):
            operations = []
            for operation in self._wsdl.services[0].ports[0].methods.values():       
                operations.append(operation.name)  
            return operations
        else:
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_soap_wsdl_not_loaded'), self._mh.fromhere())
            return None
        
    def send_request(self, operation, body, headers=None):      
        """Method sends request
        
        Args:   
           operation (str): operation name
           body (str|xml): request body
           headers (dict): HTTP headers, SOAPAction, Content-Type are set automatically       

        Returns:
           obj: response body, objectified xml
           
        Raises:
           event: soap_before_request
           event: soap_after_request
                
        """    
        
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_soap_request', operation, body, headers),
                          self._mh.fromhere()) 
            
            if (self._wsdl == None):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_soap_wsdl_not_loaded'), self._mh.fromhere())
                return None
            
            ev = event.Event('soap_before_request', operation, body, headers)
            if (self._mh.fire_event(ev) > 0):
                operation = ev.argv(0)
                body = ev.argv(1)
                headers = ev.argv(2)    
                
            if (ev.will_run_default()):                             
            
                if (headers != None):
                    self._client.set_options(headers=headers)
            
                nsmap = {'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/'}
                ns = '{%s}' % nsmap['soapenv']
                root = Element(ns+'Envelope', nsmap=nsmap)
                SubElement(root, ns+'Header')
                elem = SubElement(root, ns+'Body')
            
                if (isinstance(body, str)):
                    body = fromstring(body) 
                elif (isinstance(body, bytes)):
                    body = fromstring(body.decode())
                elem.append(body)           
            
                response = getattr(self._client.service, operation)(__inject = {'msg': tostring(root)})                
        
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_soap_response', response), self._mh.fromhere()) 
            ev = event.Event('soap_after_request')
            self._mh.fire_event(ev)        
        
            return response
            
        except (WebFault, TransportError, URLError, ValueError, XMLSyntaxError, MethodNotFound) as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None                     