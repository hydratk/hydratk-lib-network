.. _module_lib_network_ldap:

LDAP
====

This sections contains module documentation of ldap module.

client
^^^^^^

Module client provides class LDAPClient for LDAP protocol using external module
`python-ldap <https://www.python-ldap.org/docs.html>`_ in version >= 2.4.25.
python-ldap requires non-Python libraries which are automatically installed by setup script (libldap2-dev, libsasl2-dev, libssl-dev for apt-get, 
openldap-devel for yum). 

When Python3 is used python-ldap is replaced by module `pyldap <https://github.com/pyldap/pyldap>`_ in version >= 2.4.25 which provides compatible interface.
Unit tests available at hydratk/lib/network/ldap/client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - ldap client instance
* _host - server hostname (or IP address)
* _port - port number (default 389 for LDAP, 636 for LDAPS)
* _secured - bool, secured protocol LDAPS
* _user - username
* _passw - password
* _base_dn - base distinguished name
* _verbose - verbose mode, disabled by default
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* client - returns _client
* host - returns _host
* port - returns _port
* secured - returns _secured
* user - returns _user
* passw - returns _passw
* base_dn - returns _base_dn
* verbose - returns _verbose
* is_connected - returns _is_connected

**Methods** :

* __init__ 

Sets MasterHeade reference and turns on verbose mode using ldap method set_option (if enabled).

* connect 

Connects to server (specified via host, base_dn, port, user, passw, secured).  First fires event ldap_before_connect where parameters can be rewritten. Calls Java method connect.
Connects to server using ldap methods initialize, simple_bind_s (including authentication). After successful connection fires event 
ldap_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.ldap.client import LDAPClient
     
     res = c.connect(host='127.0.0.1', base_dn='dc=test,dc=com', port=389, user='admin', passw='bowman', secured=False)
     
* disconnect

Disconnects from server using ldap method unbind and returns bool.

  .. code-block:: python
  
     res = c.disconnect() 
     
* read

Reads records from database. First fires event ldap_before_read where parameters (rdn, filter, attrs, fetch_one, get_child, cn_only, attrs_only) 
can be rewritten. rdn is relative distinguished name and is appended to base_dn if provided, otherwise method searches within whole base_dn.
filter is objectClass=* by default (no filtering) and is LDAP database schema specific. attrs is list of returned attributes (all by default).

fetch_one is bool, only one record is returned (all records returned by default). get_child is bool, top level including child records
are returned (True by default). cn_only is bool, only common name is returned (False by default). attrs_only is bool, only attribute names
are returned without the records (False by default).

Method reads record using ldap method search_s according to given base, scope (top-level or children), filter, attributes.
The result is transformed to dictionary form (key CN is always present even if not requested, it is record identifier)
After that method fires event ldap_after_read and returns list of dictionary (key - attribute name, value - attribute value).

  .. code-block:: python
  
     # single record
     res = c.read('ou=groups', fetch_one=True)
     # returns [{'objectClass': ['organizationalUnit', 'top'], 'ou': 'groups', 'CN': 'ou=groups,'+base_dn}]
     
     # multiple records
     res = c.read('ou=groups', fetch_one=False)
     
     # top-level records
     res = c.read('ou=groups', get_child=False)
     
     # common name
     res = c.read('ou=groups', cn_only=True)
     # returns ['ou=groups,'+base_dn], list of string instead of dict
     
     # attribute titles
     res = c.read('ou=groups', attrs_only=True)
     # returns ['objectClass', 'ou'], list of string instead of dict 
     
     # given attributes
     res = c.read('ou=groups', attrs=['objectClass'])
     
     # filter
     res = c.read('ou=groups', filter='cn=user')
     
* create

Creates record in database. First fires event ldap_before_create where parameters (rdn, attrs) can be rewritten.
rdn is automatically joined with base_dn so you don't specify full path. Attributes are transformed to LDIF format using ldap method addModlist. 
Method creates record using ldap method add_s. After that fires event ldap_after_create and returns bool.

  .. code-block:: python
  
     attrs = {'cn': 'test', 'gidNumber': '503', 'objectClass': ['top','posixGroup']}
     cn = 'cn=test,ou=groups'
     res = c.create(cn, attrs)
     
* update

Updates record in database. First fires event ldap_before_update where parameters (rdn, attrs) can be rewritten.
rdn is automatically joined with base_dn so you don't specify full path. Methods reads original record from database and transforms current and new
attributes to LDIF format using ldap method modifyModlist. Methods updates record using ldap method modify_s. 

When new rdn is different (new attributes contain cn or uid) the record identifier is replaced using ldap method modrdn_s.
After that fires event ldap_after_update and returns bool.

  .. code-block:: python
  
     # update record
     attrs = {'cn': 'test', 'gidNumber': '503', 'objectClass': ['top','posixGroup']}
     cn = 'cn=test,ou=groups'
     c.create(cn, attrs)
     res = c.update(cn, {'gidNumber': '504'})  
     
     # replace record
     res = c.update(cn, {'cn': 'test2'}) 
     
* delete

Method deletes record from database. First fires event ldap_before_delete where parameter rdn can be rewritten.
rdn is automatically joined with base_dn so you don't specify full path. Methods delete record using ldap method delete_s.
After that fires event ldap_after_delete and returns bool.

  .. code-block:: python
    
     res = c.delete(cn)