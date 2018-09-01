.. _tutor_network_tut10_selenium:

Toturial 10: Selenium bridge
============================

This sections shows several examples how to use Selenium bridge.

API
^^^

Module hydratk.lib.bridge.selen

Constructor requires attribute browser. Only browsers with headless mode are supported (PhantomJS project was cancelled).
Browser libraries are not bundled with HydraTK and must be installed individually.  

Supported browsers:

* Firefox (needs browser and geckodriver)
* Chrome (needs browser and chromedriver)

Methods:

* open: open web page URL
* close: close browser
* wait_for_element: wait for element presence
* get_element: get element using various methods
* read_element: read element value
* set_element: set element value
* exe_script: execute JavaScript code
* save_screen: save screenshot
* check_alert: check if alert is present
* get_current_url: get current url
* get_title: get page title
* go_back: emulates browser back button
* refresh: emulates browser refresh button
* get_screen: get screenshot content

  .. note::
   
     API uses HydraTK core functionalities so it must be running.

Examples
^^^^^^^^

  .. code-block:: python
  
     # import library
     from hydratk.lib.bridge.selen import SeleniumBridge
     
     # initialize bridge
     bridge = SeleniumBridge('Firefox')
     
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
     
     # headless mode
     bridge = SeleniumBridge('Firefox', headless=True)
     bridge = SeleniumBridge('Chrome', headless=True)
     
     # save video
     # file movie_yyyymmddhh24miss.gif is created
     # videos from standard mode are of better quality than from headless mode
     bridge = SeleniumBridge('Firefox', save_video=True)
     bridge = SeleniumBridge('Chrome', headless=True, save_video=True)  