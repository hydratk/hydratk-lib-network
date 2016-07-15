# -*- coding: utf-8 -*-
"""Generic RPC client factory

.. module:: network.rpc.client
   :platform: Unix
   :synopsis: Generic RPC client factory
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

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
        error: ValueError
                
    """       

    provider = provider.upper()        
    if (provider in providers):
        mod = import_module('hydratk.lib.network.rpc.{0}'.format(providers[provider]))                
        return mod.RPCClient(*args)
    else:
        raise ValueError('Unknown provider:{0}'.format(provider))
        return None                           