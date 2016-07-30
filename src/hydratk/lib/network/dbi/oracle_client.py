# -*- coding: utf-8 -*-
"""ORACLE DB client

.. module:: network.dbi.oracle_client
   :platform: Unix
   :synopsis: ORACLE DB client
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
from cx_Oracle import Error, connect, NUMBER, STRING, TIMESTAMP, CLOB, BLOB
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
    
    _data_types = {
       'int'      : NUMBER,
       'float'    : NUMBER,
       'string'   : STRING,
       'timestamp': TIMESTAMP,
       'clob'     : CLOB,
       'blob'     : BLOB
    }
    
    def __init__(self):
        """Class constructor
           
        Called when the object is initialized  
        
        Args: 
           none       
           
        """    
        
        self._mh = MasterHead.get_head() 
        
    @property
    def client(self):
        """ Oracle client property getter """
        
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
        
    def connect(self, host=None, port=1521, sid=None, user=None, passw=None):
        """Method connects to database
        
        Args:            
           host (str): hostname
           port (int): port
           sid (str): db instance
           user (str): username
           passw (str): password
             
        Returns:
           bool: result
           
        Raises:
           event: dbi_before_connect
           event: dbi_after_connect
                
        """        
        
        try:
                    
            message = '{0}/{1}@{2}:{3}/{4}'.format(user, passw, host, port, sid)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_connecting', message), self._mh.fromhere())
            
            ev = event.Event('dbi_before_connect', host, port, sid, user, passw)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                port = ev.argv(1)
                sid = ev.argv(2)
                user = ev.argv(3)
                passw = ev.argv(4)   
            
            if (ev.will_run_default()):
                self._host = host 
                self._port = port               
                self._sid = sid
                self._user = user
                self._passw = passw
                
                dsn_str = '{0}:{1}/{2}'.format(self._host, self._port, self._sid)
                self._client = connect(user=self._user, password=self._passw, dsn=dsn_str)                      
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
            
            ev = event.Event('dbi_before_exec_query', query, bindings, fetch_one)
            if (self._mh.fire_event(ev) > 0):
                query = ev.argv(0)
                bindings = ev.argv(1)
                fetch_one = ev.argv(2)          

            if (ev.will_run_default()):
                cur = self._client.cursor()    
                
                if (bindings != None):
                    for i in range(0, len(bindings)):
                        query = replace(query, '?', ':{0}'.format(i+1), 1) if (version_info[0] == 2) else query.replace('?', ':{0}'.format(i+1), 1)

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
        
    def call_proc(self, p_name, param_names=[], i_values={}, o_types={}, type='proc', ret_type=None, autocommit=True):
        """Method calls procedure/function from database
        
        Args:
           p_name (str): procedure name
           param_names (list): parameter names (input, output)
           i_values (dict): input parameter values
           o_types (dict): output parameter types  
           type (str): code type, func|function|proc|procedure
           ret_type (str): return type, string, optional, used for function only
           autocommit (bool): autocommit                    
             
        Returns:
           tuple: result (according to ret_type) (for function only), params (dict)
           
        Raises:
           event: dbi_before_call_proc
           event: dbi_after_call_proc
                
        """        
        
        try:                    
        
            message = p_name + ' params: {0}'.format(i_values) if (len(i_values) > 0) else p_name
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_calling_proc', message), self._mh.fromhere())
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_dbi_not_connected'), self._mh.fromhere()) 
                return None             
            
            ev = event.Event('dbi_before_call_proc', p_name, param_names, i_values, o_types, type, ret_type)
            if (self._mh.fire_event(ev) > 0):
                p_name = ev.argv(0)
                param_names = ev.argv(1)
                i_values = ev.argv(2)   
                o_types = ev.argv(3)
                type = ev.argv(4)
                ret_type = ev.argv(5)                          
            
            if (ev.will_run_default()):
                if (type not in ('func', 'function', 'proc', 'procedure')):
                    self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_dbi_unknown_type', self.type), self._mh.fromhere())
                    return None
                
                cur = self._client.cursor()
            
                params = []
                for name in param_names:
                    if (name in i_values):
                        params.append(i_values[name])
                    elif (name in o_types):
                        
                        if (o_types[name].lower() == 'cursor'):
                            params.append(self._client.cursor())
                        else:
                            params.append(cur.var(self._data_types[o_types[name].lower()])) 
                    else:
                        params.append(None)                               
                
                if (type in ('func', 'function')):
                    result = cur.callfunc(p_name, self._data_types[ret_type.lower()], params) 
                else:
                    cur.callproc(p_name, params)
                                   
                output = {}
                i = 0 
                for param in params:
                    name = param_names[i]
                                                  
                    if (param.__class__.__module__ == 'cx_Oracle'):
                        
                        if (param.__class__.__name__ == 'Cursor'):
                            columns = [j[0].lower() for j in param.description]                    
                            param = [dict(zip(columns, row)) for row in param]                              
                        else:
                            param = param.getvalue()
                            if (name in o_types and o_types[name] == 'int' and param != None):
                                param = int(param)
                    
                    if (name in o_types):    
                        output[name] = param
                    i = i+1 
                    
                if (autocommit):
                    self._client.commit()             
            
            cur.close()  
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_proc_called', output), self._mh.fromhere())
            
            if (type in ('func', 'function')): 
                ev = event.Event('dbi_after_call_proc', result, output) 
                self._mh.fire_event(ev)               
                return result, output
            else:
                ev = event.Event('dbi_after_call_proc', output) 
                self._mh.fire_event(ev)                 
                return output
        
        except Error as ex:
            self._client.rollback()
            self._mh.dmsg('htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return None      
        
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