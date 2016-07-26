# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.inet.client.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for INET packet messages
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
    'htk_inet_sending_packet'      : ["Odesílám packet, iface: '{0}'"],   
    'htk_inet_packet_sent'         : ["Packet odeslán"], 
    'htk_inet_sending_recv_packet' : ["Odesílám a příjímám packety, iface: '{0}', retry: '{1}', timeout: '{2}'"],   
    'htk_inet_packet_sent_recv'    : ["Packety odeslány a přijaty"],
    'htk_inet_ping'                : ["Ping destination: '{0}', protocol: '{1}', port: '{2}'"],
    'htk_inet_ping_ok'             : ["Ping byl úspěšný"],
    'htk_inet_ping_nok'            : ["Ping byl neúspěšný"],
    'htk_inet_traceroute'          : ["Traceroute destination: '{0}', protocol: '{1}', port: '{2}', max_hops: '{3}'"],
    'htk_inet_traceroute_ok'       : ["Traceroute byl úspěšný"],
    'htk_inet_traceroute_nok'      : ["Traceroute byl neúspěšný"],
    'htk_inet_sniffer_started'     : ["Spouštím sniffer output: '{0}', iface: '{1}', filter: '{2}', timeout: '{3}'"],
    'htk_inet_sniffer_stopped'     : ["Sniffer byl zastaven"]            
}