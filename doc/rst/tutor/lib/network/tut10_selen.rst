.. _tutor_network_tut10_selenium:

Toturial 10: Selenium bridge
============================

This sections shows several examples how to use Selenium bridge.

API
^^^

Module hydratk.lib.bridge.selen

Constructor requires attribute browser, PhantomJS (headless browser) is chosen by default.
Browser libraries including PhantomJS are not bundled with HydraTK and must be installed individually.  

Supported browsers:

* Android
* BlackBerry
* Firefox
* Internet Explorer
* Opera
* PhantomJS
* Safari

Methods:

* open: open web page URL
* close: close browser
* wait_for_element: wait for element presence
* get_element: get element using various methods
* read_element: read element value
* set_element: set element value
* exe_script: execute JavaScript code
* save_screen: save screenshot

  .. note::
   
     API uses HydraTK core functionalities so it must be running.

Examples
^^^^^^^^

  .. code-block:: python
  
     # import library
     from hydratk.lib.bridge.selen import SeleniumBridge
     
     # initialize bridge
     bridge = SeleniumBridge('PhantomJS')
     
     # open registration module
     bridge.open('https://oneportal.com/web/registration')  
     
     # wait for element presence
     bridge.wait_for_element('firstName') 
          
     # fill registration form
     bridge.set_element('firstName', 'Charlie')
     bridge.set_element('lastName', 'Bowman')  
     bridge.set_element('phoneNumber', '603603603')
     bridge.set_element('email', 'aaa@xxx.com')
     bridge.set_element('marketingAgreement1', False)
     
     # save screenshot
     bridge.save_screen('fig.png')
     
     # submit form
     bridge.set_element('button', method='tag', attr='text', attr_val='Continue'))
     
     # wait for element presence
     bridge.wait_for_element('//input[@class='result']', method='xpath')
     
     # read element text
     result = bridge.read_element('//input[@class='result']', method='xpath')
     assert (result == 'User registered')
     
     # close browser
     bridge.close()