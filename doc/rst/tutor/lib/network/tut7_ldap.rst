.. _tutor_network_tut7_ldap:

Tutorial 7: LDAP
================

This sections shows several examples how to use JMS client.

API
^^^

Module hydratk.lib.network.LDAP

Methods:

* connect: connect to LDAP server
* disconnect: disconnect from LDAP server
* read: read records
* create: create record
* update: update record
* delete: delete record

  .. note::
   
     API uses HydraTK core functionalities so it must be running.

Examples
^^^^^^^^

  .. code-block:: python
  
     # import library
     from hydratk.lib.network.ldap.client import LDAPClient
     
     # initialize client
     client = LDAPClient()
     
     # connect to server
     # returns bool
     client.connect(host='localhost', base_dn='dc=test,dc=com', user='admin', passw='bowman')  
     
     # read records from organization unit, base DN dc=test,dc=com is reused 
     # returns list of records
     print client.read('ou=users')
     
     # [{'objectClass': ['organizationalUnit', 'top'], 'ou': 'users', 'CN': 'ou=users,dc=test,dc=com'}, 
     #  {'objectClass': ['inetOrgPerson', 'top'], 'cn': ' Bowman', 'CN': 'cn=Bowman,ou=users,dc=test,dc=com', 'sn': 'Bowman'}, 
     #  {'cn': 'Vince Neil', 'mobile': '603603603', 'l': 'Prague', 'objectClass': ['inetOrgPerson', 'top'], 
     #   'sn': 'Neil', 'mail': 'aaa@xxx.com', 'givenName': 'Vince', 'CN': 'cn=Vince Neil,ou=users,dc=test,dc=com'}, 
     # ]   
     
     # read concrete record
     print client.read('ou=users', filter='cn=Bowman')  
     
     # [{'objectClass': ['inetOrgPerson', 'top'], 'cn': ' Bowman', 'CN': 'cn=Bowman,ou=users,dc=test,dc=com', 'sn': 'Bowman'}]
     
     # create record
     # returns bool
     attrs = {'cn':'Calder', 'sn':'Calder', 'givenName':'Mike', 'objectClass':['top','inetOrgPerson']}
     client.create('cn=Calder,ou=users', attrs)
     
     # update record, including CN
     # returns bool
     attrs = {'sn':'Page', 'givenName':'Jimmy', 'cn':'Page'}
     client.update('cn=Calder,ou=users', attrs)     
     
     # delete record, already with new CN
     # returns bool
     client.delete('cn=Page,ou=users')
     
     # disconnect from database
     # returns bool
     client.disconnect()     