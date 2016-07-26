# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.rpc.client.en.messages
   :platform: Unix
   :synopsis: English language translation for RPC client messages
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
    'htk_rpc_init_proxy'        : ["Initializing proxy remote object on URL: '{0}'"],
    'htk_rpc_proxy_initialized' : ["Proxy initialized"],
    'htk_rpc_proxy_not_init'    : ["Proxy not initialized yet"],
    'htk_rpc_call_method'       : ["Calling remote method: '{0}' with parameters: '{1}'"],
    'htk_rpc_method_called'     : ["Method returned: '{0}'"]
}
