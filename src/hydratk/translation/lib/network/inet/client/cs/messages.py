# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.inet.client.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for INET client messages
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

language = {
  'name' : 'Čeština',
  'ISO-639-1' : 'cs'
}

from hydratk.core import const

HIGHLIGHT_START = chr(27)+chr(91)+"1m"
HIGHLIGHT_US    = chr(27)+chr(91)+"4m"
HIGHLIGHT_END   = chr(27)+chr(91)+"0m"

msg = {    
    'htk_inet_unknown_method' : ["Neznámá metoda pro protokol: '{0}'"],
    'htk_inet_connecting'     : ["Připojuji se na server: '{0}'"],
    'htk_inet_connected'      : ["Spojení se serverem bylo úspěšné"],
    'htk_inet_disconnecting'  : ["Ukončuji spojení se serverem"],    
    'htk_inet_disconnected'   : ["Spojení se serverem bylo ukončeno"],
    'htk_inet_not_connected'  : ["Není navázáno spojení se serverem"], 
    'htk_inet_sending_data'   : ["Odesílám data: '{0}'"],
    'htk_inet_data_sent'      : ["Data odeslána"],
    'htk_inet_receiving_data' : ["Přijímám data do velikosti: '{0}'"],
    'htk_inet_data_received'  : ["Přijata data: '{0}'"]           
}