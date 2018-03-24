# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.data.loader.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for loader messages
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

language = {
    'name': 'Čeština',
    'ISO-639-1': 'cs'
}

from hydratk.core import const

HIGHLIGHT_START = chr(27) + chr(91) + "1m"
HIGHLIGHT_US = chr(27) + chr(91) + "4m"
HIGHLIGHT_END = chr(27) + chr(91) + "0m"

msg = {
    'htk_loader_file_not_found': ["Soubor {0} nenalezen"],
    'htk_loader_unknown_extension': ["Neznámá přípona: {0}"]
}
