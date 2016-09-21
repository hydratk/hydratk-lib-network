.. _tutor_network_tut8_rest:

Tutorial 8: REST
================

This sections shows several examples how to use REST client.

API
^^^

Module hydratk.lib.network.rest.client

Supported protocols:

* HTTP/HTTPS

Methods:

* send_request: send request to server
* get_header: get response header

  .. note::
   
     API uses HydraTK core functionalities so it must be running.

Examples
^^^^^^^^

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.rest.client as rest
    
     # initialize client
     client = rest.RESTClient()
     
     # send HTTP GET request 
     # returns status 200 and HTML body
     status, body = client.send_request('google.com')
     
     # send HTTP GET request with URL param
     status, body = client.send_request('http://metalopolis.net/art_downtown.asp', 
                                         params={'id2': '7871'})  
                  
     # send HTTP POST request to submit form                       
     status, body = client.send_request('http://metalopolis.net/fastsearch.asp', method='POST', 
                                         params={'verb': 'motorhead', 'submit': '>>>'}) 
      
     # send HTTPS GET request with authentication Basic, Digest, NTLM, certificate                                   
     status, body = client.send_request('https://trac.hydratk.org/hydratk/login', 
                                         user='aaa', passw='bbb', auth='Basic')  
     status, body = client.send_request('https://trac.hydratk.org/hydratk/login', 
                                         user='aaa', passw='bbb', auth='Digest')  
     status, body = client.send_request('https://trac.hydratk.org/hydratk/login', 
                                         user='aaa', passw='bbb', auth='NTLM')   
     status, body = client.send_request('https://trac.hydratk.org/hydratk/login', 
                                         cert='/home/lynus/cert.pem')  
     status, body = client.send_request('https://trac.hydratk.org/hydratk/login', 
                                         cert=('/home/lynus/cert.pem', '/home/lynus/key.pem'))                                                                                                                                                                      
                                         
     # send HTTP POST request with JSON body 
     data = r'{"userId": 1, "id": 101, "title": "bowman", "body": "bowman"}'
     status, body = client.send_request('http://jsonplaceholder.typicode.com/posts', method='POST', body=data,
                                         content_type='json')     
                                         
     # send HTTP GET request to receive JSON body
     status, body = client.send_request('http://jsonplaceholder.typicode.com/posts/100', method='GET') 
     
     # send HTTP GET request to receive XML body
     status, body = client.send_request('http://httpbin.org/xml', method='GET')  
     
     # send request with cookies
     status, body = client.send_request('http://test.com', cookies={'name': 'value'})
     
     # send request with proxy
     status, body = client.send_requst('http://test.com', proxies={'http': 'http://10.10.1.10:3128'})
     
     # download file
     url = 'https://pypi.python.org/packages/82/a3/ef4eb2dc3fcaaa5346d51548fcc3c8f0f4e1769d8ad4052430cd8ef1a1af/hydratk-ext-datagen-0.1.0.tar.gz#md5=5695263be75afd60473374e17c0f5785'
     file = 'hydratk-ext-datagen-0.1.0.tar.gz'
     status, body = client.send_request(url, method='GET', file=file)
     
     # upload file                  
     url = 'http://www.filedropper.com/'
     status, body = client.send_request(url, method='POST', file='test.txt')