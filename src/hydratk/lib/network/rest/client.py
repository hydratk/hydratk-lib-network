# -*- coding: utf-8 -*-
"""Generic REST client for protocols HTTP, HTTPS

.. module:: network.rest.client
   :platform: Unix
   :synopsis: Generic REST client for protocols HTTP, HTTPS
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
rest_before_request
rest_after_request

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
import requests
from requests.exceptions import RequestException
from requests.packages.urllib3 import disable_warnings
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from requests_ntlm import HttpNtlmAuth
from simplejson import loads
from simplejson.scanner import JSONDecodeError
from lxml import objectify
from lxml.etree import XMLSyntaxError
from sys import stderr
from os import path

mime_types = {
    'file': 'multipart/form-data',
    'form': 'application/x-www-form-urlencoded',
    'html': 'text/html',
    'json': 'application/json',
    'text': 'text/plain',
    'xml': 'application/xml'
}


class RESTClient(object):
    """Class RESTClient
    """

    _mh = None
    _url = None
    _proxies = None
    _cert = None
    _req_header = None
    _req_body = None
    _res_status = None
    _res_header = None
    _res_body = None
    _cookies = None
    _verbose = None
    _config = {}
    _history = None

    def __init__(self, verbose=False):
        """Class constructor

        Called when the object is initialized 

        Args:                   
           verbose (bool): verbose mode

        """

        self._mh = MasterHead.get_head()
        self._mh.find_module('hydratk.lib.network.rest.client', None)

        self._verbose = verbose
        if (self._verbose):
            self._config['verbose'] = stderr
        else:
            disable_warnings()

    @property
    def url(self):
        """ URL property getter """

        return self._url

    @property
    def proxies(self):
        """ proxies property getter """

        return self._proxies

    @property
    def cert(self):
        """ cert property getter """

        return self._cert

    @property
    def req_header(self):
        """ request header property getter """

        return self._req_header

    @property
    def req_body(self):
        """ request body property getter """

        return self._req_body

    @property
    def res_status(self):
        """ response status code property getter """

        return self._res_status

    @property
    def res_header(self):
        """ response header property getter """

        return self._res_header

    @property
    def res_body(self):
        """ response body property getter """

        return self._res_body

    @property
    def cookies(self):
        """ cookies property getter """

        return self._cookies

    @property
    def verbose(self):
        """ verbose mode property getter """

        return self._verbose

    @property
    def config(self):
        """ config property getter """

        return self._config

    @property
    def history(self):
        """ history property getter """

        return self._history

    def send_request(self, url, proxies=None, user=None, passw=None, auth='Basic', cert=None, verify_cert=True, method='GET', headers=None,
                     cookies=None, body=None, params=None, file=None, content_type=None, timeout=10):
        """Method sends request to server

        Args:
           url (str): URL
           proxies (dict): HTTP proxies {http: url, https: url}
           user (str): username
           passw (str): password     
           auth (str): authentication type Basic|Digest|NTLM      
           cert (obj): str (path to cert.perm path), tuple (path to cert.pem path, path to key.pem path)
           verify_cert (bool): verify certificate
           method (str): HTTP method GET|POST|PUT|DELETE|HEAD|OPTIONS
           headers (dict): HTTP headers
           cookies (dict): cookies (name:value)
           body (str): request body, POST method used by default
           params (dict): parameters, sent in URL for GET method, in body for POST|PUT|DELETE method
           file (str): filename including path, download for GET, upload for POST|PUT
           content_type (str): type of content, file|form|html|json|text|xml
           timeout (int): timeout

        Returns:
           tuple: status (int), body (str) (json object, xml object, otherwise original string)

        Raises:
           event: rest_before_request
           event: rest_after_request

        """

        try:

            message = 'url:{0}, proxies:{1}, user:{2}, passw:{3}, auth:{4}, cert:{5}, '.format(url, proxies, user, passw, auth, cert) + \
                      'verify_cert:{0}, method:{1}, headers:{2}, cookies:{3}, body:{4}, params:{5}, '.format(verify_cert, method, headers, cookies, body, params) + \
                      'file:{0}, content_type:{1}, timeout:{2}'.format(
                          file, content_type, timeout)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_rest_request', message), self._mh.fromhere())

            ev = event.Event('rest_before_request', url, proxies, user, passw, auth, cert, verify_cert,
                             method, headers, cookies, body, params, file, content_type, timeout)
            if (self._mh.fire_event(ev) > 0):
                url = ev.argv(0)
                proxies = ev.argv(1)
                user = ev.argv(2)
                passw = ev.argv(3)
                auth = ev.argv(4)
                cert = ev.argv(5)
                verify_cert = ev.argv(6)
                method = ev.argv(7)
                headers = ev.argv(8)
                cookies = ev.argv(9)
                body = ev.argv(10)
                params = ev.argv(11)
                file = ev.argv(12)
                content_type = ev.argv(13)
                timeout = ev.argv(14)

            if (ev.will_run_default()):

                if (user != None):
                    if (auth == 'Basic'):
                        auth = HTTPBasicAuth(user, passw)
                    elif (auth == 'Digest'):
                        auth = HTTPDigestAuth(user, passw)
                    elif (auth == 'NTLM'):
                        auth = HttpNtlmAuth(user, passw)
                    else:
                        auth = HTTPBasicAuth(user, passw)
                else:
                    auth = None

                self._url = url
                self._proxies = proxies
                self._cert = cert
                verify = True if (cert != None and verify_cert) else False

                method = method.lower() if (
                    method.lower() in ['get', 'post', 'put', 'delete', 'head', 'options']) else 'get'
                if (params != None and method in ('post', 'put', 'delete')):
                    content_type = 'form'
                if (body != None and method == 'get'):
                    method = 'post'
                file_dict = None
                if (file != None):
                    if (method in ['post', 'put']):
                        if (not path.exists(file)):
                            self._mh.dmsg('htk_on_error', self._mh._trn.msg(
                                'htk_rest_unknown_file', file), self._mh.fromhere())
                            return None, None
                        file_dict = {'file': open(file, 'rb')}
                    elif (method == 'get'):
                        filepath = '/'.join(file.split('/')[:-1])
                        if (filepath != '' and not path.exists(filepath)):
                            self._mh.dmsg('htk_on_error', self._mh._trn.msg(
                                'htk_rest_unknown_dir', filepath), self._mh.fromhere())
                            return None, None
                if (content_type != None and content_type in mime_types):
                    if (headers == None):
                        headers = {}
                    headers['Content-Type'] = mime_types[content_type]

                res = None
                res = getattr(requests, method)(self._url, proxies=proxies, auth=auth, cert=cert, params=params, data=body, headers=headers,
                                                cookies=cookies, files=file_dict, timeout=timeout, verify=verify)
                self._res_status, self._res_header, body = res.status_code, res.headers, res.text
                self._cookies, self._history = res.cookies, res.history

                if (file != None and method == 'get'):
                    body = None
                    with open(file, 'wb') as f:
                        f.write(res.content)

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_rest_response', self._res_status, self._res_header, body), self._mh.fromhere())
            ev = event.Event('rest_after_request')
            self._mh.fire_event(ev)

            content_type = self.get_header('Content-Type')
            if (content_type != None):
                if ('json' in content_type and len(body) > 0):
                    body = loads(body)
                elif ('xml' in content_type and len(body) > 0):
                    body = objectify.fromstring(body.encode('utf-8'))

            if (body.__class__.__name__ == 'bytes'):
                body = body.decode('latin-1')
            self._res_body = body

            return (self._res_status, self._res_body)

        except (RequestException, JSONDecodeError, XMLSyntaxError) as ex:
            if (str(ex) == 'WWW-Authenticate'):
                return (401, None)
            self._mh.dmsg(
                'htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            status = res.status_code if (res != None) else None
            body = res.text if (res != None) else None
            return status, body

    def get_header(self, title):
        """Method gets response header

        Args:
           title (str): header title

        Returns:
           str: header

        """

        title = title.lower()
        if (title in self._res_header):
            return self._res_header[title]
        else:
            return None
