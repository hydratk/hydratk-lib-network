# -*- coding: utf-8 -*-
"""XML-RPC client

.. module:: network.rpc.jsonrpc_client
   :platform: Unix
   :synopsis: JSON-RPC client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
rpc_before_init_proxy
rpc_after_init_proxy
rpc_before_call_method
rpc_after_call_method

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from socket import error, setdefaulttimeout
from jsonrpclib import Server, Fault
from jsonrpclib.jsonrpc import ProtocolError
from sys import version_info

try:
    from xmlrpclib import ProtocolError as ProtocolError2
    from exceptions import IOError
except ImportError:
    from xmlrpc.client import ProtocolError as ProtocolError2


class RPCClient(object):
    """Class RPCClient
    """

    _mh = None
    _proxy = None

    def __init__(self):
        """Class constructor

        Called when the object is initialized

        Args:                   
           none

        """

        self._mh = MasterHead.get_head()

    @property
    def proxy(self):
        """ proxy object property getter """

        return self._proxy

    def init_proxy(self, url, timeout=10):
        """Method initializes proxy to remote object

        Args:            
           url (str): remote object url
           timeout (int): timeout

        Returns:
           bool: result

        Raises:
           event: rpc_before_init_proxy
           event: rpc_after_init_proxy

        """

        ex_list = (Fault, ProtocolError, ProtocolError2, error, IOError) if (
            version_info[0] == 2) else (ProtocolError, error, IOError)

        try:

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_rpc_init_proxy', url), self._mh.fromhere())

            ev = event.Event('rpc_before_init_proxy', url, timeout)
            if (self._mh.fire_event(ev) > 0):
                url = ev.argv(0)
                timeout = ev.argv(1)

            if (ev.will_run_default()):
                setdefaulttimeout(timeout)
                self._proxy = Server(url)

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_rpc_proxy_initialized'), self._mh.fromhere())
            ev = event.Event('rpc_after_init_proxy')
            self._mh.fire_event(ev)

            return True

        except ex_list as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return False

    def call_method(self, name, *args):
        """Method call remote method

        Args:         
           name (str): method name   
           args (args): method parameters

        Returns:
           obj: method output

        Raises:
           event: rpc_before_call_method
           event: rpc_after_call_method

        """

        ex_list = (Fault, ProtocolError, ProtocolError2, error, IOError) if (
            version_info[0] == 2) else (ProtocolError, error, IOError)

        try:

            args = list(args)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_rpc_call_method', name, args), self._mh.fromhere())

            if (self._proxy is None):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg(
                    'htk_rpc_proxy_not_init'), self._mh.fromhere())
                return None

            ev = event.Event('rpc_before_call_method', name, args)
            if (self._mh.fire_event(ev) > 0):
                name = ev.argv(0)
                args = ev.argv(1)

            if (ev.will_run_default()):
                output = getattr(self._proxy, name)(*args)

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_rpc_method_called', output), self._mh.fromhere())
            ev = event.Event('rpc_after_call_method')
            self._mh.fire_event(ev)

            return output

        except ex_list as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None
