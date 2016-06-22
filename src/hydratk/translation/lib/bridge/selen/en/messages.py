# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.bridge.selen.en.messages
   :platform: Unix
   :synopsis: English language translation for Selenium bridge messages
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
    'htk_selen_opening'          : ["Opening browser on page with URL: '{0}'"],
    'htk_selen_opened'           : ["Page opened"],
    'htk_selen_closed'           : ["Browser closed"],
    'htk_selen_waiting'          : ["Waiting for element presence: '{0}', timeout: '{1}'"],
    'htk_selen_wait_finished'    : ["Waiting interval finished"],
    'htk_selen_get'              : ["Getting element: '{0}', method: '{1}', single: '{2}'"],
    'htk_selen_read'             : ["Reading element with params: '{0}'"],
    'htk_selen_set'              : ["Setting element with params: '{0}'"],
    'htk_selen_executing_script' : ["Executing script: {0}"],
    'htk_selen_script_executed'  : ["Script executed"],
    'htk_selen_saving_screen'    : ["Saving screenshot to '{0}'"],
    'htk_selen_screen_saved'     : ["Screenshot saved"]
}
