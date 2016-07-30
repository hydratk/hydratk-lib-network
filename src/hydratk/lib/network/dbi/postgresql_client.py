# -*- coding: utf-8 -*-
"""PostgreSQL DB client

.. module:: network.dbi.postgresql_client
   :platform: Unix
   :synopsis: PostgreSQL DB client
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
from psycopg2 import Error, connect
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
    _sid = None
    _user = None
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
        """ PostgreSQL client property getter """
        
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
    def sid(self):
        """ server SID property getter """
        
        return self._sid
    
    @property
    def user(self):
        """ username property getter """
        
        return self._user
    
    @property
    def passw(self):
        """ user password property getter """
        
        return self._passw           
    
    @property
    def is_connected(self):
        """ is_connected property getter """
        
        return self._is_connected      
        
    def connect(self, host=None, port=5432, sid=None, user=None, passw=None, timeout=10):
        """Method connects to database
        
        Args:            
           host (str): hostname
           port (int): port
           sid (str): db instance
           user (str): username
           passw (str): password
           timeout (int): timeout
             
        Returns:
           bool: result
           
        Raises:
           event: dbi_before_connect
           event: dbi_after_connect
                
        """        
        
        try:
                    
            message = '{0}/{1}@{2}:{3}/{4} timeout:{5}'.format(user, passw, host, port, sid, timeout)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_connecting', message), self._mh.fromhere())
            
            ev = event.Event('dbi_before_connect', host, port, sid, user, passw, timeout)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                port = ev.argv(1)
                sid = ev.argv(2)
                user = ev.argv(3)
                passw = ev.argv(4)  
                timeout = ev.argv(5)          
            
            if (ev.will_run_default()):
                self._host = host     
                self._port = port           
                self._sid = sid
                self._user = user
                self._passw = passw
                
                self._client = connect(host=self._host, port=self._port, database=self._sid,
                                       user=self._user, password=self._passw, connect_timeout=timeout)
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
                cur = self._client.cursor()    
                
                if (bindings != None):
                    query = replace(query, '?', '%s') if (version_info[0] == 2) else query.replace('?', '%s')
                    cur.execute(query, tuple(bindings))
                else:
                    cur.execute(query)

                rows = None
                if (cur.description != None):
                    columns = [i[0].lower() for i in cur.description]                    
                    rows = [dict(zip(columns, row)) for row in cur]          
                
                if (fetch_one):
                    rows = rows[0] if (len(rows) > 0) else [] 
                   
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