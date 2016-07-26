# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.email.client.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for EMAIL client messages
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
    'htk_email_unknown_protocol' : ["Neznámý protokol: '{0}'"],
    'htk_email_unknown_method'   : ["Neznámá metoda pro protokol: '{0}'"],
    'htk_email_connecting'       : ["Připojuji se na server: '{0}'"],
    'htk_email_connected'        : ["Spojení se serverem bylo úspěšné"],
    'htk_email_disconnected'     : ["Spojení se serverem bylo ukončeno"],
    'htk_email_not_connected'    : ["Není navázáno spojení se serverem"],
    'htk_email_sending'          : ["Odesílám email: '{0}'"],
    'htk_email_sent'             : ["Email odeslán"],
    'htk_email_counting'         : ["Vypisuji počet emailů"],
    'htk_email_count'            : ["Počet emailů: '{0}'"],
    'htk_email_listing'          : ["Vypisuji seznam emailů"],
    'htk_email_listed'           : ["Emaily vypsány"],
    'htk_email_receiving'        : ["Přijímám email: '{0}'"], 
    'htk_email_received'         : ["Email přijat"]
}