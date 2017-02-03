.. _module_lib_database_dbo:

DBO
===

This sections contains module documentation of dbo module.

mssql
^^^^^

Module driver provides class DBODriver which impletements client MSSQL database using external module 
`pymssql <http://pymssql.org/en/stable/>`_ in version >= 2.1.3.
Unit tests available at hydratk/lib/database/dbo/mssql/01_methods_ut.jedi

**Attributes** :

* _host - server hostname (or IP address)
* _port - port number (default 1433)
* _dbname - database name
* _driver_options - configuration dictionary (timeout, factory, ...)

**Methods** :

* _parse_dsn

Method parse dsn (connection string). Sets _host, _port, _dbname, _username, _password.

  .. code-block:: python
  
     from hydratk.lib.database.dbo.dbo import DBO
     
     dsn = 'pgsql:host=10.0.0.1;port=1433;database=test;user=test;password=test'
     c = DBO(dsn)
     d = c._dbo_driver   
     res = d._parse_dsn(dsn)     

* _apply_driver_options

Method updates driver options.

  .. code-block:: python
  
     opt = {'timeout': 10}
     d._apply_driver_options(opt)

* connect

Method connects to server using pymssql method connect. Parameters are already set by method _parse_dsn.

  .. code-block:: python
  
     dsn = 'pgsql:host=10.0.0.1;port=1433;database=test;user=test;password=test'
     c = DBO(dsn, autoconnect=False)
     d = c._dbo_driver
     d.connect()  

* close

Method disconnects from server using pymssql method close.

* commit

Method commits transaction using pymssql method commit.

* execute

Method executes query using pymssql method execute and returns cursor (results must be extracted i.e. using method fetchall).

  .. code-block:: python
   
     # read query
     res = d.execute('SELECT count(*) FROM customer').fetchall()
     
     # write query 
     d.execute('INSERT INTO lov_status VALUES (4, \'test\')')
     
     # variables binding
     res = d.execute('SELECT * FROM lov_status WHERE id = %s', [4]).fetchall()

* rollback

Method rollbacks transaction using pymssql method rollback.

* __getitem__

Method gets given psycopg2 attribute if exists.

* __getattr__

Method gets given connection or psycopg2 attribute if exists.

* table_exists

Method checks if given table exists in database. It executes special query
SELECT count(*) found FROM information_schema.tables WHERE table_catalog=%s AND table_type='BASE TABLE' and table_name=%s.

  .. code-block:: python
  
     res = d.table_exists('customer')

* result_as_dict

Method enables return of query result in dictionary form.

  .. code-block:: python
  
     # no dictionary
     d.result_as_dict(False)
     recs = d.execute('SELECT * FROM lov_status').fetchall()    
     # access recs[0][1]
     
     # dictionary
     d.result_as_dict(True)
     recs = d.execute('SELECT * FROM lov_status').fetchall()
     # access recs[0]['title']   

mysql
^^^^^

Module driver provides class DBODriver which impletements client MySQL database using external module 
`MySQL-python <https://github.com/farcepest/MySQLdb1>`_ in version >= 1.2.3.
Unit tests available at hydratk/lib/database/dbo/mysql/01_methods_ut.jedi

MySQL-python requires non-Python libraries which are automatically installed by setup script (python-mysqldb, libmysqlclient-dev for apt-get, mysql-devel for yum).
When Python3 is used MySQL-python is replaced by module `mysqlclient <https://github.com/PyMySQL/mysqlclient-python>`_ in version >= 1.3.7 
which provides compatible interface.

**Attributes** :

* _host - server hostname (or IP address)
* _port - port number (default 3306)
* _dbname - database name (default mysql)
* _driver_options - configuration dictionary (timeout, factory, ...)

**Methods** :

* _parse_dsn

Method parse dsn (connection string). Sets _host, _port, _dbname, _username, _password.

  .. code-block:: python
  
     from hydratk.lib.database.dbo.dbo import DBO
     
     dsn = 'pgsql:host=127.0.0.1;port=3306;database=mysql;user=root;password=root'
     c = DBO(dsn)
     d = c._dbo_driver   
     res = d._parse_dsn(dsn)     

* _apply_driver_options

Method updates driver options.

  .. code-block:: python
  
     opt = {'timeout': 10}
     d._apply_driver_options(opt)

* connect

