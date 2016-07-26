# -*- coding: utf-8 -*-
"""Generic JMS client factory

.. module:: network.jms.client
   :platform: Unix
   :synopsis: Generic JMS client factory
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from importlib import import_module

protocols = {
  'JMS'  : 'jms_client',
  'STOMP': 'stomp_client',
  'AMQP' : 'amqp_client'
}

def JMSClient(protocol='JMS', *args, **kwargs):
    """JMS client factory method
        
    Args:            
        protocol (str): JMS protocol, JMS|STOMP|AMQP
        args (args): arguments 
        kwargs (kwargs): key value arguments
           
    Returns:
        obj: JMSClient
       
    Raises:
        error: NotImplementedError
                
    """       

    protocol = protocol.upper()        
    if (protocol in protocols):
        mh = MasterHead.get_head()
        mod = import_module('hydratk.lib.network.jms.{0}'.format(protocols[protocol]))
        mh.find_module('hydratk.lib.network.jms.client', None)                   
        return mod.JMSClient(*args, **kwargs)
    else:
        raise NotImplementedError('Unknown protocol:{0}'.format(protocol))                          