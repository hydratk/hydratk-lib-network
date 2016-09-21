.. _tutor_network_tut11_soap:

Tutorial 11: SOAP
=================

This sections shows several examples how to use SOAP client.

API
^^^

Module hydratk.lib.network.soap.client

Methods:

* load_wsdl: load service definition from WSDL (remote located on server, local located on file system)
* get_operations: get service operations
* send_request: send request to server

  .. note::
   
     API uses HydraTK core functionalities so it must be running.

Examples
^^^^^^^^

  .. code-block:: python
     
     # import library
     import hydratk.lib.network.soap.client as soap
    
     # initialize client
     client = soap.SOAPClient()
     
     # load WSDL from server
     # returns bool
     client.load_wsdl('http://www.webservicex.com/globalweather.asmx?WSDL')
     
     # get service operations
     # returns list of names
     client.get_operations()
     
     # send request to chosen operation with XML body
     # SOAP envelope is added by client itself
     body = '<web:GetCitiesByCountry xmlns:web=\"http://www.webserviceX.NET\"><web:CountryName>Italy</web:CountryName>
             </web:GetCitiesByCountry>'
      
     # returns XML body        
     response = client.send_request('GetCitiesByCountry', body=body)
     
     # load WSDL from filesystem, service uses authentication Basic, NTLM, certificate
     # WSDL is stored on filesystem, real service endpoint is not specified in WSDL 
     client.load_wsdl(path_to_wsdl, location='local', user='soap_user', passw='soap_passw', auth='Basic', endpoint='soap_mu_url')
     client.load_wsdl(path_to_wsdl, location='local', user='soap_user', passw='soap_passw', auth='NTLM', endpoint='soap_mu_url')
     client.load_wsdl(path_to_wsdl, location='local', cert='/home/lynus/cert.pem', endpoint='soap_mu_url')
     client.load_wsdl(path_to_wsdl, location='local', cert=('/home/lynus/cert.pem', '/home/lynus/key.pem'), endpoint='soap_mu_url')
     
     # load WSDL from filesystem, service uses authentication via specific HTTP headers
     client.load_wsdl(path_to_wsdl, location='local', endpoint='soap_cm_url', 
                      headers = {'Username' : 'soap_user', 'Password' : 'soap_passw'}) 
                      
     # load WSDL using proxy
     client.load_wsdl(url, proxies={'http': 'http://10.10.1.10:3128'})                      