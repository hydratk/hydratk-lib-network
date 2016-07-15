# -*- coding: utf-8 -*-
"""Generic DB client factory

.. module:: network.dbi.client
   :platform: Unix
   :synopsis: Generic DB client factory
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from importlib import import_module

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
    if (engine in engines):            
        mod = import_module('hydratk.lib.network.dbi.{0}'.format(engines[engine]))                 
        return mod.DBClient(*args, **kwargs)
    else:
        raise ValueError('Unknown engine:{0}'.format(engine))
        return None                           