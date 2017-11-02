# -*- coding: utf-8 -*-
"""MongoDB client

.. module:: network.dbi.nosql.mongodb_client
   :platform: Unix
   :synopsis: MongoDB client
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
from pymongo import MongoClient
from pymongo.errors import PyMongoError


class DBClient(object):
    """Class DBClient
    """

    _mh = None
    _client = None
    _host = None
    _port = None
    _db = None
    _user = None
    _passw = None
    _is_connected = None
    _db_obj = None

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

    def connect(self, host, port=27017, db='', user=None, passw=None, timeout=10):
        """Method connects to database

        Args:            
           host (str): host
           port (int): port
           db (str): database
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
                user, passw, host, port, db, timeout)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_dbi_connecting', message), self._mh.fromhere())

            ev = event.Event(
                'dbi_before_connect', host, port, db, user, passw, timeout)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                port = ev.argv(1)
                db = ev.argv(2)
                user = ev.argv(3)
                passw = ev.argv(4)
                timeout = ev.argv(5)

            if (ev.will_run_default()):
                self._host = host
                self._port = port
                self._db = db
                self._user = user
                self._passw = passw

                self._client = MongoClient(
                    host=self._host, port=self._port, connect=True, connectTimeoutMS=timeout * 1000)
                self._client.is_mongos
                self._db_obj = self._client[self._db]
                if (self._user != None):
                    self._db_obj.authenticate(self._user, self._passw)
                self._is_connected = True

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_dbi_connected'), self._mh.fromhere())
            ev = event.Event('dbi_after_connect')
            self._mh.fire_event(ev)

            return True

        except PyMongoError as ex:
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
                self._client.close()
                self._is_connected = False
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                    'htk_dbi_disconnected'), self._mh.fromhere())
                return True

        except PyMongoError as ex:
            self._mh.dmsg(
                'htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return False

    def exec_command(self, command, collection, document=None, filter=None, single=True):
        """Method executes command

        See MongoDB documentation for more info.

        Args:            
           command (str): command insert|find|aggregate|update|replace|delete|drop
           collection (str): collection name
           document (obj): json object or list of json objects (for many records), used for insert, update
           filter (obj): json object, used for find, aggregate, update, replace, delete
           single (bool): apply to single record

        Returns:
           tuple: result (bool), output (obj)
                  record id (obj) or records ids (list) for insert
                  records (list) for find, aggregate
                  records count for update, replace, delete
                  empty for drop

        Raises:
           event: dbi_before_exec_command
           event: dbi_after_exec_command

        """

        try:

            message = 'command:{0}, collection:{1}, document:{2}, filter:{3}, single:{4}'.format(
                command, collection, document, filter, single)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_dbi_executing_command', message), self._mh.fromhere())

            if (command not in ['insert', 'find', 'aggregate', 'update', 'replace', 'delete', 'drop']):
                self._mh.dmsg('htk_on_error', 'database error: unknown command {0}'.format(
                    command), self._mh.fromhere())
                return False, None

            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg(
                    'htk_dbi_not_connected'), self._mh.fromhere())
                return False, None

            ev = event.Event(
                'dbi_before_exec_command', command, collection, document, filter, single)
            if (self._mh.fire_event(ev) > 0):
                command = ev.argv(0)
                collection = ev.argv(1)
                document = ev.argv(2)
                filter = ev.argv(3)
                single = ev.argv(4)

            if (ev.will_run_default()):

                output = None
                col = self._db_obj[collection]
                if (command == 'insert'):
                    output = col.insert_one(document).inserted_id if (
                        single or document.__class__.__name__ != 'list') else col.insert_many(document).inserted_ids

                elif (command == 'find'):
                    res = col.find(filter)
                    output = []
                    for doc in res:
                        output.append(doc)

                elif (command == 'aggregate'):
                    res = col.aggregate(filter) if (
                        filter.__class__.__name__ == 'list') else col.aggregate([filter])
                    output = []
                    for doc in res:
                        output.append(doc)

                elif (command == 'update'):
                    output = col.update_one(filter, document).modified_count if (
                        single) else col.update_many(filter, document).modified_count

                elif (command == 'replace'):
                    output = col.replace_one(filter, document).modified_count

                elif (command == 'delete'):
                    output = col.delete_one(filter).deleted_count if (
                        single) else col.delete_many(filter).deleted_count

                elif (command == 'drop'):
                    col.drop()

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_dbi_command_executed'), self._mh.fromhere())
            ev = event.Event('dbi_after_exec_command', True, output)
            self._mh.fire_event(ev)

            return True, output

        except PyMongoError as ex:
            self._mh.dmsg(
                'htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return False, None
