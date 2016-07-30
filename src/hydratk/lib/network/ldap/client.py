# -*- coding: utf-8 -*-
"""Generic LDAP client

.. module:: network.ldap.client
   :platform: Unix
   :synopsis: Generic LDAP client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
ldap_before_connect
ldap_after_connect
ldap_before_read
ldap_after_read
ldap_before_create
ldap_after_create
ldap_before_update
ldap_after_update
ldap_before_delete
ldap_after_delete

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from hydratk.lib.array.operation import subdict
from ldap import set_option, initialize, LDAPError, OPT_DEBUG_LEVEL, OPT_NETWORK_TIMEOUT, SCOPE_BASE, SCOPE_SUBTREE
from ldap.modlist import addModlist, modifyModlist

class LDAPClient(object):
    """Class LDAPClient
    """
    
    _mh = None
    _client = None
    _host = None
    _port = None
    _secured = None
    _user = None
    _passw = None
    _base_dn = None
    _verbose = None
    _is_connected = None
    
    def __init__(self, verbose=False):
        """Class constructor
           
        Called when the object is initialized   
        
        Args:
           verbose (bool): verbose mode        
           
        """          
        
        self._mh = MasterHead.get_head() 
        self._mh.find_module('hydratk.lib.network.ldap.client', None)  
                          
        self._verbose = verbose
        if (self._verbose):
            set_option(OPT_DEBUG_LEVEL, 1)
        
    @property
    def client(self):
        """ LDAP client property getter """
        
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
    def secured(self):
        """ secured property getter """
        
        return self._secured     
    
    @property
    def user(self):
        """ user property getter """
        
        return self._user 
    
    @property
    def passw(self):
        """ passw property getter """
        
        return self._passw      
    
    @property
    def base_dn(self):
        """ base_dn property getter """
        
        return self._base_dn  
    
    @property
    def verbose(self):   
        """ verbose mode property getter """
        
        return self._verbose       
    
    @property
    def is_connected(self):   
        """ is_connected property getter """
        
        return self._is_connected                      
    
    def connect(self, host, base_dn, port=None, user=None, passw=None, secured=False, timeout=10):
        """Method connects to server
        
        Args:
           host (str): server host
           base_dn (str): base distinguished name
           port (str): server port, default protocol port                      
           user (str): username, default without base_dn
           passw (str): password
           secured (bool): secured protocol
           timeout (int): timeout

        Returns:
           bool: result         
             
        Raises:
           event: ldap_before_connect
           event: ldap_after_connect     
                
        """           
        
        try:            
                         
            message = 'host:{0}, base_dn:{1}, port:{2}, secured:{3}, user:{4}, passw:{5}, timeout:{6}'.format(
                       host, base_dn, port, secured, user, passw, timeout)                            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ldap_connecting', message), self._mh.fromhere())

            ev = event.Event('ldap_before_connect', host, base_dn, port, secured, user, passw, timeout)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                base_dn = ev.argv(1)
                port = ev.argv(2)
                secured = ev.argv(3)
                user = ev.argv(4)
                passw = ev.argv(5)               
                timeout = ev.argv(6)
            
            self._host = host
            self._port = port
            self._secured = secured
            self._base_dn = base_dn
            self._user = user
            self._passw = passw  
            
            if (ev.will_run_default()):  
                    
                if (self._port == None):
                    self._port = 389 if (not self._secured) else 636
                    
                protocol = 'ldap' if (not self._secured) else 'ldaps'                                        
                uri = '{0}://{1}:{2}'.format(protocol, self._host, self._port)                         
                self._client = initialize(uri) 
                self._client.set_option(OPT_NETWORK_TIMEOUT, timeout)

                if (self._user != None):
                    user = self._user
                    if ('cn=' not in self._user and 'uid=' not in self._user):
                        user = 'cn={0},{1}'.format(self._user, self._base_dn)
                    self._client.simple_bind_s(user, self._passw)                                     
                else:
                    self._client.simple_bind_s()
                
                self._is_connected = True
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ldap_connected'), self._mh.fromhere()) 
            ev = event.Event('ldap_after_connect')
            self._mh.fire_event(ev)   
                                                   
            return True                      
            
        except LDAPError as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False              
    
    def disconnect(self):        
        """Method disconnects from server
        
        Args:
           none
           
        Returns:
           bool: result         
                
        """           
         
        try:                                                 
                
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_ldap_not_connected'), self._mh.fromhere()) 
                return False
            else:                
                self._client.unbind()          
                self._is_connected = False     
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ldap_disconnected'), self._mh.fromhere())  
                return True  
    
        except LDAPError as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False 
        
    def read(self, rdn=None, filter='objectClass=*', attrs=[], fetch_one=False, get_child=True, 
             cn_only=False, attrs_only=False):
        """Method reads records
        
        Args:
           rdn (str): relative distinguished name (inc. organization unit)
           filter (str): search filter, default all object classes
           attrs (list): returned attributes, default all
           fetch_one (bool): fetch one record
           get_child (bool): get also child records
           cn_only (bool): get common name only
           attrs_only (bool): get attributes only

        Returns:
           list: records, dictionary of attributes        
             
        Raises:
           event: ldap_before_read
           event: ldap_after_read     
                
        """         
        
        try:
            
            message = 'rdn:{0}, filter:{1}, attrs:{2}'.format(rdn, filter, attrs) + \
                      ', fetch_one:{0}, cn_only:{1}, attrs:{2}'.format(fetch_one, cn_only, attrs_only)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ldap_reading', message), self._mh.fromhere())
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_ldap_not_connected'), self._mh.fromhere()) 
                return None            
            
            ev = event.Event('ldap_before_read', rdn, filter, attrs, get_child, fetch_one, cn_only, attrs_only)
            if (self._mh.fire_event(ev) > 0):
                rdn = ev.argv(0)
                filter = ev.argv(1)
                attrs = ev.argv(2)
                get_child = ev.argv(3) 
                fetch_one = ev.argv(4) 
                cn_only = ev.argv(5)
                attrs_only = ev.argv(6)
                
            if (ev.will_run_default()):  
                
                base = self._base_dn if (rdn == None) else '{0},{1}'.format(rdn, self._base_dn)
                scope = SCOPE_SUBTREE if (get_child and not attrs_only) else SCOPE_BASE
                recs = self._client.search_s(base=base, scope=scope, filterstr=filter, attrlist=attrs)
                
                if (fetch_one):
                    recs = [recs[0]]
                
                records = []
                if (cn_only):
                    for rec in recs:
                        records.append(rec[0])
                elif (attrs_only):
                    records = recs[0][1].keys()
                else:
                    for rec in recs:
                        record = rec[1]
                        record['CN'] = rec[0]  
                        
                        for key, value in record.items():
                            if (value.__class__.__name__ == 'list'):
                                if (len(value) > 1):
                                    for i in range(0, len(value)):
                                        value[i] = value[i].decode()
                                    record[key] = value
                                else:
                                    record[key] = value[0].decode()
                                                                                          
                        records.append(record)

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ldap_read', len(records)), self._mh.fromhere()) 
            ev = event.Event('ldap_after_read')
            self._mh.fire_event(ev)   
                                                   
            return records                                   
            
        except LDAPError as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None                
        
    def create(self, rdn, attrs={}):
        """Method creates record
        
        Args:
           rdn (str): relative distinguished name (inc. organization unit)
           attrs (dict): attributes attr/value, internally transformed to LDIF

        Returns:
           bool: result        
             
        Raises:
           event: ldap_before_create 
           event: ldap_after_create
                
        """   
        
        try:
                           
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ldap_creating', rdn, attrs), self._mh.fromhere())
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_ldap_not_connected'), self._mh.fromhere()) 
                return False            
            
            ev = event.Event('ldap_before_create', rdn, attrs)
            if (self._mh.fire_event(ev) > 0):
                rdn = ev.argv(0)              
                attrs = ev.argv(1)
            
            if (ev.will_run_default()):  
                dn = '{0},{1}'.format(rdn, self._base_dn) 
                for key, val in attrs.items():
                    if (val.__class__.__name__ == 'list'):
                        for i in range(0, len(val)):
                            attrs[key][i] = bytes(str(val[i]).encode('utf-8'))
                    else:
                        attrs[key] = bytes(str(val).encode('utf-8'))                                  
                ldif = addModlist(attrs)
                self._client.add_s(dn, ldif)
                                          
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ldap_created'), self._mh.fromhere()) 
            ev = event.Event('ldap_after_create')
            self._mh.fire_event(ev)
                        
            return True       
        
        except LDAPError as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False          
    
    def update(self, rdn, attrs):
        """Method updates record
        
        Args:
           rdn (str): relative distinguished name (inc. organization unit)
           attrs (dict): attributes attr/value, cn/uid will is used to change RDN
                         current attributes are read internally, transformed to LDIF

        Returns:
           bool: result        
             
        Raises:
           event: ldap_before_update 
           event: ldap_after_update
                
        """ 
        
        try:
                           
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ldap_updating', rdn, attrs), self._mh.fromhere())
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_ldap_not_connected'), self._mh.fromhere()) 
                return False            
            
            ev = event.Event('ldap_before_update', rdn, attrs)
            if (self._mh.fire_event(ev) > 0):
                rdn = ev.argv(0)              
                attrs = ev.argv(1)
            
            if (ev.will_run_default()):     
                dn = '{0},{1}'.format(rdn, self._base_dn)                          
                recs = self.read(rdn, fetch_one=True)
                
                if(recs == None):
                    return False
                                
                record = recs[0]           
                rdn_new = None
                if ('cn' in attrs or 'uid' in attrs):
                    key = 'cn' if 'cn' in attrs else 'uid'
                    rdn_new = attrs[key]
                    del attrs[key]                                                                                         
                
                attrs_old = subdict(record, attrs.keys())                          
                ldif = modifyModlist(attrs_old, attrs)
                
                for i in range(0, len(ldif)):
                    item = list(ldif[i])
                    if (item[0] == 0 and item[1] in attrs):
                        val = attrs[item[1]]
                        if (val.__class__.__name__ == 'list'):
                            for j in range(0, len(val)):
                                val[j] = bytes(str(val[j]).encode('utf-8'))
                            item[i][2] = val
                        else:
                            item[2] = [bytes(str(val).encode('utf-8'))]
                    ldif[i] = tuple(item)
                            
                self._client.modify_s(dn, ldif)
                
                if (rdn_new != None):
                    rdn = rdn.split(',')[0]
                    rdn_new = rdn.replace(rdn.split('=')[1], rdn_new)
                    self._client.modrdn_s(dn, rdn_new)
                                          
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ldap_updated'), self._mh.fromhere()) 
            ev = event.Event('ldap_after_update')
            self._mh.fire_event(ev)
                        
            return True       
        
        except LDAPError as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False          
    
    def delete(self, rdn):        
        """Method deletes record
        
        Args:
           rdn (str): relative distinguished name (inc. organization unit)

        Returns:
           bool: result        
             
        Raises:
           event: ldap_before_delete  
           event: ldap_after_delete
                
        """   
        
        try:
                           
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ldap_deleting', rdn), self._mh.fromhere())
            
            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_ldap_not_connected'), self._mh.fromhere()) 
                return False            
            
            ev = event.Event('ldap_before_delete', rdn)
            if (self._mh.fire_event(ev) > 0):
                dn = ev.argv(0)              
            
            if (ev.will_run_default()):  
                dn = '{0},{1}'.format(rdn, self._base_dn)                             
                self._client.delete_s(dn)
                                          
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ldap_deleted'), self._mh.fromhere()) 
            ev = event.Event('ldap_after_delete')
            self._mh.fire_event(ev)
                        
            return True       
        
        except LDAPError as ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False            