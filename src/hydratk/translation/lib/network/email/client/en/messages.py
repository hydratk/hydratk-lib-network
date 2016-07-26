# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.email.client.en.messages
   :platform: Unix
   :synopsis: English language translation for EMAIL client messages
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
    'htk_email_unknown_protocol' : ["Unknown protocol: '{0}'"],
    'htk_email_unknown_method'   : ["Unknown method for protocol: '{0}'"],
    'htk_email_connecting'       : ["Connecting to server: '{0}'"],
    'htk_email_connected'        : ["Connected successfully"],
    'htk_email_disconnected'     : ["Disconnected from server"],
    'htk_email_not_connected'    : ["Not connected to server"],
    'htk_email_sending'          : ["Sending email: '{0}'"],
    'htk_email_sent'             : ["Email sent"],
    'htk_email_counting'         : ["Counting emails"],
    'htk_email_count'            : ["Email count: '{0}'"],
    'htk_email_listing'          : ["Listing emails"],
    'htk_email_listed'           : ["Emails listed"],
    'htk_email_receiving'        : ["Receiving email: '{0}'"], 
    'htk_email_received'         : ["Email received"]
}
