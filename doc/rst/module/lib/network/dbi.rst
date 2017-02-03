.. _module_lib_network_dbi:

DBI
===

This sections contains module documentation of dbi module.

client
^^^^^^

Module client provides common way to initialize database client of any supported engine.
It implements factory design pattern, each client provides class DBClient.
Unit tests available at hydratk/lib/network/dbi/client/01_methods_ut.jedi

Following **engines** are supported:

* SQLite - module sqlite_client
* Oracle - module oracle_client
* MySQL - module mysql_client
* PostgreSQL - module postgresql_client
* JDBC - module jdbc_client
* MSSQL - module mssql_client
* Redis - module nosql.redis_client
* MongoDB - module nosql.mongodb_client
* Cassandra - module nosql.cassandra_client

**Methods** :

* DBClient 

Creates DBClient instance of given engine (use engine name, case is ignored).
Any constructor parameters can be passed as args, kwargs (currently supported for JDBC only).
When engine is not supported NotImplementedError is raised.

  .. code-block:: python
  
     from hydratk.lib.network.dbi.client import DBClient
     
     c1 = DBClient('SQLITE')
     c2 = DBClient('JDBC', verbose=True, jvm_path='path/to/jvm')
     
sqlite_client
^^^^^^^^^^^^^

Module provides class DBClient which implements client for SQLite database using Python module 
`sqlite3 <https://docs.python.org/3.6/library/sqlite3.html>`_.
Unit tests available at hydratk/lib/network/dbi/sqlite_client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - sqlite3 client instance
* _db_file - str, SQLite database filename including path
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* client - returns _client
* db_file - returns _db_file
* is_connected - returns _is_connected

**Methods** :

* __init__

Constructor called by DBClient method, sets MasterHead reference.

* connect

Connects to database (specified via parameter db_file).
First fires event dbi_before_connect where parameters can be rewritten. Sets _client to sqlite3 client instance (using method sqlite3.connect).
After successful connection fires event dbi_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.dbi.client import DBClient
     
     c = DBClient('SQLITE')
     res = c.connect(db_file='/var/local/hydratk/testenv/testenv.db3')     

* disconnect

Disconnects from database using sqlite3 method close and returns bool.

  .. code-block:: python
  
     res = c.disconnect()
      
* exec_query

Executes SQL query. First fires event dbi_before_exec_query where parameters (query, bindings, fetch_one, autocommit) can be rewritten.
Creates sqlite3 cursor and executes query (using sqlite3 method execute). Query string supports variables binding (character ? in query).

Internal query result (read query) is returned using sqlite3 method fetchall by default (or using fetchone when parameter fetch_one=True).
When write query is executed the output is None of course. Write query is commited by default (use parameter autocommit=False to avoid it).

After that method fires event dbi_after_exec_query and returns bool, output as list of dictionaries (one dict per each row, keys are column names).
Technically dictionary is not standard Python dict but sqlite3.Row object (you can access columns as in standard dict).

  .. code-block:: python
  
     query = 'SELECT a.id, a.name, a.reg_no FROM customer a , payer b WHERE a.id = b.customer'
     
     # select single row, automatically returns first list item
     res, rows = c.exec_query(query, fetch_one=True)
     print (rows['id'], rows['name'], rows['reg_no']) 
     
     # select multiple rows
     res, rows = c.exec_query(query)
     print (rows[0]['id'], rows[0]['name'], rows[0]['reg_no']) 
     
     # query with variable binding
     query = 'SELECT id, name, reg_no FROM customer WHERE id = ? AND name = ?'
     res, rows = c.exec_query(query, [2, 'Charlie Bowman'])       
     
     # write query
     query = 'INSERT INTO customer (name, status, segment) VALUES (?, ?, ?)'
     bindings = ['test test', 3, 2]
     res, rows = c.exec_query(query, bindings)         

* commit

Commits transaction using sqlite3 method commit and returns bool.
Method exec_query uses autocommit by default, so this method should be used only when autocommit is disabled.

  .. code-block:: python
  
     c.exec_query('INSERT INTO customer (name, status, segment) VALUES (?, ?, ?)', ['test test', 1, 2], autocommit=False)
     res = c.commit()

* rollback

Rollbacks transaction using sqlite3 method rollback and returns bool.
Method exec_query uses autocommit by default, so this method should be used only when autocommit is disabled.

  .. code-block:: python
  
     c.exec_query('INSERT INTO customer (name, status, segment) VALUES (?, ?, ?)', ['test test', 1, 2], autocommit=False)
     res = c.rollback()  
     
