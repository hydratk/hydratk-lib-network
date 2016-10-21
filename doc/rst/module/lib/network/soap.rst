.. _module_lib_network_soap:

SOAP
====

This sections contains module documentation of soap module.

client
^^^^^^

Module client provides class SOAPClient for SOAP protocol using external module
`suds <https://fedorahosted.org/suds/wiki/Documentation>`_ in version >= 0.4.
When Python3 is used module suds is replace by `suds_py3 <https://github.com/cackharot/suds-py3>`_ in version 1.3.2.0

Unit tests available at hydratk/lib/network/soap/client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - suds client instance
* _wsdl - parsed WSDL object
* _url - URL
* _proxies - HTTP proxies configuration
* _location - wsdl location, remote or local
* _user - username
* _passw - password
* _cert - path to certificate file
* _endpoint - service endpoint
* _headers - request HTTP headers
* _verbose - verbose mode

**Properties (Getters)** :

* client - returns _client
* wsdl - returns _wsdl
* url - _returns url
* proxies - _returns _proxies
* location - returns _location
* user - returns _user
* passw - returns _passw
* cert - returns _cert
* endpoint - returns _endpoint
* headers - returns _headers
* verbose - returns _verbose

**Methods** :

* __init__ 

Sets MasterHead reference and turns on verbose mode (if enabled). 

* load_wsdl

Methods loads service definition from WSDL. First fires event soap_before_load_wsdl where parameters (url, proxies, location, user, passw, 
auth, cert, endpoint, headers, use_cache, timeout) can be rewritten.

