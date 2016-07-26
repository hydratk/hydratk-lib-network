# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.rpc.client.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for RPC client messages
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
    'htk_rpc_init_proxy'        : ["Inicializuji proxy ke vzdálenému objektu na URL: '{0}'"],
    'htk_rpc_proxy_initialized' : ["Proxy inicializována"],
    'htk_rpc_proxy_not_init'    : ["Proxy není inicializována"],
    'htk_rpc_call_method'       : ["Volám vzdálenou metodu: '{0}' s parametry: '{1}'"],
    'htk_rpc_method_called'     : ["Metoda vrátila: '{0}'"]
}