# -*- coding: utf-8 -*-
"""Generic JMS client factory

.. module:: network.jms.client
   :platform: Unix
   :synopsis: Generic JMS client factory
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

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
        error: ValueError
                
    """       

    protocol = protocol.upper()        
    if (protocols.has_key(protocol)):
            
        client = None     
        lib_call = 'from hydratk.lib.network.jms.' + protocols[protocol] + ' import JMSClient; client = JMSClient(*args, **kwargs)'                                             
        exec lib_call
                        
        return client

    else:
        raise ValueError('Unknown protocol:{0}'.format(protocol))
        return None                           