# -*- coding: utf-8 -*-
"""Generic RPC client factory

.. module:: network.rpc.client
   :platform: Unix
   :synopsis: Generic RPC client factory
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from importlib import import_module

providers = {
  'RMI': 'rmi_client'
}

def RPCClient(provider, *args):
    """RPC client factory method
        
    Args:            
        provider (str): RPC provider, RMI
        args (args): arguments 
        kwargs (kwargs): key value arguments
           
    Returns:
        obj: RPCClient
       
    Raises:
        error: NotImplementedError
                
    """       

    provider = provider.upper()        
    if (provider in providers):
        mh = MasterHead.get_head()
        mod = import_module('hydratk.lib.network.rpc.{0}'.format(providers[provider]))
        mh.find_module('hydratk.lib.network.rpc.client', None)                  
        return mod.RPCClient(*args)
    else:
        raise NotImplementedError('Unknown provider:{0}'.format(provider))                     