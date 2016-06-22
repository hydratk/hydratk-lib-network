# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.rest.client.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for REST client messages
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
    'htk_rest_request'  : ["Posílám požadavek na server: '{0}', uživatel:'{1}', heslo:'{2}', metoda:'{3}', " + \
                          "hlavičky:'{4}', tělo:'{5}', parametry:'{6}'"],
    'htk_rest_response' : ["Obdržena odpověď ze serveru: hlavička: {0}, tělo: {1}"] 
}
