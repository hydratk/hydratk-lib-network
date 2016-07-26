# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.inet.client.en.messages
   :platform: Unix
   :synopsis: English language translation for INET client messages
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

language = {
  'name' : 'English',
  'ISO-639-1' : 'en'
}

from hydratk.core import const

HIGHLIGHT_START = chr(27)+chr(91)+"1m"
HIGHLIGHT_US    = chr(27)+chr(91)+"4m"
HIGHLIGHT_END   = chr(27)+chr(91)+"0m"

msg = {
    'htk_inet_unknown_method' : ["Unknown method for protocol: '{0}'"],
    'htk_inet_connecting'     : ["Connecting to server: '{0}'"],
    'htk_inet_connected'      : ["Connected successfully"],
    'htk_inet_disconnecting'  : ["Disconnecting from server"],
    'htk_inet_disconnected'   : ["Disconnected from server"],
    'htk_inet_not_connected'  : ["Not connected to server"],
    'htk_inet_sending_data'   : ["Sending data: '{0}'"],
    'htk_inet_data_sent'      : ["Data sent"],
    'htk_inet_receiving_data' : ["Receiving data up to size: '{0}'"],
    'htk_inet_data_received'  : ["Received data: '{0}'"]    
}
