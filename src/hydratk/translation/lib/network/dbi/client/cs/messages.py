# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.dbi.client.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for DB client messages
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
    'htk_dbi_unknown_type'       : ["Neznámý typ procedury: '{0}'"],       
    'htk_dbi_connecting'         : ["Připojuji se na server: '{0}'"],
    'htk_dbi_connected'          : ["Spojení se serverem bylo úspěšné"],
    'htk_dbi_connecting_error'   : ["Nastala chyba při spojení se serverem"],
    'htk_dbi_disconnecting'      : ["Ukončuji spojení se serverem"],    
    'htk_dbi_disconnected'       : ["Spojení se serverem bylo ukončeno"],
    'htk_dbi_disconnecting_error': ["Nastala chyba při ukončování spojení se serverem"],
    'htk_dbi_not_connected'      : ["Není navázáno spojení se serverem"],    
    'htk_dbi_executing_query'    : ["Vykonávám dotaz: '{0}'"],
    'htk_dbi_query_executed'     : ["Vykonávání dotazu ukončeno"],
    'htk_dbi_query_error'        : ["Nastala chyba při vykonávání dotazu"],    
    'htk_dbi_calling_proc'       : ["Volám proceduru: '{0}'"],
    'htk_dbi_proc_called'        : ["Volání procedury ukončeno: '{0}'"] 
}