oracle_client
^^^^^^^^^^^^^

Module provides class DBClient which implements client for Oracle database using external module 
`cx_Oracle <http://cx-oracle.readthedocs.io/en/latest/index.html>`_ in version >= 5.1.3.
Unit tests available at hydratk/lib/network/dbi/oracle_client/01_methods_ut.jedi

cx_Oracle requires non-Python libraries which are automatically installed by setup script (libaio1, libaio-dev for apt-get, libaio for yum).
When PyPy is used cx_Oracle is replaced by module `cx_oracle_on_ctypes <https://github.com/lameiro/cx_oracle_on_ctypes.git>`_  which
provides compatible interface.
cx_Oracle also requires Oracle client (not bundled with hydratk). Installation script checks system variable $ORACLE_HOME and omits 
cx_Oracle installation if not set.

**Attributes** :

* _mh - MasterHead reference
* _client - cx_Oracle client instance
* _host - database server hostname (or IP address)
* _port - database port (default 1521)
* _sid - database SID
* _user - username
* _passw - password
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* client - returns _client
* host - returns _host
* port - returns _client
* sid - returns _sid
* user - returns _user
* passw - returns _passw
* is_connected - returns _is_connected

**Methods** :

See sqlite_client for more examples (the interface is common).

* __init__ 

Constructor called by DBClient method, sets MasterHead reference.

* connect

Connects to database (specified via parameters host, port, sid, user, passw).
First fires event dbi_before_connect where parameters can be rewritten. Sets _client to cx_Oracle client instance (using method cx_Oracle.connect).
After successful connection fires event dbi_after_connect and returns bool. Connection timeout is handled by cx_Oracle itself and can't be specified.

  .. code-block:: python
  
     from hydratk.lib.network.dbi.client import DBClient
     
     c = DBClient('ORACLE')
     res = c.connect(host='127.0.0.1', port=49161, sid='xe', user='crm', passw='crm')     

* disconnect

Disconnects from database using cx_Oracle method close and returns bool. 
      
* exec_query

Executes SQL query. First fires event dbi_before_exec_query where parameters (query, bindings, fetch_one, autocommit) can be rewritten.
Creates cx_Oracle cursor and executes query (using cx_Oracle method execute). Query string supports variables binding (character ? in query).
Binding is internally changed to Oracle format (:1, :2, ..., ? character is common for all engines).

Internal query result (read query) is transformed to dictionary output.
When write query is executed the output is None of course. Write query is commited by default (use parameter autocommit=False to avoid it).
After that method fires event dbi_after_exec_query and returns bool, output as list of dictionaries (one dict per each row, keys are column names).      

* call_proc

Call stored procedure or function written in PL/SQL. First fires event dbi_before_call_proc where parameters (p_name, param_names, i_values, o_types, 
type, ret_type, autocommit) can be rewritten. Creates cx_Oracle cursor.

param_names is list of procedure parameter names (it is recommended to use real names but it is up to you, cx_Oracle uses parameter positioning instead of names). 
i_values is dictionary of input parameter values passed to procedure (key - param name, value - param value).
o_types is dictionary of output parameters types returned by procedure. Method supports types: int, float, string, timestamp, clob, blob which 
are translated to cx_Oracle types NUMBER, NUMBER, STRING, TIMESTAMP, CLOB, BLOB. type is proc|procedure or func|function to call procedure 
or function, proc is used by default. ret_type is function output type (similar to o_types).

Method passes input values and output types to cx_Oracle method callproc or callfunc. The output is transformed to dictionary form.
Oracle ref_cursor is also transformed to dictionary. Method commits transaction by default (use parameter autocommit=False to avoid it).
It fires event dbi_after_call_proc and returns output type (for function) and dictionary.

  .. code-block:: python
  
     # read function f_read in package customer_pck
     param_names = ['id', 'name', 'status', 'segment', 'birth_no', 'reg_no', 'tax_no', 'err']      
     input_values = {'id': 5}
     output_types = {'name': 'string', 'status': 'string', 'segment': 'int',
                     'birth_no': 'string', 'reg_no': 'string', 'tax_no': 'string', 'err': 'string'}                
     ret, res = c.call_proc('customer_pck.f_read', param_names, input_values, output_types, 'func', 'int')        
     # returns {'name': 'Charlie Bowman', 'status': 'suspend', 'segment': 2, 'birth_no': '700101/0001', 'reg_no': '1234', 'tax_no': 'CZ1234', 'err': None}
     
     # write function f_create
     param_names = ['id', 'name', 'status', 'segment', 'birth_no', 'reg_no', 'tax_no', 'err'] 
     input_values = {'name': name, 'status': status, 'segment': segment, 'birth_no': birth_no, 
                     'reg_no': reg_no, 'tax_no': tax_no}
     output_types = {'id': 'int', 'err': 'string'}                
     ret, res = c.call_proc('customer_pck.f_create', param_names, input_values, output_types, 'func', 'int')      
     # returns {'id': 6, 'err': None}

