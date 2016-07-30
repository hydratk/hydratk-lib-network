# -*- coding: utf-8 -*-
"""DBO PostgreSQL driver

.. module:: lib.database.dbo.drivers.sqlite.driver
   :platform: Unix
   :synopsis: DBO PosgreSQL driver
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import psycopg2
from  psycopg2.extras import RealDictCursor
import os
from hydratk.lib.database.dbo import dbodriver 

class DBODriver(dbodriver.DBODriver):
    """Class DBODriver
    """
        
    _host           = None
    _port           = 5432
    _dbname         = 'postgres'
    _driver_options = {
                   'timeout'           : 5.0,
                   'detect_types'      : 0,
                   'isolation_level'   : None, #available “DEFERRED”, “IMMEDIATE” or “EXCLUSIVE”
                   'check_same_thread' : None,
                   'factory'           : 'Connection',
                   'cached_statements' : 100
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
            #print(dsn_opt_token)
            opt = dsn_opt_token.split('=')
                     
            if opt[0] == 'host':
                self._host     = opt[1]
            if opt[0] == 'port':
                self._port     = int(opt[1])                    
            if opt[0] == 'database':
                self._dbname   = opt[1]
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
        
        #print(self._dbname, self._host, self._port, self._username, self._password)
        
        self._dbcon = psycopg2.connect(database=self._dbname, host=self._host, port=self._port, user=self._username, password=self._password)
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
        if type(self._dbcon).__name__ == 'connection':
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
                
        if hasattr(psycopg2, name):
            return getattr(psycopg2, name)
            
    def __getattr__(self,name):
        """Method gets attribute
        
        Args:   
           name (str): attribute name
           
        Returns:
           obj: attribute value
                
        """ 
                
        if type(self._dbcon).__name__ == 'Connection':    
            if hasattr(self._dbcon, name):
                return getattr(self._dbcon,name)
            
            if hasattr(psycopg2, name):
                return getattr(psycopg2,name) 
            
    def table_exists(self, table_name):
        """Method checks if table exists
        
        Args:   
           table_name (str): table
           
        Returns:
           bool: result (not working now)
                
        """ 
                
        if table_name is not None and table_name != '':
            query = "SELECT count(*) found FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' and table_name=%s"
            self._cursor.execute(query, [table_name])
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
                
        self._cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")
        tables = list(self._cursor.fetchall())
        query = ''
        for col in tables:
            query += "drop table if exists {0} cascade;".format(col['table_name'])        
        self._cursor.execute(query)
        self.commit()
    
    def result_as_dict(self, state):   
        """Method enales query result in dictionary form
        
        Args:   
           state (bool): enable dictionary
           
        Returns:
           void
           
        Raises:
           error: TypeError
                
        """ 
                    
        if state in (True, False):
            self._result_as_dict = state
            if state == True:                                                
                self._cursor = self._dbcon.cursor(cursor_factory=RealDictCursor)                
            else:                              
                self._cursor = self._dbcon.cursor()
        else:
            raise TypeError('Boolean value expected')
        