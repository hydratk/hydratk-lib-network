# -*- coding: utf-8 -*-
"""Generic EMAIL client factory

.. module:: network.email.client
   :platform: Unix
   :synopsis: Generic EMAIL client factory
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from importlib import import_module

protocols = {
  'SMTP': 'smtp_client',
  'POP' : 'pop_client',
  'IMAP': 'imap_client'
}

def EmailClient(protocol, *args, **kwargs):
    """Email client factory method
        
    Args:            
        protocol (str): Email protocol, SMTP|POP|IMAP
        args (args): arguments 
        kwargs (kwargs): key value arguments
           
    Returns:
        obj: EmailClient
       
    Raises:
        error: NotImplementedError
                
    """       

    protocol = protocol.upper()        
    if (protocol in protocols):
        mh = MasterHead.get_head()
        mod = import_module('hydratk.lib.network.email.{0}'.format(protocols[protocol]))
        mh.find_module('hydratk.lib.network.email.client', None)                  
        return mod.EmailClient(*args, **kwargs)
    else:
        raise NotImplementedError('Unknown protocol:{0}'.format(protocol))                         