* commit

Commits transaction using cx_Oracle method commit and returns bool.
Methods exec_query, call_proc use autocommit by default, so this method should be used only when autocommit is disabled.

* rollback

Rollbacks transaction using cx_Oracle method rollback and returns bool.
Methods exec_query, call_proc use autocommit by default, so this method should be used only when autocommit is disabled.

mysql_client
^^^^^^^^^^^^

Module provides class DBClient which implements client for MySQL database using external module 
`MySQL-python <https://github.com/farcepest/MySQLdb1>`_ in version >= 1.2.3.
Unit tests available at hydratk/lib/network/dbi/mysql_client/01_methods_ut.jedi

MySQL-python requires non-Python libraries which are automatically installed by setup script (python-mysqldb, libmysqlclient-dev for apt-get, mysql-devel for yum).
When Python3 is used MySQL-python is replaced by module `mysqlclient <https://github.com/PyMySQL/mysqlclient-python>`_ in version >= 1.3.7 
which provides compatible interface.

**Attributes** :

* _mh - MasterHead reference
* _client - MySQLdb client instance
* _host - database server hostname (or IP address)
* _port - database port (default 3306)
* _sid - database SID (to be common with oracle_client)
* _user - username
* _passw - password
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* client - returns _client
* host - returns _host
* port - returns _client
* sid - returns _sid
* user - returns _user
* passw - returns _passw
* is_connected - returns _is_connected

**Methods** :

See sqlite_client for more examples (the interface is common).

* __init__

Constructor called by DBClient method, sets MasterHead reference.

* connect

Connects to database (specified via parameters host, port, sid, user, passw).
First fires event dbi_before_connect where parameters can be rewritten. Sets _client to MySQLdb client instance (using method MySQLdb.connect).
After successful connection fires event dbi_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.dbi.client import DBClient
     
     c = DBClient('MYSQL')
     res = c.connect(host='127.0.0.1', port=3306, sid='mysql', user='root', passw='root')     

* disconnect

Disconnects from database using MySQLdb method close and returns bool. 
      
* exec_query

Executes SQL query. First fires event dbi_before_exec_query where parameters (query, bindings, fetch_one, autocommit) can be rewritten.
Creates MySQLdb cursor and executes query (using MySQLdb method execute). Query string supports variables binding (character ? in query).
Binding is internally changed to MySQL format (%s, ? character is common for all engines).

Internal query result (read query) is transformed to dictionary output.
When write query is executed the output is None of course. Write query is commited by default (use parameter autocommit=False to avoid it).
After that method fires event dbi_after_exec_query and returns bool, output as list of dictionaries (one dict per each row, keys are column names).      

* call_proc

Call stored procedure or function written in MySQL. First fires event dbi_before_call_proc where parameters (p_name, param_names, i_values, o_types, 
type, ret_type, autocommit) can be rewritten. Creates MySQLdb cursor.

param_names is list of procedure parameter names (it is recommended to use real names but it is up to you, MySQLdb uses parameter positioning instead of names). 
i_values is dictionary of input parameter values passed to procedure (key - param name, value - param value).
o_types is dictionary of output parameters types returned by procedure. Method supports types: int, string. type is proc|procedure or func|function to call procedure 
or function, proc is used by default. ret_type is function output type (similar to o_types).

