# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.ldap.client.en.messages
   :platform: Unix
   :synopsis: English language translation for LDAP client messages
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
    'htk_ldap_connecting'    : ["Connecting to server: '{0}'"],
    'htk_ldap_connected'     : ["Connected successfully"],
    'htk_ldap_disconnected'  : ["Disconnected from server"],
    'htk_ldap_not_connected' : ["Not connected to server"],
    'htk_ldap_reading'       : ["Reading records: '{0}'"],
    'htk_ldap_read'          : ["Records read: '{0}'"],
    'htk_ldap_creating'      : ["Creating record RDN:'{0}', attributes:'{1}'"],
    'htk_ldap_created'       : ["Record created"],
    'htk_ldap_updating'      : ["Updating record RDN:'{0}', attributes:'{1}'"],
    'htk_ldap_updated'       : ["Record updated"],
    'htk_ldap_deleting'      : ["Deleting record RDN:'{0}'"],
    'htk_ldap_deleted'       : ["Record deleted"]
}