Method connects to server using MySQLdb method connect. Parameters are already set by method _parse_dsn.

  .. code-block:: python
  
     dsn = 'pgsql:host=127.0.0.1;port=3306;database=mysql;user=root;password=root'
     c = DBO(dsn, autoconnect=False)
     d = c._dbo_driver
     d.connect()  

* close

Method disconnects from server using MySQLdb method close.

* commit

Method commits transaction using MySQLdb method commit.

* execute

Method executes query using MySQLdb method execute and returns cursor (results must be extracted i.e. using method fetchall).

  .. code-block:: python
   
     # read query
     res = d.execute('SELECT count(*) FROM customer').fetchall()
     
     # write query 
     d.execute('INSERT INTO lov_status VALUES (4, \'test\')')
     
     # variables binding
     res = d.execute('SELECT * FROM lov_status WHERE id = %s', [4]).fetchall()

* rollback

Method rollbacks transaction using MySQLdb method rollback.

* __getitem__

Method gets given MySQLdb attribute if exists.

* __getattr__

Method gets given connection or MySQLdb attribute if exists.

* table_exists

Method checks if given table exists in database. It executes special query
SELECT count(*) found FROM information_schema.tables WHERE table_schema=%s AND table_type='BASE TABLE' and table_name=%s.

  .. code-block:: python
  
     res = d.table_exists('customer')

* erase_database

Method drops all tables in database. It executes special query
SELECT table_name FROM information_schema.tables WHERE table_schema=%s AND table_type='BASE TABLE' AND engine='InnoDB' to get table names.
Then it drops them using query.

* result_as_dict

Method sets cursor class DictCursor to return query result in dictionary form.

  .. code-block:: python
  
     # no dictionary
     d.result_as_dict(False)
     recs = d.execute('SELECT * FROM lov_status').fetchall()    
     # access recs[0][1]
     
     # dictionary
     d.result_as_dict(True)
     recs = d.execute('SELECT * FROM lov_status').fetchall()
     # access recs[0]['title']      

oracle
^^^^^^

Module driver provides class DBODriver which impletements client MySQL database using external module 
`cx_Oracle <http://cx-oracle.readthedocs.io/en/latest/index.html>`_ in version >= 5.1.3.
Unit tests available at hydratk/lib/database/dbo/oracle/01_methods_ut.jedi

cx_Oracle requires non-Python libraries which are automatically installed by setup script (libaio1, libaio-dev for apt-get, libaio for yum).
When PyPy is used cx_Oracle is replaced by module `cx_oracle_on_ctypes <https://github.com/lameiro/cx_oracle_on_ctypes.git>`_  which
provides compatible interface.
cx_Oracle also requires Oracle client (not bundled with hydratk). Installation script checks system variable $ORACLE_HOME and omits 
cx_Oracle installation if not set.

**Attributes** :

* _host - server hostname (or IP address)
* _port - port number (default 1521)
* _dbname - database name
* _driver_options - configuration dictionary (timeout, factory, auto_commit, ...)

**Methods** :

* _parse_dsn

Method parse dsn (connection string). Sets _host, _port, _dbname, _username, _password.

  .. code-block:: python
  
     from hydratk.lib.database.dbo.dbo import DBO
     
     dsn = 'pgsql:host=127.0.0.1;port=49161;database=xe;user=crm;password=crm'
     c = DBO(dsn)
     d = c._dbo_driver   
     res = d._parse_dsn(dsn)     

* _apply_driver_options

Method updates driver options.

  .. code-block:: python
  
     opt = {'timeout': 10}
     d._apply_driver_options(opt)

* connect

Method connects to server using cx_Oracle method connect. Parameters are already set by method _parse_dsn.

  .. code-block:: python
  
     dsn = 'pgsql:host=127.0.0.1;port=49161;database=xe;user=crm;password=crm'
     c = DBO(dsn, autoconnect=False)
     d = c._dbo_driver
     d.connect()  

* close

Method disconnects from server using cx_Oracle method close.

* commit

Method commits transaction using cx_Oracle method commit.

* execute

Method executes query using cx_Oracle method execute and returns cursor (results must be extracted i.e. using method fetchall).

  .. code-block:: python
   
     # read query
     res = d.execute('SELECT count(*) FROM customer').fetchall()
     
     # write query 
     d.execute('INSERT INTO lov_status VALUES (4, \'test\')')
     
     # variables binding
     res = d.execute('SELECT * FROM lov_status WHERE id = :1', [4]).fetchall()

* rollback

