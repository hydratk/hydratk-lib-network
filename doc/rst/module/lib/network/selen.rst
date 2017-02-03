.. _module_lib_bridge_selen:

Selen
=====

This sections contains module documentation of selen module.

selen
^^^^^

Module provides class SeleniumBridge which implements bridge to Selenium WebDriver API using external module
`selenium <http://selenium-python.readthedocs.io/>`_ in version >= 2.46.1.
selenium requires non-Python libraries which are automatically installed by setup script (libfontconfig for apt-get, fontconfig for yum).

Unit tests available at hydratk/lib/bridge/selen/01_methods_ut.jedi, 02_methods_ut.jedi

selen uses running browser to execute tests on web page. Browsers are not bundled with hydratk and must be installed separately.
The recommended browser is `PhantomJS <http://phantomjs.org/>`_ because it is headless (it doesn't require OS with GUI).

Supported browsers:

* PhantomJS
* Android
* BlackBerry
* Firefox
* Chrome
* Ie
* Opera
* Safari

**Attributes** :

* _mh - MasterHead reference
* _client - selen client instance
* _browser - browser name
* _url - web page URL
* _confirm_alert - confirm or dimiss alert form

**Properties (Getters)** :

* client - returns _client
* browser - returns _browser
* url - returns _url
* confirm_alert - return _confirm_alert

**Properties (Setters)** :

* confirm_alert - sets _confirm_alert

**Methods** :

* __init__

Constructor sets _client to requested browser (PHANTOMJS by default) object instance. If browser is not supported NotImplementedError is raised.

  .. code-block:: python
  
     from hydratk.lib.bridge.selen import SeleniumBridge
     
     c = SeleniumBridge('PHANTOMJS')
     
* open

Method opens web page in browser. First it fires event selen_before_open where parameters (url, timeout) can be rewritten.
It sets timeout (default 20s) using selenium method set_page_load_timeout and gets page (using method get).
After that fires event selen_after_open and returns bool.

  .. code-block:: python
  
     url = 'http://127.0.0.1:8080/Autobot/'  
     res = c.open(url) 
     
* close

Method closes browser using selenium method quit.

  .. code-block:: python
  
     res = c.close()
     
* wait_for_element

Method waits for presence element on web page till given timeout (default 5s). First is fires event selen_before_wait where parameters (ident, method, timeout)
can be rewritten. Two check methods are supported: id (ident = unique element id), xpath (ident = xpath query).
Method uses selenium methods WebDriverWait and find_element_by_id or find_element_by_xpath.

After that it fires event selen_after_wait and returns bool (True when element found, False when not found within timeout).

  .. code-block:: python
  
     # method id
     res = c.wait_for_element('customerRead', 'id')
     
     # method xpath
     res = c.wait_for_element('//div[@id=\'customerRead\']', 'xpath')
     
* get_element

Method returns reference to element object. First it fires event selen_before_get_elem where parameters (ident, method, single) can be rewritten.  
Method supports several methods for element search, each one uses different selenium method.

id - uses find_element_by_id
class - uses find_element_by_class_name or find_elements_by_class_name
css - uses find_element_by_css_selector or find_elements_by_css_selector
text - uses find_element_by_link_text or find_elements_by_link_text
name - uses find_element_by_name or find_elements_by_name
tag - uses find_element_by_tag_name or find_elements_by_tag_name
xpath - uses find_element_by_xpath or find_elements_by_xpath

By default it returns first element which is found, uses single=False to return all elements.

  .. code-block:: python
  
     # id 
     res = c.get_element('customerRead', 'id')
     
     # class
     res = c.get_element('v-formlayout-row', 'class')
     
     # css
     res = c.get_element('.autobot .v-tabsheet-tabitemcell .v-caption .v-captiontext', 'css')
     
     # tag
     res = c.get_element('td', 'tag')
     
     # xpath
     res = c.get_element('//input[@type=\'text\']', 'xpath')
     
* read_element

Method reads element value. First it fires event selen_before_read_elem where parameters (ident, method, attr, attr_val) can be rewritten.
Parameters attr, attr_val are used to precise element search. attr is additional HTML element attribute, attr_val is requested value.
It gets elements object using method get_element (supports all methods) and searches the valid one.

Method returns value of attribute text. If element has no such attribute it returns None.
When you want to read elements which has not attribute text, you can use method exec_script and get the value via JavaScript.

  .. code-block:: python
  
     # element id 
     res = c.read_element('customerId')
     
     # element with attribute type = text
     res = c.read_element('customerId', attr='type', attr_val='text') 
     
     # element with attribute tabindex = 0
     res = c.read_element('customerId', attr='tabindex', attr_val='0')
     
* set_element

Methods sets element value. First it fires event selen_before_set_elem where parameters (ident, val, method, attr, attr_val) can be rewritten.
Parameters attr, attr_val are used to precise element search. attr is additional HTML element attribute, attr_val is requested value.      
It gets elements object using method get_element (supports all methods) and searches the valid one.

If element is checkbox, method checks/unchecks it. It gets current state using selenium method is_selected and then uses method click.
If element is button, method uses selenium method click.
Otherwise method use selenium method send_keys (it is considered text field). After that returns bool.

  .. code-block:: python
  
     # element id
     elem, val = 'customerId', 'xx'
     res = c.set_element(elem, val)
     
     # element with attribute type = text
     res = c.set_element('customerId', val, attr='type', attr_val='text')
     
* exec_script

Method executes JavaScript. First it fires event selen_before_script where parameter script can be rewritten.
It uses selenium method execute_script. Script parameters are passed as args.
After that fires event selen_after_script and returns script output.

  .. code-block:: python
  
     # read text field
     script = "return document.getElementById('{0}').value;".format(elem)
     res = c.exec_script(script)        
     
     # read select
     script = "var e = document.getElementById('customerStatus').getElementsByTagName('select')[0];return e.options[1].text;"
     res = c.exec_script(script) 
     
* save_screen

Method saves screenshot of web page. It works also for browser PhantomJS which is headless.
First it fires event selen_before_save_screen where parameter outfile (default screen.png)can be rewritten.
It uses selenium method save_screenshot. After that fires event selen_after_save_screen and returns bool.

  .. code-block:: python
  
     file = '/var/local/hydratk/test.png'
     res = c.save_screen(file)
     
* check_alert

Methods checks if alert is present and returns bool, str (alert text).
The form is confirmed or dismissed according to _confirm_url.
It uses selenium methods switch_to_alert, accept, dismiss.

* get_current_url

Methods returns current url using selenium method get_current_url.

* get_title

Method returns page title using selenium attribute title.

* go_back

Method emulates browser button back using selenium method back, it returns bool.

* refresh                                     

Method emulates browser button refresh using selenium method refresh, it returns bool.

* get_screen

Methods gets screenshot content in png (default) or base64 format.