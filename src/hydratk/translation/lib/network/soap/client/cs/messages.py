# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.soap.client.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for SOAP client messages
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
    'htk_soap_loading_wsdl'    : ["Nahrávám WSDL umístěné na: '{0}', uživatel: '{1}', heslo: '{2}', " + \
                                  "endpoint: '{3}', hlavičky: '{4}'"],
    'htk_soap_wsdl_loaded'     : ["WSDL nahráno"],
    'htk_soap_wsdl_not_loaded' : ["WSDL ještě nebly nahráno"],
    'htk_soap_request'         : ["Posílám požadavek na server, operace: '{0}', tělo:'{1}', hlavičky:'{2}'"],
    'htk_soap_response'        : ["Obdržena odpověď ze serveru: '{0}'"] 
}
