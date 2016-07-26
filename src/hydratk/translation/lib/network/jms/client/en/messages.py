# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.jms.client.en.messages
   :platform: Unix
   :synopsis: English language translation for JMS client messages
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
    'htk_jms_connecting'          : ["Connecting to JMS server with params: '{0}'"],
    'htk_jms_connected'           : ["Connected to JMS server"],
    'htk_jms_connecting_error'    : ["Error occured during connecting to JMS server"],
    'htk_jms_disconnecting'       : ["Disconnecting from JMS server"],
    'htk_jms_disconnected'        : ["Disconnected from JMS server"],
    'htk_jms_disconnecting_error' : ["Error occured during disconnecting from JMS server"],
    'htk_jms_not_connected'       : ["Not connected to server"],
    'htk_jms_sending_msg'         : ["Sending message with params: '{0}'"],
    'htk_jms_msg_sent'            : ["Message sent"],
    'htk_jms_sending_error'       : ["Error occured during message sending"],
    'htk_jms_receiving_msg'       : ["Receiving messages with params: '{0}'"],
    'htk_jms_msg_received'        : ["Received '{0}' messages"],
    'htk_jms_receiving_error'     : ["Error occured during message receiving"],
    'htk_jms_browsing'            : ["Browsing queue with params: '{0}'"] 
}