Method passes input values and output types to MySQLdb method callproc or callfunc. The output is read using special query SELECT @_{p_name}_{0}, @_{p_name}_{1}
Method commits transaction by default (use parameter autocommit=False to avoid it).
It fires event dbi_after_call_proc and returns output type (for function) and dictionary.

  .. code-block:: python
  
     # read function read_customer
     param_names = ['id', 'name', 'status', 'segment', 'birth_no', 'reg_no', 'tax_no', 'err']      
     input_values = {'id': 5}
     output_types = {'name': 'string', 'status': 'int', 'segment': 'int',
                     'birth_no': 'string', 'reg_no': 'string', 'tax_no': 'string', 'err': 'string'}                
     res = c.call_proc('read_customer', param_names, input_values, output_types, 'proc')  
     # returns {'name': 'Charlie Bowman', 'status': 'suspend', 'segment': 2, 'birth_no': '700101/0001', 'reg_no': '1234', 'tax_no': 'CZ1234', 'err': None}
     
     # write function create_customer
     param_names = ['id', 'name', 'status', 'segment', 'birth_no', 'reg_no', 'tax_no', 'err'] 
     id, name, status, segment, birth_no, reg_no, tax_no = 66, 'test test', 3, 2, '700101/0001', '1234', 'CZ1234'     
     input_values = {'id': id, 'name': name, 'status': status, 'segment': segment, 'birth_no': birth_no, 
                     'reg_no': reg_no, 'tax_no': tax_no}
     output_types = {'err': 'string'}                
     res = c.call_proc('create_customer', param_names, input_values, output_types, 'proc')        
     # returns {'id': 6, 'err': None}

* commit

Commits transaction using MySQLdb method commit and returns bool.
Methods exec_query, call_proc use autocommit by default, so this method should be used only when autocommit is disabled.

* rollback

Rollbacks transaction using MySQLdb method rollback and returns bool.
Methods exec_query, call_proc use autocommit by default, so this method should be used only when autocommit is disabled.

postgresql_client
^^^^^^^^^^^^^^^^^

Module provides class DBClient which implements client for PostgreSQL database using external module 
`psycopg2 <http://pythonhosted.org/psycopg2/>`_ in version >= 2.4.5.
Unit tests available at hydratk/lib/network/dbi/postgresql_client/01_methods_ut.jedi

psycopg2 requires non-Python libraries which are automatically installed by setup script (python-psycopg2, libpq-dev for apt-get, python-psycopg2, postgresql-devel for yum).
When PyPy is used psycopg2 is replaced by module `psycopg2cffi <https://github.com/chtd/psycopg2cffi>`_ in version >= 2.7.4 
which provides compatible interface.

**Attributes** :

* _mh - MasterHead reference
* _client - psycopg2 client instance
* _host - database server hostname (or IP address)
* _port - database port (default 5432)
* _sid - database SID (to be common with oracle_client)
* _user - username
* _passw - password
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* client - returns _client
* host - returns _host
* port - returns _client
* sid - returns _sid
* user - returns _user
* passw - returns _passw
* is_connected - returns _is_connected

**Methods** :

See sqlite_client for more examples (the interface is common).

* __init__

Constructor called by DBClient method, sets MasterHead reference.

* connect

Connects to database (specified via parameters host, port, sid, user, passw).
First fires event dbi_before_connect where parameters can be rewritten. Sets _client to psycopg2 client instance (using method psycopg2.connect).
After successful connection fires event dbi_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.dbi.client import DBClient
     
     c = DBClient('POSTGRESQL')
     res = c.connect(host='127.0.0.1', port=5432, sid='postgre', user='lynus', passw='bowman')     

* disconnect

Disconnects from database using psycopg2 method close and returns bool. 
      
* exec_query

Executes SQL query. First fires event dbi_before_exec_query where parameters (query, bindings, fetch_one, autocommit) can be rewritten.
Creates psycopg2 cursor and executes query (using psycopg2 method execute). Query string supports variables binding (character ? in query).
Binding is internally changed to PostgreSQL format (%s, ? character is common for all engines).

Internal query result (read query) is transformed to dictionary output.
When write query is executed the output is None of course. Write query is commited by default (use parameter autocommit=False to avoid it).
After that method fires event dbi_after_exec_query and returns bool, output as list of dictionaries (one dict per each row, keys are column names).      

* call_proc

Call stored procedure written in PL/pgSQL. First fires event dbi_before_call_proc where parameters (p_name, param_names, i_values, o_types, autocommit) can be rewritten. 
Creates psycopg2 cursor.

param_names is list of procedure parameter names (it is recommended to use real names but it is up to you, psycopg2 uses parameter positioning instead of names). 
i_values is dictionary of input parameter values passed to procedure (key - param name, value - param value).
o_types is dictionary of output parameters types returned by procedure. Method supports types: int, string. 

