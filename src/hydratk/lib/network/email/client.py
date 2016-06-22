# -*- coding: utf-8 -*-
"""Generic EMAIL client factory

.. module:: network.email.client
   :platform: Unix
   :synopsis: Generic EMAIL client factory
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

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
        error: ValueError
                
    """       

    protocol = protocol.upper()        
    if (protocols.has_key(protocol)):
            
        client = None     
        lib_call = 'from hydratk.lib.network.email.' + protocols[protocol] + ' import EmailClient; client = EmailClient(*args, **kwargs)'                                             
        exec lib_call
                        
        return client

    else:
        raise ValueError('Unknown protocol:{0}'.format(protocol))
        return None                           