Method rollbacks transaction using cx_Oracle method rollback.

* __getitem__

Method gets given cx_Oracle attribute if exists.

* __getattr__

Method gets given connection or cx_Oracle attribute if exists.

* table_exists

Method checks if given table exists in database. It executes special query
SELECT count(*) found FROM all_tables WHERE owner=:1 AND table_name=:2.

  .. code-block:: python
  
     res = d.table_exists('customer')

* erase_database

Method drops all tables in database. It executes special query
SELECT table_name FROM all_tables WHERE owner=:1 to get table names.
Then it drops them using query.

* result_as_dict

Method sets cursor class DictCursor to return query result in dictionary form.

  .. code-block:: python
  
     # no dictionary
     d.result_as_dict(False)
     recs = d.execute('SELECT * FROM lov_status').fetchall()    
     # access recs[0][1]
     
     # dictionary
     d.result_as_dict(True)
     recs = d.execute('SELECT * FROM lov_status').fetchall()
     # access recs[0]['title']
     
* _make_dict

Auxiliary method, it returns output in dictionary form instead of tuple.
Methods execute, table_exists, erase_database use it to override standard row factory (tuple).      

pgsql
^^^^^

Module driver provides class DBODriver which impletements client PostgreSQL database using external module 
`psycopg2 <http://pythonhosted.org/psycopg2/>`_ in version >= 2.4.5.
Unit tests available at hydratk/lib/database/dbo/pgsql/01_methods_ut.jedi

psycopg2 requires non-Python libraries which are automatically installed by setup script (python-psycopg2, libpq-dev for apt-get, python-psycopg2, postgresql-devel for yum).
When PyPy is used psycopg2 is replaced by module `psycopg2cffi <https://github.com/chtd/psycopg2cffi>`_ in version >= 2.7.4 
which provides compatible interface.

**Attributes** :

* _host - server hostname (or IP address)
* _port - port number (default 5432)
* _dbname - database name (default postgres)
* _driver_options - configuration dictionary (timeout, factory, ...)

**Methods** :

* _parse_dsn

Method parse dsn (connection string). Sets _host, _port, _dbname, _username, _password.

  .. code-block:: python
  
     from hydratk.lib.database.dbo.dbo import DBO
     
     dsn = 'pgsql:host=127.0.0.1;port=5432;database=postgre;user=lynus;password=bowman'
     c = DBO(dsn)
     d = c._dbo_driver   
     res = d._parse_dsn(dsn)     

* _apply_driver_options

Method updates driver options.

  .. code-block:: python
  
     opt = {'timeout': 10}
     d._apply_driver_options(opt)

* connect

Method connects to server using psycopg2 method connect. Parameters are already set by method _parse_dsn.

  .. code-block:: python
  
     dsn = 'pgsql:host=127.0.0.1;port=5432;database=postgre;user=lynus;password=bowman'
     c = DBO(dsn, autoconnect=False)
     d = c._dbo_driver
     d.connect()  

* close

Method disconnects from server using psycopg2 method close.

* commit

Method commits transaction using psycopg2 method commit.

* execute

Method executes query using psycopg2 method execute and returns cursor (results must be extracted i.e. using method fetchall).

  .. code-block:: python
   
     # read query
     res = d.execute('SELECT count(*) FROM customer').fetchall()
     
     # write query 
     d.execute('INSERT INTO lov_status VALUES (4, \'test\')')
     
     # variables binding
     res = d.execute('SELECT * FROM lov_status WHERE id = %s', [4]).fetchall()

* rollback

Method rollbacks transaction using psycopg2 method rollback.

* __getitem__

Method gets given psycopg2 attribute if exists.

* __getattr__

Method gets given connection or psycopg2 attribute if exists.

* table_exists

Method checks if given table exists in database. It executes special query
SELECT count(*) found FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' and table_name=%s.

  .. code-block:: python
  
     res = d.table_exists('customer')

* erase_database

Method drops all tables in database. It executes special query
SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' to get table names.
Then it drops them using query.

* result_as_dict

Method sets factory RealDictCursor to return query result in dictionary form.

  .. code-block:: python
  
     # no dictionary
     d.result_as_dict(False)
     recs = d.execute('SELECT * FROM lov_status').fetchall()    
     # access recs[0][1]
     
     # dictionary
     d.result_as_dict(True)
     recs = d.execute('SELECT * FROM lov_status').fetchall()
     # access recs[0]['title']      