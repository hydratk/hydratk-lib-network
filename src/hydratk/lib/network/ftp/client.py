# -*- coding: utf-8 -*-
"""Generic FTP client factory

.. module:: network.ftp.client
   :platform: Unix
   :synopsis: Generic FTP client factory
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

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
        error: ValueError
                
    """       

    protocol = protocol.upper()        
    if (protocols.has_key(protocol)):
            
        client = None     
        lib_call = 'from hydratk.lib.network.ftp.' + protocols[protocol] + ' import FTPClient; client = FTPClient(*args, **kwargs)'                                             
        exec lib_call
                        
        return client

    else:
        raise ValueError('Unknown protocol:{0}'.format(protocol))
        return None                           