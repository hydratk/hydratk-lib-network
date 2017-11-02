# -*- coding: utf-8 -*-
"""Redis client

.. module:: network.dbi.nosql.redis_client
   :platform: Unix
   :synopsis: Redis client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
dbi_before_connect
dbi_after_connect
dbi_before_exec_command
dbi_after_exec_command

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from redis import StrictRedis, RedisError
from sys import version_info


class DBClient(object):
    """Class DBClient
    """

    _mh = None
    _client = None
    _host = None
    _port = None
    _db = None
    _passw = None
    _is_connected = None

    def __init__(self):
        """Class constructor

        Called when the object is initialized   

        Args:  
           none     

        """

        self._mh = MasterHead.get_head()

    @property
    def client(self):
        """ SQLite client property getter """

        return self._client

    @property
    def host(self):
        """ host property getter """

        return self._host

    @property
    def port(self):
        """ port property getter """

        return self._port

    @property
    def db(self):
        """ db property getter """

        return self._db

    @property
    def passw(self):
        """ passw property getter """

        return self._passw

    @property
    def is_connected(self):
        """ is_connected property getter """

        return self._is_connected

    def connect(self, host, port=6379, db=0, passw=None, timeout=10):
        """Method connects to database

        Args:            
           host (str): host
           port (int): port
           db (int): database
           passw (str): password
           timeout (int): timeout

        Returns:
           bool: result

        Raises:
           event: dbi_before_connect
           event: dbi_after_connect

        """

        try:

            message = '{0}:{1}/{2} passw:{3}, timeout:{4}'.format(
                host, port, db, passw, timeout)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_dbi_connecting', message), self._mh.fromhere())

            ev = event.Event(
                'dbi_before_connect', host, port, db, passw, timeout)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                port = ev.argv(1)
                db = ev.argv(2)
                passw = ev.argv(3)
                timeout = ev.argv(4)

            if (ev.will_run_default()):
                self._host = host
                self._port = port
                self._db = db
                self._passw = passw

                self._client = StrictRedis(host=self._host, port=self._port, db=self._db, password=self._passw,
                                           socket_connect_timeout=timeout)
                self._client.execute_command('PING')
                self._is_connected = True

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_dbi_connected'), self._mh.fromhere())
            ev = event.Event('dbi_after_connect')
            self._mh.fire_event(ev)

            return True

        except RedisError as ex:
            self._mh.dmsg(
                'htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return False

    def exec_command(self, command):
        """Method executes command

        See Redis documentation for more info.

        Args:            
           command (str): command

        Returns:
           tuple: result (bool), output (obj)

        Raises:
           event: dbi_before_exec_command
           event: dbi_after_exec_command

        """

        try:

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_dbi_executing_command', command), self._mh.fromhere())

            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg(
                    'htk_dbi_not_connected'), self._mh.fromhere())
                return False, None

            ev = event.Event('dbi_before_exec_command', command)
            if (self._mh.fire_event(ev) > 0):
                command = ev.argv(0)

            if (ev.will_run_default()):
                output = self._client.execute_command(command)
                if (version_info[0] == 3 and output.__class__.__name__ == 'bytes'):
                    output = output.decode()

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_dbi_command_executed'), self._mh.fromhere())
            ev = event.Event('dbi_after_exec_command', True, output)
            self._mh.fire_event(ev)

            return True, output

        except RedisError as ex:
            self._mh.dmsg(
                'htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return False, None

    def get(self, key):
        """Method executes command GET

        Args:            
           key (str): key

        Returns:
           str: value

        """

        command = 'GET {0}'.format(key)
        res, output = self.exec_command(command)
        return output

    def set(self, key, value):
        """Method executes command SET

        Args:            
           key (str): key
           value (str): value

        Returns:
           bool

        """

        command = 'SET {0} {1}'.format(key, value)
        res, output = self.exec_command(command)
        return res

    def exists(self, key):
        """Method executes command EXISTS

        Args:            
           key (str): key

        Returns:
           bool

        """

        command = 'EXISTS {0}'.format(key)
        res, output = self.exec_command(command)
        return output

    def delete(self, key):
        """Method executes command DEL

        Args:            
           key (str): key           

        Returns:
           bool

        """

        command = 'DEL {0}'.format(key)
        res, output = self.exec_command(command)
        return res
