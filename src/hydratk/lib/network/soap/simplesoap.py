# -*- coding: utf-8 -*-
"""Pycurl wrapped object oriented soap client solution

.. module:: network.soap.simplesoap
   :platform: Unix
   :synopsis: Pycurl wrapped object oriented soap client solution
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import pycurl
import pytz
import datetime


from hydratk.lib.data.xml import XMLValidate
from hydratk.lib.system import fs
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

curl_info_map  = {
                       'effective_url'           : 'EFFECTIVE_URL',
                       'response_code'           : 'RESPONSE_CODE',
                       'http_connectcode'        : 'HTTP_CONNECTCODE',
                       'filetime'                : 'INFO_FILETIME',
                       'total_time'              : 'TOTAL_TIME',
                       'namelookup_time'         : 'NAMELOOKUP_TIME',
                       'connect_time'            : 'CONNECT_TIME',
                       'appconnect_time'         : 'APPCONNECT_TIME',              
                       'pretransfer_time'        : 'PRETRANSFER_TIME',
                       'starttransfer_time'      : 'STARTTRANSFER_TIME',
                       'redirect_time'           : 'REDIRECT_TIME',
                       'redirect_count'          : 'REDIRECT_COUNT',
                       'redirect_url'            : 'REDIRECT_URL',
                       'size_upload'             : 'SIZE_UPLOAD',
                       'size_download'           : 'SIZE_DOWNLOAD',
                       'speed_download'          : 'SPEED_DOWNLOAD',
                       'speed_upload'            : 'SPEED_UPLOAD',
                       'header_size'             : 'HEADER_SIZE',
                       'request_size'            : 'REQUEST_SIZE',
                       'ssl_verify_result'       : 'SSL_VERIFY_RESULT',
                       'ssl_engines'             : 'SSL_ENGINES',
                       'content_length_download' : 'CONTENT_LENGTH_DOWNLOAD',
                       'content_length_upload'   : 'CONTENT_LENGTH_UPLOAD',
                       'content_type'            : 'CONTENT_TYPE',
                       'private'                 : 'PRIVATE',
                       'httpauth_avail'          : 'HTTPAUTH_AVAIL',
                       'proxyauth_avail'         : 'PROXYAUTH_AVAIL',
                       'os_errno'                : 'OS_ERRNO',
                       'num_connects'            : 'NUM_CONNECTS',
                       'primary_ip'              : 'PRIMARY_IP',
                       'primary_port'            : 'PRIMARY_PORT',
                       'local_ip'                : 'LOCAL_IP',
                       'local_port'              : 'LOCAL_PORT',                       
                       'lastsocket'              : 'LASTSOCKET',
                       'activesocket'            : 'ACTIVESOCKET',                       
                       'tls_session'             : 'TLS_SESSION',                                                   
}

HTTP_AUTH_BASIC = pycurl.HTTPAUTH

class SoapResponse(object):
    """Class SoapResponse
    """
    
    _msg          = None
    _resp_headers = []
    _resp_code    = 0    
    _info         = {}
    
    @property
    def response_code(self):
        """ response_code property getter """
        
        return self._resp_code
    
    @property
    def info(self):
        """ info property getter """
        
        return self._info
    
    @property
    def headers(self):
        """ headers property getter """
        
        return self._resp_headers
        
    @property
    def msg(self):
        """ msg property getter """
        
        return self._msg 
    
    @msg.setter
    def msg(self, data):
        """ msg property setter """
        self._msg = data       
                     
    @property
    def message(self):
        """ message property getter """
        
        return self._msg

    @message.setter
    def message(self, data):
        """ message property setter """
        self._msg = data    
 
    def _extract_info(self, curl_obj):
        """Methods extracts parameters from CURL object

        Args:
           curl_obj (obj): CURL object

        Returns:
           void
    
        """
                
        for info_key, curl_opt in curl_info_map.items():                                                
            if hasattr(curl_obj, curl_opt): 
                curl_val = curl_obj.getinfo(getattr(curl_obj, curl_opt))
                self._info[info_key] = curl_val
           
    def _apply_info(self):
        """Methods stores response code

        Args:        
           none   

        Returns:
           void
    
        """
                
        self._resp_code = self._info['response_code']
                    
    def __init__(self, curl_obj):
        """Class constructor 
        
        Called when object is initialized

        Args:
           curl_obj (obj): CURL object
    
        """
                
        self._extract_info(curl_obj)
        self._apply_info()
        
        
class SoapRequest(object):
    """Class SoapRequest
    """
    
    _msg         = None
    _req_url     = None
    _req_method  = pycurl.POST
    _req_headers = [
                     "Content-type: text/xml; charset=utf-8"
                   ]
        
    def __init__(self, request_url=None):
        """Class constructor
        
        Called when object is initialized

        Args:
           request_url (str): URL
    
        """
                
        self._req_url = request_url      
    
    @property
    def url(self):
        """ url property getter, setter """
        
        return self._req_url
    
    @url.setter
    def url(self, url):
        """ url property setter """
        
        self._req_url = url
            
    @property
    def headers(self):
        """ header property getter, setter """
        
        return self._req_headers
    
    @headers.setter
    def headers(self, header):
        """ headers property setter """
        
        self._req_headers = header
    
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
        """ message propery getter, setter """
        
        return self._msg
    
    @message.setter
    def message(self, msg):
        """ message property setter """
        
        self._msg = msg
         

class SoapResponseMessage(object):
    """Class SoapResponseMessage
    """
    
    _content = None
    
    def __init__(self, content=None):
        """Class constructor
        
        Called when object is initialized

        Args:
           content (str): response content
    
        """
                
        if content is not None:
            self._content = content
            
    @property
    def content(self):
        """ content property getter, setter """
        
        return self._content
    
    @content.setter
    def content(self, content):
        """ content property setter """
        
        self._content = content


class SoapRequestMessage(XMLValidate):
    """Class SoapRequestMessage
    """
    
    _bind_lchr = '['
    _bind_rchr = ']'
    _content   = None
    
    def __init__(self, content=None, source='file'):
        """Class constructor
        
        Called when object is initialized

        Args:
           content (str): filename including path if source=file
                          request content if source=str
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
        """Methods loads request content from file

        Args:
           msg_file (str): filename including path

        Returns:
           void
    
        """
        
        self._content = fs.file_get_contents(msg_file)             
        
    def bind_var(self, *args, **kwargs):
        """Methods binds input data to request template

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
    
    
    def xsd_validate(self):
        """Methods validates request xml according to xsd

        Args:
           none

        Returns:
           tuple: result (bool), message (str)
    
        """
                
        from lxml.etree import DocumentInvalid, XMLSyntaxError       
        result = True
        msg    = None
        try:
            XMLValidate.xsd_validate(self, self._content)
        except (DocumentInvalid, XMLSyntaxError) as e:
            msg    = e
            result = False
            
        return (result, msg)
           
class SoapClient():
    """Class SoapClient
    """
    
    _connection_timeout = 30
    _request            = None    
    _response           = None
    _curl               = None

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
             
    def __init__(self):
        """Class constructor
        
        Called when object is initialized

        Args:
           none
    
        """
                
        self._curl = pycurl.Curl()
    
    def set_auth(self, username, password, auth_type=HTTP_AUTH_BASIC):
        """Methods sets authentication headers

        Args:
           username (str): username
           password (str): password
           auth_type (str) HTTP authentication, Basic supported only

        Returns:
           void
    
        """
                
        self._curl.setopt(self._curl.HTTPAUTH, auth_type)
        if auth_type == HTTP_AUTH_BASIC:
            self._curl.setopt(self._curl.USERPWD, "{username}:{password}".format(username=username,password=password))                   
    
    def send(self, timeout=_connection_timeout):  
        """Methods sends request

        Args:
           timeout (int): connection timeout

        Returns:
           void
    
        """              
        
        buff = BytesIO()                
        self._curl.setopt(self._curl.URL, self.request.url)
        self._curl.setopt(self._curl.HTTPHEADER, self.request.headers)
        self._curl.setopt(self._curl.POSTFIELDS, str(self.request.msg.content))
        self._curl.setopt(self._curl.WRITEDATA, buff)
        
        self._curl.perform()        
        self._response = SoapResponse(self._curl)
        self._response.msg = SoapResponseMessage(buff.getvalue().decode())
        self._curl.close()

         
def xml_timestamp(location='Europe/Prague'):
    """Methods creates timestamp including time zone

    Args:
       location (str): time zone location

    Returns:
       str: timestamp
    
    """  
          
    return datetime.datetime.now(pytz.timezone(location)).isoformat()