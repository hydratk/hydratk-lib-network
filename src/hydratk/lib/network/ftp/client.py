# -*- coding: utf-8 -*-
"""Generic FTP client factory

.. module:: network.ftp.client
   :platform: Unix
   :synopsis: Generic FTP client factory
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from importlib import import_module

protocols = {
  'FTP' : 'ftp_client',
  'SFTP': 'sftp_client',
  'TFTP': 'tftp_client'
}

def FTPClient(protocol='FTP', *args, **kwargs):
    """FTP client factory method
        
    Args:            
        protocol (str): FTP protocol, FTP|SFTP|TFTP
        args (args): arguments
        kwargs (kwargs): key value arguments 
           
    Returns:
        obj: FTPClient
       
    Raises:
        error: NotImplementedError
                
    """       

    protocol = protocol.upper()        
    if (protocol in protocols):
        mh = MasterHead.get_head()
        mod = import_module('hydratk.lib.network.ftp.{0}'.format(protocols[protocol]))
        mh.find_module('hydratk.lib.network.ftp.client', None)                  
        return mod.FTPClient(*args, **kwargs)
    else:
        raise NotImplementedError('Unknown protocol:{0}'.format(protocol))                         