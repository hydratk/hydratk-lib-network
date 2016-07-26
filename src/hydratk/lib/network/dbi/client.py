# -*- coding: utf-8 -*-
"""Generic DB client factory

.. module:: network.dbi.client
   :platform: Unix
   :synopsis: Generic DB client factory
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
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
        error: NotImplementedError
                
    """       

    engine = engine.upper()        
    if (engine in engines):            
        mh = MasterHead.get_head()        
        mod = import_module('hydratk.lib.network.dbi.{0}'.format(engines[engine]))
        mh.find_module('hydratk.lib.network.dbi.client', None)                 
        return mod.DBClient(*args, **kwargs)
    else:
        raise NotImplementedError('Unknown engine:{0}'.format(engine))                       