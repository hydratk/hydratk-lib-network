# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.term.client.en.messages
   :platform: Unix
   :synopsis: English language translation for TERMINAL client messages
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
    'htk_term_unknown_protocol'  : ["Unknown protocol: '{0}'"],
    'htk_term_connecting'        : ["Connecting to server: '{0}'"],
    'htk_term_connected'         : ["Connected successfully"],
    'htk_term_disconnected'      : ["Disconnected from server"],
    'htk_term_not_connected'     : ["Not connected to server"],
    'htk_term_executing_command' : ["Executing command: '{0}'"],
    'htk_term_command_executed'  : ["Command executed"]
}
