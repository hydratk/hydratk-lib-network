# -*- coding: utf-8 -*-
"""Generic TERM client factory

.. module:: network.term.client
   :platform: Unix
   :synopsis: Generic TERM client factory
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

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
    if (protocols.has_key(protocol)):
            
        client = None     
        lib_call = 'from hydratk.lib.network.term.' + protocols[protocol] + ' import TermClient; client = TermClient(*args, **kwargs)'                                             
        exec lib_call
                        
        return client

    else:
        raise ValueError('Unknown protocol:{0}'.format(protocol))
        return None                           