Method passes input values and output types to psycopg2 method callproc. The output is read using method fetchone.
Method commits transaction by default (use parameter autocommit=False to avoid it).
It fires event dbi_after_call_proc and returns dictionary.

  .. code-block:: python
  
     # read function read_customer
     param_names = ['id', 'name', 'status', 'segment', 'birth_no', 'reg_no', 'tax_no', 'err']      
     input_values = {'id': 5}
     output_types = {'name': 'string', 'status': 'int', 'segment': 'int',
                     'birth_no': 'string', 'reg_no': 'string', 'tax_no': 'string', 'err': 'string'}                
     res = c.call_proc('read_customer', param_names, input_values, output_types, 'proc')  
     # returns {'name': 'Charlie Bowman', 'status': 'suspend', 'segment': 2, 'birth_no': '700101/0001', 'reg_no': '1234', 'tax_no': 'CZ1234', 'err': None}
     
     # write function create_customer
     param_names = ['id', 'name', 'status', 'segment', 'birth_no', 'reg_no', 'tax_no', 'err'] 
     id, name, status, segment, birth_no, reg_no, tax_no = 66, 'test test', 3, 2, '700101/0001', '1234', 'CZ1234'     
     input_values = {'id': id, 'name': name, 'status': status, 'segment': segment, 'birth_no': birth_no, 
                     'reg_no': reg_no, 'tax_no': tax_no}
     output_types = {'err': 'string'}                
     res = c.call_proc('create_customer', param_names, input_values, output_types, 'proc')        
     # returns {'id': 6, 'err': None}

* commit

Commits transaction using psycopg2 method commit and returns bool.
Methods exec_query, call_proc use autocommit by default, so this method should be used only when autocommit is disabled.

* rollback

Rollbacks transaction using psycopg2 method rollback and returns bool.
Methods exec_query, call_proc use autocommit by default, so this method should be used only when autocommit is disabled.

jdbc_client
^^^^^^^^^^^

Module provides class DBClient which implements client for JDBC using Java bridge.
Unit tests available at hydratk/lib/network/dbi/jdbc_client/01_methods_ut.jedi
It requires JDBC driver for used database stored in /var/local/hydratk/java, drivers are not bundled with hydratk.

When PyPy is used method DBClient raises NotImplementedError. External module JPype1 is not compatible without any alternative.

**Attributes** :

* _mh - MasterHead reference
* _bridge - Java bridge instance
* _client - DBClient Java class instance
* _verbose - verbose mode, disabled by default
* _driver - JDBC driver class name
* _conn_str - connection string with database specific format 
* _user - username
* _passw - password
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* bridge - returns _bridge
* client - returns _client
* verbose - returns _verbose
* driver - returns _driver
* conn_str - returns _conn_str
* user - returns _user
* passw - returns _passw
* is_connected - returns _is_connected

**Methods** :

See sqlite_client for more examples (the interface is common).

* __init__ 

Constructor called by DBClient method. Provides parameters verbose, jvm_path, classpath, options.
See Java bridge documentation for more details, usually the parameters mustn't be provided, they are determined from default configuration.
Initializes Java bridge, starts JVM and initializes DBClient object (DBClient.class in /var/local/hydratk)
Parameter verbose enables debug messages in DBClient class (source code in java/DBClient.java).

* close

Stops JVM.

* connect

Connects to database (specified via parameters driver, conn_str, user, passw).
First fires event dbi_before_connect where parameters can be rewritten. Calls Java method connect.
After successful connection fires event dbi_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.dbi.client import DBClient
     
     c = DBClient('JDBC')
     # ojdbc6.jar is stored in /val/local/hydratk/java, it is automatically added to classpath
     driver, conn_str, user, passw = 'oracle.jdbc.driver.OracleDriver', 'jdbc:oracle:thin:@127.0.0.1:49161/XE', 'crm', 'crm'        
     res = c.connect(driver, conn_str, user, passw)   
     
Method DBClient.connect loads JDBC driver class, sets timeout, connect to database (java.sql.DriverManager.getConnection), disables autocommit and returns bool.

* disconnect

Disconnects from database using Java method disconnect and returns bool.
Method DBClient.disconnect closes database connection and returns bool. 
      
* exec_query

Executes SQL query. First fires event dbi_before_exec_query where parameters (query, bindings, fetch_one, autocommit) can be rewritten.
Eexecutes query (using Java method exec_query). Query string supports variables binding (character ? in query).
Binding is internally transformed to Java ArrayList structure.

Internal query result (read query) is transformed to dictionary output.
When write query is executed the output is None of course. Write query is commited by default (use parameter autocommit=False to avoid it).
After that method fires event dbi_after_exec_query and returns bool, output as list of dictionaries (one dict per each row, keys are column names).      

Method DBClient.exec_query transforms query and bindings to prepared statement and call executeQuery. Stores output of ResultSetMetaData
and returns ArrayList.

* commit

