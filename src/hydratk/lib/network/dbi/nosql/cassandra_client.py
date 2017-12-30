# -*- coding: utf-8 -*-
"""Cassandra client

.. module:: network.dbi.nosql.cassandra_client
   :platform: Unix
   :synopsis: MongoDB client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
dbi_before_connect
dbi_after_connect
dbi_before_exec_query
dbi_after_exec_query

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from cassandra.cluster import Cluster, DriverException, NoHostAvailable
from cassandra.auth import PlainTextAuthProvider
from cassandra.protocol import SyntaxException
from sys import version_info

if (version_info[0] == 2):
    from string import replace


class DBClient(object):
    """Class DBClient
    """

    _mh = None
    _client = None
    _host = None
    _port = None
    _key_space = None
    _user = None
    _passw = None
    _is_connected = None
    _session = None

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
    def key_space(self):
        """ key_space property getter """

        return self._key_space

    @property
    def user(self):
        """ user property getter """

        return self._user

    @property
    def passw(self):
        """ passw property getter """

        return self._passw

    @property
    def is_connected(self):
        """ is_connected property getter """

        return self._is_connected

    def connect(self, host, port=9042, key_space=None, user=None, passw=None, timeout=10):
        """Method connects to database

        Args:            
           host (obj): host (str) or hosts (list)
           port (int): port
           key_space (str): key space
           user (str) username
           passw (str): password
           timeout (int): timeout

        Returns:
           bool: result

        Raises:
           event: dbi_before_connect
           event: dbi_after_connect

        """

        try:

            message = '{0}/{1}@{2}:{3}/{4} timeout:{5}'.format(
                user, passw, host, port, key_space, timeout)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_dbi_connecting', message), self._mh.fromhere())

            ev = event.Event(
                'dbi_before_connect', host, port, key_space, user, passw, timeout)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                port = ev.argv(1)
                key_space = ev.argv(2)
                user = ev.argv(3)
                passw = ev.argv(4)
                timeout = ev.argv(5)

            if (ev.will_run_default()):
                self._host = host
                self._port = port
                self._key_space = key_space
                self._user = user
                self._passw = passw

                points = [self._host] if (
                    self._host.__class__.__name__ != 'list') else self._host
                auth = PlainTextAuthProvider(self._user, self._passw) if (
                    self._user != None) else None
                self._client = Cluster(
                    contact_points=points, port=self._port, auth_provider=auth, control_connection_timeout=timeout)
                self._session = self._client.connect()
                if (self._key_space != None):
                    self._session.execute('USE {0}'.format(self._key_space))
                self._is_connected = True

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_dbi_connected'), self._mh.fromhere())
            ev = event.Event('dbi_after_connect')
            self._mh.fire_event(ev)

            return True

        except (DriverException, NoHostAvailable, SyntaxException) as ex:
            self._mh.dmsg(
                'htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return False

    def disconnect(self):
        """Method disconnects from database

        Args:   
           none         

        Returns:
           bool: result

        """

        try:

            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg(
                    'htk_dbi_not_connected'), self._mh.fromhere())
                return False
            else:
                self._client.shutdown()
                self._is_connected = False
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                    'htk_dbi_disconnected'), self._mh.fromhere())
                return True

        except (DriverException, NoHostAvailable, SyntaxException) as ex:
            self._mh.dmsg(
                'htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return False

    def exec_query(self, query, bindings=None, fetch_one=False):
        """Method executes query

        See Cassandra documentation for more info.

        Args:            
           query (str): query, binded variables are marked with ?
           bindings (list): query bindings 
           fetch_one (bool): fetch one row only

        Returns:
           tuple: result (bool), rows (list) (accessible by row.column)

        Raises:
           event: dbi_before_exec_query
           event: dbi_after_exec_query   

        """

        try:

            message = query + \
                ' binding: {0}'.format(bindings) if (
                    bindings != None) else query
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_dbi_executing_query', message), self._mh.fromhere())

            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg(
                    'htk_dbi_not_connected'), self._mh.fromhere())
                return False, None

            ev = event.Event(
                'dbi_before_exec_query', query, bindings, fetch_one)
            if (self._mh.fire_event(ev) > 0):
                query = ev.argv(0)
                bindings = ev.argv(1)
                fetch_one = ev.argv(2)

            if (ev.will_run_default()):

                if ('SELECT' in query and 'ALLOW FILTERING' not in query):
                    query += ' ALLOW FILTERING'
                if (bindings != None):
                    query = replace(query, '?', '%s') if (
                        version_info[0] == 2) else query.replace('?', '%s')
                    rs = self._session.execute(query, list(bindings))
                else:
                    rs = self._session.execute(query)

                rows = []
                for row in rs:
                    rows.append(row)
                if (fetch_one):
                    rows = rows[0]

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_dbi_query_executed'), self._mh.fromhere())
            ev = event.Event('dbi_after_exec_query', True, rows)
            self._mh.fire_event(ev)

            return True, rows

        except (DriverException, NoHostAvailable, SyntaxException) as ex:
            self._mh.dmsg(
                'htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return False, None
