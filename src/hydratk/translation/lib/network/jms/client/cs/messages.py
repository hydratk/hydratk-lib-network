# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.jms.client.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for JMS client messages
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
    'htk_jms_connecting'          : ["Připojuji se na JMS server s parametry: '{0}'"],
    'htk_jms_connected'           : ["Spojení s JMS serverem bylo úspěšné"],
    'htk_jms_connecting_error'    : ["Nastala chyba při spojení s JMS serverem"],
    'htk_jms_disconnecting'       : ["Ukončuji spojení s JMS serverem"],
    'htk_jms_disconnected'        : ["Spojení s JMS serverem bylo ukončeno"],
    'htk_jms_disconnecting_error' : ["Nastala chyba při ukončování spojení s JMS serverem"],
    'htk_jms_not_connected'       : ["Není navázáno spojení se serverem"],
    'htk_jms_sending_msg'         : ["Odesílám zprávu s parametry: '{0}'"],
    'htk_jms_msg_sent'            : ["Zpráva odeslána"],
    'htk_jms_sending_error'       : ["Nastala chyba při odesílání zprávy"],
    'htk_jms_receiving_msg'       : ["Přijímám zprávy s parametry: '{0}'"],
    'htk_jms_msg_received'        : ["Přijato '{0}' zpráv"],
    'htk_jms_receiving_error'     : ["Nastala chyba při přijímání zpráv"],
    'htk_jms_browsing'            : ["Procházím frontu s parametry: '{0}'"]     
}