Commits transaction using Java method commit and returns bool.
Methods exec_query, call_proc use autocommit by default, so this method should be used only when autocommit is disabled.
Method DBClient.commit commits transaction and returns bool.

* rollback

Rollbacks transaction using Java method rollback and returns bool.
Methods exec_query, call_proc use autocommit by default, so this method should be used only when autocommit is disabled.
Method DBClient.rollback rollbacks transaction and returns bool.

mssql_client
^^^^^^^^^^^^

Module provides class DBClient which implements client for MSSQL database using external module 
`pymssql <http://pymssql.org/en/stable/>`_ in version >= 2.1.3.
Unit tests available at hydratk/lib/network/dbi/mssql_client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - pymssql client instance
* _host - database server hostname (or IP address)
* _port - database port (default 1433)
* _sid - database SID (to be common with oracle_client)
* _user - username
* _passw - password
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* client - returns _client
* host - returns _host
* port - returns _client
* sid - returns _sid
* user - returns _user
* passw - returns _passw
* is_connected - returns _is_connected

**Methods** :

See sqlite_client for more examples (the interface is common).

* __init__

Constructor called by DBClient method, sets MasterHead reference.

* connect

Connects to database (specified via parameters host, port, sid, user, passw).
First fires event dbi_before_connect where parameters can be rewritten. Sets _client to pymssql client instance (using method pymssql.connect).
After successful connection fires event dbi_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.dbi.client import DBClient
     
     c = DBClient('POSTGRESQL')
     res = c.connect(host='10.0.0.1', port=1433, sid='test', user='test', passw='test')     

* disconnect

Disconnects from database using pymssql method close and returns bool. 
      
* exec_query

Executes SQL query. First fires event dbi_before_exec_query where parameters (query, bindings, fetch_one, autocommit) can be rewritten.
Creates psycopg2 cursor and executes query (using pymssql method execute). Query string supports variables binding (character ? in query).
Binding is internally changed to MSSQL format (%s, ? character is common for all engines).

Internal query result (read query) is transformed to dictionary output.
When write query is executed the output is None of course. Write query is commited by default (use parameter autocommit=False to avoid it).
After that method fires event dbi_after_exec_query and returns bool, output as list of dictionaries (one dict per each row, keys are column names).      

* call_proc

Call stored procedure written in T-SQL. First fires event dbi_before_call_proc where parameters (p_name, param_names, i_values, o_types, autocommit) can be rewritten. 
Creates psycopg2 cursor.

param_names is list of procedure parameter names (it is recommended to use real names but it is up to you, pymssql uses parameter positioning instead of names). 
i_values is dictionary of input parameter values passed to procedure (key - param name, value - param value).
o_types is dictionary of output parameters types returned by procedure. Method supports types: int, string. 

Method passes input values and output types to pymssql method callproc. Method commits transaction by default (use parameter autocommit=False to avoid it).
It fires event dbi_after_call_proc and returns dictionary.

  .. code-block:: python
  
     # read function read_customer
     param_names = ['id', 'name', 'status', 'segment', 'birth_no', 'reg_no', 'tax_no', 'err']      
     input_values = {'id': id}
     output_types = {'name': 'string', 'status': 'int', 'segment': 'int',
                     'birth_no': 'string', 'reg_no': 'string', 'tax_no': 'string', 'err': 'string'}                
     res = c.call_proc('read_customer', param_names, input_values, output_types) 
     # returns {'name': 'Charlie Bowman', 'status': 'suspend', 'segment': 2, 'birth_no': '700101/0001', 'reg_no': '1234', 'tax_no': 'CZ1234', 'err': None}
     
     # write function create_customer
     param_names = ['id', 'name', 'status', 'segment', 'birth_no', 'reg_no', 'tax_no', 'err'] 
     id, name, status, segment, birth_no, reg_no, tax_no = 66, 'test test', 3, 2, '700101/0001', '1234', 'CZ1234'     
     input_values = {'id': id, 'name': name, 'status': status, 'segment': segment, 'birth_no': birth_no, 
                     'reg_no': reg_no, 'tax_no': tax_no}
     output_types = {'err': 'string'}                
     res = c.call_proc('create_customer', param_names, input_values, output_types, 'proc')        
     # returns {'id': 6, 'err': None}

* commit

Commits transaction using pymssql method commit and returns bool.
Methods exec_query, call_proc use autocommit by default, so this method should be used only when autocommit is disabled.

* rollback

