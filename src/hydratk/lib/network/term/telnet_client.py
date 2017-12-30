# -*- coding: utf-8 -*-
"""Telnet client

.. module:: network.lib.telnet_client
   :platform: Unix
   :synopsis: Telnet client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
term_before_connect
term_after_connect
term_before_exec_command
term_after_exec_command

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from telnetlib import Telnet
from socket import error
from sys import version_info


class TermClient(object):
    """Class TermClient
    """

    _mh = None
    _client = None
    _host = None
    _port = None
    _verbose = None
    _is_connected = None
    _br = None

    def __init__(self, verbose=False, br='\n'):
        """Class constructor

        Called when the object is initialized 

        Args:      
           verbose (bool): verbose mode
           br (str): line break character

        """

        self._mh = MasterHead.get_head()
        self._client = Telnet()

        self._br = br
        self._verbose = verbose
        if (self._verbose):
            self._client.set_debuglevel(2)

    @property
    def client(self):
        """ Telnet client property getter """

        return self._client

    @property
    def host(self):
        """ server host property getter """

        return self._host

    @property
    def port(self):
        """ server port property getter """

        return self._port

    @property
    def verbose(self):
        """ verbose mode property getter """

        return self._verbose

    @property
    def is_connected(self):
        """ is client connected property getter """

        return self._is_connected

    def connect(self, host, port=23, timeout=10):
        """Method connects to server

        Args:
           host (str): server host
           port (int): server port, default protocol port
           timeout (int): timeout           

        Returns:
           tuple: result (bool), output (list)

        Raises:
           event: term_before_connect
           event: term_after_connect          

        """

        try:

            message = '{0}:{1} timeout:{2}'.format(host, port, timeout)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_term_connecting', message), self._mh.fromhere())

            ev = event.Event('term_before_connect', host, port, timeout)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                port = ev.argv(1)
                timeout = ev.argv(2)

            self._host = host
            self._port = port

            if (ev.will_run_default()):
                self._client.open(self._host, self._port, timeout=timeout)
                self._is_connected = True
                out = self._read()

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_term_connected'), self._mh.fromhere())
            ev = event.Event('term_after_connect')
            self._mh.fire_event(ev)

            return True, out

        except error as ex:
            self._mh.dmsg(
                'htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            self._client.close()
            return False, [str(ex)]

    def disconnect(self):
        """Method disconnects from server

        Args:
           none

        Returns:
           bool: result

        """

        try:

            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg(
                    'htk_term_not_connected'), self._mh.fromhere())
                return False
            else:
                self._client.close()
                self._is_connected = False
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                    'htk_term_disconnected'), self._mh.fromhere())
                return True

        except error as ex:
            self._mh.dmsg(
                'htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False

    def exec_command(self, command):
        """Method executes command

        Args:
           command (str): command                   

        Returns:
           tuple: result (bool), output (list)

        Raises:
           event: term_before_exec_command
           event: term_after_exec_command   

        """

        try:

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_term_executing_command', command), self._mh.fromhere())

            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg(
                    'htk_term_not_connected'), self._mh.fromhere())
                return False, None

            ev = event.Event('term_before_exec_command', command)
            if (self._mh.fire_event(ev) > 0):
                command = ev.argv(0)

            if (ev.will_run_default()):
                command += self._br
                self._client.write(
                    command if (version_info[0] == 2) else command.encode('utf-8'))
                out = self._read()

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_term_command_executed'), self._mh.fromhere())
            ev = event.Event('term_after_exec_command')
            self._mh.fire_event(ev)

            return True, out

        except error as ex:
            self._mh.dmsg(
                'htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False, [str(ex)]

    def _read(self):
        """Method reads server output

        Args:
           none                 

        Returns:
           list

        """

        buff, out = [], None
        while (out != '' and out != b''):
            out = self._client.read_until(
                self._br if (version_info[0] == 2) else self._br.encode('utf-8'), 2)
            buff.append(out)

        return buff[:-1]
