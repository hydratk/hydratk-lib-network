# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.ldap.client.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for LDAP client messages
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
    'htk_ldap_connecting'    : ["Připojuji se na server: '{0}'"],
    'htk_ldap_connected'     : ["Spojení se serverem bylo úspěšné"],
    'htk_ldap_disconnected'  : ["Spojení se serverem bylo ukončeno"],
    'htk_ldap_not_connected' : ["Není navázáno spojení se serverem"],
    'htk_ldap_reading'       : ["Načítám záznamy: '{0}'"],
    'htk_ldap_read'          : ["Načteno záznamů: '{0}'"],
    'htk_ldap_creating'      : ["Vytvářím záznam RDN:'{0}', attributy:'{1}'"],
    'htk_ldap_created'       : ["Záznam vytvořen"],
    'htk_ldap_updating'      : ["Aktualizuji záznam RDN:'{0}', attributy:'{1}'"],
    'htk_ldap_updated'       : ["Záznam aktualizován"],
    'htk_ldap_deleting'      : ["Mažu záznam RDN:'{0}'"],
    'htk_ldap_deleted'       : ["Záznam smazán"]
}