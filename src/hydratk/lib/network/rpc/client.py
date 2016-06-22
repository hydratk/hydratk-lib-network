# -*- coding: utf-8 -*-
"""Generic RPC client factory

.. module:: network.rpc.client
   :platform: Unix
   :synopsis: Generic RPC client factory
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

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
    if (providers.has_key(provider)):
            
        client = None     
        lib_call = 'from hydratk.lib.network.rpc.' + providers[provider] + ' import RPCClient; client = RPCClient(*args, **kwargs)'                                             
        exec lib_call
                        
        return client

    else:
        raise ValueError('Unknown provider:{0}'.format(provider))
        return None                           