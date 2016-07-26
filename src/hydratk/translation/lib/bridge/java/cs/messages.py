# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.bridge.java.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for Java bridge messages
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
    'htk_java_already_started' : ["JVM je již spuštěno"],
    'htk_java_restart_tried'   : ["JVM není možné restartovat"],
    'htk_java_starting_jvm'    : ["Spouštím JVM na cestě: '{0}', classpath: '{1}', JVM options: '{2}'"],
    'htk_java_started'         : ["JVM bylo úspěšně spuštěno"],
    'htk_java_not_started'     : ["JVM ještě nebylo spuštěno"],
    'htk_java_stopping_jvm'    : ["Zastavuji JVM"],
    'htk_java_stoppped'        : ["JVM bylo zastaveno"],
    'htk_java_unknown_type'    : ["Neznámý datový typ: '{0}'"]
}
