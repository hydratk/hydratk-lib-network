# -*- coding: utf-8 -*-
"""Bridge to Selenium WebDriver

.. module:: bridge.selen
   :platform: Unix
   :synopsis: Bridge to Selenium WebDriver
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
selen_before_save_video
selen_after_save_video

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support.events import AbstractEventListener
from selenium.webdriver.common.utils import is_url_connectable
from selenium.webdriver.remote.webelement import WebElement
from os import devnull
from datetime import datetime

browsers = [
    'FIREFOX',
    'CHROME'
]


class SeleniumBridge(object):
    """Class SeleniumBridge
    """

    _mh = None
    _client = None
    _browser = None
    _url = None
    _confirm_alert = True

    def __init__(self, browser, headless=False, save_video=False, filename=None, duration=0.5, **kwargs):
        """Class constructor

        Called when the object is initialized   

        Args:            
           browser (str): browser name
           headless (bool): headless mode
           save_video (bool): save video from browser
           filename (str): video filename
           duration (float): frame duration in seconds
           kwargs (dict): keyword arguments, browser specific

        Raises:
           error: NotImplementedError

        """

        self._mh = MasterHead.get_head()
        self._mh.find_module('hydratk.lib.bridge.selen', None)

        self._browser = browser.upper()
        if (self._browser in browsers):

            client = None
            if (self._browser == 'FIREFOX'):
                firefox_profile = kwargs['firefox_profile'] if ('firefox_profile' in kwargs) else None
                firefox_binary = kwargs['firefox_binary'] if ('firefox_binary' in kwargs) else None
                timeout = kwargs['timeout'] if ('timeout' in kwargs) else 30
                capabilities = kwargs['capabilities'] if ('capabilities' in kwargs) else webdriver.common.desired_capabilities.DesiredCapabilities.FIREFOX.copy()
                if ('capabilities' not in kwargs):
                    capabilities['acceptInsecureCerts'] = True

                proxy = kwargs['proxy'] if ('proxy' in kwargs) else None
                executable_path = kwargs['executable_path'] if ('executable_path' in kwargs) else 'geckodriver'
                options = kwargs['options'] if ('options' in kwargs) else None
                log_path = kwargs['log_path'] if ('log_path' in kwargs) else devnull

                firefox_options = kwargs['firefox_options'] if ('firefox_options' in kwargs) else webdriver.FirefoxOptions()
                if (headless):
                    firefox_options.add_argument('--headless')

                service_args = kwargs['service_args'] if ('service_args' in kwargs) else None
                desired_capabilities = kwargs['desired_capabilities'] if ('desired_capabilities' in kwargs) else None

                client = webdriver.firefox.webdriver.WebDriver(firefox_profile, firefox_binary, timeout, capabilities, proxy, executable_path,
                                                               options, log_path, firefox_options, service_args, desired_capabilities)

            elif (self._browser == 'CHROME'):
                executable_path = kwargs['executable_path'] if ('executable_path' in kwargs) else 'chromedriver'
                port = kwargs['port'] if ('port' in kwargs) else 0
                options = kwargs['options'] if ('options' in kwargs) else None
                service_args = kwargs['service_args'] if ('service_args' in kwargs) else None
                desired_capabilities = kwargs['desired_capabilities'] if ('desired_capabilities' in kwargs) else None
                service_log_path = kwargs['log_path'] if ('log_path' in kwargs) else devnull
                chrome_options = kwargs['chrome_options'] if ('chrome_options' in kwargs) else webdriver.ChromeOptions()
                if ('chrome-options' not in kwargs):
                    chrome_options.add_argument('--no-sandbox')
                    chrome_options.add_argument('--disable-dev-shm-usage')
                    chrome_options.add_argument('start-maximized')
                    chrome_options.add_argument('disable-infobars')
                    chrome_options.add_argument('--ignore-certificate-errors')
                if (headless):
                    chrome_options.add_argument('--headless')

                client = webdriver.chrome.webdriver.WebDriver(executable_path, port, options, service_args, desired_capabilities,
                                                              service_log_path, chrome_options)

            if (save_video):
                filename = filename if (filename != None) else 'movie_{0}.gif'.format(datetime.now().strftime('%Y%m%d%H%M%S'))
                self._client = EventFiringWebDriver(client, EventListener(filename, duration))
            else:
                self._client = client

        else:
            raise NotImplementedError(self._mh._trn.msg('htk_selen_unknown_browser', self._browser))

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

    @property
    def confirm_alert(self):
        """ confirm_alert property getter """

        return self._confirm_alert

    @confirm_alert.setter
    def confirm_alert(self, value):
        """ confirm_alert property setter """

        self._confirm_alert = value

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

            self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_opening', url), self._mh.fromhere())
            ev = event.Event('selen_before_open', url, timeout)
            if (self._mh.fire_event(ev) > 0):
                url = ev.argv(0)
                timeout = ev.argv(1)

            self._url = url
            if (ev.will_run_default()):

                self._client.set_page_load_timeout(timeout)
                self._client.get(url)

            self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_opened'), self._mh.fromhere())
            ev = event.Event('selen_after_open')
            self._mh.fire_event(ev)

            return True

        except WebDriverException as ex:
            self._mh.demsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
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
            self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_closed'), self._mh.fromhere())
            return True

        except WebDriverException as ex:
            self._mh.demsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
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

            self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_waiting', ident, timeout), self._mh.fromhere())
            ev = event.Event('selen_before_wait', ident, method, timeout)
            if (self._mh.fire_event(ev) > 0):
                ident = ev.argv(0)
                method = ev.argv(1)
                timeout = ev.argv(2)

            if (ev.will_run_default()):
                if (method == 'id'):
                    WebDriverWait(self._client, timeout).until(
                        lambda cond: self._client.find_element_by_id(ident))
                elif (method == 'xpath'):
                    WebDriverWait(self._client, timeout).until(
                        lambda cond: self._client.find_element_by_xpath(ident))

            self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_wait_finished'), self._mh.fromhere())
            ev = event.Event('selen_after_wait')
            self._mh.fire_event(ev)

            return True

        except WebDriverException as ex:
            self._mh.demsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False

    def get_element(self, ident, method='id', single=True):
        """Method gets element

        Args:            
           ident (mixed): (str) element identification, method specific or (object) WebElement
           method (str): search method, id|class|css|text|name|tag|xpath
           single (bool): get single element, used for method class|css|text|name|tag|xpath

        Returns:
           obj: WebElement or list of WebElement

        Raises:
           event: selenium_before_get_elem

        """

        try:

            self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_get', ident, method, single), self._mh.fromhere())
            ev = event.Event('selen_before_get_elem', ident, method, single)
            if (self._mh.fire_event(ev) > 0):
                ident = ev.argv(0)
                method = ev.argv(1)
                single = ev.argv(2)

            if (ev.will_run_default()):
                if isinstance(ident, WebElement):
                    return ident

                if (method == 'id'):
                    elements = self._client.find_element_by_id(ident)
                elif (method == 'class'):
                    if (single):
                        elements = self._client.find_element_by_class_name(
                            ident)
                    else:
                        elements = self._client.find_elements_by_class_name(
                            ident)
                elif (method == 'css'):
                    if (single):
                        elements = self._client.find_element_by_css_selector(
                            ident)
                    else:
                        elements = self._client.find_elements_by_css_selector(
                            ident)
                elif (method == 'text'):
                    if (single):
                        elements = self._client.find_element_by_link_text(
                            ident)
                    else:
                        elements = self._client.find_elements_by_link_text(
                            ident)
                elif (method == 'name'):
                    if (single):
                        elements = self._client.find_element_by_name(ident)
                    else:
                        elements = self._client.find_elements_by_name(ident)
                elif (method == 'tag'):
                    if (single):
                        elements = self._client.find_element_by_tag_name(ident)
                    else:
                        elements = self._client.find_elements_by_tag_name(
                            ident)
                elif (method == 'xpath'):
                    if (single):
                        elements = self._client.find_element_by_xpath(ident)
                    else:
                        elements = self._client.find_elements_by_xpath(ident)
                else:
                    return None

            return elements

        except WebDriverException as ex:
            self._mh.demsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None

    def read_element(self, ident, method='id', attr=None, attr_val=None, el_type=None):
        """Method reads element value

        Args:            
           ident (str): element identification, method specific
           method (str): search method, id|class|css|text|name|tag|xpath
           attr (str): element attribute or text, used as additional condition in element search
           attr_val (str): attribute or text value
           el_type (str): expected element type (read from attribute type by default)

        Returns:
           str: element value

        Raises:
           event: selenium_before_read_elem

        """

        try:

            message = 'ident:{0}, method:{1}, attr:{2}, attr_val:{3}, el_type:{4}'.format(ident, method, attr, attr_val, el_type)
            self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_read', message), self._mh.fromhere())

            ev = event.Event('selen_before_read_elem', ident, method, attr, attr_val, el_type)
            if (self._mh.fire_event(ev) > 0):
                ident = ev.argv(0)
                method = ev.argv(1)
                attr = ev.argv(2)
                attr_val = ev.argv(3)
                el_type = ev.argv(4)

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
                    return None

                elem_type = element.get_attribute('type') if (el_type == None) else el_type
                if (elem_type in ['checkbox', 'radio']):
                    result = element.is_selected()
                elif (elem_type == 'select'):
                    result = Select(element).first_selected_option.text
                elif (element.get_attribute('value') != None):
                    result = element.get_attribute('value')
                elif (hasattr(element, 'text')):
                    result = element.text
                else:
                    result = None

                return result

        except WebDriverException as ex:
            self._mh.demsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None

    def set_element(self, ident, val=None, method='id', attr=None, attr_val=None, el_type=None):
        """Method sets element value

        Args:            
           ident (str): element identification, method specific
           val (str): value to set
           method (str): search method, id|class|css|text|name|tag|xpath
           attr (str): element attribute or text, used as additional condition in element search
           attr_val (str): attribute or text value
           el_type (str): expected element type (read from attribute type by default)

        Returns:
           bool: result

        Raises:
           event: selenium_before_set_elem

        """

        try:

            message = 'ident:{0}, val:{1}, method:{2}, attr:{3}, attr_val:{4}, el_type:{5}'.format(ident, val, method, attr, attr_val, el_type)
            self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_set', message), self._mh.fromhere())

            ev = event.Event('selen_before_set_elem', ident, val, method, attr, attr_val, el_type)
            if (self._mh.fire_event(ev) > 0):
                ident = ev.argv(0)
                val = ev.argv(1)
                method = ev.argv(2)
                attr = ev.argv(3)
                attr_val = ev.argv(4)
                el_type = ev.argv(5)

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

                elem_type = element.get_attribute('type') if (el_type == None) else el_type
                if (elem_type in ['checkbox', 'radio']):
                    selected = element.is_selected()
                    if ((selected and not val) or (not selected and val)):
                        element.click()
                elif (elem_type == 'submit'):
                    element.click()
                elif (elem_type == 'select'):
                    Select(element).select_by_visible_text(val)
                else:
                    element.clear()
                    element.send_keys(val)

            return True

        except WebDriverException as ex:
            self._mh.demsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
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

            self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_executing_script', script), self._mh.fromhere())
            ev = event.Event('selen_before_script', script)
            if (self._mh.fire_event(ev) > 0):
                script = ev.argv(0)

            if (ev.will_run_default()):
                output = self._client.execute_script(script, *args)

            self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_script_executed'), self._mh.fromhere())
            ev = event.Event('selen_after_script')
            self._mh.fire_event(ev)

            return output

        except WebDriverException as ex:
            self._mh.demsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
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

            self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_saving_screen', outfile), self._mh.fromhere())
            ev = event.Event('selen_before_save_screen', outfile)
            if (self._mh.fire_event(ev) > 0):
                outfile = ev.argv(0)

            if (ev.will_run_default()):
                res = self._client.save_screenshot(outfile)

            if (res):
                self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_screen_saved'), self._mh.fromhere())
                ev = event.Event('selen_after_save_screen')
                self._mh.fire_event(ev)
                return True
            else:
                raise WebDriverException('Invalid path: {0}'.format(outfile))

        except WebDriverException as ex:
            self._mh.demsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False

    def check_alert(self, confirm=None):
        """Method checks if alert is present

        Args:    
           confirm (bool): confirm dialogue

        Returns:
           tuple: result (bool), value (str)

        """

        try:

            alert = self._client.switch_to_alert()
            value = alert.text
            confirm = confirm if (confirm != None) else self._confirm_alert

            if (confirm):
                alert.accept()
            else:
                alert.dismiss()

            return True, value

        except WebDriverException as ex:
            self._mh.demsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False, None

    def get_current_url(self):
        """Method gets current URL

        Args:    
           none        

        Returns:
           str

        """

        try:

            return self._client.current_url

        except WebDriverException as ex:
            self._mh.demsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False

    def get_title(self):
        """Method gets page title

        Args:    
           none        

        Returns:
           str

        """

        try:

            return self._client.title

        except WebDriverException as ex:
            self._mh.demsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False

    def go_back(self):
        """Method goes to previous page

        Args:    
           none        

        Returns:
           bool

        """

        try:

            self._client.back()
            return True

        except WebDriverException as ex:
            self._mh.demsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False

    def refresh(self):
        """Method refreshes page

        Args:    
           none        

        Returns:
           bool

        """

        try:

            self._client.refresh()
            return True

        except WebDriverException as ex:
            self._mh.demsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False

    def get_screen(self, output='png'):
        """Method gets screenshot content

        Args:    
           output (str): output type png|base64

        Returns:
           str

        """

        try:

            screen = None
            if (output == 'png'):
                screen = self._client.get_screenshot_as_png()
            elif (output == 'base64'):
                screen = self._client.get_screenshot_as_base64()

            return screen

        except WebDriverException as ex:
            self._mh.demsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False

class EventListener(AbstractEventListener):
    """Class EventListener
    """
    
    _mh = None
    _screens = []
    _filename = None
    _duration = 0.0

    def __init__(self, filename, duration):
        """Class constructor

        Called when the object is initialized

        Args:
           filename (str): video filename
           duration (float): frame duration in seconds

        """

        AbstractEventListener.__init__(self)

        self._mh = MasterHead.get_head()
        self._screens = []
        self._filename = filename
        self._duration = duration

    def _get_screen(self, driver):
        """Method gets screenshot

        Args:
           driver (obj): driver reference

        Returns:
           void

        """

        self._screens.append(driver.get_screenshot_as_png())
        
    def _save_video(self):
        """Method saves video from screenshots

        Args:
           none

        Returns:
           void

        """
        
        try:

            from imageio import imread, get_writer

            self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_saving_video', self._filename, self._duration), self._mh.fromhere())
            ev = event.Event('selen_before_save_video', self._filename, self._duration)
            if (self._mh.fire_event(ev) > 0):
                self._filename = ev.argv(0)
                self._duration = ev.argv(1)

            if (ev.will_run_default()):
                with get_writer(self._filename, duration=self._duration) as w:
                    for screen in self._screens:
                        w.append_data(imread(screen))

            self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('htk_selen_video_saved'), self._mh.fromhere())
            ev = event.Event('selen_after_save_video')
            self._mh.fire_event(ev)

        except Exception as ex:
            self._mh.demsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())

    def after_change_value(self, element, driver):
        
        self._get_screen(driver)

    def after_click(self, element, driver):

        self._get_screen(driver)

    def after_execute_script(self, script, driver):

        self._get_screen(driver)

    def after_navigate_back(self, driver):

        self._get_screen(driver)

    def after_navigate_forward(self, driver):

        self._get_screen(driver)

    def after_navigate_to(self, url, driver):

        self._get_screen(driver)

    def after_quit(self, driver):

        self._save_video()

    def before_close(self, driver):

        self._get_screen(driver)

    def before_quit(self, driver):

        self._get_screen(driver)
