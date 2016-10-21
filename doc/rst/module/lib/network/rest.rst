.. _module_lib_network_rest:

REST
====

This sections contains module documentation of rest module.

client
^^^^^^

Module client provides class RESTClient for REST API using external modules
`requests <http://docs.python-requests.org/en/master/>`_ in version >= 2.11.1,  
`requests-ntlm <https://github.com/requests/requests-ntlm>`_ in version 0.3.0, 
`lxml <http://lxml.de/>`_ in version >= 3.3.3, `simplejson <https://github.com/simplejson/simplejson>`_ in version >= 3.8.2.

lxml requires non-Python libraries which are automatically installed by setup script (python-lxml, libxml2-dev, libxslt1-dev for apt-get, 
python-lxml, libxml2-devel, libxslt-devel for yum). Unit tests available at hydratk/lib/network/rest/client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _url - URL
* _proxies - HTTP proxies configuration
* _cert - path to certificate file
* _req_header - request headers
* _req_body - request body
* _res_status - response status
* _res_header - response headers
* _res_body - response body
* _cookies - cookies
* _verbose - verbose mode
* _config - auxiliary configuration, verbose redirected to stderr
* _history - HTTP redirect history

**Properties (Getters)** :

* url - _returns url
* proxies - _returns _proxies
* cert - returns _cert
* req_header - returns _req_header
* req_body - returns _req_body
* res_status - returns _req_status
* res_headers - returns _res_headers
* res_body - returns _res_body
* cookies - returns _cookies
* verbose - returns _verbose
* config - returns _config
* history - retutns _history

**Methods** :

* __init__ 

Sets MasterHead reference and turns on verbose mode (if enabled). Debug messages redirected to stderr.

* get_header

Method returns given response HTTP header.

  .. code-block:: python
  
     from hydratk.lib.network.rest.client import RESTClient
     
     c = RESTClient()
     c.send_request('http://localhost:8080/Autobot/rs/crm/')
     res = c.get_header('content-type')
     
* send_request

Method send request to server. First fires event rest_before_request where parameters (url, proxies, user, passw, auth, cert, method, headers, 
cookies, body, params, file, content_type, timeout) can be rewritten.

url should start with http:// or https://. proxies is dictionary configuration of HTTP proxies (see requests documentation). auth is authentication type 
(supported types: Basic, Digest, NTLM). method is HTTP method (supported methods: GET, POST, PUT, DELETE, HEAD, OPTIONS). headers is dictionary of
request HTTP headers. cookies is dictionary (cookie name and value). 

params is dictionary (parameters name and value), they are sent as part of URL for GET methods otherwise in body. file is filename including path
to be downloaded from server (GET method) or uploaded to server (POST, PUT methods). content_type is user friendly mime type translated to valid HTTP
Content-Type header. Request timeout is 10s by default (parameter timeout).

Supported mime types:
file -> multipart/form-data            
form -> application/x-www-form-urlencoded
html -> text/html  
json -> application/json  
text -> text/plain
xml -> application/xml     

Methods prepares authentication using requests methods HTTPBasicAuth, HTTPDigestAuth, HTTPNtlmAuth (Basic is default).
GET is default HTTP method. When file is uploaded the content is included to request. Methods send request using request method (get, post, put, delete, head, options).
Stores response to attributes _res_status, _res_header, _res_body, _cookies, _history.

When file is downloaded the methods writes content to file. When response content type is json or xml, the body is automatically
to json object (using method simplejson.loads) or xml object (using method lxml.objectify). 
After that fires event rest_after_request an returns tuple of status, body. 

  .. code-block:: python
  
     # GET JSON content
     url = 'http://localhost:8080/Autobot/rs/crm/customer'
     headers, params = {'Accept': 'application/json'}, {'id': 0} 
     res, out = c.send_request(url, method='GET', headers=headers, params=params) 
     
     # POST JSON content
     name, status, segment = 'Charlie Bowman', 'active', 2
     body = {'name': name, 'status': status, 'segment': segment}
     content_type = 'json'
     res, out = c.send_request(url, method='POST', content_type=content_type, body=dumps(body))         
  
     # PUT JSON content
     name, status, segment = 'Vince Neil', 'suspend', 3
     body = {'id': id, 'name': name, 'status': status, 'segment': segment}
     res, out = c.send_request(url, method='PUT', content_type=content_type, body=dumps(body))         
     
     # GET XML content
     url = 'http://localhost:8080/Autobot/rs/crm/customer'
     headers, params = {'Accept': 'application/xml'}, {'id': 0} 
     res, out = c.send_request(url, method='GET', headers=headers, params=params)
     
     # POST XML content
     name, status, segment = 'Charlie Bowman', 'active', 2
     body = '<customer><name>{0}</name><status>{1}</status><segment>{2}</segment></customer>'.format(name, status, segment)
     content_type = 'xml'
     res, out = c.send_request(url, method='POST', content_type=content_type, body=body)   
     
     # PUT XML content
     name, status, segment = 'Vince Neil', 'suspend', 3
     body = '<customer><id>{0}</id><name>{1}</name><status>{2}</status><segment>{3}</segment></customer>'.format(id, name, status, segment)
     res, out = c.send_request(url, method='PUT', content_type=content_type, body=body)  
     
  .. code-block:: python
  
     # HTTPS request
     url = 'https://google.com'
     res, out = c.send_request(url) 
     
     # GET request with parameters
     url = 'http://metalopolis.net/art_downtown.asp'
     params = {'id': '7871'}
     res, out = c.send_request(url, method='GET', params=params)  
     
     # POST form
     url = 'http://metalopolis.net/fastsearch.asp'
     params={'verb': 'motorhead', 'submit': '>>>'}
     res, out = c.send_request(url, method='POST', params=params)
     
     # Basic authentication
     url = 'https://git-retail.hydratk.org/'
     res, out = c.send_request(url, user='xxx', passw='xxx', auth='Basic')    
     
     # Digest authentication
     url = 'https://trac.hydratk.org/hydratk/login'
     res, out = c.send_request(url, user='xxx', passw='xxx', auth='Digest') 
     
     # upload file
     url = 'http://www.filedropper.com/'
     res, out = c.send_request(url, method='POST', file=file)
     
     # download file
     url = 'https://pypi.python.org/packages/82/a3/ef4eb2dc3fcaaa5346d51548fcc3c8f0f4e1769d8ad4052430cd8ef1a1af/hydratk-ext-datagen-0.1.0.tar.gz#md5=5695263be75afd60473374e17c0f5785'
     file = 'hydratk-ext-datagen-0.1.0.tar.gz'
     res, out = c.send_request(url, method='GET', file=file)                                                  