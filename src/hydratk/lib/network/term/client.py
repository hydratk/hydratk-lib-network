# -*- coding: utf-8 -*-
"""Generic TERM client factory

.. module:: network.term.client
   :platform: Unix
   :synopsis: Generic TERM client factory
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from importlib import import_module

protocols = {
  'SSH': 'ssh_client'
}

def TermClient(protocol='SSH', *args, **kwargs):
    """TERM client factory method
        
    Args:            
        provider (str): TERM protocol, SSH
        args (args): arguments
        kwargs (kwargs): key value arguments 
           
    Returns:
        obj: TermClient
       
    Raises:
        error: ValueError
                
    """       

    protocol = protocol.upper()        
    if (protocol in protocols):
        mod = import_module('hydratk.lib.network.term.{0}'.format(protocols[protocol]))                 
        return mod.TermClient(*args, **kwargs)
    else:
        raise ValueError('Unknown protocol:{0}'.format(protocol))
        return None                           