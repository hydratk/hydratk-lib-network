.. _tutor_network_tut1_dbi:

Tutorial 1: Database
====================

This sections shows several examples how to use database client.

API
^^^

Module hydratk.lib.network.dbi.client.

Method DBClient is factory method which requires attribute engine to create 
proper DBClient object instance. Additional attributes are passed as args, kwargs. 

Supported engines:

* SQLite - module sqlite_client
* Oracle - module oracle_client
* MySQL - module mysql_client
* PostgreSQL - module postgresql_client
* JDBC - module jdbc_client
* MSSQL - module mssql_client
* Redis - module nosql.redis_client
* MongoDB - module nosql.mongodb_client
* Cassandra - module nosql.cassandra_client

Methods for relational db:

* connect: connect to database file (SQLite) or database server (Oracle, MySQL, PostgreSQL, JDBC)  
* disconnect: disconnect from database
* exec_query: execute query, prepared statements with variable bindings are supported (use ? character)
* call_proc: call procedure (has no return param) or function (has return param), supported for Oracle, MySQL, PostgreSQL/MSSQL (procedure only)
* commit: commit transaction
* rollback: rollback transaction
* close: stop JVM, supported for JDBC

  .. note::
   
     API uses HydraTK core functionalities so it must be running.

SQLite
^^^^^^

  .. code-block:: python
  
     # import library
     from hydratk.lib.network.dbi.client import DBClient
     
     # initialize client
     client = DBClient('sqlite')
     
     # connect to database
     # returns bool
     client.connect(db_file='/home/lynus/hydratk/testenv.db3')
     
     # select records from table
     # returns bool, list of rows
     res, rows = client.exec_query('SELECT * FROM LOV_STATUS')
     
     for row in rows:
         print row 
     
     # insert record to table
     client.exec_query('INSERT INTO LOV_STATUS (id, title) VALUES (4, \'pokus\')')
     
     # delete record from table
     client.exec_query('DELETE FROM LOV_STATUS WHERE id = 4;')
     
     # insert record using prepared statement with variable binding
     client.exec_query('INSERT INTO LOV_STATUS (id, title) VALUES (?, ?)', [4, 'pokus 2'])
     
     # delete record using prepared statement with variable binding
     client.exec_query('DELETE FROM LOV_STATUS WHERE id = ?', [4])
     res, rows = client.exec_query('SELECT title FROM LOV_STATUS')
     
     # disconnect from database
     # returns bool
     client.disconnect()
     
Oracle
^^^^^^

Oracle client is not bundled with HydraTK and must be installed individually.

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.dbi.client as db
    
     # initialize client
     client = db.DBClient('oracle')  
     
     # connect to database
     client.connect(host='localhost', port=49161, sid='XE', user='crm', passw='crm')   
     
     # select records from table
     # returns bool, list of rows
     res, rows = client.exec_query('SELECT * FROM CUSTOMER')
     
     for row in rows:
         print row      
     
     # call function
     param_names = ['id', 'name', 'status', 'segment', 'birth_no', 'reg_no', 'tax_no', 'err']
     input_values = {'name': 'Charlie Bowman', 'status': 'active', 'segment': 2,
                     'birth_no': '840809/0009', 'reg_no': '12345', 'tax_no': 'CZ12345'}
     output_types = {'id': 'int', 'err': 'string'}
     result_type = 'int'
     
     # returns result, output param values dictionary
     res, params = client.call_proc('crm.customer_pck.f_create', param_names, input_values, output_types, 'func', result_type)
                      
     # call procedure
     param_names = ['id', 'name', 'status', 'segment', 'birth_no', 'reg_no', 'tax_no', 'err']
     input_values = {'id': id}
     output_types = {'name': 'string', 'status': 'string', 'segment': 'int',
                     'birth_no': 'string', 'reg_no': 'string', 'tax_no': 'string', 'err': 'string'}
                     
     # returns output param values dictionary                     
     params = client.call_proc('crm.customer_pck.p_read', param_names, input_values, output_types, 'proc')
     
     # disconnect from database
     # returns bool
     client.disconnect() 
     