Rollbacks transaction using pymssql method rollback and returns bool.
Methods exec_query, call_proc use autocommit by default, so this method should be used only when autocommit is disabled.     

nosql.redis_client
^^^^^^^^^^^^^^^^^^

Module provides class DBClient which implements client for Redis NoSQL database using external module 
`redis <https://github.com/andymccurdy/redis-py>`_ in version >= 2.10.5.
Unit tests available at hydratk/lib/network/dbi/nosql/redis_client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - redis client instance
* _host - database server hostname (or IP address)
* _port - database port (default 6379)
* _db - database id (default 0)
* _passw - password (typically not required)
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* client - returns _client
* host - returns _host
* port - returns _client
* db - returns _db
* passw - returns _passw
* is_connected - returns _is_connected

**Methods** :

* __init__

Constructor called by DBClient method, sets MasterHead reference.

* connect

Connects to database (specified via parameters host, port, db, passw).
First fires event dbi_before_connect where parameters can be rewritten. Sets _client to redis client instance (using constructor redis.StrictRedis).
Checks availability using PING command After successful connection fires event dbi_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.dbi.client import DBClient
     
     c = DBClient('REDIS')
     res = c.connect(host='127.0.0.1', port=6379, db=0)     
      
* exec_command

Executes REDIS command via redis method execute_command. First fires event dbi_before_exec_command where parameter command can be rewritten.
Command output is not None only for read commands. After that method fires event dbi_after_exec_query and returns bool, command output.  
See REDIS documentation for command reference.    

  .. code-block:: python
    
     # set key
     key, val = 'test_key', 'test_val'
     cmd = 'SET {0} {1}'.format(key, val)
     res, out = c.exec_command(cmd)  
     
     # get key
     cmd = 'GET {0}'.format(key)
     res, out = c.exec_command(cmd)  # out = test_val 
     
     # check if key exists
     cmd = 'EXISTS {0}'.format(key)
     res, out = c.exec_command(cmd)     
     
     # delete key
     cmd = 'DEL {0}'.format(key)
     res, out = c.exec_command(cmd)           
     
* get

Simplified GET command, calls exec_command and returns output.

* set

Simplified SET command, calls exec_command and returns bool.

* exists

Simplified EXISTS command, calls exec_command and returns bool.

* delete

Simplified DEL command, call exec_command and returns bool.

nosql.mongodb_client
^^^^^^^^^^^^^^^^^^^^

Module provides class DBClient which implements client for MongoDB NoSQL database using external module 
`pymongo <https://api.mongodb.com/python/current/>`_ in version >= 3.3.0.
Unit tests available at hydratk/lib/network/dbi/nosql/mongodb_client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - redis client instance
* _host - database server hostname (or IP address)
* _port - database port (default 27017)
* _db - database id
* _user - username
* _passw - password (typically not required)
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.
* _db_obj - auxiliary database object reference (it has no getter)

**Properties (Getters)** :

* client - returns _client
* host - returns _host
* port - returns _client
* db - returns _db
* user - returns _user
* passw - returns _passw
* is_connected - returns _is_connected

**Methods** :

* __init__

Constructor called by DBClient method, sets MasterHead reference.

* connect

Connects to database (specified via parameters host, port, db, user, passw).
First fires event dbi_before_connect where parameters can be rewritten. Sets _client to redis client instance (using constructor pymongo.MongoClient).
Checks availability using PING command. After successful connection fires event dbi_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.dbi.client import DBClient
     
     c = DBClient('MONGODB')
     res = c.connect(host='127.0.0.1', port=27017, db='test') 
     
* disconnect

Disconnects from database using pymongo method close and returns bool.
      
* exec_command

Executes MONGODB command. First fires event dbi_before_exec_command where parameter (command, collection, document, filter, single) can be rewritten.
Available commands are insert|find|aggregate|update|replace|delete|drop. Each command leads to specific pymongo method (insert_one, insert_many,
find, aggregate, update_one, update_many, replace_one, delete_one, delete_many, drop).

