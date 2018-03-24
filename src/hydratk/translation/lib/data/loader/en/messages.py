# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.data.loader.en.messages
   :platform: Unix
   :synopsis: English language translation loader messages
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

language = {
    'name': 'English',
    'ISO-639-1': 'en'
}

from hydratk.core import const

HIGHLIGHT_START = chr(27) + chr(91) + "1m"
HIGHLIGHT_US = chr(27) + chr(91) + "4m"
HIGHLIGHT_END = chr(27) + chr(91) + "0m"

msg = {
    'htk_loader_file_not_found': ["File {0} not found"],
    'htk_loader_unknown_extension': ["Unknown extension: {0}"]
}
