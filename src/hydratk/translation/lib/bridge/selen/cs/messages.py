# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.bridge.selen.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for Selenium bridge messages
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
    'htk_selen_opening'          : ["Otevírám prohlížeč na stránce s URL: '{0}'"],
    'htk_selen_opened'           : ["Stránka otevřena"],
    'htk_selen_closed'           : ["Prohlížeč uzavřen"],
    'htk_selen_waiting'          : ["Čekám na přítomnost elementu: '{0}', timeout: '{1}'"],
    'htk_selen_wait_finished'    : ["Čekací interval skončil"],
    'htk_selen_get'              : ["Hledám element: '{0}', method: '{1}', single: '{2}'"],
    'htk_selen_read'             : ["Čtu element s parametry: '{0}'"],
    'htk_selen_set'              : ["Nastavuji element s parametry: '{0}'"],
    'htk_selen_executing_script' : ["Spouštím skript: {0}"],
    'htk_selen_script_executed'  : ["Skript spuštěn"],    
    'htk_selen_saving_screen'    : ["Ukládám obrázek do '{0}'"],
    'htk_selen_screen_saved'     : ["Obrázek uložen"]
}
