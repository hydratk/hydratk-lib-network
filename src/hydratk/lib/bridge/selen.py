# -*- coding: utf-8 -*-
"""Bridge to Selenium webdriver

.. module:: bridge.selen
   :platform: Unix
   :synopsis: Bridge to Selenium webdriver
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
selen_before_open
selen_after_open
selen_before_wait
selen_after_wait
selen_before_get_elem
selen_before_read_elem
selen_before_set_elem
selen_before_script
selen_after_script
selen_before_save_screen
selen_after_save_screen

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.utils import is_url_connectable
from importlib import import_module

browsers = {
  'ANDROID'    : 'Android',
  'BLACKBERRY' : 'BlackBerry',
  'FIREFOX'    : 'Firefox',
  'CHROME'     : 'Chrome',
  'IE'         : 'Ie',
  'OPERA'      : 'Opera',
  'PHANTOMJS'  : 'PhantomJS',
  'SAFARI'     : 'Safari'
}            

class SeleniumBridge(object):
    """Class SeleniumBridge
    """
    
    _mh = None
    _client = None
    _browser = None
    _url = None
    
    def __init__(self, browser='PhantomJS'):
        """Class constructor
           
        Called when the object is initialized   
        
        Args:            
           browser (str): browser name, default PhantomJS
           
        Raises:
           error: NotImplementedError
                
        """           
        
        self._mh = MasterHead.get_head()
        self._mh.find_module('hydratk.lib.bridge.selen', None)  
                
        self._browser = browser.upper()
        if (self._browser in browsers):
            
            mod = import_module('selenium.webdriver')   
            if (self._browser == 'PHANTOMJS'):                
                client = mod.__dict__[browsers[self._browser]](service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
                client.set_window_size(1024, 768)         
            else:
                client = mod.__dict__[browsers[self._browser]]()
                
            self._client = client            

        else:
            raise NotImplementedError('Unknown browser:{0}'.format(browser)) 
        
    @property
    def client(self):
        """ client property getter """
        
        return self._client
    
    @property
    def browser(self):
        """ browser property getter """
        
        return self._browser
    
    @property
    def url(self):
        """ url property getter """
        
        return self._url        
    
    def open(self, url, timeout=20):
        """Method opens web page from URL
        
        Args:            
           url (str): page URL
           timeout (int): timeout
             
        Returns:
           bool: result
           
        Raises:
           event: selen_before_open
           event: selen_after_open
                
        """         
        
        try:
        
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_opening', url), self._mh.fromhere())
            ev = event.Event('selen_before_open', url, timeout)
            if (self._mh.fire_event(ev) > 0):
                url = ev.argv(0)
                timeout = ev.argv(1)
          
            self._url = url
            if (ev.will_run_default()): 
                
                self._client.set_page_load_timeout(timeout)
                self._client.get(url)
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_opened'), self._mh.fromhere())
            ev = event.Event('selen_after_open')
            self._mh.fire_event(ev)    
                
            return True
            
        except WebDriverException as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False  
        
    def close(self):
        """Method closes client
        
        Args:    
           none        
             
        Returns:
           bool: result
                
        """         
        
        try:
                    
            self._client.quit()
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_closed'), self._mh.fromhere())
            return True
        
        except WebDriverException as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False                  
        
    def wait_for_element(self, ident, method='id', timeout=5):
        """Method waits for element presence till timeout 
        
        Args:            
           ident (str): element id
           method (str): search method id|xpath
           timeout (float): timeout   
           
        Returns:
           bool           
           
        Raises:
           event: selenium_before_wait
           event: selenium_after_wait
                
        """   
           
        try:
               
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_waiting', ident, timeout), self._mh.fromhere())
            ev = event.Event('selen_before_wait', ident, timeout)
            if (self._mh.fire_event(ev) > 0):
                ident = ev.argv(0) 
                timeout = ev.argv(1)              
             
            if (ev.will_run_default()): 
                if (method == 'id'):   
                    WebDriverWait(self._client, timeout).until(lambda cond: self._client.find_element_by_id(ident))
                elif (method == 'xpath'):
                    WebDriverWait(self._client, timeout).until(lambda cond: self._client.find_element_by_xpath(ident))
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_wait_finished'), self._mh.fromhere())
            ev = event.Event('selen_after_wait')
            self._mh.fire_event(ev) 
            
            return True               
         
        except WebDriverException as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())   
            return False           
        
    def get_element(self, ident, method='id', single=True):
        """Method gets element
        
        Args:            
           ident (str): element identification, method specific
           method (str): search method, id|class|css|text|name|tag|xpath
           single (bool): get single element, used for method class|css|text|name|tag|xpath
             
        Returns:
           obj: WebElement or list of WebElement
           
        Raises:
           event: selenium_before_get_elem
                
        """          
        
        try:
        
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_get', ident, method, single), self._mh.fromhere())
            ev = event.Event('selen_before_get_elem', ident, method, single)
            if (self._mh.fire_event(ev) > 0):
                ident = ev.argv(0)
                method = ev.argv(1)
                single = ev.argv(2)         
        
            if (ev.will_run_default()): 
                if (method == 'id'):
                    elements = self._client.find_element_by_id(ident)
                elif (method == 'class'):            
                    if (single):
                        elements = self._client.find_element_by_class_name(ident)
                    else:
                        elements = self._client.find_elements_by_class_name(ident)      
                elif (method == 'css'):            
                    if (single):
                        elements = self._client.find_element_by_css_selector(ident)
                    else:
                        elements = self._client.find_elements_by_css_selector(ident) 
                elif (method == 'text'):            
                    if (single):
                        elements = self._client.find_element_by_link_text(ident)
                    else:
                        elements = self._client.find_elements_by_link_text(ident)   
                elif (method == 'name'):            
                    if (single):
                        elements = self._client.find_element_by_name(ident)
                    else:
                        elements = self._client.find_elements_by_name(ident)                         
                elif (method == 'tag'):            
                    if (single):
                        elements = self._client.find_element_by_tag_name(ident)
                    else:
                        elements = self._client.find_elements_by_tag_name(ident)
                elif (method == 'xpath'):
                    if (single):
                        elements = self._client.find_element_by_xpath(ident)
                    else:
                        elements = self._client.find_elements_by_xpath(ident) 
                else:
                    return None 
        
            return elements
        
        except WebDriverException as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None    
        
    def read_element(self, ident, method='id', attr=None, attr_val=None):
        """Method reads element value
        
        Args:            
           ident (str): element identification, method specific
           method (str): search method, id|class|css|text|name|tag|xpath
           attr (str): element attribute or text, used as additional condition in element search
           attr_val (str): attribute or text value
             
        Returns:
           str: element value
           
        Raises:
           event: selenium_before_read_elem
                
        """             
        
        try:
        
            message = 'ident:{0}, method:{1}, attr:{2}, attr_val:{3}'.format(ident, method, attr, attr_val)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_read', message), self._mh.fromhere())
            
            ev = event.Event('selen_before_read_elem', ident, method, attr, attr_val)
            if (self._mh.fire_event(ev) > 0):
                ident = ev.argv(0)        
                method = ev.argv(1)
                attr = ev.argv(2)
                attr_val = ev.argv(3)
        
            if (ev.will_run_default()): 
                element = None
                if (attr != None):
                    elements = self.get_element(ident, method, False)
                    elements = [elements] if (elements.__class__.__name__ != 'list') else elements
                    for item in elements:
                        if (attr == 'text' and item.text == attr_val):
                            element = item
                            break
                        elif (item.get_attribute(attr) == attr_val):
                            element = item
                    
                else:
                    element = self.get_element(ident, method)                         
            
                result = element.text if (hasattr(element, 'text')) else None
                return result
        
        except WebDriverException as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None         
    
    def set_element(self, ident, val=None, method='id', attr=None, attr_val=None):    
        """Method sets element value
        
        Args:            
           ident (str): element identification, method specific
           val (str): value to set
           method (str): search method, id|class|css|text|name|tag|xpath
           attr (str): element attribute or text, used as additional condition in element search
           attr_val (str): attribute or text value
             
        Returns:
           bool: result
           
        Raises:
           event: selenium_before_set_elem
                
        """           
        
        try:
        
            message = 'ident:{0}, val:{1}, method:{2}, attr:{3}, attr_val:{4}'.format(ident, val, method, attr, attr_val)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_set', message), self._mh.fromhere())
            
            ev = event.Event('selen_before_set_elem', ident, val, method, attr, attr_val)
            if (self._mh.fire_event(ev) > 0):
                ident = ev.argv(0)      
                val = ev.argv(1)
                method = ev.argv(2)
                attr = ev.argv(3)
                attr_val = ev.argv(4)  
        
            if (ev.will_run_default()): 
                element = None
                if (attr != None):
                    elements = self.get_element(ident, method, False)
                    elements = [elements] if (elements.__class__.__name__ != 'list') else elements
                    for item in elements:
                        if (attr == 'text' and item.text == attr_val):
                            element = item
                            break
                        elif (item.get_attribute(attr) == attr_val):
                            element = item
                    
                else:
                    element = self.get_element(ident, method)                         
            
                if (element == None):
                    return False
              
                elem_type = element.get_attribute('type')            
                if (elem_type == 'checkbox'):    
                    selected = element.is_selected()
                    if ((selected and not val) or (not selected and val)):
                        element.click()
                elif (elem_type == 'submit'):
                    element.click()
                else:
                    element.send_keys(val)
                            
            return True     
    
        except WebDriverException as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False  
        
    def exec_script(self, script, *args):    
        """Method execute JavaScript code
        
        Args:            
           script (str): JavaScript code
           args (args): script arguments   
           
        Returns:
           obj: script output
           
        Raises:
           event: selen_before_script
           event: selen_after_script 
                
        """    
        
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_executing_script', script), self._mh.fromhere())
            
            ev = event.Event('selen_before_script', script)
            if (self._mh.fire_event(ev) > 0):
                script = ev.argv(0)    
                
            if (ev.will_run_default()): 
                output = self._client.execute_script(script, *args)
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_script_executed'), self._mh.fromhere())
            ev = event.Event('selen_after_script')
            self._mh.fire_event(ev)   
            
            return output                 
            
        except WebDriverException as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())   
            return None    
        
    def save_screen(self, outfile='screen.png'):    
        """Method saves screenshot
        
        Args:            
           outfile (str): output filename
             
        Returns:
           bool: result  
           
        Raises:
           event: selen_before_save_screen
           event: selen_after_save_screen      
                
        """    
        
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_saving_screen', outfile), self._mh.fromhere())
            
            ev = event.Event('selen_before_save_screen', outfile)
            if (self._mh.fire_event(ev) > 0):
                outfile = ev.argv(0)    
                
            if (ev.will_run_default()): 
                res = self._client.save_screenshot(outfile)
                
            if (res):    
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_screen_saved'), self._mh.fromhere())
                ev = event.Event('selen_after_save_screen')
                self._mh.fire_event(ev)                  
                return True
            else:
                raise WebDriverException('Invalid path: {0}'.format(outfile))     
            
        except WebDriverException as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False                                                                                             