JDBC
^^^^

Part of JDBC client library is implemented in Java as a wrapper application which uses Java JDBC API.
Python client library uses Java bridge to create Java object instance. 
Specific Java libraries are needed to access database via JDBC, they are not bundled with hydratk.
 
After installation do following actions:
1. Check that directory /var/local/hydratk/java was created and contains files: DBClient.java, DBClient.class.
2. Store specific client jar file to same directory (i.e. ojdbc6.jar).

  .. note ::
  
     JDBC is not supported for PyPy due to module JPype1.

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.dbi.client as db
    
     # initialize client
     client = db.DBClient('jdbc', True)  
     
     # connect to database
     client.connect(driver='oracle.jdbc.driver.OracleDriver', conn_str='jdbc:oracle:thin:@localhost:49161/XE', user='crm', passw='crm')   
     
     # select records from table
     # returns bool, list of rows
     res, rows = client.exec_query('SELECT * FROM LOV_STATUS')
     
     for row in rows:
         print row 
     
     # insert record to table
     client.exec_query('INSERT INTO LOV_STATUS (id, title) VALUES (4, \'pokus\')')
                     
     # returns output param values dictionary                     
     params = client.call_proc('crm.customer_pck.p_read', param_names, input_values, output_types, 'proc')
     
     # disconnect from database
     # returns bool
     client.disconnect() 
     
     # stop JVM
     client.stop()
     
MySQL
^^^^^

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.dbi.client as db
    
     # initialize client
     client = db.DBClient('mysql')  
     
     # connect to database
     client.connect(host='localhost', port=3306, sid='mysql', user='root', passw='root')   
       
     # select records from table
     # returns bool, list of rows
     res, rows = client.exec_query('SELECT * FROM CUSTOMER')
     
     for row in rows:
         print row         
            
     # call procedure
     param_names = ['id', 'name', 'status', 'segment', 'birth_no', 'reg_no', 'tax_no', 'err']
     input_values = {'id': id}
     output_types = {'name': 'string', 'status': 'string', 'segment': 'int',
                     'birth_no': 'string', 'reg_no': 'string', 'tax_no': 'string', 'err': 'string'}
                     
     # returns output param values dictionary                     
     params = client.call_proc('read_customer', param_names, input_values, output_types, 'proc')
     
     # disconnect from database
     # returns bool
     client.disconnect() 

PostgreSQL
^^^^^^^^^^   

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.dbi.client as db
    
     # initialize client
     client = db.DBClient('postgresql')  
     
     # connect to database
     client.connect(host='localhost', port=5432, sid='postgre', user='root', passw='root')   
          
     # select records from table
     # returns bool, list of rows
     res, rows = client.exec_query('SELECT * FROM CUSTOMER')
     
     for row in rows:
         print row            
            
     # call procedure
     param_names = ['id', 'name', 'status', 'segment', 'birth_no', 'reg_no', 'tax_no', 'err']
     input_values = {'id': id}
     output_types = {'name': 'string', 'status': 'string', 'segment': 'int',
                     'birth_no': 'string', 'reg_no': 'string', 'tax_no': 'string', 'err': 'string'}
                     
     # returns output param values dictionary                     
     params = client.call_proc('read_customer', param_names, input_values, output_types)
     
     # disconnect from database
     # returns bool
     client.disconnect()  
     
MSSQL
^^^^^ 

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.dbi.client as db
    
     # initialize client
     client = db.DBClient('mssql')  
     
     # connect to database
     client.connect(host='10.0.0.1', port=1433, sid='test', user='root', passw='root')   
          
     # select records from table
     # returns bool, list of rows
     res, rows = client.exec_query('SELECT * FROM CUSTOMER')
     
     for row in rows:
         print row            
            
     # call procedure
     param_names = ['id', 'name', 'status', 'segment', 'birth_no', 'reg_no', 'tax_no', 'err']
     input_values = {'id': id}
     output_types = {'name': 'string', 'status': 'string', 'segment': 'int',
                     'birth_no': 'string', 'reg_no': 'string', 'tax_no': 'string', 'err': 'string'}
                     
     # returns output param values dictionary                     
     params = client.call_proc('read_customer', param_names, input_values, output_types)
     
     # disconnect from database
     # returns bool
     client.disconnect()  
     
