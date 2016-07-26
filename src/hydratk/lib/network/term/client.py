# -*- coding: utf-8 -*-
"""Generic TERM client factory

.. module:: network.term.client
   :platform: Unix
   :synopsis: Generic TERM client factory
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
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
        error: NotImplementedError
                
    """       

    protocol = protocol.upper()        
    if (protocol in protocols):
        mh = MasterHead.get_head()
        mod = import_module('hydratk.lib.network.term.{0}'.format(protocols[protocol]))
        mh.find_module('hydratk.lib.network.term.client', None)                   
        return mod.TermClient(*args, **kwargs)
    else:
        raise NotImplementedError('Unknown protocol:{0}'.format(protocol))             