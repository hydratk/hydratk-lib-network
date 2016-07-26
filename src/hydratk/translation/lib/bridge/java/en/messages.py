# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.bridge.java.en.messages
   :platform: Unix
   :synopsis: English language translation for Java bridge messages
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
    'htk_java_already_started' : ["JVM is already started"],
    'htk_java_restart_tried'   : ["JVM cannot be restarted"],
    'htk_java_starting_jvm'    : ["Starting JVM on path: '{0}', classpath: '{1}', JVM options: '{2}'"],
    'htk_java_started'         : ["JVM was successfully started"],
    'htk_java_not_started'     : ["JVM was not started yet"],
    'htk_java_stopping_jvm'    : ["Stopping JVM"],
    'htk_java_stopped'         : ["JVM was stopped"],
    'htk_java_unknown_type'    : ["Unknown datatype: '{0}'"]
}
