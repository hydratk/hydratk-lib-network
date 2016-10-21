.. _module_lib_data_loader:

Loader
======

This sections contains module documentation of loader module.

loader
^^^^^^

Module loader provides methods for loading data from external sources.
Unit tests available at hydratk/lib/data/loader/01_methods_ut.jedi

**Methods** :

* load_from_file

Method loads data from text file (formats: csv,tsv,xlsx,ods)using external modules `pyexcel <https://github.com/pyexcel/pyexcel>`_ in version >= 0.2.0,
`pyexcel-xlsx <https://github.com/pyexcel/pyexcel-xlsx>`_ in version >= 0.1.0, 
`pyexcel-ods3 <https://github.com/pyexcel/pyexcel-ods3>`_ in version >= 0.1.1. 

For csv, tsv format you can use parameters: header (index of header row, default 0), delimiter (default ; for csv, tab for tsv).
Method reads data using pyexcel methods get_records (header provided) or get_array
For xlsx, ods formats you can use parameters: header (index of header row, default 0), sheet (name of sheet, default 1st sheet).
Method reads data using pyexcel methods get_book and to_records (header provided) or to_array.

Method returns data as list of list (header not provided) or list of dictionary (keys named from header).

  .. code-block:: python
  
     # csv file 
     path = '/var/local/hydratk/yoda/helpers/yodahelpers/hydratk/lib/data/data.csv'
     res = load_from_file(path, header=None)
     # returns ['col1', 'col2', 'col3', 'a', 'b', 'c', 1, 2, 3]
     
     # tsv file
     path = '/var/local/hydratk/yoda/helpers/yodahelpers/hydratk/lib/data/data.tsv'
     res = load_from_file(path, header=None)  
     # returns ['col1', 'col2', 'col3', 'a', 'b', 'c', 1, 2, 3]
     
     # file with header
     path = '/var/local/hydratk/yoda/helpers/yodahelpers/hydratk/lib/data/data.csv'
     res = load_from_file(path, header=0) 
     # returns [{'col1':'a', 'col2':'b', 'col3':'c'}, {'col1':1, 'col2':2, 'col3':3}]
     
     # delimiter
     res = load_from_file(path, delimiter=';') 
     
  .. code-block:: python
  
     # xlsx file
     path = '/var/local/hydratk/yoda/helpers/yodahelpers/hydratk/lib/data/data.xlsx'
     res = load_from_file(path, header=None)
     # returns ['col1', 'col2', 'col3', 'a', 'b', 'c', 1, 2, 3]
     
     # ods file
     path = '/var/local/hydratk/yoda/helpers/yodahelpers/hydratk/lib/data/data.ods'
     res = load_from_file(path, header=None)
     # returns ['col1', 'col2', 'col3', 'a', 'b', 'c', 1, 2, 3]
     
     # file with header
     path = '/var/local/hydratk/yoda/helpers/yodahelpers/hydratk/lib/data/data.xlsx'
     res = load_from_file(path, header=0)
     # returns [{'col1':'a', 'col2':'b', 'col3':'c'}, {'col1':1, 'col2':2, 'col3':3}]
     
     # sheet
     res = load_from_file(path, sheet='test')                              

* load_from_db

Methods loads data from database using module dbi.
Supports two engine types, file (engine SQLITE) and server (engines ORACLE, MYSQL, POSTGRESQL, MSSQL).
Connect to file database using parameter db_file, connect to server database using parameters (host, port, sid, user, passw).

Method initializes DBClient, calls method exec_query (specified via parameters query, bindings). Returns query output as
list of dictionaries. Module dbi implements also engines JDBC and NoSQL which are not supported by this method.

  .. code-block:: python
  
     # file database
     path = '/var/local/hydratk/testenv/testenv.db3'
     query = 'SELECT * FROM lov_status'
     res = load_from_db('SQLITE', query, db_file=path) 
     
     # server database
     host, port, sid, user, passw = '127.0.0.1', 3306, 'mysql', 'root', 'root'
     query, bindings = 'SELECT title FROM lov_status WHERE id = ?', [2]
     res = load_from_db('MYSQL', query, bindings, host=host, port=port, sid=sid, user=user, passw=passw)      