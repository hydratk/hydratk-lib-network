# -*- coding: utf-8 -*-
"""Generic DB client factory

.. module:: network.dbi.client
   :platform: Unix
   :synopsis: Generic DB client factory
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

engines = {
  'SQLITE'    : 'sqlite_client',
  'ORACLE'    : 'oracle_client',
  'MYSQL'     : 'mysql_client',
  'POSTGRESQL': 'postgresql_client',
  'JDBC'      : 'jdbc_client'
}

def DBClient(engine='SQLITE', *args, **kwargs):    
    """DB client factory method
        
    Args:            
        engine (str): DB engine, SQLITE|ORACLE|MYSQL|POSTGRESQL|JDBC
        args (args): arguments 
        kwargs (kwargs): key value arguments
           
    Returns:
        obj: DBClient
       
    Raises:
        error: ValueError
                
    """       

    engine = engine.upper()        
    if (engines.has_key(engine)):
            
        client = None     
        lib_call = 'from hydratk.lib.network.dbi.' + engines[engine] + ' import DBClient; client = DBClient(*args, **kwargs)'                                             
        exec lib_call
                        
        return client

    else:
        raise ValueError('Unknown engine:{0}'.format(engine))
        return None                           