proxies is dictionary configuration of HTTP proxies (see requests documentation). location is WSDL location, remote when located on server 
(url should start with http:// or https://, default), local when located on localhost (url is filename including path, method automatically prepends file://). 
auth is authentication type (supported types: Basic, NTLM). cert is path to certificate file. 

endpoint is service url (by default derived from WSDL, must be specified when WSDL doesn't specify real service URL, typical for multiple environments).
headers is dictionary of request HTTP headers. use_cache is bool, wsdl is loaded from suds cache instead of server (True by default). WSDL is kept
in cache for 1 day, use False when you WSDL is being frequently changed (typical for debugging phase). Request timeout is 10s by default (parameter timeout).

NTLM authentication is prepared using suds method WindowsHttpAuthenticated. Certificate is included using auxiliary class RequestsTransport.
Method sets _client using suds constructor Client, any parameters are passed as kwargs. Stores parsed WSDL to _wsdl.
After that fires event soap_after_load_wsdl and returns bool.

  .. code-block:: python
  
     from hydratk.lib.network.soap.client import SOAPClient
     
     # remote WSDL
     c = SOAPClient()
     url = 'http://localhost:8080/Autobot/crm?wsdl'
     res = c.load_wsdl(url, location='remote')  
     
     # local WSDL
     url = '/var/local/hydratk/testenv/crm.wsdl'
     res = c.load_wsdl(url, location='local')  
     
* get_operations

Method returns all operations specified in WSDL (names only, parameters are not returned).

  .. code-block:: python
  
     res = c.get_operations()        
     
* send_request

Methods sends SOAP request to server. First fires event soap_before_request where parameters (operation, body, headers) can be rewritten.
body is xml string or xml object (lxml.etree) without SOAP envelope. Methods automatically includes SOAP envelope (including header, body).
Methods calls _client method operation and sends xml request. After that fires event soap_after_request and returns xml response object (lxml.objectify).

  .. code-block:: python
  
     # read operation
     op, ns = 'readCustomer', '\"http://autobot.bowman.com/\"'
     doc = '<aut:{0} xmlns:aut={1}><id>0</id></aut:{2}>'.format(op, ns, op) 
     res = c.send_request(op, doc, headers={'SOAPAction': op}) 
     
     # write operation
     op = 'createCustomer'
     name, status, segment = 'Charlie Bowman', 'active', 3
     doc = '<aut:{0} xmlns:aut={1}><name>{2}</name><status>{3}</status>'.format(op, ns, name, status) + \
           '<segment>{0}</segment></aut:{1}>'.format(segment, op) 
     res = c.send_request(op, doc, headers={'SOAPAction': op}) 
     
* class RequestsTransport

Auxiliary class derived from suds class HttpAuthenticated. Used when HTTP request contains certificate.

simplesoap
^^^^^^^^^^

Modules provides simplified SOAP client with with possibility to send requests from template.
It sends HTTP request using module `pycurl <http://pycurl.io/docs/latest/index.html>`_ in version 7.19.5.1.
pycurl requires non-Python libraries which are automatically installed by setup script (python-pycurl, libcurl4-openssl-dev for apt-get, python-pycurl, libcurl-devel for yum).

Unit tests available at hydratk/lib/network/soap/simplesoap/01_methods_ut.jedi

**Classes** :

* SoapClient

**Attributes** :
_request, _response, _connection_timeout, _curl

**Properties (Getters)** :
request, response

**Properties (Setters** :
request

**Methods** :
set_auth - sets authentication headers using pycurl method setopt (Basic authentication supported)
send - sends request using pycurl method perform, sets content using method setopt (url, headers, body), stores the response 

  .. code-block:: python
  
     from hydratk.lib.network.soap.simplesoap import SoapClient, SoapRequest, SoapRequestMessage
     
     msg = '<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:aut=\"http://autobot.bowman.com/\">' + \
           '<soapenv:Header/><soapenv:Body><aut:readCustomer><id>0</id></aut:readCustomer></soapenv:Body></soapenv:Envelope>'
     rqm = SoapRequestMessage(msg, 'str')
     rq = SoapRequest()
     rq.url = 'http://localhost:8080/Autobot/crm'
     rq.message = rqm
     c = SoapClient()
     c.request = rq
     c.send()
     res = c._response.message.content    

* SoapRequest

**Attributes** :
_msg, _req_url, _req_method, _req_headers

**Properties (Getters)** :
url, headers, msg, message

**Properties (Setters)** :
url, headers, msg, message

**Methods** :
__init__ - sets _req_url

* SoapRequestMessage

**Attributes** :
_bind_lchr, _bind_rchr, _content

**Properties (Getters)** :
content

**Properties (Setters)** :
content

**Methods** :
__init__ - sets _content, it is possible to load message from file
load_from_file - sets _content with file content
bind_var - fills message template with given data passed as args, kwargs
xsd_validate - validates xml request according to XSD, returns bool and error text (for invalid xml)

  .. code-block:: python
  
     msg = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">' + \
           '<soapenv:Header/><soapenv:Body><readCustomer><id>[id]</id><name>[name]</name></readCustomer></soapenv:Body></soapenv:Envelope>' 
 
     # bind args
     c = SoapRequestMessage(msg, 'str')
     id, name = '1', 'Charlie Bowman'
     c.bind_var({'id': id}, {'name': name})
     
     # bind kwargs
     c.bind_var({'id': id, 'name': name})
     
     # xml validation
     msg = '<htk:read_customer xmlns:htk=\"http://hydratk.org/\"><id>0</id></htk:read_customer>' 
     c = SoapRequestMessage(msg, 'str')
     c.load_xsd_file('/var/local/hydratk/testenv/crm.xsd')
     res, m = c.xsd_validate()                
     
* SoapResponse

**Attributes** :
_msg, _resp_headers, _resp_code, _info

**Properties (Getters)** :
response_code, info, headers, msg, message

**Properties (Setters)** :
msg, message

**Methods** :
__init__ - calls _extract_info, _apply_info 
_apply_info - sets _resp_code
_extract_info - sets _info dictionary from response object, items are translated to more user friendly name (according to mapping curl_info_map) 

* SoapResponseMessage

**Attributes** :
_content

**Properties (Getters)** :
content

**Properties (Setters)** :
content   

**Methods** :
__init__ - sets _content        

* xml_timestamp

Method prepares timestamp including time zone in IS format. It uses external module
`pytz <http://pythonhosted.org/pytz/>`_ in version >= 2016.6.1. 