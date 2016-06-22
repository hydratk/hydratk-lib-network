# -*- coding: utf-8 -*-
"""Module for data loading from external resources

.. module:: lib.data.loader
   :platform: Unix
   :synopsis: Module for data loading from external resources
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

def load_from_file(filename, header=0, delimiter=None, sheet=None):
    """Method loads data from file
        
    Args:
        filename (str): filename, supported extensions csv|tsv|xlsx|ods
        header (int): row id with header defining column names, default first row
        delimiter (str): delimiter, supported for csv|tsv formats, default ;|tab
        sheet (str): sheet name, supported for xlsx|ods formats, default first sheet
        
    Returns:
        list: list of records, record is dictionary if header is present, otherwise list
        
    Raises:
        error: ValueError 
                
    """        
    
    from os import path
    if (not path.exists(filename)):
        raise ValueError('File {0} not found'.format(filename))
    
    extension = filename.split('.')[-1]    
    if (extension in ['csv', 'tsv']):
        
        from pyexcel import get_records, get_array   
        
        if (delimiter == None):
            delimiter = ';' if (extension == 'csv') else '\t'
                     
        if (header != None):
            records = get_records(file_name=filename, delimiter=delimiter, name_columns_by_row=header)
        else:
            records = get_array(file_name=filename, delimiter=delimiter)                    

    elif (extension in ['xlsx', 'ods']):
             
        from pyexcel import get_book     
                
        if (extension == 'xlsx'):
            from pyexcel.ext import xlsx
        else:
            from pyexcel.ext import ods3
            
        book = get_book(file_name=filename)
        if (sheet == None):
            sheet = book.sheet_by_index(0)
        else:
            sheet = book.sheet_by_name(sheet)
            
        if (header != None):
            sheet.name_columns_by_row(header)
            records = sheet.to_records()
        else:
            records = sheet.to_array()
        
    else:
        raise ValueError('Unknown extension: {0}'.format(extension))
    
    return records

def load_from_db(engine, query, bindings=None, host=None, port=None, sid=None, user=None, passw=None, db_file=None):
    """Method loads data from database
        
    Args:        
        engine (str): DB engine, SQLITE|ORACLE|MYSQL|POSTGRESQL
        query (str): SQL query
        bindings (list): query bindings 
        host (str): hostname
        port (int): port
        sid (str): db instance
        user (str): username
        passw (str): password
        db_file (str): database file
        
    Returns:
        list: list of records, record is dictionary
        
    Raises:
        error: ValueError 
                
    """   
    
    from hydratk.lib.network.dbi.client import DBClient
    
    db = DBClient(engine)
    
    if (engine.upper() == 'SQLITE'):
        db.connect(db_file)
    else:
        db.connect(host, port, sid, user, passw)
    
    res, records = db.exec_query(query, bindings)
    
    db.disconnect()
    
    return records