Read commands find, aggregate have expected output. Write commands insert, update, replace, delete return insert_id, update_count, modified_count, delete_count.
Output of drop command is None. Filter must fulfill MongoDB syntax. After that method fires event dbi_after_exec_query and returns bool, command in dict form. 

  .. code-block:: python

     # insert document
     collection = 'test'
     doc = {"customer": {"name": "Charlie Bowman", "status": "active", "segment": 2,
                         "payer": {"name": "Charlie Bowman", "status": "active"},
                         "services": [{"id": 615, "status": "active"}, {"id": 619, "status": "suspend"}]}}
     res, id = c.exec_command('insert', collection, doc)   
     
     # insert multiple documents
     doc = [{"customer": {"_id": "1", "name": "Charlie Bowman"}},
            {"customer": {"_id": "2", "name": "Vince Neil", "payer": {"status": "active"}}}]      
     res, id = c.exec_command('insert', collection, doc, single=False)  
     
     # find one document
     val = "Vince Neil"
     filter = {"customer.name": val, "customer.payer.status": "active"}
     res, rows = c.exec_command('find', collection, filter=filter)    
     
     # find multiple documents
     filter = {"$or": [{"customer.name": "Charlie Bowman"}, {"customer.name": "Vince Neil"}]}
     res, rows = c.exec_command('find', collection, filter=filter)  
     
     # aggregate documents
     filter = [{"$group": {"_id": "$customer.name", "count": {"$sum": 1}}}]
     res, rows = c.exec_command('aggregate', collection, filter=filter)              

     # aggregate documents with match
     filter = [{"$match": {"customer.payer.status": "active"}},
               {"$group": {"_id": "$customer.name", "count": {"$sum": 1}}}]
     res, rows = c.exec_command('aggregate', collection, filter=filter)     

     # update document
     doc, filter = {"$set": {"customer.name": "Vince Neil 2"}}, {"customer.name": "Vince Neil"}
     res, count = c.exec_command('update', collection, doc, filter) 
     
     # replace document
     doc, filter = {"customer": {"name": "Vince Neil"}}, {"customer.name": "Vince Neil 2"}
     res, count = c.exec_command('replace', collection, doc, filter)
     
     # delete document
     filter = {"customer.name": "Vince Neil"}
     res, count = c.exec_command('delete', collection, filter=filter) 
     
     # drop collection
     res, out = c.exec_command('drop', collection)             

nosql.cassandra_client
^^^^^^^^^^^^^^^^^^^^^^

Module provides class DBClient which implements client for Cassandra NoSQL database using external module 
`cassandra-driver <https://datastax.github.io/python-driver/>`_ in version >= 3.7.0.
Unit tests available at hydratk/lib/network/dbi/nosql/cassandra_client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - redis client instance
* _host - database server hostname (or IP address)
* _port - database port (default 9042)
* _key_space - database key space
* _user - username
* _passw - password
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.
* _session - auxiliary session object reference (it has no getter)

**Properties (Getters)** :

* client - returns _client
* host - returns _host
* port - returns _client
* key_space - returns _key_space
* user - returns _user
* passw - returns _passw
* is_connected - returns _is_connected

**Methods** :

* __init__

Constructor called by DBClient method, sets MasterHead reference.

* connect

Connects to database (specified via parameters host, port, key_space, user, passw).
First fires event dbi_before_connect where parameters can be rewritten. Sets _client to cassandra client instance (using constructor cassandra.Cluster).
Checks availability using USE command. After successful connection fires event dbi_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.dbi.client import DBClient
     
     c = DBClient('CASSANDRA')
     res = c.connect(host='127.0.0.1', port=9042, db='test') 
     
* disconnect

Disconnects from database using cassandra method shutdown and returns bool.

* exec_query

Executes CASSANDRA query. First fires event dbi_before_exec_query where parameters (query, bindings, fetch_one) can be rewritten.
Executes query (using cassandra method execute). Query string supports variables binding (character ? in query).
Binding is internally changed to CASSANDRA format (%s, ? character is common for all engines). 

Filtering is automatically allowed. CASSANDRA doesn't support queries with joined tables (just one table).
After that method fires event dbi_after_exec_query and returns bool, output as list of objects (one object per each row, accessible via row.column).

  .. code-block:: python

     # select single row, automatically returns first list item
     query = 'SELECT * FROM customer WHERE id = 1'
     res, rows = c.exec_query(query, fetch_one=True) 
     print(rows.id, rows.name, rows.reg_no)
     
     # select multiple rows
     query = 'SELECT * FROM customer'
     res, rows = c.exec_query(query, fetch_one=False) 
     print(rows[1].id, rows[1].name, rows[1].reg_no)
     
     # query with variable binding
     query = 'SELECT id, name, reg_no FROM customer WHERE id = ? AND name = ?'
     res, rows = c.exec_query(query, [2, 'Charlie Bowman'])      
     
     # write query
     query = 'INSERT INTO customer (id, name, status, segment) VALUES (?, ?, ?, ?)'
     bindings = [66, 'test test', 3, 2]
     res, rows = c.exec_query(query, bindings)