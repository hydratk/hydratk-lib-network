# -*- coding: utf-8 -*-
"""DBO Oracle driver

.. module:: lib.database.dbo.drivers.oracle.driver
   :platform: Unix
   :synopsis: DBO Oracle driver
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

import cx_Oracle
from hydratk.lib.database.dbo import dbodriver
from platform import python_implementation


class DBODriver(dbodriver.DBODriver):
    """Class DBODriver
    """

    _host = None
    _port = 1521
    _dbname = None
    _driver_options = {
        'timeout': 5.0,
        'detect_types': 0,
        # available “DEFERRED”, “IMMEDIATE” or “EXCLUSIVE”
        'isolation_level': None,
        'check_same_thread': None,
        'factory': 'Connection',
                   'cached_statements': 100,
                   'auto_commit': True
    }

    def _parse_dsn(self, dsn):
        """Method parses dsn

        Args:   
           dsn (str): dsn

        Returns:
           bool: True

        Raises:
           exception: Exception

        """
        dsn_opt = dsn.split(':')[1]
        dsn_opt_tokens = dsn_opt.split(';')
        for dsn_opt_token in dsn_opt_tokens:
            # print(dsn_opt_token)
            opt = dsn_opt_token.split('=')

            if opt[0] == 'host':
                self._host = opt[1]
            if opt[0] == 'port':
                self._port = int(opt[1])
            if opt[0] == 'database':
                self._dbname = opt[1]
            if opt[0] == 'user':
                self._username = opt[1]
            if opt[0] == 'password':
                self._password = opt[1]

        return True

    def _apply_driver_options(self, driver_options):
        """Method sets driver options

        Args:   
           driver_option (dict): driver options

        Returns:
           void

        """

        for optname, optval in driver_options.items():
            if optname in self._driver_options:
                self._driver_options[optname] = optval

    def connect(self):
        """Method connects to database

        Args:   
           none

        Returns:
           void

        """

        dsn = '{0}:{1}/{2}'.format(self._host, self._port, self._dbname)
        self._dbcon = cx_Oracle.connect(
            dsn=dsn, user=self._username, password=self._password)
        self.result_as_dict(self._result_as_dict)

    def close(self):
        """Method disconnects from database

        Args:  
           none 

        Returns:
           void

        Raises:
           exception: DBODriverException

        """
        if type(self._dbcon).__name__.lower() == 'connection':
            self._dbcon.close()
        else:
            raise dbodriver.DBODriverException('Not connected')

    def commit(self):
        """Method commits transaction

        Args:
           none   

        Returns:
           void

        Raises:
           exception: DBODriverException

        """

        if type(self._dbcon).__name__.lower() == 'connection':
            self._dbcon.commit()
        else:
            raise dbodriver.DBODriverException('Not connected')

    def error_code(self):
        pass

    def error_info(self):
        pass

    def qexec(self):
        pass

    def get_attribute(self):
        pass

    def in_transaction(self):
        pass

    def last_insert_id(self):
        pass

    def prepare(self):
        pass

    def query(self):
        pass

    def execute(self, sql, *parameters):
        """Method executes query

        Args:   
           sql (str): SQL query
           parameters (args): query parameters

        Returns:
           obj: cursor

        """

        self._cursor.execute(sql, *parameters)
        if (self._result_as_dict and 'SELECT' in sql.upper()):
            self._cursor.rowfactory = self._make_dict(self._cursor)
        elif (self._driver_options['auto_commit']):
            self.commit()
        return self._cursor

    def quote(self):
        pass

    def rollback(self):
        """Method rollbacks transaction

        Args: 
           none  

        Returns:
           void

        Raises:
           exception: DBODriverException

        """

        if type(self._dbcon).__name__.lower() == 'connection':
            self._dbcon.rollback()
        else:
            raise dbodriver.DBODriverException('Not connected')

    def set_attribute(self):
        pass

    def __getitem__(self, name):
        """Method gets item

        Args:   
           name (str): item name

        Returns:
           obj: item value

        """

        if hasattr(cx_Oracle, name):
            return getattr(cx_Oracle, name)

    def __getattr__(self, name):
        """Method gets attribute

        Args:   
           name (str): attribute name

        Returns:
           obj: attribute value

        """

        if type(self._dbcon).__name__.lower() == 'connection':
            if hasattr(self._dbcon, name):
                return getattr(self._dbcon, name)

            if hasattr(cx_Oracle, name):
                return getattr(cx_Oracle)

    def table_exists(self, table_name):
        """Method checks if table exists

        Args:   
           table_name (str): table

        Returns:
           bool: result

        """

        if table_name is not None and table_name != '':
            query = "SELECT count(*) found FROM all_tables WHERE owner=:1 AND table_name=:2"
            self._cursor.execute(
                query, [self._username.upper(), table_name.upper()])
            self._cursor.rowfactory = self._make_dict(self._cursor)
            recs = self._cursor.fetchall()
            result = True if (recs[0]['found'] == 1) else False
        return result

    def database_exists(self):
        pass

    def remove_database(self):
        pass

    def erase_database(self):
        """Method drops database

        Args:  
           none 

        Returns:
           void

        """

        self._cursor.execute(
            "SELECT table_name FROM all_tables WHERE owner=:1", [self._username.upper()])
        self._cursor.rowfactory = self._make_dict(self._cursor)
        tables = list(self._cursor.fetchall())
        for col in tables:
            self._cursor.execute(
                "drop table {0} cascade constraints".format(col['table_name']))
        self.commit()

    def result_as_dict(self, state):
        """Method enables query result in dictionary form

        Args:   
           state (bool): enable dictionary

        Returns:
           void

        Raises:
           error: TypeError

        """

        if state in (True, False):
            self._result_as_dict = state
            self._cursor = self._dbcon.cursor()
        else:
            raise TypeError('Boolean value expected')

    def _make_dict(self, cursor):
        """Method for overriding row factory to return dictionary  

        Args:   
           cursor (obj): database cursor

        Returns:
           method

        """

        columns = [d[0].lower() for d in cursor.description]

        def create_row(*args):
            if (python_implementation() == 'PyPy'):
                args = args[0]
            return dict(zip(columns, args))
        return create_row
