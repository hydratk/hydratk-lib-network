.. _module_lib_database_pgsql:

PGSQL
=====

This sections contains module documentation of pgsql module.

driver
^^^^^^

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