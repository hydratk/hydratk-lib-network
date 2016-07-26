# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.term.client.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for TERMINAL client messages
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
    'htk_term_unknown_protocol'  : ["Neznámý protokol: '{0}'"],
    'htk_term_connecting'        : ["Připojuji se na server: '{0}'"],
    'htk_term_connected'         : ["Spojení se serverem bylo úspěšné"],
    'htk_term_disconnected'      : ["Spojení se serverem bylo ukončeno"],
    'htk_term_not_connected'     : ["Není navázáno spojení se serverem"],
    'htk_term_executing_command' : ["Vykonávám příkaz: '{0}'"],
    'htk_term_command_executed'  : ["Vykonávání příkazu ukončeno"]
}