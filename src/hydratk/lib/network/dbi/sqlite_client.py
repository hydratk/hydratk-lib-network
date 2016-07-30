# -*- coding: utf-8 -*-
"""SQLite DB client

.. module:: network.dbi.sqlite_client
   :platform: Unix
   :synopsis: SQLite DB client
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
from sqlite3 import Error, connect, Row

class DBClient(object):
    """Class DBClient
    """
    
    _mh = None
    _client = None
    _db_file = None
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
    def db_file(self):
        """ database file property getter """
        
        return self._db_file
    
    @property 
    def is_connected(self):
        """ is_connected property getter """
        
        return self._is_connected    
        
    def connect(self, db_file, timeout=10):            
        """Method connects to database
        
        Args:            
           db_file (str): path to database file
           timeout (int): timeout
             
        Returns:
           bool: result
           
        Raises:
           event: dbi_before_connect
           event: dbi_after_connect
                
        """        
        
        try:
                    
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_connecting', db_file), self._mh.fromhere())
            
            ev = event.Event('dbi_before_connect', db_file)
            if (self._mh.fire_event(ev) > 0):
                db_file = ev.argv(0)               
            
            if (ev.will_run_default()):
                self._db_file = db_file
                self._client = connect(self._db_file, timeout=timeout)
                self._client.execute('PRAGMA foreign_keys = ON')   
                self._is_connected = True            

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_connected'), self._mh.fromhere())
            ev = event.Event('dbi_after_connect')
            self._mh.fire_event(ev)   
                        
            return True
    
        except Error as ex:
            self._mh.dmsg('htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
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
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_dbi_not_connected'), self._mh.fromhere()) 
                return False        
            else:            
                self._client.close()
                self._is_connected = False
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_disconnected'), self._mh.fromhere())
                return True
        
        except Error as ex:
            self._mh.dmsg('htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return False    
        
    def exec_query(self, query, bindings=None, fetch_one=False, autocommit=True):
        """Method executes query
        
        Args:            
           query (str): query, binded variables are marked with ?
           bindings (list): query bindings 
           fetch_one (bool): fetch one row only
           autocommit (bool): autocommit
             
        Returns:
           tuple: result (bool), rows (list) (accessible by column name)
          
        Raises:
           event: dbi_before_exec_query
           event: dbi_after_exec_query   
                
        """        
        
        try:
                    
            message = query + ' binding: {0}'.format(bindings) if (bindings != None) else query
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_executing_query', message), self._mh.fromhere())
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_dbi_not_connected'), self._mh.fromhere()) 
                return False, None          
            
            ev = event.Event('dbi_before_exec_query', query, bindings, fetch_one, autocommit)
            if (self._mh.fire_event(ev) > 0):
                query = ev.argv(0)
                bindings = ev.argv(1)
                fetch_one = ev.argv(2)          
                autocommit = ev.argv(3)

            if (ev.will_run_default()):
                self._client.row_factory = Row
                cur = self._client.cursor()    
                
                if (bindings != None):
                    cur.execute(query, tuple(bindings))
                else:
                    cur.execute(query)      
                
                if (fetch_one):
                    rows = cur.fetchone()
                else:
                    rows = cur.fetchall()           
                
                if (autocommit and 'SELECT ' not in query.upper()):
                    self._client.commit()
                
            cur.close()  
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_query_executed'), self._mh.fromhere())
            ev = event.Event('dbi_after_exec_query', True, rows)
            self._mh.fire_event(ev) 
                                      
            return True, rows
        
        except Error as ex:            
            if ('SELECT ' not in query.upper()):
                self._client.rollback()
            
            self._mh.dmsg('htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return False, None     
        
    def commit(self):
        """Method commits transaction
        
        Args:            
           none
             
        Returns:
           bool: result
                
        """    
        
        try:
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_dbi_not_connected'), self._mh.fromhere()) 
                return False  
            else:            
                self._client.commit()
                return True
            
        except Error as ex:
            self._mh.dmsg('htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return False    
        
    def rollback(self):
        """Method rollbacks transaction
        
        Args:            
           none
             
        Returns:
           bool: result
                
        """    
        
        try:
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_dbi_not_connected'), self._mh.fromhere()) 
                return False  
            else:            
                self._client.rollback()
                return True
            
        except Error as ex:
            self._mh.dmsg('htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return False                          