Redis
^^^^^

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.dbi.client as db
     
     # initialize client
     client = db.DBClient('redis')
     
     # connect to database
     client.connect(host='127.0.0.1', port=6379, db=0)
     
     # set key, returns bool
     res = client.set(key, value)
     
     # get key, returns str
     res = client.get(key, value)
     
     # check if key exists, returns bool
     res = client.exists(key)
     
     # delete key, returns bool
     res = client.delete(key)
     
     # execute command
     # returns bool, output
     res, output = client.exec_command('INCR key')    
     
MongoDB
^^^^^^^

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.dbi.client as db
     
     # initialize client
     client = db.DBClient('mongodb')         
     
     # connect to database
     client.connect(host='127.0.0.1', port=27017, db='test')   
     
     # insert record to database
     # returns bool, id
     doc = {"customer": {"name": "Charlie Bowman", "status": "active", "segment": 2,
                         "payer": {"name": "Charlie Bowman", "status": "active"},
                         "services": [{"id": 615, "status": "active"}, {"id": 619, "status": "suspend"}]}}
     res, id = client.exec_command('insert', collection='test', document=doc)
     
     # find record
     # returns bool, rows
     res, rows = client.exec_command('find', collection='test', filter={'_id': id})
     
     # find records using complex filter
     filter = {"$or": [{"customer.name": "Charlie Bowman"}, {"customer.name": "Vince Neil"}]}
     res, rows = client.exec_command('find', collection='test', filter=filter)
     
     # aggregate records
     # returns bool, rows
     filter = [{"$match": {"customer.payer.status": "active"}},
               {"$group": {"_id": "$customer.name", "count": {"$sum": 1}}}]
     res, rows = c.exec_command('aggregate', 'test', filter=filter)     
     
     # update multiple records
     # returns bool, modified count
     doc, filter = {"$set": {"customer.name": "Vince Neil 2"}}, {"customer.name": "Vince Neil"}
     res, count = client.exec_command('update', 'test', document=doc, filter=filter, single=False)
     
     # replace record
     # returns bool, modified count
     doc, filter = {"customer": {"name": "Vince Neil"}}, {"customer.name": "Vince Neil 2"}
     res, count = client.exec_command('replace', 'test', doc, filter)
     
     # delete record
     # returns bool, deleted count
     res, count = client.exec_command('delete', 'test', filter={"customer.name": "Vince Neil"})
     
     # drop collection
     # returns bool, None
     res, out = client.exec_command('drop', collection='test')
     
     # disconnect from database
     # returns bool
     client.disconnect()        
     
Cassandra
^^^^^^^^^

  .. code-block:: python
  
     # import library
     from hydratk.lib.network.dbi.client import DBClient
     
     # initialize client
     client = DBClient('cassandra')
     
     # connect to database
     # returns bool
     client.connect(host='127.0.0.1', port=9042, key_space='test')
     
     # select records from table
     # returns bool, list of rows
     res, rows = client.exec_query('SELECT * FROM LOV_STATUS')
     
     for row in rows:
         print row 
     
     # insert record to table
     client.exec_query('INSERT INTO LOV_STATUS (id, title) VALUES (4, \'pokus\')')
     
     # delete record from table
     client.exec_query('DELETE FROM LOV_STATUS WHERE id = 4;')
     
     # insert record using prepared statement with variable binding
     client.exec_query('INSERT INTO LOV_STATUS (id, title) VALUES (?, ?)', [4, 'pokus 2'])
     
     # delete record using prepared statement with variable binding
     client.exec_query('DELETE FROM LOV_STATUS WHERE id = ?', [4])
     res, rows = client.exec_query('SELECT title FROM LOV_STATUS')
     
     # disconnect from database
     # returns bool
     client.disconnect()     